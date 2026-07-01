import time
import requests
from pathlib import Path

from constants.companyIdMap import companyIdMap
from constants.url import historyUrl
from utils.session import make_session, prime_session, TIMEOUT
from utils.params import build_history_payload
from utils.history import page_starts, records_to_dataframe, records_total, AuthError

OUT_DIR = Path("../data/company-wise")
PAGE_SIZE = 50  # the API silently returns an empty result for length >= 100
DELAY = 0.3  # polite delay between requests (seconds)
MAX_ATTEMPTS = 4  # per company, refreshing the CSRF token between attempts


def _post(session, token, company_id, start, length):
    time.sleep(DELAY)
    payload = build_history_payload(start, length, company_id, token)
    resp = session.post(historyUrl, data=payload, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def fetch_history(session, token, company_id, size=PAGE_SIZE):
    """Fetch all history rows for a company (newest-first). Raises AuthError if
    the API returns an error payload (caller refreshes the token and retries)."""
    first = _post(session, token, company_id, 0, 1)
    total = records_total(first)
    rows = []
    for start in page_starts(total, size):
        page = _post(session, token, company_id, start, size)
        records_total(page)  # guard: a mid-pagination error must not be silent
        rows.extend(page.get("data", []))
    return rows


def collect_company(session, token, symbol, company_id):
    """Return (rows, token). rows is None on failure, [] if genuinely untraded.
    Refreshes the CSRF token and retries on auth/HTTP/timeout errors."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            print(f"Collecting {symbol} (id={company_id}) [attempt {attempt}]...")
            return fetch_history(session, token, company_id), token
        except (AuthError, requests.RequestException) as exc:
            print(f"  issue ({type(exc).__name__}): {exc}; refreshing token")
            time.sleep(2)
            try:
                token = prime_session(session)
            except requests.RequestException:
                pass
        except Exception as exc:  # noqa: BLE001 - keep the run alive
            print(f"  FAILED {symbol}: {exc}")
            return None, token
    return None, token


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    session = make_session()
    token = prime_session(session)

    seeded = skipped = empty = failed = 0
    for symbol, company_id in companyIdMap.items():
        out_file = OUT_DIR / f"{symbol}.csv"
        if out_file.exists():
            skipped += 1
            continue

        rows, token = collect_company(session, token, symbol, company_id)
        if rows is None:
            failed += 1
            continue
        if not rows:
            print(f"  no records for {symbol} (untraded)")
            empty += 1
            continue

        df = records_to_dataframe(rows)
        df.to_csv(out_file, index=False)
        print(f"  wrote {len(df)} rows -> {out_file.name}")
        seeded += 1

    print(f"\nDone. seeded={seeded} skipped={skipped} empty={empty} failed={failed}")


if __name__ == "__main__":
    main()
