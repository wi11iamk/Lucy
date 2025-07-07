"""
Plot daily average of the *top* emotion score in logs/interaction_log.jsonl.

Usage
-----
python -m analysis.plot_emotions \
    --log-path logs/interaction_log.jsonl \
    --out docs/img/emotion_trend.png
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import pathlib
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def load_records(log_path: pathlib.Path) -> List[dict]:
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_path}")
    records = []
    with log_path.open() as fh:
        for line in fh:
            j = json.loads(line)
            ts = dt.date.fromisoformat(j["timestamp"][:10])
            if j["emotion_scores"]:
                top_score = max(j["emotion_scores"].values())
                records.append({"date": ts, "score": top_score})
    if not records:
        raise ValueError("No emotion_scores found in log.")
    return records


def plot(records: List[dict], out_file: pathlib.Path) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df = pd.DataFrame(records).groupby("date").mean()
    plt.figure()
    df["score"].plot(marker="o")
    plt.title("Average top-emotion score per day")
    plt.ylabel("Score (0-1)")
    plt.xlabel("Date")
    plt.tight_layout()
    plt.savefig(out_file)
    plt.close()


def cli(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Plot emotion trend.")
    parser.add_argument(
        "--log-path", type=pathlib.Path, default="logs/interaction_log.jsonl"
    )
    parser.add_argument(
        "--out", type=pathlib.Path, default="docs/img/emotion_trend.png"
    )
    args = parser.parse_args(argv)

    records = load_records(args.log_path)
    plot(records, args.out)
    print(f"Wrote {args.out}")


if __name__ == "__main__":  # pragma: no cover
    cli()
