# Google Scholar Dashboard Pipeline

The Citation Metrics dashboard on the Research tab is refreshed by a GitHub
Action (`.github/workflows/update-scholar.yml`) that runs `scripts/fetch_scholar.py`
twice a day, caches the results into the repo, and commits them.

## How failures are handled

Google Scholar has no official API and actively blocks automated requests
from datacenter IP ranges — which is what GitHub Actions runners use. So on
any given run the fetch **may be blocked**, and that is expected, not a bug.

The pipeline is built to degrade gracefully:

- **Blocked fetch** → the script keeps the last-good `scholar_stats.json`
  and charts, logs a `::warning::`, and **exits successfully** (green run).
  The dashboard keeps showing the previous numbers with its "Data as of"
  date, and the next scheduled run tries again.
- **A real bug** (e.g. a dependency changes its API) → the script exits with
  an error and the workflow run goes **red**, so you actually hear about the
  things worth fixing.

Because of this, a green run does not always mean the data changed, and a
stale "Data as of" date for a day or two just means Google was blocking the
fetch. The twice-daily schedule (≈1am and ≈12:30pm ET) self-heals these.

## Making the fetch reliable (optional): ScraperAPI

Free proxies are unreliable, so blocks can persist for a few days. To make
the fetch consistently succeed, add a free [ScraperAPI](https://www.scraperapi.com/)
key. The free tier (1,000 credits/month) far exceeds what one daily fetch
needs, and `scholarly` supports it natively.

1. Sign up at scraperapi.com and copy your API key.
2. In the GitHub repo: **Settings → Secrets and variables → Actions →
   New repository secret**.
3. Name it exactly `SCRAPERAPI_KEY`, paste the key, and save.

That's it — the workflow already passes the secret through to the script,
which routes every fetch through ScraperAPI when the key is present and
falls back to direct + free-proxy rotation when it is not. No code change
needed to turn it on or off.

## Manual run

You can trigger a refresh anytime from **Actions → Update Site Data
(Scholar + Substack) → Run workflow**.
