import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from main import calculate_score, load_golden_set, evaluate


class GoldenSetTests(unittest.TestCase):
    def test_golden_set_has_30_questions(self):
        items = load_golden_set()
        self.assertEqual(len(items), 30)
        self.assertEqual(items[0]["id"], "Q001")
        self.assertEqual(items[-1]["id"], "Q030")

    def test_score_all_keywords(self):
        score, matched, missing = calculate_score("Tokens split text into units.", ["tokens", "text"])
        self.assertEqual(score, 100.0)
        self.assertEqual(len(matched), 2)
        self.assertEqual(missing, [])

    def test_score_partial_keywords(self):
        score, matched, missing = calculate_score("Tokens are useful.", ["tokens", "vocabulary"])
        self.assertEqual(score, 50.0)
        self.assertEqual(matched, ["tokens"])
        self.assertEqual(missing, ["vocabulary"])

    def test_empty_keyword_list(self):
        self.assertEqual(calculate_score("some answer", []), (0, [], []))

    def test_invalid_golden_set_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.json"
            path.write_text(json.dumps([{"id": "Q1"}]), encoding="utf-8")
            with self.assertRaises(ValueError):
                load_golden_set(path)

    @patch("main.get_llm_answer", return_value="Tokenization splits text into tokens.")
    def test_evaluate_with_mock_model(self, mock_answer):
        sample = [{
            "id": "QTEST",
            "question": "What is tokenization?",
            "expected_answer": "Splitting text into tokens.",
            "keywords": ["splits", "text", "tokens"],
            "source": "https://example.com"
        }]
        rows, total, successful = evaluate(sample)
        self.assertEqual(successful, 1)
        self.assertEqual(rows[0]["Status"], "PASS")
        self.assertEqual(total, 100.0)


if __name__ == "__main__":
    unittest.main()
