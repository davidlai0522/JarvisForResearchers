# pipeline/notes.py
"""
Publish a hand-written HTML note as a page under docs/notes/ and push to GitHub.

Notes are submitted via the Telegram bot (/note or an .html file upload).
Each note becomes its own page; docs/notes/index.md lists them newest-first.
"""
import datetime
import pathlib
import re
import subprocess

import yaml

from config import cfg


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def _has_remote() -> bool:
    return bool(_git("remote", check=False).stdout.strip())


def _slugify(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")[:60] or "note"


def _rebuild_notes_index() -> None:
    """Regenerate docs/notes/index.md with a listing of all notes, newest first."""
    notes_dir = pathlib.Path("docs/notes")
    notes_dir.mkdir(parents=True, exist_ok=True)
    notes = sorted(
        [p for p in notes_dir.glob("*.md") if p.name != "index.md"],
        reverse=True,
    )

    meta: list[dict] = []
    for note_file in notes:
        text = note_file.read_text(encoding="utf-8")
        fm: dict = {}
        if text.startswith("---"):
            try:
                end = text.index("---", 3)
                fm = yaml.safe_load(text[3:end]) or {}
            except Exception:
                pass
        meta.append({
            "title": str(fm.get("title", note_file.stem)),
            "date": str(fm.get("date", "")),
            "file": note_file.name,
        })

    lines = ["---\nhide:\n  - toc\n---\n\n"]
    lines.append("# Notes\n\n")
    lines.append("Hand-written notes and write-ups.\n\n")
    lines.append("---\n\n")
    if not meta:
        lines.append("*No notes yet. Send one to the Telegram bot with `/note` or an `.html` file.*\n")
    for m in meta:
        lines.append(f'## [{m["title"]}]({m["file"].replace(".md", "/")})\n\n')
        if m["date"]:
            lines.append(f'*{m["date"]}*\n\n')
    (notes_dir / "index.md").write_text("".join(lines), encoding="utf-8")


def publish_note(title: str, html_body: str) -> dict:
    """Write an HTML note page, regenerate the index, commit and push.

    The raw HTML is saved as a static asset under docs/notes/html/ and loaded
    inside an <iframe> on the note's MkDocs page.  This fully isolates the
    note's CSS from the rest of the site.

    Returns {"path": Path, "pushed": bool, "url": str | None}.
    """
    title = title.strip()
    date = datetime.date.today().isoformat()
    stem = f"{date}-{_slugify(title)}"

    # Save the raw HTML as a static asset (copied as-is by MkDocs)
    html_dir = pathlib.Path("docs/notes/html")
    html_dir.mkdir(parents=True, exist_ok=True)
    (html_dir / f"{stem}.html").write_text(html_body.strip(), encoding="utf-8")

    # Write the .md page — just an iframe pointing at the static HTML file.
    # The iframe is same-origin on GitHub Pages so the resize script can read
    # contentDocument.documentElement.scrollHeight without CORS issues.
    dest = pathlib.Path("docs/notes") / f"{stem}.md"
    dest.parent.mkdir(parents=True, exist_ok=True)

    front_matter = yaml.safe_dump(
        {"title": title, "date": date},
        sort_keys=False,
        allow_unicode=True,
    ).strip()

    iframe = (
        f'<iframe src="../html/{stem}.html" '
        f'style="width:100%;border:none;display:block;" '
        f'id="rl-note-frame" scrolling="no"></iframe>\n'
        f'<script>\n'
        f'(function(){{\n'
        f'  var f = document.getElementById("rl-note-frame");\n'
        f'  f.addEventListener("load", function(){{\n'
        f'    try {{ f.style.height = f.contentDocument.documentElement.scrollHeight + "px"; }}\n'
        f'    catch(e) {{ f.style.height = "1200px"; }}\n'
        f'  }});\n'
        f'}})();\n'
        f'</script>\n'
    )

    dest.write_text(f"---\n{front_matter}\n---\n\n{iframe}", encoding="utf-8")

    _rebuild_notes_index()
    _git("add", "docs/notes/")
    _git("commit", "-m", f"feat: new note — {title[:60]}")

    if not _has_remote():
        return {"path": dest, "pushed": False, "url": None}

    _git("push")
    url = f"{cfg.blog.site_url}/notes/{stem}/" if cfg.blog.site_url else None
    return {"path": dest, "pushed": True, "url": url}
