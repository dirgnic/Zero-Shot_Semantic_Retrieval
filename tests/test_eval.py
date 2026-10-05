import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from romansh_retrieval.data import make_pairs
from romansh_retrieval.eval import eval_pair


class EvalTest(unittest.TestCase):
    def test_tfidf_retrieval_finds_easy_matches(self):
        frame = pd.DataFrame(
            {
                "rm-sursilv": ["ina casa", "il cudisch", "igl utschi"],
                "rm-vallader": ["ina chasa", "il cudesch", "igl utsche"],
            }
        )
        pairs = make_pairs(frame, "rm-sursilv", "rm-vallader")

        rows = eval_pair(pairs, method="tfidf", batch_size=2)
        all_row = next(row for row in rows if row["bucket"] == "all")

        self.assertEqual(all_row["n"], 3)
        self.assertGreaterEqual(all_row["recall_at_1"], 2 / 3)


if __name__ == "__main__":
    unittest.main()
