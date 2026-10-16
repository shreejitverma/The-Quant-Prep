---
type: problem-set
track: [quant-trader, quant-research, quant-dev]
tier: core
status: solid
prereqs: [order-book-imbalance-and-microprice, market-impact-models]
est_hours: 4
sources: [Harris (2003) Trading and Exchanges - Market Microstructure for Practitioners. Oxford University Press, Bouchaud Bonart Donier and Gould (2018) Trades Quotes and Prices. Cambridge University Press, Hasbrouck (2007) Empirical Market Microstructure. Oxford University Press, Kyle (1985) Continuous Auctions and Insider Trading. Econometrica 53(6) 1315-1335, Almgren and Chriss (2000) Optimal Execution of Portfolio Transactions. Journal of Risk 3(2) 5-39, Perold (1988) The Implementation Shortfall. Journal of Portfolio Management 14(3) 4-9, Almgren Thum Hauptmann and Li (2005) Direct Estimation of Equity Market Impact. Risk 18(7)]
---

# Microstructure Problem Set

## TL;DR

- Most microstructure interview questions reduce to a handful of formulas: Roll's $c = \sqrt{-\text{Cov}}$, Glosten-Milgrom's conditional expectations, Kyle's $\lambda = \sigma_v/(2\sigma_u)$, the square-root law, the Almgren-Chriss sinh trajectory and Perold's shortfall decomposition.
- Always state the sign convention (buy positive) and the unit (dollars, ticks, basis points) before computing.
- Separate what is transitory (spread, temporary impact, bounce) from what is permanent (information, permanent impact); most "trick" questions hinge on that split.
- Fee and rule questions need the net price and the current rule text with its date; numeric questions need the arithmetic said out loud.

## Learning objectives

- Answer microstructure questions from market-making and HFT interviews.
- Solve spread, informed-trading, impact, execution, TCA, auction, fee and latency problems quickly and with the right units.

## Core concepts

### Formula sheet

| Topic | Result | Note |
| :--- | :--- | :--- |
| Roll | $c = \sqrt{-\text{Cov}(\Delta p_t, \Delta p_{t-1})}$, spread $2c$ | [Spread Models](03-Spread-Models-Roll-and-Glosten-Milgrom.md) |
| Glosten-Milgrom | ask $= \mathbb{E}[V \mid \text{buy}]$, bid $= \mathbb{E}[V \mid \text{sell}]$; symmetric half-spread $\mu(V_H - V_L)/2$ | [Spread Models](03-Spread-Models-Roll-and-Glosten-Milgrom.md) |
| Spread decomposition | $\Delta p_t = (\theta + \phi) q_t - \phi q_{t-1} + u_t$ | [Spread Models](03-Spread-Models-Roll-and-Glosten-Milgrom.md) |
| Kyle | $\lambda = \sqrt{\Sigma_0}/(2\sigma_u)$, $\beta = \sigma_u/\sqrt{\Sigma_0}$, profit $\tfrac12\sigma_u\sqrt{\Sigma_0}$, $\text{Var}(v \mid p) = \Sigma_0/2$ | [Kyle Model](04-Kyle-Model-and-Informed-Trading.md) |
| Square-root law | $I \approx Y\sigma_D\sqrt{Q/V_D}$ | [Market Impact Models](06-Market-Impact-Models.md) |
| Almgren-Chriss | $x(t) = X\sinh(\kappa(T - t))/\sinh(\kappa T)$, $\kappa = \sqrt{\lambda\sigma^2/\eta}$ | [Almgren-Chriss](07-Optimal-Execution-Almgren-Chriss.md) |
| Perold | delay + execution + opportunity + fees = paper P&L minus real P&L | [Execution and TCA](08-Execution-Algorithms-and-TCA.md) |
| Auction | maximise $\min(D(p), S(p))$, then minimise imbalance | [Exchange Mechanics](02-Exchange-Mechanics-Auctions-and-Fees.md) |
| Latency | maker loses a race with $N$ equal racers with probability $(N-1)/N$ | [Latency Arbitrage](10-Latency-Arbitrage-and-Speed.md) |

### How to answer

1. Restate the quantity asked for, with its sign convention and unit.
2. Write the formula, then plug in, saying each intermediate number.
3. Sanity-check the magnitude (a spread in cents, an impact in basis points, a probability in $[0, 1]$).
4. Add one sentence of interpretation: what a trader would do differently because of the number.

## Worked examples

### Example 1: Glosten-Milgrom updating after sells (problems 2 and 3)

"$V \in \{48, 52\}$ equally likely, 40% of traders informed."
The half-spread is $0.4 \times 2 = 0.8$, so bid 49.2 and ask 50.8.
After one sell, $P(V_H \mid \text{sell}) = 0.5 \times 0.3/(0.5 \times 0.3 + 0.5 \times 0.7) = 0.3$, since an informed trader never sells when $V = 52$.
The next bid is the expectation after a second sell: $P(V_H) = 0.3 \times 0.3/(0.3 \times 0.3 + 0.7 \times 0.7) = 0.155172$, so the bid is $48 + 4 \times 0.155172 = 48.62069$.

### Example 2: Perold shortfall (problem 14)

"Decide to buy 50,000 at 30.00; arrival 30.05; 40,000 filled at an average of 30.20; close 30.40; fees 0.4 cents a share."
Delay $40{,}000 \times 0.05 = 2{,}000$; execution $40{,}000 \times 0.15 = 6{,}000$; opportunity $10{,}000 \times 0.40 = 4{,}000$; fees 160.
Total 12,160 dollars, or 81.07 bp of the 1,500,000 paper notional.

### Example 3: a small auction (problem 21)

Buys: 300 at the open, 1,000 at 10.02, 500 at 10.01; sells: 800 at 10.00, 600 at 10.01, 400 at 10.03.

| Price | Demand | Supply | Executable |
| ---: | ---: | ---: | ---: |
| 10.00 | 1,800 | 800 | 800 |
| 10.01 | 1,800 | 1,400 | 1,400 |
| 10.02 | 1,300 | 1,400 | 1,300 |
| 10.03 | 300 | 1,800 | 300 |

The auction clears at 10.01 with 1,400 shares and a 400-share buy imbalance.

### Example 4: Almgren-Chriss urgency (problem 12)

"$\lambda = 2 \times 10^{-6}$, $\sigma = 0.5$, $\eta = 10^{-6}$, $T = 2$ days."
$\kappa = \sqrt{2 \times 10^{-6} \times 0.25/10^{-6}} = 0.7071$ per day, and after one day the fraction left is $\sinh(0.7071)/\sinh(1.4142) = 0.3966$, against 0.5 for TWAP.

## Pitfalls

- Mixing per-share and total quantities, or dollars and basis points, in the same line.
- Forgetting the factor $\tfrac12$ in one-period Kyle or the $\sqrt{\cdot}$ in Roll.
- Quoting a Roll spread when the autocovariance is positive.
- Using the participation rate as a fraction of others' volume instead of total volume.
- Leaving the opportunity cost of unfilled shares out of a shortfall.
- Treating proposed or exempted rules (the 10-mil fee cap, the half-penny tick, rescission of Rule 611) as in force as of 2026-10.

## Interview questions

> [!question]- ms-ps-roll-spread | The first-order autocovariance of trade-price changes is $-0.0004$. Roll spread?
> 0.04: $c = \sqrt{0.0004} = 0.02$ and the spread is $2c$.

> [!question]- ms-ps-gm-quotes | $V \in \{48, 52\}$ equally likely, 40% of traders informed. Glosten-Milgrom bid and ask?
> 49.2 and 50.8: half-spread $0.4 \times (52 - 48)/2 = 0.8$.

> [!question]- ms-ps-gm-after-sell | Same model, one sell has occurred. What is the next bid?
> About 48.621.
> $P(V_H \mid \text{sell}) = 0.3$, then the bid is $\mathbb{E}[V \mid \text{two sells}]$ with $P(V_H) = 0.09/0.58 = 0.1552$.

> [!question]- ms-ps-kyle-lambda | $\sigma_v = 1.5$, $\sigma_u = 30{,}000$ shares. Kyle's lambda, beta and insider profit?
> $\lambda = 2.5 \times 10^{-5}$ per share, $\beta = 20{,}000$ shares per dollar, profit 22,500 dollars.
> $\lambda = \sigma_v/(2\sigma_u)$, $\beta = \sigma_u/\sigma_v$, profit $\sigma_v\sigma_u/2$.

> [!question]- ms-ps-kyle-flow | In that market, how far does 10,000 shares of net order flow move the price?
> 0.25 dollars: $2.5 \times 10^{-5} \times 10{,}000$.

> [!question]- ms-ps-kyle-noise | Noise-trader variance quadruples. What happens to lambda and insider profit?
> $\sigma_u$ doubles, so $\lambda$ halves to $1.25 \times 10^{-5}$ and profit doubles to 45,000; informativeness is unchanged.

> [!question]- ms-ps-kyle-posterior | $\sigma_v = 2$ in a one-period Kyle market. Posterior standard deviation of value after trading?
> About 1.414: posterior variance is $\Sigma_0/2 = 2$.

> [!question]- ms-ps-sqrt-impact | Daily vol 1.5%, order 4% of daily volume, $Y = 1$. Square-root impact?
> 30 bp: $150 \times \sqrt{0.04}$ bp.

> [!question]- ms-ps-sqrt-scaling | Under the square-root law, how much more per share does a 9% of ADV order cost than a 4% order?
> 1.5 times: $\sqrt{9/4}$.

> [!question]- ms-ps-impact-dollars | 200,000 shares of a $40 stock with 30 bp of impact. Dollar cost?
> 24,000 dollars: 30 bp of 8,000,000.

> [!question]- ms-ps-fair-pricing | Peak impact is 30 bp and impact accumulated as a square root along the order. Fair-pricing estimate of permanent impact?
> 20 bp, two thirds of the peak, the average of $\sqrt{q}$ on $[0, 1]$.

> [!question]- ms-ps-propagator-decay | With a power-law propagator $\ell^{-1/2}$, what fraction of a constant-rate metaorder's peak impact remains at four times its duration (continuum)?
> About 26.8%: $\sqrt{4} - \sqrt{3}$.

> [!question]- ms-ps-almgren-temp | Almgren et al. (2005): temporary cost $\eta\sigma(X/(VT))^{3/5}$ with $\eta = 0.142$. Daily vol 2%, $X/V = 0.2$, $T = 0.4$ days?
> About 18.74 bp: $0.142 \times 0.5^{0.6} \times 200$ bp.

> [!question]- ms-ps-ac-kappa | $\lambda = 2 \times 10^{-6}$, $\sigma = 0.5$, $\eta = 10^{-6}$, $T = 2$ days. Urgency and fraction left after one day?
> $\kappa = 0.7071$ per day; $\sinh(0.7071)/\sinh(1.4142) = 0.3966$ left, against 0.5 under TWAP.

> [!question]- ms-ps-twap-cost | Sell 500,000 shares over 2 days with linear temporary impact $\eta = 10^{-6}$ and $\sigma = 0.5$. TWAP temporary cost and cost standard deviation (continuous)?
> 125,000 dollars ($\eta X^2/T$) and about 204,124 dollars ($\sigma X\sqrt{T/3}$).

> [!question]- ms-ps-perold | Decide to buy 50,000 at 30.00, arrival 30.05, 40,000 filled at 30.20, close 30.40, fees 0.4 cents. Shortfall?
> 12,160 dollars (81.07 bp): delay 2,000, execution 6,000, opportunity 4,000, fees 160.

> [!question]- ms-ps-vwap-share | You were 25% of interval volume, averaged 30.20, and the VWAP was 30.16. True slippage against everyone else?
> About 5.33 cents: others' VWAP is $(30.16 - 0.25 \times 30.20)/0.75 = 30.1467$.

> [!question]- ms-ps-pov | Participating at 20% of total volume while others trade 400,000 shares. Your shares?
> 100,000: $0.2/0.8 \times 400{,}000$.

> [!question]- ms-ps-maker-capture | One-cent spread, 25-mil maker rebate. Round-trip capture per share and per 100 shares?
> 0.015 per share, 1.50 dollars per 100 shares.

> [!question]- ms-ps-net-price | An offer at 10.05 on a venue charging takers 30 mils and another at 10.05 paying takers 10 mils. All-in prices?
> 10.053 and 10.049; take the second first.

> [!question]- ms-ps-effective-realized | A buy at 10.05 with the mid at 10.04; five minutes later the mid is 10.06. Effective, realized, impact?
> Effective half-spread 0.01, realized -0.01, impact 0.02; the maker lost a cent.

> [!question]- ms-ps-relative-tick | One-cent tick on a $2 stock, and a 30-mil access fee on a $10 stock, in basis points?
> 50 bp and 3 bp.

> [!question]- ms-ps-auction | Buys: 300 at market, 1,000 at 10.02, 500 at 10.01. Sells: 800 at 10.00, 600 at 10.01, 400 at 10.03. Clearing price and volume?
> 10.01 with 1,400 shares and a 400-share buy imbalance (10.02 would execute only 1,300).

> [!question]- ms-ps-race | A fair-value jump of 2 cents against a half-spread of 0.5 cents on a 500-share quote, four equal racers. Maker's expected loss?
> 5.625 dollars: the sniper's 7.5-dollar gain times 3/4.

> [!question]- ms-ps-weighted-mid | Bid 50.00 x 300, ask 50.01 x 900. Imbalance and weighted mid?
> 0.25 and 50.0025: the large ask queue pulls fair value toward the bid.

> [!question]- ms-ps-markout | You buy at 20.00; the mid is 20.005 after 1 s and 19.98 after 60 s. Markouts?
> +0.5 cents at 1 s and -2 cents at 60 s: the fill was adversely selected at the longer horizon.

> [!question]- ms-ps-iso | Protected offers 15.01 x 200 and 15.02 x 300; buy 1,000 limit 15.03 with 800 offered at 15.03. ISO sweep average price?
> 15.023: 200 at 15.01, 300 at 15.02 and 500 at 15.03.

> [!question]- ms-ps-rule201 | A stock closed at 80. At what price does the Reg SHO short-sale price test trigger?
> 72: a 10% decline from the prior close.

> [!question]- ms-ps-roll-persistence | Trade signs have autocorrelation 0.6. What fraction of the true half-spread does Roll report?
> 40%: it estimates $c(1 - \rho)$.

> [!question]- ms-ps-mrr | Regress price changes on $q_t$ and $q_{t-1}$: coefficients 0.06 and -0.04. Components?
> Transitory 0.04, permanent 0.02, adverse-selection share one third.

> [!question]- ms-ps-rule-status | As of 2026-10, which of these are in force: the 10-mil access fee cap, the half-penny tick, Rule 611?
> Only Rule 611; compliance with the amended fee cap and tick is exempted until the first business day of November 2027, and the June 2026 proposal to rescind Rule 611 had not been adopted when this was written (check sec.gov).

## In this repo and SDE-Interview-Prep

- Code: [problem_set.py](code/problem_set.py) computes and asserts every number above (`python problem_set.py`).
- [Microstructure and order matching drill (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/01%20-%20Market%20%26%20Microstructure%20Fundamentals/Drill%20-%2001%20Microstructure%20and%20Order%20Matching%20Mechanics.md)

## Further reading

- Larry Harris, *Trading and Exchanges: Market Microstructure for Practitioners* (Oxford University Press, 2003).
- Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (Cambridge University Press, 2018).
- Joel Hasbrouck, *Empirical Market Microstructure* (Oxford University Press, 2007).
- Related notes: every concept note in this section, especially [Order Book Imbalance and the Microprice](11-Order-Book-Imbalance-and-Microprice.md) and [Adverse Selection and Flow Toxicity](05-Adverse-Selection-and-Flow-Toxicity.md).
