---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: []
est_hours: 5
sources: [Arthur Benjamin and Michael Shermer - Secrets of Mental Math (2006), Zetamac arithmetic game default settings - https://arithmetic.zetamac.com/, Xinfeng Zhou - A Practical Guide to Quantitative Finance Interviews (2008)]
---

# Mental Math

## TL;DR

- Speed comes from a small set of reflexes: complements to round numbers, $(a+b)(a-b)=a^2-b^2$, squaring near a base, and a memorised fraction table.
- Always anchor on the nearest easy number and correct: $68 \times 72 = 70^2 - 2^2 = 4896$, $96^2 = 92 \times 100 + 4^2 = 9216$.
- Percentages are fractions in disguise, and $x\%$ of $y$ equals $y\%$ of $x$.
- Estimate first, then compute; the estimate catches order-of-magnitude slips and tells you how many digits you need.
- Relative errors add under multiplication and division, so round factors in opposite directions.
- Practise daily with `./qp drill arith` and `./qp drill optiver`, and track scores; accuracy first, then speed.

## Learning objectives

- Multiply two-digit numbers, divide and convert fractions to decimals quickly.
- Use anchoring, rounding-and-correcting, and percentage tricks.
- Hit a Zetamac-style score of 40+ and finish an 80-question, 8-minute test.
- Practise daily with `qp drill arith` and `qp drill optiver`.

## Core concepts

### Why it is tested

Trading desks price things in seconds, and a candidate who stalls on $7 \times 13$ cannot think about edge, position and risk at the same time.
Mental arithmetic appears in timed numerical tests, in phone screens and inside trading games, where the arithmetic is the overhead and the decision is what is being scored.
The goal is to make arithmetic cost so little attention that the remaining attention goes to the problem.

### Addition and subtraction: complements and left-to-right

- Add left to right: $67 + 58 = 67 + 50 + 8 = 117 + 8 = 125$.
- Round and correct: $67 + 58 = 67 + 60 - 2 = 125$.
- Complement to a power of ten: take every digit from 9 and the last non-zero digit from 10.
  $1000 - 387 = 613$ because $9-3=6$, $9-8=1$, $10-7=3$.
- Subtraction as "counting up": $1000 - 387$ is $13$ to reach $400$ plus $600$, so $613$.
- Change-making in P&L: selling at $101.25$ what you bought at $98.70$ gains $1.30$ to reach $100$ plus $1.25$, so $2.55$.

### Multiplication

- **Distribute on the easy part.** $7 \times 86 = 7 \times 80 + 7 \times 6 = 560 + 42 = 602$.
- **Difference of squares.** When two numbers are symmetric about an easy midpoint, $(m+d)(m-d) = m^2 - d^2$.
  $47 \times 53 = 50^2 - 3^2 = 2491$ and $998 \times 1002 = 10^6 - 4 = 999996$.
- **Squaring near a base.** $n^2 = (n+d)(n-d) + d^2$; pick $d$ so that one factor is round.
  $57^2 = 64 \times 50 + 7^2 = 3200 + 49 = 3249$.
  Near 100: $96^2 = (96 - 4) \times 100 + 16 = 9216$ and $104^2 = 108 \times 100 + 16 = 10816$.
- **Squares ending in 5.** $(10a+5)^2 = 100a(a+1) + 25$, so $65^2 = 4225$ (from $6 \times 7 = 42$).
- **Same tens, units summing to 10.** $(10a+b)(10a+10-b) = 100a(a+1) + b(10-b)$, so $43 \times 47 = 2021$ and $37 \times 33 = 1221$.
- **Cross multiplication (vertical and crosswise).** For $ab \times cd$: units $b d$, tens $a d + b c$, hundreds $a c$, carrying left.
  $34 \times 26$: units $24$ (write 4 carry 2), tens $3 \cdot 6 + 4 \cdot 2 + 2 = 28$ (write 8 carry 2), hundreds $3 \cdot 2 + 2 = 8$, giving $884$.
  Check: $30^2 - 4^2 = 884$.
- **Halve and double.** $125 \times 48 = 1000 \times 6 = 6000$ because $125 = 1000/8$.
  $25 \times k = 100k/4$ and $5 \times k = 10k/2$.

### Division and fractions

Division is multiplication by a reciprocal, so memorising reciprocals turns most divisions into one multiplication.

| Fraction | Decimal | Fraction | Decimal |
| :--- | :--- | :--- | :--- |
| $1/2$ | $0.5$ | $1/9$ | $0.\overline{1}$ |
| $1/3$ | $0.\overline{3}$ | $1/11$ | $0.\overline{09}$ |
| $1/4$ | $0.25$ | $1/12$ | $0.08\overline{3}$ |
| $1/5$ | $0.2$ | $1/13$ | $0.\overline{076923}$ |
| $1/6$ | $0.1\overline{6}$ | $1/16$ | $0.0625$ |
| $1/7$ | $0.\overline{142857}$ | $1/20$ | $0.05$ |
| $1/8$ | $0.125$ | $1/40$ | $0.025$ |

- Multiples follow: $3/8 = 0.375$, $5/8 = 0.625$, $7/8 = 0.875$, $3/16 = 0.1875$, $7/16 = 0.4375$.
- Sevenths cycle through the same digits: $2/7 = 0.285714...$, $3/7 = 0.428571...$
- $n/9$ repeats the digit $n$; $n/99$ repeats the two-digit block $n$ ($17/99 = 0.1717...$).
- Scale to a friendly denominator: $17/40 = 42.5/100 = 0.425$.
- Decimal divisors: multiply both sides by the same power of ten, so $3.6 / 0.12 = 360 / 12 = 30$.

### Percentages

- $x\%$ of $y$ equals $y\%$ of $x$: $16\%$ of $25$ is $25\%$ of $16 = 4$.
- $12.5\% = 1/8$, $37.5\% = 3/8$, $62.5\% = 5/8$, $87.5\% = 7/8$, $16.7\% \approx 1/6$, $33.3\% \approx 1/3$.
- Build from $10\%$ and $1\%$: $15\%$ of $360 = 36 + 18 = 54$.
- Successive changes multiply: $+20\%$ then $-20\%$ is $1.2 \times 0.8 = 0.96$, a $4\%$ loss.
- A fall of $p$ needs a rise of $p/(1-p)$ to recover: $-20\%$ needs $+25\%$, $-50\%$ needs $+100\%$.
- Rule of 72: money at $r\%$ doubles in about $72/r$ periods ($1.07^{10} \approx 1.967$).

### Estimation and error control

- Estimate before computing, so you know the magnitude and how many digits matter.
- Relative errors add under multiplication and division: rounding one factor up $2\%$ and another down $2\%$ nearly cancels.
- $\pi \times 27.3$: $3 \times 27.3 = 81.9$, plus $0.14 \times 27.3 \approx 3.82$, so about $85.7$ (exact $85.77$).
- Square roots by linearisation: $\sqrt{a^2 + e} \approx a + e/(2a)$, so $\sqrt{50} \approx 7 + 1/14 \approx 7.07$.
- Last-digit and casting-out-nines checks catch most slips: the digit sum of a product is congruent mod 9 to the product of the digit sums.

### Practice regimen

The repo's drills generate problems in the formats interviews commonly use.

- `./qp drill arith` uses Zetamac default rules: 120 seconds of $a+b$ with $a,b \in [2,100]$, the matching subtractions, $a \times b$ with $a \in [2,12]$ and $b \in [2,100]$, and the matching divisions.
- `./qp drill optiver` is 80 mixed questions in 8 minutes (6 seconds each on average): two-digit products, decimals, percentages, fraction-to-decimal conversions and fraction arithmetic.
- `./qp drill mm` is the market-making dice game; it trains arithmetic under the load of quoting and tracking a position (see [Trading Games in Interviews](05-Trading-Games-in-Interviews.md)).

A regimen that works for most people:

1. Weeks 1-2: 15 minutes a day; three `arith` runs and one `optiver` run, then review every miss and add the underlying fact to a flash list.
2. Weeks 3-4: add the square and reciprocal tables until recall is instant; aim for zero errors before chasing speed.
3. Ongoing: one `mm` game a day, saying bid, ask, position and fair value aloud.

Personal targets, set as goals rather than as any firm's cut-off: 40+ on the Zetamac-style sprint as a floor, 60+ as a comfortable level, and completing all 80 `optiver` questions with at most 2 or 3 errors.
Firms do not publish thresholds, and figures quoted on forums vary; treat them as anecdotes.

## Worked examples

### Example 1: $68 \times 72$ and $57 \times 63$ in one breath

Both pairs straddle a round midpoint.
$68 \times 72 = 70^2 - 2^2 = 4900 - 4 = 4896$.
$57 \times 63 = 60^2 - 3^2 = 3600 - 9 = 3591$.
Say the midpoint first; the correction is always subtracted and is a small square.

### Example 2: position value on a numerical test

"You hold 48 contracts at 12.5% of 640 each; what is the position worth?"
$12.5\%$ of $640$ is $640/8 = 80$.
$48 \times 80 = 3840$.
Check the magnitude: about $50 \times 80 = 4000$, slightly less, consistent.

### Example 3: converting $17/40$ and $7/16$, then combining

$17/40$: scale by $2.5$ to get $42.5/100 = 0.425$.
$7/16 = 7 \times 0.0625 = 0.4375$.
Sum: $0.425 + 0.4375 = 0.8625$.
As a fraction check, $17/40 + 7/16 = 68/160 + 70/160 = 138/160 = 0.8625$.

### Example 4: squaring and chaining under time pressure

"What is $96^2 - 4^2$?"
Do not compute $96^2$; factor: $(96-4)(96+4) = 92 \times 100 = 9200$.
Before computing, ask whether an identity removes work; that habit saves more time than raw speed.

### Example 5: estimate with error control

"Roughly, $3.14159 \times 27.3$."
Round $\pi$ down to $3$; since $\pi/3 \approx 1.047$, the product $81.9$ is about $4.7\%$ too low.
Add $4.7\%$ of $82 \approx 3.85$ for about $85.75$.
The exact value is $85.77$, so the estimate is within $0.03\%$.

## Pitfalls

- Chasing speed before accuracy; most timed tests and all trading games punish errors more than slowness.
- Computing exactly when the question only needs a comparison or an order of magnitude.
- Losing the decimal point in decimal division; clear decimals by scaling both numbers first.
- Treating $+x\%$ and $-x\%$ as cancelling.
- Misremembering $1/7$ or $1/12$; drill the table until it is reflexive.
- Skipping the sanity check (magnitude, last digit, parity) because the answer "felt right".
- Freezing on a hard item in a fixed-length test; skip, bank the easy ones and return.

## Interview questions

> [!question]- int-math-product-47-53 | Compute $47 \times 53$ mentally.
> $2491$. The numbers straddle $50$, so $50^2 - 3^2 = 2500 - 9 = 2491$.

> [!question]- int-math-square-96 | Compute $96^2$.
> $9216$. $96^2 = (96-4)(96+4) + 4^2 = 92 \times 100 + 16 = 9216$.

> [!question]- int-math-square-65 | Compute $65^2$.
> $4225$. For a number ending in 5, multiply the tens digit by its successor ($6 \times 7 = 42$) and append 25.

> [!question]- int-math-same-tens-43-47 | Compute $43 \times 47$.
> $2021$. Same tens digit and units summing to 10: $4 \times 5 = 20$ followed by $3 \times 7 = 21$.

> [!question]- int-math-998-times-1002 | Compute $998 \times 1002$.
> $999996$. $(1000-2)(1000+2) = 10^6 - 4$.

> [!question]- int-math-seven-sixteenths | Write $7/16$ as a decimal.
> $0.4375$. $1/16 = 0.0625$ and $7 \times 0.0625 = 0.4375$.

> [!question]- int-math-one-seventh-cycle | Write $3/7$ as a decimal to six places.
> $0.428571$. Every $k/7$ is a rotation of the cycle $142857$; $3/7$ starts at the digit 4.

> [!question]- int-math-up-down-twenty-percent | A price rises $20\%$ then falls $20\%$. Net change?
> $-4\%$. The factors multiply: $1.2 \times 0.8 = 0.96$.

> [!question]- int-math-recover-from-drawdown | After a $20\%$ loss, what gain restores the starting value?
> $25\%$. You need $1/(1-0.2) = 1.25$; in general a loss $p$ needs a gain $p/(1-p)$.

> [!question]- int-math-percent-swap | What is $16\%$ of $25$?
> $4$. $x\%$ of $y$ equals $y\%$ of $x$, and $25\%$ of $16$ is $4$.

> [!question]- int-math-rule-of-72 | Roughly how long does money take to double at $6\%$ a year?
> About 12 years. Rule of 72: $72/6 = 12$; the exact figure is $\ln 2 / \ln 1.06 \approx 11.9$.

> [!question]- int-math-sqrt-50 | Estimate $\sqrt{50}$ to two decimals.
> About $7.07$. $\sqrt{49 + 1} \approx 7 + 1/(2 \cdot 7) = 7.071$; the true value is $7.0711$.

> [!question]- int-math-cross-multiply-34-26 | Compute $34 \times 26$ and verify it a second way.
> $884$. Cross multiplication: units $4 \cdot 6 = 24$, tens $3 \cdot 6 + 4 \cdot 2 + 2 = 28$, hundreds $3 \cdot 2 + 2 = 8$; check with $30^2 - 4^2 = 884$.

> [!question]- int-math-125-times-48 | Compute $125 \times 48$.
> $6000$. $125 = 1000/8$, so $125 \times 48 = 1000 \times 6$.

## Further reading

- Arthur Benjamin and Michael Shermer, *Secrets of Mental Math* (2006): the standard reference for left-to-right methods and squaring tricks.
- Zetamac arithmetic game: https://arithmetic.zetamac.com/ (the public tool `./qp drill arith` mirrors).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews* (2008), for how arithmetic appears inside interview problems.
- [Sequences and Numerical Reasoning Tests](06-Sequences-and-Numerical-Reasoning.md) and [Estimation and Fermi Problems](04-Estimation-and-Fermi-Problems.md).
