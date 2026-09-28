---
type: problem-set
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [classic-expectation-problems, martingales-and-optional-stopping]
est_hours: 10
sources: [Zhou - A Practical Guide to Quantitative Finance Interviews, Crack - Heard on the Street, Joshi Denson and Downes - Quant Job Interview Questions and Answers, Mosteller - Fifty Challenging Problems in Probability, Blitzstein and Hwang - Introduction to Probability (2nd ed.), Winkler - Mathematical Puzzles - A Connoisseur's Collection]
---

# Probability Problem Set

## TL;DR

- Name the tool before computing: symmetry, complement, indicators, conditioning on the first step, a martingale, or a picture.
- Say a quick bound or limiting case first (for example "it must be below $1/2$ because..."), then compute, then check the answer against the bound.
- Most traps are conditioning traps: the information you are given, and how you came to know it, defines the sample space.
- For waiting times, write the state machine; for "which comes first", write first-step equations; for "fair game", reach for optional stopping.
- Aim for under five minutes per easy and medium card, with the reasoning spoken aloud.

## Learning objectives

- Solve mixed probability questions under time pressure, speaking the reasoning aloud.
- Sanity-check every answer with a bound, a symmetry or a limiting case.
- Reach interview speed: most questions in under five minutes, hard classics in under fifteen.
- Recognise which technique a question is testing from its wording.

## Core concepts

This note is a drill set; the theory lives in the topic notes linked below.
The toolkit, with the signal in the question that should trigger each technique:

| Technique | Signal in the question | Example card |
| :--- | :--- | :--- |
| Complement | "at least one" | `prob-ps-at-least-one-six-two-dice` |
| Symmetry and exchangeability | identical items, "which is first", random order | `prob-ps-airplane-seat` |
| Indicators and linearity | "expected number of ..." | `prob-ps-deck-red-then-black` |
| Tail sum $E[N] = \sum P(N > n)$ | "expected number of draws until ..." | `prob-ps-rolls-until-repeat-face` |
| Bayes with a table of counts | "given that ...", tests, coins | `prob-ps-disease-test-bayes` |
| First-step analysis | games, patterns, "who wins" | `prob-ps-alternating-first-head` |
| Martingales and optional stopping | fair games, hitting probabilities | `prob-ps-fair-walk-exit-time` |
| Geometry (area ratios) | continuous uniforms, sticks, circles | `prob-ps-three-uniform-lengths-triangle` |
| Memorylessness | exponential lifetimes, Poisson arrivals | `prob-ps-exponential-remaining-life` |
| Bijection or relabelling | counts that look hard to enumerate | `prob-ps-n-plus-one-coins` |

Topic notes: [Counting](01-Counting-and-Combinatorics.md), [Bayes](02-Conditional-Probability-and-Bayes.md), [Expectation](04-Expectation-Variance-and-Linearity.md), [Order statistics](08-Order-Statistics-and-Extremes.md), [Geometric probability](09-Geometric-Probability.md), [Markov chains](10-Markov-Chains.md), [Random walks](11-Random-Walks-and-Gamblers-Ruin.md), [Martingales](12-Martingales-and-Optional-Stopping.md), [Poisson processes](13-Poisson-Processes.md), [Classic expectation problems](14-Classic-Expectation-Problems.md).

## Worked examples

### The lost boarding pass (airplane seat)

"100 passengers board in order; the first has lost his pass and sits in a uniformly random seat. Everyone else takes their own seat if free, otherwise a uniformly random free seat. Probability the last passenger gets her own seat?"
"Key observation: whenever someone chooses randomly, seat 1 and seat 100 are both still free and equally likely to be chosen."
"The process ends, as far as the last passenger is concerned, the first time a random chooser picks seat 1 or seat 100: seat 1 resolves everything (all later passengers find their seats), seat 100 dooms her."
"Picks of other seats just pass the problem to another random chooser, and by symmetry seat 1 and seat 100 are equally likely to be the first of the two picked."
"So the answer is $1/2$, independent of $n \ge 2$; bonus: passenger $k$ gets his own seat with probability $(n-k+1)/(n-k+2)$ for $k \ge 2$."

### 100 prisoners and 100 boxes

"Each prisoner may open 50 of 100 boxes to find his own number; all must succeed; no communication after the start. Random guessing succeeds with probability $2^{-100}$."
"Strategy: prisoner $i$ opens box $i$, then the box whose number he found, and so on. He follows the cycle of the permutation that contains $i$ and succeeds iff that cycle has length at most 50."
"So everyone succeeds iff the random permutation has no cycle longer than 50."
"For $k > 50$ there can be at most one cycle of length $k$, and the number of permutations with a given $k$-cycle is $\binom{100}{k}(k-1)!\,(100-k)! = 100!/k$, so $P(\text{a } k\text{-cycle}) = 1/k$."
"Failure probability $\sum_{k=51}^{100} 1/k = H_{100} - H_{50} \approx 0.688$, success about $0.312$, tending to $1 - \ln 2 \approx 0.307$."
"The point: the strategy makes the prisoners' successes perfectly correlated, not individually better; each still succeeds with probability $1/2$."

### Rolls until a six, given all rolls were even

"Roll a die until the first six. Given that every roll was even, what is the expected number of rolls?"
"Tempting answer: the conditioning makes it a three-sided die $\{2, 4, 6\}$, so 3. That is wrong."
"Correct framing: the conditioning event is 'no odd number appears before the first 6'. Equivalently, roll until the first outcome in $\{1, 3, 5, 6\}$ and condition on it being 6."
"The time $T$ to hit $\{1, 3, 5, 6\}$ is geometric with success probability $2/3$, and which of the four values ends it is independent of $T$."
"So conditioning on the stopping value being 6 does not change $T$: $E[T] = 3/2$."
"Sanity check: conditioning on all-even strongly favours short sequences, since long sequences are unlikely to avoid odds, so the answer should be well below 3."

### Boy born on a Tuesday

"A family has two children; you learn that at least one is a boy born on a Tuesday. Probability both are boys? Assume sexes and weekdays are uniform and independent, and that the information was generated by asking 'is there a boy born on Tuesday?'."
"Each child is one of 14 equally likely (sex, day) types, giving $196$ ordered pairs."
"Pairs with at least one Tuesday boy: $196 - 13^2 = 27$."
"Of those, both boys: $7^2 - 6^2 = 13$ (boy-boy pairs minus those with no Tuesday boy)."
"So $13/27$, between the $1/3$ of 'at least one boy' and the $1/2$ of 'this particular child is a boy'; the more specific the information, the closer it gets to identifying one child."
"The senior point is the protocol caveat: if the parent volunteered a random child's description, the answer is $1/2$."

### A tosses n+1 coins, B tosses n

"A flips $n+1$ fair coins, B flips $n$. Probability A gets more heads?"
"A has one extra coin, so $H_A + T_A = H_B + T_B + 1$. Therefore exactly one of '$H_A > H_B$' and '$T_A > T_B$' holds."
"Swapping heads and tails is a symmetry, so each has probability $1/2$."
"The answer is $1/2$ for every $n$, with no binomial sums needed."

### Both positive in a correlated normal pair

"$(X, Y)$ is standard bivariate normal with correlation $\rho$. Find $P(X > 0, Y > 0)$."
"Write $X = Z_1$, $Y = \rho Z_1 + \sqrt{1-\rho^2} Z_2$ with $(Z_1, Z_2)$ rotationally symmetric."
"Each condition is a half-plane through the origin in the $Z$-plane, and the intersection is a wedge with angle $\pi/2 + \arcsin\rho$."
"By rotational symmetry the probability is the angle over $2\pi$: $1/4 + \arcsin(\rho)/(2\pi)$."
"Checks: $\rho = 0$ gives $1/4$, $\rho = 1$ gives $1/2$, $\rho = -1$ gives 0; for $\rho = 1/2$ it is $1/3$."

## Pitfalls

- Answering before fixing the sample space in conditioning puzzles; say how the information was obtained.
- Replacing a conditional process by a naive "restricted die" (the even-rolls trap).
- Multiplying probabilities of dependent events, or adding probabilities of overlapping events.
- Skipping the sanity check: every probability must lie in $[0, 1]$, and limiting cases ($n = 1$, $\rho = 0$, $p = 1/2$) should reproduce known answers.
- Spending minutes on algebra when a symmetry kills the problem; ask "what is exchangeable here?" first.

## Interview questions

### Counting and basic probability

> [!question]- prob-ps-at-least-one-six-two-dice | Two fair dice are rolled. Probability at least one shows a six?
> $11/36$. Complement: $1 - (5/6)^2 = 1 - 25/36$.

> [!question]- prob-ps-sum-three-dice-ten | Three fair dice. Probability the sum is 10?
> $1/8$. There are 27 of the 216 outcomes; by symmetry 10 and 11 are the two modal sums.

> [!question]- prob-ps-three-hearts | Three cards are drawn without replacement. Probability all are hearts?
> $11/850 \approx 0.0129$. $\frac{13}{52}\cdot\frac{12}{51}\cdot\frac{11}{50}$.

> [!question]- prob-ps-four-different-suits | Four cards are drawn. Probability they are all different suits?
> $2197/20825 \approx 0.105$. $13^4/\binom{52}{4}$, or $1 \cdot \frac{39}{51}\cdot\frac{26}{50}\cdot\frac{13}{49}$.

> [!question]- prob-ps-full-house | Probability a five-card poker hand is a full house?
> $6/4165 \approx 0.00144$. $13\binom43 \cdot 12\binom42 = 3744$ hands out of $\binom{52}{5} = 2{,}598{,}960$.

> [!question]- prob-ps-de-mere | Which is more likely: at least one six in 4 rolls of a die, or at least one double six in 24 rolls of two dice?
> The first: $1 - (5/6)^4 \approx 0.518$ versus $1 - (35/36)^{24} \approx 0.491$.

> [!question]- prob-ps-exactly-fifty-heads | 100 fair coin flips. Probability of exactly 50 heads?
> About $0.0796$. $\binom{100}{50}/2^{100}$; Stirling gives $1/\sqrt{50\pi} \approx 0.0798$.

### Conditional probability and Bayes

> [!question]- prob-ps-boy-girl | A family has two children and at least one is a boy. Probability both are boys?
> $1/3$. Of BB, BG, GB, GG, the condition removes GG, leaving one of three equally likely cases.

> [!question]- prob-ps-monty-hall | Monty Hall: you pick a door, the host (who knows) opens a different door with a goat and offers a switch. Should you switch?
> Yes: switching wins $2/3$. Your first pick is right with probability $1/3$ and the host's action never changes that.

> [!question]- prob-ps-disease-test-bayes | Prevalence 1%, test sensitivity 99% and specificity 99%. Probability of disease given a positive test?
> $1/2$. Per 10,000 people: 99 true positives and 99 false positives.

> [!question]- prob-ps-double-headed-coin | One of two coins is double-headed. You pick one at random and get three heads. Probability it is the double-headed coin?
> $8/9$. Odds prior $1:1$ times likelihood ratio $1 : 1/8$ gives $8:1$.

> [!question]- prob-ps-two-aces-given-one | Two cards are dealt. Given at least one is an ace, probability both are aces? Given one is the ace of spades?
> $1/33$ and $1/17$. $\binom42/(\binom{52}{2} - \binom{48}{2}) = 6/198$; with the ace of spades known, the other card is an ace with probability $3/51$.

> [!question]- prob-ps-revolver-spin | A revolver has 6 chambers with 2 adjacent bullets. After spinning, the first shot is empty. Better to spin again or fire?
> Fire without spinning: survive $3/4$ versus $2/3$. Of the 4 empty chambers, 3 are followed by an empty chamber.

> [!question]- prob-ps-laplace-rule | A coin has unknown bias with a uniform prior. After $k$ heads in $n$ flips, probability the next flip is heads?
> $(k+1)/(n+2)$. The posterior is $\text{Beta}(k+1, n-k+1)$ and its mean is the predictive probability.

> [!question]- prob-ps-tuesday-boy | Two children; at least one is a boy born on a Tuesday. Probability both are boys?
> $13/27$. Of 196 equally likely (sex, day) pairs, 27 contain a Tuesday boy, of which 13 are boy-boy. Depends on how the information was obtained.

### Expectation and linearity

> [!question]- prob-ps-die-squared | Expected value of the square of a fair die roll?
> $91/6 \approx 15.17$. $(1 + 4 + 9 + 16 + 25 + 36)/6$; note it exceeds $3.5^2$ by the variance $35/12$.

> [!question]- prob-ps-variance-hundred-dice | Variance of the sum of 100 fair dice?
> $3500/12 \approx 291.7$. Independent, so $100 \times 35/12$; standard deviation about $17.1$.

> [!question]- prob-ps-flips-until-both-faces | Expected fair-coin flips until you have seen both heads and tails?
> $3$. The first flip gives one face, then wait a geometric(1/2) time, mean 2, for the other.

> [!question]- prob-ps-expected-runs | Expected number of runs in 10 fair coin flips (HHTHT has 4 runs)?
> $5.5$. One run plus an indicator for each of the 9 adjacent pairs that differ, each with probability $1/2$.

> [!question]- prob-ps-deck-red-then-black | In a shuffled deck, expected number of positions where a red card is immediately followed by a black card?
> $13$. 51 adjacent pairs, each red-then-black with probability $\frac{26}{52}\cdot\frac{26}{51}$.

> [!question]- prob-ps-rolls-until-repeat-face | Expected number of die rolls until some face repeats?
> $1223/324 \approx 3.77$. Tail sum over $P(\text{first } n \text{ distinct}) = \prod_{j<n}(6-j)/6$ for $n = 0, \dots, 6$.

> [!question]- prob-ps-von-neumann-fair-coin | How do you get a fair bit from a coin with unknown bias $p$, and how many flips does it take on average?
> Flip pairs; HT means 0, TH means 1, otherwise repeat. Each pair succeeds with probability $2pq$, so $1/(pq)$ flips on average.

### Continuous distributions and geometry

> [!question]- prob-ps-max-three-uniforms-tail | Three i.i.d. uniforms. Probability the maximum exceeds $0.9$?
> $0.271$. $1 - 0.9^3$.

> [!question]- prob-ps-sum-two-uniforms-tail | $X, Y$ i.i.d. $U(0,1)$. Probability $X + Y > 1.5$?
> $1/8$. The corner triangle with legs $1/2$.

> [!question]- prob-ps-exponential-remaining-life | A component's lifetime is exponential with mean 3 years and it has lasted 2 years. Expected remaining life?
> $3$ years. Memorylessness: the residual life is again exponential with mean 3.

> [!question]- prob-ps-piece-containing-midpoint | A stick is broken at a uniform point. Expected length of the piece containing the midpoint?
> $3/4$. It is $\max(U, 1-U)$, uniform on $[1/2, 1]$; larger than $1/2$ because long pieces are more likely to cover a fixed point.

> [!question]- prob-ps-correlation-x-and-sum | $X, Y$ i.i.d. with finite variance. Correlation of $X$ and $X + Y$?
> $1/\sqrt2$. $\operatorname{Cov} = \operatorname{Var}(X)$ and $\operatorname{sd}(X+Y) = \sqrt2\,\operatorname{sd}(X)$.

> [!question]- prob-ps-symmetric-conditional-mean | $X, Y$ i.i.d. with finite mean. What is $E[X \mid X + Y = s]$?
> $s/2$. By symmetry $E[X \mid S] = E[Y \mid S]$ and they sum to $s$.

> [!question]- prob-ps-half-normal-mean | $Z \sim N(0,1)$. What is $E[Z \mid Z > 0]$?
> $\sqrt{2/\pi} \approx 0.798$. $E[Z\mathbf{1}_{Z>0}] = \phi(0) = 1/\sqrt{2\pi}$, divided by $1/2$.

> [!question]- prob-ps-max-two-normals | $Z_1, Z_2$ i.i.d. $N(0,1)$. What is $E[\max(Z_1, Z_2)]$?
> $1/\sqrt\pi \approx 0.564$. $\max = \frac{Z_1 + Z_2}{2} + \frac{|Z_1 - Z_2|}{2}$ and $Z_1 - Z_2 \sim N(0, 2)$ has $E|\cdot| = 2/\sqrt\pi$.

> [!question]- prob-ps-three-uniform-lengths-triangle | Three lengths are i.i.d. $U(0,1)$. Probability they form a triangle?
> $1/2$. Fails iff one exceeds the sum of the other two; $P(X > Y + Z) = 1/6$ (simplex volume), and the three events are disjoint.

> [!question]- prob-ps-bivariate-orthant | $(X,Y)$ standard bivariate normal with correlation $1/2$. Probability both are positive?
> $1/3$. In general $1/4 + \arcsin(\rho)/(2\pi)$, the angle of a wedge over $2\pi$.

### Markov chains, random walks and martingales

> [!question]- prob-ps-alternating-first-head | A and B alternate flipping a fair coin, A first; the first head wins. Probability A wins?
> $2/3$. $p = 1/2 + \frac14 p$, since after two tails the game restarts.

> [!question]- prob-ps-first-to-roll-six | A and B alternate rolling a die, A first; the first six wins. Probability A wins?
> $6/11$. $p = 1/6 + (5/6)^2 p$.

> [!question]- prob-ps-walk-returns-at-four | A fair $\pm 1$ walk starts at 0. Probability it is at 0 after 4 steps?
> $3/8$. $\binom42/2^4 = 6/16$.

> [!question]- prob-ps-fair-walk-exit-time | A fair walk starts at 3 with absorbing barriers 0 and 10. Probability of hitting 10, and expected duration?
> $3/10$ and $21$. Optional stopping on $S_n$ and on $S_n^2 - n$ gives $i/N$ and $i(N-i)$.

> [!question]- prob-ps-biased-walk-plus-two | A walk moves up with probability $0.6$. Probability it hits $+2$ before $-2$ from 0?
> $9/13$. With $r = q/p = 2/3$, $h = (1 - r^2)/(1 - r^4) = 1/(1 + r^2)$.

> [!question]- prob-ps-hth-before-hht | A fair coin is flipped until HTH or HHT appears. Probability HTH comes first?
> $1/3$. From H: HH leads to HHT surely (any later T completes it), and HT then H wins for HTH; first-step gives $a_H = \frac12 a_{HT}$, $a_{HT} = \frac12 + \frac12 a_H$.

> [!question]- prob-ps-expected-hthh-waiting | Expected fair-coin flips until HTHH?
> $18$. Prefixes that are also suffixes: HTHH ($16$) and H ($2$).

### Poisson processes and waiting times

> [!question]- prob-ps-poisson-both-in-first-half | A Poisson process has exactly 2 events in $[0, 1]$. Probability both occurred before $1/2$?
> $1/4$. Given the count, the event times are i.i.d. uniform.

> [!question]- prob-ps-poisson-three-events | Trades arrive as Poisson with rate 2 per minute. Probability of exactly 3 trades in a minute?
> $e^{-2}\,2^3/3! \approx 0.180$.

> [!question]- prob-ps-poisson-quiet-period | Market orders arrive at 10 per second. Probability of a gap longer than 0.5 seconds starting now?
> $e^{-5} \approx 0.0067$. The wait to the next arrival is $\text{Exp}(10)$ from any fixed time.

### Hard classics

> [!question]- prob-ps-n-plus-one-coins | A flips $n+1$ fair coins, B flips $n$. Probability A has more heads?
> $1/2$. Exactly one of "A has more heads" and "A has more tails" holds, and they are symmetric.

> [!question]- prob-ps-rolls-until-six-given-even | Roll a die until the first six. Given all rolls were even, expected number of rolls?
> $3/2$, not 3. It is the time to first hit $\{1,3,5,6\}$ (geometric with $p = 2/3$) conditioned on the stopping value being 6, which is independent of the time.

> [!question]- prob-ps-airplane-seat | 100 passengers; the first sits randomly, the rest take their seat or a random free one. Probability the last passenger gets her seat?
> $1/2$. The first random choice of seat 1 or seat 100 decides it, and the two are symmetric.

> [!question]- prob-ps-hundred-prisoners | 100 prisoners each open 50 of 100 boxes to find their number, all must succeed. Best success probability?
> About $0.312$ with the cycle-following strategy: succeed iff no cycle exceeds 50, and $P = 1 - \sum_{k=51}^{100} 1/k$.

> [!question]- prob-ps-uniforms-first-decrease | Draw uniforms until one is smaller than its predecessor. Expected number of draws?
> $e$. The first $n$ draws are increasing with probability $1/n!$, so $E[N] = \sum_{n \ge 0} P(N > n) = \sum 1/n!$.

> [!question]- prob-ps-sphere-four-points | Four uniform points on a sphere. Probability the tetrahedron contains the centre?
> $1/8$. Pair each of three points with its antipode; exactly one of the 8 sign choices contains the centre, whatever the fourth point is.

> [!question]- prob-ps-closer-to-centre | Uniform point in the unit square. Probability it is closer to the centre than to the boundary?
> $(4\sqrt2 - 5)/3 \approx 0.219$. In one eighth of the square the region is bounded by the parabola $x = 1/4 - y^2$; integrate to $y = (\sqrt2 - 1)/2$ and multiply by 8.

## Further reading

- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapters 2 and 4.
- Timothy Crack, *Heard on the Street: Quantitative Questions from Wall Street Job Interviews*.
- Joshi, Denson and Downes, *Quant Job Interview Questions and Answers*, probability chapter.
- Frederick Mosteller, *Fifty Challenging Problems in Probability*.
- Peter Winkler, *Mathematical Puzzles: A Connoisseur's Collection* (airplane seat, prisoners and boxes).
