.PHONY: test fetch smoke smoke-embeddings summarize

test:
	python3 -m unittest discover -s tests

fetch:
	python3 scripts/fetch_mediomatix.py --splits validation test

smoke:
	python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500

smoke-embeddings:
	python3 scripts/run_retrieval.py --split validation --methods tfidf embeddings --pairs rm-sursilv:rm-vallader --max-rows 20 --batch-size 4 --out-dir reports/smoke_embeddings

summarize:
	python3 scripts/summarize_report.py reports/retrieval_validation.csv
