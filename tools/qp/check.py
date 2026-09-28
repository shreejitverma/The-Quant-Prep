"""Content validation: schema, prerequisites, cards, links and style.

``qp check`` is the CI gate for the curriculum. Every rule is here so authors and
agents get the same answer locally and in CI.
"""

from __future__ import annotations

import os
import re
import subprocess
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import unquote

from .vault import NOTE_TYPES, PRIVATE_DIR, STATUSES, TIERS, TRACKS, Vault

SDE_URL = "https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/"
SDE_ENV = "SDE_REPO"
LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
EMOJI_RE = re.compile("[\U0001f300-\U0001faff\U00002700-\U000027bf\U0001f000-\U0001f2ff\U00002600-\U000026ff]")
EM_DASH = "—"
SOLID_SECTIONS = ("TL;DR", "Learning objectives", "Core concepts", "Worked examples", "Pitfalls", "Interview questions", "Further reading")
MIN_CARDS = {"concept": 6, "problem-set": 15, "playbook": 3}
REQUIRED = ("type", "track", "tier", "status")


@dataclass(frozen=True)
class Finding:
    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.rule}] {self.message}"


def sde_root(root: Path) -> Path | None:
    env = os.environ.get(SDE_ENV)
    candidate = Path(env).expanduser() if env else root.parent / "SDE-Interview-Prep"
    return candidate if (candidate / ".git").exists() or (candidate / "README.md").exists() else None


def strip_code(text: str) -> str:
    """Blank out fenced and inline code, keeping line numbers stable."""
    text = FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE_RE.sub("``", text)


def line_of(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def check_links(path: Path, source: Path, text: str, sde: Path | None) -> list[Finding]:
    out = []
    clean = strip_code(text)
    for m in LINK_RE.finditer(clean):
        target = m.group(1)
        line = line_of(clean, m.start())
        if target.startswith(SDE_URL):
            if sde is None:
                continue  # SDE clone absent (e.g. CI); qp check --strict-sde turns this into an error
            rel = unquote(target[len(SDE_URL) :].split("#", 1)[0])
            if not (sde / rel).exists():
                out.append(Finding(str(path), line, "sde-link", f"SDE-Interview-Prep has no {rel}"))
            continue
        if re.match(r"^[a-z]+:", target) or target.startswith("#"):
            continue
        rel = unquote(target.split("#", 1)[0])
        if not rel:
            continue
        resolved = (source.parent / rel).resolve()
        if not resolved.exists():
            out.append(Finding(str(path), line, "link", f"broken relative link {target}"))
    return out


def check_style(path: Path, text: str) -> list[Finding]:
    out = []
    for i, line in enumerate(text.splitlines(), 1):
        if EM_DASH in line:
            out.append(Finding(str(path), i, "style", "em dash; use a plain '-'"))
        if EMOJI_RE.search(line):
            out.append(Finding(str(path), i, "style", "emoji"))
    return out


def check_vault(vault: Vault, strict_sde: bool = False, files: list[Path] | None = None) -> list[Finding]:
    findings = [Finding(e.split(":", 1)[0], 1, "parse", e.split(": ", 1)[-1]) for e in vault.errors]
    sde = sde_root(vault.root)
    if strict_sde and sde is None:
        findings.append(Finding(".", 1, "sde-link", f"SDE-Interview-Prep clone not found; set {SDE_ENV}"))
    for note in vault.notes.values():
        if note.id.startswith("moc:"):
            continue
        p = str(note.path)
        missing = [k for k in REQUIRED if not note.meta.get(k)]
        if missing:
            findings.append(Finding(p, 1, "schema", f"missing frontmatter: {', '.join(missing)}"))
            continue
        if note.type not in NOTE_TYPES:
            findings.append(Finding(p, 1, "schema", f"type {note.type!r} not in {NOTE_TYPES}"))
        bad = [t for t in note.tracks if t not in TRACKS]
        if bad:
            findings.append(Finding(p, 1, "schema", f"unknown track(s) {bad}"))
        if note.tier not in TIERS:
            findings.append(Finding(p, 1, "schema", f"tier {note.tier!r} not in {TIERS}"))
        if note.status not in STATUSES:
            findings.append(Finding(p, 1, "schema", f"status {note.status!r} not in {STATUSES}"))
        for pre in note.prereqs:
            if pre not in vault.notes:
                findings.append(Finding(p, 1, "prereq", f"unknown prerequisite {pre!r}"))
        if note.trackable and not note.est_hours:
            findings.append(Finding(p, 1, "schema", "trackable note needs est_hours"))
        if note.type == "firm":
            for f in note.meta.get("focus") or []:
                if f not in vault.notes:
                    findings.append(Finding(p, 1, "prereq", f"unknown focus topic {f!r}"))
        if note.status in ("solid", "canonical") and note.trackable:
            headings = {h.strip().lower() for h in re.findall(r"^##\s+(.+)$", note.body, re.MULTILINE)}
            for want in SOLID_SECTIONS:
                if want.lower() not in headings:
                    findings.append(Finding(p, 1, "solid", f"status {note.status} needs a '## {want}' section"))
            need = MIN_CARDS.get(note.type, 0)
            if len(note.cards) < need:
                findings.append(Finding(p, 1, "solid", f"status {note.status} needs at least {need} cards, has {len(note.cards)}"))
        for card in note.cards:
            if not card.answer:
                findings.append(Finding(p, card.line, "card", f"card {card.id!r} has no answer"))
    findings += prereq_cycles(vault)
    findings += private_not_tracked(vault)
    targets = (
        files
        if files is not None
        else sorted({n.path for n in vault.notes.values()} | {Path(x) for x in ("README.md",) if (vault.root / x).exists()})
    )
    sources = {n.path: n.source for n in vault.notes.values()}
    for rel in targets:
        source = sources.get(rel, vault.root / rel)
        text = source.read_text(encoding="utf-8")
        findings += check_links(rel, source, text, sde)
        findings += check_style(rel, text)
    return sorted(findings, key=lambda f: (f.path, f.line, f.rule))


def private_not_tracked(vault: Vault) -> list[Finding]:
    """The private overlay must never be committed: fail if git tracks anything under it."""
    if not (vault.root / ".git").exists():
        return []
    try:
        out = subprocess.run(["git", "ls-files", "--", PRIVATE_DIR], cwd=vault.root, capture_output=True, text=True, check=True).stdout
    except (OSError, subprocess.CalledProcessError) as exc:
        return [Finding(PRIVATE_DIR, 1, "private", f"could not verify the private overlay is untracked: {exc}")]
    return [Finding(line, 1, "private", "private overlay file is tracked by git; run git rm --cached") for line in out.splitlines()]


def prereq_cycles(vault: Vault) -> list[Finding]:
    WHITE, GREY, BLACK = 0, 1, 2
    color = {i: WHITE for i in vault.notes}
    out: list[Finding] = []

    def visit(nid: str, trail: list[str]) -> None:
        color[nid] = GREY
        for p in vault.notes[nid].prereqs:
            if p not in vault.notes:
                continue
            if color[p] == GREY:
                cyc = trail[trail.index(p) :] + [p] if p in trail else [nid, p]
                out.append(Finding(str(vault.notes[nid].path), 1, "prereq", "prerequisite cycle: " + " -> ".join(cyc)))
            elif color[p] == WHITE:
                visit(p, trail + [p])
        color[nid] = BLACK

    for nid in vault.notes:
        if color[nid] == WHITE:
            visit(nid, [nid])
    return out
