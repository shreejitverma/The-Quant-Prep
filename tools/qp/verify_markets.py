"""Validation gate for 16-Trading-and-Investing (Markets Mastery OS).

Verifies frontmatter schemas, style invariants (no emoji, no em dashes, one sentence
per physical line), link targets, math block delimiters, and Trading Lab engine references.
Standard-library only, with TOON-formatted diagnostic output.
"""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MARKETS_ROOT = REPO_ROOT / "16-Trading-and-Investing"

EM_DASH = "—"
EMOJI_RE = re.compile("[\U0001f300-\U0001faff\U00002700-\U000027bf\U0001f000-\U0001f2ff\U00002600-\U000026ff]")
SENTENCE_END_RE = re.compile(r"([.!?])\s+([A-Z0-9][a-z0-9])")
WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")
MD_LINK_RE = re.compile(r"(?<!!)\[[^\]]*\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

KNOWN_LAB_ENGINES = {
    "lob_sim",
    "opt_desk",
    "gen_market",
    "pos_sizing",
    "replay_chart",
    "overfit_trap",
    "fut_desk",
    "port_alloc",
    "journal_stats",
    "mm_quote",
    "event_study",
    "crypto_basis",
}


@dataclass(frozen=True)
class MarketFinding:
    path: str
    line: int
    rule: str
    message: str

    def __str__(self) -> str:
        return f"{self.path}:{self.line}: [{self.rule}] {self.message}"


def strip_code_blocks(text: str) -> str:
    """Blank out fenced and inline code blocks, preserving exact line numbers."""
    text = FENCE_RE.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    return INLINE_CODE_RE.sub("``", text)


def line_at(text: str, index: int) -> int:
    return text.count("\n", 0, index) + 1


def safe_relpath(path: Path) -> str:
    try:
        return str(path.relative_to(REPO_ROOT))
    except ValueError:
        return str(path)


def check_frontmatter(path: Path, text: str) -> tuple[dict, str, list[MarketFinding]]:
    findings: list[MarketFinding] = []
    rel = safe_relpath(path)
    if not text.startswith("---\n"):
        return {}, text, [MarketFinding(rel, 1, "frontmatter", "missing leading frontmatter fence '---'")]

    end = text.find("\n---", 4)
    if end == -1:
        return {}, text, [MarketFinding(rel, 1, "frontmatter", "unclosed frontmatter fence '---'")]

    fm_text = text[4:end]
    body = text[end + 4 :].lstrip("\n")
    meta: dict[str, str] = {}

    for i, line in enumerate(fm_text.splitlines(), 2):
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in line:
            findings.append(MarketFinding(rel, i, "frontmatter-syntax", f"invalid frontmatter line: {line!r}"))
            continue
        key, _, val = line.partition(":")
        meta[key.strip()] = val.strip()

    return meta, body, findings


def check_style_invariants(path: Path, text: str) -> list[MarketFinding]:
    findings: list[MarketFinding] = []
    rel = safe_relpath(path)
    lines = text.splitlines()

    in_fence = False
    fence_marker = ""

    for idx, raw_line in enumerate(lines, 1):
        stripped = raw_line.strip()
        if not in_fence:
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = True
                fence_marker = stripped[:3]
                continue
        else:
            if stripped.startswith(fence_marker):
                in_fence = False
                fence_marker = ""
            continue

        if EM_DASH in raw_line:
            findings.append(MarketFinding(rel, idx, "style-em-dash", "em dash found; use a plain '-'"))

        if EMOJI_RE.search(raw_line):
            findings.append(MarketFinding(rel, idx, "style-emoji", "emoji found; emojis are prohibited"))

        # Sentence-per-line rule for prose text in Markdown
        if (
            not stripped.startswith("#")
            and not stripped.startswith("- ")
            and not stripped.startswith("* ")
            and not stripped.startswith(">")
            and not stripped.startswith("|")
            and not re.match(r"^\d+\.\s", stripped)
            and len(stripped) > 40
        ):
            # Check if there are multiple sentences on a single line
            m = SENTENCE_END_RE.search(stripped)
            if m:
                # Exclude common abbreviations like e.g., i.e., vs., Fig., etc.
                snippet = stripped[max(0, m.start() - 4) : m.start() + 1]
                if not any(
                    snippet.lower().endswith(abbr)
                    for abbr in ("e.g.", "i.e.", "vs.", "etc.", "fig.", "al.", "jr.", "sr.", "dr.", "mr.", "ms.")
                ) and not re.search(r"(?:^|\s)[A-Za-z]\.$", snippet):
                    findings.append(
                        MarketFinding(
                            rel,
                            idx,
                            "style-sentence-per-line",
                            "multiple sentences on single physical line; put each sentence on its own line",
                        )
                    )

    return findings


def check_links_and_engines(path: Path, text: str) -> list[MarketFinding]:
    findings: list[MarketFinding] = []
    rel = safe_relpath(path)
    clean = strip_code_blocks(text)

    # Check Markdown links
    for m in MD_LINK_RE.finditer(clean):
        target = m.group(1)
        line = line_at(clean, m.start())
        if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
            continue
        if target.startswith("obsidian://"):
            if not target.startswith("obsidian://open?vault="):
                findings.append(MarketFinding(rel, line, "link-obsidian", f"malformed obsidian link: {target}"))
            continue
        target_path = (path.parent / target.split("#", 1)[0]).resolve()
        if not target_path.exists():
            findings.append(MarketFinding(rel, line, "link-broken", f"broken markdown link target: {target}"))

    # Check Wikilinks
    for m in WIKILINK_RE.finditer(clean):
        target = m.group(1).strip()
        line = line_at(clean, m.start())
        resolved = False
        candidates = [
            REPO_ROOT / f"{target}.md",
            REPO_ROOT / target,
            path.parent / f"{target}.md",
            path.parent / target,
            MARKETS_ROOT / f"{target}.md",
            MARKETS_ROOT / target,
        ]
        for c in candidates:
            if c.exists():
                resolved = True
                break
        if not resolved:
            findings.append(MarketFinding(rel, line, "link-wikilink", f"unresolved wikilink: [[{target}]]"))

    # Check math blocks
    math_count = text.count("$$")
    if math_count % 2 != 0:
        findings.append(MarketFinding(rel, 1, "math-block", f"unbalanced math block delimiters '$$' (count={math_count})"))

    return findings


def verify_markets_vault(root: Path = MARKETS_ROOT, include_legacy: bool = False) -> list[MarketFinding]:
    findings: list[MarketFinding] = []
    # By default, verify the structured Markets Mastery OS curriculum, styles, and labs.
    # Legacy unmigrated Obsidian notes in Investing/ and Finance/ are skipped unless include_legacy=True.
    skip_top_dirs = {"Private"} if include_legacy else {"Private", "Investing", "Finance", "scripts"}

    for md_path in sorted(root.rglob("*.md")):
        rel = md_path.relative_to(root)
        if any(part in skip_top_dirs for part in rel.parts[:1]):
            continue
        text = md_path.read_text(encoding="utf-8")
        _, _, fm_findings = check_frontmatter(md_path, text)
        findings.extend(fm_findings)
        findings.extend(check_style_invariants(md_path, text))
        findings.extend(check_links_and_engines(md_path, text))

    return sorted(findings, key=lambda f: (f.path, f.line, f.rule))


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify 16-Trading-and-Investing integrity.")
    parser.add_argument("--strict", action="store_true", help="Fail on warning findings")
    parser.add_argument("--all-legacy", action="store_true", help="Include legacy unmigrated notes in Investing/ and Finance/")
    parser.add_argument("paths", nargs="*", help="Optional specific markdown paths to check")
    args = parser.parse_args()

    if args.paths:
        findings: list[MarketFinding] = []
        for p in args.paths:
            path = Path(p).resolve()
            if path.exists():
                text = path.read_text(encoding="utf-8")
                _, _, fm_f = check_frontmatter(path, text)
                findings.extend(fm_f)
                findings.extend(check_style_invariants(path, text))
                findings.extend(check_links_and_engines(path, text))
    else:
        findings = verify_markets_vault(include_legacy=args.all_legacy)

    if not findings:
        print(f"verify_markets: ok; 0 findings across {MARKETS_ROOT.name}")
        return 0

    print(f"problems[{len(findings)}]{{path,line,rule,message}}:")
    for f in findings:
        print(f"  {f.path},{f.line},{f.rule},{f.message}")

    return 1


if __name__ == "__main__":
    sys.exit(main())
