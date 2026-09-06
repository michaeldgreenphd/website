# AGENTS.md

Read by both Claude Code (imported by `CLAUDE.md`) and Codex reviewers
(loaded directly). It must stay tool-neutral: nothing here may assume a
particular agent, tool, or sandbox. Claude-Code-specific notes live in
`CLAUDE.md`; parked work in `docs/BACKLOG.md`. Directory-level facts live
in `scripts/AGENTS.md`, `.github/workflows/AGENTS.md` and
`images/AGENTS.md`, next to the files they govern.

## Repository in one paragraph

A static personal website (Michael D. Green, PhD) on GitHub Pages at
https://www.michaeldgreen.phd/ (`CNAME`): `index.html` is a self-contained
single page (inline CSS, self-hosted fonts in `fonts/`, no external
scripts); `faq.html` and `published-manuscripts.html` share `theme.css`;
`404.html` forwards old root-level PDF links. A GitHub Actions workflow
(`.github/workflows/update-scholar.yml`) runs twice a day: the three
`scripts/fetch_*.py` scripts write JSON/PNG data files and
`scripts/render_snapshot.py` renders them into marked blocks in
`index.html`, which the workflow then commits. Pushing to `main` deploys
within a couple of minutes.

## Pull request workflow — required

1. Branch from `main` and open a pull request against `main`. Never push to
   `main` directly unless the owner explicitly says to.
2. **Immediately after opening the PR, post a comment on it containing
   exactly `@codex review`.** Do this for every PR, without being asked, and
   again after any push that changes the diff so the new head is reviewed.
3. Address every Codex finding before the PR is considered done: verify it
   against the diff, push a fix for anything real, and reply on the thread
   saying what changed. Resolve the threads you addressed.
4. **Ask before disputing.** When a finding is unclear, or looks wrong,
   do not argue with it or ignore it — post a comment addressed to
   `@codex` with the specific question (what it expects, or why it thinks
   the current code is wrong), then act on the answer: fix, or reply with
   the reason it should not be taken. Codex answers direct questions; it
   does not respond to ordinary thread replies.
5. **One editor per branch.** Never use `@codex address that feedback`, or
   otherwise ask Codex to push commits, while an agent or session is
   working on the branch — two editors on one branch produce conflicting
   commits. Asking Codex questions is fine at any time.
6. Keep the PR title and description accurate as the branch changes.
7. Agents do not merge; the owner merges.

## Rules for edits

- **Never hand-edit the generated blocks in `index.html`** — everything
  between `<!-- data:NAME -->` and `<!-- /data:NAME -->` (citation metrics,
  the chart, recent posts, the publication list, the ORCID date) — nor
  `scholar_stats.json`, `substack_posts.json`, `orcid_works.json`, or
  `citations_over_time*.png`. Change `scripts/render_snapshot.py` or the
  fetch scripts instead, then run the renderer; a second run must print
  "unchanged".
- Keep the homepage flat and quiet: no entrance or scroll animations, no
  cards or pill tags, no third-party scripts, no web-font CDN. Green
  (`--ink`) is the only accent. (`faq.html` and `published-manuscripts.html`
  still load Google Fonts; self-hosting them is a backlog item, not a rule
  violation.)
- Images carry `width` and `height` attributes, `loading="lazy"` below the
  fold, and use `%20` for spaces in paths. New **asset** files (images,
  PDFs, fonts) use lowercase-hyphenated names. Markdown documentation
  follows the repository's existing uppercase convention (`README.md`,
  `AGENTS.md`, `docs/SCHOLAR_PIPELINE.md`, `docs/BACKLOG.md`).
- The CV keeps its dated filename (a stable name was offered and declined)
  and is linked from two places in `index.html` (the header link row and
  the top of the CV section); update both when a new PDF is uploaded.
- The email address lives only at the end of `faq.html`, not on the homepage.
- The JSON-LD Person block in `<head>` carries `jobTitle`/`affiliation`;
  update it whenever the masthead role line changes.
- `robots.txt` must keep Googlebot and the answer-time AI crawlers allowed;
  only training/bulk-scraping agents are disallowed. Never add `noindex` or
  `nosnippet` to the homepage.
- The owner's prose is used verbatim. Do not rewrite copy or headings, add
  emoji, or shift the tone toward marketing.
- `README.md` is the owner-facing guide; update it when a convention here
  changes.

## Decisions — settled, do not re-propose

Each of these was weighed (most in a 2026-09 seven-lens audit with
adversarial review) and decided. Reopen one only if the owner asks.

- **No entrance or scroll animations** (added once, then removed at the
  owner's request because text appeared to "fly in").
- **No Content-Security-Policy meta tag.** On a site reviewed from a phone,
  CSP violations fail silently (an embed or image just vanishes); escaping
  feed text in the renderer is the real fix and is done.
- **No email obfuscation, contact form, or analytics.** The address is
  public in the CV and on ORCID anyway; friction is applied by placement
  (end of the FAQ) and, if ever wanted, a subject-line token — see the
  backlog.
- **No "smarter" sanity guard on Scholar numbers.** A never-lower or
  percentage rule would wedge the pipeline on legitimate citation drops
  (they happen when Scholar merges duplicates). The existing refusal of an
  empty or zero payload is the right guard, and it fails loudly.
- **The tabbed site, hero action buttons, and heritage background pattern
  are retired for good.** The last tabbed version is at commit `60bd128`
  (`tabbed-site.html`); the vine border around the headshot is the one
  decorative element kept.
- **Curated content is hand-picked and never regenerated from data**: the
  co-author line (seven names, chosen by the owner), "Select Service and
  Awards", "Select Media Appearances", and the omission of conference
  abstracts and posters from Publications. A reviewer should not flag
  these as incomplete; an agent should not "complete" them.
- **Publications sit at the bottom of the page and stay collapsed**; the
  section order (about, research, for fun, cv, media, contact,
  publications) is the owner's.

## Design system facts

These govern `index.html`, `theme.css`, `faq.html` and
`published-manuscripts.html`, which all sit at the repository root, so
they stay in this file.

Tokens live in `index.html` in three blocks — `:root` (light),
`@media (prefers-color-scheme: dark)` scoped to `:root:not([data-theme="light"])`,
and `:root[data-theme="dark"]` — and a new token must be added to all three.

| Token      | Light     | Dark      | Note                                   |
|------------|-----------|-----------|----------------------------------------|
| `--ink`    | `#1E5B40` | `#4FB784` | the only accent                        |
| `--bg`     | `#F4F6F2` | `#0F1E18` |                                        |
| `--text`   | `#16211C` | `#EDF2EE` |                                        |
| `--text-2` | `#566159` | `#B4C3B9` | supporting copy                        |
| `--muted`  | `#5F6C64` | `#869187` | ≥ 4.5:1 on `--bg`; do not lighten      |
| `--line`   | `#DBE2DC` | `#294034` | hairlines                              |
| `--tint`   | `rgba(30, 91, 64, 0.06)` | `rgba(79, 183, 132, 0.12)` | faint green wash: row separators in `ul.rows` |

These seven are the complete set of **theme tokens**; the only other custom
properties are the three font stacks (`--serif`, `--sans`, `--mono`). Three
functional colours in `index.html` deliberately sit outside the tokens and
are not to be flagged or "tokenised": `::selection` uses a fixed
`rgba(62, 158, 108, 0.28)` highlight in both themes; the Substack
`.embed-frame` keeps `background: #fff` (see below); and the `#000` in the
sticky bar's `mask-image` gradient is an alpha mask, not a rendered colour.
Derived values via `color-mix()` on a token are fine. `theme.css` (the two
secondary pages only) uses its own `--color-*` names for the same values.

- **Font faces that exist** (`fonts/`, latin + latin-ext subsets, weight in
  the filename where a family has more than one): Fraunces 600 upright and
  400 italic; DM Sans variable 400–700; IBM Plex Mono 400 and 500 as two
  static faces. Any other weight or style renders as a synthetic fallback
  (a Fraunces 700 heading becomes fake-bold). Adding one means adding its
  woff2 files and `@font-face` blocks for both subsets, and a `preload` if
  it is used above the fold. This inventory is the **homepage's only**:
  `faq.html` and `published-manuscripts.html` load Google Fonts with a
  wider set — Fraunces 500/600/700 upright, DM Sans 400/500/700, IBM Plex
  Mono 400/500/600, no italics — so those weights are valid there and
  nothing more.
- Type roles: Fraunces for the name, section headings, publication years
  and italic venues; DM Sans for reading text; IBM Plex Mono for the label
  layer (sticky bar, dates, metrics, captions) at 400, with 500 reserved
  for the publications fold's summary line. The page column is 46rem;
  paragraphs are capped at 42rem.
- **Deliberate things that look like bugs — leave them**: the Substack
  iframe keeps `background: #fff` (its form text would vanish on the dark
  page); the Spotify iframe is transparent and borderless and drops to
  152px on phones (its compact card); `color-scheme` is never declared (it
  paints an opaque canvas behind both iframes); on phones the sticky bar's
  link row scrolls sideways with a fade as the cue (wrapping is the
  fallback if the owner dislikes it); photos are dimmed to 88% brightness
  in dark mode; the publications' year labels hang in the left margin only
  at viewports of 60rem and up.

## What a reviewer should look for

- Anything that reaches the page from a data file must be escaped by the
  renderer (`clean()` / `safe_url()` in `scripts/render_snapshot.py`); the
  fetch scripts strip markup before writing JSON. Flag any new path where
  feed text could reach the DOM unescaped or a non-http(s) URL could become a
  link.
- Workflow changes: the checkout uses `persist-credentials: false` and the
  commit step is handed the token explicitly; every fetch/render step has a
  `timeout-minutes` and `continue-on-error: true`; dependencies stay pinned;
  a new script appears in `on.push.paths`; no tags or releases are created
  from CI.
- Accessibility and mobile: heading order, link text that names its
  destination, tap targets in the sticky bar, contrast of `--muted` text on
  both backgrounds, `scroll-padding-top` clearance under the sticky bar.
- Determinism: the renderer must not introduce timestamps or ordering that
  changes between runs with identical data.
- In `index.html`: any CSS that names a font weight or style not in the
  self-hosted inventory above, or a new theme colour that is not a token
  (or `color-mix()` of one) — the three functional exceptions documented
  under Design system facts are fine. For `faq.html` and
  `published-manuscripts.html`, check weights against their Google Fonts
  set instead.
- Do not flag generated-block content, `%20` paths, the intentional absence
  of the email address on the homepage, the curated lists, or the
  deliberate look-like-bugs listed under Design system facts.

## Verifying a change

```
python3 -m http.server 8000          # serve, then open http://localhost:8000/
python scripts/render_snapshot.py    # run twice; second run prints "unchanged"
python -m py_compile scripts/*.py    # after touching any script
```

Serve locally rather than opening the file directly, and check any visual
change at a phone width (~390px) and on desktop, in light and dark mode.
Validate `.github/workflows/update-scholar.yml` with PyYAML after touching
it. Verify a deploy by the "pages build and deployment" run for the commit,
not by fetching the site.

## Conventions

- Commit messages: a short imperative subject and a body that says what
  changed and why. One concern per commit where practical.
