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

## Hooks and permissions

- `.claude/settings.json` denies pushes to `main`, PR merges, the GitHub
  MCP tools that commit files to a branch directly (`create_or_update_file`,
  `push_files`, `delete_file`; use git in the sandbox instead), and edits
  to the generated data files, and runs two hooks: `pre-push-guard.sh` before
  every Bash command and `post-edit-check.sh` after every edit (a
  `py_compile` for Python files, a PyYAML parse for workflow files). The
  YAML check needs PyYAML, which the cloud container ships; a local
  checkout without it gets a "NOT validated" message from the hook until
  `pip install pyyaml`.
- The push guard (`pre-push-guard.py`, behind the `.sh` wrapper) reads the
  command text and stops accidental pushes to `main`: a refspec whose
  destination is `main`, an all-ref mode, or a bare or `HEAD` push while
  `main` is checked out in the repository the command selects. Pushing
  another branch by name is always allowed. Deliberate evasion through an
  alias, `eval`, or a nested shell is out of its scope; GitHub branch
  protection is the control for that. Run
  `bash .claude/hooks/pre-push-guard.test.sh` after changing it.

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
