#!/usr/bin/env python3
"""Build a single PDF of the whole tutorial (index + 8 patterns).

Combines every page into one HTML document (ids/links namespaced per page,
Q&A blocks expanded, light theme) and prints it with headless Chrome.
Usage: python3 scripts/build-pdf.py   ->  dist/system-design-patterns.pdf
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
PAGES = [ROOT / "index.html"] + sorted((ROOT / "patterns").glob("[0-9][0-9]-*.html"))


def prefix_for(name: str) -> str:
    m = re.match(r"(\d\d)-", name)
    return f"p{m.group(1)}" if m else "p00"


PREFIX = {p.name: prefix_for(p.name) for p in PAGES}

LINK_RE = re.compile(r'href="(?:\.\./)?(?:patterns/)?([\w-]+\.html)(?:#([^"]*))?"')


def convert(path: Path) -> str:
    html = path.read_text(encoding="utf-8")
    pfx = PREFIX[path.name]
    start = re.search(r'<div class="content[^"]*">', html)
    end = html.index('<div class="pager" data-pager>')
    body = html[start.end():end]

    body = re.sub(r'\bid="([^"]+)"', lambda m: f'id="{pfx}-{m.group(1)}"', body)
    body = re.sub(r'href="#([^"]+)"', lambda m: f'href="#{pfx}-{m.group(1)}"', body)

    def cross(m):
        target = PREFIX.get(m.group(1))
        if not target:
            return m.group(0)
        return f'href="#{target}-{m.group(2) or "top"}"'

    body = LINK_RE.sub(cross, body)
    body = body.replace('<details class="qa">', '<details class="qa" open>')
    return f'<section class="pdf-page" id="{pfx}-top">{body}</section>'


PRINT_CSS = """
@page { size: A4; margin: 16mm 14mm; }
* { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html { scroll-behavior: auto; }
body { background: #fff; font-size: 13px; line-height: 1.6; }
.pdf-page + .pdf-page { break-before: page; }
.hero h1 { break-after: avoid; }
h2, h3, h4 { break-after: avoid; }
figure.diagram, .callout, pre, details.qa, .proscons, tr, .card, .step { break-inside: avoid; }
pre { white-space: pre-wrap; word-break: break-word; overflow: visible; font-size: 12px; }
.table-wrap { overflow: visible; }
table { font-size: 12px; table-layout: auto; }
th, td { overflow-wrap: anywhere; padding: 6px 8px; }
th { white-space: normal; letter-spacing: 0; }
main { padding: 0; }
details.qa summary::before { display: none; }
.content, .content.wide { max-width: none; padding: 0; margin: 0; }
a { text-decoration: none; }
"""


def main() -> int:
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    if not chrome:
        print("Chrome/Chromium not found", file=sys.stderr)
        return 1

    css = (ROOT / "assets" / "style.css").read_text(encoding="utf-8")
    marker = (
        '<svg width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
        '<marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse">'
        '<path class="arrowhead" d="M0 0 L10 5 L0 10 z"/></marker></defs></svg>'
    )
    sections = "\n".join(convert(p) for p in PAGES)
    doc = (
        '<!doctype html><html lang="en" data-theme="light"><head><meta charset="utf-8">'
        "<title>System Design Patterns</title>"
        f"<style>{css}\n{PRINT_CSS}</style></head><body>{marker}"
        f'<div class="shell"><main>{sections}</main></div></body></html>'
    )

    DIST.mkdir(exist_ok=True)
    html_path = DIST / "tutorial.html"
    pdf_path = DIST / "system-design-patterns.pdf"
    html_path.write_text(doc, encoding="utf-8")

    cmd = [
        chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
        "--no-pdf-header-footer", "--generate-pdf-document-outline",
        f"--print-to-pdf={pdf_path}", html_path.as_uri(),
    ]
    subprocess.run(cmd, check=True, capture_output=True)
    print(pdf_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
