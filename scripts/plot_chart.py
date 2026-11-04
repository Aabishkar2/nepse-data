"""Render the NEPSE index / AD Line chart from data/combined.csv.

Produces two PNGs under charts/:
  ad_line_recent.png - last ~250 trading days (the actionable view)
  ad_line_full.png   - full history available

Two stacked panels, each on a single y-axis (no dual-axis panels):
  top    - NEPSE index close, 5-day MA, 7-day MA
  bottom - AD Line (cumulative advancers - decliners), 5-day MA, 7-day MA
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "combined.csv"
CHART_DIR = Path(__file__).resolve().parent.parent / "charts"

# Validated categorical slots (dataviz skill default palette), light mode.
RAW_COLOR = "#2a78d6"   # slot 1 blue
MA7_COLOR = "#eb6834"   # slot 2 orange
MA5_COLOR = "#1baf7a"   # slot 3 aqua

SURFACE = "#fcfcfb"
PRIMARY_INK = "#0b0b0b"
SECONDARY_INK = "#52514e"
MUTED = "#898781"
GRID = "#e1e0d9"


def style_axes(ax, title):
    ax.set_title(title, color=PRIMARY_INK, fontsize=11, loc="left", pad=8)
    ax.set_facecolor(SURFACE)
    ax.grid(True, color=GRID, linewidth=0.8)
    ax.tick_params(colors=MUTED, labelsize=8)
    for spine in ax.spines.values():
        spine.set_color(GRID)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m"))


def render(df: pd.DataFrame, out_path: Path, label: str):
    fig, (ax_top, ax_bottom) = plt.subplots(
        2, 1, figsize=(11, 7), sharex=True, facecolor=SURFACE,
        gridspec_kw={"height_ratios": [1, 1], "hspace": 0.25},
    )

    ax_top.plot(df["date"], df["nepse_close"], color=RAW_COLOR, linewidth=1.6, label="NEPSE close")
    ax_top.plot(df["date"], df["nepse_ma5"], color=MA5_COLOR, linewidth=1.1, label="5-day MA")
    ax_top.plot(df["date"], df["nepse_ma7"], color=MA7_COLOR, linewidth=1.1, label="7-day MA")
    style_axes(ax_top, "NEPSE Index")
    ax_top.legend(loc="upper left", frameon=False, fontsize=8, labelcolor=SECONDARY_INK)

    ax_bottom.plot(df["date"], df["ad_line"], color=RAW_COLOR, linewidth=1.6, label="AD Line")
    ax_bottom.plot(df["date"], df["ad_line_ma5"], color=MA5_COLOR, linewidth=1.1, label="5-day MA")
    ax_bottom.plot(df["date"], df["ad_line_ma7"], color=MA7_COLOR, linewidth=1.1, label="7-day MA")
    ax_bottom.axhline(0, color=MUTED, linewidth=0.8)
    style_axes(ax_bottom, "Advance/Decline Line (cumulative advancers − decliners)")
    ax_bottom.legend(loc="upper left", frameon=False, fontsize=8, labelcolor=SECONDARY_INK)

    fig.suptitle(
        f"NEPSE market breadth — {label}  (updated {df['date'].max():%Y-%m-%d})",
        color=PRIMARY_INK, fontsize=12, x=0.01, ha="left",
    )
    fig.autofmt_xdate()
    CHART_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(out_path, dpi=150, facecolor=SURFACE, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {out_path}")


def rebase_ad_line(df: pd.DataFrame) -> pd.DataFrame:
    """Shift the AD line (and its MAs) so the window starts at 0.

    The AD line is cumulative since 1995, so its absolute level in any short
    window is a huge arbitrary offset (tens of thousands) that would otherwise
    flatten the recent-window plot. Rebasing shows the quantity that actually
    matters for a short window: net breadth change since the window started.
    """
    df = df.copy()
    offset = df["ad_line"].iloc[0]
    for col in ("ad_line", "ad_line_ma5", "ad_line_ma7"):
        df[col] = df[col] - offset
    return df


def main():
    df = pd.read_csv(DATA_PATH, parse_dates=["date"])
    render(df, CHART_DIR / "ad_line_full.png", "full history")
    recent = rebase_ad_line(df.tail(250).reset_index(drop=True))
    render(recent, CHART_DIR / "ad_line_recent.png", "last 250 trading days, AD line rebased to 0 at window start")


if __name__ == "__main__":
    main()
