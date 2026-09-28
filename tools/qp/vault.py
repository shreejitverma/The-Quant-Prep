"""Load the curriculum: notes, frontmatter and question cards.

The Markdown notes on disk are the single source of truth. This module parses them
into plain dataclasses and never writes to them (see ``moc.py`` for the one writer).
"""

from __future__ import annotations

import os
import re
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

SECTION_RE = re.compile(r"^(\d\d)-[A-Za-z0-9-]+$")
ORDER_RE = re.compile(r"^(\d\d)-(.+)$")
CARD_RE = re.compile(r"^> \[!question\]-?\s+([a-z0-9][a-z0-9-]*)\s*\|\s*(.+?)\s*$")
HEADING_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)

TRACKS = ("quant-trader", "quant-research", "quant-dev")
TRACK_LABELS = {"quant-trader": "Quant Trader", "quant-research": "Quant Researcher", "quant-dev": "Quant Developer"}
TIERS = ("core", "advanced", "senior")
STATUSES = ("seed", "draft", "solid", "canonical")
# Note types whose mastery is tracked. Everything else is supporting material.
TRACKABLE_TYPES = ("concept", "problem-set", "playbook")
NOTE_TYPES = TRACKABLE_TYPES + ("reference", "firm", "moc", "guide")
# Folders inside a section that never hold notes.
PRIVATE_DIR = "private"
SKIP_DIRS = {"code", "protocol-specs", "_archive", "node_modules", "__pycache__"}


class VaultError(ValueError):
    """A note that cannot be parsed at all."""


@dataclass(frozen=True)
class Card:
    id: str
    prompt: str
    answer: str
    note_id: str
    line: int


@dataclass
class Note:
    id: str
    path: Path  # relative to the repo root
    section: str  # section folder name, e.g. "01-Probability"
    order: int  # numeric filename prefix, 99 when absent
    title: str
    meta: dict
    body: str
    cards: list[Card] = field(default_factory=list)

    @property
    def type(self) -> str:
        return str(self.meta.get("type") or "")

    @property
    def tracks(self) -> list[str]:
        value = self.meta.get("track") or []
        return value if isinstance(value, list) else [value]

    @property
    def tier(self) -> str:
        return str(self.meta.get("tier") or "core")

    @property
    def status(self) -> str:
        return str(self.meta.get("status") or "seed")

    @property
    def prereqs(self) -> list[str]:
        value = self.meta.get("prereqs") or []
        return value if isinstance(value, list) else [value]

    @property
    def est_hours(self) -> float:
        value = self.meta.get("est_hours")
        return float(value) if isinstance(value, (int, float)) else 0.0

    @property
    def extends(self) -> str | None:
        value = self.meta.get("extends")
        return str(value).lower() if value else None

    @property
    def trackable(self) -> bool:
        # A private note that extends a syllabus topic contributes cards to that topic instead.
        return self.type in TRACKABLE_TYPES and not self.extends


@dataclass
class Section:
    folder: str
    number: int
    title: str
    notes: list[Note] = field(default_factory=list)
    library: bool = False
    private: bool = False


@dataclass
class Vault:
    root: Path
    sections: list[Section]
    notes: dict[str, Note]
    cards: dict[str, Card]
    errors: list[str]  # problems found while loading (duplicates, parse errors)

    def topics(self, tracks: list[str] | None = None) -> list[Note]:
        """Trackable notes in syllabus order, optionally filtered to any of ``tracks``."""
        out = []
        for section in self.sections:
            for note in section.notes:
                if note.trackable and (not tracks or set(tracks) & set(note.tracks)):
                    out.append(note)
        return out

    def firms(self) -> list[Note]:
        return sorted((n for n in self.notes.values() if n.type == "firm"), key=lambda n: n.title.lower())

    def resolve(self, query: str) -> Note | None:
        """Find a note by exact id, then by unique id or title prefix/substring."""
        q = query.strip().lower()
        if q in self.notes:
            return self.notes[q]
        for pool in (
            [n for n in self.notes.values() if n.id.startswith(q)],
            [n for n in self.notes.values() if q in n.id or q in n.title.lower()],
        ):
            if len(pool) == 1:
                return pool[0]
        return None


def parse_scalar(raw: str):
    raw = raw.strip()
    if raw == "":
        return None
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        return [parse_scalar(x) for x in inner.split(",")] if inner else []
    if len(raw) >= 2 and raw[0] == raw[-1] and raw[0] in "\"'":
        return raw[1:-1]
    if re.fullmatch(r"-?\d+", raw):
        return int(raw)
    if re.fullmatch(r"-?\d+\.\d+", raw):
        return float(raw)
    return raw


def split_frontmatter(text: str) -> tuple[dict, str, int]:
    """Return (meta, body, body_start_line). Supports the flat YAML subset the vault uses."""
    if not text.startswith("---\n"):
        return {}, text, 1
    end = text.find("\n---", 4)
    if end == -1:
        raise VaultError("frontmatter is not closed")
    meta: dict = {}
    for lineno, line in enumerate(text[4:end].splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line or line.startswith(" "):
            raise VaultError(f"line {lineno}: unsupported frontmatter syntax: {line!r}")
        key, _, value = line.partition(":")
        meta[key.strip()] = parse_scalar(value)
    rest = text[end + 4 :]
    body = rest[1:] if rest.startswith("\n") else rest
    body_start = text[: end + 4].count("\n") + 2
    return meta, body, body_start


def parse_cards(body: str, note_id: str, first_line: int) -> list[Card]:
    cards: list[Card] = []
    lines = body.splitlines()
    i = 0
    while i < len(lines):
        m = CARD_RE.match(lines[i])
        if not m:
            i += 1
            continue
        start = i
        answer_lines = []
        i += 1
        while i < len(lines) and lines[i].startswith(">"):
            answer_lines.append(lines[i][2:] if lines[i].startswith("> ") else lines[i][1:])
            i += 1
        cards.append(Card(m.group(1), m.group(2), "\n".join(answer_lines).strip(), note_id, first_line + start))
    return cards


def note_id_for(path: Path) -> str:
    if path.name.lower() == "readme.md":
        return "moc:" + path.parent.as_posix()
    stem = path.stem
    m = ORDER_RE.match(stem)
    return (m.group(2) if m else stem).lower()


def load_note(root: Path, rel: Path, section: str, source: Path | None = None, nid: str | None = None) -> Note:
    text = (source or root / rel).read_text(encoding="utf-8")
    meta, body, body_start = split_frontmatter(text)
    nid = nid or note_id_for(rel)
    m = ORDER_RE.match(rel.stem)
    heading = HEADING_RE.search(body)
    title = heading.group(1) if heading else rel.stem.replace("-", " ")
    note = Note(nid, rel, section, int(m.group(1)) if m else 99, title, meta, body)
    note.cards = parse_cards(body, nid, body_start)
    return note


def section_info(root: Path, folder: str) -> tuple[str, bool]:
    """(title, is_library). A README with ``curriculum: false`` marks a free-form library section
    (for example an Obsidian research vault) that qp lists but does not parse or validate."""
    readme = root / folder / "README.md"
    title, library = folder[3:].replace("-", " "), False
    if readme.exists():
        meta, body, _ = split_frontmatter(readme.read_text(encoding="utf-8"))
        m = HEADING_RE.search(body)
        title = m.group(1) if m else title
        library = str(meta.get("curriculum")).lower() == "false"
    return title, library


def private_root(root: Path) -> Path:
    """The private overlay: ``$QP_PRIVATE`` if set, else ``<repo>/private`` (gitignored)."""
    env = os.environ.get("QP_PRIVATE")
    return Path(env).expanduser() if env else root / PRIVATE_DIR


def load_vault(root: Path = REPO_ROOT) -> Vault:
    sections: list[Section] = []
    notes: dict[str, Note] = {}
    cards: dict[str, Card] = {}
    errors: list[str] = []

    def add(note: Note, section: Section) -> None:
        if note.id in notes:
            errors.append(f"{note.path}: duplicate note id {note.id!r} (also {notes[note.id].path})")
            return
        notes[note.id] = note
        for card in note.cards:
            if card.id in cards:
                errors.append(f"{note.path}:{card.line}: duplicate card id {card.id!r} (also in {cards[card.id].note_id})")
                continue
            cards[card.id] = card
        section.notes.append(note)

    for folder in sorted(p.name for p in root.iterdir() if p.is_dir() and SECTION_RE.match(p.name)):
        title, library = section_info(root, folder)
        section = Section(folder, int(folder[:2]), title, library=library)
        paths = [root / folder / "README.md"] if library else sorted((root / folder).rglob("*.md"))
        for path in paths:
            rel = path.relative_to(root)
            if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[1:-1]):
                continue
            try:
                add(load_note(root, rel, folder), section)
            except (VaultError, UnicodeDecodeError) as exc:
                errors.append(f"{rel}: {exc}")
        section.notes.sort(key=lambda n: (n.path.parent != Path(folder), n.path.parent.as_posix(), n.order, n.id))
        sections.append(section)

    proot = private_root(root)
    if proot.is_dir():
        section = Section(PRIVATE_DIR, 99, "Private", private=True)
        readme = proot / "README.md"
        if readme.exists():
            _, body, _ = split_frontmatter(readme.read_text(encoding="utf-8"))
            m = HEADING_RE.search(body)
            section.title = m.group(1) if m else section.title
        for path in sorted(proot.rglob("*.md")):
            inner = path.relative_to(proot)
            if any(part in SKIP_DIRS or part.startswith(".") for part in inner.parts[:-1]):
                continue
            rel = Path(PRIVATE_DIR) / inner  # display path; the file may live outside the repo
            try:
                # namespaced so a private note can never shadow a syllabus id
                nid = "moc:private" if inner.as_posix().lower() == "readme.md" else f"private:{inner.with_suffix('').as_posix().lower()}"
                add(load_note(root, rel, PRIVATE_DIR, source=path, nid=nid), section)
            except (VaultError, UnicodeDecodeError) as exc:
                errors.append(f"{rel}: {exc}")
        section.notes.sort(key=lambda n: (n.path.parent.as_posix(), n.order, n.id))
        sections.append(section)
        for note in section.notes:  # merge overlay cards into the topics they extend
            target = notes.get(note.extends) if note.extends else None
            if note.extends and (target is None or not target.trackable):
                errors.append(f"{note.path}: extends unknown topic {note.extends!r}")
            elif target is not None:
                target.cards.extend(note.cards)
    return Vault(root, sections, notes, cards, errors)
