# Contributing to The Quant Prep

Contributions that make a note more correct, clearer, or more complete are the most valuable ones.
The seed notes (status `seed` in `./qp syllabus`) are the writing backlog.

## Workflow

1. Fork and clone; create a branch.
2. Write or fix notes following [Note Conventions](00-Start-Here/Note-Conventions.md).
3. Run the checks below and fix everything they report.
4. Open a pull request describing what changed and how you verified any numbers.

```sh
./qp check                                        # schema, prerequisites, cards, links, style
./qp index                                        # regenerate section README tables
python3 -m unittest discover -s tools/tests -t .  # platform tests
tools/scan-secrets.sh                             # secrets in your commits vs origin/main
ruff check . && ruff format --check .             # Python lint and format
```

The secret scan checks only the commits your branch adds, which keeps it fast.
It includes what a merge commit adds beyond git's automatic merge, such as a conflict resolution, so a secret cannot slip in through a merge.
For an audit of the whole tree, run `gitleaks dir . --no-banner --redact` (several minutes, because `_archive/` is large).
Reviewed findings that are not credentials are listed in `.gitleaksignore`; add one only after confirming the value is not a secret.

## Standards

- **Correctness first.** Every number in a note or card is computed, not remembered; say how you checked it in the pull request.
- **No emojis and no em dashes** anywhere, including code comments and commit messages; use a plain `-`.
- **One sentence per line** in Markdown prose.
- **File names.** Notes use `NN-Title-Case-With-Hyphens.md` so they sort in study order; code uses `snake_case`.
- **Python:** type hints where they clarify, ruff-clean, seeded randomness in examples, no work at import time.
- **C++:** C++20, RAII and clear ownership, no undefined behaviour; examples must build warning-free with `-Wall -Wextra -Wpedantic` on GCC and Clang.
- **Firm guides:** only sourced facts, with sources listed; mark anything reported but unverified.
- **Third-party material:** link to it; do not copy book text, paid course material or other people's notebooks into the syllabus.

## Code of conduct

Be respectful and constructive. This is a learning community.
