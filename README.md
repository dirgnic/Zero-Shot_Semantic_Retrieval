# Zero-Shot Semantic Retrieval

This project compares lexical similarity with semantic similarity for aligned
Romansh idiom segments from the Mediomatix corpus.

The retrieval task is simple: given one segment in a source idiom, rank all
candidate segments in a target idiom and check whether the aligned segment is
ranked first.

## Data

Main evaluation data:

- Dataset: `ZurichNLP/mediomatix`
- License: CC-BY-NC-SA-4.0
- Splits: `train`, `validation`, `test`, `no_surm`
- Idiom columns: `rm-sursilv`, `rm-sutsilv`, `rm-surmiran`, `rm-puter`,
  `rm-vallader`

The manually aligned `validation` split is the default gold-standard evaluation
set. The noisier corpus named in the proposal feedback is the unaligned
`ZurichNLP/mediomatix-raw` dataset, which belongs to the data-quality branch.

## Baseline And Models

The baseline is character n-gram TF-IDF with cosine similarity. This is a
lexical baseline because it rewards shared spelling patterns across idioms.

The zero-shot semantic model is a multilingual sentence-transformer encoder,
used without Romansh task-specific fine-tuning.

## Lexical-Overlap Split

For each evaluated source-target pair, overlap is measured with character
3- to 5-gram Jaccard similarity on the aligned gold pair. The bottom third is
reported as `low`, the top third as `high`, and the middle third as `mid`.
This makes the RQ2 comparison explicit before model scoring.

## Diagrams

Mind-map, process-flow, and overlap-classification diagrams are in
[`docs/diagrams/retrieval_pipeline.md`](docs/diagrams/retrieval_pipeline.md).
TF-IDF validation-result diagrams are in
[`docs/diagrams/validation_results.md`](docs/diagrams/validation_results.md).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional embedding backend:

```bash
pip install -r requirements-embeddings.txt
```

## Run

Download the aligned Mediomatix data:

```bash
python3 scripts/fetch_mediomatix.py --splits validation test
```

Run a quick TF-IDF retrieval experiment:

```bash
python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 1000
```

Summarize a report:

```bash
python3 scripts/summarize_report.py reports/retrieval_validation.csv
```

Run TF-IDF plus zero-shot embeddings after installing the optional backend:

```bash
python3 scripts/run_retrieval.py \
  --split validation \
  --methods tfidf embeddings \
  --model sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2 \
  --max-rows 1000
```

Use `--max-rows 0` for the full split.
