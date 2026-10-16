"""Shared constants and helpers for the CFA Level II platform scripts.

Run every script from the repository root: python3 17-CFA/scripts/cfa_l2/<script>.py
"""

from __future__ import annotations

import json
import os
import re
from pathlib import Path

VAULT = Path(os.environ.get("CFA_VAULT", Path(__file__).resolve().parents[3]))
# Copyrighted inputs never enter git: the curriculum extracts (build/ is ignored) and the private overlay
# (17-CFA/Private/ is ignored). CFA_BUILD and CFA_PRIVATE let a worktree verify its own notes against the
# main checkout's copies without moving L2.
BUILD = Path(os.environ.get("CFA_BUILD", VAULT / "build" / "cfa_l2"))
PRIVATE = Path(os.environ.get("CFA_PRIVATE", VAULT / "17-CFA" / "Private"))
PDF_DIR = Path(os.environ.get("CFA_PDF_DIR", PRIVATE / "Curriculum-PDF"))
L2 = VAULT / "17-CFA" / "CFA-L-2"
# Each LM note's Practice problems section embeds <note>-Practice-Problems from here (restated curriculum problems).
PRACTICE_PRIVATE = PRIVATE / "CFA-L-2" / "Practice-Problems"

EXAM_DATE = "2026-11-24"

# code, folder slug, volume number, display name, official weight band (CFA Institute, fetched 2026-08-26)
TOPICS = [
    ("01", "01-Quantitative-Methods", 1, "Quantitative Methods", "5-10%"),
    ("02", "02-Economics", 2, "Economics", "5-10%"),
    ("03", "03-Financial-Statement-Analysis", 3, "Financial Statement Analysis", "10-15%"),
    ("04", "04-Corporate-Issuers", 4, "Corporate Issuers", "5-10%"),
    ("05", "05-Equity-Valuation", 5, "Equity Valuation", "10-15%"),
    ("06", "06-Fixed-Income", 6, "Fixed Income", "10-15%"),
    ("07", "07-Derivatives", 7, "Derivatives", "5-10%"),
    ("08", "08-Alternative-Investments", 8, "Alternative Investments", "5-10%"),
    ("09", "09-Portfolio-Management", 9, "Portfolio Management", "10-15%"),
    ("10", "10-Ethics", 10, "Ethical and Professional Standards", "10-15%"),
]
TOPIC_BY_CODE = {t[0]: t for t in TOPICS}
TOPIC_BY_VOLUME = {t[2]: t for t in TOPICS}

COMMAND_VERBS = [
    "analyze",
    "analyse",
    "apply",
    "assess",
    "calculate",
    "classify",
    "compare",
    "contrast",
    "critique",
    "define",
    "demonstrate",
    "describe",
    "determine",
    "discuss",
    "distinguish",
    "estimate",
    "evaluate",
    "explain",
    "formulate",
    "identify",
    "interpret",
    "judge",
    "justify",
    "list",
    "recommend",
    "select",
    "show",
    "summarize",
]

EMOJI_RE = re.compile("[\U0001f300-\U0001faff☀-➿⬀-⯿\U0001f000-\U0001f2ff]")
EM_DASH = "—"
F_ID = re.compile(r"\^(f-(\d{2})-(\d{2})-(\d+))\s*$", re.M)
FM_LINE = re.compile(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$")


def slugify(text: str) -> str:
    text = re.sub(r"[^A-Za-z0-9]+", "-", text).strip("-")
    return re.sub(r"-{2,}", "-", text)


def lm_note_name(code: str, lm: int, title: str) -> str:
    return f"LM{lm:02d}-{slugify(title)}"


def load_manifest() -> dict:
    """The extraction manifest; every script that needs the curriculum extracts starts here."""
    path = BUILD / "manifest.json"
    if not path.exists():
        raise SystemExit(
            f"curriculum extracts not found at {BUILD}: run extract.py then parse.py from the main checkout, "
            "or set CFA_BUILD (and CFA_PRIVATE) to the main checkout's build/cfa_l2 and 17-CFA/Private"
        )
    return json.loads(path.read_text())


def load_module(code: str, lm: int) -> dict:
    return json.loads((BUILD / TOPIC_BY_CODE[code][1] / f"LM{lm:02d}.json").read_text())


def read_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text()
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    fm: dict = {}
    for line in text[4:end].splitlines():
        m = FM_LINE.match(line)
        if m:
            fm[m.group(1)] = _parse_scalar(m.group(2))
    return fm, text[end + 5 :]


def _raw_frontmatter_lines(path: Path) -> list[str]:
    if not path.exists():
        return []
    text = path.read_text()
    if not text.startswith("---\n"):
        return []
    end = text.find("\n---\n", 4)
    return text[4:end].splitlines() if end >= 0 else []


def _parse_scalar(v: str):
    v = v.strip()
    if v.startswith("[") and v.endswith("]"):
        return [x.strip().strip('"').strip("'") for x in v[1:-1].split(",") if x.strip()]
    if v.startswith('"') and v.endswith('"'):
        return v[1:-1]
    if re.fullmatch(r"-?\d+", v):
        return int(v)
    if re.fullmatch(r"-?\d+\.\d+", v):
        return float(v)
    if v in ("true", "false"):
        return v == "true"
    return v


def _format_scalar(k: str, v) -> str:
    if isinstance(v, list):
        return f"{k}: [{', '.join(str(x) for x in v)}]"
    if isinstance(v, bool):
        return f"{k}: {'true' if v else 'false'}"
    if isinstance(v, str) and (":" in v or v == "" or v.startswith("[") or "#" in v or '"' in v):
        escaped = v.replace('"', '\\"')
        return f'{k}: "{escaped}"'
    return f"{k}: {v}"


def write_frontmatter(path: Path, fm: dict, body: str) -> None:
    """Write fm and body to path, keeping every existing frontmatter line whose value is unchanged byte-identical.

    Only keys whose parsed value differs from the file's current value are re-serialized, so quoted strings such as
    topic_code: "01" survive a round trip through read_frontmatter even though the parser returns a plain "01".
    """
    lines = ["---"]
    seen: set[str] = set()
    for raw in _raw_frontmatter_lines(path):
        m = FM_LINE.match(raw)
        if not m:
            lines.append(raw)
            continue
        k = m.group(1)
        if k not in fm or k in seen:
            continue
        seen.add(k)
        lines.append(raw if _parse_scalar(m.group(2)) == fm[k] else _format_scalar(k, fm[k]))
    for k, v in fm.items():
        if k not in seen:
            lines.append(_format_scalar(k, v))
    lines.append("---")
    path.write_text("\n".join(lines) + "\n" + body)
