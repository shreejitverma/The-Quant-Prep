"""Compute mastery per LM from attempts and errors, write it back to LM frontmatter, and move Kanban cards.

Mastery model (0-100):
  accuracy   recency-weighted accuracy over attempts touching the LM (half-life 14 days), default 0 with no attempts
  errors     each unresolved error on the LM subtracts 4 points (max 20)
  calibration if mean confidence exceeds accuracy by more than 10 points, subtract the excess (max 15)
  teach-back  a Teach-back section with 200 or fewer characters of prose caps mastery at 60
  status      not-started (no attempts, no teach-back), learning (<50), practicing (50-84), mastered (85+)
  next_review spaced by mastery: 1, 3, 7, 14, or 30 days from the last attempt

Only mastery, status, last_reviewed and next_review are rewritten in the frontmatter; every other line is kept verbatim.
Kanban (00-Strategy/Study-Board.md) is regenerated from scratch on every run: a module with a written teach-back that is
not yet mastered goes to Teach-Back Done, every other module goes to the column named after its status.
"""
from __future__ import annotations

import datetime as dt
import math
import re
import sys

from cfa_common import L2, TOPICS, read_frontmatter, write_frontmatter

TODAY = dt.date.today()
BOARD_NOTE = "This board is rewritten by `17-CFA/scripts/cfa_l2/mastery.py` on every run; cards added here by hand are discarded, so keep non-module tasks in [[Study-Plan]] or a daily note."


def parse_date(v) -> dt.date | None:
    try:
        return dt.date.fromisoformat(str(v)[:10])
    except Exception:
        return None


def collect() -> tuple[dict, dict]:
    attempts: dict[str, list] = {}
    for note in (L2 / "22-Attempts").glob("*.md"):
        fm, _ = read_frontmatter(note)
        if fm.get("type") != "cfa-attempt":
            continue
        d = parse_date(fm.get("date"))
        if not d or not fm.get("max"):
            continue
        acc = float(fm["score"]) / float(fm["max"])
        conf = float(fm.get("confidence", 3)) / 5
        lms = set()
        lm = str(fm.get("lm", "")).strip('"')
        if re.fullmatch(r"\d{2}-\d{2}", lm):
            lms.add(lm)
        for los in fm.get("los_missed", []) if isinstance(fm.get("los_missed"), list) else []:
            m = re.match(r"los-(\d{2})-(\d{2})", str(los))
            if m:
                lms.add(f"{m.group(1)}-{m.group(2)}")
        for key in lms:
            attempts.setdefault(key, []).append((d, acc, conf))
    errors: dict[str, int] = {}
    for note in (L2 / "23-Error-Log").glob("*.md"):
        fm, _ = read_frontmatter(note)
        if fm.get("type") == "cfa-error" and fm.get("resolved") is not True:
            key = str(fm.get("lm", "")).strip('"')
            errors[key] = errors.get(key, 0) + 1
    return attempts, errors


def main() -> int:
    attempts, errors = collect()
    rows = []
    for code, slug, vol, name, weight in TOPICS:
        for note in sorted((L2 / slug).glob("LM*.md")):
            fm, body = read_frontmatter(note)
            if fm.get("type") != "cfa-lm":
                continue
            key = f"{code}-{int(fm.get('lm', 0)):02d}"
            hist = attempts.get(key, [])
            if hist:
                w = [(math.pow(0.5, (TODAY - d).days / 14), a, c) for d, a, c in hist]
                sw = sum(x[0] for x in w)
                acc = sum(x[0] * x[1] for x in w) / sw
                conf = sum(x[0] * x[2] for x in w) / sw
                mastery = 100 * acc
                gap = 100 * (conf - acc)
                if gap > 10:
                    mastery -= min(15, gap - 10)
                last = max(d for d, _, _ in hist)
            else:
                mastery, last = 0.0, None
            mastery -= min(20, 4 * errors.get(key, 0))
            tb = re.search(r"^## Teach-back\s*$(.*?)(?=^## |\Z)", body, re.S | re.M)
            tb_text = re.sub(r">\s*\[!note\][^\n]*|>\s*", "", tb.group(1)).strip() if tb else ""
            teach_done = len(tb_text) > 200
            if not teach_done:
                mastery = min(mastery, 60)
            mastery = int(max(0, min(100, round(mastery))))
            if not hist and not teach_done:
                status = "not-started" if fm.get("status", "not-started") == "not-started" else fm.get("status")
            elif mastery >= 85:
                status = "mastered"
            elif mastery >= 50:
                status = "practicing"
            else:
                status = "learning"
            interval = 30 if mastery >= 85 else 14 if mastery >= 70 else 7 if mastery >= 50 else 3 if mastery > 0 else 1
            anchor = last or TODAY
            fm["mastery"] = mastery
            fm["status"] = status
            fm["last_reviewed"] = str(last) if last else fm.get("last_reviewed", "")
            fm["next_review"] = str(anchor + dt.timedelta(days=interval))
            write_frontmatter(note, fm, body)
            rows.append((key, note.stem, mastery, status, fm["next_review"], len(hist), errors.get(key, 0), teach_done))
    board = L2 / "00-Strategy" / "Study-Board.md"
    if board.exists():
        cols = {"not-started": "Not Started", "learning": "Reading", "practicing": "Practicing", "mastered": "Mastered"}
        cards: dict[str, list[str]] = {c: [] for c in ["Not Started", "Reading", "Practicing", "Teach-Back Done", "Mastered"]}
        for key, stem, m, status, nr, n, e, teach_done in rows:
            col = "Teach-Back Done" if teach_done and status != "mastered" else cols[status]
            cards[col].append(f"- [ ] [[{stem}]] {m}")
        text = board.read_text()
        head = text.split("## Not Started", 1)[0]
        fm_end = head.find("\n---\n", 4) if head.startswith("---\n") else -1
        head = (head[: fm_end + 5] if fm_end >= 0 else "") + "\n" + BOARD_NOTE + "\n\n"
        settings = text[text.find("%% kanban:settings"):] if "%% kanban:settings" in text else ""
        body = "".join(f"## {c}\n\n" + "\n".join(items) + ("\n" if items else "") + "\n\n" for c, items in cards.items())
        board.write_text(head + body + settings)
    print(f"{'lm':<6} {'note':<52} {'mast':>4} {'status':<12} {'next':<10} {'att':>3} {'err':>3}")
    for r in rows:
        print(f"{r[0]:<6} {r[1][:52]:<52} {r[2]:>4} {r[3]:<12} {r[4]:<10} {r[5]:>3} {r[6]:>3}")
    print(f"mastery updated for {len(rows)} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
