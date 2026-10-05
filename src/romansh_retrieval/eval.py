from __future__ import annotations

from collections.abc import Sequence

import numpy as np

from .metrics import summarize_by_bucket
from .methods import embedding_vectors, tfidf_vectors
from .overlap import add_overlap_buckets


def ranks_from_vectors(query_vecs, cand_vecs, gold: Sequence[int], batch_size: int = 128):
    gold = np.asarray(gold, dtype=int)
    ranks = np.empty(len(gold), dtype=int)

    for start in range(0, len(gold), batch_size):
        stop = min(start + batch_size, len(gold))
        scores = query_vecs[start:stop] @ cand_vecs.T
        if hasattr(scores, "toarray"):
            scores = scores.toarray()
        scores = np.asarray(scores)

        for offset, row in enumerate(scores):
            gold_score = row[gold[start + offset]]
            ranks[start + offset] = int(np.sum(row > gold_score) + 1)

    return ranks


def eval_pair(
    pairs,
    method: str,
    model_name: str | None = None,
    batch_size: int = 128,
) -> list[dict]:
    pairs, thresholds = add_overlap_buckets(pairs)
    queries = pairs["src_text"].tolist()
    candidates = pairs["tgt_text"].tolist()

    if method == "tfidf":
        query_vecs, cand_vecs = tfidf_vectors(queries, candidates)
    elif method == "embeddings":
        if not model_name:
            raise ValueError("model_name is required for embedding evaluation.")
        query_vecs, cand_vecs = embedding_vectors(
            queries, candidates, model_name=model_name, batch_size=batch_size
        )
    else:
        raise ValueError("method must be 'tfidf' or 'embeddings'.")

    ranks = ranks_from_vectors(
        query_vecs, cand_vecs, pairs["gold"].to_numpy(), batch_size=batch_size
    )

    rows = summarize_by_bucket(ranks, pairs["bucket"].tolist())
    for row in rows:
        row["low_max"] = thresholds["low_max"]
        row["high_min"] = thresholds["high_min"]
    return rows
