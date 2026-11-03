import contextlib
import io
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

import run_retrieval
from summarize_report import summarize_report

from romansh_retrieval.config import DEFAULT_MODELS, XLM_R_MODEL


class RecordingEncoder:
    """Small deterministic embeddings let us test experiment wiring offline."""

    def __init__(self):
        self.inputs = []

    def encode(self, texts, **kwargs):
        self.inputs.append(list(texts))
        # Each text pair shares a trailing ID, so the correct target ranks first.
        ids = [int(text.rsplit(" ", 1)[1]) for text in texts]
        return np.eye(6, dtype=np.float32)[ids]


class ModelsTest(unittest.TestCase):
    def test_cli_defaults_include_both_baselines(self):
        args = run_retrieval.parse_args(["--methods", "embeddings"])
        self.assertEqual(args.models, list(DEFAULT_MODELS))

    def test_legacy_model_option_selects_only_xlm_r(self):
        args = run_retrieval.parse_args(["--model", XLM_R_MODEL])
        self.assertEqual(args.models, [XLM_R_MODEL])

    def test_invalid_sizes_fail_before_loading_models(self):
        for option, value in (("--batch-size", "0"), ("--max-rows", "-1"),
                              ("--max-seq-length", "0")):
            with self.subTest(option=option), contextlib.redirect_stderr(io.StringIO()):
                with self.assertRaises(SystemExit):
                    run_retrieval.parse_args([option, value])

    def test_models_share_samples_and_are_loaded_once_for_all_directions(self):
        frame = pd.DataFrame({
            "rm-sursilv": [f"source {i}" for i in range(6)],
            "rm-vallader": [f"target {i}" for i in range(6)],
        })
        args = run_retrieval.parse_args([
            "--methods", "tfidf", "embeddings",
            "--pairs", "rm-sursilv:rm-vallader,rm-vallader:rm-sursilv",
            "--max-rows", "3", "--batch-size", "2",
        ])
        encoders = [RecordingEncoder(), RecordingEncoder()]
        with patch.object(run_retrieval, "load_embedding_model", side_effect=encoders) as load:
            with contextlib.redirect_stdout(io.StringIO()):
                rows = run_retrieval.run_experiments(frame, args)

        self.assertEqual(load.call_count, 2)
        self.assertEqual(encoders[0].inputs, encoders[1].inputs)
        self.assertEqual(len(encoders[0].inputs), 4)
        all_rows = [row for row in rows if row["bucket"] == "all"]
        self.assertEqual(len(all_rows), 6)  # Three systems, two directions each.
        for row in all_rows:
            self.assertEqual(row["n"], 3)
            if row["method"] == "embeddings":
                self.assertEqual(row["recall_at_1"], 1.0)
                self.assertEqual(row["max_seq_length"], 128)

    def test_summary_does_not_mix_embedding_models(self):
        rows = pd.DataFrame([
            {"method": "embeddings", "model": model, "bucket": "all",
             "src": "rm-sursilv", "n": 10, "recall_at_1": score,
             "mrr": score, "mean_rank": 2 - score}
            for model, score in zip(DEFAULT_MODELS, (1.0, 0.2))
        ])
        summary = summarize_report(rows).set_index("model")
        self.assertEqual(len(summary), 2)
        self.assertEqual(summary.loc[DEFAULT_MODELS[0], "recall_at_1"], 1.0)
        self.assertEqual(summary.loc[DEFAULT_MODELS[1], "recall_at_1"], 0.2)


if __name__ == "__main__":
    unittest.main()
