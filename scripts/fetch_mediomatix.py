#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from romansh_retrieval.config import HF_DATASET, HF_PARQUET_URL, SPLITS


def parse_args():
    parser = argparse.ArgumentParser(description="Download Mediomatix parquet splits.")
    parser.add_argument("--splits", nargs="+", default=["validation"], choices=SPLITS)
    parser.add_argument("--out-dir", default="data/raw")
    parser.add_argument("--force", action="store_true")
    return parser.parse_args()


def download_split(split: str, out_dir: Path, force: bool = False) -> Path:
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / f"{split}.parquet"
    if out_path.exists() and not force:
        print(f"kept {out_path}")
        return out_path

    tmp_path = out_path.with_suffix(".tmp")
    url = HF_PARQUET_URL.format(split=split)
    print(f"downloading {HF_DATASET}:{split}")
    with requests.get(url, stream=True, timeout=60) as response:
        response.raise_for_status()
        with tmp_path.open("wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

    frame = pd.read_parquet(tmp_path)
    tmp_path.replace(out_path)
    print(f"wrote {out_path} ({len(frame):,} rows)")
    return out_path


def main():
    args = parse_args()
    out_dir = Path(args.out_dir)
    for split in args.splits:
        download_split(split, out_dir, force=args.force)


if __name__ == "__main__":
    main()
