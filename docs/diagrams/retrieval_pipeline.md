# Retrieval Pipeline Diagrams

These diagrams explain how the retrieval branch separates the data, classifies
lexical-overlap cases, and reports results.

For diagrams based on the TF-IDF validation smoke run, see
[`validation_results.md`](validation_results.md).

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
    Evaluation
      Rank all target candidates
      Recall@1
      MRR
      Mean rank
      Bucket-level comparison
```

## Process Flow

```mermaid
flowchart TD
    A["ZurichNLP/mediomatix"] --> B["Download parquet split"]
    B --> C["Load split: validation by default"]
    C --> D["Choose source-target idiom pair"]
    D --> E["Clean text and strip HTML"]
    E --> F["Drop rows missing source or target text"]
    F --> G["Create aligned pairs"]
    G --> H["Classify lexical overlap"]
    G --> I["Build retrieval representations"]
    H --> J["low / mid / high bucket"]
    I --> K["TF-IDF char n-grams"]
    I --> L["Multilingual embeddings"]
    K --> M["Cosine similarity ranking"]
    L --> M
    J --> N["Bucket labels for analysis"]
    M --> O["Rank of gold aligned target"]
    O --> P["Recall@1, MRR, mean rank"]
    N --> P
    P --> Q["CSV/JSON report"]
```

## Lexical-Overlap Classification

```mermaid
flowchart LR
    A["Source segment"] --> C["Character 3-5 grams"]
    B["Gold target segment"] --> D["Character 3-5 grams"]
    C --> E["Jaccard overlap"]
    D --> E
    E --> F{"Overlap score"}
    F -->|"<= pair q33"| G["low overlap"]
    F -->|"q33 - q67"| H["mid overlap"]
    F -->|">= pair q67"| I["high overlap"]
```

The thresholds are recomputed for each source-target idiom pair, so `low`,
`mid`, and `high` always describe that pair's own lexical-overlap distribution.

## PCR-Style Summary

```mermaid
flowchart LR
    P["Process<br/>download, clean, pair"] --> C["Classify<br/>low / mid / high overlap"]
    C --> R["Report<br/>Recall@1 and MRR by method and bucket"]
```

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
