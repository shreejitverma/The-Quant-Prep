"""Assemble the six mocks inside the official weight bands.

22 item sets per mock: 20 scored plus 2 unscored in the real exam, all treated as scored here.
Per-topic counts (sum 22, all inside the bands): Quant 2, Econ 1, FSA 3, Corporate 2, Equity 3, FI 3, Deriv 2, Alts 1, PM 3, Ethics 2.

Mocks 1 and 2 are drawn from the item-set bank (`source: bank`) and embed each set's sections.
Mocks 3 to 6 are the fresh sets written per MOCK_SPEC.md, stored as bank notes with `source: mock-0<n>`;
this script inlines them into `### Vignette` / `### Questions` blocks and one foldable answer key per set.
Rerun after any edit to an item-set note; the mocks are generated, do not hand-edit them.
"""

from __future__ import annotations

import random
import re
import sys
from pathlib import Path

from cfa_common import L2, read_frontmatter

TARGET = {"01": 2, "02": 1, "03": 3, "04": 2, "05": 3, "06": 3, "07": 2, "08": 1, "09": 3, "10": 2}
BANK_MOCKS = (1, 2)
FRESH_MOCKS = (3, 4, 5, 6)
MOCKS_DIR = L2 / "21-Mocks"


def header(n: int, note: str) -> list[str]:
    return [
        "---",
        "type: cfa-mock",
        f"mock: {n}",
        "sessions: 2",
        "minutes_per_session: 132",
        "tags: [cfa/l2, cfa/mock]",
        "---",
        f"# Mock {n}",
        "",
        "Two sessions of 2 hours 12 minutes, 11 item sets each, no notes, calculator reset before each session.",
        f"Log the attempt with QuickAdd (CFA: log attempt) with source Mock-{n:02d} and confidence recorded before opening any answer key.",
        note,
        "",
    ]


def sections(body: str) -> dict[str, str]:
    """Split an item-set body into its level-2 sections, keyed by heading text."""
    out: dict[str, str] = {}
    parts = re.split(r"^## (.+)$", body, flags=re.M)
    for name, text in zip(parts[1::2], parts[2::2], strict=True):
        out[name.strip()] = text.strip("\n")
    return out


def demote(text: str) -> str:
    """Push headings inside a section one level down so they nest under the mock's ### blocks."""
    return re.sub(r"^(#{3,5}) ", r"#\1 ", text, flags=re.M)


def as_callout(text: str) -> list[str]:
    out = []
    for line in text.splitlines():
        if line.startswith(">"):
            out.append(line)
        else:
            out.append(("> " + line) if line.strip() else ">")
    return out


def answer_block(i: int, key: str, secs: dict[str, str]) -> list[str]:
    lines = [f"> [!success]- Item set {i} ({key})"]
    body = [ln for ln in secs.get("Answer key", "").splitlines() if not re.match(r"^>\s*\[!success\]", ln)]
    while body and not body[0].strip(" >"):
        body.pop(0)
    lines += as_callout("\n".join(body))
    distractors = secs.get("Distractor design", "").strip()
    if distractors:
        lines += [">", "> **Distractor design**", ">"] + as_callout(distractors)
    return lines + [""]


def load_sets() -> list[tuple[Path, dict]]:
    out = []
    for note in sorted((L2 / "20-Item-Set-Bank").rglob("IS-*.md")):
        fm, _ = read_frontmatter(note)
        if fm.get("type") == "cfa-itemset":
            out.append((note, fm))
    return out


def code_of(fm: dict) -> str:
    return str(fm.get("topic_code")).zfill(2)


def key_of(fm: dict) -> str:
    return f"{code_of(fm)}-{int(fm.get('lm', 0)):02d}"


def render_bank_mocks(sets: list[tuple[Path, dict]]) -> tuple[dict[str, str], list[str], int]:
    """Mocks 1 and 2 as {file name: text}, plus progress messages and a count of shortfalls."""
    random.seed(2026)
    bank: dict[str, list[tuple[Path, dict]]] = {c: [] for c in TARGET}
    for note, fm in sets:
        if fm.get("source") == "bank":
            bank[code_of(fm)].append((note, fm))
    used: set[Path] = set()
    short = 0
    out: dict[str, str] = {}
    msgs: list[str] = []
    for n in BANK_MOCKS:
        chosen = []
        for code, k in TARGET.items():
            pool = [s for s in bank[code] if s[0] not in used]
            random.shuffle(pool)
            pick = []
            for s in pool:  # never the same LM twice in one mock
                if len(pick) < k and key_of(s[1]) not in {key_of(p[1]) for p in pick}:
                    pick.append(s)
            if len(pick) < k:
                msgs.append(f"Mock-{n:02d}: topic {code} has only {len(pick)} unused bank item sets, need {k}")
                short += 1
            chosen += pick
            used |= {p[0] for p in pick}
        random.shuffle(chosen)
        lines = header(n, "Built from the item-set bank by build_mocks.py; each block embeds the bank note.")
        for i, (p, fm) in enumerate(chosen, 1):
            if i in (1, 12):
                lines += [f"## Session {1 if i == 1 else 2}", ""]
            lines += [
                f"## Item set {i} ({key_of(fm)}): [[{p.stem}]]",
                "",
                f"![[{p.stem}#Vignette]]",
                "",
                f"![[{p.stem}#Questions]]",
                "",
            ]
        lines += ["## Answer keys", ""]
        for i, (p, fm) in enumerate(chosen, 1):
            lines += [f"### Item set {i} ({key_of(fm)})", "", f"![[{p.stem}#Answer key]]", "", f"![[{p.stem}#Distractor design]]", ""]
        out[f"Mock-{n:02d}.md"] = "\n".join(lines)
        msgs.append(f"Mock-{n:02d}: {len(chosen)} item sets from the bank")
    return out, msgs, short


def render_fresh_mock(n: int, sets: list[tuple[Path, dict]]) -> tuple[str | None, str, int]:
    """One fresh mock's text (None when it has no item sets), a progress message, and 1 if it is not 22 sets."""
    mine = [(p, fm) for p, fm in sets if fm.get("source") == f"mock-{n:02d}"]
    if not mine:
        return None, f"Mock-{n:02d}: no item sets with source mock-{n:02d}, skipped", 1
    random.seed(2026 + n)
    random.shuffle(mine)
    lines = header(n, f"Fresh item sets written for this mock (source mock-{n:02d}); each also lives in the bank under its own note.")
    keys = []
    for i, (p, fm) in enumerate(mine, 1):
        if i in (1, 12):
            lines += [f"## Session {1 if i == 1 else 2}", ""]
        secs = sections(read_frontmatter(p)[1])
        keys.append((i, key_of(fm), secs))
        lines += [
            f"## Item set {i} ({key_of(fm)}): {fm.get('title', p.stem)}",
            "",
            f"Source: [[{p.stem}]], difficulty {fm.get('difficulty')}.",
            "",
            "### Vignette",
            "",
            demote(secs.get("Vignette", "")),
            "",
            "### Questions",
            "",
            demote(secs.get("Questions", "")),
            "",
        ]
    lines += ["## Answer keys", ""]
    for i, key, secs in keys:
        lines += answer_block(i, key, secs)
    return "\n".join(lines), f"Mock-{n:02d}: {len(mine)} fresh item sets", 0 if len(mine) == 22 else 1


def render_mocks() -> tuple[dict[str, str], list[str], int]:
    """Every mock as {file name: text} from the current item sets, without writing anything.

    verify_practice.py compares this with the committed mocks, so a mock can never drift from its sources.
    """
    sets = load_sets()
    out, msgs, problems = render_bank_mocks(sets)
    for n in FRESH_MOCKS:
        text, msg, bad = render_fresh_mock(n, sets)
        msgs.append(msg)
        problems += bad
        if text is not None:
            out[f"Mock-{n:02d}.md"] = text
    return out, msgs, problems


def main() -> int:
    MOCKS_DIR.mkdir(exist_ok=True)
    mocks, msgs, problems = render_mocks()
    for name, text in mocks.items():
        (MOCKS_DIR / name).write_text(text)
    print("\n".join(msgs))
    return 0 if not problems else 1


if __name__ == "__main__":
    sys.exit(main())
