#!/usr/bin/env python3
"""Export the provided Mediomatix splits for the fine-tuning notebook."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from romansh_retrieval.config import IDIOMS
from romansh_retrieval.data import load_split

SPLIT_FILES = {
    "train": "train.jsonl",
    "validation": "valid.jsonl",
    "test": "test.jsonl",
}


def export_splits(data_dir: str | Path, out_dir: str | Path) -> dict[str, Path]:
    """Retain every row/column and refuse to replace any existing destination."""
    frames = {split: load_split(split, data_dir) for split in SPLIT_FILES}
    for split, frame in frames.items():
        missing = sorted(set(IDIOMS) - set(frame.columns))
        if missing:
            raise ValueError(f"{split} is missing idiom columns: {', '.join(missing)}")

    destinations = {
        split: Path(out_dir) / name for split, name in SPLIT_FILES.items()
    }
    for path in destinations.values():
        if path.exists():
            raise FileExistsError(
                f"Refusing to overwrite {path}; choose a new --out-dir"
            )

    Path(out_dir).mkdir(parents=True, exist_ok=True)
    for split, path in destinations.items():
        # Exclusive creation also protects against a file appearing after the check.
        with path.open("x", encoding="utf-8") as stream:
            stream.write(frames[split].to_json(
                orient="records", lines=True, force_ascii=False
            ))
    return destinations


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Export Mediomatix Parquet to the fine-tuning notebook's JSONL."
    )
    parser.add_argument("--data-dir", default="data/raw")
    parser.add_argument("--out-dir", default="data")
    args = parser.parse_args()
    try:
        paths = export_splits(args.data_dir, args.out_dir)
    except (FileNotFoundError, FileExistsError, ValueError) as exc:
        parser.error(str(exc))
    for split, path in paths.items():
        print(f"{split}: wrote {path}")


if __name__ == "__main__":
    main()
