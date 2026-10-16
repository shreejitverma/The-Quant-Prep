"""Behaviour tests for tools/run_examples.py: discovery rules and failure reporting."""

from __future__ import annotations

import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from tools import run_examples

GUARD = 'if __name__ == "__main__":\n'


class RunExamples(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.write("01-Alpha/README.md", "---\ntype: moc\n---\n\n# Alpha\n")
        self.write("01-Alpha/code/good.py", GUARD + "    print('ok')\n")
        self.write("01-Alpha/code/bad.py", GUARD + "    assert 1 + 1 == 3, 'drifted'\n")
        self.write("01-Alpha/code/helpers.py", "def f():\n    return 1\n")  # a module, not an example
        self.write("01-Alpha/code/sub/deep.py", GUARD + "    pass\n")
        self.write("01-Alpha/code/slow.py", "# qp-examples: skip needs a GPU\n" + GUARD + "    raise SystemExit(1)\n")
        self.write("01-Alpha/notes.py", GUARD + "    raise SystemExit(1)\n")  # outside code/
        self.write("02-Library/README.md", "---\ncurriculum: false\n---\n\n# Library\n")
        self.write("02-Library/code/lib.py", GUARD + "    raise SystemExit(1)\n")

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, rel: str, text: str) -> None:
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")

    def main(self, *argv: str) -> tuple[int, str]:
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = run_examples.main(["--root", str(self.root), *argv])
        return code, out.getvalue()

    def test_discovers_only_guarded_scripts_in_curriculum_code_folders(self):
        found = {e.path.as_posix(): e.skip for e in run_examples.discover(self.root)}
        self.assertEqual(
            found,
            {
                "01-Alpha/code/bad.py": None,
                "01-Alpha/code/good.py": None,
                "01-Alpha/code/slow.py": "needs a GPU",
                "01-Alpha/code/sub/deep.py": None,
            },
        )

    def test_failing_example_fails_the_run_and_is_reported(self):
        code, out = self.main()
        self.assertEqual(code, 1)
        self.assertIn("FAIL  01-Alpha/code/bad.py  exit 1", out)
        self.assertIn("drifted", out)
        self.assertIn("skip  01-Alpha/code/slow.py  (needs a GPU)", out)
        self.assertIn("examples: 2 passed, 1 failed, 1 skipped", out)

    def test_path_filter_and_clean_run(self):
        code, out = self.main("01-Alpha/code/good.py")
        self.assertEqual(code, 0)
        self.assertIn("examples: 1 passed, 0 failed, 0 skipped", out)

    def test_nothing_to_run_is_an_error(self):
        code, out = self.main("99-Nothing")
        self.assertEqual(code, 1)
        self.assertIn("0 examples found", out)

    def test_timeout_is_a_failure(self):
        self.write("01-Alpha/code/hang.py", "import time\n" + GUARD + "    time.sleep(5)\n")
        code, out = self.main("--timeout", "0.5", "01-Alpha/code/hang.py")
        self.assertEqual(code, 1)
        self.assertIn("timed out", out)


if __name__ == "__main__":
    unittest.main()
