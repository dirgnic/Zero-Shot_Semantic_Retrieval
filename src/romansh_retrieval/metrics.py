from __future__ import annotations

from collections.abc import Iterable

import numpy as np


def summarize_ranks(ranks: Iterable[int]) -> dict[str, float]:
    values = np.asarray(list(ranks), dtype=float)
    if values.size == 0:
        return {"n": 0, "recall_at_1": 0.0, "mrr": 0.0, "mean_rank": 0.0}

    return {
        "n": int(values.size),
        "recall_at_1": float(np.mean(values == 1)),
        "mrr": float(np.mean(1.0 / values)),
        "mean_rank": float(np.mean(values)),
    }


def summarize_by_bucket(ranks: Iterable[int], buckets: Iterable[str]) -> list[dict]:
    rank_values = np.asarray(list(ranks), dtype=int)
    bucket_values = np.asarray(list(buckets), dtype=object)

    rows = [{"bucket": "all", **summarize_ranks(rank_values)}]
    for bucket in ("low", "mid", "high"):
        mask = bucket_values == bucket
        rows.append({"bucket": bucket, **summarize_ranks(rank_values[mask])})
    return rows
