#!/usr/bin/env python3
"""Build a static site in ./_site: every folder gets an index.html listing its contents."""
import html, shutil, sys
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "_site"
SKIP = {".git", ".github", "scripts", "_site"}


def render(title, dirs, files, is_root):
    items = []
    if not is_root:
        items.append('<li><a href="../">&larr; Back</a></li>')
    items += [f'<li>&#128193; <a href="{quote(d)}/">{html.escape(d)}</a></li>' for d in dirs]
    items += [f'<li><a href="{quote(f)}">{html.escape(f)}</a></li>' for f in files]
    return (
        '<!doctype html><html><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1">'
        f"<title>{html.escape(title)}</title>"
        "<style>body{font-family:sans-serif;max-width:40em;margin:2em auto;padding:0 1em}"
        "li{margin:.4em 0}</style></head><body>"
        f"<h1>{html.escape(title)}</h1><ul>{''.join(items)}</ul></body></html>"
    )


def build(src, dst, is_root=False):
    dst.mkdir(parents=True, exist_ok=True)
    dirs, files = [], []
    for p in sorted(src.iterdir(), key=lambda p: p.name.lower()):
        if p.name.startswith(".") or (is_root and p.name in SKIP):
            continue
        if p.is_dir():
            dirs.append(p.name)
            build(p, dst / p.name)
        elif p.name != "index.html" and (not is_root or p.name != "README.md"):
            files.append(p.name)
            shutil.copy2(p, dst / p.name)
        elif p.name == "index.html":
            shutil.copy2(p, dst / p.name)
    if "index.html" not in {p.name for p in src.iterdir()}:
        title = "Documents" if is_root else src.name
        (dst / "index.html").write_text(render(title, dirs, files, is_root), encoding="utf-8")


if __name__ == "__main__":
    if OUT.exists():
        shutil.rmtree(OUT)
    build(ROOT, OUT, is_root=True)
    print(f"Built {OUT}", file=sys.stderr)
