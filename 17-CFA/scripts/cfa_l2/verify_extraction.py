"""Gate for the extraction layer: every module must have LOS, examples, and practice problems with solutions."""
from __future__ import annotations

import json
import sys

from cfa_common import BUILD, load_manifest


def main() -> int:
    manifest = load_manifest()
    total, ok, failures = 0, 0, []
    print(f"{'code':>4} {'lm':>2} {'LOS':>3} {'ex':>3} {'pp':>3} {'sol':>3} {'eq':>4} {'review':>6}  status")
    for topic in manifest["topics"]:
        for module in topic["modules"]:
            total += 1
            d = json.loads((BUILD / topic["slug"] / f"LM{module['lm']:02d}.json").read_text())
            n_los, n_ex = len(d["los"]), len(d["examples"])
            n_pp, n_sol = len(d["practice"]["problems"]), len(d["practice"]["solutions"])
            problems, notes = [], []
            n_kc = sum(1 for e in d["examples"] if e.get("kind") == "knowledge_check")
            if n_los == 0:
                problems.append("no LOS")
            if n_ex == 0:
                notes.append("curriculum has no examples or knowledge checks")
            if n_pp == 0 and n_kc == 0:
                problems.append("no practice problems")
            elif n_pp == 0:
                notes.append(f"no EOC set; {n_kc} knowledge checks with solutions serve as practice")
            if n_pp and n_sol == 0:
                problems.append("no solutions")
            if n_pp != n_sol:
                problems.append(f"problems {n_pp} != solutions {n_sol}")
            status = ("OK" if not problems else "FAIL: " + "; ".join(problems)) + (" (" + "; ".join(notes) + ")" if notes else "")
            if not problems:
                ok += 1
            else:
                failures.append((topic["code"], module["lm"], status))
            print(f"{topic['code']:>4} {module['lm']:>2} {n_los:>3} {n_ex:>3} {n_pp:>3} {n_sol:>3} {len(d['equations']):>4} {d['needs_review_count']:>6}  {status}")
    print(f"\ncoverage: {ok}/{total} modules pass")
    return 0 if ok == total else 1


if __name__ == "__main__":
    sys.exit(main())
