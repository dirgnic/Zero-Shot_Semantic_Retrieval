#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from romansh_retrieval.config import (
    DEFAULT_MAX_SEQ_LENGTH,
    DEFAULT_MODELS,
    SPLITS,
    all_pairs,
)
from romansh_retrieval.data import load_split, make_pairs
from romansh_retrieval.eval import eval_pair
from romansh_retrieval.methods import load_embedding_model


def parse_args(argv=None):
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
    model_group = parser.add_mutually_exclusive_group()
    model_group.add_argument("--model", help="Run one embedding model (legacy option).")
    model_group.add_argument(
        "--models",
        nargs="+",
        help="Embedding model IDs. Defaults to multilingual MiniLM and raw XLM-R.",
    )
    parser.add_argument(
        "--max-seq-length",
        type=int,
        default=DEFAULT_MAX_SEQ_LENGTH,
        help="Maximum tokens for every embedding model (default: 128).",
    )
    parser.add_argument("--device", help="Embedding device, e.g. cpu, cuda, or mps.")
    parser.add_argument("--max-rows", type=int, default=1000)
    parser.add_argument("--batch-size", type=int, default=128)
    parser.add_argument("--seed", type=int, default=13)
    args = parser.parse_args(argv)
    model_names = [args.model] if args.model else (args.models or DEFAULT_MODELS)
    args.models = list(dict.fromkeys(model_names))
    if args.batch_size < 1 or args.max_seq_length < 1 or args.max_rows < 0:
        parser.error("batch size and max sequence length must be positive; max rows >= 0")
    return args


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


def run_experiments(frame: pd.DataFrame, args) -> list[dict]:
    max_rows = None if args.max_rows == 0 else args.max_rows
    rows = []
    directions = parse_pairs(args.pairs)

    for method in dict.fromkeys(args.methods):
        model_names = args.models if method == "embeddings" else [None]
        for model_name in model_names:
            # Reuse one loaded model across all directions, then release it before
            # loading the next. Sampling uses the same rows and seed for each model.
            model = (
                load_embedding_model(
                    model_name, max_seq_length=args.max_seq_length, device=args.device
                )
                if method == "embeddings"
                else None
            )
            for src, tgt in directions:
                pairs = make_pairs(frame, src, tgt, max_rows=max_rows, seed=args.seed)
                if pairs.empty:
                    print(f"skip {src}->{tgt}: no aligned rows")
                    continue

                label = model_name or "char_tfidf"
                print(f"running {method} [{label}]: {src}->{tgt} ({len(pairs):,} rows)")
                result = eval_pair(
                    pairs,
                    method=method,
                    model_name=model_name,
                    batch_size=args.batch_size,
                    embedding_model=model,
                )
                for row in result:
                    row.update(
                        {
                            "split": args.split,
                            "method": method,
                            "src": src,
                            "tgt": tgt,
                            "model": label,
                            "max_seq_length": (
                                args.max_seq_length if method == "embeddings" else None
                            ),
                            "similarity": "cosine",
                            "seed": args.seed,
                        }
                    )
                rows.extend(result)
            del model
    return rows


def main():
    args = parse_args()
    frame = load_split(args.split, args.data_dir)
    rows = run_experiments(frame, args)

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
