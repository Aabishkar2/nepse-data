"""Fetch/update the NEPSE main index daily history from ShareSansar.

Writes/updates data/nepse-index.csv with columns:
published_date, open, high, low, close, point_change, pct_change, turnover

On first run it backfills the full available history (back to 1997-07-20).
On later runs it only requests days after the last date already on file.
"""
import csv
import datetime as dt
import json
import subprocess
import time
import urllib.parse
from pathlib import Path
from zoneinfo import ZoneInfo

NEPSE_INDEX_ID = 12  # "NEPSE Index" option value on the index-history-data form
ENDPOINT = "https://www.sharesansar.com/index-history-data"
PAGE_SIZE = 50  # the API silently returns an empty result for length >= 100
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "nepse-index.csv"
EARLIEST_FROM = "1994-01-01"  # earlier than any real data; server clamps it

# ShareSansar's WAF fingerprints the TLS/HTTP client: plain `requests` calls get
# silently blocked (HTTP 202, empty payload) while curl is let through. Shelling
# out to curl (present on GitHub's ubuntu runners) sidesteps that reliably.
CURL_HEADERS = [
    "-A", "Mozilla/5.0 (compatible; nepse-breadth-bot/1.0)",
    "-H", "X-Requested-With: XMLHttpRequest",
]


def today_nepal() -> str:
    return dt.datetime.now(ZoneInfo("Asia/Kathmandu")).strftime("%Y-%m-%d")


def fetch_page(date_from: str, date_to: str, start: int) -> dict:
    params = {
        "draw": 1,
        "start": start,
        "length": PAGE_SIZE,
        "index_id": NEPSE_INDEX_ID,
        "from": date_from,
        "to": date_to,
    }
    url = f"{ENDPOINT}?{urllib.parse.urlencode(params)}"
    result = subprocess.run(
        ["curl", "-s", "--fail", *CURL_HEADERS, url],
        capture_output=True, text=True, timeout=30,
    )
    result.check_returncode()
    return json.loads(result.stdout)


def fetch_range(date_from: str, date_to: str) -> list[dict]:
    rows = []
    start = 0
    while True:
        payload = fetch_page(date_from, date_to, start)
        rows.extend(payload.get("data", []))
        total = payload.get("recordsTotal", 0)
        start += PAGE_SIZE
        if start >= total:
            break
        time.sleep(0.3)  # polite delay between pages
    return rows


def load_existing() -> dict[str, dict]:
    if not OUT_PATH.exists():
        return {}
    with OUT_PATH.open(newline="") as f:
        return {row["published_date"]: row for row in csv.DictReader(f)}


def main():
    existing = load_existing()
    date_from = max(existing) if existing else EARLIEST_FROM
    date_to = today_nepal()

    fetched = fetch_range(date_from, date_to)
    print(f"Fetched {len(fetched)} index rows for {date_from}..{date_to}")

    for row in fetched:
        existing[row["published_date"]] = {
            "published_date": row["published_date"],
            "open": row["open"],
            "high": row["high"],
            "low": row["low"],
            "close": row["current"],
            "point_change": row["change_"],
            "pct_change": row["per_change"],
            "turnover": row["turnover"],
        }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "published_date", "open", "high", "low", "close",
                "point_change", "pct_change", "turnover",
            ],
        )
        writer.writeheader()
        for date in sorted(existing):
            writer.writerow(existing[date])

    print(f"Wrote {len(existing)} total index rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()
