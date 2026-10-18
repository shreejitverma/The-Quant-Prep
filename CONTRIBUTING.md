# Contributing to The Quant Prep

Thank you for helping.
The most valuable contribution is a correction: a wrong number in a public study guide misleads everyone who reads it.
After that come deeper explanations, better worked examples, sharper cards and platform improvements.

Everything here is public.
Read [How Notes Are Verified](00-Start-Here/How-Notes-Are-Verified.md) first: it is the standard every change is held to.

## Contents

- [Set up](#set-up)
- [Checks](#checks)
- [Write or fix a note](#write-or-fix-a-note)
- [Question cards](#question-cards)
- [Code examples](#code-examples)
- [Sources and facts](#sources-and-facts)
- [Before you open a pull request](#before-you-open-a-pull-request)
- [Private material](#private-material)
- [Platform changes](#platform-changes)
- [Style](#style)

## Set up

```sh
git clone https://github.com/shreejitverma/The-Quant-Prep.git
cd The-Quant-Prep
git clone https://github.com/shreejitverma/SDE-Interview-Prep.git ../SDE-Interview-Prep   # optional, for --strict-sde link checks
```

- **Platform:** Python 3.10 or later, standard library only; `./qp` runs straight from the checkout.
- **Examples:** numpy, pandas and matplotlib.
  Use `environment.yml` with conda, or run a script without installing anything: `uv run --no-project --with numpy --with pandas --with matplotlib python <file>.py`.
- **Lint:** [ruff](https://docs.astral.sh/ruff/), configured in `pyproject.toml`.
- **C++ examples:** GCC 13 or Clang 18 or later with C++20.
- **Secret scan:** [gitleaks](https://github.com/gitleaks/gitleaks) for `tools/scan-secrets.sh`.
- **Reading:** open the folder as an [Obsidian](https://obsidian.md) vault; `tools/obsidian/README.md` sets up the shared plugins.

Keep your own study progress out of the repo: it lives in `$QP_HOME` (default `~/.local/share/quant-prep/`).

## Checks

Run all of these before a pull request; CI runs the same on Linux.

```sh
./qp check                                        # schema, prerequisites, cards, links, style; add --strict-sde with SDE-Interview-Prep cloned
./qp index                                        # regenerate the README tables (section topic tables and the root catalog)
python3 -m unittest discover -s tools/tests -t .  # platform tests
ruff check . && ruff format --check .             # Python lint and format
python3 tools/run_examples.py                     # every Python example; asserted numbers fail on drift
tools/scan-secrets.sh                             # secrets in your branch's commits versus origin/main
python3 16-Trading-and-Investing/scripts/verify_markets.py   # extra rules for the Markets Mastery OS (section 16 changes)
```

`python3 tools/run_examples.py 06-Fixed-Income-and-Asset-Classes` runs one section; `--list` shows what would run.
The secret scan checks only the commits your branch adds, including what a merge commit adds beyond git's automatic merge.
For a whole-tree audit run `gitleaks dir . --no-banner --redact` (slow, because `_archive/` is large); reviewed non-secrets go in `.gitleaksignore`.

## Write or fix a note

The rules for files, frontmatter, sections and cards are in [Note Conventions](00-Start-Here/Note-Conventions.md); `./qp check` enforces the mechanical parts.
The workflow:

1. **Read before you write.** Read the note, its section README, its prerequisites, the notes that link to it, and the section's `code/` folder.
   Good models of the standard: [Expectation, Variance and Linearity](01-Probability/04-Expectation-Variance-and-Linearity.md), [Stochastic Differential Equations](04-Stochastic-Calculus/03-Stochastic-Differential-Equations.md) and [FRTB Sensitivities-Based Method: Delta](17-Regulatory-Capital-Basel-and-FRTB/07-FRTB-Sensitivities-Based-Method-Delta.md).
2. **Write the code first.** Put every computation the note will quote in a script in the section's `code/` folder (see [Code examples](#code-examples)).
3. **Write the note** in the required section order: TL;DR, Learning objectives, Core concepts, Worked examples, Pitfalls, Interview questions, then Further reading.
   Derive what interviewers ask you to derive, solve the examples the way you would say them out loud, and explain how practitioners use the idea.
   Add a Mermaid diagram wherever there is a flow, architecture, state machine or decision.
4. **Trace every number.** Go through the body, tables and card answers; each number must be printed and asserted by your script, a stated input, or a cited constant.
5. **Regenerate and check.** Run `./qp index`, then every command in [Checks](#checks).
6. **Set the status.** A note is `solid` only when every required section is present, it has enough cards, and step 4 passed; otherwise leave it `draft`.
   Never set `canonical`: that is reserved for human expert review.

Never rename a published note file casually: the note id comes from the file name, and prerequisites, firm focus lists and learner progress refer to it.
Never edit inside the `qp:moc` or `qp:catalog` markers by hand; `./qp index` owns those blocks.

## Question cards

```markdown
> [!question]- fi-swap-par-rate | What is the par rate of a swap, in one line?
> The fixed rate that makes the swap's value zero at inception: floating-leg PV divided by the fixed-leg annuity.
```

- **Ids are permanent.** Learner review history is keyed on the id, so never change or reuse one; you may always fix the answer.
- **Ids are unique and prefixed** with the section prefix from [Note Conventions](00-Start-Here/Note-Conventions.md#question-cards); check with `grep -rn "<id> |" --include=*.md .` before using one.
- **How many:** `./qp check` requires at least 6 cards on a `solid` concept note and 15 on a problem set; aim for 15 and 25, covering definitions, derivations, numerical problems, "what goes wrong if", design trade-offs and senior judgement.
- **Answer first,** then the shortest convincing argument.
- **Self-contained:** a card is shown alone during review, so it must make sense without the note around it, including the hardware or assumptions behind any measured figure.

## Code examples

### Python

`tools/run_examples.py` discovers and runs every `.py` file under a curriculum section's `code/` folder that has an `if __name__ == "__main__":` guard.

- **Print and assert** every number the notes quote, at the quoted rounding, against an independently computed value.
- **Name what you back:** put the note section or card id next to each assert block.
- **Be deterministic:** seed every random generator; never assert on wall-clock time.
- **Be platform-stable:** CI runs on Linux x86-64 with a different BLAS and libm from your laptop.
  Stop iterative solvers on a residual or step tolerance well above machine precision, never on an iteration count that depends on rounding noise.
  Before a pull request, run your section in a Linux container:
  `docker run --rm --platform linux/amd64 -v "$PWD":/repo:ro -w /tmp python:3.12 sh -c "cp -r /repo /tmp/r && cd /tmp/r && pip install -q numpy pandas matplotlib && MPLBACKEND=Agg python tools/run_examples.py <section>"`.
- **Be fast:** each example should finish in well under a minute.
- **Keep imports cheap:** no work at import time; type hints where they clarify; ruff-clean.
- **Opt out only with a reason:** a line `# qp-examples: skip <reason>` excludes a file (for example, one that needs a GPU), and the runner prints the reason.

### C++

C++ lives in `12-Quant-Development/code/cpp`, with framework-free unit tests in `tests/test_*.cpp` that exit non-zero on failure.
CI builds and runs every file with both `g++` and `clang++`:

```sh
# warning-free optimised build of every example and test
$CXX -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -pthread -I . -o /tmp/x file.cpp
# every example and test under AddressSanitizer and UndefinedBehaviorSanitizer
$CXX -std=c++20 -O1 -g -fsanitize=address,undefined -fno-sanitize-recover=all -fno-omit-frame-pointer -pthread -I . -o /tmp/x file.cpp && /tmp/x
# files that include <thread> also under ThreadSanitizer
$CXX -std=c++20 -O1 -g -fsanitize=thread -pthread -I . -o /tmp/x file.cpp && /tmp/x
```

- RAII and clear ownership; no raw `new` or `delete`; no undefined behaviour; be explicit about memory ordering in concurrent code.
- A file that must not be run starts with `// qp-examples: no-run (<reason>)`.
- To match CI exactly, build in an `ubuntu:24.04` container with its default `g++` and `clang` packages.

## Sources and facts

- **Never invent** an API, paper, statistic, rule number, incident, firm practice or URL.
- **Regulation:** quote the primary text with its paragraph (Basel Framework standards such as `MAR21.6`, `CRE52.39`); date-stamp implementation details ("as of 2026-10").
- **Papers and books:** authors, title, venue or edition, year, and chapter where you name one; attribute a result to the paper and table that contain it.
- **Firms and incidents:** only with a public primary or reputable source; firm guides stay `draft` until a human verifies them.
- **Market data:** label illustrative inputs as hypothetical; quote real levels only with a source and date.
- **Causal claims:** say a simulation "shows why" only if the script isolates that cause with a one-change control and asserts it; otherwise state what was measured.
- **When unsure, leave it out.**
- **Third-party material:** link to it; do not copy book text, paid course material or other people's notebooks.

## Before you open a pull request

- [ ] Every command in [Checks](#checks) passes, and your section's examples pass in the Linux container.
- [ ] Every number you added or changed is printed and asserted, a labelled input, or a cited constant.
- [ ] No assert compares a value with itself or with the same formula written twice.
- [ ] Every card's shown working reproduces its answer from the inputs it quotes.
- [ ] Every citation is real and says what you attribute to it.
- [ ] No card id was changed or reused, and no note file was renamed.
- [ ] Sign conventions are stated wherever they differ between instruments or quoting conventions.

In the pull request, say what changed, why, and how you verified each number and fact.

## Private material

- `private/` (or `$QP_PRIVATE`) is a gitignored overlay for question banks and personal notes; `./qp check` fails if anything in it is tracked.
  Never copy its content into a public note.
- `16-Trading-and-Investing/Private/` holds personal trades and portfolios and is gitignored except its README.
- `17-CFA/Private/` holds CFA Institute curriculum text and is gitignored except its README; public CFA notes follow the rules in [CLAUDE.md](CLAUDE.md#private-data).
- Learner progress lives outside the repo; never commit a `state.json`.

## Platform changes

The `qp` platform in `tools/qp/` uses the Python standard library only, so learners need no install step.
[The qp platform](tools/qp/README.md) documents its architecture, data model, HTTP API and extension points.

- Add or update a test in `tools/tests/` for every behaviour change; tests execute the public interface and assert observable results.
- Keep output AXI-style for agents: compact TOON-like lists, explicit empty states and a next-step `help` line.
- Update [Using the Platform](00-Start-Here/Using-the-Platform.md) when a command, flag or default changes.

## Style

- No emojis and no em or en dashes anywhere, including code comments and commit messages; use a plain `-`.
- One sentence per line in Markdown prose.
- Frontmatter is flat; list items must not contain commas.
- Notes use `NN-Title-Case-With-Hyphens.md` so they sort in study order; code uses `snake_case`.
- Link notes with relative Markdown links, not wikilinks; link SDE-Interview-Prep with absolute GitHub URLs.

## Code of conduct

Be respectful and constructive.
This is a learning community: assume good faith, critique the content, not the person.
