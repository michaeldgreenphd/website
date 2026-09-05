# CLAUDE.md

Instructions for Claude Code sessions working in this repository. `AGENTS.md`
holds the same conventions for other agents; keep the two in sync.

## What this is

The personal website of Michael D. Green, PhD — a flat single page
(`index.html`) plus `faq.html`, `published-manuscripts.html` and `404.html`,
served by GitHub Pages at https://www.michaeldgreen.phd/ (`CNAME`). Pushing
to `main` deploys within a couple of minutes. `README.md` is the owner-facing
guide; keep it accurate when conventions change.

## Pull request workflow — required

1. Branch from `main`, open a pull request against `main`. Never push to
   `main` directly unless the owner explicitly says to.
2. **Immediately after opening the PR, post a comment on it containing
   exactly `@codex review`.** This triggers the Codex reviewer. Do this for
   every PR, without being asked.
3. Watch the PR (subscribe to its activity if the tooling allows) and address
   every Codex finding: verify it against the diff, push a fix for anything
   real, and reply on the thread with a reason when a suggestion should not
   be taken. Resolve the threads you addressed. After pushing changes that
   alter the diff, post `@codex review` again so the new head is reviewed.
4. Keep the PR description accurate as the branch changes. Do not merge the
   PR yourself unless the owner asks; they merge.

## Editing the site

- **Never hand-edit the generated blocks in `index.html`** — everything
  between `<!-- data:NAME -->` and `<!-- /data:NAME -->` (citation metrics,
  the chart, recent posts, the publication list, the ORCID date). They are
  written by `scripts/render_snapshot.py` from `scholar_stats.json`,
  `substack_posts.json` and `orcid_works.json`, which the workflow in
  `.github/workflows/update-scholar.yml` refreshes twice a day. Change the
  script or the data, then run `python scripts/render_snapshot.py`; a second
  run must print "unchanged".
- The data JSON files and `citations_over_time*.png` are generated — do not
  edit them by hand.
- `index.html` is self-contained: inline CSS with its own theme tokens, fonts
  self-hosted from `fonts/`, no external scripts. Do not add Google Fonts,
  analytics, or third-party scripts without the owner asking.
- Keep the site flat and simple: no entrance or scroll animations, no cards,
  no pill tags, nothing that reads as templated. Green (`--ink`) is the only
  accent. Both light and dark themes must be checked for any visual change.
- Images: add `width` and `height` attributes, `loading="lazy"` below the
  fold, and write spaces in paths as `%20`. Prefer lowercase-hyphenated
  names for new files.
- The CV is linked from two places in `index.html` (the header link row and
  the top of the CV section); update both when a new dated PDF is uploaded.
- The email address lives at the end of `faq.html`, not on the homepage.
- The JSON-LD Person block in `<head>` carries `jobTitle`/`affiliation`;
  update it whenever the masthead role line changes.

## Verifying a change

- Serve locally (`python3 -m http.server 8000`) rather than opening the file
  directly, and check at a phone width (~390px) and on desktop, in light and
  dark mode. A Playwright screenshot pass is available in the environment if
  needed.
- Run `python scripts/render_snapshot.py` twice after touching the renderer
  or any data file; `python -m py_compile scripts/*.py` after touching the
  scripts; validate `.github/workflows/update-scholar.yml` with PyYAML after
  touching it.
- The workflow's job runs on pushes that change the pipeline files; a red run
  means a script crashed, while a Google Scholar block is only a warning.

## Conventions

- Commit messages: a short imperative subject and a body that says what
  changed and why. One concern per commit where practical.
- Do not create tags from CI or automation; do not add robots rules that
  block Googlebot.
- Prefer small, verified pushes over speculative ones.
