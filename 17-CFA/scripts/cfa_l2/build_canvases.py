"""Generate dependency canvases from the Cross-links section of every LM note.

One canvas per topic plus a master canvas. Edge labels come from the text after the link on each Cross-links line,
for example "- [[LM02-...]]: spot rates feed the binomial tree".
"""
from __future__ import annotations

import json
import re
import sys

from cfa_common import L2, TOPICS, VAULT, read_frontmatter

L2_REL = L2.relative_to(VAULT).as_posix()  # canvas file paths are vault-root relative
LINK = re.compile(r"^\s*-\s*\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]\s*:?\s*(.*)$")


def section(body: str, name: str) -> str:
    m = re.search(rf"^## {re.escape(name)}\s*$(.*?)(?=^## |\Z)", body, re.S | re.M)
    return m.group(1) if m else ""


def main() -> int:
    out = L2 / "50-Canvases"
    out.mkdir(exist_ok=True)
    notes = {}
    for code, slug, vol, name, weight in TOPICS:
        for note in sorted((L2 / slug).glob("LM*.md")):
            fm, body = read_frontmatter(note)
            edges = []
            for line in section(body, "Cross-links").splitlines():
                m = LINK.match(line)
                if m:
                    edges.append((m.group(1).split("/")[-1], m.group(2).strip()))
            notes[note.stem] = {"path": f"{L2_REL}/{slug}/{note.name}", "topic": code, "edges": edges}
    master_nodes, master_edges = [], []
    for code, slug, vol, name, weight in TOPICS:
        mine = [k for k, v in notes.items() if v["topic"] == code]
        if not mine:
            continue
        nodes, edges = [], []
        for i, k in enumerate(mine):
            nodes.append({"id": k, "type": "file", "file": notes[k]["path"], "x": (i % 4) * 460, "y": (i // 4) * 260, "width": 400, "height": 200})
        extern = set()
        for k in mine:
            for target, label in notes[k]["edges"]:
                if target not in notes:
                    continue
                if target not in mine and target not in extern:
                    extern.add(target)
                    nodes.append({"id": target, "type": "file", "file": notes[target]["path"], "x": 2000, "y": len(extern) * 260, "width": 400, "height": 200, "color": "4"})
                edges.append({"id": f"{k}->{target}", "fromNode": k, "toNode": target, "fromSide": "right", "toSide": "left", "label": label[:80]})
        (out / f"{slug}.canvas").write_text(json.dumps({"nodes": nodes, "edges": edges}, indent=1))
        master_nodes.append({"id": slug, "type": "file", "file": f"{L2_REL}/50-Canvases/{slug}.canvas", "x": (int(code) - 1) % 5 * 460, "y": (int(code) - 1) // 5 * 300, "width": 400, "height": 240})
    seen = set()
    for k, v in notes.items():
        for target, label in v["edges"]:
            if target in notes and notes[target]["topic"] != v["topic"]:
                a, b = TOPICS[int(v["topic"]) - 1][1], TOPICS[int(notes[target]["topic"]) - 1][1]
                if (a, b) not in seen:
                    seen.add((a, b))
                    master_edges.append({"id": f"{a}->{b}", "fromNode": a, "toNode": b, "fromSide": "bottom", "toSide": "top"})
    (out / "CFA-L2-Master.canvas").write_text(json.dumps({"nodes": master_nodes, "edges": master_edges}, indent=1))
    print(f"canvases: {len(master_nodes)} topic canvases, {sum(len(v['edges']) for v in notes.values())} edges, {len(master_edges)} cross-topic edges")
    return 0


if __name__ == "__main__":
    sys.exit(main())
