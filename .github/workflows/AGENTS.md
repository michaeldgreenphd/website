# .github/workflows/ — the data refresh workflow

Read together with the root `AGENTS.md`. `update-scholar.yml` is the only
workflow; what the scripts it runs do is described in `scripts/AGENTS.md`.

- Schedule: 06:05 and 17:35 UTC daily, plus pushes that touch the files
  listed under `on.push.paths`. Add any new pipeline script to that list.
- Every fetch/render step has `timeout-minutes` and `continue-on-error:
  true`, and the job has its own timeout. The commit step runs before the
  final outcome check, so data from steps that succeeded is committed even
  when the run ends red.
- Every Python package, direct and transitive, is pinned in
  `scripts/requirements.txt` to the versions of the last green run. The
  direct pins guard known breakages (`scholarly==1.7.11` for the parser,
  `free-proxy==1.0.6` because newer releases changed `get_proxy_list()`'s
  signature, `httpx==0.27.2` because 0.28 removed the `proxies=` kwarg,
  `matplotlib==3.11.1` for the chart); the transitive pins exist because
  `bibtexparser` 2.0.0 (2026-09-08) removed a module `scholarly` imports
  while it was unpinned. Bump one line at a time and watch the next run;
  a change to the file runs the workflow on the branch that carries it.
- The checkout uses `persist-credentials: false`; the commit step is handed
  `GITHUB_TOKEN` explicitly and pushes with it. Keep it that way.
- Pushing a branch that touches the listed paths runs the workflow on that
  branch, and the bot may commit rendered data there — sync the branch
  rather than fighting it.
- No tags or releases from this or any workflow.
- Validate the file with PyYAML after touching it.
