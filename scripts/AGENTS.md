# scripts/ — the data pipeline

Read together with the root `AGENTS.md`. These four scripts are run by
`.github/workflows/update-scholar.yml`; its schedule, pins and commit step
are described in `.github/workflows/AGENTS.md`.

- `fetch_scholar.py`: four attempts of 90 seconds each (direct, then
  free-proxy rotation), each in a subprocess that is killed on timeout. A
  Google block ends in a `::warning::` and keeps the cached numbers —
  routine, not a failure. Only scholarly's `MaxTriesExceededException` and
  `DOSException` (and timeouts) count as blocks; the same other exception
  type on two or more attempts exits 1 as a real bug. Refusing an empty or zero payload is the only
  sanity guard; do not add a never-lower or percentage rule (settled
  decision, root `AGENTS.md`). Bump `CHART_STYLE_VERSION` whenever the
  chart's palette or styling changes; otherwise the PNGs are re-rendered
  only when the data changes.
- `fetch_substack.py`: keeps the cached posts on a transient failure but
  fails loudly when the cache is older than `MAX_CACHE_AGE_DAYS` (30). A
  successful fetch refreshes the cache's `updated` date weekly
  (`REFRESH_AFTER_DAYS`) even when the posts are unchanged, so that age
  counts from the last good fetch; expect one small data commit a week.
- `fetch_orcid.py`: keeps its cache on any failure. Publication links are
  built only as `https://doi.org/<DOI>`; a work without a well-formed DOI
  is listed without a link. Each work keeps its ORCID `source` (not
  rendered), and works added to or removed from the record are printed as
  `::notice::` lines in the run summary.
- `render_snapshot.py` splices generated HTML between the
  `<!-- data:NAME -->` markers in `index.html`. It is deterministic — no
  timestamps, no run-dependent ordering — and a second run on unchanged
  data prints "index.html data blocks unchanged." It omits works typed
  `conference-abstract` and `conference-poster` on purpose.
- Keep both escaping layers: the fetch scripts' `clean_text()` (tags
  stripped, entities decoded, before writing JSON) and the renderer's
  `clean()` / `safe_url()` (escaped on output; links only for http(s)
  URLs). The root reviewer checklist explains why.
- A new script must be added to `on.push.paths` in the workflow or it
  never gets a test run.
- After any change: `python -m py_compile scripts/*.py`, then run the
  renderer twice.
