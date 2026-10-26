"""Tests for seance. Ollama is mocked — no model or network needed."""

import sys
import unittest
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from seance import channel, list_spirits
from seance.__main__ import build_prompt, summon


class TestSpirits(unittest.TestCase):
    def test_four_spirits_listed(self):
        names = [name for _, name, _, _ in list_spirits()]
        self.assertEqual(names, ["COBOL", "FORTRAN", "BASIC", "ALGOL"])

    def test_offline_reply_is_deterministic(self):
        q = "Will my code outlive me?"
        self.assertEqual(channel("cobol", q), channel("cobol", q))

    def test_different_spirits_answer_differently(self):
        q = "Will my code outlive me?"
        replies = {channel(s, q) for s in ("cobol", "fortran", "basic", "algol")}
        self.assertEqual(len(replies), 4)

    def test_different_questions_answer_differently(self):
        replies = {channel("basic", q) for q in ("a?", "b?", "c?", "d?", "e?")}
        self.assertGreater(len(replies), 1)

    def test_unknown_spirit_raises(self):
        with self.assertRaises(KeyError):
            summon("rust", "hello?", offline=True)

    def test_offline_flag_reports_fallback_source(self):
        _, source = summon("fortran", "hello?", offline=True)
        self.assertIn("offline fallback", source)

    def test_model_reply_used_when_available(self):
        with mock.patch("seance.__main__.ask_model", return_value="BOO."):
            reply, source = summon("cobol", "hello?")
        self.assertEqual(reply, "BOO.")
        self.assertIn("gemma3", source)

    def test_model_failure_falls_back(self):
        with mock.patch("seance.__main__.ask_model", return_value=None):
            reply, source = summon("cobol", "hello?")
        self.assertIn("offline fallback", source)
        self.assertEqual(reply, channel("cobol", "hello?"))

    def test_prompt_names_the_spirit(self):
        prompt = build_prompt("algol", "why did you die?")
        self.assertIn("ALGOL", prompt)
        self.assertIn("why did you die?", prompt)


if __name__ == "__main__":
    unittest.main()
