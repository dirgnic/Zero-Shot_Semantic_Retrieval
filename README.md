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

The semantic experiments include two encoders, both used without any Romansh
task-specific fine-tuning:

| Model | Role | Sentence embedding |
| --- | --- | --- |
| `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Off-the-shelf multilingual semantic baseline | Its trained sentence-transformer with mean pooling |
| `FacebookAI/xlm-roberta-base` | Pretrained XLM-R baseline for the teammate's fine-tuned XLM-R | Attention-mask-aware mean pooling of the final hidden states |

Both use a maximum input length of 128 tokens by default, L2-normalized
embeddings, and cosine similarity. No training or parameter updates occur.
"Zero-shot" refers to the Romansh task; MiniLM already has sentence-embedding
training from its original authors. Raw XLM-R was pretrained for masked language
modeling, so its retrieval performance need not match a sentence-trained model.

To measure the effect of the teammate's fine-tuning, match their pooling,
tokenizer/truncation settings, normalization, and scoring with this XLM-R
baseline. Use identical held-out queries, candidates, idiom directions, and
lexical-overlap buckets. Different base models compare complete approaches;
XLM-R before/after adaptation measures the effect of fine-tuning.

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
  --max-rows 1000
```

This runs TF-IDF once and both MiniLM and XLM-R on the same sampled rows.
Each model is loaded once and reused across idiom directions. CSV/JSON reports
identify each model, input length, similarity, and sampling seed; summaries keep
models separate rather than averaging their scores together.

Run just the unfine-tuned XLM-R baseline:

```bash
python3 scripts/run_retrieval.py \
  --split validation --methods embeddings \
  --model FacebookAI/xlm-roberta-base \
  --max-seq-length 128 --batch-size 16
```

`--model` retains single-model behavior. Use `--models MODEL_A MODEL_B` for
an explicit list, including a locally saved sentence-transformer checkpoint.
For a raw fine-tuned Hugging Face checkpoint, wrap it with the same mean pooling
as XLM-R before comparing; a model's saved sentence-transformer pooling is
otherwise preserved. The script defaults to TF-IDF unless `embeddings` is
included in `--methods`.

First run a small real-model check (downloads the model weights on first use):

```bash
make test
make smoke-embeddings
python3 scripts/summarize_report.py reports/smoke_embeddings/retrieval_validation.csv
```

Use `--device cpu` to force CPU inference, and reduce `--batch-size` if memory
is limited. Use `--max-rows 0` for the full split. Reports for the same split
replace earlier files in the chosen `--out-dir`; use different output
directories to retain separate runs. Report the full split for final comparisons,
or use exactly the same sample size and seed for every system.
