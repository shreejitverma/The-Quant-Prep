---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: []
est_hours: 2
sources: [Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008), Timothy Crack - Heard on the Street: Quantitative Questions from Wall Street Job Interviews, Mark Joshi - Nick Denson and Andrew Downes - Quant Job Interview Questions and Answers]
---

# How Quant Interviews Work

## TL;DR

- Most pipelines follow the same shape: application screen, online assessment, one or two phone or video screens, then a final round ("superday") of several back-to-back interviews.
- Traders are filtered on speed and decision-making (mental maths, probability, games); researchers on depth (statistics, modelling, a project or take-home); developers on coding, systems and performance.
- Every round scores the same underlying things: correctness, speed, structured reasoning out loud, reaction to hints and new information, and judgement about risk.
- Online assessments are usually the highest-attrition stage and the most trainable; treat them as a skill to drill, not a formality.
- Firm-specific formats change often; use [the firm guides](../14-Firms/README.md) for reported details and treat them as reports, not guarantees.

## Learning objectives

- Know the typical pipeline for trader, researcher and developer roles.
- Know what each round is scoring and how to show it.

## Core concepts

### The generic pipeline

1. **Application and resume screen.** Filters on school, grades, competitions, relevant experience and, for experienced hires, track record.
   See [Resume and Application Strategy](10-Resume-and-Application-Strategy.md).
2. **Online assessment (OA).** Timed and automated.
   Commonly reported types: arithmetic sprints, numerical reasoning and sequence tests, probability multiple choice, coding challenges on a hosted platform, and sometimes a game-like or cognitive test.
3. **Phone or video screens.** One or two, typically 30 to 60 minutes with an engineer, trader or researcher; rapid-fire probability and brainteasers for traders, a live coding problem for developers, a technical conversation about past work for researchers.
4. **Final round or superday.** Several interviews in a day (on-site or virtual), often including a trading game for trader roles, a system design or low-level round for developers, and a research presentation or case for researchers, plus behavioural conversations.
5. **Decision and offer.** Often quick at trading firms; see [Offers, Compensation and Negotiation](11-Offers-Compensation-and-Negotiation.md).

Experienced hires often skip the OA and replace some puzzle rounds with deep discussion of their past work; see [Senior-Level Expectations](12-Senior-Level-Expectations.md).

### What differs by role

| Role | Emphasis in screens | Distinctive rounds |
| :--- | :--- | :--- |
| Quant trader | Mental maths, probability, expected value, betting and sizing | Market-making and trading games, estimation markets, numerical tests |
| Quant researcher | Probability, statistics, linear algebra, ML, coding for data | Research case or take-home, presentation of a project, modelling discussion |
| Quant developer | Data structures and algorithms, C++ or Python depth | Systems and low-latency design, concurrency, debugging, code review |

Hybrid roles mix these, and some firms run a common first stage for all roles.

### What each round scores

- **Online assessment:** raw accuracy and speed; there is no one to explain yourself to, so only the answer counts.
- **Phone screen:** can you get to correct answers quickly while communicating clearly; the interviewer is deciding whether a full day is worth it.
- **Technical rounds:** depth and robustness; interviewers push past the first answer with follow-ups and variations to find where understanding stops.
- **Trading games:** expected-value thinking, position and risk management, updating on information, and composure when losing.
- **Research rounds:** framing a vague problem, choosing methods, spotting leakage and overfitting, and being honest about what does not work.
- **Coding and design rounds:** working code, complexity, edge cases, testing and, for low-latency roles, awareness of memory and CPU costs.
- **Behavioural and fit:** motivation for this firm and role, collaboration, and how you handle mistakes; see [Behavioral and Fit](09-Behavioral-and-Fit.md).

### How to show what is being scored

- Think out loud in a structured way: restate, plan, compute, check.
- Give a quick estimate before an exact answer, and a sanity check after.
- Take hints as information and say how they change your approach.
- When wrong, say so quickly and fix it; recovery is scored, stubbornness is penalised.
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
The interviewer scores the speed, the method, the independent check and the readiness for the variation.

### Example 2: pacing an 80-question, 8-minute numerical test

The average budget is $480/80 = 6$ seconds per question.
A workable plan: answer immediately what takes under 6 seconds, give a second pass to anything that takes up to 12, and skip anything longer.
If wrong answers are penalised, do not guess blind unless the expected score of a guess is non-negative (see [Sequences and Numerical Reasoning](06-Sequences-and-Numerical-Reasoning.md)).
Train the pacing with `./qp drill optiver`, which uses this 80-in-8 format.

### Example 3: opening a trading round

"Make me a market on the number of heads in 10 fair coin flips."
Say the fair value and uncertainty first: the count is binomial with mean $5$ and standard deviation $\sqrt{10 \times 0.25} \approx 1.58$.
Quote something like "4.5 at 5.5" and state your size.
When the interviewer trades, say the new position and whether you think the trade was informative before re-quoting.
The round is scored on that running commentary as much as on P&L.

### Example 4: a developer's design round

"Design the order book for a single instrument."
Start with the operations and their frequencies (add, cancel, modify, match, best bid and offer queries), then the data structures (price levels in a sorted array or map, FIFO queues per level, an id-to-order index for $O(1)$ cancel), then latency concerns (allocation on the hot path, cache locality).
Say which trade-offs you are making and how you would test it.
The interviewer is scoring requirements gathering, correctness under edge cases and performance awareness, not a memorised design; see [Coding Interviews for Quants](07-Coding-Interviews-for-Quants.md).

## Pitfalls

- Treating the OA as a formality; for many candidates it is the largest filter and the most trainable.
- Preparing only puzzles for a researcher or developer role, or only LeetCode for a trader role.
- Silence while thinking; the interviewer cannot credit reasoning they do not hear.
- Defending a wrong answer instead of re-checking it.
- Over-trusting forum reports of a firm's process, which change between years and between offices.
- Neglecting behavioural preparation; "why this firm" and "tell me about a mistake" are asked at most final rounds.

## Interview questions

> [!question]- int-pipeline-typical-stages | What is the typical stage order in a quant hiring pipeline?
> Resume screen, online assessment, one or two phone or video screens, then a multi-interview final round, then an offer. Experienced hires often skip the online assessment.

> [!question]- int-pipeline-oa-scoring | What does an online assessment score that a live interview does not?
> Only the final answer, under strict time. There is no credit for reasoning, so accuracy and pacing are everything.

> [!question]- int-pipeline-trader-vs-researcher | How do trader and researcher interviews differ in emphasis?
> Traders are tested on speed, mental maths, expected value and decisions under uncertainty, often in games. Researchers are tested on depth in statistics, modelling, ML and coding for data, often with a case or project discussion.

> [!question]- int-pipeline-dev-rounds | What distinguishes quant developer rounds from generic software interviews?
> More emphasis on C++ or Python depth, performance, memory and concurrency, and domain systems such as order books and market data handlers, alongside standard algorithms.

> [!question]- int-pipeline-why-think-aloud | Why should you think out loud in a technical round?
> The interviewer scores the reasoning, not just the result; talking lets them credit partial progress and give useful hints, and shows how you would work on a desk.

> [!question]- int-pipeline-when-stuck | What should you do when stuck on an interview problem?
> Say what you have tried and ruled out, solve a smaller or special case, and ask a clarifying question. A hint taken well is usually scored better than silence.

> [!question]- int-pipeline-wrong-answer | You realise an earlier answer was wrong. What do you do?
> Say so immediately, correct it and explain the error. Self-correction signals reliability; defending a wrong answer is a strong negative.

> [!question]- int-pipeline-trading-game-scored | In a trading game, what are interviewers usually scoring?
> Expected-value reasoning, updating on information including the counterparty's trades, position and risk control, clear communication, and composure. P&L in a short game is mostly noise.

> [!question]- int-pipeline-geometric-first-six | Expected number of die rolls until the first 6?
> 6. Geometric with $p = 1/6$ has mean $1/p$; check with $E = 1 + (5/6)E$.

> [!question]- int-pipeline-test-pacing | An 80-question test lasts 8 minutes. What is your per-question budget?
> 6 seconds on average; skip anything that clearly needs more than about twice that and return if time remains.

> [!question]- int-pipeline-experienced-hire | How does the pipeline typically change for an experienced hire?
> Less emphasis on generic puzzles and OAs, more on depth in past work, domain knowledge, track record and how you would add value from day one.

> [!question]- int-pipeline-superday | What is a superday and how should you prepare for it?
> A final round of several consecutive interviews covering technical depth, role-specific exercises (games, design, research) and fit. Prepare stamina and consistency: each interviewer scores independently, so one weak round can sink the day.

## In this repo and SDE-Interview-Prep

- Firm-specific pipeline reports: [14-Firms](../14-Firms/README.md).
- Mock interview and behavioural material in SDE-Interview-Prep: [06-Interview-Prep](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/06-Interview-Prep/README.md).

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008).
- Timothy Crack, *Heard on the Street: Quantitative Questions from Wall Street Job Interviews*.
- Mark Joshi, Nick Denson and Andrew Downes, *Quant Job Interview Questions and Answers*.
