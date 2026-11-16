import sys
import unittest
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from romansh_retrieval.data import clean_text, make_pairs


class DataTest(unittest.TestCase):
    def test_clean_text_removes_html(self):
        self.assertEqual(clean_text("<strong>Allegra</strong>&nbsp;!"), "Allegra !")

    def test_make_pairs_assigns_gold_after_filtering(self):
        frame = pd.DataFrame(
            {
                "rm-sursilv": ["ina casa", None, "in cudisch"],
                "rm-vallader": ["una chasa", "plain text", "ün cudesch"],
            }
        )

        pairs = make_pairs(frame, "rm-sursilv", "rm-vallader")

        self.assertEqual(len(pairs), 2)
        self.assertEqual(pairs["gold"].tolist(), [0, 1])
        self.assertEqual(pairs["src_text"].tolist(), ["ina casa", "in cudisch"])


if __name__ == "__main__":
    unittest.main()
