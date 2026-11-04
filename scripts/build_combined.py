"""Merge market breadth with the NEPSE index and compute the AD Line + moving averages.

Reads data/market-breadth.csv and data/nepse-index.csv, writes data/combined.csv:
date, advancers, decliners, unchanged, total_traded, net_advances, ad_line,
ad_line_ma5, ad_line_ma7, nepse_close, nepse_ma5, nepse_ma7
"""
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
OUT_PATH = DATA_DIR / "combined.csv"


def main():
    breadth = pd.read_csv(DATA_DIR / "market-breadth.csv", parse_dates=["date"])
    index = pd.read_csv(DATA_DIR / "nepse-index.csv", parse_dates=["published_date"])
    index = index.rename(columns={"published_date": "date", "close": "nepse_close"})

    df = breadth.merge(index[["date", "nepse_close"]], on="date", how="left")
    df = df.sort_values("date").reset_index(drop=True)

    df["net_advances"] = df["advancers"] - df["decliners"]
    df["ad_line"] = df["net_advances"].cumsum()
    df["ad_line_ma5"] = df["ad_line"].rolling(5).mean()
    df["ad_line_ma7"] = df["ad_line"].rolling(7).mean()
    df["nepse_ma5"] = df["nepse_close"].rolling(5).mean()
    df["nepse_ma7"] = df["nepse_close"].rolling(7).mean()

    df.to_csv(OUT_PATH, index=False, date_format="%Y-%m-%d")
    print(f"Wrote {len(df)} rows -> {OUT_PATH}")


if __name__ == "__main__":
    main()
