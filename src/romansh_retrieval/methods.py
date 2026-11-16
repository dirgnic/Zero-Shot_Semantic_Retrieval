from __future__ import annotations

from collections.abc import Sequence

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

from .config import DEFAULT_MAX_SEQ_LENGTH, XLM_R_MODEL


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


def load_embedding_model(
    model_name: str,
    max_seq_length: int = DEFAULT_MAX_SEQ_LENGTH,
    device: str | None = None,
):
    """Load an inference-only encoder; raw XLM-R gets explicit mean pooling."""
    try:
        from sentence_transformers import SentenceTransformer, models
    except ImportError as exc:
        raise RuntimeError(
            "Embedding runs need sentence-transformers. "
            "Install it with: pip install -r requirements-embeddings.txt"
        ) from exc

    if model_name in (XLM_R_MODEL, "xlm-roberta-base"):
        transformer = models.Transformer(model_name, max_seq_length=max_seq_length)
        pooling = models.Pooling(
            transformer.get_word_embedding_dimension(), pooling_mode="mean"
        )
        model = SentenceTransformer(modules=[transformer, pooling], device=device)
    else:
        model = SentenceTransformer(model_name, device=device)
        model.max_seq_length = max_seq_length
    model.eval()
    return model


def embedding_vectors(
    queries: Sequence[str],
    candidates: Sequence[str],
    model_name: str,
    batch_size: int = 64,
    *,
    model=None,
) -> tuple[np.ndarray, np.ndarray]:
    if model is None:
        model = load_embedding_model(model_name)
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
