# Branch integration record

This integration combines every non-empty branch with work not already in
`main`, based on the branch heads inspected on 16 November 2026.

| Source | Pinned head | Work retained |
| --- | --- | --- |
| `main` | `7680b0d75701a58714113424c5247560e2e25ee7` | La Quotidiana quality notebook, cleaning report/counts and labelled audit. |
| `fine_tuning` | `e21a97d278ec6aa3df561b8c1394f73209c7d44e` | One unmerged commit: XLM-R notebook, training log and test summaries. |
| `retrieval_pipeline_implementation` | `a6db921f133395098a4b6417ee3e754fe782c0c9` | Sixteen unmerged commits: retrieval package, CLI tools, tests, diagrams and validation documentation. |

The two source branch heads become ancestors of the integration branch through
merge commits. Their individual commit authors and histories remain available.
The pull request targets `main`; opening it does not move `main` or remove any
source branch.

## Preservation and conflict decisions

- Every original tracked file on `main` is retained. All data-quality notebook,
  report, counts, audit and original `gitignore` bytes remain unchanged.
- The fine-tuning notebook and all three results CSVs remain byte-identical.
  Notebook outputs and cell metadata are retained.
- Retrieval source files, existing tests, diagrams, base requirements and
  optional embedding requirements remain byte-identical.
- The integration originally preserved three branch README snapshots. They remain accessible in [the last revision before documentation cleanup](https://github.com/dirgnic/Zero-Shot_Semantic_Retrieval/tree/63f0540534840d7957f7d4b8a74b9e025c90c05b). The root README now contains the current project instructions.
- The add/add conflict in `.gitignore` is resolved by retaining both entire
  rule sets, plus ignore rules for generated JSONL inputs. No pattern was
  discarded. The original non-dot `data_quality/gitignore` stays in place;
  a byte-identical `data_quality/.gitignore` activates it.
- The original Makefile remains a byte-identical prefix. Two appended targets
  fetch all training/evaluation splits and export notebook inputs.
- No file deletion is part of the integration.

## Connecting the workflows

`scripts/export_finetuning_data.py` connects the retrieval downloader's Parquet
files to the notebook's JSONL inputs. It preserves all rows, columns and split
boundaries, maps `validation` to `valid.jsonl`, validates the idiom schema before
writing, and refuses to overwrite existing destinations. Exclusive creation
also protects against a destination appearing after validation.

The notebook and retrieval runner retain their existing implementations.
`tests/test_finetuning_integration.py` loads only pure notebook definitions and
checks their agreement with the package for all twenty directions, deterministic
sampling/cleaning, TF-IDF ranks, overlap quantiles, duplicate candidates and empty
buckets. Export tests check the data handoff, missing idiom columns and retained
existing inputs. These tests do not download weights or run training cells.

The base retrieval environment stays lightweight. Optional
`requirements-finetuning.txt` and `requirements-data-quality.txt` describe the
additional notebook dependencies. Model checkpoints and generated corpora are
not added to Git.

## Scientific scope

The data-quality notebook studies `ZurichNLP/quotidiana`, configuration
`1997_2008`. The parallel retrieval and training task uses aligned Mediomatix.
The older branch README's planned `mediomatix-raw` quality study is preserved
as historical text, but is not described as the implemented quality analysis.

Committed results remain the source branches' recorded experiments. No new
performance result is implied by merging them. Full-corpus cleaning, checkpoint
downloads and GPU fine-tuning are not run as part of this integration. Candidate
pool sizes and encoder wrappers must match before interpreting score differences.

## Validation performed

- All 16 unit/integration tests passed, including the original 11 tests.
- The two notebooks pass `nbformat` validation; all 38 code cells compile
  without executing model downloads, cleaning or training.
- A temporary Parquet fixture was exported to all three JSONL inputs, evaluated
  through the CLI over all twenty directions, and summarized successfully
  (80 metric rows).
- All CLI help entry points load, and local Markdown links resolve.
- A preservation audit checked all 36 source-branch file snapshots. The only
  adaptations are the explicitly documented README/ignore/Makefile combinations;
  all original content remains available.
- The diff against `main` contains no deleted files or removed lines. The
  whitespace check passes outside the two exact legacy README snapshots noted
  above.
