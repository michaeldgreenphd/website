#!/usr/bin/env python3
"""
Google Scholar dashboard data pipeline.

Fetches profile metrics for SCHOLAR_ID from Google Scholar via the
`scholarly` package and writes three artifacts to the repository root:

  scholar_stats.json            core metrics, per-year citations, co-authors
  citations_over_time.png       styled bar chart (light theme)
  citations_over_time_dark.png  styled bar chart (dark theme)

Designed to run headlessly from a GitHub Actions cron job (see
.github/workflows/update-scholar.yml). The script is idempotent: if the
fetched data is identical to what is already committed (ignoring the
"updated" timestamp), it leaves all files untouched so the workflow's
commit step produces no churn.

Usage:
    pip install scholarly matplotlib
    python scripts/fetch_scholar.py
"""

import json
import multiprocessing
import os
import sys
import time
from datetime import date
from pathlib import Path

import matplotlib

matplotlib.use("Agg")  # headless rendering, no display required
import matplotlib.pyplot as plt
from matplotlib import font_manager
from scholarly import scholarly

# --- Configuration -----------------------------------------------------------

SCHOLAR_ID = "ea2W0QgAAAAJ"  # Michael D. Green, PhD
PROFILE_URL = f"https://scholar.google.com/citations?user={SCHOLAR_ID}&hl=en"

REPO_ROOT = Path(__file__).resolve().parent.parent
JSON_PATH = REPO_ROOT / "scholar_stats.json"
CHART_LIGHT_PATH = REPO_ROOT / "citations_over_time.png"
CHART_DARK_PATH = REPO_ROOT / "citations_over_time_dark.png"

MAX_COAUTHORS = 12   # keep the dashboard list compact
RETRIES = 4          # attempt 1 is direct; later attempts rotate free proxies
FETCH_TIMEOUT_S = 90 # hard cap per attempt; Scholar tarpits blocked IPs and
                     # scholarly will otherwise hang until the CI job times out

# Optional: a ScraperAPI key (free tier is plenty for one daily fetch) makes
# the fetch reliable through Google's datacenter-IP block. Set it as the
# SCRAPERAPI_KEY repository secret to enable; without it the script falls back
# to direct + free-proxy rotation. See docs/SCHOLAR_PIPELINE.md.
SCRAPERAPI_KEY = os.environ.get("SCRAPERAPI_KEY", "").strip()


class ScholarFetchBlocked(Exception):
    """Every fetch attempt was blocked/timed out — the expected transient
    case (Google rate-limiting CI IPs), distinct from an unexpected bug."""

# Bump to force a chart re-render on the next run even when the Scholar data
# itself is unchanged (the version is stored in scholar_stats.json and
# participates in the changed-data comparison).
CHART_STYLE_VERSION = 3

# Muted, minimalist palettes drawn from the site's design tokens (theme.css):
# desaturated green-slate bars with the current year highlighted in the
# brand primary; green-tinted neutral text instead of default blacks/grays.
PALETTES = {
    "light": {
        "bar": "#5E7D70",        # muted green-slate (neutral family)
        "bar_latest": "#2D6A4F", # --color-primary highlight for current year
        "text": "#22332B",       # --color-text
        "subtext": "#5B6962",    # --color-text-secondary
        "spine": "#E2E8E4",      # --color-border
    },
    "dark": {
        "bar": "#7FA391",        # lifted green-slate for dark surfaces
        "bar_latest": "#52B788", # dark-mode --color-primary
        "text": "#F2F5F3",
        "subtext": "#C9D4CE",
        "spine": "#3D5A4A",
    },
}


# --- Data fetching ------------------------------------------------------------


def _enable_free_proxies():
    """Route scholarly through rotating free proxies.

    Google Scholar frequently blocks or tarpits CI runner IPs; proxy
    rotation gives retries a fresh address. Best-effort: on any failure we
    continue with a direct connection.
    """
    try:
        from scholarly import ProxyGenerator

        pg = ProxyGenerator()
        if pg.FreeProxies():
            scholarly.use_proxy(pg)
            print("Retrying via free proxy rotation", file=sys.stderr)
    except Exception as err:  # noqa: BLE001
        print(f"Proxy setup failed ({err}); continuing direct", file=sys.stderr)


def _configure_proxy(attempt):
    """Configure scholarly's transport for this attempt.

    With SCRAPERAPI_KEY set, route every attempt through ScraperAPI, which
    reliably gets past Google's datacenter-IP block. Without a key, attempt 1
    goes direct and later attempts rotate free proxies (best-effort).
    """
    if SCRAPERAPI_KEY:
        try:
            from scholarly import ProxyGenerator

            pg = ProxyGenerator()
            if pg.ScraperAPI(SCRAPERAPI_KEY):
                scholarly.use_proxy(pg)
                print("Using ScraperAPI proxy", file=sys.stderr)
                return
            print("ScraperAPI rejected the key; falling back", file=sys.stderr)
        except Exception as err:  # noqa: BLE001
            print(f"ScraperAPI setup failed ({err}); falling back", file=sys.stderr)
    if attempt > 1:
        _enable_free_proxies()


def _fetch_worker(queue, attempt):
    """Child-process body: fetch the author record and report via queue."""
    try:
        _configure_proxy(attempt)
        author = scholarly.search_author_id(SCHOLAR_ID)
        author = scholarly.fill(
            author, sections=["basics", "indices", "counts", "coauthors"]
        )
        queue.put(("ok", dict(author)))
    except Exception as err:  # noqa: BLE001 - scholarly raises broadly
        queue.put(("err", repr(err)))


def fetch_author():
    """Fetch the author record with hard per-attempt timeouts.

    Each attempt runs in a separate process that is terminated at
    FETCH_TIMEOUT_S. Process isolation is deliberate: scholarly's internal
    retry loop swallows in-process timeout exceptions (signal.alarm proved
    insufficient), and a tarpitted connection would otherwise hang the CI
    job until the workflow-level timeout. Retries route through free
    proxies to get a fresh IP.
    """
    last_err = None

    for attempt in range(1, RETRIES + 1):
        queue = multiprocessing.Queue()
        proc = multiprocessing.Process(
            target=_fetch_worker, args=(queue, attempt), daemon=True
        )
        proc.start()
        proc.join(FETCH_TIMEOUT_S)

        if proc.is_alive():
            proc.terminate()
            proc.join(5)
            last_err = f"attempt timed out after {FETCH_TIMEOUT_S}s (terminated)"
            print(f"Fetch attempt {attempt}/{RETRIES}: {last_err}", file=sys.stderr)
        else:
            try:
                status, payload = queue.get(timeout=5)
            except Exception:  # noqa: BLE001 - empty queue means worker died
                status, payload = "err", "worker exited without a result"
            if status == "ok":
                return payload
            last_err = payload
            print(f"Fetch attempt {attempt}/{RETRIES} failed: {payload}", file=sys.stderr)

        if attempt < RETRIES:
            print("Retrying in 10s...", file=sys.stderr)
            time.sleep(10)

    raise ScholarFetchBlocked(f"all {RETRIES} attempts failed: {last_err}")


def build_payload(author):
    """Shape the scholarly author record into the dashboard's JSON schema."""
    cites_per_year = author.get("cites_per_year") or {}
    years = sorted(int(y) for y in cites_per_year)

    coauthors = []
    for entry in (author.get("coauthors") or [])[:MAX_COAUTHORS]:
        scholar_id = entry.get("scholar_id")
        coauthors.append(
            {
                "name": entry.get("name", ""),
                "affiliation": entry.get("affiliation", ""),
                "profile_url": (
                    f"https://scholar.google.com/citations?user={scholar_id}&hl=en"
                    if scholar_id
                    else None
                ),
            }
        )

    return {
        "scholar_id": SCHOLAR_ID,
        "profile_url": PROFILE_URL,
        "chart_style": CHART_STYLE_VERSION,
        "name": author.get("name", ""),
        "affiliation": author.get("affiliation", ""),
        "metrics": {
            "citations": author.get("citedby", 0),
            "h_index": author.get("hindex", 0),
            "i10_index": author.get("i10index", 0),
        },
        "citations_per_year": [
            {"year": y, "citations": int(cites_per_year[y] if y in cites_per_year else cites_per_year[str(y)])}
            for y in years
        ],
        "coauthors": coauthors,
    }


def payload_changed(new_payload):
    """Compare against the committed JSON, ignoring the 'updated' field."""
    if not JSON_PATH.exists():
        return True
    try:
        old = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return True
    old.pop("updated", None)
    return old != new_payload


# --- Chart rendering -----------------------------------------------------------


def pick_font():
    """Prefer DM Sans (installed by the workflow) to match site typography."""
    available = {f.name for f in font_manager.fontManager.ttflist}
    for candidate in ("DM Sans", "DejaVu Sans"):
        if candidate in available:
            return candidate
    return "sans-serif"


def render_chart(citations_per_year, palette, out_path, font_name):
    """Render a minimalist, publication-ready bar chart.

    Design notes: no gridlines or y-axis chrome -- each bar is labeled with
    its value directly; transparent background so the image sits on the
    site's card in both light and dark themes.
    """
    years = [d["year"] for d in citations_per_year]
    counts = [d["citations"] for d in citations_per_year]
    latest_year = max(years)

    fig, ax = plt.subplots(figsize=(8.4, 3.6), dpi=200)

    colors = [
        palette["bar_latest"] if y == latest_year else palette["bar"] for y in years
    ]
    bars = ax.bar(years, counts, width=0.62, color=colors, zorder=3)

    # Value labels above each bar replace the y-axis entirely; the generous
    # offset and headroom (see set_ylim below) keep them from crowding the bars
    for bar, count in zip(bars, counts):
        ax.annotate(
            f"{count:,}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 10),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=12,
            fontweight=600,
            fontfamily=font_name,
            color=palette["subtext"],
        )

    # Strip all chart chrome except a thin baseline
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(palette["spine"])
    ax.spines["bottom"].set_linewidth(1)

    ax.set_xticks(years)
    ax.set_xticklabels(
        years, fontsize=10.5, fontfamily=font_name, color=palette["text"]
    )
    ax.tick_params(axis="x", length=0, pad=8)
    ax.set_yticks([])
    # ~15px of clear headroom above the tallest label at typical render sizes
    ax.set_ylim(0, max(counts) * 1.36 if counts else 1)
    ax.margins(x=0.02)

    fig.tight_layout(pad=0.5)
    fig.savefig(out_path, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


# --- Main ----------------------------------------------------------------------


def rerender_from_cache(reason):
    """Re-render charts from the committed scholar_stats.json.

    Chart styling changes shouldn't have to wait for a day when Google
    isn't blocking the fetch: if the live fetch fails but the cached data
    predates CHART_STYLE_VERSION, render from cache and record the new
    style version. Chronic fetch failures still surface as failures on
    every other run, because the style fallback only fires once.
    """
    if not JSON_PATH.exists():
        return False
    try:
        cached = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return False
    if cached.get("chart_style") == CHART_STYLE_VERSION:
        return False  # charts already current; let the fetch failure surface
    if not cached.get("citations_per_year"):
        return False

    print(f"{reason}; re-rendering charts from cached data", file=sys.stderr)
    font_name = pick_font()
    render_chart(
        cached["citations_per_year"], PALETTES["light"], CHART_LIGHT_PATH, font_name
    )
    render_chart(
        cached["citations_per_year"], PALETTES["dark"], CHART_DARK_PATH, font_name
    )
    cached["chart_style"] = CHART_STYLE_VERSION
    JSON_PATH.write_text(
        json.dumps(cached, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print("Charts re-rendered from cache; metrics unchanged.")
    return True


def main():
    try:
        author = fetch_author()
    except ScholarFetchBlocked as err:
        # Google blocked every attempt — the expected transient case, not a
        # bug. Keep the committed last-good data (the dashboard surfaces its
        # "Data as of" date and the twice-daily schedule self-heals), refresh
        # charts from cache if the styling changed, and exit 0 so a routine
        # block doesn't show up as a failed workflow run. A genuine bug raises
        # some other exception and still fails loudly.
        rerender_from_cache(str(err))
        print(
            f"::warning::Google Scholar fetch skipped ({err}); "
            "kept the last cached metrics."
        )
        return

    payload = build_payload(author)

    # Refuse to publish obviously broken data (e.g. a blocked/empty response)
    if not payload["metrics"]["citations"] or not payload["citations_per_year"]:
        raise SystemExit("Fetched data looks empty; refusing to overwrite artifacts.")

    if not payload_changed(payload):
        print("Scholar data unchanged; leaving artifacts untouched.")
        return

    font_name = pick_font()
    render_chart(
        payload["citations_per_year"], PALETTES["light"], CHART_LIGHT_PATH, font_name
    )
    render_chart(
        payload["citations_per_year"], PALETTES["dark"], CHART_DARK_PATH, font_name
    )

    payload["updated"] = date.today().isoformat()
    JSON_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {JSON_PATH}")
    print(
        f"Citations: {payload['metrics']['citations']}, "
        f"h-index: {payload['metrics']['h_index']}, "
        f"i10-index: {payload['metrics']['i10_index']}, "
        f"years: {len(payload['citations_per_year'])}, "
        f"co-authors: {len(payload['coauthors'])}"
    )


if __name__ == "__main__":
    main()
