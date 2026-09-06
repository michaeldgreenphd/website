@AGENTS.md

# Claude Code notes

`AGENTS.md` (imported above) is shared with Codex and stays tool-neutral.
This file holds only what applies to Claude Code sessions.

## Pull requests

- After opening a PR and posting `@codex review`, call
  `subscribe_pr_activity` on it and schedule a `send_later` check-in about
  an hour out; re-arm it silently until the PR is merged or closed, then
  delete the trigger.
- End every task report with three labelled lines: **Verified** (what was
  run or checked), **Skipped** (and why), **For the owner** (anything only
  they can click: merges, dashboard toggles, profile links).

## Cloud-container gotchas

- The git proxy refuses tag pushes (HTTP 403); reference archived states
  by commit permalink.
- `www.michaeldgreen.phd` is unreachable from the sandbox; use the
  deploy-verification rule in `AGENTS.md` (the "pages build and
  deployment" run) instead of fetching the site.
- Bare headless Chromium enforces a minimum window width and crops. Use
  Playwright (`/opt/pw-browsers/chromium`, `--no-sandbox`) for ~390px
  viewports, and set lazy images to `loading="eager"` before screenshotting
  below the fold.
- The GitHub MCP connection drops and reconnects mid-session; reload the
  tools with ToolSearch rather than reporting them gone.
