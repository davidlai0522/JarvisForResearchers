#!/usr/bin/env python3
"""
JarvisForResearchers Telegram Bot
─────────────────────
Paste an arXiv link in Telegram → get a full blog post generated and saved.

Setup:
  1. cp .env.example .env
  2. Edit .env and set TELEGRAM_BOT_TOKEN=<your token from @BotFather>
  3. uv run python telegram_bot.py

Supported input formats:
  https://arxiv.org/abs/2310.12931
  https://arxiv.org/pdf/2310.12931
  arxiv.org/abs/2310.12931v2
  2310.12931   (bare ID)

Commands:
  /start          — Welcome message
  /help           — Show usage
  /force <ID>     — Run pipeline, skipping the quality gate
  /status         — Show if a pipeline is currently running
  /resources      — Show current CPU / RAM / VRAM headroom
"""
import asyncio
import html
import logging
import os
import pathlib
import re
import subprocess
import sys
from typing import Optional

import yaml

import psutil

# Load .env before anything else
try:
    from dotenv import load_dotenv

    load_dotenv(pathlib.Path(__file__).parent / ".env")
except ImportError:
    pass  # python-dotenv not installed — rely on env vars being set in the shell

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# ── Path setup ────────────────────────────────────────────────────────────────
REPO_ROOT = pathlib.Path(__file__).parent
PIPELINE_DIR = REPO_ROOT / "pipeline"
sys.path.insert(0, str(PIPELINE_DIR))

from config import cfg  # noqa: E402 — must come after sys.path insert

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("jarvisforresearchers.bot")

# ── arXiv ID regex ────────────────────────────────────────────────────────────
# Matches: 2310.12931  2310.12931v2  arxiv.org/abs/2310.12931  arxiv.org/pdf/...
ARXIV_RE = re.compile(
    r"(?:arxiv\.org/(?:abs|pdf)/)?(\d{4}\.\d{4,5}(?:v\d+)?)",
    re.IGNORECASE,
)

# ── Topic presets ─────────────────────────────────────────────────────────────
_TOPIC_PRESETS: dict[str, list[str]] = {
    "robotics": ["cs.RO", "eess.SY", "cs.CV"],
    "ai":       ["cs.AI", "cs.LG", "cs.CV", "cs.NE"],
    "balanced": ["cs.RO", "cs.AI", "cs.LG", "cs.CV"],
}

_PRESET_LABELS = {
    "robotics": "🤖 Robotics  (cs.RO, eess.SY, cs.CV)",
    "ai":       "🧠 AI / ML   (cs.AI, cs.LG, cs.CV, cs.NE)",
    "balanced": "⚖️ Balanced  (cs.RO, cs.AI, cs.LG, cs.CV)",
}

_CONFIG_PATH = REPO_ROOT / "config.yaml"


def _read_current_categories() -> list[str]:
    """Read discovery.categories fresh from config.yaml (bypasses the stale singleton)."""
    if not _CONFIG_PATH.exists():
        return ["cs.RO", "cs.AI", "cs.LG", "cs.CV"]
    raw = yaml.safe_load(_CONFIG_PATH.read_text()) or {}
    return raw.get("discovery", {}).get("categories", ["cs.RO", "cs.AI", "cs.LG", "cs.CV"])


def _write_categories(cats: list[str]) -> None:
    """Replace discovery.categories in config.yaml, preserving all other content and comments."""
    text = _CONFIG_PATH.read_text(encoding="utf-8")
    new_block = "  categories:\n" + "".join(f"  - {c}\n" for c in cats)
    updated = re.sub(
        r"  categories:\n(?:  - [^\n]*\n)*",
        new_block,
        text,
        count=1,
    )
    _CONFIG_PATH.write_text(updated, encoding="utf-8")


# ── Global state ──────────────────────────────────────────────────────────────
# Tracks whether a pipeline subprocess is currently running.
_running_lock = asyncio.Lock()
_running_paper: Optional[str] = None  # arXiv ID currently being processed


# ── Access control ────────────────────────────────────────────────────────────
def _is_allowed(user_id: int) -> bool:
    allowed = cfg.telegram.allowed_user_ids
    return (not allowed) or (user_id in allowed)


def _access_denied_text() -> str:
    return (
        "⛔ Sorry, this bot is restricted to authorised users.\n"
        "Ask the bot owner to add your user ID to `config.yaml → telegram.allowed_user_ids`."
    )


# ── Pipeline runner ───────────────────────────────────────────────────────────
def _find_existing_post(arxiv_id: str) -> Optional[pathlib.Path]:
    """Return the path to an existing blog post containing this arxiv_id, or None."""
    posts_dir = REPO_ROOT / "docs" / "posts"
    if not posts_dir.exists():
        return None
    for post_file in sorted(posts_dir.glob("*.md"), reverse=True):
        if post_file.name == "index.md":
            continue
        try:
            if arxiv_id in post_file.read_text(encoding="utf-8"):
                return post_file
        except Exception:
            continue
    return None


def _list_posts() -> list[dict]:
    """Return [{title, date, arxiv_id, stem}] for all posts, newest first."""
    posts_dir = REPO_ROOT / "docs" / "posts"
    results = []
    if not posts_dir.exists():
        return results
    for post_file in sorted(posts_dir.glob("*.md"), reverse=True):
        if post_file.name == "index.md":
            continue
        try:
            text = post_file.read_text(encoding="utf-8")
            fm: dict = {}
            if text.startswith("---"):
                end = text.index("---", 3)
                fm = yaml.safe_load(text[3:end]) or {}
            m = ARXIV_RE.search(text)
            arxiv_id = m.group(1).split("v")[0] if m else ""
            results.append({
                "title": str(fm.get("title", post_file.stem)),
                "date": str(fm.get("date", ""))[:10],
                "arxiv_id": arxiv_id,
                "stem": post_file.stem,
            })
        except Exception:
            continue
    return results


async def _run_remove(arxiv_id: str) -> str:
    """Run pipeline/run.py --remove as a subprocess. Returns an HTML status message."""
    cmd = [sys.executable, str(PIPELINE_DIR / "run.py"), "--remove", arxiv_id]
    log.info("Spawning remove: %s", " ".join(cmd))
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(REPO_ROOT),
    )
    stdout, _ = await proc.communicate()
    output = stdout.decode(errors="replace")

    if "Nothing found" in output:
        return f"❓ No post found for <code>{arxiv_id}</code>."
    if proc.returncode == 0:
        return f"✅ <b>Removed <code>{arxiv_id}</code></b>\n\nGitHub Pages will update shortly."
    tail = "\n".join(output.strip().splitlines()[-5:])
    return f"💥 <b>Remove failed for <code>{arxiv_id}</code></b>\n\n<pre>{tail[:400]}</pre>"


async def _run_pipeline(arxiv_id: str, force: bool = False, regenerate: bool = False) -> dict:
    """
    Run pipeline/run.py as a subprocess.
    Returns {"success": bool, "output": str, "post_path": str | None}.
    """
    global _running_paper

    cmd = [sys.executable, str(PIPELINE_DIR / "run.py"), "--arxiv", arxiv_id]
    if force:
        cmd.append("--force")
    if regenerate:
        cmd.append("--regenerate")

    log.info("Spawning pipeline: %s", " ".join(cmd))

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
        cwd=str(REPO_ROOT),
    )

    _running_paper = arxiv_id
    stdout, _ = await proc.communicate()
    _running_paper = None

    output = stdout.decode(errors="replace")
    success = proc.returncode == 0

    # Try to find the written post path in the output
    post_path = None
    for line in output.splitlines():
        if "Written:" in line:
            # e.g. "  Written: docs/posts/2026-05-01-some-title.md"
            post_path = line.split("Written:")[-1].strip()
            break

    log.info(
        "Pipeline finished (rc=%d) for %s — post_path=%s",
        proc.returncode,
        arxiv_id,
        post_path,
    )
    return {"success": success, "output": output, "post_path": post_path}


def _resource_snapshot() -> str:
    """Return a human-readable resource summary for /resources."""
    vm = psutil.virtual_memory()
    free_ram = vm.available / 1024**3
    total_ram = vm.total / 1024**3
    cores = psutil.cpu_count(logical=True) or 1
    load_per_core = os.getloadavg()[1] / cores

    ram_ok = free_ram >= cfg.resources.min_free_ram_gib
    cpu_ok = load_per_core <= cfg.resources.max_cpu_load_per_core

    lines = [
        "<b>System resources</b>",
        "",
        f"{'✅' if ram_ok else '❌'} RAM:  {free_ram:.1f} / {total_ram:.0f} GiB free"
        f"  (need >= {cfg.resources.min_free_ram_gib:.0f} GiB)",
        f"{'✅' if cpu_ok else '❌'} CPU:  {load_per_core:.2f} load/core (5-min avg)"
        f"  (limit {cfg.resources.max_cpu_load_per_core:.1f})",
    ]

    try:
        import torch
        if torch.cuda.is_available():
            free_vram = torch.cuda.mem_get_info()[0] / 1024**3
            total_vram = torch.cuda.get_device_properties(0).total_memory / 1024**3
            vram_ok = free_vram >= cfg.resources.min_free_vram_gib_hard
            lines.append(
                f"{'✅' if vram_ok else '❌'} VRAM: {free_vram:.1f} / {total_vram:.0f} GiB free"
                f"  (need >= {cfg.resources.min_free_vram_gib_hard:.0f} GiB)"
            )
        else:
            lines.append("ℹ️ VRAM: no GPU — will run on CPU")
    except Exception:
        lines.append("ℹ️ VRAM: could not read GPU stats")

    all_ok = ram_ok and cpu_ok
    lines += ["", "✅ Ready to run pipeline." if all_ok else "⚠️ Pipeline would be skipped right now."]
    return "\n".join(lines)


def _build_reply(arxiv_id: str, result: dict, force: bool) -> str:
    """Format the Telegram reply message from the pipeline result."""
    output = result["output"]

    # Pipeline was skipped by PipelineGuard due to resource pressure
    if result["success"] and "Run skipped" in output:
        skip_reason = ""
        for line in output.splitlines():
            if "Run skipped" in line:
                skip_reason = line.strip().lstrip("⏭️ ").lstrip()
                break
        return (
            f"⚠️ <b>Run skipped for <code>{arxiv_id}</code></b>\n\n"
            f"<i>{skip_reason}</i>\n\n"
            "The machine is under resource pressure right now.\n"
            "Use /resources to check current headroom, then try again."
        )

    if result["success"]:
        # Extract post title from output if possible
        title_line = ""
        for line in output.splitlines():
            if "feat: new post" in line.lower() or "written:" in line.lower():
                title_line = line.strip()
                break

        url_part = ""
        if result["post_path"]:
            stem = pathlib.Path(result["post_path"]).stem  # "2026-05-01-some-slug"
            if cfg.blog.site_url:
                url_part = f"\n\n🌐 <a href='{cfg.blog.site_url}/posts/{stem}/'>View on GitHub Pages</a>"
            else:
                url_part = f"\n\n📄 Saved to <code>docs/posts/{stem}.md</code>"

        return (
            f"✅ <b>Blog post generated for <code>{arxiv_id}</code>!</b>"
            f"{url_part}"
        )

    # Failed — check for quality rejection
    if "REJECTED" in output:
        rejection_line = ""
        for line in output.splitlines():
            if "REJECTED" in line or "citations" in line.lower() or "threshold" in line.lower():
                rejection_line = line.strip().lstrip("❌ ")
                break
        return (
            f"❌ <b>Quality gate rejected <code>{arxiv_id}</code></b>\n\n"
            f"<i>{rejection_line}</i>\n\n"
            f"💡 To override, reply with:\n"
            f"<code>/force {arxiv_id}</code>"
        )

    # Generic failure — show last few lines of output for debugging
    tail = "\n".join(output.strip().splitlines()[-8:])
    return (
        f"💥 <b>Pipeline failed for <code>{arxiv_id}</code></b>\n\n"
        f"<pre>{html.escape(tail)[:800]}</pre>"
    )


# ── Handlers ──────────────────────────────────────────────────────────────────
async def cmd_start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return
    await update.message.reply_html(
        "👋 <b>Welcome to JarvisForResearchers Bot!</b>\n\n"
        "Send me any arXiv link and I'll generate a full blog post for you.\n\n"
        "<b>Examples:</b>\n"
        "• <code>https://arxiv.org/abs/2310.12931</code>\n"
        "• <code>2310.12931</code>\n\n"
        "Use /help for more options."
    )


async def cmd_help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return
    await update.message.reply_html(
        "<b>JarvisForResearchers Bot — Help</b>\n\n"
        "<b>Send an arXiv link or ID to generate a blog post.</b>\n\n"
        "<b>Commands:</b>\n"
        "• /start — Welcome message\n"
        "• /help — This message\n"
        "• /topics — View or change arXiv topic categories\n"
        "• /force <code>&lt;arxiv_id&gt;</code> — Skip quality gate\n"
        "• /list — Browse and remove existing posts\n"
        "• /remove <code>&lt;arxiv_id&gt;</code> — Remove a post by arXiv ID\n"
        "• /status — Check if pipeline is running\n"
        "• /resources — Show current CPU / RAM / VRAM headroom\n\n"
        "<b>Quality gate:</b>\n"
        "Papers are checked for venue/citation quality before processing.\n"
        "Brand-new preprints (published this year) always pass.\n"
        "Use <code>/force</code> to bypass for any paper."
    )


async def cmd_resources(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return
    await update.message.reply_html(_resource_snapshot())


async def cmd_status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return
    if _running_paper:
        await update.message.reply_html(
            f"⏳ <b>Pipeline running</b>\n\n"
            f"Currently processing: <code>{_running_paper}</code>"
        )
    else:
        await update.message.reply_text("✅ No pipeline running — ready for a new paper!")


async def cmd_force(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return

    args = context.args
    if not args:
        await update.message.reply_html(
            "Usage: <code>/force &lt;arxiv_id&gt;</code>\n"
            "Example: <code>/force 2310.12931</code>"
        )
        return

    arxiv_id_raw = args[0].strip()
    match = ARXIV_RE.search(arxiv_id_raw)
    if not match:
        await update.message.reply_text(
            f"❓ Couldn't parse an arXiv ID from: {arxiv_id_raw!r}"
        )
        return

    arxiv_id = match.group(1).split("v")[0]
    await _process_arxiv(update, arxiv_id, force=True)


async def cmd_list(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return

    posts = _list_posts()
    if not posts:
        await update.message.reply_text("No blog posts yet.")
        return

    rows = []
    no_id_count = 0
    for p in posts:
        date = p["date"] or "?"
        truncated = p["title"][:36] + ("…" if len(p["title"]) > 36 else "")
        label = f"{date} · {truncated} 🗑️"
        if p["arxiv_id"]:
            rows.append([InlineKeyboardButton(label, callback_data=f"del_confirm:{p['arxiv_id']}")])
        else:
            no_id_count += 1

    note = f"\n\n<i>{no_id_count} post(s) have no arXiv ID and must be removed manually.</i>" if no_id_count else ""
    await update.message.reply_html(
        f"📚 <b>Blog Posts ({len(posts)})</b>\n\nTap a post to remove it.{note}",
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def cmd_remove(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return

    args = context.args
    if not args:
        await update.message.reply_html(
            "Usage: <code>/remove &lt;arxiv_id&gt;</code>\n"
            "Example: <code>/remove 2310.12931</code>\n\n"
            "Use /list to browse and remove posts interactively."
        )
        return

    raw = args[0].strip()
    m = ARXIV_RE.search(raw)
    if not m:
        await update.message.reply_text(f"❓ Couldn't parse an arXiv ID from: {raw!r}")
        return

    arxiv_id = m.group(1).split("v")[0]
    existing = _find_existing_post(arxiv_id)
    if not existing:
        await update.message.reply_html(
            f"❓ No blog post found for <code>{arxiv_id}</code>.\n\nUse /list to see all posts."
        )
        return

    posts = _list_posts()
    title = next((p["title"] for p in posts if p["arxiv_id"] == arxiv_id), arxiv_id)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Yes, remove", callback_data=f"del_yes:{arxiv_id}"),
        InlineKeyboardButton("❌ Cancel", callback_data=f"del_no:{arxiv_id}"),
    ]])
    await update.message.reply_html(
        f"🗑️ <b>Remove this post?</b>\n\n"
        f"<i>{title}</i>\n"
        f"arXiv: <code>{arxiv_id}</code>\n\n"
        "This will delete the post and push to GitHub Pages.",
        reply_markup=keyboard,
    )


async def handle_delete_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not _is_allowed(query.from_user.id):
        await query.edit_message_text("⛔ Not authorised.")
        return

    data = query.data or ""

    if data.startswith("del_confirm:"):
        arxiv_id = data[len("del_confirm:"):]
        posts = _list_posts()
        title = next((p["title"] for p in posts if p["arxiv_id"] == arxiv_id), arxiv_id)
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("✅ Yes, remove", callback_data=f"del_yes:{arxiv_id}"),
            InlineKeyboardButton("❌ Cancel", callback_data=f"del_no:{arxiv_id}"),
        ]])
        await query.edit_message_text(
            f"🗑️ <b>Remove this post?</b>\n\n"
            f"<i>{title}</i>\n"
            f"arXiv: <code>{arxiv_id}</code>\n\n"
            "This will delete the post and push to GitHub Pages.",
            parse_mode=ParseMode.HTML,
            reply_markup=keyboard,
        )

    elif data.startswith("del_yes:"):
        arxiv_id = data[len("del_yes:"):]
        await query.edit_message_text(
            f"🗑️ Removing post for <code>{arxiv_id}</code>…",
            parse_mode=ParseMode.HTML,
        )
        result_msg = await _run_remove(arxiv_id)
        await context.bot.send_message(
            chat_id=query.message.chat_id,
            text=result_msg,
            parse_mode=ParseMode.HTML,
        )

    elif data.startswith("del_no:"):
        await query.edit_message_text("👍 Removal cancelled.")


async def cmd_topics(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return

    current = _read_current_categories()
    args = context.args

    # Direct shortcut: /topics robotics  /topics ai  /topics balanced
    if args and args[0].lower() in _TOPIC_PRESETS:
        preset = args[0].lower()
        cats = _TOPIC_PRESETS[preset]
        _write_categories(cats)
        await update.message.reply_html(
            f"✅ <b>Topics set to {_PRESET_LABELS[preset]}</b>\n\n"
            f"Active categories: <code>{', '.join(cats)}</code>\n\n"
            "Takes effect on the next daily run."
        )
        return

    # Show current categories + preset buttons
    rows = [
        [InlineKeyboardButton(_PRESET_LABELS[p], callback_data=f"topics:{p}")]
        for p in _TOPIC_PRESETS
    ]
    await update.message.reply_html(
        f"<b>Current topics:</b> <code>{', '.join(current)}</code>\n\n"
        "Choose a preset, or use a command directly:\n"
        "<code>/topics robotics</code> · <code>/topics ai</code> · <code>/topics balanced</code>",
        reply_markup=InlineKeyboardMarkup(rows),
    )


async def handle_topics_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not _is_allowed(query.from_user.id):
        await query.edit_message_text("⛔ Not authorised.")
        return

    data = query.data or ""
    if not data.startswith("topics:"):
        return

    preset = data[len("topics:"):]
    if preset not in _TOPIC_PRESETS:
        await query.edit_message_text("❓ Unknown preset.")
        return

    cats = _TOPIC_PRESETS[preset]
    _write_categories(cats)
    await query.edit_message_text(
        f"✅ <b>Topics set to {_PRESET_LABELS[preset]}</b>\n\n"
        f"Active categories: <code>{', '.join(cats)}</code>\n\n"
        "Takes effect on the next daily run.",
        parse_mode=ParseMode.HTML,
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not _is_allowed(update.effective_user.id):
        await update.message.reply_text(_access_denied_text())
        return

    text = update.message.text or ""
    match = ARXIV_RE.search(text)
    if not match:
        return  # Not an arXiv link — ignore silently

    arxiv_id = match.group(1).split("v")[0]
    await _process_arxiv(update, arxiv_id, force=False)


async def _process_arxiv(update: Update, arxiv_id: str, force: bool) -> None:
    """Shared logic: acknowledge → run pipeline → reply."""
    global _running_paper

    # Refuse if another paper is already running
    if _running_paper:
        await update.message.reply_html(
            f"⏳ <b>Already processing <code>{_running_paper}</code></b>\n\n"
            "Please wait until the current pipeline finishes, then send your link again."
        )
        return

    # Check for existing post when not forcing
    if not force:
        existing = _find_existing_post(arxiv_id)
        if existing:
            fname = existing.stem
            if cfg.blog.site_url:
                post_ref = f"<a href='{cfg.blog.site_url}/posts/{fname}/'>View existing post</a>"
            else:
                post_ref = f"<code>{existing.relative_to(REPO_ROOT)}</code>"
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("✅ Yes, regenerate", callback_data=f"regen:yes:{arxiv_id}"),
                InlineKeyboardButton("❌ No, keep it", callback_data=f"regen:no:{arxiv_id}"),
            ]])
            await update.message.reply_html(
                f"📄 A blog post for <code>{arxiv_id}</code> already exists.\n\n"
                f"🌐 {post_ref}\n\n"
                "Do you want to regenerate it?",
                reply_markup=keyboard,
            )
            return

    force_note = " (quality gate skipped)" if force else ""
    await update.message.reply_html(
        f"🔍 Found arXiv ID <code>{arxiv_id}</code>{force_note}\n\n"
        "⏳ <b>Starting pipeline…</b>\n"
        "This typically takes 3–10 minutes (model load + inference).\n"
        "I'll reply here when it's done!"
    )

    async with _running_lock:
        result = await _run_pipeline(arxiv_id, force=force)

    reply = _build_reply(arxiv_id, result, force)
    await update.message.reply_html(reply, disable_web_page_preview=False)


async def handle_regenerate_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if not _is_allowed(query.from_user.id):
        await query.edit_message_text("⛔ Not authorised.")
        return

    parts = (query.data or "").split(":", 2)
    if len(parts) != 3 or parts[0] != "regen":
        return

    choice, arxiv_id = parts[1], parts[2]

    if choice == "no":
        await query.edit_message_text(
            f"👍 Keeping the existing post for <code>{arxiv_id}</code>.",
            parse_mode=ParseMode.HTML,
        )
        return

    # Yes — regenerate
    if _running_paper:
        await query.edit_message_text(
            f"⏳ <b>Already processing <code>{_running_paper}</code></b>\n\n"
            "Please wait until the current pipeline finishes, then try again.",
            parse_mode=ParseMode.HTML,
        )
        return

    await query.edit_message_text(
        f"🔄 Regenerating post for <code>{arxiv_id}</code>…\n\n"
        "⏳ <b>Starting pipeline…</b>\n"
        "This typically takes 3–10 minutes (model load + inference).\n"
        "I'll send a new message when it's done!",
        parse_mode=ParseMode.HTML,
    )

    async with _running_lock:
        result = await _run_pipeline(arxiv_id, force=True, regenerate=True)

    reply = _build_reply(arxiv_id, result, force=True)
    await context.bot.send_message(
        chat_id=query.message.chat_id,
        text=reply,
        parse_mode=ParseMode.HTML,
        disable_web_page_preview=False,
    )


# ── Entry point ───────────────────────────────────────────────────────────────
def main() -> None:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        print(
            "❌ TELEGRAM_BOT_TOKEN is not set.\n"
            "   1. Copy .env.example → .env\n"
            "   2. Set TELEGRAM_BOT_TOKEN=<your token> in .env\n"
            "   3. Get a token from @BotFather on Telegram."
        )
        sys.exit(1)

    log.info("Starting JarvisForResearchers Telegram bot (polling mode)…")
    log.info("Allowed users: %s", cfg.telegram.allowed_user_ids or "everyone")

    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("help", cmd_help))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("resources", cmd_resources))
    app.add_handler(CommandHandler("topics", cmd_topics))
    app.add_handler(CommandHandler("force", cmd_force))
    app.add_handler(CommandHandler("list", cmd_list))
    app.add_handler(CommandHandler("remove", cmd_remove))
    app.add_handler(CallbackQueryHandler(handle_topics_callback, pattern=r"^topics:"))
    app.add_handler(CallbackQueryHandler(handle_regenerate_callback, pattern=r"^regen:"))
    app.add_handler(CallbackQueryHandler(handle_delete_callback, pattern=r"^del_"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 JarvisForResearchers bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
