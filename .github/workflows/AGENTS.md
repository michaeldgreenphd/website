# .github/workflows/ — the data refresh workflow

Read together with the root `AGENTS.md`. `update-scholar.yml` is the only
workflow; what the scripts it runs do is described in `scripts/AGENTS.md`.

- Schedule: 06:05 and 17:35 UTC daily, plus pushes that touch the files
  listed under `on.push.paths`. Add any new pipeline script to that list.
- Every fetch/render step has `timeout-minutes` and `continue-on-error:
  true`, and the job has its own timeout. The commit step runs before the
  final outcome check, so data from steps that succeeded is committed even
  when the run ends red.
- Pins in the install step are deliberate: `scholarly==1.7.11` (parser),
  `free-proxy==1.0.6` (newer releases changed `get_proxy_list()`'s
  signature), `httpx<0.28` (known breakage), and `matplotlib` pinned to
  the last green run's version. Bump one at a time and watch the next run.
- The checkout uses `persist-credentials: false`; the commit step is handed
  `GITHUB_TOKEN` explicitly and pushes with it. Keep it that way.
- Pushing a branch that touches the listed paths runs the workflow on that
  branch, and the bot may commit rendered data there — sync the branch
  rather than fighting it.
- No tags or releases from this or any workflow.
- Validate the file with PyYAML after touching it.
