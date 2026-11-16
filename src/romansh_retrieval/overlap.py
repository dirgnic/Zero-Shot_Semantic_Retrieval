from __future__ import annotations

import re

import numpy as np
import pandas as pd

SPACE_RE = re.compile(r"\s+")


def char_ngrams(text: str, min_n: int = 3, max_n: int = 5) -> set[str]:
    text = SPACE_RE.sub(" ", text.lower()).strip()
    if not text:
        return set()

    padded = f" {text} "
    grams = set()
    for n in range(min_n, max_n + 1):
        if len(padded) < n:
            grams.add(padded)
            continue
        grams.update(padded[i : i + n] for i in range(len(padded) - n + 1))
    return grams


def jaccard(left: str, right: str, min_n: int = 3, max_n: int = 5) -> float:
    left_grams = char_ngrams(left, min_n=min_n, max_n=max_n)
    right_grams = char_ngrams(right, min_n=min_n, max_n=max_n)
    if not left_grams and not right_grams:
        return 0.0

    overlap = left_grams & right_grams
    union = left_grams | right_grams
    return len(overlap) / len(union)


def add_overlap_buckets(
    pairs: pd.DataFrame,
    low_q: float = 0.33,
    high_q: float = 0.67,
) -> tuple[pd.DataFrame, dict[str, float]]:
    if pairs.empty:
        out = pairs.copy()
        out["overlap"] = []
        out["bucket"] = []
        return out, {"low_max": 0.0, "high_min": 0.0}

    out = pairs.copy()
    out["overlap"] = [
        jaccard(src, tgt) for src, tgt in zip(out["src_text"], out["tgt_text"])
    ]

    values = out["overlap"].to_numpy()
    low_max = float(np.quantile(values, low_q))
    high_min = float(np.quantile(values, high_q))

    out["bucket"] = "mid"
    out.loc[out["overlap"] <= low_max, "bucket"] = "low"
    out.loc[out["overlap"] >= high_min, "bucket"] = "high"
    return out, {"low_max": low_max, "high_min": high_min}
