---
type: concept
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [counting-and-combinatorics]
est_hours: 4
sources: [Blitzstein and Hwang - Introduction to Probability 2nd ed ch 2, Zhou - A Practical Guide to Quantitative Finance Interviews ch 4, Mosteller - Fifty Challenging Problems in Probability, Jaynes - Probability Theory The Logic of Science ch 4]
---

# Conditional Probability and Bayes

## TL;DR

- $P(A\mid B) = P(A\cap B)/P(B)$; conditioning shrinks the sample space to $B$ and renormalises.
- Law of total probability: $P(B) = \sum_i P(B\mid A_i)P(A_i)$ over a partition; Bayes: $P(A_i\mid B) \propto P(B\mid A_i)P(A_i)$.
- Odds form is what you should compute in your head: posterior odds = prior odds $\times$ likelihood ratio, and independent evidence multiplies (log-odds add).
- Rare events dominate: a 99%-sensitive, 95%-specific test for a 1-in-1000 condition gives only about 2% posterior probability.
- Independence and conditional independence are different properties; neither implies the other.
- In Monty Hall, boy-girl and similar puzzles, the answer depends on how the information was generated, so state the protocol before computing.

## Learning objectives

- Apply the law of total probability and Bayes' rule quickly and correctly.
- Distinguish independence from conditional independence.
- Resolve the classic traps: Monty Hall, boy-girl, false positives on rare events.
- Update beliefs sequentially and explain it aloud as a trader would.

## Core concepts

### Definition and multiplication rule

For $P(B) > 0$, $P(A\mid B) = P(A\cap B)/P(B)$.
Rearranged, $P(A_1\cap\dots\cap A_n) = P(A_1)P(A_2\mid A_1)\cdots P(A_n\mid A_1,\dots,A_{n-1})$, which is how sequential card and urn problems are solved (see Example 5 in [Counting and Combinatorics](01-Counting-and-Combinatorics.md)).

### Law of total probability and Bayes

If $A_1,\dots,A_n$ partition $\Omega$,

$$
P(B) = \sum_{i} P(B\mid A_i)P(A_i), \qquad
P(A_j\mid B) = \frac{P(B\mid A_j)P(A_j)}{\sum_i P(B\mid A_i)P(A_i)}.
$$

The denominator is just the normaliser, so in practice compute the unnormalised weights $P(B\mid A_i)P(A_i)$ and divide by their sum.
"Condition on the first step" is the same law applied to a process, and it drives most recursions in [Markov Chains](10-Markov-Chains.md) and [Random Walks and Gambler's Ruin](11-Random-Walks-and-Gamblers-Ruin.md).

### Odds form and sequential updating

For two hypotheses $H$ and $H'$ and data $D$:

$$
\frac{P(H\mid D)}{P(H'\mid D)} = \frac{P(H)}{P(H')}\cdot\frac{P(D\mid H)}{P(D\mid H')}.
$$

If data points $D_1, D_2, \dots$ are conditionally independent given the hypothesis, the likelihood ratios multiply, so log-odds add:

$$
\log\text{odds}_n = \log\text{odds}_0 + \sum_{k=1}^n \log\frac{P(D_k\mid H)}{P(D_k\mid H')}.
$$

Yesterday's posterior is today's prior; the order in which evidence arrives does not matter.
This is the trader's version of Bayes: every fill, print or quote update moves your fair value by an amount proportional to how much more likely it is under one story than the other.

### Independence and conditional independence

$A$ and $B$ are independent if $P(A\cap B) = P(A)P(B)$.
A collection is mutually independent only if the product rule holds for every subcollection; pairwise independence is weaker.
Standard counterexample: $X, Y$ fair independent bits and $Z = X \oplus Y$; every pair is independent but $P(X=Y=Z=1) = 0 \ne 1/8$.

Conditional independence given $C$: $P(A\cap B\mid C) = P(A\mid C)P(B\mid C)$.

- Conditionally independent but not independent: pick a fair coin or a two-headed coin with probability $1/2$ each and toss it twice.
  Given the coin the tosses are independent, yet $P(H_1) = 3/4$ and $P(H_1H_2) = \tfrac12\cdot\tfrac14 + \tfrac12 = 5/8 \ne 9/16$.
  Unconditionally, the first toss carries information about which coin you hold.
- Independent but not conditionally independent ("explaining away"): two independent fair coins, conditioned on at least one head.
  Then $P(X=H\mid \ge 1\text{ head}) = 2/3$ but $P(X=H\mid \ge1\text{ head}, Y=H) = 1/2$.

### Laplace's rule of succession

With a uniform prior on an unknown success probability $p$ and $s$ successes in $n$ trials, the posterior is $\text{Beta}(s+1, n-s+1)$ and

$$
P(\text{next trial succeeds}\mid s \text{ of } n) = \frac{s+1}{n+2}.
$$

A single observed head moves the predictive probability of heads from $1/2$ to $2/3$.
The Beta-binomial machinery is in [Random Variables and Distributions](03-Random-Variables-and-Distributions.md).

## Worked examples

### Example 1 - a positive test for a rare condition

"A condition affects 1 in 1000 people. A test has 99% sensitivity and 95% specificity. You test positive. What is the probability you have the condition?"

Out of 100,000 people, 100 have it and 99 of them test positive.
Of the 99,900 without it, 5% test positive: 4995.
So $P = 99/(99 + 4995) \approx 1.94\%$.
In odds form: prior odds $1:999$, likelihood ratio $0.99/0.05 = 19.8$, posterior odds about $19.8:999$, about 2%.
A second independent positive multiplies the odds by another 19.8, to about $392:999$, a posterior of about 28%.
The lesson: the false-positive rate on the large population swamps the true positives on the small one.
With 1% prevalence and 99% sensitivity and specificity, the answer is exactly 50%, which is the other number worth remembering.

### Example 2 - Monty Hall and its variants

"You pick door 1. The host, who knows where the car is, always opens a goat door among the other two, choosing at random if he has a choice. He opens door 3. Switch?"

Switch; you win with probability $2/3$.
Condition on the car's location with the host's behaviour made explicit.
If the car is behind 1 (prior $1/3$), the host opens 3 with probability $1/2$.
If behind 2 (prior $1/3$), he must open 3, probability 1.
If behind 3, he cannot open 3.
Weights $\tfrac16$ and $\tfrac13$ give $P(\text{car at 2}\mid \text{opens 3}) = 2/3$.

Variant ("Monty Fall"): the host opens one of the other two doors uniformly at random, and it happens to show a goat.
Now the weights are $\tfrac13\cdot\tfrac12$ for door 1 and $\tfrac13\cdot\tfrac12$ for door 2, so switching wins with probability $1/2$.
Same observation, different protocol, different answer.

### Example 3 - the double-headed coin

"A jar has 1000 coins, one of which has heads on both sides. You pick one at random, flip it 10 times, and see 10 heads. What is the probability it is the double-headed coin?"

Prior odds $1:999$.
Likelihood of 10 heads: 1 for the double-headed coin, $2^{-10} = 1/1024$ for a fair one, so the likelihood ratio is 1024.
Posterior odds $1024:999$, so $P = 1024/2023 \approx 0.506$.
Follow-up: probability the next flip is heads is $0.506\cdot1 + 0.494\cdot\tfrac12 \approx 0.753$.

### Example 4 - boy-girl

"A family has two children. At least one is a boy. What is the probability both are boys?"

Under the protocol "sample a family among those with at least one boy", the equally likely cases are BB, BG, GB, so $1/3$.
If instead you meet one of the children at random and it is a boy, the answer is $1/2$, because BB families are twice as likely to produce that observation.
If you learn "at least one is a boy born on a Tuesday" (days equally likely), there are $14^2 - 13^2 = 27$ equally likely (sex, day) pairs with a Tuesday boy, and $7^2 - 6^2 = 13$ of them are two boys, so $13/27$.
The extra detail makes the information closer to identifying a specific child, pushing the answer towards $1/2$.

### Example 5 - sequential updating as a trader

"A coin is either fair or has $P(H) = 0.6$, equally likely. You see 7 heads in 10 flips. What do you believe, and how would you explain each update?"

Each head multiplies the odds on the biased coin by $0.6/0.5 = 1.2$, and each tail by $0.4/0.5 = 0.8$.
After 7 heads and 3 tails the likelihood ratio is $1.2^7\cdot0.8^3 \approx 1.835$, so from even odds the posterior is $1.835/2.835 \approx 0.647$.
In log terms each head adds about $0.18$ and each tail subtracts about $0.22$, so evidence favours the biased coin only when the head fraction exceeds $0.223/(0.182+0.223) \approx 0.55$.
That threshold, not $0.6$, is the decision boundary, and saying it aloud shows you understand the likelihood ratio rather than eyeballing the sample mean.

## Pitfalls

- Confusing $P(A\mid B)$ with $P(B\mid A)$ (the prosecutor's fallacy): a match being unlikely for an innocent person does not make innocence unlikely.
- Ignoring the base rate, especially with rare events.
- Ignoring the protocol that generated the information (Monty Hall, boy-girl, selection bias in backtests).
- Treating pairwise independence as mutual independence.
- Assuming independence survives conditioning, or that conditional independence implies independence.
- Multiplying likelihood ratios from evidence that is not conditionally independent (two analysts reading the same report are one data point).
- Simpson's paradox: an association within every subgroup can reverse after aggregation when group sizes differ; condition on the confounder.

## Interview questions

> [!question]- prob-bayes-rare-condition-positive-test | Prevalence 1 in 1000, sensitivity 99%, specificity 95%. You test positive. Probability you have the condition?
> About $1.9\%$.
> $0.99\cdot0.001 / (0.99\cdot0.001 + 0.05\cdot0.999) = 0.00099/0.05094$; equivalently prior odds $1{:}999$ times likelihood ratio $19.8$.

> [!question]- prob-bayes-monty-hall-switch | In Monty Hall, the host knowingly opens a goat door. Should you switch, and what is your win probability?
> Switch; $2/3$.
> Your first pick is right with probability $1/3$ and the host's action cannot change that; the remaining $2/3$ concentrates on the unopened door.

> [!question]- prob-bayes-monty-fall-random-host | The host opens one of the other two doors uniformly at random and it happens to show a goat. Does switching help?
> No; switching wins with probability $1/2$.
> Say he opens door 3. He picks it with probability $1/2$ whatever the car's location, and it shows a goat unless the car is there, so the weights are $\tfrac13\cdot\tfrac12$ for car at 1, $\tfrac13\cdot\tfrac12$ for car at 2 and 0 for car at 3: equal.

> [!question]- prob-bayes-boy-girl-at-least-one | A two-child family is selected among families with at least one boy. Probability both are boys?
> $1/3$.
> Equally likely BB, BG, GB remain; only BB qualifies. If instead a randomly chosen child is observed to be a boy, the answer is $1/2$.

> [!question]- prob-bayes-boy-born-tuesday | A two-child family has at least one boy born on a Tuesday. Probability both are boys?
> $13/27$.
> Among $14^2$ (sex, day) pairs, $14^2-13^2=27$ contain a Tuesday boy; of these $7^2-6^2=13$ are two boys.

> [!question]- prob-bayes-double-headed-coin | One of 1000 coins is double-headed. A random coin shows 10 heads in 10 flips. Probability it is the double-headed one?
> $1024/2023 \approx 0.506$.
> Prior odds $1{:}999$, likelihood ratio $2^{10}=1024$.

> [!question]- prob-bayes-three-cards | Three cards: red-red, blue-blue, red-blue. A random card is placed on the table showing red. Probability the other side is red?
> $2/3$.
> Count red faces: 3 equally likely, 2 of which belong to the red-red card.

> [!question]- prob-bayes-urn-choice | Urn A has 3 red and 1 blue, urn B has 1 red and 3 blue. You pick an urn at random and draw red. Probability it was urn A?
> $3/4$.
> Likelihood ratio $(3/4)/(1/4) = 3$ on even prior odds gives $3{:}1$.

> [!question]- prob-bayes-pairwise-not-mutual | Give three events that are pairwise independent but not mutually independent.
> Two fair bits $X, Y$ and $Z = X\oplus Y$; events $\{X=1\},\{Y=1\},\{Z=1\}$.
> Each pair has joint probability $1/4 = \tfrac12\cdot\tfrac12$, but all three equal 1 is impossible, not $1/8$.

> [!question]- prob-bayes-conditional-vs-unconditional-independence | A fair coin or a two-headed coin is chosen with probability 1/2 and flipped twice. Are the flips independent?
> No, although they are conditionally independent given the coin.
> $P(H_1)=P(H_2)=3/4$ but $P(H_1H_2) = 5/8 \ne 9/16$: seeing a head raises the chance you hold the two-headed coin.

> [!question]- prob-bayes-rule-of-succession | With a uniform prior on a coin's bias, you observe 3 heads in 3 flips. Probability the next flip is heads?
> $4/5$.
> Laplace: posterior $\text{Beta}(s+1,n-s+1)$ has mean $(s+1)/(n+2) = 4/5$.

> [!question]- prob-bayes-log-odds-evidence | Why do traders like to think in log-odds when updating on many signals?
> Conditionally independent evidence adds in log-odds.
> Posterior log-odds = prior log-odds + $\sum$ log-likelihood ratios, so each signal contributes an additive "score" and order does not matter; correlated signals must not be double counted.

> [!question]- prob-bayes-biased-coin-seven-of-ten | A coin is fair or has P(H)=0.6, equally likely a priori. You see 7 heads in 10 flips. Posterior probability it is biased?
> About $0.647$.
> Likelihood ratio $1.2^7\cdot0.8^3 \approx 1.835$, so posterior odds $1.835{:}1$.

> [!question]- prob-bayes-second-positive-test | In the 1-in-1000, 99%/95% test, a second independent test is also positive. New posterior?
> About $28\%$.
> Odds $1{:}999$ times $19.8^2 \approx 392$ give $392{:}999$; independence of test errors given status is the key assumption.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapter 2 (conditioning, Monty Hall, Simpson's paradox).
- Xinfeng Zhou, *A Practical Guide to Quantitative Finance Interviews*, chapter 4 (conditional probability and Bayes' formula).
- Frederick Mosteller, *Fifty Challenging Problems in Probability* (the prisoner's dilemma and related conditioning puzzles).
- E. T. Jaynes, *Probability Theory: The Logic of Science*, chapter 4 (hypothesis testing in log-odds, "evidence in decibels").
- Next: [Random Variables and Distributions](03-Random-Variables-and-Distributions.md).
