"""Build one formula-drill Slides deck per topic from the formula blocks in the LM notes.

Each formula becomes two slides: the prompt (name and variables to recall) and the answer (the embedded block).
Open a deck with the core Slides plugin (command: Start presentation).
"""

from __future__ import annotations

import re
import sys

from cfa_common import L2, TOPICS, read_frontmatter

BLOCK = re.compile(r"\*\*(?P<name>[^*]+)\*\*\s*\((?P<cite>V\d+ p\.[^)]*)\)\s*\n\$\$(?P<math>.*?)\$\$\s*\n\^(?P<id>f-\d{2}-\d{2}-\d+)", re.S)
MATH_ID = re.compile(r"\$\$\s*\n\^(f-\d{2}-\d{2}-\d+)")


def main() -> int:
    out = L2 / "70-Slides"
    out.mkdir(exist_ok=True)
    total, unmatched = 0, []
    for code, slug, _vol, name, _weight in TOPICS:
        slides = [
            "---",
            "type: cfa-slides",
            f'topic_code: "{code}"',
            "tags: [cfa/l2, cfa/slides]",
            "generated: true",
            "---",
            f"# {name}: formula drill",
            "",
            "Say the formula, the variables, and the keystrokes before advancing.",
            "",
        ]
        n = 0
        for note in sorted((L2 / slug).glob("LM*.md")):
            fm, body = read_frontmatter(note)
            matched = set()
            for m in BLOCK.finditer(body):
                n += 1
                matched.add(m.group("id"))
                slides += [
                    "---",
                    "",
                    f"## {m.group('name')}",
                    "",
                    f"LM{fm.get('lm')}: {fm.get('title')}",
                    "",
                    "Write it, then advance.",
                    "",
                    "---",
                    "",
                    f"## {m.group('name')} ({m.group('cite')})",
                    "",
                    f"![[{note.stem}#^{m.group('id')}]]",
                    "",
                ]
            unmatched += [f"{note.stem}: ^{i}" for i in MATH_ID.findall(body) if i not in matched]
        if n:
            (out / f"{slug}-Formula-Drill.md").write_text("\n".join(slides) + "\n")
        total += n
    print(f"slides: {total} formulas across {len(list(out.glob('*.md')))} decks")
    for u in unmatched:
        print(f"WARN math block without a slide (header must be **Name** (V<n> p.<n>[, p.<n>]) directly above $$): {u}")
    if unmatched:
        print(f"slides: {len(unmatched)} math blocks not embedded")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
