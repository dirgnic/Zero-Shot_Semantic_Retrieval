#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def parse_args():
    parser = argparse.ArgumentParser(description="Summarize retrieval report CSVs.")
    parser.add_argument("report", nargs="?", default="reports/retrieval_validation.csv")
    return parser.parse_args()


def main():
    args = parse_args()
    report = Path(args.report)
    frame = pd.read_csv(report)
    if frame.empty:
        raise SystemExit(f"{report} is empty")

    summary = (
        frame.groupby(["method", "bucket"], as_index=False)
        .agg(
            pairs=("src", "count"),
            rows=("n", "sum"),
            recall_at_1=("recall_at_1", "mean"),
            mrr=("mrr", "mean"),
            mean_rank=("mean_rank", "mean"),
        )
        .sort_values(["method", "bucket"])
    )
    print(summary.to_string(index=False))


if __name__ == "__main__":
    main()
