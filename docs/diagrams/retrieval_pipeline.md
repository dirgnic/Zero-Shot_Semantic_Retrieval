# Retrieval Pipeline Diagrams

Each idiom direction uses the same aligned queries, candidates, and lexical
overlap buckets for every selected retrieval system.

The validation figures show the three-system smoke check and the 20-direction
TF-IDF run. [Validation results](validation_results.md)

## Mind Map

```mermaid
mindmap
  root((Cross-Idiom Retrieval))
    Data
      Mediomatix aligned corpus
      Splits
        train
        validation gold set
        test
        no_surm
      Idioms
        rm-sursilv
        rm-sutsilv
        rm-surmiran
        rm-puter
        rm-vallader
    Pairing
      Pick source idiom
      Pick target idiom
      Keep rows with both texts
      Gold target is same aligned row
    Classification
      Character 3-5 grams
      Jaccard lexical overlap
      Quantile buckets
        low bottom third
        mid middle third
        high top third
    Retrieval Methods
      TF-IDF baseline
      Zero-shot embeddings optional
        Multilingual MiniLM
        Pretrained XLM-R
    Evaluation
      Rank all target candidates
      Recall@1
      MRR
      Mean rank
      Reports by model, idiom direction, and bucket
```

## Process Flow

```mermaid
flowchart TD
    Data["Aligned Mediomatix split"] --> Rows["Clean and sample rows by idiom direction"]
    Rows --> Pairs["Shared queries, candidates, and gold row IDs"]
    Pairs --> Lexical["Character TF-IDF"]
    Pairs --> MiniLM["Multilingual MiniLM"]
    Pairs --> XLMR["Pretrained XLM-R with masked mean pooling"]
    Pairs --> Buckets["Low, mid, and high lexical overlap"]
    Lexical --> Ranking["Cosine ranking within each system"]
    MiniLM --> Ranking
    XLMR --> Ranking
    Ranking --> Gold["Rank of each gold target"]
    Gold --> Metrics["Recall@1, MRR, and mean rank"]
    Buckets --> Metrics
    Metrics --> Reports["CSV and JSON by model, direction, and bucket"]

    classDef lexical fill:#fef3d7,stroke:#9a6714,color:#533300
    classDef embedding fill:#e8f0fc,stroke:#406da9,color:#142d51
    class Lexical lexical
    class MiniLM,XLMR embedding
```

The default run uses TF-IDF. Add `--methods tfidf embeddings` to compare all
three systems. MiniLM uses its saved pooling. XLM-R averages the final token
vectors over non-padding positions. Both embedding models use L2 normalization
and a default limit of 128 input tokens.

## Lexical-Overlap Classification

```mermaid
flowchart TD
    Pair["Aligned source and gold target"] --> Grams["Character 3–5 grams"]
    Grams --> Overlap["Jaccard overlap score"]
    Overlap --> Upper{"Score at or above q67?"}
    Upper -->|Yes| High["High overlap"]
    Upper -->|No| Lower{"Score at or below q33?"}
    Lower -->|Yes| Low["Low overlap"]
    Lower -->|No| Mid["Mid overlap"]
```

The 33rd and 67th percentiles come from the sampled aligned rows for each idiom
direction. The high bucket takes precedence when both thresholds coincide.

## PCR-Style Summary

| Process | Classify | Report |
| --- | --- | --- |
| Clean and sample aligned rows for each idiom direction. | Assign overlap buckets from the source and gold target texts. | Rank candidates independently for each system and summarize by model, direction, and bucket. |

## Data Separation

| Split | Role in this branch |
| --- | --- |
| `train` | Available for later training/fine-tuning coordination. |
| `validation` | Default gold-standard retrieval evaluation split. |
| `test` | Held for final selected settings. |
| `no_surm` | Extra aligned split without Surmiran coverage. |

## Interpretation

High-overlap rows are the easiest lexical-control condition. Low-overlap rows
are the main RQ2 condition because they show where spelling similarity is less
helpful and semantic retrieval should matter more.
