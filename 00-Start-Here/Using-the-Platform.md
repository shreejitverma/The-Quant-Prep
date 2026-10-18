---
type: guide
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: core
status: solid
sources: []
---

# Using the Platform

The repo is three things over one set of Markdown notes: an Obsidian vault for reading, the `qp` command line for tracking, and a local web dashboard for everything at once.
All three read the same notes, and your progress lives in one private state file outside the repo.
Developers extending the platform want [the qp platform reference](../tools/qp/README.md) instead.

## Setup

Requirements: Python 3.10 or later.
The platform uses only the standard library, so there is no install step.

```sh
git clone https://github.com/shreejitverma/The-Quant-Prep.git
cd The-Quant-Prep
./qp profile --tracks quant-trader --hours 12   # your target role(s) and weekly hours
./qp                                            # live progress
./qp serve --open                               # the dashboard at http://127.0.0.1:8765/
```

- **Tracks** are `quant-trader`, `quant-research`, `quant-dev` and `quant-risk`; pass several to study for more than one role.
- **Runnable examples** in each section's `code/` folder need numpy, pandas and matplotlib: use `environment.yml` with conda, or `uv run --no-project --with numpy --with pandas --with matplotlib python <file>.py`.
- **Cross-repo links:** keep SDE-Interview-Prep cloned next to this repo (`../SDE-Interview-Prep`) if you want `./qp check --strict-sde` to verify links into it.
- **The dashboard** loads its Markdown, maths and diagram renderers from a CDN; without network access notes show as plain text.

## A typical day

```sh
./qp                    # what is due, what to study next
./qp review             # 15-20 minutes of cards
./qp drill arith        # 2 minutes of mental arithmetic (trader and researcher tracks)
./qp next               # pick the next topic, study it, then:
./qp mark <topic> 2     # record your mastery honestly
```

## Commands

`--track` can be repeated on any command that takes it; it defaults to the tracks in your profile.

### Progress and planning

| Command | What it does |
| :--- | :--- |
| `./qp` or `./qp status [--track T]` | Readiness per track, your streak, today's review queue, the next five topics and your top five firms. |
| `./qp profile [--tracks T ...] [--hours H] [--new-cards N]` | Your target tracks, weekly hours (0 to 100) and daily new-card limit (default 20). |
| `./qp syllabus [--track T] [--section S] [--tier core\|advanced\|senior]` | Every topic with status, cards and your mastery; `--section` matches part of a folder name. |
| `./qp show <topic> [--full]` | Objectives, prerequisites, what it unlocks and its cards; `--full` prints the note. Topics resolve by id, unique prefix or part of the title. |
| `./qp mark <topic> <level>` | Record mastery: 0 unseen, 1 studied, 2 practiced, 3 mastered, 4 interview-ready (a name works too). |
| `./qp next [--track T] [--limit 8]` | Unblocked topics to study next; partly studied topics come first. |
| `./qp plan [--hours H] [--core] [--no-senior] [--weeks N]` | A dated weekly plan in prerequisite order; `--weeks` limits how many weeks are shown. |
| `./qp plan --persona P` | A plan with lab drills for a Markets Mastery persona: `holistic`, `quant_trader`, `quant_researcher`, `macro_derivatives_trader` or `retail_algorithmic_trader`. |
| `./qp firms [firm] [--limit 15]` | Readiness per firm; for one firm, its focus topics, weakest first. |
| `./qp stats [--limit 15]` | Drill history, the last 14 days of activity and your streak. |

### Review and drills

| Command | What it does |
| :--- | :--- |
| `./qp review [--track T] [--limit N]` | Interactive spaced repetition: Enter reveals the answer, 1 to 4 grades it (again, hard, good, easy), `q` quits. |
| `./qp due [--track T] [--limit N]` and `./qp grade <card> <again\|hard\|good\|easy>` | The same review without a terminal, for scripts and agents. |
| `./qp drill arith [--seconds 120] [--seed S]` | Arithmetic sprint on Zetamac rules; you stay on a problem until you answer it. |
| `./qp drill optiver [--seconds S] [--seed S]` | 80 mixed numerical questions in 8 minutes. |
| `./qp drill mm [--seed S]` | The market-making game: quote a two-sided market on the sum of hidden dice; scored by P&L. |

### Markets Mastery OS and the Trading Lab

| Command | What it does |
| :--- | :--- |
| `./qp markets [status\|gates\|mastery] [--persona P]` | Markets curriculum tracks, stage gates and your persona mastery score (default `status`, persona `holistic`). |
| `./qp lab list` | The eleven Trading Lab engines. |
| `./qp lab info <engine>` | An engine's parameters, defaults and bounds. |
| `./qp lab run <engine> key=value ...` | Run an engine; the run counts toward the Markets mastery score. |
| `./qp journal log key=value ...` | Log a trade to your journal (`r_multiple`, `pnl`, `mae_r`, `mfe_r` and `adherence` are required). |
| `./qp journal [stats]` | Journal analytics: win rate, profit factor, expectancy, drawdown, adherence and the capital gate. |

See the [Markets Mastery OS hub](../16-Trading-and-Investing/MARKETS_HUB.md) for the curriculum map and engine list.

### Dashboard and content tools

| Command | What it does |
| :--- | :--- |
| `./qp serve [--host 127.0.0.1] [--port 8765] [--open]` | The local dashboard; `--open` opens your browser. |
| `./qp check [files ...] [--strict-sde]` | Validate notes, cards, links and style (CI runs this); file arguments limit the link and style checks. |
| `./qp index` | Regenerate the generated tables in the section READMEs and the root README. |
| `./qp bank <folder> [--prefix wsq] [--name WSQ]` | Import a private question bank into the overlay (see below). |

Output is designed to be read by people and by agents: tables print as `name[N]{fields}:` with one row per line, an empty result says `0 results`, and a `help` list suggests the next step.

## The dashboard

`./qp serve --open` serves the dashboard at `http://127.0.0.1:8765/`.

| Page | What you do there |
| :--- | :--- |
| Dashboard | See your streak, review queue, mature cards, track readiness, next topics, firm readiness, best drill scores and an activity heatmap. |
| Syllabus | Browse every section; filter by text, tier, track or written notes; set mastery per topic. |
| A note | Read it with rendered maths and diagrams, quiz yourself on its folded cards, and see its prerequisites and what it unlocks. |
| Review | Work today's cards: Space reveals, keys 1 to 4 grade. |
| Drills | Arithmetic sprint, 80-in-8 and the market-making game. |
| Plan | Your weekly plan; change tracks or weekly hours. |
| Firms | Readiness per firm and each firm's focus topics. |

The Trading Lab is at `http://127.0.0.1:8765/lab/`.
Selecting an engine shows a quick preview computed in the browser; **Run Simulation** runs the real engine on the server and records the run.

The server listens only on your machine and rejects requests from other sites, so another web page cannot change your progress.

## Where progress is stored

Progress is personal and is never written into the repo.

- It lives in `$QP_HOME/state.json` if you set `QP_HOME`, else `$XDG_DATA_HOME/quant-prep/`, else `~/.local/share/quant-prep/`.
- Point `QP_HOME` at a private, backed-up folder (for example a synced drive) to keep progress across machines.
- Every write is atomic and locked, so the CLI and the dashboard can run at the same time; the previous version is kept as `state.json.bak`.
- An older version 1 file with the original three-track default gains `quant-risk` automatically and is saved as version 2.

## How the numbers are computed

- **Topic readiness** is mastery/4 when a topic has no cards; otherwise half mastery/4 and half card maturity, where a card is fully mature once its review interval reaches 21 days.
- **Track and firm readiness** are averages of topic readiness weighted by study hours and tier (core 1.0, advanced 0.6, senior 0.4).
- **A topic is mastered** at level 3; remaining hours shrink as your mastery rises.
- **Card scheduling** is SM-2 style:

| Grade | Next review | Ease (starts at 2.5, never below 1.3) |
| :--- | :--- | :--- |
| Again | Later today | down 0.2 |
| Hard | 1.2 times the last interval, at least 1 day | down 0.15 |
| Good | 1 day, then 3 days, then the last interval times the ease | unchanged |
| Easy | 4 days, then the last interval times the ease times 1.3 | up 0.15 |

- **New cards** are capped per day (`./qp profile --new-cards N`, default 20) so the queue stays manageable.

## Private overlay and question banks

`private/` (or the folder in `$QP_PRIVATE`) holds material that must never be published: question banks from courses or colleagues, personal notes.
Git ignores it, and `./qp check` fails if any file in it is ever tracked.
`qp` loads it next to the syllabus: a private note with `extends: <topic-id>` adds its cards to that topic, so they count toward the topic's readiness, the track and firm scores, and the daily review queue.

Import a bank exported as a tab-separated file of firm, category and question:

```sh
mkdir -p private/my-bank && cp export.tsv private/my-bank/source.tsv
./qp bank private/my-bank --prefix my --name "My bank"
```

- The importer merges duplicate questions (keeping every firm that asked), gives each question a stable id derived from its text, and writes `bank.json`, one note per syllabus topic under `notes/`, and `By-Firm.md`.
- Answers live in `private/my-bank/answers/*.json` as `{id: {topic, answer, verified, duplicate_of}}`; re-running the import after refreshing `source.tsv` keeps them.
- A merged question takes its id from the first variant seen, so a refresh that reorders or drops that variant changes the id; the import then lists the orphaned answer ids so you can re-key them.
- Questions without an answer are listed under "Not yet answered" and stay out of review until answered.
- The importer refuses a folder inside the repo but outside `private/` unless you pass `--allow-public`.

## Reading in Obsidian

Open the repo folder as a vault; [Dashboard](Dashboard.md) is the home note.
Question cards are collapsible callouts, so you can quiz yourself while reading; the answer stays folded until you click it.
Notes link with relative Markdown links, which work in Obsidian, on GitHub and in the dashboard.
`tools/obsidian/README.md` sets up the shared plugin configuration.

## Troubleshooting

| Symptom | Fix |
| :--- | :--- |
| `error: .../state.json is not valid JSON ...; restore state.json.bak` | The state file is corrupt; copy `state.json.bak` over `state.json` in your `QP_HOME`. |
| `review` or `drill` refuses to start | They need an interactive terminal; in scripts use `./qp due` and `./qp grade`. |
| The dashboard shows notes as raw text | The renderers come from a CDN; check your network connection and reload. |
| `403` from the dashboard | Open it at `127.0.0.1` or `localhost` on the port you started it on. |
| A note edit does not appear | The server re-reads notes at most every two seconds; reload the page. |
| An example script fails with `ModuleNotFoundError` | Install numpy, pandas and matplotlib, or run it with `uv run` as shown in Setup. |
| `./qp check` reports `[index] generated table is stale` | Run `./qp index` and commit the updated READMEs. |

## Writing and fixing notes

Follow [Note Conventions](Note-Conventions.md) and [CONTRIBUTING](../CONTRIBUTING.md), then run `./qp check` and `./qp index`.
[How Notes Are Verified](How-Notes-Are-Verified.md) states the standard every note is held to.
