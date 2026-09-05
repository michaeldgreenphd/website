# AGENTS.md

The single source of truth for AI coding and review agents (Codex, Claude
Code, others) working in this repository. `CLAUDE.md` only points here and
adds Claude-Code-specific notes; it repeats no rules, so nothing can drift.

## Repository in one paragraph

A static personal website (Michael D. Green, PhD) on GitHub Pages at
https://www.michaeldgreen.phd/ (`CNAME`): `index.html` is a self-contained
single page (inline CSS, self-hosted fonts in `fonts/`, no external scripts);
`faq.html` and `published-manuscripts.html` share `theme.css`; `404.html`
forwards old root-level PDF links. A GitHub Actions workflow
(`.github/workflows/update-scholar.yml`) runs twice a day:
`scripts/fetch_scholar.py`, `fetch_substack.py` and `fetch_orcid.py` write
JSON/PNG data files, and `scripts/render_snapshot.py` renders them into
marked blocks in `index.html`, which the workflow then commits. Pushing to
`main` deploys within a couple of minutes. `README.md` is the owner-facing
guide; keep it accurate when conventions change.

## Pull request workflow — required

1. Branch from `main` and open a pull request against `main`. Never push to
   `main` directly unless the owner explicitly says to.
2. **Immediately after opening the PR, post a comment on it containing
   exactly `@codex review`.** Do this for every PR, without being asked, and
   again after any push that changes the diff so the new head is reviewed.
3. Address every Codex finding before the PR is considered done: verify it
   against the diff, push a fix for anything real, and reply on the thread
   with a reason when a suggestion should not be taken. Resolve the threads
   you addressed.
4. Keep the PR title and description accurate as the branch changes.
5. Agents do not merge; the owner merges.

## Rules for edits

- **Never hand-edit the generated blocks in `index.html`** — everything
  between `<!-- data:NAME -->` and `<!-- /data:NAME -->` (citation metrics,
  the chart, recent posts, the publication list, the ORCID date) — nor
  `scholar_stats.json`, `substack_posts.json`, `orcid_works.json`, or
  `citations_over_time*.png`. Change `scripts/render_snapshot.py` or the
  fetch scripts instead, then run the renderer; a second run must print
  "unchanged".
- Keep the site flat and quiet: no entrance or scroll animations, no cards
  or pill tags, no third-party scripts, no analytics, no web-font CDNs.
  Green (`--ink`) is the only accent. Check light and dark themes and a
  ~390px viewport for any visual change.
- Images carry `width` and `height` attributes, `loading="lazy"` below the
  fold, and use `%20` for spaces in paths. New files use
  lowercase-hyphenated names.
- The CV is linked from two places in `index.html` (the header link row and
  the top of the CV section); update both when a new dated PDF is uploaded.
- The email address lives only at the end of `faq.html`, not on the homepage.
- The JSON-LD Person block in `<head>` carries `jobTitle`/`affiliation`;
  update it whenever the masthead role line changes.
- `robots.txt` must keep Googlebot and the answer-time AI crawlers allowed;
  only training/bulk-scraping agents are disallowed. Never add `noindex` or
  `nosnippet` to the homepage.
- Do not create tags or releases from CI or automation.

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

## Verifying a change

```
python3 -m http.server 8000          # serve, then open http://localhost:8000/
python scripts/render_snapshot.py    # run twice; second run prints "unchanged"
python -m py_compile scripts/*.py    # after touching any script
```

Serve locally rather than opening the file directly, and check at a phone
width (~390px) and on desktop, in light and dark mode. Validate
`.github/workflows/update-scholar.yml` with PyYAML after touching it. The
workflow runs on pushes that change the pipeline files; a red run means a
script crashed, while a Google Scholar block is only a warning.

## Conventions

- Commit messages: a short imperative subject and a body that says what
  changed and why. One concern per commit where practical.
- Prefer small, verified pushes over speculative ones.
