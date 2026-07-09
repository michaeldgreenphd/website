#!/usr/bin/env python3
"""
ORCID publications cache.

Fetches the public works list for ORCID_ID and writes the normalized set to
orcid_works.json in the repository root. The site's Publications tab reads this
file directly, which removes the per-visitor runtime dependency on ORCID's API
— a live third-party fetch that fails on shared/mobile IPs the same way the
Substack "Recent Posts" block did before it was cached.

Runs from the same GitHub Actions workflow as the Scholar/Substack pipelines.
Idempotent: if the work list is unchanged, the file is left untouched.

Usage:
    python scripts/fetch_orcid.py
"""

import json
import sys
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

ORCID_ID = "0000-0002-4982-8154"  # Michael D. Green, PhD
WORKS_URL = f"https://pub.orcid.org/v3.0/{ORCID_ID}/works"
PROFILE_URL = f"https://orcid.org/{ORCID_ID}"

REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "orcid_works.json"
TIMEOUT_S = 30


def fetch_works():
    request = Request(
        WORKS_URL,
        headers={
            "Accept": "application/json",
            # ORCID's public API occasionally rejects blank UAs from datacenter IPs
            "User-Agent": "michaeldgreen.phd-site/1.0 (+https://www.michaeldgreen.phd)",
        },
    )
    with urlopen(request, timeout=TIMEOUT_S) as response:
        return json.loads(response.read())


def normalize(data):
    """Reduce ORCID's verbose /works response to the fields the site renders.

    Mirrors normalizeOrcidGroup() in index.html so the cached and live-API
    paths produce identical output. Sorted newest-first.
    """
    works = []
    for entry in data.get("group", []):
        summaries = entry.get("work-summary") or []
        work = summaries[0] if summaries else entry

        title = ((work.get("title") or {}).get("title") or {}).get("value") or "Untitled"
        year = ((work.get("publication-date") or {}).get("year") or {}).get("value") or ""
        journal = (work.get("journal-title") or {}).get("value") or ""
        work_type = work.get("type") or ""

        url = ""
        ext = (work.get("external-ids") or {}).get("external-id") or []
        doi = next((i for i in ext if i.get("external-id-type") == "doi"), None)
        if doi:
            url = (doi.get("external-id-url") or {}).get("value") or ""
            if not url and doi.get("external-id-value"):
                url = f"https://doi.org/{doi['external-id-value']}"
        if not url:
            url = (work.get("url") or {}).get("value") or ""

        works.append(
            {
                "title": title,
                "year": year,
                "journal": journal,
                "type": work_type,
                "url": url,
            }
        )

    def sort_key(w):
        try:
            return int(w["year"])
        except (TypeError, ValueError):
            return 0

    works.sort(key=sort_key, reverse=True)
    return works


def main():
    try:
        works = normalize(fetch_works())
    except Exception as err:  # noqa: BLE001 - network/parse failures alike
        # A transient ORCID outage should not fail the workflow or clobber a
        # good cache — the site also falls back to the live API. Keep last-good.
        if OUT_PATH.exists():
            print(f"::warning::ORCID fetch skipped ({err}); kept the cached works.")
            return
        raise SystemExit(f"Unable to fetch ORCID works and no cache exists: {err}")

    if not works:
        raise SystemExit("ORCID returned no works; refusing to write empty cache.")

    if OUT_PATH.exists():
        try:
            old = json.loads(OUT_PATH.read_text(encoding="utf-8"))
            if old.get("works") == works:
                print("ORCID works unchanged; leaving cache untouched.")
                return
        except (json.JSONDecodeError, OSError):
            pass

    payload = {
        "updated": date.today().isoformat(),
        "source": PROFILE_URL,
        "count": len(works),
        "works": works,
    }
    OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {OUT_PATH} with {len(works)} works")


if __name__ == "__main__":
    main()
