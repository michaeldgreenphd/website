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

MAX_COAUTHORS = 12  # keep the dashboard list compact
RETRIES = 3         # Scholar occasionally rate-limits; retry with backoff

# Muted, minimalist palettes. Bars use a slate blue; the latest (current)
# year is highlighted in the site's brand green to tie into the theme.
PALETTES = {
    "light": {
        "bar": "#46627F",        # muted slate blue
        "bar_latest": "#2D6A4F", # brand green highlight for the current year
        "text": "#333333",
        "subtext": "#666666",
        "spine": "#D0D0D0",
    },
    "dark": {
        "bar": "#8FAEC9",        # lifted slate for dark backgrounds
        "bar_latest": "#52B788",
        "text": "#F5F5F5",
        "subtext": "#C9C9C9",
        "spine": "#4A6354",
    },
}


# --- Data fetching ------------------------------------------------------------


def fetch_author():
    """Fetch and hydrate the author record, retrying on transient failures."""
    last_err = None
    for attempt in range(1, RETRIES + 1):
        try:
            author = scholarly.search_author_id(SCHOLAR_ID)
            return scholarly.fill(
                author, sections=["basics", "indices", "counts", "coauthors"]
            )
        except Exception as err:  # noqa: BLE001 - scholarly raises broadly
            last_err = err
            wait = 30 * attempt
            print(f"Fetch attempt {attempt}/{RETRIES} failed: {err}", file=sys.stderr)
            if attempt < RETRIES:
                print(f"Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
    raise SystemExit(f"Unable to fetch Google Scholar profile: {last_err}")


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

    # Value labels above each bar replace the y-axis entirely
    for bar, count in zip(bars, counts):
        ax.annotate(
            f"{count:,}",
            xy=(bar.get_x() + bar.get_width() / 2, bar.get_height()),
            xytext=(0, 5),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=9.5,
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
    ax.set_ylim(0, max(counts) * 1.18 if counts else 1)
    ax.margins(x=0.02)

    fig.tight_layout(pad=0.5)
    fig.savefig(out_path, transparent=True, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


# --- Main ----------------------------------------------------------------------


def main():
    author = fetch_author()
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
