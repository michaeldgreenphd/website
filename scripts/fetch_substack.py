#!/usr/bin/env python3
"""
Substack feed cache.

Fetches the Not Being Green RSS feed and writes the latest posts to
substack_posts.json in the repository root. scripts/render_snapshot.py then
renders it into the "Recent Posts" block of index.html, which removes any
runtime dependency on third-party RSS-to-JSON proxies (rss2json / allorigins)
that rate-limit shared mobile IPs and made the block load unreliably.

Runs from the same GitHub Actions workflow as the Scholar pipeline.
Idempotent: if the post list is unchanged, the file is left untouched.

Usage:
    python scripts/fetch_substack.py
"""

import html
import json
import re
import sys
import xml.etree.ElementTree as ET
from datetime import date, timedelta
from pathlib import Path
from urllib.request import Request, urlopen

FEED_URL = "https://www.notbeinggreen.com/feed"
REPO_ROOT = Path(__file__).resolve().parent.parent
OUT_PATH = REPO_ROOT / "substack_posts.json"
MAX_POSTS = 5
TIMEOUT_S = 30
# A feed outage keeps the cached posts; past this age the cache is stale
# enough that the run should fail loudly instead.
MAX_CACHE_AGE_DAYS = 30

TAG_RE = re.compile(r"<[^>]+>")


def clean_text(value):
    """Feed text as plain text: strip markup, decode entities, tidy spaces."""
    return " ".join(html.unescape(TAG_RE.sub("", value or "")).split())

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
    """Extract the newest posts; field names are what
    scripts/render_snapshot.py consumes (title/link/pubDate/description)."""
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.iter("item"):

        def text(tag):
            el = item.find(tag)
            return (el.text or "").strip() if el is not None and el.text else ""

        items.append(
            {
                "title": clean_text(text("title")),
                "link": text("link"),
                "pubDate": text("pubDate"),
                "description": clean_text(text("description")),
            }
        )
        if len(items) >= MAX_POSTS:
            break
    return items


def cache_is_stale():
    try:
        cached = json.loads(OUT_PATH.read_text(encoding="utf-8"))
        updated = date.fromisoformat(cached.get("updated", ""))
    except (OSError, ValueError, json.JSONDecodeError):
        return True
    return date.today() - updated > timedelta(days=MAX_CACHE_AGE_DAYS)


def main():
    try:
        items = parse_items(fetch_feed())
    except Exception as err:  # noqa: BLE001 - network/parse failures alike
        # A transient feed outage should not fail the workflow or clobber a
        # good cache — keep last-good, unless that cache is itself stale.
        if OUT_PATH.exists() and not cache_is_stale():
            print(f"::warning::Substack fetch skipped ({err}); kept the cached posts.")
            return
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
