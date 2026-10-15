# The-Quant-Prep conventions

This repo is a public curriculum, an Obsidian vault, and the `qp` learning platform at once.
Everything committed here is public.

## Layout

- `00-Start-Here/` guides; `01-` to `15-` the syllabus; `16-Trading-and-Investing/` and `17-CFA/` free-form Obsidian libraries (`curriculum: false`, not validated by `qp`).
- `17-CFA/` is the CFA Level II platform: notes are governed by `17-CFA/scripts/cfa_l2/NOTE_SPEC.md`, `ITEMSET_SPEC.md` and `MOCK_SPEC.md`, progress lives in `17-CFA/CFA-L-2/00-Strategy/Build-Checklist.md`, and `verify_notes.py` and `verify_practice.py` there must pass before shipping anything under `17-CFA/CFA-L-2/`. They read the gitignored curriculum extracts, so run them from the main checkout, or from a worktree with `CFA_BUILD` and `CFA_PRIVATE` set to the main checkout's `build/cfa_l2` and `17-CFA/Private`; CI cannot run them.
- `tools/qp/` the platform: `vault.py` (parsing), `state.py` (progress, SM-2), `planner.py`, `drills.py`, `check.py`, `moc.py`, `cli.py`, `server.py`, `web/` (static app). Standard library only.
- `tools/obsidian/` plugin lock and bootstrap; `.obsidian/` shared settings only.
- `_archive/` pre-2026 material and superseded drafts; never edit, index or link it from the syllabus.

## Notes

- Follow `00-Start-Here/Note-Conventions.md`: frontmatter schema, required sections for `solid`, card callout format `> [!question]- <id> | <prompt>`, card id prefixes per section.
- Note id is the file name without its `NN-` prefix, lower-cased; `prereqs` and firm `focus` lists use ids.
- Frontmatter is flat; list items must not contain commas (the parser splits on them).
- Never change a published card id: learner history is keyed on it.
- Link notes with relative Markdown links; link SDE-Interview-Prep with absolute GitHub URLs.
- Every number in a note or card must be computed, not recalled.
- No emojis, no em dashes, one sentence per line.
- Firm guides: sourced facts only; keep `status: draft` until a human verifies.

## Private data

- `private/` is the gitignored private overlay (question banks, personal notes); `qp` loads it with ids namespaced `private:` and merges cards from notes with `extends: <topic>` into that topic. `./qp check` fails if anything under it is tracked. Never copy its content into public notes.
- Learner progress lives outside the repo (`$QP_HOME`, default `~/.local/share/quant-prep/`); never write it into the repo.
- `16-Trading-and-Investing/Private/` is gitignored except its README; personal trades and portfolios go only there.
- `17-CFA/Private/` is gitignored except its README: CFA Institute curriculum text, prep-provider slides and the official reference lists go only there, and the curriculum extracts stay in the ignored `build/cfa_l2/`. CFA attempt, error and weekly-review logs (`17-CFA/CFA-L-2/22-` to `24-`) are personal and ignored too. Public CFA notes and item sets may quote LOS statements and the CFA Institute Code of Ethics and Standards of Professional Conduct (which CFA Institute publishes freely), and may rework curriculum examples step by step, always with volume and page cites; restated end-of-module problems go only in `17-CFA/Private/CFA-L-2/Practice-Problems/`, embedded from the note's Practice problems section; never paste curriculum summaries, lists, problem sets or slides into a public note. Derived CFA progress (mastery, status and review dates in note frontmatter, and the study board) is published by the author's choice.

## Checks

Run before committing; CI (`.github/workflows/ci.yml`) and `.no-mistakes.yaml` run the same:

```sh
./qp check              # add --strict-sde when ../SDE-Interview-Prep is cloned
./qp index              # regenerate section README tables after adding or renaming notes
python3 -m unittest discover -s tools/tests -t .
tools/scan-secrets.sh   # secrets in the branch's commits vs origin/main; rules in .gitleaks.toml
ruff check . && ruff format --check .
```

C++ examples in `12-Quant-Development/code/cpp` must build with `-std=c++20 -Wall -Wextra -Wpedantic -Werror` on GCC and Clang and run clean under ASan/UBSan (TSan for the concurrent ones).
Their unit tests live in `12-Quant-Development/code/cpp/tests/test_*.cpp` (framework-free, exit non-zero on failure) and CI runs each one warning-free and under ASan/UBSan.
Changes reach GitHub only through the `no-mistakes` pipeline.
