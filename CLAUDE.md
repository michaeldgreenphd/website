# CLAUDE.md

**Read `AGENTS.md` first — it is the single source of truth for this
repository's conventions**: the pull request workflow (including the
`@codex review` comment required on every PR), the rules for editing the
site, what reviewers look for, and how to verify a change. Nothing from it is
repeated here, so the two files cannot drift.

## Claude Code specifics

- After opening a PR, subscribe to its activity (`subscribe_pr_activity`) so
  Codex's review wakes the session, and schedule a fallback check-in about an
  hour out until the PR is merged or closed.
- Playwright and a Chromium build are available in the remote environment
  for the screenshot checks described in `AGENTS.md` ("Verifying a change");
  headless Chromium alone enforces a minimum window width, so use Playwright
  for phone-width viewports.
- When work is done, report faithfully: what was verified, what was skipped,
  and anything left for the owner to click (profile links, dashboard toggles).
