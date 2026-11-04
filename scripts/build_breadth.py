"""Aggregate per-company daily prices into market-wide advancers/decliners counts.

Reads data/company-wise/*.csv (one row per company per trading day, with a
per_change column) and writes data/market-breadth.csv with one row per
trading day: advancers, decliners, unchanged, total_traded.
"""
import csv
import glob
from collections import defaultdict
from pathlib import Path

COMPANY_DIR = Path(__file__).resolve().parent.parent / "data" / "company-wise"
OUT_PATH = Path(__file__).resolve().parent.parent / "data" / "market-breadth.csv"


def main():
    counts = defaultdict(lambda: {"advancers": 0, "decliners": 0, "unchanged": 0})

    for path in glob.glob(str(COMPANY_DIR / "*.csv")):
        with open(path, newline="") as f:
            for row in csv.DictReader(f):
                date = row["published_date"]
                per_change = float(row["per_change"])
                if per_change > 0:
                    counts[date]["advancers"] += 1
                elif per_change < 0:
                    counts[date]["decliners"] += 1
                else:
                    counts[date]["unchanged"] += 1

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATH.open("w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["date", "advancers", "decliners", "unchanged", "total_traded"])
        for date in sorted(counts):
            c = counts[date]
            total = c["advancers"] + c["decliners"] + c["unchanged"]
            writer.writerow([date, c["advancers"], c["decliners"], c["unchanged"], total])

    print(f"Wrote {len(counts)} trading days -> {OUT_PATH}")


if __name__ == "__main__":
    main()
