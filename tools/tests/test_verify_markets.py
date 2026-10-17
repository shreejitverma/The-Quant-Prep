"""Unit tests for tools/qp/verify_markets.py."""

import tempfile
import unittest
from pathlib import Path

from tools.qp.verify_markets import (
    check_frontmatter,
    check_links_and_engines,
    check_style_invariants,
    strip_code_blocks,
)


class TestVerifyMarkets(unittest.TestCase):
    def test_strip_code_blocks(self):
        text = "Hello\n```python\nprint('world')\n```\nAfter"
        stripped = strip_code_blocks(text)
        self.assertEqual(stripped.count("\n"), text.count("\n"))
        self.assertNotIn("print('world')", stripped)
        self.assertIn("Hello", stripped)
        self.assertIn("After", stripped)

    def test_check_frontmatter_valid(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            content = "---\ntype: concept\ntier: core\n---\n# Body\n"
            p.write_text(content, encoding="utf-8")
            meta, body, findings = check_frontmatter(p, content)
            self.assertEqual(meta["type"], "concept")
            self.assertEqual(meta["tier"], "core")
            self.assertEqual(findings, [])

    def test_check_frontmatter_missing_fence(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            content = "# Missing fence\n"
            p.write_text(content, encoding="utf-8")
            _, _, findings = check_frontmatter(p, content)
            self.assertTrue(any(f.rule == "frontmatter" for f in findings))

    def test_check_style_em_dash_and_emoji(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            # em dash test
            content = "This is a sentence — with an em dash.\n"
            p.write_text(content, encoding="utf-8")
            findings = check_style_invariants(p, content)
            self.assertTrue(any(f.rule == "style-em-dash" for f in findings))

            # emoji test
            emoji_content = "This has an emoji: 🚀.\n"
            p.write_text(emoji_content, encoding="utf-8")
            findings_emoji = check_style_invariants(p, emoji_content)
            self.assertTrue(any(f.rule == "style-emoji" for f in findings_emoji))

    def test_sentence_per_line(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            content = "This is the first full sentence that has some length. This is the second full sentence on the exact same line.\n"
            p.write_text(content, encoding="utf-8")
            findings = check_style_invariants(p, content)
            self.assertTrue(any(f.rule == "style-sentence-per-line" for f in findings))

    def test_math_block_delimiters(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "test.md"
            # Unbalanced $$
            content = "Formula: $$ x + y = z \n"
            p.write_text(content, encoding="utf-8")
            findings = check_links_and_engines(p, content)
            self.assertTrue(any(f.rule == "math-block" for f in findings))


if __name__ == "__main__":
    unittest.main()
