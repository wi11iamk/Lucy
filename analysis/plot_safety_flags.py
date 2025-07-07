"""
Plot weekly count of responses flagged by the safety filter.

Usage
-----
python -m analysis.plot_safety_flags \
    --log-path logs/interaction_log.jsonl \
    --out docs/img/safety_flags.png
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def load_weeks(log_path: pathlib.Path) -> pd.Series:
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")
    weeks = []
    with log_path.open() as fh:
        for line in fh:
            j = json.loads(line)
            if "⚠️" in j["llm_response"]:
                date = dt.date.fromisoformat(j["timestamp"][:10])
                iso_year, iso_week, _ = date.isocalendar()
                weeks.append(f"{iso_year}-W{iso_week:02d}")
    if not weeks:
        raise ValueError("No safety-flagged responses found in log.")
    return pd.Series(weeks)


def plot(week_series: pd.Series, out_file: pathlib.Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    counts = week_series.value_counts().sort_index()
    plt.figure(figsize=(10, 4))
    counts.plot(kind="bar")
    plt.title("Safety-flagged responses per ISO week")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig(out_file)
    plt.close()


def cli(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Plot safety flag counts.")
    parser.add_argument(
        "--log-path", type=pathlib.Path, default="logs/interaction_log.jsonl"
    )
    parser.add_argument("--out", type=pathlib.Path, default="docs/img/safety_flags.png")
    args = parser.parse_args(argv)

    weeks = load_weeks(args.log_path)
    plot(weeks, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":  # pragma: no cover
    cli()
