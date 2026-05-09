"""
Push a Telegram notification from the pipeline without requiring the bot process.
Uses only stdlib (urllib) so it works from cron with no extra deps.
"""
import json
import logging
import os
import pathlib
import urllib.error
import urllib.request

log = logging.getLogger(__name__)


def _load_token() -> str:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        # Try loading from .env in the repo root
        env_file = pathlib.Path(__file__).parent.parent / ".env"
        if env_file.exists():
            for line in env_file.read_text().splitlines():
                line = line.strip()
                if line.startswith("TELEGRAM_BOT_TOKEN="):
                    token = line.split("=", 1)[1].strip().strip('"').strip("'")
                    break
    return token


def send(text: str) -> bool:
    """Send an HTML Telegram message to notify_chat_id. Returns True on success."""
    from config import cfg

    chat_id = cfg.telegram.notify_chat_id
    if not chat_id:
        return False

    token = _load_token()
    if not token:
        log.warning("Telegram notify skipped — TELEGRAM_BOT_TOKEN not set")
        return False

    payload = json.dumps({
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": False,
    }).encode()

    req = urllib.request.Request(
        f"https://api.telegram.org/bot{token}/sendMessage",
        data=payload,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=10):
            return True
    except urllib.error.URLError as exc:
        log.warning("Telegram notify failed: %s", exc)
        return False


def notify_daily(paper: dict, post_dest=None) -> None:
    """Send a 'daily paper posted' notification for the given paper dict."""
    import pathlib
    from config import cfg

    title = paper.get("title", "Unknown title")
    arxiv_id = paper.get("id", "")

    url_part = ""
    if post_dest is not None:
        stem = pathlib.Path(post_dest).stem
        if cfg.blog.site_url:
            url_part = f"\n\n🌐 <a href='{cfg.blog.site_url}/posts/{stem}/'>View on GitHub Pages</a>"
        else:
            url_part = f"\n\n📄 Saved to <code>docs/posts/{stem}.md</code>"

    text = (
        f"📰 <b>Daily paper posted!</b>\n\n"
        f"<b>{title}</b>\n"
        f"arXiv: <code>{arxiv_id}</code>"
        f"{url_part}"
    )
    if send(text):
        print("  📲 Telegram notification sent.")
    else:
        print("  ℹ️  Telegram notification skipped (notify_chat_id not configured).")
