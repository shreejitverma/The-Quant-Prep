---
type: concept
track: [quant-trader, quant-research]
tier: advanced
status: solid
prereqs: [random-variables-and-distributions]
est_hours: 3
sources: [Blitzstein and Hwang - Introduction to Probability (2nd ed.), Grimmett and Stirzaker - Probability and Random Processes, Ross - Introduction to Probability Models, Cont and Tankov - Financial Modelling with Jump Processes]
---

# Poisson Processes

## TL;DR

- A rate-$\lambda$ Poisson process has independent increments with $N(t+s) - N(t) \sim \text{Poisson}(\lambda s)$, and i.i.d. $\text{Exp}(\lambda)$ gaps between events.
- Superposition adds rates; thinning with probability $p$ gives independent processes of rates $p\lambda$ and $(1-p)\lambda$.
- Given $N(t) = n$, the event times are $n$ i.i.d. uniforms on $[0,t]$, sorted.
- Inspection paradox: the gap covering a fixed time has mean $2/\lambda$, twice the average gap, because long gaps are more likely to be sampled.
- Compound Poisson $\sum_{k \le N(t)} Y_k$ has mean $\lambda t E[Y]$ and variance $\lambda t E[Y^2]$; it is the jump part of every Levy model.

## Learning objectives

- Use exponential inter-arrivals, memorylessness, thinning and superposition fluently.
- Use conditional uniformity of arrival times to compute expectations over event times.
- Explain the inspection (waiting-time) paradox and quantify it for general renewal processes.
- Model order arrivals and compound Poisson jumps, including their variance and kurtosis.

## Core concepts

### Three equivalent definitions

A counting process $N(t)$ with $N(0) = 0$ is Poisson with rate $\lambda$ if any of the following holds.

1. Independent increments and $N(t + s) - N(t) \sim \text{Poisson}(\lambda s)$.
2. Inter-arrival times $T_1, T_2, \dots$ are i.i.d. $\text{Exp}(\lambda)$.
3. Independent, stationary increments with $P(N(h) = 1) = \lambda h + o(h)$ and $P(N(h) \ge 2) = o(h)$ (events are rare and never simultaneous).

The third is the modelling definition: many independent agents each acting rarely produce a Poisson stream, which is also the Binomial-to-Poisson limit $\text{Bin}(n, \lambda/n) \to \text{Poisson}(\lambda)$.

### Key distributions

- $P(N(t) = k) = e^{-\lambda t} (\lambda t)^k / k!$, with mean and variance $\lambda t$.
- The $n$-th arrival time $S_n$ is $\text{Gamma}(n, \lambda)$ with mean $n/\lambda$ and variance $n/\lambda^2$, and $P(S_n \le t) = P(N(t) \ge n)$.
- $\operatorname{Cov}(N(s), N(t)) = \lambda \min(s, t)$.
- $P(N(t) \text{ even}) = (1 + e^{-2\lambda t})/2$, from $E[(-1)^{N}] = e^{-2\lambda t}$.

### Memorylessness

$P(T > s + t \mid T > s) = P(T > t)$ for $T \sim \text{Exp}(\lambda)$, and the exponential is the only continuous law with this property.
So the time from any fixed moment (or any stopping time) to the next event is again $\text{Exp}(\lambda)$, independent of the past.

### Superposition and competition

Independent Poisson processes with rates $\lambda_1, \dots, \lambda_m$ merge into a Poisson process of rate $\sum \lambda_i$.
Each event of the merged process comes from source $i$ with probability $\lambda_i / \sum_j \lambda_j$, independently across events.
So the probability that $k$ events of process 1 occur before the first event of process 2 is $(\lambda_1/(\lambda_1 + \lambda_2))^k$.

### Thinning

If each event is independently kept with probability $p$, the kept and discarded events form independent Poisson processes with rates $p\lambda$ and $(1-p)\lambda$.
The independence is the surprising part: knowing there were many buys tells you nothing about the number of sells.
With time-varying $p(t)$ you get a non-homogeneous Poisson process with intensity $\lambda p(t)$ and $N(t) \sim \text{Poisson}(\int_0^t \lambda p(s)\,ds)$.

### Conditional uniformity

Given $N(t) = n$, the unordered arrival times are i.i.d. $U(0, t)$.
So $E[\sum_{k=1}^{N(t)} S_k] = E[N(t)] \cdot t/2 = \lambda t^2/2$, and given one event in $[0, t]$ its time is uniform.

### Inspection paradox

Fix a time $t$ far from 0 and look at the gap between the last event before $t$ and the first after.
The forward wait is $\text{Exp}(\lambda)$ by memorylessness and the backward age is also (approximately) $\text{Exp}(\lambda)$, so the covering gap has mean $2/\lambda$.
For a general renewal process with gap $L$, the covering gap is length-biased with mean $E[L^2]/E[L] = E[L] + \operatorname{Var}(L)/E[L]$, and the mean wait is $E[L^2]/(2E[L])$.
Buses every 10 minutes exactly give a 5-minute average wait; Poisson buses with the same average gap give 10.
The same bias shows up as "the average class size students report exceeds the average class size" and in survivorship of long-lived orders in a book.

### Compound Poisson

$X(t) = \sum_{k=1}^{N(t)} Y_k$ with i.i.d. jumps $Y_k$ independent of $N$.
By the law of total expectation and total variance:

$$
E[X(t)] = \lambda t\, E[Y], \qquad \operatorname{Var}(X(t)) = \lambda t\, E[Y^2].
$$

Note $E[Y^2]$, not $\operatorname{Var}(Y)$: the randomness of the count contributes $\operatorname{Var}(N) E[Y]^2$.
With normal jumps of mean 0, the excess kurtosis of $X(t)$ is $3/(\lambda t)$, so rare jumps create fat tails that wash out as the horizon grows.
This is the jump component of Merton's model; see [Jump Processes and Levy Models](../04-Stochastic-Calculus/08-Jump-Processes-and-Levy-Models.md).

### Order-flow modelling

Market orders arriving at rate $\lambda$ and each hitting the bid with probability $p$ give independent buy and sell streams, which is the starting point of Glosten-Milgrom and Avellaneda-Stoikov fill models ([Avellaneda-Stoikov](../08-Market-Making/03-Inventory-Risk-and-Avellaneda-Stoikov.md) uses fill intensity $\lambda(\delta) = A e^{-k\delta}$ at quote distance $\delta$).
Real order flow is clustered and self-exciting, so Poisson is the null model; Hawkes processes are the standard extension.

## Worked examples

### Buses and the inspection paradox

"Buses arrive as a Poisson process at 6 per hour. I show up at a random time. How long do I wait, and how long is the gap I land in?"
"Memorylessness: the wait is $\text{Exp}(6/\text{hr})$, mean 10 minutes."
"Looking backward, the time since the last bus is also about $\text{Exp}(6)$, mean 10 minutes, so the gap I land in averages 20 minutes, double the 10-minute average gap."
"If buses came exactly every 10 minutes, I would wait 5 minutes on average; the variance of the gaps costs me the extra 5, via $E[L^2]/(2E[L])$."

### Thinning order flow

"Orders arrive at 10 per second and each is a buy with probability $0.3$."
"Buys form a Poisson process of rate 3, so $P(\text{no buys in a second}) = e^{-3} \approx 0.050$."
"Given exactly 5 orders in that second, the number of buys is $\text{Bin}(5, 0.3)$; unconditionally, the buy and sell counts are independent $\text{Poisson}(3)$ and $\text{Poisson}(7)$."
"So observing 20 sells in a second carries no information about buys, which is the modelling assumption to challenge if flow is correlated."

### Racing two processes

"Trader A's orders arrive at rate 2, trader B's at rate 3. Probability A sends two orders before B sends one?"
"Merge into a rate-5 process; each event is A's with probability $2/5$ independently, so the answer is $(2/5)^2 = 4/25$."
"Expected time until I have seen at least one order from each: $E[\max(T_A, T_B)] = E[T_A] + E[T_B] - E[\min] = 1/2 + 1/3 - 1/5 = 19/30$."

### Compound Poisson jump risk

"A stock has jumps at 2 per day on average, each $N(0, (1\%)^2)$. Daily jump-return standard deviation?"
"$\operatorname{Var} = \lambda E[Y^2] = 2 \times 0.0001$, so the standard deviation is $\sqrt{0.0002} \approx 1.41\%$."
"Excess kurtosis is $3/\lambda = 1.5$ at a one-day horizon and $0.075$ over 20 days: jump tails fade under aggregation."

### Arrival times given the count

"Given exactly 2 events in $[0, 1]$, probability both occurred in the first half?"
"The two times are i.i.d. uniform given the count, so $(1/2)^2 = 1/4$."
"Expected time of the first of them: the min of two uniforms, $1/3$."

## Pitfalls

- Using $\operatorname{Var}(Y)$ instead of $E[Y^2]$ in the compound Poisson variance.
- Assuming the gap containing a random time is a typical gap; it is length-biased.
- Forgetting that thinning gives independent streams only when the keep decisions are independent of everything else.
- Treating clustered real-world arrivals (trades, cancellations) as Poisson and then being surprised by the variance: check the index of dispersion $\operatorname{Var}(N)/E[N]$, which is 1 for Poisson.
- Mixing rate and mean: $\text{Exp}(\lambda)$ has mean $1/\lambda$; state which convention you use.

## Interview questions

> [!question]- prob-pp-no-event-probability | Events arrive as a Poisson process of rate 2 per minute. Probability of no events in a minute?
> $e^{-2} \approx 0.135$. $N(1) \sim \text{Poisson}(2)$ and $P(N = 0) = e^{-\lambda t}$.

> [!question]- prob-pp-superposition-rate | Two independent Poisson processes have rates $\lambda$ and $\mu$. What is their superposition, and which process produces the first event?
> A Poisson process of rate $\lambda + \mu$; the first event is from the first process with probability $\lambda/(\lambda+\mu)$, independently of when it happens.

> [!question]- prob-pp-thinning-independence | Orders arrive at rate 10/s and each is a buy with probability $0.3$. Describe the buy and sell processes.
> Independent Poisson processes with rates 3 and 7. Thinning a Poisson process by independent coin flips gives independent Poisson streams.

> [!question]- prob-pp-k-before-one | Process A has rate $\lambda$, process B rate $\mu$. Probability that $k$ A-events occur before the first B-event?
> $(\lambda/(\lambda+\mu))^k$. Each merged event is from A independently with probability $\lambda/(\lambda+\mu)$.

> [!question]- prob-pp-conditional-uniform | Given $N(t) = n$ for a Poisson process, what is the joint law of the event times?
> The order statistics of $n$ i.i.d. $U(0,t)$. The density $\lambda^n e^{-\lambda t}$ on ordered times is flat, then divide by $P(N(t) = n)$.

> [!question]- prob-pp-inspection-paradox | Buses arrive as a Poisson process with mean gap 10 minutes. Arriving at a random time, what is the mean wait and the mean length of the gap you are in?
> Wait 10 minutes; gap 20 minutes. The forward and backward times are each $\text{Exp}$ with mean 10; long gaps are sampled in proportion to their length.

> [!question]- prob-pp-deterministic-bus-wait | With a general renewal process of gaps $L$, what is the mean wait from a random time?
> $E[L^2]/(2E[L])$. Deterministic gaps of 10 give 5; exponential gaps of mean 10 give 10.

> [!question]- prob-pp-nth-arrival-gamma | What is the distribution of the time of the $n$-th event in a rate-$\lambda$ Poisson process?
> $\text{Gamma}(n, \lambda)$, mean $n/\lambda$, variance $n/\lambda^2$. It is a sum of $n$ i.i.d. exponentials, and $P(S_n \le t) = P(N(t) \ge n)$.

> [!question]- prob-pp-compound-variance | Jumps arrive at rate $\lambda$ with i.i.d. sizes $Y$. Variance of the total jump over time $t$?
> $\lambda t E[Y^2]$. Total variance: $E[N]\operatorname{Var}(Y) + \operatorname{Var}(N)E[Y]^2$ with $E[N] = \operatorname{Var}(N) = \lambda t$.

> [!question]- prob-pp-compound-kurtosis | For compound Poisson with rate $\lambda$ and $N(0,\sigma^2)$ jumps, what is the excess kurtosis at horizon $t$?
> $3/(\lambda t)$. Given $N$, the sum is $N(0, N\sigma^2)$, so $E[X^4] = 3\sigma^4 E[N^2]$ and $E[N^2] = \lambda t + (\lambda t)^2$.

> [!question]- prob-pp-max-of-two-exponential-waits | Independent Poisson streams of rates 1 and 2. Expected time until at least one event from each?
> $7/6$. $E[\max] = E[T_1] + E[T_2] - E[\min] = 1 + 1/2 - 1/3$.

> [!question]- prob-pp-even-count | For $N \sim \text{Poisson}(\mu)$, what is $P(N \text{ even})$?
> $(1 + e^{-2\mu})/2$. $E[(-1)^N] = e^{-\mu}\sum_k (-\mu)^k/k! = e^{-2\mu}$, and $P(\text{even}) - P(\text{odd}) = E[(-1)^N]$.

> [!question]- prob-pp-count-covariance | What is $\operatorname{Cov}(N(s), N(t))$ for $s \le t$?
> $\lambda s$. Write $N(t) = N(s) + (N(t) - N(s))$ with independent increments; the covariance is $\operatorname{Var}(N(s))$.

> [!question]- prob-pp-binomial-limit | 1000 independent trades each fail with probability $0.001$. Probability of no failures, and why is Poisson accurate?
> About $e^{-1} \approx 0.368$ (exactly $0.999^{1000} \approx 0.3677$). $\text{Bin}(n, \lambda/n) \to \text{Poisson}(\lambda)$ when $n$ is large and $p$ small.

## Further reading

- Blitzstein and Hwang, *Introduction to Probability* (2nd ed.), chapters 5 and 13.
- Grimmett and Stirzaker, *Probability and Random Processes*, section 6.8.
- Sheldon Ross, *Introduction to Probability Models*, chapter 5 (the most interview-aligned treatment).
- Rama Cont and Peter Tankov, *Financial Modelling with Jump Processes*, chapters 2-3.
