import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from romansh_retrieval.metrics import summarize_by_bucket, summarize_ranks
from romansh_retrieval.overlap import add_overlap_buckets, jaccard


class OverlapMetricsTest(unittest.TestCase):
    def test_jaccard_is_higher_for_similar_text(self):
        close = jaccard("ina casa", "ina chasa")
        far = jaccard("ina casa", "jeu vom oz")

        self.assertGreater(close, far)

    def test_add_overlap_buckets_keeps_all_labels(self):
        pairs = pd.DataFrame(
            {
                "src_text": ["abc def", "abc def", "abc def"],
                "tgt_text": ["abc def", "abc xyz", "uvw xyz"],
            }
        )

        out, thresholds = add_overlap_buckets(pairs)

        self.assertEqual(set(out["bucket"]), {"low", "mid", "high"})
        self.assertLessEqual(thresholds["low_max"], thresholds["high_min"])

    def test_rank_summary(self):
        self.assertEqual(summarize_ranks([1, 2])["recall_at_1"], 0.5)
        rows = summarize_by_bucket([1, 3], ["low", "high"])

        self.assertEqual(rows[0]["bucket"], "all")
        self.assertEqual(rows[1]["bucket"], "low")
        self.assertEqual(rows[3]["bucket"], "high")


if __name__ == "__main__":
    unittest.main()
