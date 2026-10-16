"""Parse each module text into structured JSON: LOS, examples, practice problems, solutions, equations.

Output: build/cfa_l2/<topic-slug>/LM<nn>.json
Anything the heuristics cannot read cleanly is flagged needs_review with a printed page so a human or agent re-reads the PDF.
"""

from __future__ import annotations

import json
import re
import sys

from cfa_common import BUILD, COMMAND_VERBS, load_manifest

ODD_CHARS = re.compile(r"[​⁡-⁤-�]")
SECTION_HEAD = re.compile(r"^\s{0,4}[A-Z][A-Z ,&/:\-\(\)]{6,}$")


def pages_of(text: str) -> list[str]:
    return text.split("\f")


def printed_page(module: dict, page_index: int) -> int:
    return module["pdf_pages"][0] + page_index - module["page_offset"]


def parse_los(text: str) -> tuple[list[str], bool]:
    """Union of every LEARNING OUTCOMES block in the module, in order, deduplicated.

    Each block runs from "The candidate should be able to:" to the first blank line
    (one blank line is tolerated when the next line is another LOS at the same indent).
    Sidebar notes printed at the right margin are stripped (3+ space runs and deep-indent lines).
    """
    items: list[str] = []
    for m in re.finditer(r"The candidate should be able to:[^\n]*\n", text):
        lines = text[m.end() :].split("\n", 80)
        base_indent = None
        blank_run = 0
        for raw in lines:
            if "\f" in raw:
                break
            stripped = raw.strip()
            if not stripped:
                blank_run += 1
                if blank_run >= 2:
                    break
                continue
            indent = len(raw) - len(raw.lstrip(" "))
            if base_indent is None:
                base_indent = indent
            if indent > base_indent + 6:
                continue  # sidebar-only line
            if indent < base_indent - 2:
                break  # left-margin header such as STANDARD I or INTRODUCTION
            line = re.split(r"\s{3,}", stripped)[0].strip()
            if not line or line.lower() == "mastery" or re.fullmatch(r"\d+", line) or re.fullmatch(r"[A-Z][A-Z ,&/:\-]{6,}", line):
                if re.fullmatch(r"[A-Z][A-Z ,&/:\-]{6,}", line):
                    break
                continue
            first = re.split(r"\W", line, maxsplit=1)[0].lower()
            prev = items[-1] if items else ""
            if blank_run == 1 and first not in COMMAND_VERBS:
                break
            blank_run = 0
            starts_new = first in COMMAND_VERBS and (
                not prev or not re.search(r"(,|\(|/|\band\b|\bor\b|\bthe\b|\bof\b|\bto\b|\ba\b|\ban\b|-)\s*$", prev)
            )
            if starts_new or not items:
                items.append(line)
            else:
                items[-1] = (prev + line) if prev.endswith("-") else prev + " " + line
    items = [re.sub(r"\s+", " ", i).strip() for i in items]
    seen, uniq = set(), []
    for i in items:
        key = i.lower()
        if key not in seen:
            seen.add(key)
            uniq.append(i)
    return uniq, len(uniq) == 0


def parse_examples(text: str, module: dict) -> list[dict]:
    pages = pages_of(text)
    out = []
    for pi, page in enumerate(pages):
        for m in re.finditer(r"^\s*(?:●\s*)?(?:EXAMPLE|Example)\s+(\d+)\b[^\n]*$", page, re.M):
            n = int(m.group(1))
            body = page[m.end() :]
            nxt = re.search(r"^\s*(?:●\s*)?(?:EXAMPLE|Example)\s+\d+\b", body, re.M)
            if nxt:
                body = body[: nxt.start()]
            else:
                # continue onto following pages until the next EXAMPLE or a practice-problems header
                for q in pages[pi + 1 : pi + 4]:
                    stop = re.search(r"^\s*(?:●\s*)?((?:EXAMPLE|Example)\s+\d+\b|PRACTICE PROBLEMS|SUMMARY)", q, re.M)
                    body += "\f" + (q[: stop.start()] if stop else q)
                    if stop:
                        break
            title_m = re.match(r"\s*\n?\s*([^\n]{3,120})", body)
            out.append(
                {
                    "n": n,
                    "printed_page": printed_page(module, pi),
                    "title": title_m.group(1).strip() if title_m else "",
                    "has_solution": bool(re.search(r"^\s*Solution", body, re.M)),
                    "text": body.strip()[:12000],
                }
            )
    for pi, page in enumerate(pages):
        for m in re.finditer(r"^\s*KNOWLEDGE CHECK\s*$", page, re.M):
            body = page[m.end() :]
            nxt = re.search(r"^\s*(KNOWLEDGE CHECK|PRACTICE PROBLEMS|SUMMARY)\s*$", body, re.M)
            if nxt:
                body = body[: nxt.start()]
            else:
                for q in pages[pi + 1 : pi + 4]:
                    stop = re.search(r"^\s*(KNOWLEDGE CHECK|PRACTICE PROBLEMS|SUMMARY)\s*$", q, re.M)
                    body += "\f" + (q[: stop.start()] if stop else q)
                    if stop:
                        break
            out.append(
                {
                    "n": 1000 + len([e for e in out if e["n"] >= 1000]) + 1,
                    "kind": "knowledge_check",
                    "printed_page": printed_page(module, pi),
                    "title": re.sub(r"\s+", " ", body.strip().split("\n", 1)[0])[:120],
                    "has_solution": bool(re.search(r"^\s*Solution", body, re.M)),
                    "text": body.strip()[:12000],
                }
            )
    # keep first occurrence of each example number (headers can repeat across page breaks)
    seen, uniq = set(), []
    for e in out:
        if e["n"] in seen:
            continue
        seen.add(e["n"])
        uniq.append(e)
    return uniq


def split_numbered(block: str) -> list[dict]:
    items, cur, num = [], [], 0
    for line in block.splitlines():
        m = re.match(r"^\s*(\d{1,3})\.(?:\s+(\S.*)|\s*)$", line)
        if m and int(m.group(1)) == num + 1:
            if cur:
                items.append({"n": num, "text": "\n".join(cur).strip()})
            num = int(m.group(1))
            cur = [m.group(2) or ""]
        elif num:
            cur.append(line)
    if cur:
        items.append({"n": num, "text": "\n".join(cur).strip()})
    return items


def after_header(text: str, *patterns: str) -> str:
    """Return the text after the first pattern that occurs, or the whole text when none does."""
    for pat in patterns:
        parts = re.split(pat, text, maxsplit=1, flags=re.M)
        if len(parts) > 1:
            return parts[1]
    return text


def parse_practice(text: str, module: dict) -> dict:
    pages = pages_of(text)
    pp = [i for i, p in enumerate(pages) if re.search(r"^\s*PRACTICE PROBLEMS\s*$", p, re.M)]
    ss = [
        i
        for i, p in enumerate(pages)
        if re.search(r"^[\s\u200b]*SOLUTIONS[\s\u200b]*$", p, re.M) or re.search(r"^Solutions\s{5,}\d+\s*$", p, re.M)
    ]
    if not pp:
        return {"problems": [], "solutions": [], "needs_review": True, "reason": "no PRACTICE PROBLEMS header"}
    p0 = pp[0]
    s0 = next((s for s in ss if s > p0), None)
    prob_text = "\n".join(pages[p0 : (s0 if s0 else len(pages))])
    sol_text = "\n".join(pages[s0:]) if s0 is not None else ""
    prob_text = prob_text.split("PRACTICE PROBLEMS", 1)[1]
    sol_text = after_header(sol_text, r"SOLUTIONS", r"^Solutions\s{5,}\d+\s*$") if sol_text else ""
    problems = split_numbered(prob_text)
    solutions = split_numbered(sol_text)
    vignettes = [
        m.group(0).strip() for m in re.finditer(r"The following information relates to questions?\s*\n?\s*[\d\-–, and]+", prob_text)
    ]
    return {
        "printed_page": printed_page(module, p0),
        "solutions_printed_page": printed_page(module, s0) if s0 is not None else None,
        "vignette_headers": vignettes,
        "problems": problems,
        "solutions": solutions,
        "raw_problems": prob_text.strip(),
        "raw_solutions": sol_text.strip(),
        "needs_review": len(problems) == 0 or len(solutions) == 0 or len(problems) != len(solutions),
    }


def parse_equations(text: str, module: dict) -> list[dict]:
    pages = pages_of(text)
    out = []
    stop_at = next((i for i, p in enumerate(pages) if re.search(r"^\s*PRACTICE PROBLEMS\s*$", p, re.M)), len(pages))
    for pi, page in enumerate(pages[:stop_at]):
        for line in page.splitlines():
            s = line.strip()
            if "=" not in s or len(s) < 4 or len(s) > 170:
                continue
            if re.search(r"[A-Za-z]", s) is None:
                continue
            if s.count(" ") > 18 and not re.search(r"[+\-*/^()]", s):
                continue  # prose sentence containing '='
            lhs = s.split("=", 1)[0].strip()
            out.append(
                {
                    "printed_page": printed_page(module, pi),
                    "text": s,
                    "lhs": lhs[:40],
                    "needs_review": bool(ODD_CHARS.search(s)) or len(lhs) > 40 or "_" in s,
                }
            )
    return out


def main() -> int:
    manifest = load_manifest()
    rows = []
    for topic in manifest["topics"]:
        for module in topic["modules"]:
            path = BUILD / topic["slug"] / f"LM{module['lm']:02d}.txt"
            text = path.read_text()
            los, los_flag = parse_los(text)
            examples = parse_examples(text, module)
            practice = parse_practice(text, module)
            equations = parse_equations(text, module)
            data = {
                "topic_code": topic["code"],
                "topic": topic["name"],
                "topic_slug": topic["slug"],
                "volume": topic["volume"],
                "weight": topic["weight"],
                "lm": module["lm"],
                "title": module["title"],
                "printed_pages": module["printed_pages"],
                "pdf_pages": module["pdf_pages"],
                "los": los,
                "los_needs_review": los_flag,
                "examples": examples,
                "practice": practice,
                "equations": equations,
                "needs_review_count": int(los_flag) + int(practice["needs_review"]) + sum(1 for e in equations if e["needs_review"]),
            }
            (BUILD / topic["slug"] / f"LM{module['lm']:02d}.json").write_text(json.dumps(data, indent=1, ensure_ascii=False))
            rows.append(
                (
                    topic["code"],
                    module["lm"],
                    module["title"][:48],
                    len(los),
                    len(examples),
                    len(practice["problems"]),
                    len(practice["solutions"]),
                    len(equations),
                    data["needs_review_count"],
                )
            )
    print(f"{'T':>2} {'LM':>2} {'title':<48} {'LOS':>3} {'ex':>3} {'pp':>3} {'sol':>3} {'eq':>4} {'rev':>4}")
    for r in rows:
        print(f"{r[0]:>2} {r[1]:>2} {r[2]:<48} {r[3]:>3} {r[4]:>3} {r[5]:>3} {r[6]:>3} {r[7]:>4} {r[8]:>4}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
