"""Behaviour tests for the CFA Level II pipeline in 17-CFA/scripts/cfa_l2.

They need none of the copyrighted curriculum extracts, so they run in CI: each test builds a tiny
repository in a temporary directory and imports the pipeline fresh against it.
"""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
import unittest
from pathlib import Path
from types import ModuleType
from unittest import mock

SCRIPTS = Path(__file__).resolve().parents[2] / "17-CFA" / "scripts" / "cfa_l2"
PIPELINE = ("cfa_common", "build_mocks", "verify_notes", "verify_practice")


def load_pipeline(root: Path) -> dict[str, ModuleType]:
    """Import the pipeline against ``root``; its paths come from the environment at import time."""
    env = {"CFA_VAULT": str(root), "CFA_BUILD": str(root / "build" / "cfa_l2"), "CFA_PRIVATE": str(root / "17-CFA" / "Private")}
    with mock.patch.dict(os.environ, env), mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
        for name in PIPELINE:
            sys.modules.pop(name, None)
        mods = {name: importlib.import_module(name) for name in PIPELINE}
    for name in PIPELINE:
        sys.modules.pop(name, None)
    return mods


def write_itemset(root: Path, stem: str, source: str, key: str = "C") -> Path:
    path = root / "17-CFA" / "CFA-L-2" / "20-Item-Set-Bank" / "09-Portfolio-Management" / f"{stem}.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        '---\ntype: cfa-itemset\ntopic: Portfolio Management\ntopic_code: "09"\ntopic_slug: 09-Portfolio-Management\n'
        f"lm: 1\ntitle: {stem}\nlos: [los-09-01-a]\ndifficulty: 3\nminutes: 12\nsource: {source}\nattempts: 0\ntags: [cfa/l2]\n---\n"
        "## Vignette\n\nA fund holds two bonds.\n\n"
        "## Questions\n\n1. Which bond returns more? (LOS: los-09-01-a)\n\n"
        f"## Answer key\n\n> [!success]- Answers and reasoning\n> 1. **{key}.** The five-year bond.\n\n"
        "## Distractor design\n\nA ignores maturity.\n"
    )
    return path


class TempRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (self.root / "17-CFA" / "CFA-L-2" / "21-Mocks").mkdir(parents=True)

    def tearDown(self):
        self.tmp.cleanup()


class MockStaleness(TempRepo):
    """Mocks are generated from item sets; verify_practice must fail whenever a committed mock differs."""

    def build(self) -> dict[str, ModuleType]:
        mods = load_pipeline(self.root)
        with mock.patch("builtins.print"):
            mods["build_mocks"].main()
        return mods

    def stale(self, mods: dict[str, ModuleType]) -> list[str]:
        expected = mods["build_mocks"].render_mocks()[0]
        return mods["verify_practice"].stale_mocks(expected, self.root / "17-CFA" / "CFA-L-2" / "21-Mocks")

    def test_freshly_built_mocks_are_current(self):
        write_itemset(self.root, "IS-09-LM01-M03", "mock-03")
        self.assertEqual(self.stale(self.build()), [])

    def test_rekeyed_item_set_makes_its_mock_stale(self):
        source = write_itemset(self.root, "IS-09-LM01-M03", "mock-03", key="C")
        mods = self.build()
        source.write_text(source.read_text().replace("**C.**", "**B.**"))
        self.assertEqual(self.stale(mods), ["Mock-03.md: stale against its item sets; run build_mocks.py"])
        self.assertIn("**B.**", mods["build_mocks"].render_mocks()[0]["Mock-03.md"])

    def test_hand_edited_missing_and_stray_mocks_are_reported(self):
        write_itemset(self.root, "IS-09-LM01-M03", "mock-03")
        mods = self.build()
        mocks = self.root / "17-CFA" / "CFA-L-2" / "21-Mocks"
        (mocks / "Mock-01.md").write_text((mocks / "Mock-01.md").read_text() + "edited by hand\n")
        (mocks / "Mock-02.md").unlink()
        (mocks / "Mock-09.md").write_text("# Mock 9\n")
        self.assertEqual(
            self.stale(mods),
            [
                "Mock-01.md: stale against its item sets; run build_mocks.py",
                "Mock-02.md: missing; run build_mocks.py",
                "Mock-09.md: not produced by build_mocks.py",
            ],
        )


class PrivatePracticeProblems(TempRepo):
    """A note's Practice problems section embeds a private note; the gate measures the private text."""

    POINTER = "\n> [!note] Kept private\n\n![[LM01-Example-Practice-Problems]]\n\n"

    def private_dir(self) -> Path:
        return self.root / "17-CFA" / "Private" / "CFA-L-2" / "Practice-Problems"

    def test_pointer_resolves_to_the_private_body(self):
        self.private_dir().mkdir(parents=True)
        (self.private_dir() / "LM01-Example-Practice-Problems.md").write_text("---\ntype: cfa-practice-private\n---\nQ1 restated.\n")
        vn = load_pipeline(self.root)["verify_notes"]
        secs = {"Practice problems": self.POINTER}
        self.assertIsNone(vn.resolve_private(secs))
        self.assertEqual(secs["Practice problems"], "Q1 restated.\n")
        self.assertIn("section too thin: Practice problems (12 chars, need 800)", vn.thin_sections(secs))

    def test_missing_private_note_fails_when_the_overlay_exists(self):
        self.private_dir().mkdir(parents=True)
        vn = load_pipeline(self.root)["verify_notes"]
        problem = vn.resolve_private({"Practice problems": self.POINTER})
        self.assertIsNotNone(problem)
        self.assertIn("embeds LM01-Example-Practice-Problems, missing from", problem)

    def test_absent_overlay_leaves_the_section_present_but_unchecked(self):
        vn = load_pipeline(self.root)["verify_notes"]
        secs = {name: "x" * 2000 for name in vn.SECTIONS} | {"Practice problems": self.POINTER}
        self.assertIsNone(vn.resolve_private(secs))
        self.assertIsNone(secs["Practice problems"])
        self.assertEqual(vn.thin_sections(secs), [])


class MissingExtracts(TempRepo):
    def test_gates_explain_how_to_point_at_the_extracts(self):
        common = load_pipeline(self.root)["cfa_common"]
        with self.assertRaises(SystemExit) as caught:
            common.load_manifest()
        self.assertIn("set CFA_BUILD", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
