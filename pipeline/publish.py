# pipeline/publish.py
import datetime
import pathlib
import re
import subprocess
import yaml
from config import cfg


def _git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def _has_remote() -> bool:
    result = _git("remote", check=False)
    return bool(result.stdout.strip())


def _rebuild_posts_nav() -> None:
    """Scan docs/posts/*.md and rewrite the Research Digest nav block in mkdocs.yml.
    Also regenerates docs/posts/index.md with a post listing."""
    posts_dir = pathlib.Path("docs/posts")
    posts = sorted(
        [p for p in posts_dir.glob("*.md") if p.name != "index.md"],
        reverse=True,  # newest first
    )

    entries: list[str] = []
    post_meta: list[dict] = []
    for post_file in posts:
        text = post_file.read_text(encoding="utf-8")
        fm: dict = {}
        if text.startswith("---"):
            try:
                end = text.index("---", 3)
                fm = yaml.safe_load(text[3:end]) or {}
            except Exception:
                pass
        title = fm.get("title", post_file.stem)
        date = fm.get("date", "")
        description = fm.get("description", "")
        if isinstance(description, str):
            description = description.strip()
        categories_raw = fm.get("categories", [])
        category = (categories_raw[0] if categories_raw else "").strip().replace('"', "")
        entries.append(f'    - "{title}": posts/{post_file.name}')
        post_meta.append({"title": title, "date": str(date), "description": description, "file": post_file.name, "category": category})

    new_nav = (
        "nav:\n"
        "  - Home: index.md\n"
        "  - Research Digest:\n"
        "    - Overview: posts/index.md\n"
        + "\n".join(entries)
        + "\n  - Weekly Digest: digest/index.md\n"
        "  - Notes: notes/index.md\n"
        "  - Tags: tags.md\n"
    )

    yml_path = pathlib.Path("mkdocs.yml")
    original = yml_path.read_text(encoding="utf-8")
    updated = re.sub(
        r"^nav:(?:\n[ \t]+.*)*",
        new_nav.rstrip("\n"),
        original,
        count=1,
        flags=re.MULTILINE,
    )
    yml_path.write_text(updated, encoding="utf-8")

    # Regenerate docs/posts/index.md with a post listing
    lines = ["---\nhide:\n  - toc\n---\n\n"]
    lines.append("# Research Digest\n\n")
    lines.append("AI-generated summaries of top robotics and ML papers, powered by Gemma 4 running locally.\n\n")
    lines.append("---\n\n")
    for m in post_meta:
        attr = f'{{ data-cat="{m["category"]}" data-date="{m["date"]}" }}'
        lines.append(f'## [{m["title"]}]({m["file"].replace(".md", "/")}){" " + attr}\n\n')
        if m["date"]:
            lines.append(f'*{m["date"]}*\n\n')
        if m["description"]:
            lines.append(f'{m["description"]}\n\n')
    pathlib.Path("docs/posts/index.md").write_text("".join(lines), encoding="utf-8")


def publish(paper: dict, post_content: str, overwrite: bool = False) -> pathlib.Path | None:
    """Write the blog post to docs/posts/ and push to GitHub.

    Returns the written post path, or None if skipped (already exists and not overwriting).
    """
    slug = re.sub(r"[^a-z0-9]+", "-", paper["title"].lower()).strip("-")[:60]
    date = datetime.date.today().isoformat()
    filename = f"{date}-{slug}.md"
    dest = pathlib.Path("docs/posts") / filename

    dest.parent.mkdir(parents=True, exist_ok=True)

    if dest.exists() and not overwrite:
        print(f"  (cached) Post already exists: {dest} — skipping commit")
        return None

    # When overwriting, remove any previous post for this paper (may have a different date prefix)
    if overwrite and paper.get("id"):
        arxiv_id = paper["id"]
        for old_post in dest.parent.glob("*.md"):
            if old_post.name == "index.md" or old_post == dest:
                continue
            try:
                if arxiv_id in old_post.read_text(encoding="utf-8"):
                    old_post.unlink()
                    print(f"  Removed old post: {old_post}")
            except Exception:
                pass

    dest.write_text(post_content, encoding="utf-8")
    print(f"  Written: {dest}")

    _rebuild_posts_nav()
    _git("add", "docs/", "mkdocs.yml")
    _git("commit", "-m", f"feat: new post — {paper['title'][:60]}")
    print(f"  ✅ Post committed locally.")

    if not _has_remote():
        remote_hint = cfg.blog.remote_url or "git@github.com:<username>/<repo>.git"
        print(
            "\n⚠️  No git remote configured — skipping push.\n"
            "  To publish to GitHub Pages, run once:\n"
            "\n"
            f"    git remote add origin {remote_hint}\n"
            "    git push -u origin main\n"
            "\n"
            "  Then future runs will push automatically.\n"
            f"  Post is ready locally at: {dest}"
        )
        return dest

    _git("push")
    site = cfg.blog.site_url
    if site:
        print(f"✅ Live at: {site}/posts/{dest.stem}/")
    else:
        print("✅ Pushed. Check your GitHub Pages URL for the live post.")
    return dest


def publish_digest(content: str) -> None:
    """Write the weekly digest post to docs/digest/posts/ and push to GitHub."""
    today = datetime.date.today()
    week_num = today.strftime("%W")
    filename = f"{today.isoformat()}-weekly-digest-week-{week_num}.md"
    dest = pathlib.Path("docs/digest/posts") / filename

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        print(f"  (cached) Digest already exists: {dest} — skipping commit")
        return
    dest.write_text(content, encoding="utf-8")
    print(f"  Written: {dest}")

    _git("add", "docs/")
    _git("commit", "-m", f"feat: weekly digest — week {week_num}")
    print("  ✅ Digest committed locally.")

    if not _has_remote():
        remote_hint = cfg.blog.remote_url or "git@github.com:<username>/<repo>.git"
        print(
            "\n⚠️  No git remote configured — skipping push.\n"
            "  To publish to GitHub Pages, run once:\n"
            "\n"
            f"    git remote add origin {remote_hint}\n"
            "    git push -u origin main\n"
            "\n"
            "  Then future runs will push automatically.\n"
            f"  Digest is ready locally at: {dest}"
        )
        return

    _git("push")
    site = cfg.blog.site_url
    if site:
        print(f"✅ Digest live at: {site}/posts/weekly-digest-week-{week_num}/")
    else:
        print("✅ Pushed weekly digest.")
