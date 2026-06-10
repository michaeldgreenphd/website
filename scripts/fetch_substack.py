#!/usr/bin/env python3
"""
Substack feed cache.

Fetches the Not Being Green RSS feed and writes the latest posts to
substack_posts.json in the repository root. The site's Media tab reads
this file directly, which removes the runtime dependency on third-party
RSS-to-JSON proxies (rss2json / allorigins) that rate-limit shared mobile
IPs and made the "Recent Posts" block load unreliably.

Runs from the same GitHub Actions workflow as the Scholar pipeline.
Idempotent: if the post list is unchanged, the file is left untouched.

Usage:
    python scripts/fetch_substack.py
"""

import json
import sys
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path
from urllib.request import Request, urlopen

FEED_URL = "https://www.notbeinggreen.com/feed"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "substack_posts.json"
MAX_POSTS = 5
TIMEOUT_S = 30

# A browser-like UA avoids over-eager CDN bot filtering on feed requests
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)


def fetch_feed():
    request = Request(
        FEED_URL,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/rss+xml, application/xml, text/xml",
        },
    )
    with urlopen(request, timeout=TIMEOUT_S) as response:
        return response.read()


def parse_items(xml_bytes):
    """Extract the newest posts; field names match what the frontend's
    formatSubstackPost() already consumes (title/link/pubDate/description)."""
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):

        def text(tag):
            el = item.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""

        items.append(
            {
                "title": text("title"),
                "link": text("link"),
                "pubDate": text("pubDate"),
                "description": text("description"),
            }
        )
        if len(items) >= MAX_POSTS:
            break
    return items


def main():
    try:
        items = parse_items(fetch_feed())
    except Exception as err:  # noqa: BLE001 - network/parse failures alike
        raise SystemExit(f"Unable to fetch Substack feed: {err}")

    if not items:
        raise SystemExit("Feed contained no items; refusing to write empty cache.")

    if OUT_PATH.exists():
        try:
            old = json.loads(OUT_PATH.read_text(encoding="utf-8"))
            if old.get("posts") == items:
                print("Substack posts unchanged; leaving cache untouched.")
                return
        except (json.JSONDecodeError, OSError):
            pass

    payload = {
        "updated": date.today().isoformat(),
        "source": FEED_URL,
        "posts": items,
    }
    OUT_PATH.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote {OUT_PATH} with {len(items)} posts")


if __name__ == "__main__":
    main()
