from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize


def tfidf_vectors(
    queries: Sequence[str],
    candidates: Sequence[str],
    min_n: int = 3,
    max_n: int = 5,
):
    vec = TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(min_n, max_n),
        lowercase=True,
        strip_accents=None,
    )
    vec.fit(list(queries) + list(candidates))
    query_vecs = normalize(vec.transform(queries))
    cand_vecs = normalize(vec.transform(candidates))
    return query_vecs, cand_vecs


def embedding_vectors(
    queries: Sequence[str],
    candidates: Sequence[str],
    model_name: str,
    batch_size: int = 64,
) -> tuple[np.ndarray, np.ndarray]:
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError as exc:
        raise RuntimeError(
            "Embedding runs need sentence-transformers. "
            "Install it with: pip install -r requirements-embeddings.txt"
        ) from exc

    model = SentenceTransformer(model_name)
    query_vecs = model.encode(
        list(queries),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    cand_vecs = model.encode(
        list(candidates),
        batch_size=batch_size,
        convert_to_numpy=True,
        normalize_embeddings=True,
        show_progress_bar=True,
    )
    return query_vecs, cand_vecs
