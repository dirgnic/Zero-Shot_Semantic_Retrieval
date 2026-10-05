#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from romansh_retrieval.config import DEFAULT_MODEL, SPLITS, all_pairs
from romansh_retrieval.data import load_split, make_pairs
from romansh_retrieval.eval import eval_pair


def parse_args():
    parser = argparse.ArgumentParser(description="Run Romansh retrieval experiments.")
    parser.add_argument("--split", default="validation", choices=SPLITS)
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--out-dir", default="reports")
    parser.add_argument(
        "--pairs",
        default="all",
        help="Use 'all' or comma-separated pairs like rm-sursilv:rm-vallader.",
    )
    parser.add_argument(
        "--methods",
        nargs="+",
        default=["tfidf"],
        choices=["tfidf", "embeddings"],
    )
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--max-rows", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=13)
    return parser.parse_args()


def parse_pairs(value: str):
    if value == "all":
        return all_pairs()

    pairs = []
    for item in value.split(","):
        src, sep, tgt = item.partition(":")
        if not sep:
            raise ValueError(f"Bad pair '{item}'. Expected src:tgt.")
        pairs.append((src.strip(), tgt.strip()))
    return tuple(pairs)


def main():
    args = parse_args()
    frame = load_split(args.split, args.data_dir)
    max_rows = None if args.max_rows == 0 else args.max_rows
    rows = []

    for src, tgt in parse_pairs(args.pairs):
        pairs = make_pairs(frame, src, tgt, max_rows=max_rows, seed=args.seed)
        if pairs.empty:
            print(f"skip {src}->{tgt}: no aligned rows")
            continue

        for method in args.methods:
            print(f"running {method}: {src}->{tgt} ({len(pairs):,} rows)")
            result = eval_pair(
                pairs,
                method=method,
                model_name=args.model,
                batch_size=args.batch_size,
            )
            for row in result:
                row.update(
                    {
                        "split": args.split,
                        "method": method,
                        "src": src,
                        "tgt": tgt,
                        "model": args.model if method == "embeddings" else "char_tfidf",
                    }
                )
            rows.extend(result)

    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_csv = out_dir / f"retrieval_{args.split}.csv"
    out_json = out_dir / f"retrieval_{args.split}.json"
    report = pd.DataFrame(rows)
    report.to_csv(out_csv, index=False)
    out_json.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(report.to_string(index=False))
    print(f"wrote {out_csv}")


if __name__ == "__main__":
    main()
