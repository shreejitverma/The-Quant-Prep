# The-Quant-Prep conventions

This repo is a public curriculum, an Obsidian vault, and the `qp` learning platform at once.
Everything committed here is public.

## Layout

- `00-Start-Here/` guides; `01-` to `15-` the syllabus; `16-Trading-and-Investing/` a free-form Obsidian library (`curriculum: false`, not validated by `qp`).
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
