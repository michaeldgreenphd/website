# AGENTS.md

Guidance for AI coding and review agents (Codex, Claude Code, others)
working in this repository. `CLAUDE.md` mirrors this for Claude Code; keep
the two in sync.

## Repository in one paragraph

A static personal website (Michael D. Green, PhD) on GitHub Pages:
`index.html` is a self-contained single page (inline CSS, self-hosted fonts
in `fonts/`, no external scripts); `faq.html` and `published-manuscripts.html`
share `theme.css`; `404.html` forwards old root-level PDF links. A GitHub
Actions workflow (`.github/workflows/update-scholar.yml`) runs twice a day:
`scripts/fetch_scholar.py`, `fetch_substack.py` and `fetch_orcid.py` write
JSON/PNG data files, and `scripts/render_snapshot.py` renders them into
marked blocks in `index.html`, which the workflow then commits.

## Pull requests

- Every pull request must receive a comment containing exactly `@codex review`
  right after it is opened, and again after any push that changes the diff.
- Codex findings are addressed before a PR is considered done: verified
  against the diff, fixed and pushed when real, or answered on the thread
  with a reason when not. Threads that were addressed get resolved.
- Agents do not merge; the owner merges.

## Rules for edits

- Do not hand-edit anything between `<!-- data:NAME -->` and
  `<!-- /data:NAME -->` in `index.html`, nor `scholar_stats.json`,
  `substack_posts.json`, `orcid_works.json`, or `citations_over_time*.png`.
  Change `scripts/render_snapshot.py` or the fetch scripts instead, then run
  the renderer; a second run must be a no-op.
- Keep the page flat and quiet: no animations, no cards or pill tags, no
  third-party scripts, no web-font CDNs, one accent colour. Check light and
  dark themes and a ~390px viewport for any visual change.
- Images carry `width`/`height`, lazy-load below the fold, and use `%20` for
  spaces in paths. New files use lowercase-hyphenated names.
- The CV is linked in two places in `index.html`; the email address lives
  only at the end of `faq.html`; the JSON-LD Person block's role fields track
  the masthead role line.
- `robots.txt` must keep Googlebot and answer-time AI crawlers allowed.

## What a reviewer should look for

- Anything that reaches the page from a data file must be escaped by the
  renderer (`clean()` / `safe_url()` in `scripts/render_snapshot.py`); the
  fetch scripts strip markup before writing JSON. Flag any new path where
  feed text could reach the DOM unescaped or a non-http(s) URL could become a
  link.
- Workflow changes: the checkout uses `persist-credentials: false` and the
  commit step is handed the token explicitly; every fetch/render step has a
  `timeout-minutes` and `continue-on-error: true`; dependencies stay pinned.
- Accessibility and mobile: heading order, link text that names its
  destination, tap targets in the sticky bar, contrast of `--muted` text on
  both backgrounds, `scroll-padding-top` clearance under the sticky bar.
- Determinism: the renderer must not introduce timestamps or ordering that
  changes between runs with identical data.
- Do not flag generated-block content, `%20` paths, or the intentional
  absence of the email address on the homepage.

## Verifying locally

```
python3 -m http.server 8000          # serve, then open http://localhost:8000/
python scripts/render_snapshot.py    # run twice; second run prints "unchanged"
python -m py_compile scripts/*.py
```
