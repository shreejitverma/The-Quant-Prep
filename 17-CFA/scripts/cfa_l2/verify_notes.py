"""Gate for the LM notes: 11 sections present and substantive, every LOS from extraction present with a block ID,
formula IDs unique and embedded in the formula sheet, no emoji, em dash or draft leftover anywhere under CFA-L-2.
A draft leftover is author reasoning left in the finished text, such as `wait:`, a line starting `Correction:`, `scratch that` or `let me recompute`."""
from __future__ import annotations

import json
import re
import sys

from cfa_common import BUILD, EM_DASH, EMOJI_RE, L2, PRACTICE_PRIVATE, lm_note_name, read_frontmatter

# Draft leftovers: an author reasoning aloud in the finished text, which has produced a wrong keyed answer before.
DRAFT_RE = re.compile(r"(?:\bwait:|^>?\s*Correction:|\bscratch that\b|\blet me (?:recompute|redo|try)\b|\boops\b|\bactually,? no[,.]|\bno:\s*(?:short|long|the)\b)", re.I | re.M)

SECTIONS = ["LOS map", "Core intuition", "Formulas and derivations", "Worked examples", "Item-set patterns", "Practice problems", "Cross-links", "Self-test", "Flashcards", "Common mistakes", "Teach-back"]
MIN_CHARS = {"LOS map": 200, "Core intuition": 1500, "Formulas and derivations": 400, "Worked examples": 800, "Item-set patterns": 800, "Practice problems": 800, "Cross-links": 60, "Self-test": 1500, "Flashcards": 800, "Common mistakes": 300, "Teach-back": 0}
PRIVATE_POINTER = re.compile(r"^!\[\[([^\]|#]+-Practice-Problems)\]\]\s*$", re.M)


def sections_of(body: str) -> dict[str, str]:
    out = {}
    for m in re.finditer(r"^## (.+?)\s*$", body, re.M):
        start = m.end()
        nxt = re.search(r"^## ", body[start:], re.M)
        out[m.group(1).strip()] = body[start : start + nxt.start()] if nxt else body[start:]
    return out


def resolve_private(secs: dict[str, str]) -> str | None:
    """Swap a Practice problems pointer for the private note it embeds, in place.

    The restated curriculum problems are copyrighted, so the public note only embeds
    PRACTICE_PRIVATE/<note>-Practice-Problems.md. Returns a failure message when the overlay exists but the
    embedded note does not. Without the overlay (a fresh clone) the section is set to None: present, unchecked.
    """
    text = secs.get("Practice problems")
    m = PRIVATE_POINTER.search(text) if text is not None else None
    if not m:
        return None
    if not PRACTICE_PRIVATE.is_dir():
        secs["Practice problems"] = None
        return None
    target = PRACTICE_PRIVATE / f"{m.group(1)}.md"
    if not target.exists():
        return f"Practice problems embeds {m.group(1)}, missing from {PRACTICE_PRIVATE}"
    secs["Practice problems"] = read_frontmatter(target)[1]
    return None


def thin_sections(secs: dict[str, str | None]) -> list[str]:
    """Required sections that are missing or below their minimum size; None means present but unchecked."""
    out = []
    for s in SECTIONS:
        if s not in secs:
            out.append(f"section missing: {s}")
        elif secs[s] is not None and len(secs[s].strip()) < MIN_CHARS[s]:
            out.append(f"section too thin: {s} ({len(secs[s].strip())} chars, need {MIN_CHARS[s]})")
    return out


def main(topic_filter: str | None = None) -> int:
    manifest = json.loads((BUILD / "manifest.json").read_text())
    failures, checked, all_f_ids = [], 0, {}
    for topic in manifest["topics"]:
        if topic_filter and topic["code"] != topic_filter:
            continue
        for module in topic["modules"]:
            note = L2 / topic["slug"] / f"{lm_note_name(topic['code'], module['lm'], module['title'])}.md"
            tag = f"{topic['code']}-{module['lm']:02d}"
            if not note.exists():
                failures.append(f"{tag}: note missing ({note.name})")
                continue
            checked += 1
            fm, body = read_frontmatter(note)
            secs = sections_of(body)
            missing_private = resolve_private(secs)
            if missing_private:
                failures.append(f"{tag}: {missing_private}")
            failures += [f"{tag}: {problem}" for problem in thin_sections(secs)]
            data = json.loads((BUILD / topic["slug"] / f"LM{module['lm']:02d}.json").read_text())
            los_ids = re.findall(r"\^los-(\d{2})-(\d{2})-([a-z]+)", body)
            if len(los_ids) < len(data["los"]):
                failures.append(f"{tag}: {len(los_ids)} LOS block IDs, extraction found {len(data['los'])} LOS")
            for c, lm, letter in los_ids:
                if c != topic["code"] or int(lm) != module["lm"]:
                    failures.append(f"{tag}: foreign LOS id ^los-{c}-{lm}-{letter}")
            f_ids = re.findall(r"\^(f-\d{2}-\d{2}-\d+)\s*$", body, re.M)
            for f in f_ids:
                if f in all_f_ids:
                    failures.append(f"{tag}: duplicate formula id {f} (also in {all_f_ids[f]})")
                all_f_ids[f] = tag
            if not f_ids and topic["code"] != "10":
                failures.append(f"{tag}: no formula block IDs")
            for k in ("type", "topic", "topic_code", "topic_slug", "volume", "lm", "title", "pages", "weight_band", "difficulty", "status", "mastery", "next_review"):
                if k not in fm:
                    failures.append(f"{tag}: frontmatter missing {k}")
            if fm.get("type") != "cfa-lm":
                failures.append(f"{tag}: type is not cfa-lm")
    sheet = L2 / "40-Formula-Sheets" / "Master-Formula-Sheet.md"
    if sheet.exists():
        embedded = set()
        for f in (L2 / "40-Formula-Sheets").glob("*.md"):
            embedded |= set(re.findall(r"#\^(f-\d{2}-\d{2}-\d+)\]\]", f.read_text()))
        for f in all_f_ids:
            if f not in embedded:
                failures.append(f"{all_f_ids[f]}: formula {f} not embedded in a formula sheet (run build_formula_sheet.py)")
    private = sorted(PRACTICE_PRIVATE.glob("*.md")) if PRACTICE_PRIVATE.is_dir() else []
    for md in [*L2.rglob("*.md"), *private]:
        if "IFT-Slides" in md.parts:
            continue
        text = md.read_text()
        where = md.relative_to(L2) if md.is_relative_to(L2) else md.relative_to(PRACTICE_PRIVATE.parent)
        if EMOJI_RE.search(text):
            failures.append(f"emoji in {where}")
        if EM_DASH in text:
            failures.append(f"em dash in {where}")
        for m in DRAFT_RE.finditer(text):
            line = text.count("\n", 0, m.start()) + 1
            failures.append(f"draft leftover {m.group(0)!r} in {where}:{line}")
    for f in failures:
        print("FAIL", f)
    print(f"\nverify_notes: {checked} notes checked, {len(failures)} failures")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else None))
