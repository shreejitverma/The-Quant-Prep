---
type: cfa-lm
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
volume: 7
lm: 2
title: "Valuation of Contingent Claims"
pages: "81-156"
weight_band: "5-10%"
difficulty: 4
los_count: 14
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/derivatives]
---

# LM2: Valuation of Contingent Claims

Difficulty 4 of 5: the binomial arithmetic is mechanical but long (three one-period trees, early exercise tests, hedge ratios at every node), the BSM and Black models demand precise input selection under five different underlyings (stock, currency, futures, FRA, forward swap rate), and the Greeks and implied volatility questions punish anyone who memorized formulas without the replication story behind them.

## LOS map

- **describe** and interpret the binomial option valuation model and its component terms (V7 p.81) ^los-07-02-a
    - Examiner asks: given u, d, S and X, identify the hedge ratio, the risk-neutral probability, or the financing leg, and state what each term of $c = hS + PV(-hS^- + c^-)$ represents economically.
- **describe** how the value of a European option can be analyzed as the present value of the option's expected payoff at expiration (V7 p.81) ^los-07-02-b
    - Examiner asks: confirm that the expectations approach discounts at the risk-free rate and weights payoffs with risk-neutral (not investor or real-world) probabilities, usually as two statements to accept or reject.
- **identify** an arbitrage opportunity involving options and describe the related arbitrage (V7 p.81) ^los-07-02-c
    - Examiner asks: the market call price sits above the model value; pick the trade set (write the call, buy h shares, borrow) and possibly compute the Time 0 arbitrage profit.
- **calculate** the no-arbitrage values of European and American options using a two-period binomial model (V7 p.81) ^los-07-02-d
    - Examiner asks: roll a two-period tree backward for a call or put, then redo it American-style by replacing a node value with a larger exercise value and quantify the early exercise premium.
- **calculate** and interpret the value of an interest rate option using a two-period binomial model (V7 p.81) ^los-07-02-e
    - Examiner asks: value a call or put on the one-year spot rate on a given rate lattice with 50/50 probabilities, discounting each step at that node's own one-period bond value, and scale by the notional.
- **identify** assumptions of the Black-Scholes-Merton option valuation model (V7 p.81) ^los-07-02-f
    - Examiner asks: pick the statement pair consistent with the BSM assumptions (GBM with lognormal prices, continuous prices and trading, no frictions, constant known rate and volatility, European exercise, constant yield).
- **interpret** the components of the Black-Scholes-Merton model as applied to call options in terms of a leveraged position in the underlying (V7 p.81) ^los-07-02-g
    - Examiner asks: identify the replicating portfolio as long $N(d_1)$ shares financed by shorting $N(d_2)$ zero-coupon bonds priced at $e^{-rT}X$, or identify $N(d_2)$ as the risk-neutral probability the call expires in the money.
- **describe** how the Black-Scholes-Merton model is used to value European options on equities and currencies (V7 p.81) ^los-07-02-h
    - Examiner asks: select the correct inputs (spot, strike, T in years, domestic risk-free rate, and dividend yield or foreign rate as the carry benefit) and the correct formula orientation for a call or put.
- **describe** how the Black model is used to value European options on futures (V7 p.81) ^los-07-02-i
    - Examiner asks: choose the futures price, not the spot index, as the underlying, discount everything at the risk-free rate, and describe the call as the present value of $F_0(T)N(d_1) - XN(d_2)$.
- **describe** how the Black model is used to value European interest rate options and European swaptions (V7 p.81) ^los-07-02-j
    - Examiner asks: pick the FRA rate as the underlying, the option-expiry-plus-accrual date as the discount horizon, the forward swap rate as the swaption underlying, and match payer/receiver swaptions to rate views and to caps, floors, and callable bonds.
- **interpret** each of the option Greeks (V7 p.81) ^los-07-02-k
    - Examiner asks: match delta, gamma, theta, vega, and rho to definitions, signs, and situations (which Greek captures time decay, why gamma peaks at the money, why call rho is positive and put rho negative).
- **describe** how a delta hedge is executed (V7 p.81) ^los-07-02-l
    - Examiner asks: compute $N_H = -\text{Portfolio delta}/\text{Delta}_H$ for a stock or option hedge, get the sign right (buy or sell), and recognize that the hedge must be rebalanced as delta drifts.
- **describe** the role of gamma risk in options trading (V7 p.81) ^los-07-02-m
    - Examiner asks: a delta-hedged short option position jumps in the underlying; identify the residual loss as gamma risk, and know that only option trades (not stock) change portfolio gamma.
- **define** implied volatility and explain how it is used in options trading (V7 p.81) ^los-07-02-n
    - Examiner asks: invert the model price to the volatility that reproduces the market price, compare model and market prices to say whether implied is above or below the input volatility, and use implied volatility to compare options across strikes, maturities, and markets.

## Core intuition

Everything in this module is one idea wearing different clothes: an option can be manufactured out of the underlying and risk-free borrowing or lending, so its price is pinned down by the cost of the manufacture, not by anyone's forecast of the underlying (V7 p.82, p.88).
The manufacturer is an arbitrageur who follows two rules: do not use your own money, and do not take any price risk (V7 p.82, p.84).
If a portfolio with zero future obligations threw off positive cash today, everyone would run it, so equilibrium prices must make the net cash flow at initiation exactly zero.
That zero-net-cash condition, applied to a written call hedged with $h$ shares and a financing leg, is the entire derivation engine of the binomial model (V7 p.87, p.88).
The law of one price does the rest: two positions with identical payoffs in every state must have identical prices (V7 p.82).

![[Option-Payoff-Diagrams.excalidraw]]

> [!abstract] Idea 1: the hedge ratio makes you indifferent to the coin flip
> In a one-period world the underlying ends at $S^+$ or $S^-$ and the call at $c^+$ or $c^-$; choosing $h = (c^+ - c^-)/(S^+ - S^-)$ makes the hedged portfolio worth the same in both states, so its payoff is riskless and must earn the risk-free rate (V7 p.87).
> A call is then literally $h$ shares partially financed by borrowing, and a put is a short position of $h$ shares (negative for puts) with lending, which is why the call hedge ratio is non-negative and the put hedge ratio non-positive (V7 p.88, p.89).
> The same object reappears continuously in BSM as $N(d_1)$ and in risk management as delta; the module is one long meditation on this ratio (V7 p.114, p.129).

The no-arbitrage construction can be rearranged into something that looks like ordinary discounted-cash-flow valuation: the option value is the present value of the expected payoff, $c = PV[\pi c^+ + (1-\pi)c^-]$ (V7 p.90).
But two things are deliberately unusual (V7 p.91).
The probability $\pi = [FV(1) - d]/(u - d)$ is not anyone's belief; it drops out of the arbitrage algebra, which is why it is called a risk-neutral probability, and it never changes when the option contract's own terms (like the strike) change (V7 p.90, p.91, p.154).
And the discount rate is the risk-free rate, not a risk-adjusted rate, because the replicating portfolio has already removed the risk.
Both subjective inputs of DCF have been replaced by objective ones, which is why the expectations approach is considered superior and is the workhorse for European options (V7 p.91).

The two-period binomial tree is just three one-period trees, solved right to left (V7 p.93).
The replication story gains two adjectives: the strategy is dynamic (the hedge ratio changes at each node, so shares are bought as the market rises and sold as it falls) and self-financing (the extra shares are paid for with exactly the extra borrowing the strategy itself generates) (V7 p.93, p.94, p.95).
European values need only the terminal payoffs, weighted by the binomial probabilities $\pi^2$, $2\pi(1-\pi)$, $(1-\pi)^2$ and discounted two periods (V7 p.95).
American values cannot take that shortcut: at every node you must compare the rolled-back model value with the immediate exercise value and keep the larger, which is why the no-arbitrage backward walk is the only general method for American options (V7 p.97, p.99, p.109).

> [!abstract] Idea 2: early exercise is about interest and dividends, never about optimism
> A deep in-the-money American put is worth exercising because the sale proceeds can start earning risk-free interest today, and that interest can exceed the put's remaining time value (V7 p.97).
> An American call on a non-dividend stock is never exercised early: the call lets you delay paying the strike, so it always trades above exercise value and is better sold than exercised (V7 p.97).
> Dividends flip the call case: exercising just before the ex-dividend date captures the dividend that the option holder would otherwise lose, so American calls on dividend payers can command an early exercise premium (V7 p.101).

Interest rate options ride the same machinery on a lattice of one-year rates, with two twists: the risk-neutral probability is fixed at 50% at every node, and the discount factor changes node by node because the discount rate is itself the underlying (V7 p.106, p.108).
A rate call pays when the observed spot rate ends above the exercise rate, a rate put when it ends below (V7 p.107).

Slice the binomial periods ever finer and the model converges to Black-Scholes-Merton, the continuous-time limit (V7 p.109, p.110).
BSM assumes the underlying follows geometric Brownian motion: continuously compounded returns are normally distributed, so prices are lognormal, can never go negative, and never jump (V7 p.110, p.111).
The other assumptions are the arbitrageur's wish list: liquid underlying, continuous trading, short selling with full proceeds, no frictions, no arbitrage, European exercise, known constant risk-free rate and volatility, and any yield paid continuously at a constant rate (V7 p.111, p.112).
The formula $c = SN(d_1) - e^{-rT}XN(d_2)$ is the one-period binomial answer with the same anatomy: a stock component $SN(d_1)$ and a bond component $e^{-rT}XN(d_2)$, so a call is a leveraged stock position (buy $N(d_1)$ shares, short $N(d_2)$ zero-coupon bonds), and a put is lending financed by a short stock position (V7 p.113, p.114).
$N(d_2)$ carries a second meaning worth its own flashcard: it is the risk-neutral probability the call expires in the money (V7 p.116).
Carry benefits (dividend yield $\delta$, foreign interest rate $r^f$) enter as a continuous yield $\gamma$ that discounts the stock component and shrinks $d_1$ and $d_2$; they lower call values and raise put values (V7 p.116, p.117).

The Black model is BSM with the underlying swapped for a futures or forward price, which is costless to carry, so the entire bracket $[F_0(T)N(d_1) - XN(d_2)]$ is discounted at $e^{-rT}$ (V7 p.120).
Two families of fixed-income options are then small modifications of Black (V7 p.123, p.126).
Interest rate caplets and floorlets use the FRA rate as the underlying, multiply by an accrual period, and discount to the settlement date $t_{j-1} + t_m$ because rates are advanced set, settled in arrears (V7 p.122, p.123).
Caps are strips of caplets hedging floating-rate borrowers, floors are strips of floorlets hedging floating-rate lenders, and a long cap plus short floor struck at the swap rate replicates a receive-floating, pay-fixed swap at zero initial cost (V7 p.124, p.125).
Swaptions replace the single payoff with an annuity of rate differences: the payer swaption pays off when the fixed swap rate rises above the exercise rate, the receiver swaption when it falls below, and the discounting hides inside the annuity factor PVA (V7 p.126, p.127).
The equivalence to remember for the exam: a callable fixed-rate bond is a straight bond plus a short receiver swaption (V7 p.127).

> [!abstract] Idea 3: the Greeks are the replication story differentiated, and implied volatility is the model inverted
> Delta is the hedge ratio ($e^{-\delta T}N(d_1)$ for calls), gamma is how fast that hedge goes stale, theta is the bleed from the calendar, vega is the exposure to the one input nobody observes, and rho is the financing-cost sensitivity (V7 p.129, p.132, p.135, p.136, p.137).
> A delta hedge only immunizes against small moves; jumps leave the delta hedger exposed through gamma, which is why gamma is largest at the money, why buying options is the only way to add gamma, and why a delta-plus-gamma approximation tracks large moves far better than delta alone (V7 p.131, p.132, p.133, p.134).
> Implied volatility is the volatility that makes the model reproduce the market price; it converts every option, whatever its strike or maturity, into a common unit, so traders quote in volatility, compare cheapness across options and markets, and read smiles, term structures, and surfaces as the market's disagreement with BSM's constant-volatility assumption (V7 p.138, p.139, p.140).

Read the whole module as a valuation ladder: one-period binomial for the logic, two-period for American exercise, lattices for rates, BSM for the continuous limit, Black for anything forward-based, and the Greeks plus implied volatility for living with the positions afterward (V7 p.82, p.142).

## Formulas and derivations

**Option exercise values at expiration** (V7 p.85)
$$
c_T = \operatorname{Max}(0, S_T - X), \qquad p_T = \operatorname{Max}(0, X - S_T)
$$
^f-07-02-1

- $S_T$: underlying price at expiration; $X$: exercise (strike) price; both in the same currency unit.
- At expiration there is no uncertainty left, so any deviation from exercise value is an immediate arbitrage (V7 p.85).
- Before expiration an option also carries non-negative time value, the market price of the payoff asymmetry; time value hits zero at expiration (V7 p.85).

**Up and down factors** (V7 p.86)
$$
u = \frac{S^+}{S}, \qquad d = \frac{S^-}{S}
$$
^f-07-02-2

- $u$ and $d$ are gross (one plus) returns for the up and down moves; higher assumed volatility widens $u$ and shrinks $d$ (V7 p.86).
- With constant $u$ and $d$ the lattice recombines ($S^{+-} = S^{-+} = udS$), so an $n$-step tree ends with $n+1$ nodes instead of $2^n$ (V7 p.93).

**Single-period hedge ratio (call)** (V7 p.87)
$$
h = \frac{c^+ - c^-}{S^+ - S^-} \ge 0
$$
^f-07-02-3

- $c^+$, $c^-$: call values after the up and down move; $S^+$, $S^-$: the corresponding underlying prices; $h$: units of the underlying held against one written call.
- Setting the two Time 1 cash flows of the written-call-plus-shares portfolio equal, $-c^+ + hS^+ = -c^- + hS^-$, and solving gives $h$; the portfolio payoff is then state-independent, hence riskless (V7 p.87).
- Same pattern up and down in numerator and denominator: option spread over underlying spread.

**No-arbitrage single-period call valuation** (V7 p.88)
$$
c = hS + PV\!\left(-hS^- + c^-\right)
$$
^f-07-02-4

- $PV(1) = 1/(1+r)$ with $r$ the periodically compounded risk-free rate per period; the argument $-hS^- + c^-$ equals $-hS^+ + c^+$ by construction of $h$.
- The Time 0 net cash flow of writing the call, buying $h$ shares, and financing must be zero, or arbitrageurs trade until it is; solving the zero condition for $c$ gives the formula (V7 p.88).
- Reading: long a call equals owning $h$ shares partially financed with borrowing, a leveraged stock position (V7 p.88).

> [!tip] Calculator
> Example 3 inputs ($h = 0.573770$, $S^- = 74$, $r = 5.15\%$): `0.573770 [x] 74 [=] [+/-] [/] 1.0515 [=]` gives $-40.379$; then `[+] 0.573770 [x] 100 [=]` is wrong order, so store: `0.573770 [x] 100 [=] STO 1` (57.377), `0.573770 [x] 74 [/] 1.0515 [=] [+/-] [+] RCL 1 [=]` gives 16.998.

**No-arbitrage single-period put valuation and put hedge ratio** (V7 p.89)
$$
p = hS + PV\!\left(-hS^- + p^-\right), \qquad h = \frac{p^+ - p^-}{S^+ - S^-} \le 0
$$
^f-07-02-5

- Because $p^+ < p^-$ while $S^+ > S^-$, the put hedge ratio is negative: replicating a long put means short selling $h$ units and lending part of the proceeds (V7 p.89).
- Writers reverse the trades: a call writer shorts stock and lends, a put writer buys stock on margin (V7 p.90).

**Expectations approach and the risk-neutral probability** (V7 p.90)
$$
c = PV\!\left[\pi c^+ + (1-\pi)c^-\right], \quad p = PV\!\left[\pi p^+ + (1-\pi)p^-\right], \quad \pi = \frac{FV(1) - d}{u - d} = \frac{1 + r - d}{u - d}
$$
^f-07-02-6

- $\pi$: risk-neutral (RN) probability of the up move; $FV(1) = 1 + r$ per period; discounting is at the risk-free rate.
- Algebraic rearrangement of the no-arbitrage result, so it embodies no assumption about risk preferences; $\pi$ is objective and is not the true probability of an up move (V7 p.90, p.91).
- Two exam-tested properties: expectation under RN probabilities, discounting at the risk-free rate; both replace the subjective inputs of DCF valuation (V7 p.91).

> [!tip] Calculator
> $u = 1.35$, $d = 0.74$, $r = 5.15\%$: `1.0515 [-] 0.74 [=] [/] ( 1.35 [-] 0.74 ) [=]` gives 0.5107.

**Put-call parity** (V7 p.92)
$$
S + p = PV(X) + c
$$
^f-07-02-7

- Two versions of portfolio insurance: stock plus put equals lending $PV(X)$ plus call, same strike and expiry; holds under any valuation model (V7 p.92).
- Rearranged, $c = S - PV(X) + p$; used constantly to get the put from the computed call (V7 p.92, p.96).

**Two-period expectations valuation** (V7 p.95)
$$
c = PV\!\left[\pi^2 c^{++} + 2\pi(1-\pi)c^{+-} + (1-\pi)^2 c^{--}\right], \qquad PV = \frac{1}{(1+r)^2}
$$
^f-07-02-8

- Terminal payoffs weighted by the binomial RN probabilities; the middle weight is $2\pi(1-\pi)$ because two paths reach the middle node; identical structure for puts (V7 p.95).
- Valid for European options only; American options must be rolled back node by node with an exercise test, because an exercised node breaks the terminal-payoff shortcut (V7 p.98, p.99).

> [!tip] Calculator
> Example 5 ($\pi = 0.5$, $c^{++} = 41.9368$, $c^{+-} = 0.4432$, $r = 5\%$): `0.5 [x^2] [x] 41.9368 [=] STO 1` (10.4842), `2 [x] 0.5 [x] 0.5 [x] 0.4432 [=] [+] RCL 1 [=] [/] 1.05 [x^2] [=]` gives 9.71.

**Escrow method for known dividends** (V7 p.100)
$$
\hat{S} = S - \gamma
$$
^f-07-02-9

- $\gamma$: present value of the dividends paid during the option's life; the binomial randomness is modeled on the dividend-stripped price $\hat{S}$, and the dividend is added back at the exercise test (V7 p.100).
- Rationale for early exercise of American calls: just before ex-dividend the option can be exercised for $(\hat{S}^+ + D) - X$, capturing a dividend the option holder otherwise never receives (V7 p.101).

**Black-Scholes-Merton model (no carry)** (V7 p.112, p.113)
$$
c = SN(d_1) - e^{-rT}XN(d_2), \qquad p = e^{-rT}XN(-d_2) - SN(-d_1)
$$
^f-07-02-10

- $r$: annualized continuously compounded risk-free rate; $T$: time to expiration in years; $N(\cdot)$: standard normal CDF; $N(-x) = 1 - N(x)$ by symmetry (V7 p.112, p.113).
- Present value of the RN expected payoff: $c = e^{-rT}[Se^{rT}N(d_1) - XN(d_2)]$, the continuous-time limit of the binomial expectations approach (V7 p.113).
- Anatomy: stock component minus bond component for calls, bond minus stock for puts (V7 p.114).

**BSM $d_1$ and $d_2$** (V7 p.113)
$$
d_1 = \frac{\ln(S/X) + \left(r + \sigma^2/2\right)T}{\sigma\sqrt{T}}, \qquad d_2 = d_1 - \sigma\sqrt{T}
$$
^f-07-02-11

- $\sigma$: annualized volatility of the continuously compounded return on the underlying; a rise in $S$ raises $d_1$ and thus $N(d_1)$ (V7 p.113, p.115).
- $N(d_2)$ is the RN probability the call expires in the money, $\operatorname{Prob}(S_T > X)$; $N(-d_2)$ the same for the put (V7 p.116).

> [!tip] Calculator
> $S = X = 100$, $r = 5\%$, $\sigma = 30\%$, $T = 1$: $\ln(1) = 0$, so `0.05 [+] 0.3 [x^2] [/] 2 [=] [/] 0.3 [=]` gives $d_1 = 0.3167 \approx 0.317$; `[-] 0.3 [=]` gives $d_2 = 0.017$; N values come from the exhibit or a lookup table.

**BSM replicating portfolio** (V7 p.114)
$$
\text{Cost} = n_S S + n_B B, \quad B = e^{-rT}X, \quad
\begin{cases} \text{call: } n_S = N(d_1) > 0,\; n_B = -N(d_2) < 0 \\ \text{put: } n_S = -N(-d_1) < 0,\; n_B = N(-d_2) > 0 \end{cases}
$$
^f-07-02-12

- A call is bought stock financed by shorting zeros (leveraged stock); a put is bought zeros financed by shorting stock; a short put is over-leveraged stock because borrowing exceeds the stock cost (V7 p.114).
- The strategy must be rebalanced continuously, buying shares as $S$ rises and selling as it falls; the cumulative loss of this buy-high sell-low trading equals exactly the option premium, or arbitrage would exist (V7 p.115).
- Real-world frictions (transaction costs, jumps, unknown volatility) make hedges imperfect, which is one reason traded options tend to be priced above naive BSM values (V7 p.115).

**Carry-benefit-adjusted BSM model** (V7 p.116)
$$
c = Se^{-\gamma T}N(d_1) - e^{-rT}XN(d_2), \qquad p = e^{-rT}XN(-d_2) - Se^{-\gamma T}N(-d_1), \qquad d_1 = \frac{\ln(S/X) + \left(r - \gamma + \sigma^2/2\right)T}{\sigma\sqrt{T}}
$$
^f-07-02-13

- $\gamma$: continuous carry benefit yield; $\gamma = \delta$ (dividend yield) for stock options, $\gamma = r^f$ (foreign risk-free rate) for currency options where $S$ is domestic currency per unit of foreign (V7 p.117, p.119).
- Carry benefits lower the expected future value of the underlying, lower $d_1$ and $d_2$, lower calls, and raise puts (V7 p.116, p.117).
- Replication with dividends: $n_S = e^{-\delta T}N(d_1)$ shares for calls (fewer shares to buy) and $n_S = -e^{-\delta T}N(-d_1)$ for puts (more shares to short) (V7 p.117).

**Carry-adjusted put-call parity** (V7 p.116)
$$
p + Se^{-\gamma T} = c + e^{-rT}X
$$
^f-07-02-14

- The stock leg is trimmed by the carry benefit because the stock holder, unlike the option holder, collects the yield (V7 p.116).
- With $\gamma = 0$ it reduces to formula 7 in continuous-rate form.

**Black model for European options on futures** (V7 p.120)
$$
c = e^{-rT}\left[F_0(T)N(d_1) - XN(d_2)\right], \qquad p = e^{-rT}\left[XN(-d_2) - F_0(T)N(-d_1)\right], \qquad d_1 = \frac{\ln\left[F_0(T)/X\right] + \left(\sigma^2/2\right)T}{\sigma\sqrt{T}}
$$
^f-07-02-15

- $F_0(T)$: futures (or forward) price today for expiry $T$; $\sigma$: volatility of the futures price; no carry term appears because a futures position is costless to carry (V7 p.120).
- Interpretation: the present value of the difference between the futures price and the exercise price, each weighted by its $N(d)$ adjustment (V7 p.121).

**Black futures put-call parity** (V7 p.120)
$$
c = e^{-rT}\left[F_0(T) - X\right] + p
$$
^f-07-02-16

- With $F_0(T) = X$ (at the money forward), call equals put; the sign of $F_0(T) - X$ tells you instantly which of the pair is dearer (V7 p.120).

**Standard market model: interest rate options** (V7 p.123)
$$
c = (AP)\,e^{-r(t_{j-1}+t_m)}\left[FRA(0,t_{j-1},t_m)N(d_1) - R_X N(d_2)\right], \qquad p = (AP)\,e^{-r(t_{j-1}+t_m)}\left[R_X N(-d_2) - FRA(0,t_{j-1},t_m)N(-d_1)\right]
$$
^f-07-02-17

- $FRA(0,t_{j-1},t_m)$: today's fixed rate on an FRA expiring at $t_{j-1}$ on a deposit maturing $t_m$ later; $R_X$: exercise rate (decimal); $AP$: accrual period (for example 90/360); $d_1 = \{\ln[FRA/R_X] + (\sigma^2/2)t_{j-1}\}/(\sigma\sqrt{t_{j-1}})$ with $\sigma$ the volatility of the FRA rate; multiply by notional (V7 p.123).
- Differences from Black to memorize: discount to $t_{j-1} + t_m$ (settled in arrears), underlying is a rate not a price, strike is a rate, and $d_1$ uses the option expiry $t_{j-1}$ (V7 p.124).
- Combinations: cap = strip of caplets (calls), floor = strip of floorlets (puts); long cap plus short floor struck at the swap rate = receive-floating, pay-fixed swap, and at that strike cap value equals floor value (V7 p.124, p.125).

**Black swaption model** (V7 p.126)
$$
PAYSWN = (AP)\,PVA\left[R_{FIX}N(d_1) - R_X N(d_2)\right], \qquad RECSWN = (AP)\,PVA\left[R_X N(-d_2) - R_{FIX}N(-d_1)\right], \qquad PVA = \sum_{j=1}^{n} PV_{0,t_j}(1)
$$
^f-07-02-18

- $R_{FIX}$: current forward swap rate for a swap starting at option expiry $T$; $R_X$: exercise swap rate; $PVA$: present value annuity factor over the swap's settlement dates, which embeds all discounting; $d_1 = \{\ln(R_{FIX}/R_X) + (\sigma^2/2)T\}/(\sigma\sqrt{T})$ with $\sigma$ the forward swap rate volatility (V7 p.126).
- The exercised payer swaption plus an offsetting at-market swap leaves an annuity of $(R_{FIX} - R_X)$, hence the annuity factor (V7 p.126).
- Equivalences: long receiver plus short payer (same strike) = receive-fixed forward swap; at the strike where payer value equals receiver value, $R_X$ is the at-market forward swap rate; long callable bond = long straight bond + short receiver swaption (V7 p.127).

**Option delta** (V7 p.129)
$$
\text{Delta}_c = e^{-\delta T}N(d_1), \qquad \text{Delta}_p = -e^{-\delta T}N(-d_1)
$$
^f-07-02-19

- Change in option value per small change in the stock, everything else constant; call delta lives in $(0, e^{-\delta T})$, put delta in $(-e^{-\delta T}, 0)$; stock delta is $+1$, short stock $-1$ (V7 p.129).
- Deep in the money, call delta drifts to 1 and put delta to $-1$; deep out, both drift to 0; the drift accelerates near expiry (V7 p.129).

**Optimal number of hedging units** (V7 p.129)
$$
N_H = -\frac{\text{Portfolio delta}}{\text{Delta}_H}
$$
^f-07-02-20

- $N_H > 0$: go long the hedging instrument; $N_H < 0$: short it; the hedging instrument can be stock (delta 1), calls, or puts (V7 p.129).
- A delta-neutral portfolio has total delta zero and is immune to very small moves only; the hedge must be rebalanced as delta changes (V7 p.129).

> [!tip] Calculator
> Short puts on 10,000 shares, put delta $-0.419$, hedge with calls of delta 0.532: portfolio delta `10000 [x] 0.419 [=]` (4,190), then `[+/-] [/] 0.532 [=]` gives $-7,876$, sell 7,876 calls.

**Delta approximation** (V7 p.130)
$$
\hat{c} - c \cong \text{Delta}_c\left(\hat{S} - S\right)
$$
^f-07-02-21

- First-order Taylor estimate of the new option price; accurate for small moves, biased low for both up and down moves on calls because the call price is convex in $S$ (V7 p.130, p.131).
- The estimation error grows with the size of the move; that error is what gamma measures (V7 p.132).

**Option gamma** (V7 p.132)
$$
\text{Gamma}_c = \text{Gamma}_p = \frac{e^{-\delta T}}{S\sigma\sqrt{T}}\, n(d_1)
$$
^f-07-02-22

- $n(d_1)$: standard normal density (lowercase); gamma is the change in delta per small change in the stock, is always non-negative, is identical for a call and its matching put (via put-call parity), and is zero for stock (V7 p.132).
- Gamma peaks near the money and shrinks deep in or out of the money; only option trades change portfolio gamma, so traders set gamma first with options, then finish delta with stock (V7 p.133).
- Gamma risk: the loss a delta hedger suffers when the price jumps instead of diffusing, leaving the linear hedge suddenly stale (V7 p.134).

**Delta-plus-gamma approximation** (V7 p.133)
$$
\hat{c} - c \approx \text{Delta}_c\left(\hat{S} - S\right) + \frac{\text{Gamma}_c}{2}\left(\hat{S} - S\right)^2
$$
^f-07-02-23

- Second-order estimate; much closer for large moves, biased low for a down move and biased high for an up move on calls (V7 p.133).
- Python check on the exhibit's parameters ($S = X = 100$, $r = 5\%$, $\sigma = 30\%$, $T = 1$): true $c(150) = 55.88$, delta-only estimate 45.44, delta-plus-gamma estimate 61.25, bracketing the truth exactly as described (V7 p.133, p.134).

Greeks summary for recall (V7 p.129, p.132, p.135, p.136, p.137):

| Greek | Measures sensitivity to | Call sign | Put sign | Where it matters most |
| --- | --- | --- | --- | --- |
| Delta | Underlying price (level) | $+$ | $-$ | Hedge sizing; ITM near 1 or $-1$, OTM near 0 |
| Gamma | Underlying price (curvature) | $+$ | $+$ | At the money, near expiry, jumps |
| Theta | Calendar time | $-$ (typically) | $-$ (typically) | Long option positions bleeding time value |
| Vega | Volatility | $+$ | $+$ | At or near the money; the largest of the five in practice |
| Rho | Risk-free rate | $+$ | $-$ | Usually minor; equal call and put values at $r = 0$ ATM |

## Worked examples

**Example 1: long call replicated with underlying and financing** (V7 p.88)
Which strategy replicates a long call in a single-period binomial framework?
B is correct: buy $h = (c^+ - c^-)/(S^+ - S^-)$ units of the underlying with financing of $-PV(-hS^- + c^-)$.
The cash flow table shows the replicating portfolio pays $c^-$ down and $c^+$ up, identical to the call in both states, because $h$ was chosen to make $-hS^- + c^- = -hS^+ + c^+$.
A uses sums instead of differences in the hedge ratio, and C short sells the underlying, which replicates a put-like exposure, not a call. ^ex-07-02-1

**Example 2: long put replicated with underlying and financing** (V7 p.89)
Which strategy replicates a long put?
A is correct: short sell $-h = -(p^+ - p^-)/(S^+ - S^-)$ units (a positive number of shares sold, since $h \le 0$) with financing $-PV(-hS^- + p^-)$, which here is lending.
The put hedge ratio is negative because $p^+ < p^-$ while $S^+ > S^-$; the terminal payoff table matches $p^-$ and $p^+$ state by state.
B buys the underlying (wrong direction for a put) and C flips the financing sign. ^ex-07-02-2

**Example 3: single-period binomial call value** (V7 p.91, p.92)
$S = 100$, $X = 100$, $r = 5.15\%$ per period, $u = 1.35$, $d = 0.74$, one period.
$S^+ = 135$, $S^- = 74$, $c^+ = \operatorname{Max}(0, 135 - 100) = 35$, $c^- = 0$.
Q1: hedge ratio $h = (35 - 0)/(135 - 74) = 0.573770$ (Python confirms), answer A.
Q2: $\pi = (1.0515 - 0.74)/(1.35 - 0.74) = 0.510656$ and $c = 0.951022[(0.510656)(35)] = 16.998$ (Python: 16.998), answer C.
No-arbitrage check: $c = 0.573770(100) + 0.951022[-0.573770(74) + 0] = 16.998$, the same value by the other route. ^ex-07-02-3

**Example 4: single-period binomial put value** (V7 p.92)
Same inputs; the put value is closest to which choice?
$p^+ = \operatorname{Max}(0, 100 - 135) = 0$, $p^- = \operatorname{Max}(0, 100 - 74) = 26$.
$p = 0.951022[(0.510656)(0) + (0.489344)(26)] = 12.10$ (Python: 12.10), answer B.
Put-call parity cross-check: $p = c - S + PV(X) = 16.998 - 100 + 95.102 = 12.10$, identical. ^ex-07-02-4

**Text demonstration: two-period call by no-arbitrage, with self-financing check** (V7 p.94, p.95)
$S = 72$, $X = 75$, $u = 1.356$, $d = 0.541$, $r = 3\%$ per period, no dividends.
Terminal stocks: $S^{++} = 132.389$, $S^{+-} = 52.819$, $S^{--} = 21.073$; only $c^{++} = 57.389$ is in the money (Python confirms all).
$\pi = (1.03 - 0.541)/(1.356 - 0.541) = 0.6$ exactly.
$h^+ = (57.389 - 0)/(132.389 - 52.819) = 0.72124$; $c^+ = (1/1.03)(0.6)(57.389) = 33.43048$; $c^- = 0$.
$h = (33.43048 - 0)/(97.632 - 38.952) = 0.56971$; $c = (1/1.03)(0.6)(33.43048) = 19.474$ (Python: 19.47407).
Replication at Time 0: buy 0.56971 shares for 41.019, borrow 21.545; at Time 1 up, the stock leg is worth 55.622 and the loan repayment 22.191, portfolio 33.431, matching $c^+$ to rounding.
Self-financing: the hedge rises to 0.72124 shares and the required borrowing becomes $-PV(-h^+S^{+-} + c^{+-}) = (1/1.03)(0.72124)(52.81891) = 36.985$ (Python: 36.98546 against the curriculum's 36.98554, a last-digit rounding difference from their rounded intermediate values); the old loan grew to exactly what the new position needs, so no fresh money enters. ^ex-07-02-5

**Example 5: two-period binomial call valuation** (V7 p.96)
$S = 50$, $X = 50$, $u = 1.356$, $d = 0.744$, $r = 5\%$ per period, European.
Q1: $\pi = (1.05 - 0.744)/(1.356 - 0.744) = 0.5$ exactly, answer C.
Q2: $c^{++} = \operatorname{Max}(0, 1.356^2 \times 50 - 50) = 41.9368$, $c^{+-} = 1.356(0.744)(50) - 50 = 0.44320$, $c^{--} = 0$.
$c = (1/1.05)^2[0.25(41.9368) + 2(0.5)(0.5)(0.4432)] = 9.71$ (Python: 9.7105), answer B; the present value factor must be squared for two periods.
Q3: put via parity: $p = c + PV(X) - S = 9.71 + 50/1.05^2 - 50 = 5.06$ (Python: 5.0620), answer A. ^ex-07-02-6

**Text demonstration: European versus American put on the same tree** (V7 p.97, p.98, p.99)
Same tree as the no-arbitrage call demo ($S = 72$, $X = 75$, $u = 1.356$, $d = 0.541$, $r = 3\%$).
European: $p^{++} = 0$, $p^{+-} = 22.18109$, $p^{--} = 53.92697$; $p^+ = (1/1.03)[0.6(0) + 0.4(22.18109)] = 8.61401$; $p^- = (1/1.03)[0.6(22.18109) + 0.4(53.92697)] = 33.86353$; $p = (1/1.03)[0.6(8.61401) + 0.4(33.86353)] = 18.16876$ (Python confirms every node, hedge ratios $-0.27876$, $-1$, $-0.43029$).
American: at the Time 1 down node the exercise value is $\operatorname{Max}(0, 75 - 38.952) = 36.048 > 33.86353$, an early exercise premium of 2.18447 at that node; replacing the node value gives $P = (1/1.03)[0.6(8.61401) + 0.4(36.048)] = 19.017$ (Python: 19.01710), an early exercise premium at Time 0 of $19.02 - 18.17 = 0.85$ (Python: 0.84834).
The lesson: American puts cannot be valued from terminal payoffs alone; the exercise test must run at every node on the way back (V7 p.98, p.99). ^ex-07-02-7

**Example 6: two-period binomial American-style put valuation** (V7 p.99, p.100)
$S_0 = 26$, $X = 25$, $u = 1.466$, $d = 0.656$, $r = 2.05\%$ per period; the early exercise premium is closest to which choice?
$\pi = (1.0205 - 0.656)/(1.466 - 0.656) = 0.45$; European nodes: $p^+ = 0$, $p^- = 7.44360$, $p = 4.01174$ (Python confirms).
Exercise value at Time 1 down: $\operatorname{Max}(0, 25 - 17.056) = 7.944 > 7.44360$ (node premium 0.5004), so replace it.
$P = (1/1.0205)[0.45(0) + 0.55(7.944)] = 4.28$ (Python: 4.28143), and the Time 0 hedge ratio steepens from $-0.35345$ to $-0.37721$.
Early exercise premium $= 4.28 - 4.01 = 0.27$ (Python: 0.2697), answer A. ^ex-07-02-8

**Text demonstration: American call on a dividend payer (escrow method)** (V7 p.100, p.101)
$S = 100$, $X = 95$, $r = 1\%$ per period, a US$3 dividend at Time 1, $u = 1.224$, $d = 0.796$.
Escrow: $\gamma = 3/1.01 = 2.970297$, so $\hat{S} = 97.0297$ and $\hat{S}^+ = 97.0297(1.224) = 118.7644$ (Python confirms).
At the Time 1 up node the cum-dividend exercise value is $\operatorname{Max}(0, 118.7644 + 3 - 95) = 26.7644$, while the model (ex-dividend) value is 24.9344 (Python: 24.9344 with $\pi = 0.5$), so the American call is exercised early to capture the dividend.
Replacing the node value lifts the Time 0 call from 12.3438 (European) to 13.2497 (American), and the hedge ratio from 0.6004 to 0.6445 (Python confirms all four).
Without dividends this could never happen: an American call on a non-dividend stock always trades above exercise value, so it is sold, not exercised (V7 p.97). ^ex-07-02-9

**Example 7: comprehensive two-period binomial valuation** (V7 p.101 to p.106)
$S = 7.35$ (AUD), $X = 8.0$, $r = 4.35\%$ per period, $u = 1.445$, $d = 0.715$, no dividends.
Q1 (European values): $\pi = (1.0435 - 0.715)/(1.445 - 0.715) = 0.45$.
Payoffs: $c^{++} = 7.347$, all other calls zero; $p^{++} = 0$, $p^{+-} = 0.406$, $p^{--} = 4.24$ (Python: 7.3470, 0.4062, 4.2425).
Time 1: $c^+ = 0.958313(0.45)(7.347) = 3.17$, $c^- = 0$; $p^+ = 0.958313[0.55(0.406)] = 0.214$, $p^- = 0.958313[0.45(0.406) + 0.55(4.24)] = 2.41$ (Python: 3.1683, 0.2141, 2.4113).
Time 0: $c = 0.91836[0.45^2(7.347)] = 1.37$ and $p = 0.91836[2(0.45)(0.55)(0.406) + 0.55^2(4.24)] = 1.36$ (Python: 1.3663 and 1.3632).
Call and put are nearly equal by design: $S = PV(X)$ here ($7.35 = 8.0/1.0435^2$), and parity says $c - p = S - PV(X)$.
Q2 (hedge ratios and interpretation): $h_c^+ = 7.347/(15.347 - 7.594) = 0.9476$, $h_c^- = 0$, $h_p^+ = -0.406/7.753 = -0.0524$, $h_p^- = -1.0$; at Time 0, $h_c = 3.1684/5.366 = 0.5905$ and $h_p = -0.4095$ (Python confirms; it returns $h_p^+ = -0.05239$ against the printed $-0.05237$, rounding in the printed $S$ values).
Interpretations verified by replication: $c^+ = 0.9476(10.621) - 6.8961 = 3.1684$, long shares partially financed by a loan; $p^+ = 0.77022 - 0.05237(10.621) = 0.214$, lending financed partly by a short sale (Python reproduces each leg).
Q3 (American): calls match the European values everywhere (no dividends, all exercise values below model values).
For the put, $p_{EV}^- = \operatorname{Max}(0, 8 - 5.255) = 2.745 > 2.41$, so replace it; the Time 0 hedge steepens to $h_p = (0.214 - 2.745)/5.366 = -0.4717$ and $P = (1/1.0435)[0.45(0.214) + 0.55(2.745)] = 1.54$ (Python: 1.5390), against 1.36 European. ^ex-07-02-10

**Example 8: option on interest rates** (V7 p.107, p.108, p.109)
Two-year European call and put on the one-year spot rate, notional US$1,000,000, exercise rate 3.25%, RN probability 0.50, on the lattice: Time 0 rate 3.0454% (one-year bond value 0.970446), Time 1 rates 3.9084% (0.962386) and 2.6034% (0.974627), Time 2 rates 3.9706%, 3.2542%, 2.2593%.
Terminal payoffs per US$1: $c^{++} = 0.039706 - 0.0325 = 0.007206$, $c^{+-} = 0.000042$, $c^{--} = 0$; $p^{++} = p^{+-} = 0$, $p^{--} = 0.0325 - 0.022593 = 0.009907$.
Time 1, discounting at each node's own bond value: $c^+ = 0.962386(0.5)(0.007206 + 0.000042) = 0.003488$; $c^- = 0.974627(0.5)(0.000042) = 0.00002$; $p^- = 0.974627(0.5)(0.009907) = 0.004828$ (Python confirms all).
Time 0: $c = 0.970446(0.5)(0.003488 + 0.00002) = 0.00170216$ and $p = 0.970446(0.5)(0.004828) = 0.00234266$, so US$1,702.16 and US$2,342.66 on the notional.
Python at full precision gets US$1,702.24 and US$2,342.57; the curriculum's figures carry the rounded Time 1 values forward, an immaterial difference worth recognizing on exam day.
The key mechanics: 50/50 probabilities, and a discount factor that changes node by node because the rate is the underlying (V7 p.108). ^ex-07-02-11

**Example 9: BSM model assumptions** (V7 p.112)
Which statement pair is consistent with BSM?
C is correct: volatility is assumed known and constant ("predicted with certainty"), and no arbitrage opportunities exist.
A fails twice (the return, not the price, is normally distributed, and GBM forbids jumps); B fails twice (no frictions such as brokerage costs, and trading is continuous). ^ex-07-02-12

**Example 10: BSM component interpretation** (V7 p.115, p.116)
$S = 100$, $X = 100$, $r = 5\%$, $T = 1$, $\sigma = 30\%$; given $PV(X) = 95.123$, $d_1 = 0.317$, $d_2 = 0.017$, $N(d_1) = 0.624$, $N(d_2) = 0.507$, $c = 14.23$, $p = 9.35$ (Python from raw inputs: $d_1 = 0.3167$, $d_2 = 0.0167$, $c = 14.23$, $p = 9.35$).
Q1: replicate the long call by buying $n_S = N(d_1) = 0.624$ shares and shorting $n_B = -N(d_2) = -0.507$ zero-coupon bonds at $B = 95.123$; cost $0.624(100) - 0.507(95.123) = 14.17$, the call value up to the rounding in the N values (answer B).
Q2: replicate the long put by shorting $0.376$ shares ($n_S = -N(-d_1)$) and buying $0.493$ bonds ($n_B = N(-d_2)$); cost $-0.376(100) + 0.493(95.123) = 9.30 \approx 9.35$ (answer C).
Bonus interpretation: $N(d_2) = 0.507$ is the RN probability this call expires in the money (V7 p.116). ^ex-07-02-13

**Example 11: BSM applied to equities** (V7 p.117, p.118)
$S = 60$, $X = 60$, $r = 2\%$, $T = 0.5$, $\delta = 2\%$, $\sigma = 45\%$.
Q1: the call is $Se^{-\delta T}N(d_1) - Xe^{-rT}N(d_2)$, answer B.
Q2: the put is $Xe^{-rT}N(-d_2) - Se^{-\delta T}N(-d_1)$, answer C.
Q3: setting $\delta = 0$ changes the values because $d_1$, $d_2$, and the stock component are all dividend-adjusted, answer C; the adjustment multiplies the stock, never the exercise price. ^ex-07-02-14

**Example 12: BSM inputs for stock options** (V7 p.118)
Bank of China shares at HKD4.41; sell three-month calls struck at 4.60; risk-free 1.60%, dividend yield 0.24%, volatility 28%.
B is correct: inputs are $S = 4.41$, $X = 4.60$, $T = 0.25$ (three months in years), $r = 0.016$, $\delta = 0.0024$, $\sigma = 0.28$.
A swaps spot and strike and leaves T in months; C sets the strike at spot and mangles T. ^ex-07-02-15

**Example 13: BSM applied to currency options** (V7 p.119, p.120)
Japanese exporter, spot 135 yen per euro, buys an at-the-money-spot euro put; Japanese rate 0.25%, European rate 1.00%.
Q1: underlying and exercise are both 135 (at the money spot means $X = S$), answer B; the pair is quoted in the domestic currency (yen) per unit of foreign (euro).
Q2: the risk-free rate is the domestic (Japanese) 0.25% and the carry rate is the foreign (European) 1.00%, answer A; the foreign rate is the carry benefit because foreign currency held can earn it. ^ex-07-02-16

**Example 14: European options on a futures index** (V7 p.121, p.122)
S&P 500 spot 1,860; 0.25-year futures at 1,851.65; $X = 1{,}860$, $r = 0.2\%$, $T = 0.25$, $\sigma = 15\%$, dividend yield 2.0%; given $N(d_1) = 0.491$, $N(d_2) = 0.461$, $c = 51.41$, $p = 59.76$ (Python from raw inputs: $N(d_1) = 0.491$, $N(d_2) = 0.461$, $c = 51.41$, $p = 59.76$).
Q1: the call is the present value of the futures price times 0.491 minus the exercise price times 0.461, answer B.
Q2: the put is the present value of the exercise price times 0.539 minus the futures price times 0.509, answer A.
Q3: the underlying is the futures price 1,851.65, not the spot 1,860, and the exercise price is 1,860, answer A; the dividend yield never enters Black directly because the futures price already embeds the carry (V7 p.120, p.122). ^ex-07-02-17

**Example 15: European interest rate options** (V7 p.125)
On 15 May you plan to borrow S$10,000,000 on 15 June for three months; three-month SORA is 0.55%, the 15 June to 15 September FRA rate is 0.68%; you buy an interest rate call struck at 0.60%.
Q1: the underlying rate in the Black-type model is the FRA rate 0.68% (a forward, never the spot rate), answer B.
Q2: the discount period runs 15 May to 15 September, the FRA's maturity date, answer C; the payoff is determined on 15 June but paid on 15 September (advanced set, settled in arrears), so discounting must cover $t_{j-1} + t_m$ (V7 p.123, p.125). ^ex-07-02-18

**Example 16: European swaptions** (V7 p.128)
Australian floating-rate borrower fears tightening within three months; buys a swaption expiring in three months on a five-year swap; three-month forward five-year swap rate 2.65%, current five-year swap rate 2.55%, three-month risk-free 2.25%.
A is correct: the underlying is the three-month forward, five-year swap rate (2.65%).
B is wrong because the current five-year swap rate is not the discount rate; C is wrong because $T = 0.25$ (the option's life), not the swap's five years.
Direction check: fearing higher rates, the borrower wants the right to pay fixed, a payer swaption. ^ex-07-02-19

**Example 17: delta hedging a written call book** (V7 p.130)
Short calls on 1,000 Apple shares at $S = 125$ with call delta 0.50; buying 500 shares delta-hedges the book (a US$0.10 rise costs US$50 on the calls and earns US$50 on the shares).
The incorrect statement is A: selling puts creates positive delta (short put delta is $+0.4$-ish), so the hedge is to short sell stock, not buy it.
B and C are true: call delta is non-negative, put delta non-positive, and delta hedging is neutralizing exposure to the underlying. ^ex-07-02-20

**Example 18: delta hedging with stock or calls** (V7 p.131, p.132)
$S = 100$, $X = 100$, $r = 5\%$, $T = 1$, $\sigma = 30\%$, $\delta = 5\%$; $\text{Delta}_c = 0.532$, $\text{Delta}_p = -0.419$; the book is short puts on 10,000 shares.
Q1: portfolio delta $= 10{,}000 \times 0.419 = +4{,}190$ (short put flips the sign), so $N_H = -4{,}190/1 = -4{,}190$: short sell 4,190 shares (Python: $\text{Delta}_c = 0.532$, $\text{Delta}_p = -0.419$ from the raw inputs), answer B.
Q2: hedging with calls, $N_H = -4{,}190/0.532 = -7{,}876$: sell 7,876 calls (Python: $-7{,}875.9$), answer A.
Q3: delta is the change in option value for a small change in the stock, everything else constant, answer B; curvature is gamma, and the probability of expiring in the money is $N(d_2)$, not delta. ^ex-07-02-21

**Example 19: gamma risk in option trading** (V7 p.134)
Short one call, delta-hedged with stock; which statement is true?
B is correct: buying any option (call or put) adds gamma, so a purchase raises overall gamma.
A is wrong because a short option position is short gamma (stock has none, so the hedge does not help); C is wrong for the same reason, and with negative gamma, large moves in either direction hurt, they do not help. ^ex-07-02-22

**Example 20: implied volatility within one market** (V7 p.141)
FTSE futures at 6,850; OTM puts offered at 190 points (16% implied volatility) and ATM puts at 280 points (15.2%); why does the client want quotes in implied volatility?
C is correct: volatility units both (A) neutralize moneyness and maturity so options can be compared for relative value, and (B) reveal where implied volatility is trading so the client can revalue her existing book at current market volatilities. ^ex-07-02-23

**Example 21: implied volatility across markets** (V7 p.141)
Dealer offers a three-month ATM FTSE call at 19% implied volatility and a one-month ITM Vodafone put at 24%; the trader thinks fair levels are 25% and 20% respectively.
B is correct: buy the FTSE call (implied 19% below her 25% view, so it is cheap and should rise) and sell the VOD put (implied 24% above her 20% view, so it is rich and should fall).
A buys the rich put and C sells the cheap call; both fight her own forecast on one leg. ^ex-07-02-24

## Item-set patterns

> [!warning] Trap 1: hedge ratio direction and ingredients
> The vignette gives $u$, $d$, $S$, $X$ and asks for the hedge ratio or the replicating trades.
> Correct: compute the state payoffs first, then $h = (c^+ - c^-)/(S^+ - S^-)$; calls have $h \ge 0$ (buy shares, borrow), puts $h \le 0$ (short shares, lend) (V7 p.87, p.89).
> Distractors invert the ratio (denominator over numerator), use terminal instead of next-period option values, or swap the call and put trade directions; the inverted ratio is recognizable because it exceeds 1.

> [!warning] Trap 2: the risk-neutral probability
> The stem asks for $\pi$ or for what the expectations approach assumes.
> Correct: $\pi = (1 + r - d)/(u - d)$ with $u = S^+/S$ and $d = S^-/S$ if not given; the expectation uses RN probabilities and discounts at the risk-free rate, and $\pi$ does not change when the option's own strike changes (V7 p.90, p.91, p.154).
> Distractors include $(S - S^-)/(S^+ - S^-) = 0.40$ in the Alpha problem (prices without the interest factor), real-world probabilities, or the claim that a new exercise price changes $\pi$ (it changes payoffs only).

> [!warning] Trap 3: forgetting the squared discount factor or a probability
> A two-period European value is requested from terminal payoffs.
> Correct: weight by $\pi^2$, $2\pi(1-\pi)$, $(1-\pi)^2$ and discount by $1/(1+r)^2$ (V7 p.95, p.96).
> Distractors discount only one period, drop the 2 in the middle weight, or present the undiscounted expected payoff (Beta Q5's 5.12 is exactly $0.46^2 \times 24.22$); an answer above the discounted expectation of the maximum payoff is arithmetically impossible.

> [!warning] Trap 4: American exercise mechanics
> An American option is valued on a two-period tree, or the early exercise premium is requested.
> Correct: roll back one node at a time, replace any node value with a larger exercise value, and only then discount to Time 0; premium = American minus European value (V7 p.98, p.99).
> Distractors are the untouched European value (Beta Q6's 4.53), the exercise value discounted straight to Time 0 without probability weighting (9.60/1.03 = 9.32), and applying early exercise to calls on non-dividend stocks (never optimal); remember the two legitimate cases are deep ITM puts and dividend-capturing calls (V7 p.97, p.101, p.146).

> [!warning] Trap 5: BSM component matching
> The stem asks which portfolio replicates a call or put, or what $N(d_1)$ and $N(d_2)$ mean.
> Correct: call = long $N(d_1)$ shares, short $N(d_2)$ zeros priced at $e^{-rT}X$; put = short $N(-d_1)$ shares, long $N(-d_2)$ zeros; $N(d_2)$ is the RN probability the call expires ITM; delta is $e^{-\delta T}N(d_1)$, not a probability (V7 p.114, p.116, p.129).
> Distractors use the raw $d_1$, $d_2$ values as quantities (TCB Q10 choice A), use $N(d_2)$ where $N(-d_2)$ belongs, or call delta "the probability of expiring in the money".

> [!warning] Trap 6: which input feeds which model
> A table offers spot, futures, FRA, and several rates; the question asks for the correct underlying and discount rate.
> Correct: BSM equity uses spot with $\gamma = \delta$; BSM currency uses the spot FX rate (domestic per foreign) with $r$ domestic and $\gamma = r^f$ foreign; Black futures uses the futures price with the risk-free rate (dividend yield already inside the futures price); interest rate options use the FRA rate and discount to $t_{j-1} + t_m$; swaptions use the forward swap rate with $T$ equal to the option's life (V7 p.117, p.119, p.120, p.123, p.126).
> Distractors are the spot index instead of the futures price, the dividend yield as discount rate, the current spot MRR or spot swap rate instead of the forward, and the swap tenor as $T$.

> [!warning] Trap 7: delta hedge arithmetic and signs
> A book of long or short options must be delta-hedged with stock or with other options.
> Correct: portfolio delta first (flip the option delta's sign for short positions), then $N_H = -\text{Portfolio delta}/\text{Delta}_H$; negative $N_H$ means sell the hedging instrument (V7 p.129, p.131).
> Distractors forget the sign flip on a short position, divide by the wrong instrument's delta, or hedge a long-stock book by selling puts (selling puts adds positive delta, worsening the exposure); selling calls is the classic long-stock hedge (V7 p.155).

> [!warning] Trap 8: implied volatility direction
> A model price computed from historical volatility differs from the market price.
> Correct: market price below the model price means implied volatility is below the volatility input, and vice versa; option price and implied volatility map one-to-one (V7 p.140, p.155).
> The distractor states the opposite direction, or claims implied and historical volatility measure the same thing; implied is forward-looking, extracted from prices, while historical looks back (V7 p.138, p.144).

> [!warning] Trap 9: swaption identities
> The stem describes a hedger or a callable bond and asks for the equivalent option position.
> Correct: fear rising rates as a future borrower = buy a payer swaption; fear falling rates as a future fixed receiver = buy a receiver swaption; long callable bond = long straight bond + short receiver swaption; long cap + short floor at the swap rate = receive-floating, pay-fixed swap at zero cost (V7 p.124, p.125, p.126, p.127).
> Distractors swap payer and receiver, attach the cap to the lender instead of the borrower, or make the callable bond long (not short) the receiver swaption.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Valuation-of-Contingent-Claims-Practice-Problems]]

## Cross-links

- [[LM01-Pricing-and-Valuation-of-Forward-Commitments]]: supplies the carry arbitrage machinery behind every underlying used here; the FRA rates and forward swap rates that feed the Black interest rate and swaption models are priced in LM1, and Black is BSM applied to a forward that already embeds the carry.
- [[LM02-The-Arbitrage-Free-Valuation-Framework]]: the fixed-income binomial tree is the same backward induction used for the interest rate options in this module; there the probabilities are fixed at 0.5/0.5 and the tree is calibrated to the benchmark curve, exactly the lattice this module's Example 8 consumes.
- [[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options]]: values callable and putable bonds by running this module's exercise test at every tree node, and this module's identity (callable bond = straight bond + short receiver swaption) prices the same option from the swaption side.
- [[LM05-Measuring-and-Managing-Market-Risk]]: the portfolio-management treatment of Greeks in risk systems; delta and gamma from this module become the sensitivity inputs for measuring and managing the market risk of option books.

## Self-test

Vignette A for Q1 to Q4: An analyst values two-year options on a non-dividend stock trading at 40 with a two-period binomial model.
The exercise price is 40, $u = 1.25$, $d = 0.80$, and the risk-free rate is 2% per period.
She computes $S^+ = 50$, $S^- = 32$, $S^{++} = 62.50$, $S^{+-} = 40$, $S^{--} = 25.60$.

> [!question] Q1
> The risk-neutral probability of an up move is closest to:
> A. 0.44.
> B. 0.49.
> C. 0.56.

> [!question] Q2
> The value of the European call is closest to:
> A. 5.17.
> B. 5.27.
> C. 5.38.

> [!question] Q3
> The hedge ratio for the call at Time 0 is closest to:
> A. 0.49.
> B. 0.60.
> C. 1.00.

> [!question] Q4
> The early exercise premium on an otherwise identical American put is closest to:
> A. 0.
> B. 0.39.
> C. 0.78.

Vignette B for Q5 to Q7: A structurer values three products: (1) a six-month European call on a stock paying a 3% continuous dividend yield, (2) a European put on an equity index futures contract, and (3) an option for a corporate treasurer who will issue five-year fixed-rate debt in six months and fears rising swap rates.
For product 1 the model reports $N(d_1) = 0.58$ and $N(d_2) = 0.52$.

> [!question] Q5
> The portfolio that replicates the long call in product 1 buys a number of shares equal to:
> A. $0.58$.
> B. $e^{-0.03 \times 0.5} \times 0.58$.
> C. $e^{-0.03 \times 0.5} \times 0.52$.

> [!question] Q6
> For product 2, the Black model values the put as the present value of:
> A. $XN(-d_2) - F_0(T)N(-d_1)$.
> B. $XN(d_2) - F_0(T)N(d_1)$.
> C. $F_0(T)N(-d_1) - XN(-d_2)$, discounted at the dividend yield.

> [!question] Q7
> The most appropriate product 3 position, and its underlying, are:
> A. a receiver swaption on the current five-year swap rate.
> B. a payer swaption on the six-month forward, five-year swap rate.
> C. an interest rate floor on the six-month FRA rate.

Vignette C for Q8 to Q10: A derivatives desk is short calls on 20,000 shares of one stock; the call delta is 0.60 and the call gamma is 0.03.
The desk head wants the book delta neutral and asks about the residual risks; separately, a dealer quotes one-month ATM implied volatility at 18% while the desk forecasts 24%.

> [!question] Q8
> To delta hedge with stock, the desk should:
> A. buy 12,000 shares.
> B. sell 12,000 shares.
> C. buy 20,000 shares.

> [!question] Q9
> After the stock hedge, a sudden large jump in the stock price (either direction) will most likely produce:
> A. a gain, because the book is long gamma.
> B. no material effect, because the book is delta neutral.
> C. a loss, because the book is short gamma and stock carries none.

> [!question] Q10
> Consistent with the desk's volatility view, the best trade on the dealer's quote is to:
> A. buy the ATM options, since implied volatility is below the forecast.
> B. sell the ATM options, since implied volatility is below the forecast.
> C. do nothing, since implied and historical volatility always converge.

> [!success]- Answer key
> Q1: B.
> $\pi = (1.02 - 0.80)/(1.25 - 0.80) = 0.22/0.45 = 0.4889$ (Python: 0.4889).
> A is $1 - \pi$ rounded down and C is $1 - \pi$ mis-signed territory; only the $(1 + r - d)/(u - d)$ construction is valid.
> Q2: A.
> $c^{++} = 22.50$, others zero; $c = 0.4889^2(22.5)/1.02^2 = 5.169$ (Python: 5.1690).
> B forgets to square the discount factor on the undiscounted-then-once-discounted path (Python: $\pi^2 c^{++}/1.02 = 5.272$); C is the undiscounted expected payoff 5.378.
> Q3: B.
> $c^+ = 0.4889(22.5)/1.02 = 10.784$, $c^- = 0$, so $h = 10.784/(50 - 32) = 0.599$ (Python: 0.5991).
> A is the RN probability masquerading as a hedge ratio; C is the Time 1 up-node hedge ratio $22.5/22.5 = 1.0$, the wrong node.
> Q4: B.
> European put by parity: $p = 5.169 + 40/1.02^2 - 40 = 3.616$ (Python: 3.6157).
> At Time 1 down, $p^- = 0.5111(14.4)/1.02 = 7.216$ but exercise pays $40 - 32 = 8.00$, so replace; $P = 0.5111(8.00)/1.02 = 4.009$ (Python: 4.0087) and the premium is $4.009 - 3.616 = 0.39$ (Python: 0.3930).
> A denies the deep-ITM put's interest advantage; C double-counts by comparing the American value to zero time-value instead of the European value.
> Q5: B.
> With a continuous dividend yield the share count is $n_S = e^{-\delta T}N(d_1) = e^{-0.015}(0.58)$; the dividend trims the shares needed because the stock leg earns the yield the option does not (V7 p.117).
> A ignores the carry adjustment; C multiplies the yield factor into the bond count $N(d_2)$, which is unaffected.
> Q6: A.
> Black put: $p = e^{-rT}[XN(-d_2) - F_0(T)N(-d_1)]$ (V7 p.120).
> B uses the call's probability arguments; C reverses the components and discounts at the dividend yield, which never appears in Black.
> Q7: B.
> A future fixed-rate payer hurt by rising rates buys the right to pay fixed: a payer swaption whose underlying is the forward swap rate for the six-month-forward five-year swap (V7 p.126, p.128).
> A profits from falling rates; C is a strip of puts on short rates, hedging a floating-rate lender, not a future fixed-rate issuer.
> Q8: A.
> Portfolio delta $= -20{,}000 \times 0.60 = -12{,}000$; $N_H = -(-12{,}000)/1 = +12{,}000$: buy 12,000 shares (V7 p.129).
> B doubles the exposure; C hedges the share count instead of the delta-weighted exposure.
> Q9: C.
> Short calls carry negative gamma and the stock hedge adds none, so any jump moves the true option value away from the linear hedge and the desk loses either way (V7 p.133, p.134).
> A describes a long-option book; B is only true for infinitesimal moves, which is precisely what a jump is not.
> Q10: A.
> The dealer's 18% implied is below the 24% forecast, so the options are cheap relative to the desk's view; buy them (long vega) and profit if implied volatility rises toward the forecast (V7 p.141).
> B sells cheap volatility; C invents a convergence law that does not exist, since implied is forward-looking and historical backward-looking (V7 p.138).

## Flashcards

#flashcards/cfa-l2/07-Derivatives/lm02

Arbitrageur's two rules (option pricing)::Do not use your own money, and do not take any price risk (V7 p.82).
Law of one price (contingent claims)::Two investments with the same future cash flows in every state must have the same current price (V7 p.82).
Time value of an option::The market value of the payoff asymmetry, always non-negative, and zero at expiration (V7 p.85).
Single-period call hedge ratio::{{h = (c+ - c-)/(S+ - S-)}}, non-negative for calls (V7 p.87).
Why is the put hedge ratio negative?::Put values fall when the underlying rises, so replication requires short selling the underlying and lending (V7 p.89).
No-arbitrage single-period call value::{{c = hS + PV(-hS- + c-)}}, a leveraged position in the underlying (V7 p.88).
Risk-neutral probability of an up move::{{pi = (1 + r - d)/(u - d)}} with u and d the gross up and down returns (V7 p.90).
Two ways the expectations approach differs from DCF::The probability is the objective risk-neutral one, not investor belief, and the discount rate is the risk-free rate, not risk adjusted (V7 p.91).
Does changing an option's strike change the risk-neutral probabilities?::No, the RN probabilities come from the underlying's price process, never from the option's contract terms (V7 p.154).
Put-call parity::{{S + p = PV(X) + c}} at the same strike and expiry, model-independent (V7 p.92).
Recombining lattice::Up-down equals down-up, so an n-step tree ends with n+1 nodes instead of 2 to the n (V7 p.93).
Self-financing::The dynamically rebalanced replicating portfolio never needs new outside funds; extra shares are bought with exactly the extra borrowing generated (V7 p.93, p.95).
Dynamic replication::The option payoff is matched exactly through a planned trading strategy whose composition changes at every node (V7 p.94).
Two-period European call by expectations::Weight terminal payoffs by pi squared, 2 pi (1 - pi), and (1 - pi) squared, then discount two periods (V7 p.95).
Why is the middle binomial weight doubled?::Two paths (up-down and down-up) reach the middle terminal node (V7 p.95).
When is an American call exercised early?::Only to capture a dividend, just before the ex-dividend date; never on a non-dividend stock (V7 p.97, p.101).
When is an American put exercised early?::Deep in the money, when interest on the exercise proceeds exceeds the remaining time value (V7 p.97).
Early exercise premium::American option value minus the otherwise identical European option value (V7 p.98).
How do you value an American option on a tree?::Work backward node by node, replacing the model value with the exercise value whenever exercise is worth more (V7 p.99, p.109).
Escrow method::Model the randomness on S-hat, the stock price minus the present value of known dividends (V7 p.100).
RN probability used on interest rate option lattices::Fixed at 50 percent for up and down at every node (V7 p.106).
What is unusual about discounting on a rate lattice?::The discount factor differs at every node because the interest rate is itself the underlying (V7 p.108).
An interest rate call is in the money when::The current spot rate is above the exercise rate (V7 p.107).
BSM stochastic process assumption::Geometric Brownian motion, so continuously compounded returns are normal, prices lognormal, no jumps, never negative (V7 p.110, p.111).
BSM rate and volatility assumptions::A known constant continuously compounded risk-free rate and a known constant return volatility, with any yield paid as a constant continuous rate (V7 p.112).
BSM call formula::{{c = S N(d1) - e^(-rT) X N(d2)}} (V7 p.112).
BSM call anatomy::Stock component S N(d1) minus bond component e^(-rT) X N(d2); the put reverses them with negated arguments (V7 p.114).
Replicating a BSM call::Buy N(d1) shares, short N(d2) zero-coupon bonds priced at e^(-rT) X (V7 p.114).
Replicating a BSM put::Short N(-d1) shares, buy N(-d2) zero-coupon bonds (V7 p.114).
Interpretation of N(d2)::The risk-neutral probability that a call expires in the money (V7 p.116).
Why is a short put over-leveraged stock?::The short put position is long shares financed by borrowing that exceeds 100 percent of the stock cost (V7 p.114).
Carry benefit gamma for stock and currency options::Dividend yield delta for stocks, foreign risk-free rate for currencies (V7 p.117, p.119).
Effect of higher carry benefits on option values::Calls fall and puts rise, because the expected future underlying value is lower (V7 p.116).
Currency option quoting convention::The underlying spot rate is domestic currency per unit of foreign, with the domestic rate for discounting and the foreign rate as carry (V7 p.119).
Black model call on futures::{{c = e^(-rT) [F N(d1) - X N(d2)]}} with the futures price as underlying (V7 p.120).
Why does no carry term appear in the Black model?::A futures position is costless to carry; the futures price already embeds the underlying's carry (V7 p.120).
Underlying for an interest rate option in the standard market model::The FRA rate observed today for the period starting at option expiry (V7 p.122, p.123).
Discount horizon for an interest rate option::The FRA maturity t(j-1) + tm, not the option expiry, because rates are advanced set and settled in arrears (V7 p.123, p.124).
Interest rate cap::A strip of interest rate call options (caplets) with sequential expiries and one exercise rate; hedges a floating-rate borrower (V7 p.124).
Interest rate floor::A strip of interest rate put options (floorlets); hedges a floating-rate lender or bond investor (V7 p.124).
Long cap plus short floor struck at the swap rate equals::A receive-floating, pay-fixed swap, at zero initial cost since cap value equals floor value at that strike (V7 p.124, p.125).
Payer swaption::The right to enter a swap paying fixed and receiving floating; gains when swap rates rise (V7 p.126).
Receiver swaption::The right to enter a swap receiving fixed and paying floating; gains when swap rates fall (V7 p.126).
Swaption underlying and time input::The forward swap rate starting at option expiry, with T equal to the swaption's own life (V7 p.126, p.128).
Why does a PVA annuity factor appear in swaption valuation?::Exercise creates an annuity of the rate difference over the swap's settlement dates, and the factor embeds all discounting (V7 p.126, p.127).
Long callable bond decomposition::Long a straight fixed-rate bond plus short a receiver swaption (V7 p.127).
Call delta and put delta::{{e^(-dT) N(d1)}} for calls and {{-e^(-dT) N(-d1)}} for puts, with d the dividend yield (V7 p.129).
Optimal hedging units::{{NH = -(portfolio delta)/(delta of hedging instrument)}}; negative means short the instrument (V7 p.129).
Where is gamma largest?::Near the money, and it grows as expiration approaches (V7 p.132).
Gamma of a call versus its matching put::Equal, by put-call parity, since the parity portfolio has constant delta (V7 p.132).
How do you change portfolio gamma?::Only by trading options; stock has zero gamma, so set gamma first with options, then finish delta with stock (V7 p.133).
Gamma risk::The loss a delta hedger takes when the underlying jumps rather than moving continuously, leaving the linear hedge stale (V7 p.134).
Delta-plus-gamma approximation bias::Biased low for a down move and high for an up move on calls, but far closer than delta alone for large moves (V7 p.133).
Sign of theta::Typically negative for options; the value bleeds as expiration approaches, fastest for at-the-money options near expiry (V7 p.135).
Which BSM input is the option value most sensitive to?::Volatility; vega is positive and identical for a call and its matching put (V7 p.136).
Rho signs::Positive for calls (options defer paying the strike) and negative for puts (options defer receiving sale proceeds) (V7 p.137).
Implied volatility::The volatility that makes the option model reproduce the observed market price; a one-to-one map from price (V7 p.138, p.140).
Volatility smile versus term structure versus surface::Smile is implied volatility across strikes, term structure across expiries, and the surface plots both at once; BSM predicts a flat surface (V7 p.139).
Model price above market price implies::The implied volatility is below the volatility used in the model (V7 p.155).
Why do traders quote options in volatility units?::Volatility strips out moneyness and maturity, so options with different strikes and expiries become directly comparable (V7 p.140, p.141).

## Common mistakes

1. Inverting the hedge ratio or building it from terminal payoffs instead of the next period's option values; the ratio is always next-period option spread over underlying spread (V7 p.87).
2. Computing the risk-neutral probability without the interest factor, as $(S - S^-)/(S^+ - S^-)$, or treating it as a real-world probability that shifts with the option's strike (V7 p.90, p.152, p.154).
3. Discounting a two-period expectation by one period only, or dropping the 2 in the $2\pi(1-\pi)$ middle weight (V7 p.95, p.96).
4. Valuing an American option from terminal payoffs with formula 8; American values require the node-by-node exercise test, and the European shortcut is a designed distractor (V7 p.98, p.99, p.153).
5. Exercising an American call on a non-dividend stock early, or forgetting that dividend capture can justify early exercise just before the ex-dividend date (V7 p.97, p.101).
6. Using $d_1$ and $d_2$ instead of $N(d_1)$ and $N(d_2)$ as the replicating quantities, or calling delta the probability of expiring in the money ($N(d_2)$ holds that role, and only under RN probabilities) (V7 p.114, p.116, p.129, p.154).
7. Feeding the spot index into the Black model or the futures price into BSM; Black takes the forward or futures price and discounts at the risk-free rate, with no explicit dividend input (V7 p.120, p.155).
8. Discounting an interest rate option only to its expiry date; settlement in arrears pushes the discount horizon to $t_{j-1} + t_m$, while $d_1$ still uses $t_{j-1}$ (V7 p.123, p.124).
9. Using the spot MRR or the current swap rate as the underlying; interest rate options ride the FRA rate and swaptions ride the forward swap rate (V7 p.123, p.126, p.155).
10. Botching the delta hedge sign: forgetting to flip delta for short positions, or hedging long stock by selling puts (which adds delta) instead of selling calls (V7 p.129, p.131, p.155).
11. Treating a delta-neutral book as riskless; gamma (jumps), vega (volatility shifts), and theta (time) all remain, and a short-option book loses on large moves in either direction (V7 p.133, p.134).
12. Reading implied volatility backward: a market price below the model price means implied volatility is below the model's input, not above (V7 p.155).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "07-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
