---
type: guide
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
sources: []
---

# Using the Platform

The repo is three things over one set of Markdown notes: an Obsidian vault for reading, the `qp` command line for tracking, and a local web dashboard for everything at once.
All three read the same notes; your progress lives in one private state file.

## Setup

Requirements: Python 3.10 or later. The platform uses only the standard library; no install step.

```sh
git clone https://github.com/shreejitverma/The-Quant-Prep.git
cd The-Quant-Prep
./qp profile --tracks quant-trader --hours 12   # choose your target role(s) and weekly hours
./qp                                            # live progress
./qp serve --open                               # the dashboard at http://127.0.0.1:8765/
```

Keep SDE-Interview-Prep cloned next to this repo (`../SDE-Interview-Prep`) so cross-repo links can be checked.
For the runnable examples in each section's `code/` folder, use `environment.yml` (conda) or `uv run --with numpy --with scipy --with pandas --with matplotlib python <file>`.
`python tools/run_examples.py` runs every example, the way CI does; every example must run cleanly, and examples that assert their numbers fail when a note's numbers drift.

## Where progress is stored

Progress is personal and is never written into the repo.
It lives in `~/.local/share/quant-prep/state.json`, or in `$QP_HOME/state.json` if you set `QP_HOME`.
Point `QP_HOME` at a private, backed-up folder to keep progress across machines.
The file is plain JSON and every write is atomic.
A version 1 file whose tracks are exactly the old default (quant-trader, quant-research and quant-dev) gains quant-risk on load, because section 17 and 18 notes used to be tagged for all three; any other saved track list is left as it is.
The file is written as version 2 on the next save.

## Commands

| Command | What it does |
| :--- | :--- |
| `./qp` | Readiness per track, today's review queue, next topics, top firms. |
| `./qp profile [--tracks T ...] [--hours H] [--new-cards N]` | Your target tracks (`quant-trader`, `quant-research`, `quant-dev`, `quant-risk`), weekly hours and daily new cards. |
| `./qp syllabus [--track T] [--section S] [--tier core]` | Every topic with status, cards and your mastery. |
| `./qp show <topic> [--full]` | Objectives, prerequisites, what it unlocks, its cards. |
| `./qp mark <topic> <0-4>` | Record mastery: 1 studied, 2 practiced, 3 mastered, 4 interview-ready. |
| `./qp next` | Unblocked topics to study next. |
| `./qp plan [--hours H] [--core] [--weeks N]` | A dated weekly plan in prerequisite order. |
| `./qp plan [--persona P]` | Tailor a weekly plan and lab drills to a Markets Mastery persona (`holistic`, `quant_trader`, `quant_researcher`, `macro_derivatives_trader`, or `retail_algorithmic_trader`). |
| `./qp review` | Interactive spaced-repetition review of due cards. |
| `./qp due` and `./qp grade <card> <again,hard,good,easy>` | The same review, non-interactively (for scripts and agents). |
| `./qp drill arith` | Arithmetic sprint on Zetamac rules (120 seconds). |
| `./qp drill optiver` | 80 mixed numerical questions in 8 minutes. |
| `./qp drill mm` | Market-making game on the sum of hidden dice. |
| `./qp stats` | Drill history and daily activity. |
| `./qp firms [firm]` | Readiness per firm; for one firm, its weakest focus topics. |
| `./qp markets [status|gates|mastery] [--persona P]` | Markets curriculum readiness, stage gates, and persona mastery scores. |
| `./qp lab [list|info <id>|run <id>]` | Browse or run a Trading Lab simulation engine. |
| `./qp serve [--open]` | Local dashboard. |
| `./qp check` | Validate notes, cards, links and style (CI runs this). |
| `./qp index` | Regenerate the topic tables in section READMEs. |
| `./qp bank <folder>` | Import a private question bank into the overlay (see below). |

The Trading Lab web interface is available at `http://localhost:8765/lab/` after starting `./qp serve`.
See the [Markets Mastery OS hub](../16-Trading-and-Investing/MARKETS_HUB.md) for the curriculum map, engine list, and study board.

## How the numbers are computed

- Topic readiness is mastery/4 when a topic has no cards; otherwise half mastery/4 and half card maturity, where a card is fully mature once its review interval reaches 21 days.
- Track and firm readiness are averages of topic readiness weighted by study hours and tier (core 1.0, advanced 0.6, senior 0.4).
- Card scheduling is SM-2 style: "again" repeats the card today, "good" goes 1 day, 3 days, then multiplies by the card's ease.
- New cards are capped per day (`./qp profile --new-cards N`, default 20) so the review queue stays manageable.

## Private overlay and question banks

`private/` (or the folder in `$QP_PRIVATE`) holds material that must never be published: question banks from courses or colleagues, personal notes.
Git ignores it, and `./qp check` fails if any file in it is ever tracked.
`qp` loads it next to the syllabus: a private note with `extends: <topic-id>` adds its cards to that topic, so they count toward the topic's readiness, the track and firm scores, and the daily review queue.

Import a bank exported as a tab-separated file of firm, category and question:

```sh
mkdir -p private/my-bank && cp export.tsv private/my-bank/source.tsv
./qp bank private/my-bank --prefix my --name "My bank"
```

The importer merges duplicate questions (keeping every firm that asked), gives each question a stable id derived from its text, and writes one note per syllabus topic plus `By-Firm.md`.
Answers live in `private/my-bank/answers/*.json` as `{id: {topic, answer, verified, duplicate_of}}`; re-running the import after refreshing `source.tsv` keeps them.
A merged question takes its id from the first variant seen, so a refresh that reorders or drops that variant changes the id; the import then lists the orphaned answer ids so you can re-key them in `answers/*.json`.
Questions without an answer are listed under "Not yet answered" and stay out of review until answered.

## Reading in Obsidian

Open the repo folder as a vault.
Question cards are collapsible callouts, so you can quiz yourself while reading; the answer stays folded until you click it.
Notes link with relative Markdown links, which work in Obsidian, on GitHub and in the dashboard.

## Writing and fixing notes

Follow [Note Conventions](Note-Conventions.md), then run `./qp check` and `./qp index`.
Seed notes are the writing backlog: `./qp syllabus` shows them with status `seed`.
