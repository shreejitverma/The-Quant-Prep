"""Import an interview question bank into the private overlay.

A bank lives in one folder (normally under ``private/``, which git ignores):

    <bank>/source.tsv        firm <TAB> category <TAB> question, one per row; a row whose
                             category cell is known starts a question, other lines continue it
    <bank>/answers/*.json    {question_id: {"topic", "answer", "duplicate_of", "verified"}}
    <bank>/bank.json         generated: merged questions with firms, topics and answers
    <bank>/notes/*.md        generated: one note per syllabus topic, ``extends: <topic>``,
                             so the cards join that topic's review queue and readiness
    <bank>/By-Firm.md        generated: every question grouped by the firms that asked it

Re-running the import after refreshing ``source.tsv`` keeps every existing answer and id:
ids are derived from the normalised question text, and answers live in their own files.
If a refresh re-keys a near-duplicate cluster, ``qp bank`` lists the orphaned answer ids to re-key.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

CATEGORIES = ("fermi", "statistics", "expected value", "bayes", "logic", "probability", "math", "coding")
NEAR_DUPLICATE = 0.93  # difflib ratio at or above which two normalised questions are merged
PENDING = "Answer pending: not written or verified yet."


@dataclass
class Question:
    id: str
    prompt: str
    firms: list[str] = field(default_factory=list)
    categories: list[str] = field(default_factory=list)
    reports: int = 1
    topic: str | None = None
    answer: str | None = None
    verified: bool = False
    duplicate_of: str | None = None

    def to_dict(self) -> dict:
        return {k: v for k, v in self.__dict__.items() if k != "id"}


def normalise(text: str) -> str:
    text = text.lower().replace("dice", "die").replace("’", "'")
    text = re.sub(r"[^a-z0-9/.^%$+-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def question_id(prefix: str, text: str) -> str:
    norm = normalise(text)
    words = re.sub(r"[^a-z0-9 ]", "", norm).split()[:6]
    digest = hashlib.sha1(norm.encode()).hexdigest()[:5]
    return f"{prefix}-{'-'.join(words)}-{digest}" if words else f"{prefix}-{digest}"


def parse_source(text: str) -> list[tuple[str, str, str]]:
    """Rows of (firm, category, question). Continuation lines are joined with a space."""
    rows: list[list[str]] = []
    for raw in text.splitlines():
        parts = raw.rstrip().split("\t")
        # a row whose second cell is a category starts a question, even when the question text
        # itself is on the following lines (editors often strip the trailing tab)
        if len(parts) >= 2 and parts[1].strip().lower() in CATEGORIES:
            rows.append([parts[0].strip(), parts[1].strip().lower(), "\t".join(parts[2:]).strip()])
        elif rows and raw.strip():
            rows[-1][2] = f"{rows[-1][2]} {raw.strip()}".strip()
    return [(f, c, re.sub(r"\s+", " ", q)) for f, c, q in rows if q.strip()]


def dedupe(rows: list[tuple[str, str, str]], prefix: str) -> dict[str, Question]:
    """Merge exact and near-exact duplicates (after normalisation), keeping every firm and category."""
    out: dict[str, Question] = {}
    norms: dict[str, str] = {}  # normalised text -> id
    for firm, category, prompt in rows:
        norm = normalise(prompt)
        qid = norms.get(norm)
        if qid is None:
            close = difflib.get_close_matches(norm, list(norms), n=1, cutoff=NEAR_DUPLICATE)
            qid = norms[close[0]] if close else None
        if qid is None:
            qid = question_id(prefix, prompt)
            out[qid] = Question(qid, prompt, reports=0)
        norms[norm] = qid
        q = out[qid]
        q.reports += 1
        if firm and firm not in q.firms:
            q.firms.append(firm)
        if category not in q.categories:
            q.categories.append(category)
    return out


def load_answers(bank: Path) -> dict[str, dict]:
    merged: dict[str, dict] = {}
    for path in sorted((bank / "answers").glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        for qid, entry in data.items():
            merged.setdefault(qid, {}).update(entry)
    return merged


def build(bank: Path, prefix: str) -> dict[str, Question]:
    questions = dedupe(parse_source((bank / "source.tsv").read_text(encoding="utf-8")), prefix)
    for qid, entry in load_answers(bank).items():
        if qid not in questions:
            continue  # answer for a question no longer in the source: ignore, keep the file
        q = questions[qid]
        q.topic = entry.get("topic", q.topic)
        q.answer = entry.get("answer", q.answer)
        q.verified = bool(entry.get("verified", q.verified))
        q.duplicate_of = entry.get("duplicate_of") or None

    # fold semantic duplicates (declared in answers) into their canonical question, following
    # chains (a -> b -> c) to the root and ignoring cycles and dangling targets
    def root(q: Question) -> Question | None:
        seen = {q.id}
        cur = q
        while cur.duplicate_of:
            nxt = questions.get(cur.duplicate_of)
            if nxt is None or nxt.id in seen:
                return None
            seen.add(nxt.id)
            cur = nxt
        return cur if cur is not q else None

    roots = {q.id: root(q) for q in questions.values()}
    for q in questions.values():
        target = roots[q.id]
        q.duplicate_of = target.id if target else None
        if target is None:
            continue
        target.reports += q.reports
        target.firms += [f for f in q.firms if f not in target.firms]
        target.categories += [c for c in q.categories if c not in target.categories]
    return questions


def card_text(q: Question) -> str:
    firms = ", ".join(q.firms) if q.firms else "firm not recorded"
    head = f"*Asked at {firms}; {', '.join(q.categories)}; reported {q.reports} time{'s' if q.reports != 1 else ''}.*"
    body = q.answer.strip() if q.answer else PENDING
    lines = [f"> [!question]- {q.id} | {q.prompt}", f"> {head}", ">"]
    lines += [f"> {line}" if line else ">" for line in body.splitlines()]
    return "\n".join(lines)


def render(bank: Path, questions: dict[str, Question], name: str, topics: dict[str, str]) -> list[Path]:
    """Write bank.json, one note per topic, By-Firm.md and README.md. Returns written paths."""
    live = [q for q in questions.values() if not q.duplicate_of]
    unknown = sorted({q.topic for q in live if q.topic and q.topic not in topics})
    if unknown:
        raise ValueError(f"unknown topic ids in answers: {', '.join(unknown)}")
    written: list[Path] = []
    (bank / "bank.json").write_text(json.dumps({q.id: q.to_dict() for q in questions.values()}, indent=1, sort_keys=True) + "\n")
    written.append(bank / "bank.json")
    notes_dir = bank / "notes"
    notes_dir.mkdir(exist_ok=True)
    for old in notes_dir.glob("*.md"):
        old.unlink()
    by_topic: dict[str, list[Question]] = {}
    for q in live:
        by_topic.setdefault(q.topic or "unsorted", []).append(q)
    for topic, qs in sorted(by_topic.items()):
        qs.sort(key=lambda q: (-q.reports, q.prompt.lower()))
        answered = sum(1 for q in qs if q.answer)
        title = topics.get(topic, "Unsorted")
        extends = f"extends: {topic}\n" if topic in topics else ""
        front = (
            f"---\ntype: {'problem-set' if extends else 'reference'}\n"
            "track: [quant-trader, quant-research, quant-dev]\ntier: core\nstatus: draft\n"
            f"{extends}est_hours: {max(1, round(len(qs) * 0.15))}\nsources: []\n---\n"
        )
        body = [
            front,
            f"# {name}: {title}",
            "",
            f"{len(qs)} question{'' if len(qs) == 1 else 's'} from {name}, {answered} answered.",
            "Private: generated by `./qp bank`; edit answers in `answers/*.json`, not here.",
            "",
        ]
        body += [card_text(q) + "\n" for q in qs if q.answer]
        pending = [q for q in qs if not q.answer]
        if pending:  # not cards: an empty answer must never enter spaced review
            body += ["## Not yet answered", ""] + [f"- `{q.id}` {q.prompt}" for q in pending] + [""]
        path = notes_dir / f"{topic}.md"
        path.write_text("\n".join(body).rstrip() + "\n")
        written.append(path)
    firms: dict[str, list[Question]] = {}
    for q in live:
        for f in q.firms or ["(firm not recorded)"]:
            firms.setdefault(f, []).append(q)
    lines = [
        "---\ntype: reference\ntrack: [quant-trader, quant-research, quant-dev]\ntier: core\nstatus: draft\nsources: []\n---\n",
        f"# {name}: questions by firm",
        "",
    ]
    for f, qs in sorted(firms.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        lines += [f"## {f} ({len(qs)})", ""]
        for q in sorted(qs, key=lambda q: q.prompt.lower()):
            link = f"notes/{q.topic or 'unsorted'}.md"
            lines.append(f"- [{q.prompt[:140]}]({link}) `{q.id}`")
        lines.append("")
    (bank / "By-Firm.md").write_text("\n".join(lines).rstrip() + "\n")
    written.append(bank / "By-Firm.md")
    return written


def orphaned_answers(bank: Path, questions: dict[str, Question]) -> list[str]:
    """Answer ids that match no current question, e.g. after a refreshed source re-keyed a cluster."""
    return sorted(qid for qid in load_answers(bank) if qid not in questions)


def summary(questions: dict[str, Question]) -> dict:
    live = [q for q in questions.values() if not q.duplicate_of]
    return {
        "rows": sum(q.reports for q in live),
        "unique": len(live),
        "answered": sum(1 for q in live if q.answer),
        "verified": sum(1 for q in live if q.verified),
        "unsorted": sum(1 for q in live if not q.topic),
        "semantic_duplicates": sum(1 for q in questions.values() if q.duplicate_of),
    }
