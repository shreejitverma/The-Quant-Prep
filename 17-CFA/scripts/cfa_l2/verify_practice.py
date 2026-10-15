"""Gate for the practice layer: item sets per LM and their structure, mock composition, SRS decks parse."""
from __future__ import annotations

import json
import re
import sys

from cfa_common import BUILD, EM_DASH, EMOJI_RE, L2, read_frontmatter

BANDS = {"01": (5, 10), "02": (5, 10), "03": (10, 15), "04": (5, 10), "05": (10, 15), "06": (10, 15), "07": (5, 10), "08": (5, 10), "09": (10, 15), "10": (10, 15)}
REQUIRED_KEYS = ("type", "topic", "topic_code", "topic_slug", "lm", "title", "los", "difficulty", "minutes", "source", "attempts", "tags")
FRESH_MOCKS = ("mock-03", "mock-04", "mock-05", "mock-06")


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.M | re.S)
    return m.group(1) if m else ""


def check_itemset(note, fm: dict, body: str, los_ids: set[str]) -> list[str]:
    fails = []
    missing = [k for k in REQUIRED_KEYS if k not in fm]
    if missing:
        fails.append(f"missing frontmatter {', '.join(missing)}")
    prefix = f"los-{str(fm.get('topic_code')).zfill(2)}-{int(fm.get('lm', 0)):02d}-"
    los = fm.get("los") if isinstance(fm.get("los"), list) else []
    bad = [x for x in los if x not in los_ids or not x.startswith(prefix)]
    if not los or bad:
        fails.append(f"frontmatter los invalid for this module: {bad or 'empty'}")
    for name in ("Vignette", "Questions", "Answer key", "Distractor design"):
        if f"## {name}" not in body:
            fails.append(f"no {name} section")
    questions = section(body, "Questions")
    qs = len(re.findall(r"^\d+\.\s", questions, re.M))
    tags = re.findall(r"\(LOS:\s*(los-[\w-]+)\)", questions)
    fresh = fm.get("source") in FRESH_MOCKS
    if fresh and qs != 4:
        fails.append(f"{qs} questions, a mock set needs exactly 4")
    elif not 4 <= qs <= 6:
        fails.append(f"{qs} questions, need 4 to 6")
    if len(tags) != qs:
        fails.append(f"{len(tags)} LOS tags for {qs} questions")
    wrong = [t for t in tags if t not in los_ids or not t.startswith(prefix)]
    if wrong:
        fails.append(f"question LOS tags not in this module: {wrong}")
    if "[!success]-" not in section(body, "Answer key"):
        fails.append("answer key is not a foldable success callout")
    keyed = len(re.findall(r"^>\s*\d+\.\s", section(body, "Answer key"), re.M))
    if keyed != qs:
        fails.append(f"answer key has {keyed} answers for {qs} questions")
    text = note.read_text()
    if EM_DASH in text:
        fails.append("em dash character")
    if EMOJI_RE.search(text):
        fails.append("emoji")
    return fails


def main() -> int:
    manifest = json.loads((BUILD / "manifest.json").read_text())
    los_ids = set(json.loads((BUILD / "los_index.json").read_text()))
    failures = []
    counts: dict[str, int] = {}
    fresh: dict[str, list[dict]] = {m: [] for m in FRESH_MOCKS}
    for note in sorted((L2 / "20-Item-Set-Bank").rglob("IS-*.md")):
        fm, body = read_frontmatter(note)
        if fm.get("type") != "cfa-itemset":
            failures.append(f"{note.name}: type is not cfa-itemset")
            continue
        key = f"{str(fm.get('topic_code')).zfill(2)}-{int(fm.get('lm', 0)):02d}"
        if fm.get("source") == "bank":
            counts[key] = counts.get(key, 0) + 1
        elif fm.get("source") in fresh:
            fresh[fm["source"]].append({**fm, "key": key})
        else:
            failures.append(f"{note.name}: unknown source {fm.get('source')!r}")
        failures += [f"{note.name}: {f}" for f in check_itemset(note, fm, body, los_ids)]
    print(f"{'lm':<6} {'bank sets':>9}")
    for topic in manifest["topics"]:
        for module in topic["modules"]:
            key = f"{topic['code']}-{module['lm']:02d}"
            n = counts.get(key, 0)
            print(f"{key:<6} {n:>9}")
            if n < 3:
                failures.append(f"{key}: {n} bank item sets, need 3")
    for src, sets in fresh.items():
        if not sets:
            continue
        keys = [s["key"] for s in sets]
        dup = sorted({k for k in keys if keys.count(k) > 1})
        if dup:
            failures.append(f"{src}: module tested twice {dup}")
        hard = sum(1 for s in sets if s.get("difficulty") == 4)
        if hard < 6:
            failures.append(f"{src}: {hard} sets at difficulty 4, need 6")
    for mock in sorted((L2 / "21-Mocks").glob("Mock-*.md")):
        fm, body = read_frontmatter(mock)
        sets = re.findall(r"^## Item set \d+.*?\((\d{2})-", body, re.M)
        if len(sets) != 22:
            failures.append(f"{mock.name}: {len(sets)} item sets, need 22")
        by = {c: sets.count(c) for c in BANDS}
        for c, (lo, hi) in BANDS.items():
            pct = 100 * by[c] / 22
            if not (lo - 2.5 <= pct <= hi + 2.5):
                failures.append(f"{mock.name}: topic {c} is {pct:.0f}% ({by[c]} sets), band {lo}-{hi}%")
        print(f"{mock.name}: {len(sets)} item sets")
    cards, dupes = 0, 0
    seen = set()
    for note in L2.rglob("*.md"):
        text = note.read_text()
        if "#flashcards/cfa-l2" not in text:
            continue
        for m in re.finditer(r"^(?!\s*[#>\-\*])(.+?)\s*::\s*(.+)$", text, re.M):
            cards += 1
            if m.group(1).strip() in seen:
                dupes += 1
            seen.add(m.group(1).strip())
        cards += len(re.findall(r"^\?\s*$", text, re.M))
    if dupes:
        failures.append(f"{dupes} duplicate single-line flashcards")
    print(f"flashcards: {cards} ({dupes} duplicates)")
    for f in failures:
        print("FAIL", f)
    print(f"\nverify_practice: {len(failures)} failures")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
