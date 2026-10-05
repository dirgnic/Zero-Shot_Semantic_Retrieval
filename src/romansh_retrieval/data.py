from __future__ import annotations

import html
import re
from pathlib import Path

import numpy as np
import pandas as pd

from .config import IDIOMS, SPLITS

TAG_RE = re.compile(r"<[^>]+>")
SPACE_RE = re.compile(r"\s+")


def clean_text(value) -> str:
    if value is None or pd.isna(value):
        return ""
    text = html.unescape(str(value))
    text = TAG_RE.sub(" ", text)
    return SPACE_RE.sub(" ", text).strip()


def load_split(split: str, data_dir: str | Path = "data/raw") -> pd.DataFrame:
    if split not in SPLITS:
        raise ValueError(f"Unknown split '{split}'. Use one of: {', '.join(SPLITS)}")

    path = Path(data_dir) / f"{split}.parquet"
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path}. Run scripts/fetch_mediomatix.py --splits {split}"
        )
    return pd.read_parquet(path)


def make_pairs(
    frame: pd.DataFrame,
    src: str,
    tgt: str,
    max_rows: int | None = None,
    seed: int = 13,
) -> pd.DataFrame:
    check_idiom(src)
    check_idiom(tgt)
    if src == tgt:
        raise ValueError("Source and target idioms must differ.")

    pairs = pd.DataFrame(
        {
            "src_idiom": src,
            "tgt_idiom": tgt,
            "src_text": frame[src].map(clean_text),
            "tgt_text": frame[tgt].map(clean_text),
        }
    )
    for col in ("book", "chapter"):
        if col in frame:
            pairs[col] = frame[col]

    pairs = pairs[(pairs["src_text"] != "") & (pairs["tgt_text"] != "")]
    if max_rows and max_rows > 0 and len(pairs) > max_rows:
        pairs = pairs.sample(n=max_rows, random_state=seed).sort_index()

    pairs = pairs.reset_index(drop=True)
    pairs["gold"] = np.arange(len(pairs))
    return pairs


def check_idiom(name: str) -> None:
    if name not in IDIOMS:
        raise ValueError(f"Unknown idiom '{name}'. Use one of: {', '.join(IDIOMS)}")
