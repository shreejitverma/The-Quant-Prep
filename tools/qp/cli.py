"""``qp``: the Quant Prep command line.

Run with no arguments for live progress. Output is TOON-style (``name[N]{fields}:``
tables) so agents and humans can both read it; errors go to stderr as ``error: ...``
with a non-zero exit code. Interactive commands (``review``, ``drill``) need a TTY;
agents use the non-interactive equivalents (``due``, ``grade``).
"""

from __future__ import annotations

import argparse
import sys
import time
from pathlib import Path

from . import drills, moc, planner
from .check import check_vault
from .state import GRADES, MASTERY_LABELS, StateError, Store
from .vault import REPO_ROOT, TRACK_LABELS, TRACKS, Note, Vault, load_vault

EXIT_OK, EXIT_FAIL, EXIT_USAGE = 0, 1, 2


class CliError(Exception):
    def __init__(self, message: str, code: int = EXIT_USAGE, hint: str | None = None):
        super().__init__(message)
        self.code = code
        self.hint = hint


# --- output helpers ----------------------------------------------------------


def cell(value) -> str:
    s = "" if value is None else str(value)
    return f'"{s}"' if any(ch in s for ch in ',"\n') else s


def table(name: str, fields: list[str], rows: list[list]) -> str:
    if not rows:
        return f"{name}: 0 results"
    out = [f"{name}[{len(rows)}]{{{','.join(fields)}}}:"]
    out += ["  " + ",".join(cell(v) for v in row) for row in rows]
    return "\n".join(out)


def pct(x: float) -> str:
    return f"{round(100 * x)}%"


def emit(*blocks: str, help_lines: list[str] | None = None) -> None:
    text = "\n".join(b for b in blocks if b)
    if help_lines:
        text += f"\nhelp[{len(help_lines)}]:\n" + "\n".join(f"  - {h}" for h in help_lines)
    print(text)


def need_note(vault: Vault, query: str, trackable: bool = False) -> Note:
    note = vault.resolve(query)
    if note is None or (trackable and not note.trackable):
        raise CliError(f"no {'topic' if trackable else 'note'} matches {query!r}", hint="run `qp syllabus` to list topic ids")
    return note


def profile_tracks(store: Store, override: list[str] | None) -> list[str]:
    tracks = override or store.profile.get("tracks") or list(TRACKS)
    bad = [t for t in tracks if t not in TRACKS]
    if bad:
        raise CliError(f"unknown track(s) {bad}; use {', '.join(TRACKS)}")
    return tracks


def parse_mastery(raw: str) -> int:
    if raw.isdigit():
        return int(raw)
    if raw in MASTERY_LABELS:
        return MASTERY_LABELS.index(raw)
    raise CliError(f"mastery must be 0-4 or one of {', '.join(MASTERY_LABELS)}")


# --- commands ----------------------------------------------------------------


def cmd_status(vault: Vault, store: Store, args) -> int:
    tracks = profile_tracks(store, args.track)
    rows = []
    for t in tracks:
        s = planner.track_summary(vault, store, t)
        rows.append([t, pct(s.readiness), f"{s.solid}/{s.topics}", round(s.hours_left)])
    c = planner.counts(vault, store, tracks)
    due = planner.due_cards(vault, store, tracks)
    nxt = planner.next_topics(vault, store, tracks, 5)
    firms = sorted(((f, planner.firm_readiness(vault, store, f)) for f in vault.firms()), key=lambda x: -x[1])
    emit(
        f"qp: Quant Prep progress for {', '.join(tracks)}",
        f"streak: {store.streak()} day(s)",
        f"state: {store.path}",
        table("tracks", ["track", "readiness", "solid", "hours_left"], rows),
        f"cards: {c['cards_due']} due, {len(due)} in today's queue, {c['cards_seen']}/{c['cards']} seen, {c['cards_mature']} mature",
        table("next", ["id", "title", "tier", "hours", "blocked_by"], [[n.id, n.title, n.tier, n.est_hours, " ".join(b)] for n, b in nxt]),
        table("firms_top", ["firm", "readiness"], [[f.title, pct(r)] for f, r in firms[:5]]),
        help_lines=[
            "`qp review` works today's card queue",
            "`qp show <id>` opens a topic, `qp mark <id> <0-4>` records mastery",
            "`qp plan` builds a weekly schedule, `qp serve` opens the web dashboard",
        ],
    )
    return EXIT_OK


def cmd_syllabus(vault: Vault, store: Store, args) -> int:
    tracks = args.track or None
    rows = []
    for section in vault.sections:
        if args.section and args.section.lower() not in section.folder.lower():
            continue
        for n in section.notes:
            if not n.trackable or (tracks and not set(tracks) & set(n.tracks)):
                continue
            if args.tier and n.tier != args.tier:
                continue
            rows.append([n.id, section.folder[:2], n.tier, n.status, n.est_hours, len(n.cards), MASTERY_LABELS[store.mastery(n.id)]])
    emit(
        table("topics", ["id", "sec", "tier", "status", "hours", "cards", "mastery"], rows),
        help_lines=["`qp show <id>` for objectives, prerequisites and path", "filter with --track, --section, --tier"],
    )
    return EXIT_OK


def cmd_show(vault: Vault, store: Store, args) -> int:
    n = need_note(vault, args.topic)
    lines = [
        f"id: {n.id}",
        f"title: {n.title}",
        f"path: {n.path}",
        f"type: {n.type}",
        f"tracks: {', '.join(n.tracks)}",
        f"tier: {n.tier}",
        f"status: {n.status}",
        f"est_hours: {n.est_hours:g}",
    ]
    if n.trackable:
        lines += [
            f"mastery: {store.mastery(n.id)} ({MASTERY_LABELS[store.mastery(n.id)]})",
            f"readiness: {pct(planner.topic_readiness(store, n))}",
        ]
    blocks = ["\n".join(lines)]
    if n.prereqs:
        blocks.append(table("prereqs", ["id", "mastery"], [[p, MASTERY_LABELS[store.mastery(p)]] for p in n.prereqs]))
    unlocks = [m.id for m in vault.notes.values() if n.id in m.prereqs]
    if unlocks:
        blocks.append(f"unlocks: {', '.join(unlocks)}")
    blocks.append(table("cards", ["id", "prompt"], [[c.id, c.prompt[:90]] for c in n.cards]))
    if args.full:
        blocks.append("---\n" + n.body.strip())
    emit(*blocks, help_lines=[f"`qp mark {n.id} <0-4>` records mastery", "`--full` prints the note body"])
    return EXIT_OK


def cmd_mark(vault: Vault, store: Store, args) -> int:
    n = need_note(vault, args.topic, trackable=True)
    level = parse_mastery(args.level)
    store.set_mastery(n.id, level)
    emit(f"marked: {n.id} = {level} ({MASTERY_LABELS[level]})", help_lines=["`qp next` suggests what to study next"])
    return EXIT_OK


def cmd_next(vault: Vault, store: Store, args) -> int:
    tracks = profile_tracks(store, args.track)
    rows = [
        [n.id, n.title, n.tier, n.est_hours, MASTERY_LABELS[store.mastery(n.id)], " ".join(b)]
        for n, b in planner.next_topics(vault, store, tracks, args.limit)
    ]
    emit(
        table("next", ["id", "title", "tier", "hours", "mastery", "blocked_by"], rows),
        help_lines=["`qp show <id>` for objectives", "blocked topics list prerequisites below 'practiced'"],
    )
    return EXIT_OK


def cmd_plan(vault: Vault, store: Store, args) -> int:
    tracks = profile_tracks(store, args.track)
    hours = args.hours or float(store.profile.get("hours_per_week", 10))
    tiers = ("core",) if args.core else ("core", "advanced") if args.no_senior else ("core", "advanced", "senior")
    weeks = planner.weekly_plan(vault, store, tracks, hours, tiers)
    shown = weeks[: args.weeks] if args.weeks else weeks
    rows = [[w["week"], w["starts"], round(w["hours"], 1), n.id] for w in shown for n in w["topics"]]
    total = sum(w["hours"] for w in weeks)
    emit(
        f"plan: {len(weeks)} week(s) at {hours:g} h/week for {', '.join(tracks)} (tiers: {', '.join(tiers)}), {total:.0f} h total",
        table("plan", ["week", "starts", "week_hours", "topic"], rows),
        help_lines=["--core limits to core topics", "--hours sets weekly hours", "`qp profile --hours N` saves it"],
    )
    return EXIT_OK


def cmd_due(vault: Vault, store: Store, args) -> int:
    tracks = profile_tracks(store, args.track)
    cards = planner.due_cards(vault, store, tracks, args.limit)
    rows = [[c.id, c.note_id, "new" if not store.card(c.id).due else store.card(c.id).due, c.prompt[:80]] for c in cards]
    emit(
        table("due", ["card", "topic", "due", "prompt"], rows),
        help_lines=["`qp grade <card> again|hard|good|easy` records a review", "`qp review` runs the queue interactively"],
    )
    return EXIT_OK


def cmd_grade(vault: Vault, store: Store, args) -> int:
    if args.card not in vault.cards:
        raise CliError(f"no card {args.card!r}", hint="run `qp due` for card ids")
    new = store.grade(args.card, args.grade)
    emit(f"graded: {args.card} {args.grade}; next due {new.due} (interval {new.interval}d, ease {new.ease:.2f})")
    return EXIT_OK


def require_tty(alt: str) -> None:
    if not sys.stdin.isatty():
        raise CliError("this command is interactive and needs a terminal", hint=alt)


def ask(prompt: str) -> str:
    try:
        return input(prompt)
    except EOFError:
        return "q"


def cmd_review(vault: Vault, store: Store, args) -> int:
    require_tty("use `qp due` and `qp grade <card> <grade>`")
    queue = planner.due_cards(vault, store, profile_tracks(store, args.track), args.limit)
    if not queue:
        emit("review: 0 cards due", help_lines=["`qp next` suggests topics to study; written topics add cards"])
        return EXIT_OK
    done = 0
    keys = {"1": "again", "2": "hard", "3": "good", "4": "easy"}
    while queue:
        card = queue.pop(0)
        note = vault.notes[card.note_id]
        print(f"\n[{done + 1}, {len(queue)} left] {note.title}\nQ: {card.prompt}")
        if ask("  (enter to reveal, q to quit) ").strip().lower() == "q":
            break
        print("A: " + card.answer.replace("\n", "\n   "))
        choice = ""
        while choice not in keys and choice != "q":
            choice = ask("  grade 1 again, 2 hard, 3 good, 4 easy (q quits): ").strip().lower()
        if choice == "q":
            break
        store.grade(card.id, keys[choice])
        done += 1
        if keys[choice] == "again":
            queue.append(card)
    emit(f"review: {done} card(s) graded", help_lines=["`qp` shows updated readiness"])
    return EXIT_OK


def run_timed_drill(store: Store, mode: str, seconds: int, limit: int | None, seed: int | None) -> dict:
    gen = drills.problems(mode, seed)
    start = time.monotonic()
    attempts = correct = 0
    problem = next(gen)
    retry_same = mode == "arith"  # Zetamac: stay on a problem until it is answered correctly
    while time.monotonic() - start < seconds and (limit is None or attempts < limit):
        left = seconds - (time.monotonic() - start)
        raw = ask(f"[{left:4.0f}s | {correct}] {problem.text} = ")
        if raw.strip().lower() == "q":
            break
        if time.monotonic() - start >= seconds:
            break
        attempts += 1
        if problem.check(raw):
            correct += 1
            problem = next(gen)
        else:
            print(f"  x  (answer {problem.answer_text})" if not retry_same else "  x")
            if not retry_same:
                problem = next(gen)
    elapsed = min(time.monotonic() - start, seconds)
    return store.record_drill(mode, attempts, correct, elapsed, correct)


def run_mm_game(store: Store, seed: int | None) -> dict:
    game = drills.MarketMakingGame(seed=seed)
    print(
        f"Market-making game: quote the sum of {game.n_dice} hidden d{game.sides}. One die is revealed per round.\n"
        f"Width between 1 and {game.max_width}; each trade is {game.lot} lots; about half the counterparties know the answer."
    )
    while not game.finished:
        print(f"\nround {game.revealed + 1}: revealed {game.known or 'nothing'}, position {game.position:+d}")
        raw = ask("  your market 'bid ask' (q quits): ").strip()
        if raw.lower() == "q":
            return {}
        try:
            bid, ask_ = (int(x) for x in raw.replace("@", " ").split())
            event = game.quote(bid, ask_)
        except ValueError as exc:
            print(f"  invalid: {exc}")
            continue
        t = event["trade"]
        result = f"you {t['side']} {t['qty']} @ {t['price']} to a {t['counterparty']} trader" if t else "no trade"
        print(f"  {result}; fair value was {event['fair_value']:g}; die revealed: {event['revealed_die']}")
    s = game.summary()
    print(
        f"\ndice {s['dice']} total {s['total']}: P&L {s['pnl']:+d} (edge at fill {s['edge_at_fill']:+g}, "
        f"adverse selection and inventory {s['adverse_and_inventory']:+g})"
    )
    return store.record_drill("mm", s["trades"], s["trades"] - s["informed_trades"], 0, s["pnl"], {"summary": s})


def cmd_drill(vault: Vault, store: Store, args) -> int:
    require_tty("drills are interactive; `qp serve` offers them in the browser")
    if args.mode == "mm":
        row = run_mm_game(store, args.seed)
    else:
        cfg = drills.DRILL_MODES[args.mode]
        print(f"{cfg['title']}: {args.seconds or cfg['seconds']}s. Answer with integers, decimals or a/b. q quits.")
        row = run_timed_drill(store, args.mode, args.seconds or cfg["seconds"], cfg["questions"], args.seed)
    if not row:
        emit("drill: abandoned, nothing recorded")
        return EXIT_OK
    best = max((d["score"] for d in store.data["drills"] if d["mode"] == args.mode), default=row["score"])
    emit(
        f"drill: {args.mode} score {row['score']:g} ({row['correct']}/{row['attempts']} correct); best {best:g}",
        help_lines=["`qp stats` shows drill history"],
    )
    return EXIT_OK


def cmd_stats(vault: Vault, store: Store, args) -> int:
    rows = [
        [d["at"][:16], d["mode"], d["score"], f"{d['correct']}/{d['attempts']}", d["seconds"]] for d in store.data["drills"][-args.limit :]
    ]
    act = sorted(store.data["activity"].items())[-14:]
    emit(
        table("drills", ["at", "mode", "score", "correct", "seconds"], rows),
        table(
            "activity",
            ["date", "reviews", "marks", "drills"],
            [[d, a.get("reviews", 0), a.get("marks", 0), a.get("drills", 0)] for d, a in act],
        ),
        f"streak: {store.streak()} day(s)",
    )
    return EXIT_OK


def cmd_firms(vault: Vault, store: Store, args) -> int:
    if args.firm:
        firm = need_note(vault, args.firm)
        if firm.type != "firm":
            raise CliError(f"{firm.id} is not a firm")
        focus = planner.firm_focus(vault, store and firm)
        rows = sorted(([n.id, n.tier, pct(planner.topic_readiness(store, n))] for n in focus), key=lambda r: int(r[2][:-1]))
        emit(
            f"firm: {firm.title} ({firm.meta.get('firm_type')}), readiness {pct(planner.firm_readiness(vault, store, firm))}",
            f"guide: {firm.path}",
            table("focus_weakest_first", ["topic", "tier", "readiness"], rows[: args.limit]),
        )
        return EXIT_OK
    rows = sorted(
        ([f.id, f.meta.get("firm_type"), f.status, pct(planner.firm_readiness(vault, store, f))] for f in vault.firms()),
        key=lambda r: -int(r[3][:-1]),
    )
    emit(table("firms", ["id", "type", "guide", "readiness"], rows), help_lines=["`qp firms <id>` lists the weakest focus topics"])
    return EXIT_OK


def cmd_profile(vault: Vault, store: Store, args) -> int:
    if args.tracks or args.hours is not None or args.new_cards is not None:
        store.set_profile(
            tracks=profile_tracks(store, args.tracks) if args.tracks else None, hours_per_week=args.hours, new_cards_per_day=args.new_cards
        )
    p = store.profile
    emit(
        f"tracks: {', '.join(p['tracks'])}",
        f"hours_per_week: {p['hours_per_week']}",
        f"new_cards_per_day: {p['new_cards_per_day']}",
        f"state: {store.path}",
        help_lines=[f"tracks: {', '.join(f'{t} ({TRACK_LABELS[t]})' for t in TRACKS)}"],
    )
    return EXIT_OK


def cmd_check(vault: Vault, store: Store | None, args) -> int:
    files = [Path(f).resolve().relative_to(vault.root) for f in args.files] if args.files else None
    findings = check_vault(vault, strict_sde=args.strict_sde, files=files)
    stale = moc.update_all(vault, apply=False)
    for folder in stale:
        print(f"{folder}/README.md:1: [index] generated table is stale; run `./qp index`")
    for f in findings:
        print(f)
    n = len(findings) + len(stale)
    counts: dict[str, int] = {}
    for note in vault.notes.values():
        if note.trackable:
            counts[note.status] = counts.get(note.status, 0) + 1
    print(
        f"check: {n} problem(s); {len(vault.notes)} notes, {len(vault.cards)} cards; status "
        + ", ".join(f"{k} {v}" for k, v in sorted(counts.items()))
    )
    return EXIT_FAIL if n else EXIT_OK


def cmd_index(vault: Vault, store: Store | None, args) -> int:
    changed = moc.update_all(vault, apply=True)
    emit(f"index: {len(changed)} README(s) updated" + (f": {', '.join(changed)}" if changed else ""))
    return EXIT_OK


def cmd_serve(vault: Vault, store: Store, args) -> int:
    from .server import serve

    serve(store, args.host, args.port, args.open)
    return EXIT_OK


# --- parser --------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="qp", description="Quant Prep: syllabus, progress, spaced review and drills.")
    sub = p.add_subparsers(dest="cmd")

    def add(name, fn, help_):
        sp = sub.add_parser(name, help=help_, description=help_)
        sp.set_defaults(fn=fn)
        return sp

    def tracks_opt(sp):
        sp.add_argument("--track", action="append", choices=TRACKS, help="limit to a track (repeatable)")

    tracks_opt(add("status", cmd_status, "progress overview (default)"))
    sp = add("syllabus", cmd_syllabus, "list topics with status and mastery")
    tracks_opt(sp)
    sp.add_argument("--section")
    sp.add_argument("--tier", choices=("core", "advanced", "senior"))
    sp = add("show", cmd_show, "show one topic")
    sp.add_argument("topic")
    sp.add_argument("--full", action="store_true")
    sp = add("mark", cmd_mark, "record mastery 0-4 for a topic")
    sp.add_argument("topic")
    sp.add_argument("level", help="0 unseen, 1 studied, 2 practiced, 3 solid, 4 interview-ready")
    sp = add("next", cmd_next, "suggest the next topics to study")
    tracks_opt(sp)
    sp.add_argument("--limit", type=int, default=8)
    sp = add("plan", cmd_plan, "weekly study plan in prerequisite order")
    tracks_opt(sp)
    sp.add_argument("--hours", type=float)
    sp.add_argument("--weeks", type=int, help="only show the first N weeks")
    sp.add_argument("--core", action="store_true", help="core topics only")
    sp.add_argument("--no-senior", action="store_true", help="core and advanced topics")
    sp = add("due", cmd_due, "list today's review queue (non-interactive)")
    tracks_opt(sp)
    sp.add_argument("--limit", type=int)
    sp = add("grade", cmd_grade, "record a card review (non-interactive)")
    sp.add_argument("card")
    sp.add_argument("grade", choices=GRADES)
    sp = add("review", cmd_review, "interactive spaced-repetition review")
    tracks_opt(sp)
    sp.add_argument("--limit", type=int)
    sp = add("drill", cmd_drill, "timed drills: arith, optiver, mm (market-making game)")
    sp.add_argument("mode", choices=("arith", "optiver", "mm"))
    sp.add_argument("--seconds", type=int)
    sp.add_argument("--seed", type=int)
    sp = add("stats", cmd_stats, "drill history and activity")
    sp.add_argument("--limit", type=int, default=15)
    sp = add("firms", cmd_firms, "readiness by firm, or focus topics for one firm")
    sp.add_argument("firm", nargs="?")
    sp.add_argument("--limit", type=int, default=15)
    sp = add("profile", cmd_profile, "show or set target tracks and weekly hours")
    sp.add_argument("--tracks", nargs="+", choices=TRACKS)
    sp.add_argument("--hours", type=float)
    sp.add_argument("--new-cards", type=int)
    sp = add("check", cmd_check, "validate notes, cards, links and style (CI gate)")
    sp.add_argument("files", nargs="*")
    sp.add_argument("--strict-sde", action="store_true", help="fail when the SDE-Interview-Prep clone is missing")
    add("index", cmd_index, "regenerate section README tables")
    sp = add("serve", cmd_serve, "run the local web dashboard")
    sp.add_argument("--host", default="127.0.0.1")
    sp.add_argument("--port", type=int, default=8765)
    sp.add_argument("--open", action="store_true", help="open a browser")
    return p


NO_STATE = {cmd_check, cmd_index}


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "fn", None):
        args = parser.parse_args(["status", *(argv or [])])
    try:
        vault = load_vault(REPO_ROOT)
        store = None if args.fn in NO_STATE else Store()
        return args.fn(vault, store, args)
    except CliError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if exc.hint:
            print(f"hint: {exc.hint}", file=sys.stderr)
        return exc.code
    except StateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return EXIT_FAIL
    except KeyboardInterrupt:
        print()
        return 130
