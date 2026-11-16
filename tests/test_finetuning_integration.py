"""Check that the preserved notebook and retrieval library share a protocol."""
import ast
import html
import json
import re
import sys
import tempfile
import unittest
from itertools import combinations
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))

from export_finetuning_data import SPLIT_FILES, export_splits
from romansh_retrieval.config import IDIOMS
from romansh_retrieval.data import make_pairs
from romansh_retrieval.eval import eval_pair


def fixture_frame():
    frame = pd.DataFrame({
        idiom: [
            "ina chasa", "ün cudesch", "<b>Allegra</b>&nbsp;!",
            "ina chasa", "text separat", "ultima lingia",
        ]
        for idiom in IDIOMS
    })
    frame.loc[1, IDIOMS[0]] = None
    frame.loc[4, IDIOMS[-1]] = "in cudisch"
    frame["book"] = [f"book-{i}" for i in range(len(frame))]
    frame["chapter"] = [f"chapter-{i}" for i in range(len(frame))]
    return frame


def notebook_protocol():
    """Load only pure definitions, without imports, downloads or training cells."""
    notebook = json.loads((ROOT / "notebooks/finetuning_mediomatix.ipynb").read_text())
    needed = {
        "clean_text", "char_ngrams", "jaccard", "add_overlap_buckets",
        "summarize_ranks", "summarize_by_bucket", "ranks_from_vectors",
        "tfidf_vectors", "build_evaluation",
    }
    namespace = {
        "html": html, "re": re, "np": np, "pd": pd,
        "TfidfVectorizer": TfidfVectorizer, "normalize": normalize,
        "SPACE_RE": re.compile(r"\s+"), "IDIOMS": list(IDIOMS),
        "IDIOM_PAIRS": list(combinations(IDIOMS, 2)), "EVAL_SEED": 13,
    }
    found = set()
    for cell in notebook["cells"]:
        if cell["cell_type"] != "code":
            continue
        definitions = [
            node for node in ast.parse("".join(cell["source"])).body
            if isinstance(node, ast.FunctionDef) and node.name in needed
        ]
        for node in definitions:
            found.add(node.name)
        if definitions:
            code = compile(ast.Module(body=definitions, type_ignores=[]),
                           "finetuning_notebook_definitions", "exec")
            exec(code, namespace)
    if found != needed:
        raise AssertionError(f"Missing notebook definitions: {needed - found}")
    return namespace


class FineTuningIntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.protocol = notebook_protocol()

    def assert_protocol_matches(self, frame, max_rows):
        nb = self.protocol
        cleaned = frame.copy()
        for idiom in IDIOMS:
            cleaned[idiom] = cleaned[idiom].map(nb["clean_text"])
        notebook_pairs, _ = nb["build_evaluation"](cleaned, max_rows)
        for (left, right), (pairs, _, thresholds) in notebook_pairs.items():
            for src, tgt, queries, candidates in [
                (left, right, pairs.src_text.tolist(), pairs.tgt_text.tolist()),
                (right, left, pairs.tgt_text.tolist(), pairs.src_text.tolist()),
            ]:
                with self.subTest(src=src, tgt=tgt):
                    query_vectors, candidate_vectors = nb["tfidf_vectors"](
                        queries, candidates
                    )
                    ranks = nb["ranks_from_vectors"](
                        query_vectors, candidate_vectors, pairs.gold.to_numpy(), 2
                    )
                    expected = [
                        {**row, **thresholds}
                        for row in nb["summarize_by_bucket"](ranks, pairs.bucket)
                    ]
                    actual = eval_pair(
                        make_pairs(frame, src, tgt, max_rows=max_rows, seed=13),
                        "tfidf", batch_size=2,
                    )
                    self.assertEqual(expected, actual)

    def test_all_twenty_directions_match_after_sampling_and_cleaning(self):
        self.assert_protocol_matches(fixture_frame(), max_rows=4)

    def test_duplicate_candidates_and_empty_overlap_groups_match(self):
        frame = pd.DataFrame({idiom: ["same text"] * 4 for idiom in IDIOMS})
        self.assert_protocol_matches(frame, max_rows=0)
        rows = eval_pair(make_pairs(frame, IDIOMS[0], IDIOMS[1]), "tfidf")
        by_bucket = {row["bucket"]: row for row in rows}
        self.assertEqual(by_bucket["all"]["recall_at_1"], 1.0)
        self.assertEqual(by_bucket["low"]["n"], 0)
        self.assertEqual(by_bucket["high"]["n"], 4)


class FineTuningExportTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.raw = Path(self.temp.name) / "raw"
        self.out = Path(self.temp.name) / "export"
        self.raw.mkdir()
        self.frame = fixture_frame()
        for split in SPLIT_FILES:
            self.frame.to_parquet(self.raw / f"{split}.parquet", index=False)

    def test_export_preserves_rows_metadata_and_unprocessed_unicode(self):
        paths = export_splits(self.raw, self.out)
        self.assertEqual({p.name for p in paths.values()},
                         {"train.jsonl", "valid.jsonl", "test.jsonl"})
        for split, path in paths.items():
            records = [json.loads(line) for line in path.read_text().splitlines()]
            self.assertEqual(len(records), len(self.frame))
            self.assertEqual(records[2][IDIOMS[0]], "<b>Allegra</b>&nbsp;!")
            self.assertEqual(records[1][IDIOMS[-1]], "ün cudesch")
            self.assertIsNone(records[1][IDIOMS[0]])
            self.assertEqual(records[-1]["book"], "book-5")
            exported = pd.read_json(path, lines=True)
            for left, right in combinations(IDIOMS, 2):
                pd.testing.assert_frame_equal(
                    make_pairs(self.frame, left, right),
                    make_pairs(exported, left, right),
                )

    def test_existing_destination_is_never_overwritten(self):
        self.out.mkdir()
        existing = self.out / "valid.jsonl"
        existing.write_text("keep this original input\n")
        with self.assertRaises(FileExistsError):
            export_splits(self.raw, self.out)
        self.assertEqual(existing.read_text(), "keep this original input\n")
        self.assertFalse((self.out / "train.jsonl").exists())

    def test_missing_idiom_fails_before_any_export_is_written(self):
        self.frame.drop(columns=[IDIOMS[0]]).to_parquet(
            self.raw / "test.parquet", index=False
        )
        with self.assertRaisesRegex(ValueError, "test is missing idiom columns"):
            export_splits(self.raw, self.out)
        self.assertFalse(self.out.exists())


if __name__ == "__main__":
    unittest.main()
