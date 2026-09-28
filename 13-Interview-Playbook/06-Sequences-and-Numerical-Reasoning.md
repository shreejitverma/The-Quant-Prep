---
type: concept
track: [quant-trader]
tier: advanced
status: solid
prereqs: [mental-math]
est_hours: 2
sources: [The On-Line Encyclopedia of Integer Sequences - https://oeis.org/, Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008)]
---

# Sequences and Numerical Reasoning Tests

## TL;DR

- Run a fixed checklist on any sequence: differences (repeat to second and third order), ratios, interleaved subsequences, known families (squares, cubes, primes, factorials, Fibonacci), then digit tricks.
- A polynomial of degree $k$ has constant $k$-th differences; $n^3 + n^2$ has constant third differences of 6.
- Mixed operations ($\times 2 - 1$, $+3$ then $-2$) show up as differences that are themselves a simple sequence.
- In numerical reasoning tests, percentage change, compounding and ratio questions dominate; average growth rates compound geometrically, not arithmetically.
- Time is the binding constraint: budget per question, skip early, and guess only when the scoring makes guessing non-negative in expectation.

## Learning objectives

- Spot common sequence rules quickly (differences, ratios, interleaving, primes).
- Manage time on numerical reasoning assessments.

## Core concepts

### Where this appears

Online assessments for trading and some research roles commonly include next-term sequence questions and data-interpretation questions under tight time limits.
Formats vary by firm and by year, and many firms use third-party test providers; treat any specific format you read about as a report rather than a fact.
The arithmetic foundation is in [Mental Math](02-Mental-Math.md).

### The checklist

Run it in this order; most items fall within the first three steps.

1. **First differences.** Constant means arithmetic; if not constant, take differences again.
   A degree-$k$ polynomial in $n$ has constant $k$-th differences equal to $k!$ times the leading coefficient.
2. **Ratios.** Constant ratio means geometric ($4, 6, 9, 13.5, \dots$ is $\times 1.5$).
   Ratios that increase by one each step suggest factorials ($1, 2, 6, 24, 120$).
3. **Differences that form a known sequence.** Differences $2, 4, 8, 16$ mean $a_{n+1} = 2a_n - c$; differences that are squares or primes mean a cumulative sum.
4. **Interleaving.** Split odd and even positions; two simple rules alternate ($1, 10, 2, 20, 3, 30$).
5. **Known families.** Squares $\pm$ a constant, cubes, triangular numbers $n(n+1)/2$, primes, Fibonacci-like recursions $a_{n} = a_{n-1} + a_{n-2}$.
6. **Digit and representation tricks.** Reversed digits, digit sums, look-and-say, numbers written in another base.

### Difference tables

For $2, 12, 36, 80, 150$:

| Level | Values |
| :--- | :--- |
| Terms | $2, 12, 36, 80, 150$ |
| 1st differences | $10, 24, 44, 70$ |
| 2nd differences | $14, 20, 26$ |
| 3rd differences | $6, 6$ |

Constant third differences mean a cubic; extend from the bottom: 3rd $6$, 2nd $32$, 1st $102$, next term $252$.
The closed form is $n^3 + n^2$, which confirms $6^3 + 6^2 = 252$.

### Numerical reasoning: the recurring calculations

- Percentage change: $(\text{new} - \text{old})/\text{old}$.
- Percentage point versus percent: a rate moving from $4\%$ to $5\%$ is 1 point, or $25\%$.
- Compound average growth over $T$ periods: $(\text{end}/\text{start})^{1/T} - 1$, which is below the arithmetic mean of the yearly rates whenever those rates vary.
- Shares and ratios: part $/$ whole, and ratio changes $A/B$ from separate changes in $A$ and $B$ via $(1+a)/(1+b)$.
- Unit conversions and currency: write the units and cancel them explicitly.

### Time management

- Budget: total time divided by questions, and a hard skip rule (for example, skip anything not solved in twice the budget).
- Answer the quick items first if the test allows navigation; bank marks.
- Guessing: with $k$ options and a penalty $c$ per wrong answer, a blind guess has expected score $1/k - c(1 - 1/k)$.
  Guess whenever this is non-negative, or whenever you can eliminate options.
- Use options to check: estimate first and eliminate impossible choices by magnitude or last digit.
- Scoring rules differ between tests; read the instructions, because whether wrong answers are penalised changes the optimal strategy.

## Worked examples

### Example 1: a cubic by difference table

"Next term: $2, 12, 36, 80, 150, ?$"
First differences $10, 24, 44, 70$; second $14, 20, 26$; third $6, 6$.
Constant third differences, so extend: second difference $32$, first difference $70 + 32 = 102$, next term $150 + 102 = 252$.
Recognise it as $n^3 + n^2 = n^2(n+1)$ to confirm.

### Example 2: three sequences in 30 seconds

- $3, 5, 9, 17, 33, ?$: differences $2, 4, 8, 16$ double, so the rule is $a_{n+1} = 2a_n - 1$ and the answer is $65$.
- $1, 4, 9, 61, 52, 63, ?$: squares with digits reversed ($16 \to 61$, $25 \to 52$, $36 \to 63$), so $49 \to 94$.
- $3, 4, 6, 8, 12, 16, 24, ?$: interleaved; odd positions $3, 6, 12, 24$ and even positions $4, 8, 16$ both double, so $32$.

### Example 3: growth rates in a data table

Revenue is $100$ in year 1, $150$ in year 2 and $120$ in year 3.
Yearly changes are $+50\%$ and $-20\%$, with arithmetic mean $+15\%$.
The compound annual growth rate is $\sqrt{120/100} - 1 \approx 9.5\%$.
A test that asks for "average annual growth" usually wants the compound rate; check the options, because the arithmetic mean is the classic trap answer.

### Example 4: when to guess

A test has 5 options, $+1$ for correct and $-0.25$ for wrong.
A blind guess scores $0.2 - 0.8 \times 0.25 = 0$ in expectation, so it is neutral; eliminating even one option makes guessing positive ($0.25 - 0.75 \times 0.25 \approx 0.06$).
With no penalty, always answer every question before time runs out.

## Pitfalls

- Stopping at first differences and declaring the sequence "random" when second or third differences are constant.
- Forcing a polynomial fit on something that is geometric or recursive; check ratios early.
- Missing interleaving because the sequence "almost" increases smoothly.
- Confusing percentage points with percent, and averaging growth rates arithmetically.
- Spending three minutes on one sequence in a test with 20-second budgets.
- Guessing blindly under a harsh penalty, or leaving blanks when there is none.

## Interview questions

> [!question]- int-seq-pronic | Next term: $2, 6, 12, 20, 30, ?$
> $42$. The terms are $n(n+1)$; equivalently the differences $4, 6, 8, 10$ increase by 2, so the next is $30 + 12$.

> [!question]- int-seq-double-minus-one | Next term: $3, 5, 9, 17, 33, ?$
> $65$. $a_{n+1} = 2a_n - 1$; the differences $2, 4, 8, 16$ double.

> [!question]- int-seq-squares-plus-one | Next term: $2, 5, 10, 17, 26, ?$
> $37$. The terms are $n^2 + 1$; differences $3, 5, 7, 9$ are the odd numbers.

> [!question]- int-seq-reversed-squares | Next term: $1, 4, 9, 61, 52, 63, ?$
> $94$. The squares $1, 4, 9, 16, 25, 36, 49$ with digits reversed.

> [!question]- int-seq-cubic-third-differences | Next term: $2, 12, 36, 80, 150, ?$
> $252$. Third differences are constant at 6; the terms are $n^3 + n^2$.

> [!question]- int-seq-look-and-say | Next term: $1, 11, 21, 1211, 111221, ?$
> $312211$. Each term describes the previous one: "three 1s, two 2s, one 1".

> [!question]- int-seq-alternating-ops | Next term: $7, 10, 8, 11, 9, 12, ?$
> $10$. Alternately add 3 and subtract 2.

> [!question]- int-seq-interleaved-doubling | Next term: $3, 4, 6, 8, 12, 16, 24, ?$
> $32$. Odd positions $3, 6, 12, 24$ and even positions $4, 8, 16$ each double.

> [!question]- int-seq-geometric-one-point-five | Next term: $4, 6, 9, 13.5, ?$
> $20.25$. Constant ratio $1.5$.

> [!question]- int-seq-factorials | Next term: $1, 2, 6, 24, 120, ?$
> $720$. Factorials; successive ratios are $2, 3, 4, 5$, so multiply by 6.

> [!question]- int-seq-cagr-trap | Revenue goes $100 \to 150 \to 120$. Average annual growth?
> About $9.5\%$ compound, $\sqrt{1.2} - 1$. The arithmetic mean of $+50\%$ and $-20\%$ ($15\%$) overstates it because growth compounds.

> [!question]- int-seq-percent-vs-points | A default rate rises from $4\%$ to $5\%$. By how much has it increased?
> 1 percentage point, which is a $25\%$ relative increase. Tests often offer both to catch the confusion.

> [!question]- int-seq-guessing-penalty | Five options, $+1$ right and $-0.25$ wrong. Should you guess blind?
> It is neutral: expected score $0.2 - 0.8 \times 0.25 = 0$. Eliminate one option and guessing becomes positive.

## Further reading

- The On-Line Encyclopedia of Integer Sequences: https://oeis.org/ (look up any sequence you could not crack, then learn its rule).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008).
- [Mental Math](02-Mental-Math.md) and [Brainteasers and Puzzles](03-Brainteasers-and-Puzzles.md).
