"""Markets Mastery gates bucket each card by the note it lives in, not by its id.

Each fixture is a real temporary vault read by ``load_vault``; the gates are evaluated through the
public ``evaluate_gate`` and ``evaluate_all_markets_gates`` functions.
"""

from __future__ import annotations

import os
import re
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.qp.markets import TRACK_METADATA, evaluate_all_markets_gates, evaluate_gate
from tools.qp.vault import REPO_ROOT, Vault, load_vault

MARKETS = "16-Trading-and-Investing"
FRONT = "---\ntype: concept\ntrack: [quant-trader]\ntier: core\nstatus: seed\nprereqs: []\nest_hours: 2\nsources: []\n---\n"


def card(cid: str) -> str:
    return f"> [!question]- {cid} | What?\n> That.\n"


def write_track(root: Path, folder: str, notes: list[list[str]]) -> None:
    """One note per entry of ``notes``, holding those card ids in order.

    Notes are named ``01-<folder>-Note-1.md``, ``02-<folder>-Note-2.md``, ... so ids stay unique across tracks.
    """
    base = root / MARKETS / folder
    base.mkdir(parents=True, exist_ok=True)
    slug = folder.replace("/", "-")
    for i, ids in enumerate(notes, 1):
        body = "\n".join(card(cid) for cid in ids)
        (base / f"{i:02d}-{slug}-Note-{i}.md").write_text(f"{FRONT}\n# Note {i}\n\n{body}", encoding="utf-8")


def bulk_notes(prefix: str, n_notes: int, per_note: int) -> list[list[str]]:
    """The original bulk build: note k holds ids ``(k - 1) * per_note + 1`` to ``k * per_note``."""
    return [[f"{prefix}{(k * per_note) + j:03d}" for j in range(1, per_note + 1)] for k in range(n_notes)]


def reviewed(ids) -> dict:
    return {"cards": {cid: {"reps": 1, "interval": 1} for cid in ids}}


def evaluate(track_id: str, stage: str, vault: Vault, state: dict):
    return evaluate_gate(track_id, stage, vault, state)


def card_requirement(gate):
    """The first requirement of every card-backed gate is its stage card count."""
    return gate.requirements[0]


class TempMarketsVault(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        # Keep any developer's private overlay out of the fixture vault.
        self.env = mock.patch.dict(os.environ, {"QP_PRIVATE": str(Path(self.tmp.name) / "no-private")})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def vault(self) -> Vault:
        vault = load_vault(self.root)
        self.assertEqual(vault.errors, [])
        return vault


class TestAppendedCardsJoinTheirNotesStage(TempMarketsVault):
    """An audit appends ``mkt-fa-257`` to note 01, a foundations note, after the 256-card bulk build."""

    def setUp(self):
        super().setUp()
        notes = bulk_notes("mkt-fa-", 8, 32)
        notes[0].append("mkt-fa-257")
        write_track(self.root, "Investing/Fundamental-Analysis", notes)
        self.original = [cid for ids in bulk_notes("mkt-fa-", 8, 32) for cid in ids]

    def test_appended_card_counts_in_foundations_total_and_passed(self):
        vault = self.vault()
        gate = evaluate("track_fa", "foundations", vault, reviewed([*self.original, "mkt-fa-257"]))
        req = card_requirement(gate)
        self.assertEqual(req.target, "129 cards")
        self.assertEqual(req.actual, "129 cards reviewed")
        self.assertTrue(gate.passed)
        core = card_requirement(evaluate("track_fa", "core", vault, reviewed(self.original)))
        self.assertEqual((core.target, core.actual), ("128 cards", "128 cards reviewed"))

    def test_learner_who_skipped_the_appended_card_does_not_pass(self):
        vault = self.vault()
        gate = evaluate("track_fa", "foundations", vault, reviewed(self.original))
        req = card_requirement(gate)
        self.assertEqual((req.target, req.actual), ("129 cards", "128 cards reviewed"))
        self.assertFalse(req.passed)
        self.assertFalse(gate.passed)
        # The core stage holds no appended card, so the same learner passes it.
        self.assertTrue(evaluate("track_fa", "core", vault, reviewed(self.original)).passed)


class TestNonNumericCardIds(TempMarketsVault):
    def test_non_numeric_id_is_bucketed_by_its_note_without_crashing(self):
        notes = bulk_notes("mkt-fa-", 8, 32)
        notes[3].append("mkt-fa-roic-check")  # note 04 is the last foundations note
        notes[5].append("mkt-fa-beneish-check")  # note 06 is a core note
        write_track(self.root, "Investing/Fundamental-Analysis", notes)
        vault = self.vault()
        everything = [cid for ids in notes for cid in ids]

        all_gates = evaluate_all_markets_gates(vault, reviewed(everything))
        found = card_requirement(all_gates["track_fa"]["foundations"])
        core = card_requirement(all_gates["track_fa"]["core"])
        self.assertEqual((found.target, found.actual), ("129 cards", "129 cards reviewed"))
        self.assertEqual((core.target, core.actual), ("129 cards", "129 cards reviewed"))

        skipped = reviewed(cid for cid in everything if cid != "mkt-fa-roic-check")
        self.assertFalse(evaluate("track_fa", "foundations", vault, skipped).passed)
        self.assertTrue(evaluate("track_fa", "core", vault, skipped).passed)

    def test_non_numeric_id_in_a_single_note_track_lands_in_core(self):
        # A one-note track splits that note's cards in half by position, so an appended card is core.
        ids = [f"mkt-car-{i:03d}" for i in range(1, 33)] + ["mkt-car-extra"]
        write_track(self.root, "07-Trading-Styles/Quant-Prop-Trading", [ids])
        vault = self.vault()
        found = card_requirement(evaluate("track_car", "foundations", vault, reviewed(ids)))
        core = card_requirement(evaluate("track_car", "core", vault, reviewed(ids)))
        self.assertEqual((found.target, found.actual), ("16 cards", "16 cards reviewed"))
        self.assertEqual((core.target, core.actual), ("17 cards", "17 cards reviewed"))
        self.assertFalse(evaluate("track_car", "core", vault, reviewed(ids[:-1])).passed)


class TestSpecialisedAndSmallTracks(TempMarketsVault):
    def test_multi_note_specialised_track_splits_at_a_note_boundary(self):
        notes = bulk_notes("mkt-his-", 10, 4)
        notes[1].append("mkt-his-041")  # note 02 sits in the first half of the ten notes
        write_track(self.root, "20-History-and-Events", notes)
        vault = self.vault()
        original = [cid for ids in bulk_notes("mkt-his-", 10, 4) for cid in ids]
        found = card_requirement(evaluate("track_his", "foundations", vault, reviewed(original)))
        core = card_requirement(evaluate("track_his", "core", vault, reviewed(original)))
        self.assertEqual((found.target, found.actual, found.passed), ("21 cards", "20 cards reviewed", False))
        self.assertEqual((core.target, core.actual, core.passed), ("20 cards", "20 cards reviewed", True))

    def test_sixty_four_card_stage_counts_a_card_appended_to_its_note(self):
        notes = bulk_notes("mkt-opt-", 4, 32)
        notes[1].append("mkt-opt-129")  # note 02 is the last foundations note of four
        write_track(self.root, "03-Options-and-Volatility", notes)
        vault = self.vault()
        original = [cid for ids in bulk_notes("mkt-opt-", 4, 32) for cid in ids]
        found = card_requirement(evaluate("track_opt", "foundations", vault, reviewed(original)))
        core = card_requirement(evaluate("track_opt", "core", vault, reviewed(original)))
        self.assertEqual((found.target, found.actual, found.passed), ("65 cards", "64 cards reviewed", False))
        self.assertEqual((core.target, core.actual, core.passed), ("64 cards", "64 cards reviewed", True))


# Per-stage card totals of every track on the repo vault, recorded from the id-range gates before the
# switch to note-based stages. Bucketing by note must reproduce them exactly for the bulk-built cards.
BULK_STAGE_TOTALS = {
    "track_0_pqt": (64, 64),
    "track_6_trd": (64, 64),
    "track_fa": (128, 128),
    "track_val": (128, 128),
    "track_vi": (128, 128),
    "track_pf": (128, 128),
    "track_opt": (64, 64),
    "track_ta": (128, 128),
    "track_sys": (128, 128),
    "track_ind": (16, 16),
    "track_mac": (16, 16),
    "track_cmd": (16, 16),
    "track_cry": (16, 16),
    "track_his": (20, 20),
    "track_psy": (16, 16),
    "track_dec": (16, 16),
    "track_exe": (16, 16),
    "track_reg": (16, 16),
    "track_car": (16, 16),
}


class TestRepoVaultStageParity(unittest.TestCase):
    """Every gate on the repo vault keeps the stage totals the id ranges gave the original bulk build.

    A bulk-built card is ``<prefix>NNN`` with ``NNN`` at most the track's bulk total; under the id ranges
    the first ``foundations`` of them were foundations and the rest core. Cards appended later by audits
    are outside that set: they raise a stage's target, so the target check only demands equality for a
    track whose cards are all bulk-built, which was every track when these totals were recorded.
    """

    @classmethod
    def setUpClass(cls):
        with mock.patch.dict(os.environ, {"QP_PRIVATE": str(REPO_ROOT / "tools" / "tests" / "no-such-private-overlay")}):
            cls.vault = load_vault(REPO_ROOT)

    def bulk_ids(self, track_id: str) -> tuple[list[str], list[str]]:
        prefix = TRACK_METADATA[track_id]["card_prefix"]
        n_found, n_core = BULK_STAGE_TOTALS[track_id]
        pattern = re.compile(re.escape(prefix) + r"(\d{3})")
        numbered = {int(m.group(1)): cid for cid in self.vault.cards if (m := pattern.fullmatch(cid))}
        self.assertEqual(set(range(1, n_found + n_core + 1)) - set(numbered), set(), f"{track_id} lost bulk cards")
        return [numbered[i] for i in range(1, n_found + 1)], [numbered[i] for i in range(n_found + 1, n_found + n_core + 1)]

    def test_every_track_is_recorded(self):
        self.assertEqual(set(BULK_STAGE_TOTALS), set(TRACK_METADATA))

    def test_reviewing_the_bulk_cards_gives_the_recorded_stage_totals(self):
        all_bulk = [cid for tid in TRACK_METADATA for ids in self.bulk_ids(tid) for cid in ids]
        all_gates = evaluate_all_markets_gates(self.vault, reviewed(all_bulk))
        for tid, (n_found, n_core) in BULK_STAGE_TOTALS.items():
            prefix = TRACK_METADATA[tid]["card_prefix"]
            only_bulk = sum(1 for cid in self.vault.cards if cid.startswith(prefix)) == n_found + n_core
            for stage, expected in (("foundations", n_found), ("core", n_core)):
                with self.subTest(track=tid, stage=stage):
                    req = card_requirement(all_gates[tid][stage])
                    self.assertEqual(req.actual, f"{expected} cards reviewed")
                    target = int(req.target.split()[0])
                    if only_bulk:
                        self.assertEqual(target, expected)
                    else:
                        self.assertGreaterEqual(target, expected)

    def test_each_bulk_card_keeps_its_id_range_stage(self):
        # Review one stage's bulk cards at a time: the other stage must see none of them.
        for tid in TRACK_METADATA:
            found_ids, core_ids = self.bulk_ids(tid)
            for stage, ids, other in (("foundations", found_ids, "core"), ("core", core_ids, "foundations")):
                with self.subTest(track=tid, stage=stage):
                    state = reviewed(ids)
                    self.assertEqual(card_requirement(evaluate(tid, stage, self.vault, state)).actual, f"{len(ids)} cards reviewed")
                    self.assertEqual(card_requirement(evaluate(tid, other, self.vault, state)).actual, "0 cards reviewed")


if __name__ == "__main__":
    unittest.main()
