# .github/workflows/ — the data refresh workflow

Read together with the root `AGENTS.md`. `update-scholar.yml` is the only
workflow; what the scripts it runs do is described in `scripts/AGENTS.md`.

- Schedule: 06:05 and 17:35 UTC daily, plus pushes that touch the files
  listed under `on.push.paths`. Add any new pipeline script to that list.
- Two jobs. `fetch` (token `contents: read`) installs the packages, runs
  the three fetchers and uploads only the five data files as an artifact.
  `publish` (`contents: write`) installs nothing: from its own checkout it
  runs `scripts/stage_data.py import` (each file must be a JSON object or a
  PNG), `render_snapshot.py`, and `stage_data.py check` (only the data
  files and the `<!-- data: -->` blocks of `index.html` may change), then
  commits. Keep third-party code out of `publish`. It is skipped on
  Dependabot's `dependabot/…` branches, whose token is read-only (matched
  by branch name, not `github.actor`, so scheduled runs on `main` always
  publish).
- Every fetch/stage/render step has `timeout-minutes` and
  `continue-on-error: true`, and each job has its own timeout. The commit
  step runs before the final outcome check, so data from steps that
  succeeded is committed even when the run ends red.
- Actions are pinned to full commit SHAs with the version in a trailing
  comment; `.github/dependabot.yml` opens a weekly grouped PR to bump them.
  Never go back to a movable tag such as `@v7`.
- The chart font is downloaded from a pinned google/fonts commit and
  checked with `sha256sum`; a mismatch falls back to DejaVu Sans.
- Every Python package, direct and transitive, is pinned in
  `scripts/requirements.txt` to the versions of the last green run. The
  direct pins guard known breakages (`scholarly==1.7.11` for the parser,
  `free-proxy==1.0.6` because newer releases changed `get_proxy_list()`'s
  signature, `httpx==0.27.2` because 0.28 removed the `proxies=` kwarg,
  `matplotlib==3.11.1` for the chart); the transitive pins exist because
  `bibtexparser` 2.0.0 (2026-09-08) removed a module `scholarly` imports
  while it was unpinned. Bump one line at a time and watch the next run;
  a change to the file runs the workflow on the branch that carries it.
- Every pin also carries sha256 hashes and the install uses
  `--require-hashes`; `scripts/build-requirements.txt` pins the setuptools
  that builds the two sdist-only packages (`--no-build-isolation`). A bump
  must replace that pin's hash lines too (the header of
  `scripts/requirements.txt` says where to get them).
- Both checkouts use `persist-credentials: false`; the commit step is
  handed `GITHUB_TOKEN` explicitly and pushes with it. Keep it that way.
- Pushing a branch that touches the listed paths runs the workflow on that
  branch, and the bot may commit rendered data there — sync the branch
  rather than fighting it.
- No tags or releases from this or any workflow.
- Validate the file with PyYAML after touching it.
