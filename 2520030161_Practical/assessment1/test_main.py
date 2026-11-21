import unittest
from main import (
    CORPUS, initial_tokenize, count_pairs, count_tokens,
    merge_pair, train_bpe, train_wordpiece
)


class TokenizerTests(unittest.TestCase):
    def test_initial_character_tokens(self):
        tokens = initial_tokenize(CORPUS)
        self.assertEqual(tokens["low"], ["l", "o", "w"])
        self.assertEqual(tokens["newest"], list("newest"))

    def test_initial_pair_frequencies_from_notes(self):
        pairs = count_pairs(initial_tokenize(CORPUS), CORPUS)
        self.assertEqual(pairs[("l", "o")], 7)
        self.assertEqual(pairs[("o", "w")], 7)
        self.assertEqual(pairs[("e", "s")], 9)
        self.assertEqual(pairs[("s", "t")], 9)

    def test_initial_token_frequency(self):
        counts = count_tokens(initial_tokenize(CORPUS), CORPUS)
        self.assertEqual(counts["l"], 13)
        self.assertEqual(counts["o"], 7)

    def test_merge_pair(self):
        tokens = {"low": ["l", "o", "w"], "lower": ["l", "o", "w", "e", "r"]}
        merged = merge_pair(tokens, ("l", "o"))
        self.assertEqual(merged["low"], ["lo", "w"])
        self.assertEqual(merged["lower"], ["lo", "w", "e", "r"])

    def test_bpe_runs_and_merges(self):
        result = train_bpe()
        self.assertEqual(result.algorithm, "BPE")
        self.assertTrue(result.merges)
        self.assertIn("low", result.final_tokens)

    def test_wordpiece_runs_and_merges(self):
        result = train_wordpiece()
        self.assertEqual(result.algorithm, "WordPiece")
        self.assertTrue(result.merges)
        self.assertIn("wildest", result.final_tokens)


if __name__ == "__main__":
    unittest.main()
