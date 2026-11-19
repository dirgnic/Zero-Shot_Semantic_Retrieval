# Romansh cross-idiom retrieval

Given a passage in one Romansh idiom, this project ranks passages in another to recover the aligned counterpart. It uses Mediomatix schoolbook passages for retrieval and a separate La Quotidiana newspaper corpus for the cleaning audit.

**Start with the [interactive pipeline notebook](notebooks/retrieval_playground.ipynb).** Explore the annotated cleaning audit, rank live Mediomatix candidates, and compare recorded held-out results by lexical overlap. The notebook includes JupyterLab setup instructions. Live fine-tuned retrieval requires a local checkpoint.

## Team contributions

| Member | Contribution |
| --- | --- |
| Sushant Gupta | Developed the La Quotidiana preprocessing pipeline, including text repair, filtering, duplicate and language checks, and a manual audit of flagged examples. [Cleaning notebook](data_quality/ETSP%20Text%20Preprocessing%20Pipeline.ipynb) |
| Ingrid-Adriana Corobana | Implemented the aligned Mediomatix retrieval pipeline across 20 directions, the character TF-IDF, MiniLM and pretrained XLM-R baselines, and the analysis by lexical overlap. [Retrieval package](src/romansh_retrieval/) |
| Marcos Galdona Peñacoba | Implemented contrastive XLM-R fine-tuning, selected checkpoints using validation performance, and evaluated fine-tuned XLM-R against pretrained XLM-R and TF-IDF on the held-out set. [Fine-tuning notebook](notebooks/finetuning_mediomatix.ipynb) |

## Evidence for the report criteria

- **NLP question and findings.** The experiments test whether multilingual encoders recover aligned passages that share little spelling. On the held-out test set, fine-tuned XLM-R reached 78.34% Recall@1 overall versus 39.92% before fine-tuning. TF-IDF scored higher than fine-tuned XLM-R in the high-overlap group (93.48% versus 86.90%). [XLM-R results](results/test_summary.csv) · [Full comparison in the report](https://www.overleaf.com/project/6aee0c96cbcd361b1fc008b5)
- **Reproducibility.** The runner uses the published splits and records the sampling seed and model settings. The [validation documentation](docs/diagrams/validation_results.md) gives the commands and candidate pool sizes. The [data-quality audit](data_quality/audit_sample_labeled.csv) records the human judgments behind the cleaning study.
- **Software engineering.** Data preparation, model scoring, overlap grouping, and metrics live in separate modules. Setup commands below document the workflow, and `make test` checks retrieval logic and integration without downloading checkpoints.

## Install and check

Run commands from the repository root. A separate virtual environment keeps the
optional model and notebook dependencies out of the base retrieval setup.

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install -r requirements.txt
make test
```

The offline tests exercise the retrieval library, shared model/sample wiring,
notebook protocol parity, and the Parquet-to-JSONL bridge. They do not download
encoder weights or claim to reproduce a full training run.

## Shared Mediomatix inputs

Download the provided splits without creating a new partition:

```bash
python3 scripts/fetch_mediomatix.py --splits train validation test
```

The runner consumes `data/raw/{train,validation,test}.parquet`. The notebook
expects `train.jsonl`, `valid.jsonl` and `test.jsonl`. Export the same records:

```bash
python3 scripts/export_finetuning_data.py --data-dir data/raw --out-dir data
```

This preserves row order, idiom columns, missing values and metadata. It performs
no sampling, text cleaning or repartitioning; each workflow retains its own
preprocessing step. `validation.parquet` maps to `valid.jsonl`. The exporter
refuses to overwrite any existing destination; choose another `--out-dir` if
inputs already exist. `make fetch-finetuning` and `make export-finetuning`
provide the same two steps separately.

## Run retrieval baselines

A lexical validation run:

```bash
python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500 --out-dir reports/tfidf-validation
python3 scripts/summarize_report.py reports/tfidf-validation/retrieval_validation.csv
```

For MiniLM and pretrained XLM-R, install the optional backend and use the same
queries/candidates for all three systems:

```bash
python3 -m pip install -r requirements-embeddings.txt
python3 scripts/run_retrieval.py --split validation --methods tfidf embeddings --max-rows 500 --batch-size 16 --out-dir reports/zero-shot-validation
```

The first embedding run downloads the selected checkpoints. Each encoder is
loaded once across directions. Reports retain model names and settings; the
summary keeps different models separate. Choose a **fresh output directory**
for each run because the existing runner names its CSV/JSON files by split.
Use `--model MODEL` for one encoder or `--models MODEL_A MODEL_B` for a custom list.
Use `--device cpu` to run on CPU and `--max-rows 0` to use all aligned rows in the chosen split.

## Run fine-tuning

```bash
python3 -m pip install -r requirements-finetuning.txt
jupyter lab
```

Open `notebooks/finetuning_mediomatix.ipynb` with a kernel whose working directory
is `notebooks/`, so its default `DATA_DIR = Path('../data')` finds the exported
files, or set `DATA_DIR` explicitly. In Colab, upload the same three JSONL files.
The preserved notebook always trains a new model; a GPU is recommended.

Its current configuration uses the original splits, masked mean pooling,
128-token inputs, seed 42 for training, evaluation seed 13, and validation macro
MRR for checkpoint selection. Checkpoints are written under the notebook's
`OUTPUT_DIR` and are intentionally not committed. The committed CSVs in
[results/](results/) are retained records from the fine-tuning branch; merging
them does not rerun or regenerate those experiments.

## Inspect or rerun corpus-quality work

The existing [cleaning report](data_quality/cleaning_report.md),
[counts](data_quality/cleaning_counts.json) and
[labelled audit](data_quality/audit_sample_labeled.csv) can be inspected directly.
To run its notebook, use the optional environment:

```bash
python3 -m pip install -r requirements-data-quality.txt
```

Review the last cell of `data_quality/ETSP Text Preprocessing Pipeline.ipynb`
before executing the full notebook. It calls `main` with `model_v3.bin` for
GlotLID; model/data downloads and full-corpus processing can be substantial.
Choose a separate working/output location to retain the committed reference
report and counts rather than overwriting them with a new run.
The original `data_quality/gitignore` is retained; an identical `.gitignore`
activates those existing rules for future generated files.

## Compare results with matching protocols

- The fine-tuning notebook evaluates both directions for each of ten idiom pairs
  and reports macro averages over all twenty directions.
- The documented retrieval validation run uses 500 candidates per direction;
  the 20-query smoke check is only a wiring check.
- Compare model scores only after matching split, candidate pool, sample size,
  seed, preprocessing, pooling, truncation and overlap groups. The notebook's
  model-selection cell loads `AutoModel`; the runner uses MiniLM's saved
  `SentenceTransformer` wrapper. Real-encoder equivalence is not asserted by
  the offline protocol tests.
- The integration tests check sampling, TF-IDF, Jaccard groups, optimistic ties
  and empty-bucket metrics against the notebook's pure definitions, without
  executing download/training cells.

[Protocol diagrams](docs/diagrams/retrieval_pipeline.md) and
[documented validation results](docs/diagrams/validation_results.md) remain
available alongside the preserved fine-tuning CSVs and corpus-quality reports.
