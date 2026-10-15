"""List learning modules that still need an LM note, with everything an authoring agent needs.

Usage: python3 17-CFA/scripts/cfa_l2/notes_todo.py [--json] [--topic 03]
Prints, per missing module: topic, code, lm, title, note name, output path, module txt/json paths, chars,
printed page range, page offset, LOS IDs, and the note names of the other modules in the topic for cross-links.
"""
from __future__ import annotations

import json
import sys

from cfa_common import BUILD, L2, VAULT, TOPICS, lm_note_name, load_manifest, read_frontmatter
from verify_notes import resolve_private, sections_of, thin_sections


def incomplete(path) -> bool:
    """True when the note exists but is missing or too thin in any required section (an interrupted agent)."""
    _, body = read_frontmatter(path)
    secs = sections_of(body)
    return resolve_private(secs) is not None or bool(thin_sections(secs))


def main() -> int:
    as_json = "--json" in sys.argv
    topic_filter = sys.argv[sys.argv.index("--topic") + 1] if "--topic" in sys.argv else None
    man = load_manifest()
    todo = []
    for t in man["topics"]:
        if topic_filter and t["code"] != topic_filter:
            continue
        names = {m["lm"]: lm_note_name(t["code"], m["lm"], m["title"]) for m in t["modules"]}
        for m in t["modules"]:
            name = names[m["lm"]]
            path = L2 / t["slug"] / f"{name}.md"
            if path.exists() and not incomplete(path):
                continue
            status = "incomplete" if path.exists() else "missing"
            d = json.loads((BUILD / t["slug"] / f"LM{m['lm']:02d}.json").read_text())
            todo.append({
                "topic": t["name"], "code": t["code"], "slug": t["slug"], "volume": t["volume"], "weight": t["weight"],
                "lm": m["lm"], "title": m["title"], "note": name, "status": status, "output": str(path.relative_to(VAULT)),
                "txt": f"build/cfa_l2/{t['slug']}/LM{m['lm']:02d}.txt", "json": f"build/cfa_l2/{t['slug']}/LM{m['lm']:02d}.json",
                "chars": m["chars"], "printed_pages": f"{m['printed_pages'][0]}-{m['printed_pages'][1]-1}", "page_offset": m["page_offset"],
                "los": [f"los-{t['code']}-{m['lm']:02d}-{chr(97+i)}" for i in range(len(d["los"]))],
                "counts": {"los": len(d["los"]), "examples": len(d["examples"]), "problems": len(d["practice"]["problems"])},
                "siblings": [n for lm, n in names.items() if lm != m["lm"]],
            })
    if as_json:
        print(json.dumps(todo, indent=1))
    else:
        for x in todo:
            print(f"{x['code']}-{x['lm']:02d} {x['status']:<10} {x['chars']:>7} chars  LOS {x['counts']['los']:>2}  ex {x['counts']['examples']:>2}  pp {x['counts']['problems']:>2}  pp.{x['printed_pages']:<8} {x['note']}")
        print(f"\n{len(todo)} notes to write")
    return 0


if __name__ == "__main__":
    sys.exit(main())
