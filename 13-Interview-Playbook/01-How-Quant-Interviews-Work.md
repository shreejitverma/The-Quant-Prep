---
type: concept
track: [quant-trader, quant-research, quant-dev, quant-risk]
tier: core
status: solid
prereqs: []
est_hours: 2
sources: [Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008), Timothy Crack - Heard on the Street: Quantitative Questions from Wall Street Job Interviews, Mark Joshi - Nick Denson and Andrew Downes - Quant Job Interview Questions and Answers, Jane Street - Trading interviews - https://www.janestreet.com/trading-interviews, Jane Street - Strategy and Product interviewing - https://www.janestreet.com/join-jane-street/sp/interviewing/]
---

# How Quant Interviews Work

## TL;DR

- Prepare for a common shape: application screen, often an online assessment, one or two phone or video screens, then a final round ("superday") of several interviews; each firm's careers pages describe its own version.
- Expect trader rounds to stress speed and decision-making (mental maths, probability, games), researcher rounds depth (statistics, modelling, a project or take-home), and developer rounds coding, systems and performance.
- In every round, show the same things: correctness, speed, structured reasoning out loud, reaction to hints and new information, and judgement about risk.
- Online assessments are among the most trainable stages; treat them as a skill to drill, not a formality.
- Formats change; read the firm's own pages first, then [the firm guides](../14-Firms/README.md), and treat candidate reports as reports, not guarantees.

## Learning objectives

- Know the typical pipeline for trader, researcher and developer roles.
- Know what each round is scoring and how to show it.

## Core concepts

### The generic pipeline

The stages below are a preparation checklist, not a description of any one firm; firms skip, merge and reorder them.

1. **Application and resume screen.** Expect school, grades, competitions, relevant experience and, for experienced hires, track record to be read.
   See [Resume and Application Strategy](10-Resume-and-Application-Strategy.md).
2. **Online assessment (OA).** Timed and automated.
   Formats to prepare for: arithmetic sprints, numerical reasoning and sequence tests, probability multiple choice, coding challenges on a hosted platform, and game-like or cognitive tests.
3. **Phone or video screens.** One or two, with an engineer, trader or researcher; prepare rapid-fire probability and brainteasers for trading roles, a live coding problem for developer roles, and a technical conversation about past work for research roles.
4. **Final round or superday.** Several interviews, on-site or virtual, which may include a trading game for trader roles, a system design or low-level round for developers, and a research presentation or case for researchers, plus behavioural conversations.
5. **Decision and offer.** See [Offers, Compensation and Negotiation](11-Offers-Compensation-and-Negotiation.md).

Two published examples, as of November 2026: Jane Street's trading interview page describes phone interviews at the start and in-person interviews for the final stage, with final-round questions that may cover problem solving, probability and statistics, coding, data analysis and general interests.
Its Strategy and Product page describes an online assessment, one or two video interviews and a final round of in-person interviews.

Experienced hires may skip the OA and replace some puzzle rounds with deep discussion of their past work; see [Senior-Level Expectations](12-Senior-Level-Expectations.md).

### What differs by role

| Role | Emphasis in screens | Distinctive rounds |
| :--- | :--- | :--- |
| Quant trader | Mental maths, probability, expected value, betting and sizing | Market-making and trading games, estimation markets, numerical tests |
| Quant researcher | Probability, statistics, linear algebra, ML, coding for data | Research case or take-home, presentation of a project, modelling discussion |
| Quant developer | Data structures and algorithms, C++ or Python depth | Systems and low-latency design, concurrency, debugging, code review |

Hybrid roles mix these, and a first stage may be shared across roles.

### What each round is likely to score

- **Online assessment:** raw accuracy and speed; there is no one to explain yourself to, so only the answer counts.
- **Phone screen:** can you get to correct answers quickly while communicating clearly; treat it as the gate to the final round.
- **Technical rounds:** depth and robustness; expect follow-ups and variations that push past the first answer to find where understanding stops.
- **Trading games:** expected-value thinking, position and risk management, updating on information, and composure when losing.
- **Research rounds:** framing a vague problem, choosing methods, spotting leakage and overfitting, and being honest about what does not work.
- **Coding and design rounds:** working code, complexity, edge cases, testing and, for low-latency roles, awareness of memory and CPU costs.
- **Behavioural and fit:** motivation for this firm and role, collaboration, and how you handle mistakes; see [Behavioral and Fit](09-Behavioral-and-Fit.md).

### How to show what is being scored

- Think out loud in a structured way: restate, plan, compute, check.
- Give a quick estimate before an exact answer, and a sanity check after.
- Take hints as information and say how they change your approach.
- When wrong, say so quickly and fix it; "correct your mistakes" is one of the tips on Jane Street's trading interview page.
- In games and markets, state position and reasoning before every decision.

### Preparation map

| Stage | Notes in this repo | Drill |
| :--- | :--- | :--- |
| OA arithmetic and numerical | [Mental Math](02-Mental-Math.md), [Sequences and Numerical Reasoning](06-Sequences-and-Numerical-Reasoning.md) | `./qp drill arith`, `./qp drill optiver` |
| Screens | [Brainteasers and Puzzles](03-Brainteasers-and-Puzzles.md), [Probability](../01-Probability/README.md) | `./qp review` |
| Estimation markets | [Estimation and Fermi Problems](04-Estimation-and-Fermi-Problems.md) | - |
| Trading games | [Trading Games in Interviews](05-Trading-Games-in-Interviews.md) | `./qp drill mm` |
| Coding | [Coding Interviews for Quants](07-Coding-Interviews-for-Quants.md) | - |
| Research case | [Research Case Studies and Take-Homes](08-Research-Case-Studies-and-Take-Homes.md) | - |

## Worked examples

### Example 1: a phone-screen probability question, answered aloud

"What is the expected number of rolls of a fair die to get the first 6?"

A strong answer, in the order spoken:
"The number of rolls is geometric with success probability $1/6$, so the expectation is $1/p = 6$.
To check it with a first-step argument: $E = 1 + (5/6)E$, which gives $E/6 = 1$ and $E = 6$."
Then anticipate the follow-up: "Two 6s in a row would be $E = 42$ by the same first-step method."
The interviewer can credit the speed, the method, the independent check and the readiness for the variation.

### Example 2: pacing an 80-question, 8-minute numerical test

The average budget is $480/80 = 6$ seconds per question.
A workable plan: answer immediately what takes under 6 seconds, give a second pass to anything that takes up to 12, and skip anything longer.
If wrong answers are penalised, do not guess blind unless the expected score of a guess is non-negative (see [Sequences and Numerical Reasoning](06-Sequences-and-Numerical-Reasoning.md)).
Train the pacing with `./qp drill optiver`, which uses this 80-in-8 format; the drill's name is the repo's label, not a description of any firm's current test.

### Example 3: opening a trading round

"Make me a market on the number of heads in 10 fair coin flips."
Say the fair value and uncertainty first: the count is binomial with mean $5$ and standard deviation $\sqrt{10 \times 0.25} \approx 1.58$.
Quote something like "4.5 at 5.5" and state your size.
When the interviewer trades, say the new position and whether you think the trade was informative before re-quoting.
Expect the running commentary to count as much as the P&L.

### Example 4: a developer's design round

"Design the order book for a single instrument."
Start with the operations and their frequencies (add, cancel, modify, match, best bid and offer queries), then the data structures (price levels in a sorted array or map, FIFO queues per level, an id-to-order index for $O(1)$ cancel), then latency concerns (allocation on the hot path, cache locality).
Say which trade-offs you are making and how you would test it.
Show requirements gathering, correctness under edge cases and performance awareness rather than a memorised design; see [Coding Interviews for Quants](07-Coding-Interviews-for-Quants.md).

## Pitfalls

- Treating the OA as a formality; failing it ends the process, and it is among the most trainable stages.
- Preparing only puzzles for a researcher or developer role, or only LeetCode for a trader role.
- Silence while thinking; the interviewer cannot credit reasoning they do not hear.
- Defending a wrong answer instead of re-checking it.
- Over-trusting forum reports of a firm's process, which change between years and between offices.
- Neglecting behavioural preparation; have answers to "why this firm" and "tell me about a mistake" ready before any final round.

## Interview questions

> [!question]- int-pipeline-typical-stages | What is the typical stage order in a quant hiring pipeline?
> A common order to prepare for: resume screen, online assessment, one or two phone or video screens, then a multi-interview final round, then an offer.
> Firms skip or merge stages (Jane Street's trading page, for example, describes phone interviews then in-person finals), and experienced hires may skip the online assessment.

> [!question]- int-pipeline-oa-scoring | What does an online assessment score that a live interview does not?
> Only the final answer, under strict time. There is no credit for reasoning, so accuracy and pacing are everything.

> [!question]- int-pipeline-trader-vs-researcher | How do trader and researcher interviews differ in emphasis?
> Expect trader rounds to stress speed, mental maths, expected value and decisions under uncertainty, often in games. Expect researcher rounds to stress depth in statistics, modelling, ML and coding for data, often with a case or project discussion.

> [!question]- int-pipeline-dev-rounds | What distinguishes quant developer rounds from generic software interviews?
> More emphasis on C++ or Python depth, performance, memory and concurrency, and domain systems such as order books and market data handlers, alongside standard algorithms.

> [!question]- int-pipeline-why-think-aloud | Why should you think out loud in a technical round?
> Talking shows the reasoning, not just the result; it lets the interviewer credit partial progress and give useful hints, and shows how you would work on a desk.

> [!question]- int-pipeline-when-stuck | What should you do when stuck on an interview problem?
> Say what you have tried and ruled out, solve a smaller or special case, and ask a clarifying question. Take a hint as information rather than sitting in silence.

> [!question]- int-pipeline-wrong-answer | You realise an earlier answer was wrong. What do you do?
> Say so immediately, correct it and explain the error. Self-correction signals reliability; defending a wrong answer is a strong negative.

> [!question]- int-pipeline-trading-game-scored | In a trading game, what should you show beyond P&L?
> Expected-value reasoning, updating on information including the counterparty's trades, position and risk control, clear communication, and composure. P&L in a short game is mostly noise.

> [!question]- int-pipeline-geometric-first-six | Expected number of die rolls until the first 6?
> $6$. Geometric with $p = 1/6$ has mean $1/p$; check with $E = 1 + (5/6)E$.

> [!question]- int-pipeline-test-pacing | An 80-question test lasts 8 minutes. What is your per-question budget?
> 6 seconds on average; skip anything that clearly needs more than about twice that and return if time remains.

> [!question]- int-pipeline-experienced-hire | How does the pipeline typically change for an experienced hire?
> Expect less emphasis on generic puzzles and OAs, and more on depth in past work, domain knowledge, track record and how you would add value from day one.

> [!question]- int-pipeline-superday | What is a superday and how should you prepare for it?
> A final round of several consecutive interviews covering technical depth, role-specific exercises (games, design, research) and fit. Prepare stamina and consistency: each interview is a separate data point, so one weak round can sink the day.

> [!question]- int-pipeline-two-sixes-in-a-row | Expected number of die rolls until two 6s in a row?
> $42$.
> With $E_0$ from scratch and $E_1$ after a single 6: $E_0 = 1 + \tfrac56 E_0 + \tfrac16 E_1$ and $E_1 = 1 + \tfrac56 E_0$, so $E_0 = 6 + 36 = 42$.

> [!question]- int-pipeline-ten-flips-market | Make a market on the number of heads in 10 fair coin flips. What do you say first?
> Fair value $5$ and standard deviation $\sqrt{10 \times 0.25} \approx 1.58$, then a quote such as 4.5 at 5.5 with a size.
> Stating the distribution first shows where the width comes from.

> [!question]- int-pipeline-where-to-check-format | Where should you look first for a firm's interview format, and how should you treat forum reports?
> The firm's own careers and interview pages, which some firms publish (Jane Street's trading page, for example, as of November 2026).
> Forum and candidate reports vary by year, office and role; use them for practice ideas, not as a guarantee of what you will see.

> [!question]- int-pipeline-oa-guessing | An online test penalises wrong answers. When should you guess?
> Only when the expected score of the guess is non-negative: with $k$ options and penalty $c$, a blind guess is worth $1/k - c(1 - 1/k)$.
> Eliminating options raises that value, so narrow down before guessing (see [Sequences and Numerical Reasoning](06-Sequences-and-Numerical-Reasoning.md)).

## In this repo and The-Distinguished-Engineer

- Code: [`code/interview_01_pipeline.py`](code/interview_01_pipeline.py) prints and asserts the numbers on this page: the waiting times for one 6 and for two 6s in a row by solving the absorbing Markov chain exactly and by seeded simulation, the coin-flip market by enumerating all $2^{10}$ sequences, and the pacing budget from the drill's own configuration.
- Firm-specific pipeline reports: [14-Firms](../14-Firms/README.md).
- Mock interview and behavioural material in The-Distinguished-Engineer: [06-Interview-Prep](https://github.com/shreejitverma/The-Distinguished-Engineer/blob/main/06-Interview-Prep/README.md).

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008).
- Timothy Crack, *Heard on the Street: Quantitative Questions from Wall Street Job Interviews*.
- Mark Joshi, Nick Denson and Andrew Downes, *Quant Job Interview Questions and Answers*.
- Jane Street, "Trading interviews", https://www.janestreet.com/trading-interviews (process and tips, checked November 2026).
- Jane Street, "What to expect in your Strategy & Product interviews", https://www.janestreet.com/join-jane-street/sp/interviewing/ (checked November 2026).
