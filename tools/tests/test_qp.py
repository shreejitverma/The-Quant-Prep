"""Behaviour tests for the qp platform. Run: python3 -m unittest discover tools/tests"""

from __future__ import annotations

import datetime as dt
import json
import os
import random
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from fractions import Fraction
from http.server import ThreadingHTTPServer
from pathlib import Path
from unittest import mock

from tools.qp import bank, check, drills, moc, planner, server
from tools.qp.state import CardSchedule, StateError, Store, schedule
from tools.qp.vault import load_vault, note_id_for, parse_cards, parse_scalar, split_frontmatter

FRONT = "---\ntype: {type}\ntrack: [{track}]\ntier: {tier}\nstatus: {status}\nprereqs: [{prereqs}]\nest_hours: {hours}\nsources: []\n---\n"


def card(cid: str, prompt: str = "What?", answer: str = "That.") -> str:
    return f"> [!question]- {cid} | {prompt}\n> {answer}\n"


def write_note(
    root: Path,
    rel: str,
    title: str,
    body: str = "",
    type_: str = "concept",
    track: str = "quant-trader",
    tier: str = "core",
    status: str = "seed",
    prereqs: str = "",
    hours: int = 2,
) -> None:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        FRONT.format(type=type_, track=track, tier=tier, status=status, prereqs=prereqs, hours=hours) + f"\n# {title}\n\n{body}",
        encoding="utf-8",
    )


def fixture_vault(root: Path) -> None:
    (root / "01-Alpha").mkdir()
    (root / "01-Alpha" / "README.md").write_text(
        "---\ntype: moc\ntrack: [quant-trader]\ntier: core\nstatus: solid\n---\n\n# Alpha\n\nIntro.\n"
    )
    write_note(root, "01-Alpha/01-Base.md", "Base", card("a-one") + "\n" + card("a-two"), hours=4)
    write_note(root, "01-Alpha/02-Middle.md", "Middle", card("a-three"), prereqs="base", hours=6)
    write_note(root, "01-Alpha/03-Top.md", "Top", "", prereqs="middle", tier="advanced", hours=3)
    write_note(root, "01-Alpha/04-Side.md", "Side", "", track="quant-dev", hours=2)
    (root / "02-Firms").mkdir()
    (root / "02-Firms" / "Acme.md").write_text(
        "---\ntype: firm\ntrack: [quant-trader]\ntier: core\nstatus: draft\nfocus: [middle, top]\n---\n\n# Acme\n"
    )


class TempRepo(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name) / "repo"
        self.root.mkdir()
        fixture_vault(self.root)
        self.home = Path(self.tmp.name) / "home"
        self.env = mock.patch.dict(os.environ, {"QP_TODAY": "2026-01-10", "SDE_REPO": str(Path(self.tmp.name) / "sde")})
        self.env.start()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def vault(self):
        return load_vault(self.root)

    def store(self):
        return Store(self.home)


class VaultParsing(unittest.TestCase):
    def test_scalars(self):
        self.assertEqual(parse_scalar("[a, b]"), ["a", "b"])
        self.assertEqual(parse_scalar("[]"), [])
        self.assertIsNone(parse_scalar(""))
        self.assertEqual(parse_scalar("4"), 4)
        self.assertEqual(parse_scalar("2.5"), 2.5)
        self.assertEqual(parse_scalar('"x: y"'), "x: y")

    def test_frontmatter_body_and_line(self):
        meta, body, start = split_frontmatter("---\na: 1\n---\n\n# T\n")
        self.assertEqual(meta, {"a": 1})
        self.assertTrue(body.startswith("\n# T"))
        self.assertEqual(start, 4)

    def test_rejects_nested_yaml(self):
        with self.assertRaises(ValueError):
            split_frontmatter("---\na:\n  - b\n---\n")

    def test_cards_multiline_and_separated(self):
        body = card("x-1", "P1", "A1") + "> more\n\n" + card("x-2", "P2", "A2") + "\nnot a card\n"
        cards = parse_cards(body, "n", 10)
        self.assertEqual([c.id for c in cards], ["x-1", "x-2"])
        self.assertEqual(cards[0].answer, "A1\nmore")
        self.assertEqual(cards[0].line, 10)

    def test_note_ids(self):
        self.assertEqual(note_id_for(Path("01-A/03-The-Greeks.md")), "the-greeks")
        self.assertEqual(note_id_for(Path("14-Firms/Jane-Street.md")), "jane-street")
        self.assertEqual(note_id_for(Path("01-A/README.md")), "moc:01-A")


class VaultLoading(TempRepo):
    def test_loads_sections_topics_cards(self):
        v = self.vault()
        self.assertEqual([s.folder for s in v.sections], ["01-Alpha", "02-Firms"])
        self.assertEqual([n.id for n in v.topics()], ["base", "middle", "top", "side"])
        self.assertEqual([n.id for n in v.topics(["quant-dev"])], ["side"])
        self.assertEqual(set(v.cards), {"a-one", "a-two", "a-three"})
        self.assertEqual(v.firms()[0].id, "acme")
        self.assertEqual(v.errors, [])

    def test_duplicate_card_ids_reported(self):
        write_note(self.root, "01-Alpha/05-Dup.md", "Dup", card("a-one"))
        v = self.vault()
        self.assertTrue(any("duplicate card id 'a-one'" in e for e in v.errors))

    def test_library_section_is_listed_not_parsed(self):
        lib = self.root / "03-Library"
        (lib / "deep").mkdir(parents=True)
        (lib / "README.md").write_text("---\ntype: moc\ncurriculum: false\n---\n\n# Library\n")
        (lib / "deep" / "Note.md").write_text("no frontmatter, [[wikilink]] \u2014 anything goes\n")
        v = self.vault()
        section = v.sections[-1]
        self.assertTrue(section.library)
        self.assertEqual([n.id for n in section.notes], ["moc:03-Library"])
        self.assertEqual(check.check_vault(v), [])
        self.assertNotIn("03-Library", moc.update_all(v, apply=False))

    def test_resolve(self):
        v = self.vault()
        self.assertEqual(v.resolve("mid").id, "middle")
        self.assertIsNone(v.resolve("zzz"))


class Scheduling(unittest.TestCase):
    D = dt.date(2026, 1, 1)

    def test_good_progression(self):
        c = schedule(CardSchedule(), "good", self.D)
        self.assertEqual((c.interval, c.reps, c.due), (1, 1, "2026-01-02"))
        c = schedule(c, "good", self.D)
        self.assertEqual(c.interval, 3)
        c = schedule(c, "good", self.D)
        self.assertEqual(c.interval, round(3 * 2.5))

    def test_again_resets_and_lowers_ease(self):
        c = schedule(schedule(CardSchedule(), "good", self.D), "again", self.D)
        self.assertEqual((c.interval, c.reps, c.lapses, c.due), (0, 0, 1, "2026-01-01"))
        self.assertAlmostEqual(c.ease, 2.3)

    def test_ease_floor(self):
        c = CardSchedule()
        for _ in range(20):
            c = schedule(c, "again", self.D)
        self.assertAlmostEqual(c.ease, 1.3)

    def test_easy_new_card(self):
        c = schedule(CardSchedule(), "easy", self.D)
        self.assertEqual(c.interval, 4)
        self.assertAlmostEqual(c.ease, 2.65)

    def test_hard(self):
        c = schedule(schedule(schedule(CardSchedule(), "good", self.D), "good", self.D), "hard", self.D)
        self.assertEqual((c.interval, c.reps), (round(3 * 1.2), 3))
        self.assertAlmostEqual(c.ease, 2.35)

    def test_unknown_grade(self):
        with self.assertRaises(StateError):
            schedule(CardSchedule(), "meh", self.D)


class StoreBehaviour(TempRepo):
    def test_roundtrip_and_atomic_file(self):
        s = self.store()
        s.set_mastery("base", 3)
        s.grade("a-one", "good")
        s2 = self.store()
        self.assertEqual(s2.mastery("base"), 3)
        self.assertEqual(s2.card("a-one").interval, 1)
        self.assertEqual(s2.data["cards"]["a-one"]["first"], "2026-01-10")
        self.assertEqual(sorted(p.name for p in self.home.iterdir()), ["state.json", "state.json.bak", "state.lock"])
        backup = json.loads((self.home / "state.json.bak").read_text())
        self.assertEqual(backup["topics"]["base"]["mastery"], 3)  # the version before the grade
        self.assertNotIn("a-one", backup["cards"])

    def test_two_processes_do_not_lose_updates(self):
        server_side, terminal = self.store(), self.store()  # e.g. `qp serve` and `qp review` at once
        terminal.grade("a-one", "good")
        server_side.set_mastery("base", 2)  # must not overwrite the terminal's grade
        server_side.grade("a-two", "easy")
        terminal.set_mastery("middle", 1)
        final = self.store()
        self.assertEqual(set(final.data["cards"]), {"a-one", "a-two"})
        self.assertEqual((final.mastery("base"), final.mastery("middle")), (2, 1))
        server_side.refresh()
        self.assertEqual(server_side.mastery("middle"), 1)

    def test_profile_validation(self):
        s = self.store()
        for bad in ({"hours_per_week": -5}, {"hours_per_week": 0}, {"new_cards_per_day": -1}):
            with self.assertRaises(StateError):
                s.set_profile(**bad)
        s.set_profile(hours_per_week=12)
        self.assertEqual(self.store().profile["hours_per_week"], 12)

    def test_rejects_bad_mastery(self):
        with self.assertRaises(StateError):
            self.store().set_mastery("base", 7)

    def test_corrupt_and_future_files_fail_loudly(self):
        self.home.mkdir()
        (self.home / "state.json").write_text("{not json")
        with self.assertRaises(StateError):
            self.store()
        (self.home / "state.json").write_text(json.dumps({"version": 99}))
        with self.assertRaises(StateError):
            self.store()

    def test_streak(self):
        s = self.store()
        s.data["activity"] = {"2026-01-08": {"reviews": 1}, "2026-01-09": {"reviews": 1}}
        self.assertEqual(s.streak(), 2)  # today not yet active: streak still alive
        s.data["activity"]["2026-01-10"] = {"reviews": 1}
        self.assertEqual(s.streak(), 3)
        s.data["activity"] = {"2026-01-07": {"reviews": 1}}
        self.assertEqual(s.streak(), 0)


class Planning(TempRepo):
    def test_order_respects_prereqs(self):
        order = [n.id for n in planner.study_order(self.vault(), self.store(), ["quant-trader"])]
        self.assertLess(order.index("base"), order.index("middle"))
        self.assertLess(order.index("middle"), order.index("top"))
        self.assertNotIn("side", order)

    def test_prereq_from_other_track_is_pulled_in(self):
        write_note(self.root, "01-Alpha/05-Needs-Side.md", "Needs side", prereqs="side")
        order = [n.id for n in planner.study_order(self.vault(), self.store(), ["quant-trader"])]
        self.assertLess(order.index("side"), order.index("needs-side"))

    def test_mastered_topics_drop_out_and_hours_bin(self):
        s = self.store()
        s.set_mastery("base", 3)
        weeks = planner.weekly_plan(self.vault(), s, ["quant-trader"], 6)
        ids = [[n.id for n in w["topics"]] for w in weeks]
        self.assertEqual(ids, [["middle"], ["top"]])
        self.assertEqual(weeks[1]["starts"], "2026-01-17")

    def test_readiness_formula(self):
        v, s = self.vault(), self.store()
        base = v.notes["base"]
        self.assertEqual(planner.topic_readiness(s, base), 0.0)
        s.set_mastery("base", 4)
        self.assertAlmostEqual(planner.topic_readiness(s, base), 0.5)  # cards unseen
        s.data["cards"]["a-one"] = {**CardSchedule(interval=21, due="2026-02-01").to_dict()}
        s.data["cards"]["a-two"] = {**CardSchedule(interval=42, due="2026-02-01").to_dict()}
        self.assertAlmostEqual(planner.topic_readiness(s, base), 1.0)
        top = v.notes["top"]
        s.set_mastery("top", 2)
        self.assertAlmostEqual(planner.topic_readiness(s, top), 0.5)  # no cards: mastery only

    def test_due_queue_budget_and_order(self):
        s = self.store()
        s.data["profile"]["new_cards_per_day"] = 2
        v = self.vault()
        self.assertEqual([c.id for c in planner.due_cards(v, s)], ["a-one", "a-two"])
        s.grade("a-one", "again")  # due today, and it consumed one new-card slot
        self.assertEqual([c.id for c in planner.due_cards(v, s)], ["a-one", "a-two"])

    def test_firm_readiness_uses_focus(self):
        v, s = self.vault(), self.store()
        firm = v.notes["acme"]
        self.assertEqual([n.id for n in planner.firm_focus(v, firm)], ["middle", "top"])
        s.set_mastery("top", 4)
        s.set_mastery("middle", 4)
        s.data["cards"]["a-three"] = CardSchedule(interval=30, due="2026-03-01").to_dict()
        self.assertAlmostEqual(planner.firm_readiness(v, s, firm), 1.0)

    def test_next_prefers_unblocked(self):
        nxt = planner.next_topics(self.vault(), self.store(), ["quant-trader"], 3)
        self.assertEqual(nxt[0][0].id, "base")
        blocked = dict((n.id, b) for n, b in nxt)
        self.assertEqual(blocked["middle"], ["base"])


class Drills(unittest.TestCase):
    def test_parse_and_format(self):
        self.assertEqual(drills.parse_number("3/8"), Fraction(3, 8))
        self.assertEqual(drills.parse_number(" 1,250.5 "), Fraction(2501, 2))
        self.assertIsNone(drills.parse_number("abc"))
        self.assertIsNone(drills.parse_number("1/0"))
        self.assertEqual(drills.fmt(Fraction(5, 4)), "1.25")
        self.assertEqual(drills.fmt(Fraction(-1, 8)), "-0.125")
        self.assertEqual(drills.fmt(Fraction(1, 3)), "1/3")

    def independent_eval(self, text: str) -> Fraction:
        if text.endswith(" as a decimal"):
            return Fraction(text.split()[0])
        if "% of " in text:
            p, n = text.split("% of ")
            return Fraction(p) * Fraction(n) / 100
        a, op, b = text.split(" ")
        a, b = Fraction(a), Fraction(b)
        return {"+": a + b, "-": a - b, "x": a * b, "/": a / b}[op]

    def test_generated_answers_are_right(self):
        for mode in ("arith", "optiver"):
            gen = drills.problems(mode, seed=7)
            for _ in range(2000):
                p = next(gen)
                expected = self.independent_eval(p.text)
                self.assertEqual(p.answer, expected, p.text)
                self.assertTrue(p.check(drills.fmt(p.answer)) or p.tolerance > 0, p.text)
                if mode == "arith":
                    self.assertEqual(p.answer.denominator, 1)
                    self.assertGreaterEqual(p.answer, 2)

    def test_tolerance_for_repeating_answers(self):
        p = drills.Problem("1/3 + 1/3", Fraction(2, 3), Fraction(1, 2000))
        self.assertTrue(p.check("0.667"))
        self.assertFalse(p.check("0.66"))

    def test_seeded_problems_are_deterministic(self):
        a, b, c = drills.problems("optiver", 3), drills.problems("optiver", 3), drills.problems("optiver", 4)
        first = [next(a).text for _ in range(50)]
        self.assertEqual(first, [next(b).text for _ in range(50)])
        self.assertNotEqual(first, [next(c).text for _ in range(50)])

    def test_rejects_ambiguous_answers(self):
        for raw in ("1/2/3", "1e3", "1_000", "", "3/", "/4"):
            self.assertIsNone(drills.parse_number(raw), raw)

    def test_mm_game_accounting(self):
        rng = random.Random(1)
        for seed in range(200):
            g = drills.MarketMakingGame(seed=seed)
            while not g.finished:
                fv = int(g.fair_value)
                width = rng.randint(1, g.max_width)
                g.quote(fv - width // 2, fv - width // 2 + width)
            s = g.summary()
            self.assertEqual(s["total"], sum(g.dice))
            self.assertAlmostEqual(s["edge_at_fill"] + s["adverse_and_inventory"], s["pnl"])
            self.assertEqual(g.position, sum(t.qty if t.side == "buy" else -t.qty for t in g.trades))
            for t in g.trades:
                if t.counterparty == "informed":  # informed flow only trades when the quote is wrong
                    self.assertTrue((t.side == "sell" and s["total"] > t.price) or (t.side == "buy" and s["total"] < t.price))

    def test_mm_game_validation(self):
        g = drills.MarketMakingGame(seed=1)
        with self.assertRaises(ValueError):
            g.quote(10, 10)
        with self.assertRaises(ValueError):
            g.quote(10, 20)
        for _ in range(g.n_dice):
            g.quote(13, 15)
        with self.assertRaises(ValueError):
            g.quote(13, 15)

    def test_fair_value(self):
        g = drills.MarketMakingGame(seed=1, dice=[6, 1, 1, 1])
        self.assertEqual(g.fair_value, 14)
        g.quote(13, 15)
        self.assertEqual(g.fair_value, Fraction(6) + 3 * Fraction(7, 2))


class Checks(TempRepo):
    def rules(self, **kw):
        return {(f.rule, Path(f.path).name) for f in check.check_vault(self.vault(), **kw)}

    def test_clean_fixture(self):
        self.assertEqual(check.check_vault(self.vault()), [])

    def test_catches_problems(self):
        write_note(
            self.root,
            "01-Alpha/05-Bad.md",
            "Bad",
            "Broken [x](nope.md) and a dash — here.\n\n```\n[ok](inside-code.md)\n```\n",
            status="solid",
            prereqs="ghost",
            track="quant-trader, astronaut",
        )
        rules = self.rules()
        for rule in ("link", "style", "prereq", "schema", "solid"):
            self.assertIn((rule, "05-Bad.md"), rules)
        messages = [f.message for f in check.check_vault(self.vault())]
        self.assertFalse(any("inside-code" in m for m in messages))

    def test_prereq_cycle(self):
        write_note(self.root, "01-Alpha/01-Base.md", "Base", prereqs="top")
        cycles = [f for f in check.check_vault(self.vault()) if "cycle" in f.message]
        self.assertEqual(len(cycles), 1)
        self.assertIn("base", cycles[0].message)

    def test_sde_links(self):
        url = check.SDE_URL + "04-System-Design/README.md"
        write_note(self.root, "01-Alpha/05-Sde.md", "Sde", f"[sd]({url}) [bad]({check.SDE_URL}nope%20here.md)")
        self.assertEqual({r for r in self.rules() if r[0] == "sde-link"}, set())  # no clone: skipped
        self.assertIn("sde-link", {r for r, _ in self.rules(strict_sde=True)})
        sde = Path(os.environ["SDE_REPO"])
        (sde / "04-System-Design").mkdir(parents=True)
        (sde / "README.md").write_text("x")
        (sde / "04-System-Design" / "README.md").write_text("x")
        findings = [f for f in check.check_vault(self.vault()) if f.rule == "sde-link"]
        self.assertEqual(len(findings), 1)
        self.assertIn("nope here.md", findings[0].message)


class Index(TempRepo):
    def test_moc_is_idempotent_and_preserves_prose(self):
        v = self.vault()
        self.assertEqual(moc.update_all(v), ["01-Alpha"])
        text = (self.root / "01-Alpha" / "README.md").read_text()
        self.assertIn("Intro.", text)
        self.assertIn("[Middle](02-Middle.md)", text)
        self.assertEqual(moc.update_all(self.vault()), [])


class Api(TempRepo):
    def setUp(self):
        super().setUp()
        app = server.App(self.store(), vault_loader=lambda: load_vault(self.root))
        self.httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.make_handler(app, set()))
        port = self.httpd.server_address[1]
        self.httpd.RequestHandlerClass = server.make_handler(app, {f"http://127.0.0.1:{port}"})
        self.base = f"http://127.0.0.1:{port}"
        threading.Thread(target=self.httpd.serve_forever, daemon=True).start()

    def tearDown(self):
        self.httpd.shutdown()
        self.httpd.server_close()
        super().tearDown()

    def call(self, path, body=None, headers=None):
        data = None if body is None else json.dumps(body).encode()
        req = urllib.request.Request(self.base + path, data=data, headers={"Content-Type": "application/json", **(headers or {})})
        try:
            with urllib.request.urlopen(req) as r:
                return r.status, json.loads(r.read())
        except urllib.error.HTTPError as e:
            with e:
                return e.code, json.loads(e.read())

    def test_summary_and_mark(self):
        code, s = self.call("/api/summary")
        self.assertEqual(code, 200)
        self.assertEqual(s["queue"], 3)
        code, row = self.call("/api/mark", {"id": "base", "level": 2})
        self.assertEqual((code, row["mastery"]), (200, 2))
        self.assertEqual(self.store().mastery("base"), 2)

    def test_cross_origin_post_refused(self):
        code, body = self.call("/api/mark", {"id": "base", "level": 2}, {"Origin": "http://evil.example"})
        self.assertEqual(code, 403)
        self.assertEqual(self.store().mastery("base"), 0)

    def test_grade_and_validation(self):
        self.assertEqual(self.call("/api/grade", {"card": "a-one", "grade": "good"})[0], 200)
        self.assertEqual(self.call("/api/grade", {"card": "a-one", "grade": "meh"})[0], 400)
        self.assertEqual(self.call("/api/grade", {"card": "nope", "grade": "good"})[0], 404)
        self.assertEqual(self.call("/api/drill", {"mode": "arith", "attempts": 3, "correct": 5})[0], 400)

    def test_rejects_wrong_content_type_and_host(self):
        req = urllib.request.Request(
            self.base + "/api/mark", data=b'{"id": "base", "level": 2}', headers={"Content-Type": "text/plain; x=application/json"}
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req)
        with ctx.exception:
            self.assertEqual(ctx.exception.code, 415)
        self.assertEqual(self.call("/api/summary", headers={"Host": "attacker.example:80"})[0], 403)
        self.assertEqual(self.call("/api/mark", {"id": "base", "level": 2}, {"Sec-Fetch-Site": "cross-site"})[0], 403)
        self.assertEqual(self.store().mastery("base"), 0)

    def test_security_headers(self):
        with urllib.request.urlopen(self.base + "/api/summary") as r:
            self.assertIn("script-src 'self' https://cdn.jsdelivr.net", r.headers["Content-Security-Policy"])
            self.assertEqual(r.headers["X-Content-Type-Options"], "nosniff")

    def test_sees_updates_from_another_process(self):
        self.store().set_mastery("top", 4)  # a terminal session writes while the server runs
        code, note = self.call("/api/note/top")
        self.assertEqual(note["mastery"], 4)

    def test_path_traversal_blocked(self):
        (Path(self.tmp.name) / "secret.txt").write_text("s")
        self.assertEqual(self.call("/files/../secret.txt")[0], 404)
        with urllib.request.urlopen(self.base + "/files/01-Alpha/01-Base.md") as r:
            self.assertEqual(r.headers["Content-Type"], "text/plain; charset=utf-8")
            self.assertIn(b"# Base", r.read())

    def test_mm_game_over_http(self):
        code, g = self.call("/api/mm/new", {})
        self.assertEqual(code, 200)
        for _ in range(4):
            code, res = self.call("/api/mm/quote", {"game": g["game"], "bid": 13, "ask": 15})
            self.assertEqual(code, 200)
        self.assertTrue(res["state"]["finished"])
        self.assertEqual(self.store().data["drills"][-1]["mode"], "mm")
        self.assertEqual(self.call("/api/mm/quote", {"game": g["game"], "bid": 13, "ask": 15})[0], 404)


if __name__ == "__main__":
    unittest.main()


class QuestionBank(TempRepo):
    SOURCE = (
        "Jane Street\tprobability\tFlip two coins. P(two heads)?\n"
        "Optiver\tprobability\tFlip two coins.  P(two heads)?\n"  # same after normalisation
        "\tbayes\tA question\n"
        "continued on the next line\n"
        "Citadel\tcoding\t\n"
        "Reverse a list.\n"
        "IMC Trading\tlogic\tUnanswered puzzle\n"
    )

    def setUp(self):
        super().setUp()
        self.bankdir = self.root / "private" / "demo"
        (self.bankdir / "answers").mkdir(parents=True)
        (self.bankdir / "source.tsv").write_text(self.SOURCE)

    def test_parse_and_dedupe(self):
        rows = bank.parse_source(self.SOURCE)
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[2], ("", "bayes", "A question continued on the next line"))
        self.assertEqual(rows[3], ("Citadel", "coding", "Reverse a list."))
        qs = bank.dedupe(rows, "wsq")
        self.assertEqual(len(qs), 4)
        coin = next(q for q in qs.values() if q.prompt.startswith("Flip"))
        self.assertEqual((coin.firms, coin.reports), (["Jane Street", "Optiver"], 2))
        self.assertEqual(bank.question_id("wsq", "Flip two coins. P(two heads)?"), coin.id)  # stable id

    def answer(self, **entries):
        (self.bankdir / "answers" / "a.json").write_text(json.dumps(entries))

    def test_overlay_cards_join_topics_and_readiness(self):
        qs = bank.dedupe(bank.parse_source(self.SOURCE), "wsq")
        ids = {q.prompt[:4]: q.id for q in qs.values()}
        self.answer(
            **{
                ids["Flip"]: {"topic": "base", "answer": "1/4", "verified": True},
                ids["A qu"]: {"topic": "middle", "answer": "x"},
                ids["Reve"]: {"topic": "middle", "duplicate_of": ids["A qu"]},
            }
        )
        topics = {n.id: n.title for n in self.vault().topics()}
        built = bank.build(self.bankdir, "wsq")
        bank.render(self.bankdir, built, "Demo", topics)
        self.assertEqual(bank.summary(built)["semantic_duplicates"], 1)
        self.assertEqual(built[ids["A qu"]].firms, ["Citadel"])  # folded from the duplicate
        v = self.vault()
        self.assertEqual(v.sections[-1].folder, "private")
        base = v.notes["base"]
        self.assertIn(ids["Flip"], [c.id for c in base.cards])  # merged into the public topic
        self.assertFalse(v.notes["base-demo"].trackable if "base-demo" in v.notes else False)
        overlay = next(n for n in v.notes.values() if n.extends == "base")
        self.assertFalse(overlay.trackable)
        self.assertNotIn(ids["Unan"], v.cards)  # unanswered questions are listed, not carded
        self.assertIn(ids["Unan"], (self.bankdir / "notes" / "unsorted.md").read_text())
        self.assertIn(ids["Flip"], [c.id for c in planner.due_cards(v, self.store())])
        self.assertEqual(check.check_vault(v), [])

    def test_unknown_topic_rejected(self):
        qs = bank.dedupe(bank.parse_source(self.SOURCE), "wsq")
        self.answer(**{next(iter(qs)): {"topic": "no-such-topic", "answer": "x"}})
        with self.assertRaises(ValueError):
            bank.render(self.bankdir, bank.build(self.bankdir, "wsq"), "Demo", {n.id: n.title for n in self.vault().topics()})

    def test_extends_unknown_topic_is_an_error(self):
        (self.root / "private" / "x.md").write_text(
            "---\ntype: problem-set\ntrack: [quant-trader]\ntier: core\nstatus: draft\nextends: ghost\nest_hours: 1\n---\n\n# X\n"
        )
        self.assertTrue(any("extends unknown topic" in e for e in self.vault().errors))

    def test_tracked_private_file_fails_check(self):
        import subprocess

        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        (self.root / "private" / "leak.md").write_text("secret\n")
        subprocess.run(["git", "add", "-f", "private/leak.md"], cwd=self.root, check=True)
        self.assertIn("private", {f.rule for f in check.check_vault(self.vault())})
