# CLAUDE.md

Static tutorial site: 8 system design patterns, one HTML page each, plus `index.html`. No build step, no dependencies for the site itself. See `README.md` for the content overview.

## Layout

- `index.html`, `patterns/01…08-*.html`: content pages. Each loads `assets/style.css` and `assets/main.js`.
- `assets/main.js` injects the topbar, sidebar, "on this page" TOC, prev/next pager and the shared SVG `#arrow` marker. Pages only contain content; they declare `<body data-page="NN" data-root="../">` (`data-page="index" data-root=""` for the index).
- The `PATTERNS` list in `main.js` drives navigation. Adding or renaming a pattern page means updating it, `index.html` cards, `README.md`, and the page's `data-page` id.
- Diagrams are inline SVG using the classes in `style.css` (`n-*` nodes, `t-*` text, `l-*` lines, `marker-end="url(#arrow)"`). Colors come from CSS variables so light/dark both work. Don't hardcode colors.
- Every pattern page keeps the same section order (TL;DR, problem, when it comes up, solutions, trade-offs, technologies, when not to use, interview script, Q&A, related). Heading `id`s are linked from other pages (e.g. `05-long-running-tasks.html#messaging-models`), so don't rename them casually.

## Deploy

`.github/workflows/pages.yml` publishes on every push to `main`, copying only `index.html`, `assets/` and `patterns/` into the site. Anything else in the repo (scripts, README, this file) is not published. Pushing to `main` deploys, so confirm before pushing.

## PDF export

`python3 scripts/build-pdf.py` builds one combined PDF of the whole tutorial at `dist/system-design-patterns.pdf` (git-ignored). Requires Chrome/Chromium and Python 3 stdlib only.

It extracts each page's `<div class="content">` (everything before `<div class="pager" data-pager>`), namespaces ids and links per page (`pNN-…`), opens all `<details class="qa">`, forces the light theme, and prints with headless Chrome. It does not run `main.js`.

Rerun it after content changes. If you add a new kind of element that depends on `main.js`, collapses, scrolls (`overflow-x`), or uses `white-space: nowrap`, check it in print layout. A single overflowing element makes Chrome shrink the whole PDF to fit. When changing the script, check `document.documentElement.scrollWidth` stays within the page width (about 688px) with print media emulated.

## Conventions

- Plain HTML/CSS/JS, no frameworks or bundlers. Keep it that way.
- Figures (throughput, limits, timeouts) are approximate and hedged in the text; keep that tone.
- Conventional Commits for messages (`feat:`, `docs:`, `build:`, `ci:`).
