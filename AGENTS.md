# AGENTS.md

The single source of truth for AI coding and review agents (Codex, Claude
Code, others) working in this repository. `CLAUDE.md` only points here and
adds Claude-Code-specific notes; it repeats no rules, so nothing can drift.
Unfinished and parked work lives in `docs/BACKLOG.md`.

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
- The owner's prose is used verbatim. Do not rewrite copy or headings, add
  emoji, or shift the tone toward marketing.

## Decisions — settled, do not re-propose

Each of these was weighed (most in a 2026-09 seven-lens audit with
adversarial review) and decided. Reopen one only if the owner asks.

- **No entrance or scroll animations.** Added once at the owner's request,
  then removed at the owner's request because text appeared to "fly in".
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
- **The CV keeps its dated filename** (a stable `michael-green-cv.pdf` was
  offered and declined for now); hence the two-link rule above.

## Design system facts

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

- **Font faces that exist** (`fonts/`, latin + latin-ext subsets): Fraunces
  600 upright and 400 italic; DM Sans variable 400–700; IBM Plex Mono 400
  and 500. Any other weight or style renders as a synthetic fallback (a
  Fraunces 700 heading becomes fake-bold). Adding one means adding its
  woff2 files and `@font-face` blocks for both subsets, and a `preload`
  if it is used above the fold. `faq.html` and `published-manuscripts.html`
  still load Google Fonts; the homepage does not.
- Type roles: Fraunces for the name, section headings, publication years
  and italic venues; DM Sans for reading text; IBM Plex Mono for the label
  layer (sticky bar, dates, metrics, captions). The page column is 46rem;
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
- **Headshot assets** derive from `images/Fall 2025 Headshot.JPG`:
  `headshot-408.jpg` (page, 408×570), `headshot-icon.png` (256px square,
  link previews), `favicon-64.png`, `apple-touch-icon.png` (180px). When
  the photo changes, regenerate all four (Pillow; square crop biased toward
  the face) and update the JSON-LD `image`.

## Pipeline facts

- Schedule: 06:05 and 17:35 UTC daily, plus pushes that touch the pipeline
  files listed under `on.push.paths` in the workflow — **add any new script
  to that list** or it will not get a test run.
- Scholar fetch: four attempts of 90 seconds each (direct, then free-proxy
  rotation), each in a subprocess that is killed on timeout. A Google block
  ends in a `::warning::` and keeps the cached numbers — routine, not a
  failure. A red run means a script crashed or the render step failed and
  should be looked at.
- `CHART_STYLE_VERSION` in `scripts/fetch_scholar.py` must be bumped
  whenever the chart's palette or styling changes; otherwise the PNGs are
  only re-rendered when the data changes.
- Substack keeps its cached posts on a transient failure but fails loudly
  when the cache is older than 30 days. ORCID keeps its cache on failure.
- Feed text is cleaned at fetch time (tags stripped, entities decoded) and
  escaped again by the renderer on output; links are emitted only for
  http(s) URLs. Keep both layers.
- Pins are deliberate: `scholarly==1.7.11` (parser), `free-proxy==1.0.6`
  and `httpx<0.28` (known breakages), `matplotlib` to the last green run's
  version. Bump on purpose, one at a time, and watch the next run.
- The workflow checks out with `persist-credentials: false` and the commit
  step is handed the token explicitly; pushing a branch that touches
  pipeline files runs the workflow on that branch, and the bot may commit
  rendered data there — sync the branch rather than fighting it.
- Verify a deploy by the "pages build and deployment" run for the commit,
  not by fetching the site.

## Remote-environment gotchas

Learned in Claude Code cloud sessions; other sandboxes may match.

- The git proxy refuses tag pushes (HTTP 403). Reference archived states
  by commit permalink instead of tags.
- Outbound fetches to `www.michaeldgreen.phd` are blocked by the network
  policy; see the deploy-verification note above.
- Google Fonts is unreachable, so screenshots of the two pages that still
  use it show fallback type; the homepage's self-hosted fonts render.
- Bare headless Chromium enforces a minimum window width and crops; use
  Playwright (available in the environment) for ~390px viewports, and
  force `loading="lazy"` images eager before screenshotting below the fold.
- The GitHub MCP connection can drop and reconnect mid-session; reload the
  tools rather than assuming they are gone.

## What a reviewer should look for

- Anything that reaches the page from a data file must be escaped by the
  renderer (`clean()` / `safe_url()` in `scripts/render_snapshot.py`); the
  fetch scripts strip markup before writing JSON. Flag any new path where
  feed text could reach the DOM unescaped or a non-http(s) URL could become a
  link.
- Workflow changes: the checkout uses `persist-credentials: false` and the
  commit step is handed the token explicitly; every fetch/render step has a
  `timeout-minutes` and `continue-on-error: true`; dependencies stay pinned;
  a new script appears in `on.push.paths`.
- Accessibility and mobile: heading order, link text that names its
  destination, tap targets in the sticky bar, contrast of `--muted` text on
  both backgrounds, `scroll-padding-top` clearance under the sticky bar.
- Determinism: the renderer must not introduce timestamps or ordering that
  changes between runs with identical data.
- Any CSS that names a font weight or style not listed above, or a colour
  not in the token table.
- Do not flag generated-block content, `%20` paths, the intentional absence
  of the email address on the homepage, the curated lists, or the
  deliberate look-like-bugs listed under Design system facts.

## Verifying a change

```
python3 -m http.server 8000          # serve, then open http://localhost:8000/
python scripts/render_snapshot.py    # run twice; second run prints "unchanged"
python -m py_compile scripts/*.py    # after touching any script
```

Serve locally rather than opening the file directly, and check at a phone
width (~390px) and on desktop, in light and dark mode. Validate
`.github/workflows/update-scholar.yml` with PyYAML after touching it.

## Conventions

- Commit messages: a short imperative subject and a body that says what
  changed and why. One concern per commit where practical.
- Prefer small, verified pushes over speculative ones.
