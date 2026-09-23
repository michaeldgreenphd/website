#!/usr/bin/env python3
"""
ORCID publications cache.

Fetches the public works list for ORCID_ID and writes the normalized set to
orcid_works.json in the repository root. scripts/render_snapshot.py then
renders it into the Publications section of index.html, which removes any
per-visitor runtime dependency on ORCID's API — a live third-party fetch that
fails on shared/mobile IPs the same way the Substack "Recent Posts" block did
before it was cached.

Runs from the same GitHub Actions workflow as the Scholar/Substack pipelines.
Idempotent: if the work list is unchanged, the file is left untouched.

Usage:
    python scripts/fetch_orcid.py
"""

import html
import json
import re
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

# Only what an HTML parser would treat as a tag, so text such as
# "aged <65 and >85 years" is not cut down to "aged 85 years"
TAG_RE = re.compile(r"</?[A-Za-z][^<>]*>")
# Bidi controls and Unicode tag characters: invisible on the page, but they
# reorder or hide words in the text that is stored and committed
INVISIBLE_RE = re.compile("[\u202a-\u202e\u2066-\u2069\U000e0000-\U000e007f]")
DOI_RE = re.compile(r"^10\.\d{4,9}/\S+$")
DOI_PREFIX_RE = re.compile(r"^(?:doi:\s*|https?://(?:dx\.)?doi\.org/)", re.IGNORECASE)


def clean_text(value):
    """Plain text: strip markup (Crossref-fed titles carry <i>/<sub>), decode
    entities, drop invisible controls, tidy whitespace."""
    text = INVISIBLE_RE.sub("", html.unescape(TAG_RE.sub("", value or "")))
    return " ".join(text.split())


def doi_url(value):
    """https://doi.org/<DOI> for a well-formed DOI (bare, doi:-prefixed or
    already a doi.org link), else ''."""
    doi = DOI_PREFIX_RE.sub("", str(value or "").strip())
    return f"https://doi.org/{doi}" if DOI_RE.match(doi) else ""


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

    Field names are what scripts/render_snapshot.py consumes. Sorted
    newest-first.
    """
    works = []
    for entry in data.get("group", []):
        summaries = entry.get("work-summary") or []
        work = summaries[0] if summaries else entry

        title = clean_text(((work.get("title") or {}).get("title") or {}).get("value")) or "Untitled"
        year = ((work.get("publication-date") or {}).get("year") or {}).get("value") or ""
        journal = clean_text((work.get("journal-title") or {}).get("value"))
        work_type = work.get("type") or ""
        source = clean_text(((work.get("source") or {}).get("source-name") or {}).get("value"))

        # Links go only to doi.org, built from the DOI itself. A work's own
        # url and external-id-url can point anywhere, and any party the ORCID
        # record trusts (including Crossref/DataCite auto-update) can set them.
        ext = (work.get("external-ids") or {}).get("external-id") or []
        doi = next((i for i in ext if i.get("external-id-type") == "doi"), None) or {}
        candidates = [
            doi.get("external-id-value"),
            (doi.get("external-id-url") or {}).get("value"),
            (work.get("url") or {}).get("value"),
        ]
        url = next((u for u in map(doi_url, candidates) if u), "")

        works.append(
            {
                "title": title,
                "year": year,
                "journal": journal,
                "type": work_type,
                "url": url,
                # Who added the work to the ORCID record; not rendered
                "source": source,
            }
        )

    def sort_key(w):
        try:
            return int(w["year"])
        except (TypeError, ValueError):
            return 0

    works.sort(key=sort_key, reverse=True)
    return works


def report_changes(old_works, new_works):
    """Print a ::notice:: for each work added to or removed from the record,
    so a new entry (and who added it) shows in the run summary before it has
    been on the homepage for long."""

    def key(work):
        return work.get("url") or work.get("title")

    def notice(text):
        # Workflow-command escaping; clean_text() has already removed newlines
        print("::notice::" + text.replace("%", "%25"))

    old_keys = {key(w) for w in old_works if isinstance(w, dict)}
    new_keys = {key(w) for w in new_works}
    for work in new_works:
        if key(work) not in old_keys:
            notice(f"ORCID added: {work['title']} (source: {work['source'] or 'unknown'})")
    for work in old_works:
        if isinstance(work, dict) and key(work) not in new_keys:
            notice(f"ORCID removed: {work.get('title')}")


def main():
    try:
        works = normalize(fetch_works())
    except Exception as err:  # noqa: BLE001 - network/parse failures alike
        # A transient ORCID outage should not fail the workflow or clobber a
        # good cache. Keep last-good; the page keeps its last rendered list.
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
            report_changes(old.get("works") or [], works)
        except (json.JSONDecodeError, OSError):
            pass

    payload = {
        "updated": date.today().isoformat(),
        "source": PROFILE_URL,
        "count": len(works),
        "works": works,
    }
    # Encode before opening, so an encoding error cannot leave an empty file
    OUT_PATH.write_bytes(
        (json.dumps(payload, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
    )
    print(f"Wrote {OUT_PATH} with {len(works)} works")


if __name__ == "__main__":
    main()
