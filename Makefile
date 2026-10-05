.PHONY: test fetch smoke summarize

test:
	python3 -m unittest discover -s tests

fetch:
	python3 scripts/fetch_mediomatix.py --splits validation test

smoke:
	python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500

summarize:
	python3 scripts/summarize_report.py reports/retrieval_validation.csv
