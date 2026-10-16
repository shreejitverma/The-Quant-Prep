"""Run every runnable Python example in the syllabus and fail if any of them fails.

An example is a ``.py`` file under ``NN-Section/code/`` of a curriculum section (library sections
with ``curriculum: false`` are skipped) that has an ``if __name__ == "__main__":`` guard.
Every example must run cleanly; examples that assert their numbers also fail when a note's numbers drift.
Examples run with ``MPLBACKEND=Agg`` unless the caller sets it, so plots never open a window.
A file opts out with a line ``# qp-examples: skip <reason>``; the reason is printed.

Usage: python tools/run_examples.py [--list] [--timeout SECONDS] [paths ...]
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from tools.qp.vault import SECTION_RE, section_info  # noqa: E402

MAIN_GUARD = re.compile(r"""^if __name__ == ["']__main__["']:""", re.MULTILINE)
SKIP_MARK = re.compile(r"^# qp-examples: skip (.+)$", re.MULTILINE)


@dataclass(frozen=True)
class Example:
    path: Path  # relative to the repo root
    skip: str | None  # reason, when the file opts out


def discover(root: Path) -> list[Example]:
    found = []
    for section in sorted(p for p in root.iterdir() if p.is_dir() and SECTION_RE.match(p.name)):
        if section_info(root, section.name)[1]:
            continue
        code = section / "code"
        if not code.is_dir():
            continue
        for path in sorted(code.rglob("*.py")):
            if "__pycache__" in path.parts:
                continue
            text = path.read_text(encoding="utf-8")
            if not MAIN_GUARD.search(text):
                continue
            skip = SKIP_MARK.search(text)
            found.append(Example(path.relative_to(root), skip.group(1).strip() if skip else None))
    return found


def run(root: Path, examples: list[Example], timeout: float) -> list[tuple[Example, str]]:
    """Run each example from the repo root; return (example, failure detail) for the failures."""
    failures = []
    env = {**os.environ, "MPLBACKEND": os.environ.get("MPLBACKEND", "Agg")}
    for ex in examples:
        if ex.skip:
            print(f"skip  {ex.path}  ({ex.skip})")
            continue
        start = time.monotonic()
        try:
            proc = subprocess.run(
                [sys.executable, str(ex.path)], cwd=root, env=env, capture_output=True, text=True, timeout=timeout, check=False
            )
        except subprocess.TimeoutExpired:
            failures.append((ex, f"timed out after {timeout:g}s"))
            print(f"FAIL  {ex.path}  (timeout)")
            continue
        took = time.monotonic() - start
        if proc.returncode == 0:
            print(f"ok    {ex.path}  {took:.1f}s")
        else:
            tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-20:])
            failures.append((ex, f"exit {proc.returncode}\n{tail}"))
            print(f"FAIL  {ex.path}  exit {proc.returncode}")
    return failures


def selects(arg: str, path: Path) -> bool:
    """True if ``arg`` names the example ``path`` or a directory containing it."""
    arg = arg.removeprefix("./").rstrip("/")
    rel = path.as_posix()
    return rel == arg or rel.startswith(arg + "/")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--list", action="store_true", help="list discovered examples and exit")
    ap.add_argument("--timeout", type=float, default=600.0, help="per-example timeout in seconds")
    ap.add_argument("--root", type=Path, default=REPO_ROOT, help=argparse.SUPPRESS)
    ap.add_argument("paths", nargs="*", help="only run these examples, or the examples under these directories")
    args = ap.parse_args(argv)
    root = args.root.resolve()
    examples = discover(root)
    if args.paths:
        examples = [e for e in examples if any(selects(p, e.path) for p in args.paths)]
    if args.list:
        for e in examples:
            print(f"{e.path}" + (f"  (skip: {e.skip})" if e.skip else ""))
        print(f"{len(examples)} example(s)")
        return 0
    if not examples:
        print("0 examples found")
        return 1
    failures = run(root, examples, args.timeout)
    for ex, detail in failures:
        print(f"\n--- {ex.path}: {detail}")
    ran = sum(1 for e in examples if not e.skip)
    print(f"\nexamples: {ran - len(failures)} passed, {len(failures)} failed, {len(examples) - ran} skipped")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
