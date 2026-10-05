.PHONY: test fetch smoke

test:
	python3 -m unittest discover -s tests

fetch:
	python3 scripts/fetch_mediomatix.py --splits validation test

smoke:
	python3 scripts/run_retrieval.py --split validation --methods tfidf --max-rows 500
