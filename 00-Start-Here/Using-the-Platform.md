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

## Where progress is stored

Progress is personal and is never written into the repo.
It lives in `~/.local/share/quant-prep/state.json`, or in `$QP_HOME/state.json` if you set `QP_HOME`.
Point `QP_HOME` at a private, backed-up folder to keep progress across machines.
The file is plain JSON and every write is atomic.

## Commands

| Command | What it does |
| :--- | :--- |
| `./qp` | Readiness per track, today's review queue, next topics, top firms. |
| `./qp syllabus [--track T] [--section S] [--tier core]` | Every topic with status, cards and your mastery. |
| `./qp show <topic> [--full]` | Objectives, prerequisites, what it unlocks, its cards. |
| `./qp mark <topic> <0-4>` | Record mastery: 1 studied, 2 practiced, 3 solid, 4 interview-ready. |
| `./qp next` | Unblocked topics to study next. |
| `./qp plan [--hours H] [--core] [--weeks N]` | A dated weekly plan in prerequisite order. |
| `./qp review` | Interactive spaced-repetition review of due cards. |
| `./qp due` and `./qp grade <card> <again,hard,good,easy>` | The same review, non-interactively (for scripts and agents). |
| `./qp drill arith` | Arithmetic sprint on Zetamac rules (120 seconds). |
| `./qp drill optiver` | 80 mixed numerical questions in 8 minutes. |
| `./qp drill mm` | Market-making game on the sum of hidden dice. |
| `./qp stats` | Drill history and daily activity. |
| `./qp firms [firm]` | Readiness per firm; for one firm, its weakest focus topics. |
| `./qp serve [--open]` | Local dashboard. |
| `./qp check` | Validate notes, cards, links and style (CI runs this). |
| `./qp index` | Regenerate the topic tables in section READMEs. |

## How the numbers are computed

- Topic readiness is mastery/4 when a topic has no cards; otherwise half mastery/4 and half card maturity, where a card is fully mature once its review interval reaches 21 days.
- Track and firm readiness are averages of topic readiness weighted by study hours and tier (core 1.0, advanced 0.6, senior 0.4).
- Card scheduling is SM-2 style: "again" repeats the card today, "good" goes 1 day, 3 days, then multiplies by the card's ease.
- New cards are capped per day (`./qp profile --new-cards N`, default 20) so the review queue stays manageable.

## Reading in Obsidian

Open the repo folder as a vault.
Question cards are collapsible callouts, so you can quiz yourself while reading; the answer stays folded until you click it.
Notes link with relative Markdown links, which work in Obsidian, on GitHub and in the dashboard.

## Writing and fixing notes

Follow [Note Conventions](Note-Conventions.md), then run `./qp check` and `./qp index`.
Seed notes are the writing backlog: `./qp syllabus` shows them with status `seed`.
