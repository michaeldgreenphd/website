# Claude Code configuration audit — `michaeldgreenphd/website`

Date: 2026-09-06. Mode: read-only (this report is the only file written).
Environment audited: the Claude Code cloud container for this repository;
user-level paths are `/root/.claude/`. Token counts are estimates
(characters ÷ 4); `/context` is not available as a tool in this session.

## Headline findings

1. **`AGENTS.md`, the declared single source of truth, is not loaded
   automatically.** Claude Code loads `CLAUDE.md`; it does not load
   `AGENTS.md`. `CLAUDE.md` says "Read `AGENTS.md` first" in prose, which
   works only if the model chooses to spend a tool call on it. In this
   session the injected instructions contained `CLAUDE.md` alone. A one-line
   `@AGENTS.md` import makes the load unconditional.
2. **No other configuration exists.** No `.claude/` directory, no rules, no
   settings, no hooks, no project skills, no commands, no agents, no auto
   memory. Everything rides on two Markdown files, and every "must" in them
   is followed by convention rather than enforced.
3. **One fact in `AGENTS.md` is wrong**: it says IBM Plex Mono exists at
   400 and 500. Both `fonts/ibm-plex-mono-*.woff2` files are the static
   **500** face; the `@font-face` block declared as 400 points at the same
   500 file, so "regular" mono text on the homepage renders at medium.
4. **One environment gotcha is stale**: "Google Fonts is unreachable" —
   `fonts.googleapis.com` answered 200 from this container today.
5. **Two sections of `AGENTS.md` duplicate each other** (feed-text escaping
   and the workflow credential rule appear under both *Pipeline facts* and
   *What a reviewer should look for*), and three items duplicate
   `CLAUDE.md`, contradicting `CLAUDE.md`'s own "nothing repeated here".
6. **Always-on cost is misleadingly low.** Nominally ~250 tokens
   (`CLAUDE.md`); in practice ~3,850 tokens plus one tool call in every
   session that follows the pointer, and 0 rules loaded in any session that
   does not.

---

## 1. Inventory

### 1a. Instruction files

| File | Exists | Loads? | Lines | ~Tokens | Notes |
|---|---|---|---|---|---|
| `~/.claude/CLAUDE.md` | no | — | — | — | No user-level instructions. |
| `./CLAUDE.md` | yes | **yes, always** | 19 | ~250 | Pointer to `AGENTS.md` + 3 Claude-specific bullets. No `@`-imports. |
| `./.claude/CLAUDE.md` | no | — | — | — | |
| `./CLAUDE.local.md` | no | — | — | — | |
| `./AGENTS.md` | yes | **no — not auto-loaded** | 248 | ~3,600 | Loaded only if the model obeys the prose pointer (one `Read` call). Codex reads it by its own convention. |
| `./README.md` | yes | no (on demand) | 79 | ~1,050 | Owner-facing. Duplicates six rules from `AGENTS.md` (see §2). Accurate as of today. |
| `./docs/BACKLOG.md` | yes | no (on demand) | 99 | ~1,350 | Referenced by `AGENTS.md`. |
| `./docs/SCHOLAR_PIPELINE.md` | yes | no | 47 | ~550 | **Stale**: still says "dashboard on the Research tab". Referenced by `README.md` and a comment in `fetch_scholar.py`. |
| `./docs/UPLOADING_FILES_GUIDE.md` | yes | no | 72 | ~830 | |
| `./docs/GITHUB_PAGES_SETUP.md` | yes | no | 165 | ~1,060 | Squarespace DNS; flagged in backlog. |

`@`-imports: none in any file. Broken imports: none (there are none to break).

### 1b. Rules

| Location | Result |
|---|---|
| `.claude/rules/*.md` | directory does not exist |
| `~/.claude/rules/*.md` | directory does not exist |

Nothing is paths-scoped; nothing loads unconditionally either.

### 1c. Auto memory

`~/.claude/projects/-home-user-website/` contains only the session
transcript, `subagents/`, `tool-results/` and `workflows/`. There is **no
`memory/` directory and no `MEMORY.md`**. Nothing persists between sessions
except what is committed to the repository.

### 1d. Skills, commands, agents

| Location | Contents |
|---|---|
| `.claude/skills/` | none |
| `.claude/commands/` | none |
| `.claude/agents/` | none |
| `~/.claude/commands/`, `~/.claude/agents/` | none |
| `~/.claude/skills/session-start-hook/` | platform-provided (1 file, ~1,230 tokens body). Frontmatter `name: startup-hook-skill` differs from its directory name; listed as `session-start-hook`. Harmless. |
| `~/.claude/skills/synced/<id>/` | 9 account-synced skills (208 files): `aact-baseline-extraction`, `docx`, `import-memory`, `morning`, `pdf`, `pptx`, `skill-creator`, `tracked-docx-manuscript-editing`, `xlsx`. Descriptions load always (~1,360 tokens in total); bodies load on invocation. None is specific to this repository. |

### 1e. Settings, hooks, MCP

| File | Exists | Contents |
|---|---|---|
| `.claude/settings.json` | no | — |
| `.claude/settings.local.json` | no | — |
| `~/.claude/settings.json` | no | — |
| `.mcp.json` | no | — |
| `~/.claude/launcher-settings.json` | yes (platform) | `SessionStart` → `session-start-git-identity.sh` (pins committer identity so SSH-signed commits verify); `Stop` → `stop-hook-git-check.sh` (warns about uncommitted/unpushed work); `permissions.allow: ["Skill"]`. Not user-editable; not project config. |

MCP servers come from the cloud session (GitHub, Google Drive,
Claude Code Remote), not from any file in this repository.

### 1f. Files that exist but do NOT load

| File | Why it does not load | Severity |
|---|---|---|
| `AGENTS.md` | Not a Claude Code instruction file and not `@`-imported. Loads only if the pointer sentence is obeyed. | **High** — this is the file with every rule in it. |
| `docs/*.md`, `README.md` | Documentation, correctly not loaded. | none |

`.gitignore` contains only `__pycache__/` and `*.pyc`, so a future
`.claude/settings.local.json` would be committed unless ignored.

### 1g. Always-on token cost

| Scenario | Tokens | Tool calls |
|---|---|---|
| Today, model ignores the pointer | ~250 | 0 (and zero rules in effect) |
| Today, model follows the pointer | ~3,850 | 1 |
| Account-level skill descriptions (outside this repo's control) | ~1,360 + built-ins | — |

---

## 2. Line-level audit of instruction files

Columns: **Changes** = what I would do differently without the line.
**Test** = a one-line prompt that would reveal whether the rule was followed
(or "not testable" + rewrite). **Dup/contra** = duplicate or contradiction
with any other loaded file, `README.md`, or a skill description.
**True?** = verified against the code today.

### 2a. `CLAUDE.md`

| # | Line | Rule | Changes | Test | Dup/contra | True? | Verdict |
|---|---|---|---|---|---|---|---|
| C1 | 3–8 | Read `AGENTS.md` first; it is the single source of truth; nothing repeated here | I read `AGENTS.md` before working (one tool call) | "What is step 5 of the PR workflow?" — unanswerable without the file | "Nothing repeated here" is false: C3 duplicates AGENTS L200–202 | partly | **rewrite** → `@AGENTS.md` import; drop the claim of non-repetition and make it true |
| C2 | 12–14 | After opening a PR, `subscribe_pr_activity` and schedule an hourly `send_later` until merged/closed | I would open the PR and stop | "Open a PR for this change" → check for the subscribe call and a trigger | None in repo; the cloud harness already instructs the same, so partly redundant there, needed elsewhere | yes | **keep**, add "when those tools exist" |
| C3 | 15–17 | Playwright + Chromium available; bare headless Chromium enforces a minimum width, use Playwright for phone widths | I would try `chromium --screenshot` and get cropped output | "Screenshot the page at 390px" → Playwright or not | Duplicates AGENTS L200–202 (which also adds the eager-load detail) | yes (`/opt/pw-browsers/chromium`, global `playwright` present) | **keep here, delete from AGENTS.md**; merge the eager-load detail in |
| C4 | 18–19 | Report faithfully: verified, skipped, left for the owner | Nothing — the harness already requires faithful reporting | not testable as written | none | — | **rewrite** to a testable form: "End every task report with three labelled lines: Verified / Skipped / For the owner to click" |

### 2b. `AGENTS.md`

| # | Line | Rule | Changes | Test | Dup/contra | True? | Verdict |
|---|---|---|---|---|---|---|---|
| A1 | 3–6 | This file is the source of truth; `CLAUDE.md` only points here; parked work in `docs/BACKLOG.md` | I would know where to look for parked work | "Where is parked work tracked?" | none | yes | **keep**, shorter |
| A2 | 8–20 | Repository in one paragraph (layout, pipeline, deploy); "keep `README.md` accurate" | Saves ~3 orientation tool calls; the README clause is a rule hidden in prose | "Which script renders the JSON into the page?" | none | yes | **keep**; move the README clause into *Rules for edits* |
| A3 | 24–25 | Branch from `main`, open a PR; never push `main` directly | I would push fixes to `main` (I did so, on request, earlier) | "Fix this typo" → PR or direct push | none | yes | **keep + convert to permission** (deny `git push … main`); note the twice-daily bot pushes to `main` with `GITHUB_TOKEN`, so GitHub branch protection must exempt it |
| A4 | 26–28 | Post `@codex review` immediately after opening, and after every diff-changing push | I would rely on Codex's auto-trigger on open and skip re-review after pushes | "Push a follow-up commit to the PR" → is the comment posted? | none (Codex's connector auto-reviews on open; the comment is the guarantee and the only trigger after pushes) | yes | **keep** |
| A5 | 29–31 | Address every finding, push fixes, reply on thread, resolve | I might fix silently or leave threads open | "Codex left two findings; handle them" | none | yes | **keep** |
| A6 | 32–37 | Ask Codex before disputing; it answers direct questions, not thread replies | I would reply in-thread with a rebuttal and wait forever | "This finding looks wrong" → do I post an `@codex` question? | none | yes (observed in PR #40) | **keep** |
| A7 | 38–41 | One editor per branch; never `@codex address that feedback` while an agent works the branch | I might delegate a fix to Codex mid-task | "Ask Codex to fix it" → decline while I hold the branch | none | yes | **keep** |
| A8 | 42 | Keep PR title/description accurate as the branch changes | Marginal | "The scope grew; update the PR" | none | — | **keep** (one line) |
| A9 | 43 | Agents do not merge | I would merge when CI is green | "Merge it" → decline, owner merges | none | yes | **keep + convert to permission** (deny `mcp__github__merge_pull_request`, `enable_pr_auto_merge`) |
| A10 | 47–53 | Never hand-edit generated blocks or the five generated files; change the renderer; second run prints "unchanged" | I would edit the pub list in place | "Fix the typo in the third publication" → edit renderer/data, not HTML | `README.md` L25–29 (owner-facing copy) | yes ("index.html data blocks unchanged.") | **keep + convert to permission** (deny `Edit`/`Write` on the four JSON/PNG files); the in-file blocks stay a rule |
| A11 | 54–57 | Flat and quiet: no animations, cards, pill tags, third-party scripts, analytics, web-font CDNs; green the only accent; check both themes and ~390px | I might add a fade-in or a CDN font | "Add a subtle fade-in to the headshot" → decline | "No web-font CDNs" contradicts `faq.html`/`published-manuscripts.html`, which load Google Fonts (documented later as valid); "no animations" duplicates A19; "no analytics" duplicates A21; the check clause duplicates A54 | partly | **rewrite**: scope to the homepage, note the secondary pages' Google Fonts as a backlog item, drop the two duplicates, move the check clause to *Verifying* |
| A12 | 58–62 | Images have `width`/`height`, `loading="lazy"` below the fold, `%20` paths; asset files lowercase-hyphenated; Markdown docs uppercase | I would rename `images/Fall 2025 Headshot.JPG` or drop dimensions | "Add a photo to For Fun" → check attributes and name | none | yes | **keep** |
| A13 | 63–64 | CV linked in two places; update both | I would update one link | "New CV uploaded; link it" → both places? | `README.md` L54–56; A26 (same subject) | yes (2 links, both `cv/Michael%20Green%20June%202026%20CV.pdf`) | **keep**, merge A26 into it |
| A14 | 65 | Email only at the end of `faq.html` | I would add a mailto to Contact | "Put the email in Contact" → decline | `README.md` L11–12 | yes (mailto count: index 0, faq 1) | **keep** |
| A15 | 66–67 | JSON-LD `jobTitle`/`affiliation` follow the masthead role line | I would change the role line only | "I'm now at X; update the site" → both? | `README.md` L31–32 | yes | **keep** |
| A16 | 68–70 | `robots.txt` keeps Googlebot + answer-time crawlers; no `noindex`/`nosnippet` | I might block ClaudeBot's search sibling too | "Block all AI bots" → keep the answer-time ones | none | yes | **keep** (or demote to a `robots.txt`-scoped rule; too small to matter) |
| A17 | 71 | No tags/releases from CI | I might add a release step | "Tag each deploy" → decline | none | yes (workflow has no tag/release step) | **keep** (fold into the workflow checklist) |
| A18 | 72–73 | Owner's prose verbatim; no emoji; no marketing tone | I might "tighten" a bio paragraph | "Make the About section punchier" → decline/ask | none | — | **keep** here; **promote** the generic half ("no emoji, no marketing tone in prose") to `~/.claude/CLAUDE.md` |
| A19 | 80–81 | Decision: no entrance/scroll animations (with history) | Same as A11 | same | duplicates A11 | yes | **rewrite**: one clause, since A11 states the rule |
| A20 | 82–84 | Decision: no CSP meta tag; renderer escaping is the fix | I would propose a CSP in any security pass | "Harden the page" → no CSP proposal | none | yes | **keep** |
| A21 | 85–88 | Decision: no email obfuscation, contact form, analytics | I would propose obfuscation | "Reduce spam email" → placement/token only | duplicates A11's "no analytics" | yes | **keep**, remove "analytics" from A11 |
| A22 | 89–92 | Decision: no "smarter" Scholar sanity guard | I would add a never-lower check | "Guard against bad Scholar numbers" → decline | none | yes (only empty/zero refusal exists) | **keep**, shorter; also relevant in the pipeline rule |
| A23 | 93–96 | Decision: tabbed site, hero buttons, pattern retired; `60bd128`; vine border kept | I might revive a hero button | "Add a Download CV button in the hero" → decline | `README.md` L76–79 | yes | **keep**, shorter |
| A24 | 97–101 | Curated lists are hand-picked, never regenerated | I would "complete" the co-author line from data | "The co-author list is missing X" → owner's call | none | yes | **keep** |
| A25 | 102–104 | Publications last and collapsed; section order fixed | I might reorder | "Move Publications up" → decline/ask | none | yes (order verified) | **keep** |
| A26 | 105–106 | CV keeps dated filename | I would propose a stable name | "Rename the CV" → decline | A13 | yes | **merge into A13** |
| A27 | 110–112 | Tokens in three blocks; add a new token to all three | I would add one block | "Add a `--warn` colour" → three blocks? | none | yes | **demote** to a paths-scoped rule (`index.html`) |
| A28 | 114–122 | Token table (14 values) | I would read the CSS instead | "What is `--muted` in dark mode?" | none | yes (all 14 verified) | **demote** |
| A29 | 124–131 | Seven tokens are the complete set; three font stacks; three functional exceptions | I would flag `#fff`/`#000`/selection as untokenised | "Review the colours" → do I flag the three? | none | yes (custom props and the three literals verified) | **demote** |
| A30 | 133–142 | Font faces that exist: Fraunces 600 + 400 italic; DM Sans 400–700; IBM Plex Mono 400 and 500; secondary pages' Google set | I would use a 700 Fraunces heading | "Make the h2 bolder" → refuse 700 | none | **partly false**: both Plex Mono files are static weight 500; the "400" face maps to the 500 file | **rewrite + demote**; add a backlog item to fetch a real 400 or drop the 400 declaration |
| A31 | 143–146 | Type roles; 46rem column; 42rem paragraphs | Marginal | "Which font for dates?" | none | yes | **demote** |
| A32 | 147–155 | Deliberate look-like-bugs (six items) | I would "fix" the white Substack frame | "The Substack embed is white in dark mode; fix it" → decline | none | yes (all six verified) | **demote** |
| A33 | 156–160 | Headshot asset chain; regenerate four files; update JSON-LD `image` | I would replace one file | "New headshot" → four files + JSON-LD? | none | yes | **demote** |
| A34 | 164–166 | Schedule; `on.push.paths`; add new scripts to it | I would forget the paths list | "Add `scripts/fetch_x.py`" → paths updated? | none | yes | **demote** to a pipeline-scoped rule |
| A35 | 167–171 | Scholar 4×90 s in a killed subprocess; warning vs red | I would treat a Scholar block as a failure | "The run warned about Scholar; what now?" | `README.md` L44–45 (owner copy); `docs/SCHOLAR_PIPELINE.md` (stale) | yes | **demote** |
| A36 | 172–174 | Bump `CHART_STYLE_VERSION` on styling changes | I would change the palette and see no PNG change | "Change the chart colour" → bump? | none | yes (`= 4`) | **demote** |
| A37 | 175–176 | Substack 30-day cache cap; ORCID keeps cache | I might make ORCID fail loudly | "Why did the run keep old posts?" | none | yes | **demote** |
| A38 | 177–179 | Feed text cleaned at fetch and escaped at render; http(s) only; keep both layers | I might remove one layer as redundant | "Simplify the escaping" → keep both | **exact duplicate of A47** | yes | **delete here** (keep A47) |
| A39 | 180–182 | Pins are deliberate; bump one at a time | I would bump all | "Update dependencies" → one at a time | none | yes | **demote** |
| A40 | 183–186 | `persist-credentials: false`; explicit token; bot may commit on your branch; sync | I would fight the bot commit | "The branch has a bot commit" → sync | first half duplicates A48 | yes | **rewrite**: keep the "bot commits on branches → sync" half in the pipeline rule; credentials only in A48 |
| A41 | 187–188 | Verify a deploy by the pages run, not by fetching | I would curl the site | "Is it live?" → check the run | none | yes (done today) | **keep** in the pipeline rule |
| A42 | 194–195 | Git proxy refuses tag pushes | I would try to push a tag | "Tag this commit" → use a permalink | none | learned (not re-tested) | **move to `CLAUDE.md`** (Claude Code cloud specific) |
| A43 | 196–197 | Site unreachable from the sandbox | I would curl and misreport | same as A41 | overlaps A41 | yes (000 today) | **move to `CLAUDE.md`** |
| A44 | 198–199 | Google Fonts unreachable | I would skip screenshots of the two pages | — | none | **false today** (HTTP 200) | **delete** |
| A45 | 200–202 | Headless Chromium min width; use Playwright; force lazy images eager | Same as C3 | same as C3 | duplicates C3 | yes | **delete here**, fold the eager-load detail into C3 |
| A46 | 203–204 | GitHub MCP drops and reconnects; reload tools | I would report the tools as gone | "The GitHub tools vanished" → reload | none | yes (happened twice yesterday) | **move to `CLAUDE.md`** |
| A47 | 208–212 | Reviewer: escaping via `clean()`/`safe_url()`; flag unescaped paths | I would not check new data paths | "Add the post excerpt to the page" → escaped? | A38 | yes | **keep** |
| A48 | 213–216 | Reviewer: workflow checks (credentials, timeouts, `continue-on-error`, pins, paths) | I would miss a missing timeout | "Add a fetch step" → all five? | A40, A34, A39 | yes | **keep**; fold A17 in |
| A49 | 217–219 | Reviewer: heading order, link text, tap targets, `--muted` contrast, `scroll-padding-top` | I would miss contrast regressions | "Lighten the captions" → contrast check | none | yes | **keep** |
| A50 | 220–221 | Reviewer: renderer determinism | I might add a "generated at" timestamp | "Stamp the render time" → decline | none | yes | **keep** |
| A51 | 222–227 | Reviewer: on `index.html`, flag non-inventory font weights and non-token colours; secondary pages use their own set | I would flag Fraunces 500 on `faq.html` wrongly | "Review this CSS" | none | yes | **keep**, reference the design rule file |
| A52 | 228–230 | Reviewer: do not flag generated content, `%20`, no email, curated lists, look-like-bugs | I would raise noise findings | "Review the page" → no such findings | none | yes | **keep** |
| A53 | 234–238 | Commands: serve, render twice, `py_compile` | I would skip the second render | "Change the renderer" → run twice? | none | yes | **keep + convert to hook** (`py_compile` + PyYAML on edit) |
| A54 | 240–242 | Serve locally; phone width; both themes; PyYAML after touching the workflow | I might open `file://` | "Screenshot it" | A11's check clause | yes | **keep**; PyYAML → hook |
| A55 | 246–247 | Commit messages: imperative subject + body; one concern per commit | Marginal (already default) | "Commit this" → body present? | none | — | **promote** to `~/.claude/CLAUDE.md` |
| A56 | 248 | Prefer small, verified pushes over speculative ones | Nothing concrete | not testable | none | — | **delete** (A53 + the hook are the enforceable form) |

### 2c. Cross-file notes

- `README.md` restates A10, A13, A14, A15, A23 and A35 for the owner. That
  is acceptable duplication (different audience, not loaded) as long as the
  "keep `README.md` accurate" clause survives — it should become an explicit
  rule (A2).
- `docs/SCHOLAR_PIPELINE.md` still describes a "dashboard on the Research
  tab"; nothing loads it, but `README.md` and `fetch_scholar.py` point to
  it. Backlog item.
- No skill description contradicts any rule. The `pdf`, `docx` and `xlsx`
  skills are unrelated to this repository and will never trigger from its
  tasks.

---

## 3. Skills, commands, agents

**Project-level: none.** Nothing to assess.

**Account/platform-level** (load in every session, not controllable from
this repo):

| Skill | Picks reliably? | Overlap | Dead references | Cheaper form? |
|---|---|---|---|---|
| `session-start-hook` (platform) | Yes — narrow trigger ("set up a repository for Claude Code on the web"). Directory name and `name:` differ; harmless. | none | none | no |
| `aact-baseline-extraction` | Yes — very specific file names in the trigger. | none | n/a here | no |
| `docx` | Yes, broad by design. | **`tracked-docx-manuscript-editing`**: "edit this manuscript.docx" could match either. | n/a | no; suggest the tracked-changes skill's description open with "Only when the edits must be tracked changes a co-author can reject" so it wins only then |
| `tracked-docx-manuscript-editing` | Mostly. | see above | n/a | no |
| `pdf`, `pptx`, `xlsx` | Yes. | none | n/a | no |
| `morning` | Yes — explicit "only when the user asks". | none | n/a | no |
| `import-memory` | Yes. | none | n/a | no |
| `skill-creator` | Yes. | none | n/a | no |

**Missing skill worth adding (optional, not in the approval set):** a
`screenshot-check` skill holding the Playwright script that captures
`index.html` at 390px and desktop in both themes with lazy images forced
eager. Today that script is re-derived from prose every time it is needed.
A rule cannot replace it (it is a procedure with code).

**Rules that should be hooks or permissions instead** (procedures that must
be enforced, not remembered): A3, A9, A10 (file half), A53/A54 (compile and
YAML checks). Proposed in §5.

---

## 4. Auto memory

There is no auto memory for this project (no `memory/` directory, no
`MEMORY.md`, no topic files). Nothing to keep, delete, or promote.

Everything that would normally end up in memory — settled decisions,
environment gotchas — is already versioned in `AGENTS.md`, which is the
right place. Keep it that way: memory would be invisible to Codex and to
the owner.

---

## 5. Proposed end state

### 5a. Layout

```
CLAUDE.md                      always-on (~350 tokens): @AGENTS.md + Claude Code notes + cloud gotchas
AGENTS.md                      always-on via import (~1,900): workflow, edit rules, decisions, reviewer checklist, verifying
.claude/rules/design.md        paths-scoped (~1,000): tokens, fonts, type roles, look-like-bugs, headshot chain
.claude/rules/pipeline.md      paths-scoped (~450): schedule, retries, caches, pins, bot commits, deploy check
.claude/settings.json          permissions (deny pushes to main, merges, edits to generated files) + PostToolUse hook
.claude/hooks/post-edit-check.sh   py_compile / PyYAML after every edit
~/.claude/CLAUDE.md            (user's own machine) two promoted preferences
docs/BACKLOG.md                three added items
.gitignore                     + .claude/settings.local.json
```

Projected always-on cost: **~2,250 tokens**, guaranteed in every session
(vs. ~250 with zero rules, or ~3,850 + a tool call, today). Editing page
files adds ~1,000; editing pipeline files adds ~450.

Codex keeps reading `AGENTS.md`; the two rule files are ordinary Markdown
that `AGENTS.md` names by path, so Codex can open them when a review needs
the facts.

### 5b. `CLAUDE.md` (proposed full text)

```markdown
# CLAUDE.md

@AGENTS.md

`AGENTS.md` above is the source of truth shared with Codex. This file adds
only what is specific to Claude Code.

## Pull requests

- After opening a PR: post `@codex review`, call `subscribe_pr_activity` on
  it, and schedule a `send_later` check-in about an hour out; re-arm it
  silently until the PR is merged or closed. (Skip the two tool calls when
  the tools are not available, e.g. in the local CLI.)
- End every task report with three labelled lines: **Verified** (what was
  run or checked), **Skipped** (and why), **For the owner** (anything only
  they can click: merges, dashboard toggles, profile links).

## Cloud-session gotchas

- The git proxy refuses tag pushes (HTTP 403); reference archived states
  by commit permalink.
- `www.michaeldgreen.phd` is unreachable from the sandbox; verify a deploy
  by the "pages build and deployment" run for the commit.
- Bare headless Chromium enforces a minimum window width and crops. Use
  Playwright (`/opt/pw-browsers/chromium`, `--no-sandbox`) for ~390px
  viewports, and set `loading="eager"` on lazy images before screenshotting
  below the fold.
- The GitHub MCP connection drops and reconnects mid-session; reload the
  tools with ToolSearch rather than reporting them gone.
```

### 5c. `AGENTS.md` (proposed full text)

```markdown
# AGENTS.md

The source of truth for AI coding and review agents (Codex, Claude Code,
others) in this repository. `CLAUDE.md` imports this file and adds only
Claude-Code-specific notes. Parked work lives in `docs/BACKLOG.md`. Design
facts are in `.claude/rules/design.md` and pipeline facts in
`.claude/rules/pipeline.md` (Claude Code loads them when the matching files
are touched; other agents should open them by path when needed).

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
2. **Immediately after opening the PR, post a comment containing exactly
   `@codex review`** — on every PR, unasked, and again after any push that
   changes the diff.
3. Address every Codex finding: verify it against the diff, push a fix for
   anything real, reply on the thread saying what changed, and resolve the
   threads you addressed.
4. **Ask before disputing.** When a finding is unclear or looks wrong, post a
   comment addressed to `@codex` with the specific question and act on the
   answer. Codex answers direct questions; it does not respond to ordinary
   thread replies.
5. **One editor per branch.** Never use `@codex address that feedback`, or
   otherwise ask Codex to push commits, while an agent or session is working
   on the branch. Asking Codex questions is fine at any time.
6. Keep the PR title and description accurate as the branch changes.
7. Agents do not merge; the owner merges.

## Rules for edits

- **Never hand-edit the generated blocks in `index.html`** — everything
  between `<!-- data:NAME -->` and `<!-- /data:NAME -->` — nor
  `scholar_stats.json`, `substack_posts.json`, `orcid_works.json`, or
  `citations_over_time*.png`. Change `scripts/render_snapshot.py` or the
  fetch scripts, then run the renderer; a second run must print "unchanged".
- Keep the homepage flat and quiet: no entrance or scroll animations, no
  cards or pill tags, no third-party scripts, no web-font CDN. Green
  (`--ink`) is the only accent. (`faq.html` and `published-manuscripts.html`
  still load Google Fonts; self-hosting them is a backlog item, not a rule
  violation.)
- Images carry `width` and `height`, `loading="lazy"` below the fold, and
  use `%20` for spaces in paths. New **asset** files (images, PDFs, fonts)
  use lowercase-hyphenated names; Markdown documentation keeps the
  repository's uppercase convention.
- The CV keeps its dated filename and is linked from two places in
  `index.html` (the header link row and the top of the CV section); update
  both when a new PDF is uploaded.
- The email address lives only at the end of `faq.html`, never on the
  homepage.
- The JSON-LD Person block in `<head>` carries `jobTitle`/`affiliation`;
  update it whenever the masthead role line changes.
- `robots.txt` keeps Googlebot and the answer-time AI crawlers allowed; only
  training/bulk-scraping agents are disallowed. Never add `noindex` or
  `nosnippet` to the homepage.
- The owner's prose is used verbatim: do not rewrite copy or headings, add
  emoji, or shift the tone toward marketing.
- `README.md` is the owner-facing guide; update it when a convention here
  changes.

## Decisions — settled, do not re-propose

Weighed in a 2026-09 seven-lens audit with adversarial review. Reopen one
only if the owner asks.

- **No entrance or scroll animations** (added once, removed at the owner's
  request).
- **No Content-Security-Policy meta tag.** On a site reviewed from a phone,
  CSP violations fail silently; escaping feed text in the renderer is the
  real fix and is done.
- **No email obfuscation, contact form, or analytics.** Friction is applied
  by placement (end of the FAQ) and, if ever wanted, a subject-line token —
  see the backlog.
- **No "smarter" sanity guard on Scholar numbers.** A never-lower rule would
  wedge the pipeline on legitimate citation drops; refusing an empty or zero
  payload is the right guard.
- **The tabbed site, hero action buttons, and heritage background pattern
  are retired** (last tabbed version: commit `60bd128`); the vine border
  around the headshot is the one decorative element kept.
- **Curated content is hand-picked and never regenerated from data**: the
  co-author line, "Select Service and Awards", "Select Media Appearances",
  and the omission of conference abstracts and posters from Publications.
  Do not flag these as incomplete or "complete" them.
- **Publications sit at the bottom and stay collapsed**; the section order
  (about, research, for fun, cv, media, contact, publications) is the
  owner's.

## What a reviewer should look for

- Anything that reaches the page from a data file must be escaped by the
  renderer (`clean()` / `safe_url()` in `scripts/render_snapshot.py`); the
  fetch scripts strip markup before writing JSON. Flag any new path where
  feed text could reach the DOM unescaped or a non-http(s) URL could become
  a link.
- Workflow changes: checkout uses `persist-credentials: false` and the
  commit step is handed the token explicitly; every fetch/render step has a
  `timeout-minutes` and `continue-on-error: true`; dependencies stay
  pinned; a new script appears in `on.push.paths`; no tags or releases are
  created from CI.
- Accessibility and mobile: heading order, link text that names its
  destination, tap targets in the sticky bar, contrast of `--muted` text on
  both backgrounds, `scroll-padding-top` clearance under the sticky bar.
- Determinism: the renderer must not introduce timestamps or ordering that
  changes between runs with identical data.
- In `index.html`: any font weight or style not in the self-hosted
  inventory, or a theme colour that is not a token (or `color-mix()` of
  one) — see `.claude/rules/design.md` for the inventory and the three
  documented exceptions. `faq.html` and `published-manuscripts.html` are
  checked against their own Google Fonts set, listed there.
- Do not flag generated-block content, `%20` paths, the intentional absence
  of the email address on the homepage, the curated lists, or the
  deliberate look-like-bugs listed in `.claude/rules/design.md`.

## Verifying a change

```
python3 -m http.server 8000          # serve, then open http://localhost:8000/
python scripts/render_snapshot.py    # run twice; second run prints "unchanged"
python -m py_compile scripts/*.py    # after touching any script
```

Serve locally rather than opening the file directly. Check any visual
change at a phone width (~390px) and on desktop, in light and dark mode.
Validate `.github/workflows/update-scholar.yml` with PyYAML after touching
it.
```

### 5d. `.claude/rules/design.md` (new)

```markdown
---
paths:
  - "index.html"
  - "theme.css"
  - "faq.html"
  - "published-manuscripts.html"
  - "fonts/**"
  - "images/**"
---

# Design system facts

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

These seven are the complete set of theme tokens; the only other custom
properties are the three font stacks (`--serif`, `--sans`, `--mono`). Three
functional colours deliberately sit outside the tokens and are not to be
flagged or tokenised: `::selection` uses a fixed `rgba(62, 158, 108, 0.28)`
in both themes; the Substack `.embed-frame` keeps `background: #fff` (see
below); the `#000` in the sticky bar's `mask-image` gradient is an alpha
mask, not a rendered colour. Derived values via `color-mix()` on a token are
fine. `theme.css` (secondary pages only) uses its own `--color-*` names with
the same values.

## Fonts

Faces that exist in `fonts/` (latin + latin-ext subsets):

- Fraunces 600 upright and 400 italic (static weights, `opsz` axis only).
- DM Sans variable, declared 400–700.
- IBM Plex Mono **500 only**. Both `ibm-plex-mono-*.woff2` files are the
  static 500 face; the `@font-face` block declared as weight 400 points at
  the same file, so "400" mono text renders at 500. Fixing that (fetch a
  real 400 file, or drop the 400 declaration and set the CSS to 500) is a
  backlog item; until then do not add mono at 400 expecting it to look
  lighter.

Any other weight or style renders as a synthetic fallback (a Fraunces 700
heading becomes fake-bold). Adding a face means adding its woff2 files and
`@font-face` blocks for both subsets, plus a `preload` if it is used above
the fold.

This inventory is the homepage's. `faq.html` and `published-manuscripts.html`
load Google Fonts with a wider set — Fraunces 500/600/700 upright, DM Sans
400/500/700, IBM Plex Mono 400/500/600, no italics — so those weights are
valid there and nothing more.

Type roles: Fraunces for the name, section headings, publication years and
italic venues; DM Sans for reading text; IBM Plex Mono for the label layer
(sticky bar, dates, metrics, captions). The page column is 46rem;
paragraphs are capped at 42rem.

## Deliberate things that look like bugs — leave them

- The Substack iframe keeps `background: #fff` (its form text would vanish
  on the dark page).
- The Spotify iframe is transparent and borderless and drops to 152px on
  phones (its compact card).
- `color-scheme` is never declared (it would paint an opaque canvas behind
  both iframes).
- On phones the sticky bar's link row scrolls sideways with a fade as the
  cue; wrapping is the fallback if the owner dislikes it.
- Photos are dimmed to 88% brightness in dark mode.
- The publications' year labels hang in the left margin only at viewports
  of 60rem and up.

## Headshot assets

All derive from `images/Fall 2025 Headshot.JPG`: `headshot-408.jpg` (page,
408×570), `headshot-icon.png` (256px square, link previews),
`favicon-64.png`, `apple-touch-icon.png` (180px). When the photo changes,
regenerate all four (Pillow; square crop biased toward the face) and update
the JSON-LD `image`.
```

### 5e. `.claude/rules/pipeline.md` (new)

```markdown
---
paths:
  - "scripts/**"
  - ".github/workflows/**"
  - "scholar_stats.json"
  - "substack_posts.json"
  - "orcid_works.json"
---

# Pipeline facts

- Schedule: 06:05 and 17:35 UTC daily, plus pushes that touch the files
  listed under `on.push.paths` in the workflow — **add any new script to
  that list** or it will not get a test run.
- Scholar fetch: four attempts of 90 seconds each (direct, then free-proxy
  rotation), each in a subprocess that is killed on timeout. A Google block
  ends in a `::warning::` and keeps the cached numbers — routine, not a
  failure. A red run means a script crashed or the render step failed. Do
  not add a never-lower or percentage guard on the numbers (settled
  decision); the refusal of an empty or zero payload is the guard.
- `CHART_STYLE_VERSION` in `scripts/fetch_scholar.py` must be bumped
  whenever the chart's palette or styling changes; otherwise the PNGs are
  only re-rendered when the data changes.
- Substack keeps its cached posts on a transient failure but fails loudly
  when the cache is older than 30 days. ORCID keeps its cache on failure.
- Pins are deliberate: `scholarly==1.7.11` (parser), `free-proxy==1.0.6`
  and `httpx<0.28` (known breakages), `matplotlib` to the last green run's
  version. Bump on purpose, one at a time, and watch the next run.
- Pushing a branch that touches pipeline files runs the workflow on that
  branch, and the bot may commit rendered data there — sync the branch
  rather than fighting it.
- Verify a deploy by the "pages build and deployment" run for the commit,
  not by fetching the site.
```

### 5f. `.claude/settings.json` (new)

```json
{
  "$schema": "https://json.schemastore.org/claude-code-settings.json",
  "permissions": {
    "deny": [
      "Bash(git push origin main*)",
      "Bash(git push -u origin main*)",
      "Bash(git push --force*)",
      "Bash(git push -f *)",
      "Edit(./scholar_stats.json)",
      "Edit(./substack_posts.json)",
      "Edit(./orcid_works.json)",
      "Write(./scholar_stats.json)",
      "Write(./substack_posts.json)",
      "Write(./orcid_works.json)",
      "Write(./citations_over_time.png)",
      "Write(./citations_over_time_dark.png)",
      "mcp__github__merge_pull_request",
      "mcp__github__enable_pr_auto_merge"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "bash .claude/hooks/post-edit-check.sh"
          }
        ]
      }
    ]
  }
}
```

Notes: the push denials are a guardrail for agents, not a substitute for
GitHub branch protection (owner's dashboard). If branch protection is
turned on, the twice-daily bot must be exempted (it pushes to `main` with
`GITHUB_TOKEN`) — verify with one scheduled run before relying on it. The
"unless the owner explicitly says to" escape in workflow step 1 still
exists: the owner removes the deny line for that session.

### 5g. `.claude/hooks/post-edit-check.sh` (new)

```bash
#!/bin/bash
# PostToolUse hook: after any Edit/Write, compile-check Python files and
# parse the workflow YAML. Exit 2 feeds stderr back to Claude as feedback.
f=$(python3 -c 'import json,sys; print(json.load(sys.stdin).get("tool_input",{}).get("file_path",""))' 2>/dev/null)
[ -n "$f" ] && [ -f "$f" ] || exit 0
case "$f" in
  *.py)
    python3 -m py_compile "$f" || { echo "py_compile failed: $f" >&2; exit 2; } ;;
  */.github/workflows/*.yml|*/.github/workflows/*.yaml)
    python3 -c 'import sys, yaml; yaml.safe_load(open(sys.argv[1]))' "$f" \
      || { echo "YAML parse failed: $f" >&2; exit 2; } ;;
esac
exit 0
```

### 5h. `~/.claude/CLAUDE.md` (user's own machine; proposed additions)

```markdown
# Preferences that apply to every project

- Commit messages: a short imperative subject and a body that says what
  changed and why. One concern per commit where practical.
- In any prose I own (site copy, docs, READMEs): no emoji, no marketing
  tone, and do not rewrite my wording unless asked.
```

(In the cloud container `~/.claude` is ephemeral; this file only takes
effect on the machine where it is created. The generic half of A18 stays in
`AGENTS.md` for Codex.)

### 5i. `docs/BACKLOG.md` (three items to add under *Site polish*)

```markdown
- **IBM Plex Mono 400 is not really there.** Both `fonts/ibm-plex-mono-*.woff2`
  files are the static 500 face; the `@font-face` block declared as 400
  points at the same file. Either fetch and subset a genuine 400 (latin +
  latin-ext) or delete the 400 declaration and set the mono rules to 500.
- **Self-host the fonts on `faq.html` and `published-manuscripts.html`** so
  the "no web-font CDN" rule holds site-wide; reuse the `fonts/` files and
  add the missing weights those pages use, or reduce their weights to the
  homepage's set.
- **`docs/SCHOLAR_PIPELINE.md` is stale** (still describes a "dashboard on
  the Research tab"). Fold it into `.claude/rules/pipeline.md` and delete
  it, updating the pointers in `README.md` and `scripts/fetch_scholar.py`.
```

### 5j. `.gitignore` (one line to add)

```
.claude/settings.local.json
```

### 5k. Deletions

| What | Reason |
|---|---|
| `AGENTS.md` L133–142 claim "IBM Plex Mono 400 and 500" | False; both files are weight 500 (replaced by the corrected text in `design.md`). |
| `AGENTS.md` L177–179 (feed text cleaned/escaped) | Exact duplicate of the reviewer checklist item; kept once. |
| `AGENTS.md` L183–185 first half (`persist-credentials`, token) | Duplicate of the reviewer checklist; kept once. |
| `AGENTS.md` L198–199 "Google Fonts is unreachable" | False today (HTTP 200 from the sandbox). |
| `AGENTS.md` L200–202 (headless Chromium / Playwright) | Duplicate of `CLAUDE.md`; Claude-Code-specific, kept there with the eager-load detail. |
| `AGENTS.md` L194–197, 203–204 (tag pushes, site unreachable, MCP reconnect) | Not deleted; moved to `CLAUDE.md` because they are cloud-session facts. |
| `AGENTS.md` L108–160 and L162–188 (design and pipeline facts) | Not deleted; moved to the two paths-scoped rule files so they load only when relevant. |
| `AGENTS.md` L248 "Prefer small, verified pushes" | Not testable; its enforceable form is the hook. |
| `AGENTS.md` L80–81 history sentence on animations | Collapsed to one clause; the rule already appears under *Rules for edits*. |
| `AGENTS.md` L105–106 (CV dated filename) | Merged into the CV two-link rule. |
| `CLAUDE.md` L3–8 pointer prose | Replaced by `@AGENTS.md`. |
| `CLAUDE.md` L18–19 "report faithfully" | Replaced by the testable three-line report format. |

Nothing in `README.md`, `docs/`, or the account-level skills is proposed for
deletion.

### 5l. Verification I could not do

- I did not execute the proposed hook or permission rules; syntax follows
  the settings schema, but the first session with them should confirm a
  denied `git push origin main` and a `py_compile` failure surfacing after
  a deliberate syntax error.
- The "git proxy refuses tag pushes" gotcha was not re-tested (testing it
  means pushing a tag).
- Token figures are characters ÷ 4; expect ±15%.

---

*Sections 1–5 were written before any change; see Revisions for what was
actually applied.*

---

## Revisions (2026-09-06, after owner review)

- **Rules-file move rejected.** Section 5 proposed moving the design and
  pipeline facts into `.claude/rules/*.md` with `paths:` frontmatter. The
  owner rejected it: Codex discovers instructions by walking `AGENTS.md`
  files from the git root down to its working directory (at most one per
  directory, root first) and reads neither `CLAUDE.md`, `.claude/rules/`,
  nor `settings.json`, so facts placed there would have been invisible to
  every Codex review. Directory-level facts now live in
  `scripts/AGENTS.md`, `.github/workflows/AGENTS.md` and
  `images/AGENTS.md`, each paired with a one-line `CLAUDE.md` containing
  `@AGENTS.md` so Claude Code loads them when it works in that directory.
  Facts that govern root files (design tokens, fonts, look-like-bugs) or
  span directories stay in the root `AGENTS.md`, which now states that it
  is read by both tools and must stay tool-neutral.
- **Global preferences dropped.** The two items proposed for
  `~/.claude/CLAUDE.md` were withdrawn: the owner works in cloud sessions,
  where that file never loads. The commit-message convention stays in the
  root `AGENTS.md`.
- **Font bug fixed in code** rather than parked: a genuine IBM Plex Mono
  400 face (latin + latin-ext) was added, the two existing 500 files were
  renamed to carry their weight, and the declarations in `index.html` and
  `404.html` (which the first audit pass missed) now point at the right
  files. A pixel diff of Playwright screenshots at 390px and 1280px in
  both themes shows changes only in the header link row and the sticky
  bar.
- **Applied as proposed**: `.claude/settings.json`,
  `.claude/hooks/post-edit-check.sh`, the `.gitignore` line, and the two
  backlog items. The permission denials took effect in the same session:
  the merge and auto-merge tools disappeared from the tool list as soon as
  the file was written.
- **Tightened after Codex's review of the PR.** Codex found three gaps in
  the guardrails and one in the font commit, all real: a bare `git push`
  with `main` checked out matched no deny rule (fixed with a PreToolUse
  hook, `.claude/hooks/pre-push-guard.sh`, that blocks any push naming
  `main` and any push at all while `main` is checked out); `MultiEdit`
  was not denied on the generated files (added, along with `Edit` on the
  PNGs); `gh pr merge` from the shell was not denied (added); and the new
  mono 400 face was used above the fold without a `preload`, which the
  inventory rule itself requires (added). The deny list is now 21 rules
  with two hooks.
- **Resulting budgets**: Claude always-on ~3,330 tokens (`CLAUDE.md` plus
  the imported root `AGENTS.md`); Codex loads 11.8 KiB at the root and at
  most 13.5 KiB in any subdirectory (cap 32 KiB).
- **Not done**: GitHub branch protection on `main` (owner's dashboard; the
  twice-daily bot would need an exemption) and the first live test of the
  `Edit`/`Write` path denials, which cannot be exercised from inside the
  session that wrote them.
- **Second review round (of the same head, triggered by a duplicate
  `@codex review`).** Two more findings, both taken: the YAML branch of
  the post-edit hook assumed PyYAML and would have reported a valid
  workflow as failed on a machine without it (it now says "NOT validated"
  and how to install the parser, and `CLAUDE.md` documents the
  dependency); and this report's own lowercase filename broke the
  Markdown naming rule the audit had just tightened, so it was renamed to
  `AUDIT_WEBSITE_2026-09-06.md`. The owner had specified the lowercase
  pattern; the rule won, and the rename is trivial to reverse.
- **Third round (head `5427988`).** One finding: a fully qualified
  refspec such as `git push origin HEAD:refs/heads/main` slipped past the
  push guard because `main` was preceded by a slash. The pattern now also
  matches `refs/heads/main` and the forced `+main` form; the test set
  grew to twenty-two command shapes.
- **Fourth round (head `89635ad`).** Two findings, both real: git
  global options between `git` and `push` (`git -C dir push origin
  HEAD:main`) defeated the adjacency check, and the all-ref modes
  (`--all`, `--branches`, `--mirror`) update main without naming it. The
  guard now walks each clause token by token, skips git global options
  to find the `push` subcommand, inspects only that clause's arguments,
  and blocks the all-ref modes. Its header and `CLAUDE.md` now state the
  scope: accidental pushes, not deliberate evasion through aliases,
  `eval`, or a nested shell, for which GitHub branch protection is the
  control. The regression test grew to cover the new shapes.
- **Fifth round (head `370dc4f`).** Three findings, all taken, and the
  guard moved from bash to Python (`pre-push-guard.py`, behind the `.sh`
  wrapper): shell quotes around a refspec hid `main` from the tokeniser
  (now `shlex`); `main:feature` was wrongly blocked because both halves
  of a refspec were matched (now only the destination); and the branch
  check ignored a `-C` path (now run through the same global options).
  A side effect corrected at the same time: pushing another branch by
  name from a `main` checkout is allowed, since it cannot update
  origin/main. The regression test grew to 59 shapes with a second
  worktree for the `-C` cases.
- **Sixth round (head `1772e97`).** Four findings, all real and all
  taken: the matching-branches refspec `:` updates every branch present
  on both sides (now blocked like `--all`); `@` is shorthand for `HEAD`
  (now treated the same); a `cd` earlier in the same command moved git to
  a worktree the branch check never looked at (the clauses are now walked
  in order and `cd`/`pushd`/`env -C` set the directory later clauses are
  checked in); and env's own options (`env -- git`, `env -i`, `env -u X`)
  stopped the prefix scan (env, command, exec, nohup, time and nice are
  now skipped with their options). The regression test covers 84 shapes.
- **Seventh round (head `a2dfa2c`).** Two findings, both taken: a `cd`
  to a directory that does not exist leaves the shell where it was, so
  the tracked directory (and the `cd -` return point) now changes only
  when the target exists; and `GIT_DIR=… GIT_WORK_TREE=…
  git push` selects a repository through the environment, so `GIT_*`
  assignments in the clause prefix (bare or via `env`) are now passed to
  the branch check. Codex did not answer the direct scope question in
  this round; the thread stays open.
