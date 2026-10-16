"""Regenerate 00-Strategy/Study-Plan.md from the manifest and the hour assumptions in its frontmatter.

Pass 1 time per module is proportional to curriculum length with a 3-hour floor, in dependency-then-weight order.
Tasks carry [due:: YYYY-MM-DD] and #cfa/plan so the Tasks plugin can query them.
"""

from __future__ import annotations

import datetime as dt
import sys

from cfa_common import L2, lm_note_name, load_manifest, read_frontmatter

PLAN = L2 / "00-Strategy" / "Study-Plan.md"
ORDER = ["01", "03", "05", "06", "07", "04", "02", "08", "09", "10"]


FLOOR_HOURS = 3.0


def task(text: str, due: dt.date) -> str:
    return f"- [ ] {text} #cfa/plan [due:: {due.isoformat()}]"


def allocate(chars: list[int], total_hours: float, floor: float = FLOOR_HOURS) -> list[float]:
    """Split total_hours in proportion to chars with a per-module floor.

    Modules that would fall under the floor are pinned to it and the remaining hours are redistributed
    proportionally among the rest, repeating until no further module drops under the floor.
    The result sums to total_hours unless the floor alone exceeds it, in which case every module gets the floor.
    """
    pinned: set[int] = set()
    while True:
        free_chars = sum(c for i, c in enumerate(chars) if i not in pinned)
        free_hours = total_hours - floor * len(pinned)
        if free_chars == 0 or free_hours <= 0:
            return [floor] * len(chars)
        alloc = [floor if i in pinned else c / free_chars * free_hours for i, c in enumerate(chars)]
        below = {i for i, a in enumerate(alloc) if i not in pinned and a < floor}
        if not below:
            return alloc
        pinned |= below


def main() -> int:
    fm = read_frontmatter(PLAN)[0] if PLAN.exists() else {}
    wd, we = float(fm.get("weekday_hours", 3.5)), float(fm.get("weekend_hours", 7))
    start, exam = dt.date(2026, 8, 26), dt.date(2026, 11, 24)
    man = load_manifest()
    topics = {t["code"]: t for t in man["topics"]}
    mods = [(c, m, lm_note_name(c, m["lm"], m["title"])) for c in ORDER for m in topics[c]["modules"]]
    p1_days = 49
    days = [start + dt.timedelta(i) for i in range(p1_days)]
    cap = [we if d.weekday() >= 5 else wd for d in days]
    total_hours = sum(cap)
    alloc = allocate([m["chars"] for _, m, _ in mods], total_hours)
    schedule, di, used = [], 0, 0.0
    for (c, m, n), h in zip(mods, alloc, strict=True):
        remaining = h
        while remaining > 1e-6 and di < p1_days:
            take = min(cap[di] - used, remaining)
            remaining -= take
            used += take
            if used >= cap[di] - 1e-6:
                di, used = di + 1, 0.0
        schedule.append((c, m, n, days[min(di, p1_days - 1)], h))
    out = [
        "---",
        "type: cfa-study-plan",
        "tags: [cfa/l2, cfa/plan]",
        "exam_date: 2026-11-24",
        "plan_start: 2026-08-26",
        f"weekday_hours: {wd}",
        f"weekend_hours: {we}",
        "target_mock6: 85",
        "---",
        "# Study Plan: 90 days to 24 November 2026",
        "",
        "Three overlapping passes.",
        (
            f"Hours assumed: {wd} on weekdays, {we} on weekend days, about "
            f"{round(sum(we if (start + dt.timedelta(i)).weekday() >= 5 else wd for i in range(90)))} "
            "in total; edit the properties above and regenerate with `python3 17-CFA/scripts/cfa_l2/build_plan.py` "
            "if your availability changes."
        ),
        (
            "Module time in Pass 1 is proportional to curriculum length with a 3-hour floor, in dependency-then-weight "
            "order: Quant, FSA, Equity, Fixed Income, Derivatives, Corporate Issuers, Economics, Alternatives, "
            "Portfolio Management, Ethics."
        ),
        "Daily, from day 1: 20 to 30 minutes of SRS review (`#flashcards/cfa-l2`).",
        "From week 3: one interleaved item set per day from already-studied modules.",
        "",
        "## Weekly milestones",
        "",
        "| Week | Dates | Milestone |",
        "|---|---|---|",
    ]
    ms = [
        "Quant LM1-5 done; Ethics Standards read once (V10 LM1-2, no notes)",
        "Quant done; FSA LM1-2",
        "FSA LM3-6",
        "Equity LM1-4",
        "Equity done; Fixed Income LM1-3",
        "Fixed Income done; Derivatives; Corporate Issuers LM1-2",
        "Corporate done; Economics; Alternatives; PM LM1-3; Ethics LM1-3; Pass 1 complete 13 Oct",
        "Pass 2: 6-8 item sets per day, mixed topics; Mock 1 on 18 Oct",
        "Pass 2 continues; every miss logged; mastery all LMs 50+",
        "Pass 2 ends; Mock 2 on 1 Nov; mastery all LMs 60+",
        "Pass 3: Mock 3 (5 Nov), Mock 4 (9 Nov); error log to zero unresolved",
        "Mock 5 (13 Nov), Mock 6 (17 Nov) target 85+; all LMs 70+, top-weight LMs 85+",
        "Formula and calculator drill; Ethics reread; rest. Exam 24 Nov",
    ]
    for i in range(13):
        a, b = start + dt.timedelta(7 * i), start + dt.timedelta(7 * i + 6)
        out.append(f"| {i + 1} | {a.strftime('%d %b')} to {min(b, exam).strftime('%d %b')} | {ms[i]} |")
    out += [
        "",
        "## Pass 1: learn every module (26 Aug to 13 Oct)",
        "",
        (
            "Per module: read the LM note, rework every example, do the practice problems, do one item "
            "set, write the teach-back, start its SRS deck."
        ),
        "",
    ]
    out.append(
        task(
            "Read the Code and Standards once end to end (V10 LM1 and the Standard headings of LM2), no notes yet", start + dt.timedelta(5)
        )
    )
    for c, m, n, due, h in schedule:
        out.append(task(f"Study [[{n}|{topics[c]['name']} LM{m['lm']}: {m['title']}]] ({h:.1f} h)", due))
        out.append(task(f"Teach-back and 1 item set for [[{n}|LM{m['lm']} {m['title'][:40]}]]", due))
    out += [
        "",
        "## Pass 2: item sets only (14 Oct to 3 Nov)",
        "",
        "Timed at 18 minutes per set, mixed topics, confidence recorded before checking, every miss logged with QuickAdd.",
        "",
    ]
    d = dt.date(2026, 10, 14)
    while d <= dt.date(2026, 11, 3):
        out.append(task(f"{8 if d.weekday() >= 5 else 6} timed item sets, mixed topics, log attempts and errors", d))
        if d.weekday() == 6:
            out.append(task("Weekly review (QuickAdd: CFA weekly review); run mastery.py", d))
        d += dt.timedelta(1)
    out.append(task("[[Mock-01]] under full exam timing (two sessions of 2h12m), log the attempt", dt.date(2026, 10, 18)))
    out.append(task("[[Mock-02]] under full exam timing, log the attempt", dt.date(2026, 11, 1)))
    out += [
        "",
        "## Pass 3: mocks and repair (4 Nov to 23 Nov)",
        "",
        "Mocks on alternating days at full timing; off days on the error log, formula sheet, Slides drill and Ethics rereads.",
        "",
    ]
    mocks = {dt.date(2026, 11, 5): 3, dt.date(2026, 11, 9): 4, dt.date(2026, 11, 13): 5, dt.date(2026, 11, 17): 6}
    d = dt.date(2026, 11, 4)
    while d <= dt.date(2026, 11, 23):
        if d in mocks:
            out.append(task(f"[[Mock-{mocks[d]:02d}]] under full exam timing, log the attempt, log every miss", d))
        elif d >= dt.date(2026, 11, 21):
            out.append(task("Formula drill (Slides decks), calculator drill, Ethics reread; no new material; sleep", d))
        else:
            out.append(task("Repair day: clear unresolved errors, reread weakest 3 LMs by mastery, formula sheet pass, SRS", d))
        if d.weekday() == 6:
            out.append(task("Weekly review; run mastery.py", d))
        d += dt.timedelta(1)
    out += ["", "## Exam day", "", "- [ ] Exam: 24 November 2026. See [[Exam-Day-Playbook]] #cfa/plan [due:: 2026-11-24]", ""]
    PLAN.write_text("\n".join(out) + "\n")
    print(f"study plan written: {len(out)} lines, pass 1 hours {round(total_hours)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
