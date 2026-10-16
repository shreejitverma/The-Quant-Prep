"""Split each curriculum volume into learning-module text files.

Output: build/cfa_l2/<topic-slug>/LM<nn>.txt and build/cfa_l2/manifest.json
Pages are separated by form feeds in the .txt so downstream parsers can cite printed pages.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys

from cfa_common import BUILD, PDF_DIR, TOPICS

LM_HEADER = re.compile(r"LEARNING\s+MODULE\s+(\d+)\s+(.+?)(?:\s+by\s|\s+LEARNING OUTCOMES|\s{3,})", re.S)
PRINTED_PAGE = re.compile(r"^\s*(?:[A-Za-z][^\n]{0,80}?\s{2,})?(\d{1,3})\s*$|^\s*(\d{1,3})\s{2,}[A-Z][^\n]{0,80}$", re.M)


def pdftotext(pdf) -> list[str]:
    out = subprocess.run(["pdftotext", "-layout", str(pdf), "-"], capture_output=True, text=True, check=True).stdout
    return out.split("\f")


def find_offset(pages: list[str], lm_start_idx: int) -> int:
    """Return pdf_page - printed_page using running headers on the pages after the module start."""
    votes: dict[int, int] = {}
    for i in range(lm_start_idx + 1, min(lm_start_idx + 12, len(pages))):
        first = pages[i].strip().splitlines()[:1]
        if not first:
            continue
        line = first[0]
        m = re.match(r"^\s*(\d{1,3})\s{2,}\S", line) or re.match(r"^.*\S\s{2,}(\d{1,3})\s*$", line)
        if m:
            printed = int(m.group(1))
            votes[(i + 1) - printed] = votes.get((i + 1) - printed, 0) + 1
    return max(votes, key=votes.get) if votes else 0


def main() -> int:
    BUILD.mkdir(parents=True, exist_ok=True)
    manifest = {"topics": []}
    for code, slug, vol, name, weight in TOPICS:
        pdf = PDF_DIR / f"cfa-program2026L2V{vol}.pdf"
        pages = pdftotext(pdf)
        starts = []
        for i, p in enumerate(pages):
            head = p[:600]
            m = LM_HEADER.search(head)
            if m and "LEARNING OUTCOMES" in p[:3000] or (m and i < 3):
                title = re.sub(r"\s+", " ", m.group(2)).strip()
                starts.append((i, int(m.group(1)), title))
        # dedupe consecutive detections of the same module number
        modules = []
        for i, n, title in starts:
            if modules and modules[-1][1] == n:
                continue
            modules.append((i, n, title))
        (BUILD / slug).mkdir(exist_ok=True)
        entries = []
        for k, (i, n, title) in enumerate(modules):
            end = modules[k + 1][0] if k + 1 < len(modules) else len(pages)
            offset = find_offset(pages, i)
            text = "\f".join(pages[i:end])
            (BUILD / slug / f"LM{n:02d}.txt").write_text(text)
            entries.append(
                {
                    "lm": n,
                    "title": title,
                    "pdf_pages": [i + 1, end],
                    "printed_pages": [i + 1 - offset, end - offset],
                    "page_offset": offset,
                    "chars": len(text),
                }
            )
            print(f"V{vol} LM{n} {title!r}: pdf {i + 1}-{end}, printed {i + 1 - offset}-{end - offset}, {len(text)} chars")
        manifest["topics"].append(
            {
                "code": code,
                "slug": slug,
                "volume": vol,
                "name": name,
                "weight": weight,
                "pdf": pdf.name,
                "pages": len(pages),
                "modules": entries,
            }
        )
    (BUILD / "manifest.json").write_text(json.dumps(manifest, indent=2))
    total = sum(len(t["modules"]) for t in manifest["topics"])
    print(f"\nmodules found: {total}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
