---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [limit-order-books-and-order-types]
est_hours: 4
sources: [Bouchaud Bonart Donier and Gould (2018) Trades Quotes and Prices. Cambridge University Press - chapters 10 to 13, Toth Lemperiere Deremble de Lataillade Kockelkoren and Bouchaud (2011) Anomalous Price Impact and the Critical Nature of Liquidity in Financial Markets. Physical Review X 1 021006, Almgren Thum Hauptmann and Li (2005) Direct Estimation of Equity Market Impact. Risk 18(7) 57-62 (working paper dated May 10 2005), Bouchaud Gefen Potters and Wyart (2004) Fluctuations and Response in Financial Markets - The Subtle Nature of Random Price Changes. Quantitative Finance 4(2) 176-190, Lillo and Farmer (2004) The Long Memory of the Efficient Market. Studies in Nonlinear Dynamics and Econometrics 8(3), Gatheral (2010) No-Dynamic-Arbitrage and Market Impact. Quantitative Finance 10(7) 749-759, Obizhaeva and Wang (2013) Optimal Trading Strategy and Supply/Demand Dynamics. Journal of Financial Markets 16(1) 1-32, Farmer Gerig Lillo and Waelbroeck (2013) How Efficiency Shapes Market Impact. Quantitative Finance 13(11) 1743-1758]
---

# Market Impact Models

## TL;DR

- Market impact is the price move caused by your own trading; for a metaorder (a large order split into many child orders) it is the dominant cost and it scales with volatility and with size relative to volume.
- The square-root law: peak impact $\approx Y\,\sigma_D\sqrt{Q/V_D}$ with $Y$ of order one, roughly independent of how long the metaorder took; cost per share grows like $\sqrt{Q}$ and total cost like $Q^{3/2}$.
- Temporary impact depends on trading rate and disappears when you stop; permanent impact is what remains; Almgren et al. (2005) fit linear permanent impact and a 3/5-power temporary impact on Citigroup US equity orders.
- Propagator models write the price as a sum of past trade signs times a decaying kernel $G(\ell)$; because order signs have long memory, $G$ must decay as a power law with $\beta = (1 - \gamma)/2$ for prices to stay diffusive.
- After a metaorder ends, impact decays slowly (power law), and fair-pricing arguments put the long-run impact at about two thirds of the peak for square-root impact.

## Learning objectives

- State the square-root impact law and its empirical support.
- Separate temporary and permanent impact; explain the propagator model.
- Estimate the cost of a large order from volume and volatility.
- Simulate transient impact and the diffusion constraint linking sign memory and impact decay.

## Core concepts

### Vocabulary

- A metaorder is a parent order of total size $Q$ executed over a period $T$ through many child orders.
- Impact $I(t) = \varepsilon\,(m_t - m_0)$ is the signed move of the mid (or a fair price) from the start, with $\varepsilon = +1$ for a buy.
- Peak impact is $I(T)$ at the end of execution; permanent impact is $I(\infty)$; temporary impact is the difference.
- Cost (slippage) is the average execution price minus the arrival price, signed; with no spread or fees it is the average of $I(t)$ over the fills.

Impact is measured on average over many metaorders, because any single order's price path is dominated by volatility: Almgren et al. report regression $R^2$ below 1% for their impact fits, exactly as expected when impact is small relative to price noise.

### The square-root law

For a metaorder of size $Q$ in a stock with daily volume $V_D$ and daily volatility $\sigma_D$:

$$
I(Q) \approx Y\, \sigma_D \sqrt{\frac{Q}{V_D}}, \qquad Y = O(1).
$$

Facts to know:

- It is reported across equities, futures, options and other markets, over a wide range of $Q/V_D$, by Toth et al. (2011) and in the survey of Bouchaud, Bonart, Donier and Gould (2018).
- To first order it does not depend on the execution horizon $T$ or the number of child orders, which a linear-in-rate model would not predict.
- Concavity means the marginal share costs less than the average share of a smaller order: doubling the order raises cost per share by $\sqrt{2}$ and total cost by $2\sqrt{2}$.
- Toth et al. explain it with a latent order book whose liquidity vanishes linearly near the current price: removing $Q$ shares then moves the price by an amount proportional to $\sqrt{Q}$.
- It is a statement about averages: the prefactor $Y$ varies by market and period and must be calibrated on your own fills.

### Almgren, Thum, Hauptmann and Li (2005)

On a large set of Citigroup US equity desk orders they fit power laws for permanent and temporary impact, scaled by daily volatility $\sigma$ and daily volume $V$:

$$
I = \gamma\,\sigma\,\frac{X}{V}\left(\frac{\Theta}{V}\right)^{1/4}, \qquad J = \frac{I}{2} + \eta\,\sigma\left|\frac{X}{VT}\right|^{3/5},
$$

where $X$ is the order size, $T$ its duration in days, $\Theta$ shares outstanding, $I$ the permanent move and $J$ the realised cost.
Their unconstrained fit gives $\alpha = 0.891 \pm 0.10$ for the permanent exponent, $\delta = 0.267 \pm 0.22$ for the turnover factor and $\beta = 0.600 \pm 0.038$ for the temporary exponent; they fix $\alpha = 1$ (linear permanent impact, which is required for absence of arbitrage, citing Huberman and Stanzl), $\delta = 1/4$, and $\beta = 3/5$, rejecting the square-root temporary exponent $1/2$ at the 95% level.
With exponents fixed, $\gamma = 0.314 \pm 0.041$ and $\eta = 0.142 \pm 0.0062$.
The temporary cost depends on the trading rate $X/(VT)$, so in this model trading more slowly is cheaper, unlike the pure square-root law.

### Temporary and permanent impact

The Almgren-Chriss family splits impact into:

- permanent impact $g(v)$, a shift in the price that persists, linear in the shares traded;
- temporary impact $h(v)$, a concession paid on each child order that depends on the current trading rate $v$ and disappears when trading stops.

This split is simple and makes optimal execution tractable (see [Optimal Execution: Almgren-Chriss](07-Optimal-Execution-Almgren-Chriss.md)), but real impact decays gradually rather than either vanishing instantly or persisting forever.
Transient impact models describe the decay explicitly.

### Propagator models

Bouchaud, Gefen, Potters and Wyart (2004) write the mid price as a linear superposition of past trade impacts:

$$
m_t = m_{-\infty} + \sum_{s < t} G(t - s)\,\varepsilon_s + \text{noise},
$$

with $\varepsilon_s = \pm 1$ the sign of trade $s$ and $G(\ell)$ the propagator, the average impact of one trade after $\ell$ trades.

Order signs have long memory: their autocorrelation decays as $C(\ell) \sim \ell^{-\gamma}$ with $0 < \gamma < 1$, largely because metaorders are split into many same-sign child orders (Lillo and Farmer 2004).
If $G$ were constant (permanent impact), prices would inherit this memory and become predictable.
Prices are close to a martingale, so $G$ must decay; with $G(\ell) \sim \ell^{-\beta}$ the variance of price changes over $L$ trades scales as $L^{2 - 2\beta - \gamma}$, and prices are diffusive (variance linear in $L$) only when

$$
\beta = \beta_c = \frac{1 - \gamma}{2}.
$$

Market makers' liquidity provision, which leans against persistent flow, is the mechanism that produces this fine balance.
A slower decay ($\beta < \beta_c$) gives trending, superdiffusive prices; a faster decay ($\beta > \beta_c$) gives mean-reverting, subdiffusive prices.

### Impact decay and no-dynamic-arbitrage

For a metaorder traded at a constant rate with a power-law propagator $G(\ell) = \ell^{-1/2}$, the peak impact after $T$ steps grows like $\sqrt{T}$, and after the end of trading the impact decays like $\sqrt{T + s} - \sqrt{s}$ (continuum limit), a slow power law with no permanent floor.
An exponential kernel (Obizhaeva and Wang's resilience model) instead decays geometrically.
Gatheral (2010) shows that, under no dynamic arbitrage (no round trip with negative expected cost), exponential decay of impact is compatible only with linear instantaneous impact, so the shape of impact and the shape of decay cannot be chosen independently.

Farmer, Gerig, Lillo and Waelbroeck (2013) add a fair-pricing condition: the average price paid over a metaorder equals the price after impact has relaxed.
With square-root impact accumulated along the order, the average price paid is $\int_0^1 \sqrt{q}\,dq = 2/3$ of the peak impact, so the permanent impact is about two thirds of the peak.

### How practitioners use impact models

- Pre-trade cost estimates: half-spread plus a calibrated $Y\sigma\sqrt{Q/V}$ (or a rate-dependent model), used to choose schedule, venue mix and whether to trade at all.
- Capacity: with cost per unit notional $\propto \sqrt{Q}$, the alpha net of costs is $\alpha Q - kQ^{3/2}$, maximised at $Q^* = (2\alpha/3k)^2$; this is how a fund sizes a strategy.
- Post-trade TCA separates impact (it reverts or not) from adverse price moves using markouts; see [Execution Algorithms and TCA](08-Execution-Algorithms-and-TCA.md).
- Market makers use propagator-style models of their own flow to predict how far a sweep will carry the price and how quickly it will come back.

## Worked examples

### Example 1: a pre-trade estimate with the square-root law

"Daily volatility 2%, $Y = 1$. What does the square-root law predict for orders of 0.1%, 1%, 5%, 10% and 25% of daily volume?"

| $Q/V$ | 0.1% | 1% | 5% | 10% | 25% |
| :--- | ---: | ---: | ---: | ---: | ---: |
| Impact (bp) | 6.32 | 20.00 | 44.72 | 63.25 | 100.00 |

For 100,000 shares of a $50 stock trading 2,000,000 shares a day, $Q/V = 5\%$ and the notional is $5,000,000, so the impact cost is about $5{,}000{,}000 \times 44.72 \text{ bp} \approx \$22{,}361$.
Doubling the order to 10% of volume raises the per-share cost by $\sqrt{2} = 1.414$ and the total cost by $2.828$.

### Example 2: reproduce Almgren et al.'s Table 3

Buying 10% of daily volume ($X/V = 0.1$), with their coefficients:

| Stock | $\Theta/V$ | $I/\sigma$ | $I$ (bp) | $T$ (days) | $K/\sigma$ | $K$ (bp) | $J = I/2 + K$ (bp) |
| :--- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| IBM ($\sigma = 1.57\%$) | 263.4 | 0.126 | 19.9 | 0.1 | 0.142 | 22.3 | 32.2 |
| | | | | 0.2 | 0.094 | 14.7 | 24.6 |
| | | | | 0.5 | 0.054 | 8.5 | 18.4 |
| DRI ($\sigma = 2.26\%$) | 87.1 | 0.096 | 21.7 | 0.1 | 0.142 | 32.1 | 42.9 |
| | | | | 0.2 | 0.094 | 21.2 | 32.0 |
| | | | | 0.5 | 0.054 | 12.2 | 23.1 |

These round to the paper's published 20 and 22 bp permanent and 32, 25, 18 and 43, 32, 23 bp realised costs.
IBM's permanent impact relative to volatility is larger than DRI's because IBM turns over a smaller fraction of its shares each day ($\Theta/V = 263$ versus 87).
Spreading the trade from a tenth of a day to half a day cuts IBM's temporary cost from 22.3 to 8.5 bp, which is the rate dependence a pure square-root law does not have.

### Example 3: how a metaorder's impact decays

Propagator $G(\ell) = \ell^{-1/2}$, one unit bought per step.

- Peak impact after 100 steps is 18.59 and after 400 steps 38.56: quadrupling duration at the same rate doubles peak impact (ratio 2.07), the square-root shape again.
- After a 400-step metaorder, the impact remaining at $2T$, $5T$ and $10T$ is 42.9%, 24.5% and 16.8% of the peak, close to the continuum values $\sqrt2 - 1 = 41.4\%$, $\sqrt5 - 2 = 23.6\%$ and $\sqrt{10} - 3 = 16.2\%$.
- With an exponential kernel of timescale 100 steps, the impact at $2T$ is $e^{-4} = 1.8\%$ of the peak: exponential resilience forgets fast, power-law markets do not.

### Example 4: the diffusion constraint in simulation

Trade signs are generated as the sign of fractional Gaussian noise with Hurst exponent 0.75, which gives $C(\ell) \sim \ell^{-1/2}$ ($\gamma = 0.5$) and $\beta_c = 0.25$; at lags 10 and 100 the theoretical sign autocorrelations are 0.0757 and 0.0239, and the simulation (16 paths of 65,536 trades, seed 7) gives about 0.0759 and 0.0241.
Prices are built with $G(\ell) = \ell^{-\beta}$, and $D(L) = \text{Var}(m_{t+L} - m_t)/L$ is compared at $L = 2{,}048$ and $L = 16$:

| $\beta$ | $D(2048)/D(16)$ | Behaviour |
| ---: | ---: | :--- |
| 0.10 | about 3.80 | superdiffusive (trending) |
| 0.25 | about 0.94 | close to diffusive |
| 0.40 | about 0.26 | subdiffusive (mean-reverting) |

Only the critical decay keeps the price close to a random walk while the order flow itself is strongly persistent.

### Example 5: fair pricing

If peak impact is 30 bp and impact accumulated as $\sqrt{q}$ along the order, the average price paid sits $\int_0^1 \sqrt{q}\,dq = 2/3$ of the way up, so fair pricing predicts a permanent impact of about 20 bp after reversion.

## Pitfalls

- Treating a single order's price move as its impact; volatility swamps it, and only averages over many orders identify impact.
- Applying a linear model to large orders: linear impact overstates the cost of small orders and understates large ones relative to square-root.
- Forgetting that impact is measured relative to volatility and volume: the same share count is cheap in a liquid, calm stock and expensive in an illiquid, volatile one.
- Calibrating impact on your own fills without conditioning on alpha: if you buy before prices rise because your signal works, the rise looks like impact.
- Assuming impact decays instantly or never; it decays slowly, so back-to-back metaorders in the same direction pay for each other's impact.
- Choosing an impact shape and a decay kernel independently; some combinations allow price manipulation round trips.
- Reading the propagator's decay as market inefficiency; it is what keeps prices efficient when order flow is persistent.

## Interview questions

> [!question]- ms-impact-sqrt-law | State the square-root impact law.
> Peak impact $\approx Y\sigma_D\sqrt{Q/V_D}$ with $Y$ of order one.
> It is concave in size and roughly independent of the execution horizon.

> [!question]- ms-impact-sqrt-numeric | Daily vol 2%, order 5% of daily volume, $Y = 1$. Impact?
> About 44.7 bp: $200 \times \sqrt{0.05}$ bp.

> [!question]- ms-impact-double-size | Under the square-root law, what happens to cost per share and total cost when you double the order?
> Cost per share rises by $\sqrt2 \approx 1.41$, total cost by $2\sqrt2 \approx 2.83$.
> Total cost scales as $Q^{3/2}$.

> [!question]- ms-impact-dollar-cost | 100,000 shares of a $50 stock, 2,000,000 shares daily volume, 2% daily vol. Rough impact cost in dollars?
> About 22,000 dollars: 44.7 bp of 5,000,000 dollars.

> [!question]- ms-impact-almgren-exponents | What did Almgren et al. (2005) find for impact exponents?
> Permanent impact roughly linear in size (fitted 0.891, fixed at 1) and temporary impact a 3/5 power of trading rate (0.600 plus or minus 0.038), rejecting the square root for temporary impact.
> Coefficients $\gamma = 0.314$, $\eta = 0.142$, with a turnover factor $(\Theta/V)^{1/4}$.

> [!question]- ms-impact-why-linear-permanent | Why should permanent impact be linear in size?
> Nonlinear permanent impact admits round-trip strategies with negative expected cost (Huberman and Stanzl), and linear impact makes the permanent effect independent of how the trade is scheduled.

> [!question]- ms-impact-temp-vs-perm | Define temporary and permanent impact.
> Temporary impact is the rate-dependent concession that disappears after trading stops; permanent impact is the part of the price move that remains.
> In practice impact decays gradually, so the split depends on the horizon at which you measure.

> [!question]- ms-impact-propagator | Write the propagator model.
> $m_t = \sum_{s<t} G(t - s)\,\varepsilon_s + \text{noise}$: each trade's sign moves the price by a decaying kernel $G$.
> It models transient impact and reconciles persistent order flow with unpredictable prices.

> [!question]- ms-impact-beta-critical | Trade signs have autocorrelation $\ell^{-\gamma}$. What propagator decay keeps prices diffusive?
> $G(\ell) \sim \ell^{-\beta}$ with $\beta = (1 - \gamma)/2$.
> Price change variance scales as $L^{2 - 2\beta - \gamma}$; set the exponent to 1.

> [!question]- ms-impact-sign-memory-source | Why do trade signs have long memory?
> Large metaorders are split into many child orders of the same sign, and metaorder sizes are broadly distributed.
> Lillo and Farmer documented the power-law decay of sign autocorrelation.

> [!question]- ms-impact-decay-shape | With $G(\ell) = \ell^{-1/2}$, what fraction of peak impact remains at twice the metaorder's duration?
> About $\sqrt2 - 1 = 41\%$ in the continuum limit (42.9% in the discrete simulation).
> Power-law decay is slow and has no permanent floor in this model.

> [!question]- ms-impact-two-thirds | Under fair pricing with square-root impact, how much of the peak impact is permanent?
> About two thirds, because the average price paid along a square-root path is $2/3$ of the peak.
> Farmer, Gerig, Lillo and Waelbroeck (2013).

> [!question]- ms-impact-gatheral | What does Gatheral's no-dynamic-arbitrage result say about exponential decay?
> Exponential decay of impact is consistent only with linear instantaneous impact.
> Nonlinear impact with exponential decay allows round trips with negative expected cost.

> [!question]- ms-impact-rate-dependence | Under Almgren et al.'s model, IBM's temporary cost for 10% of volume falls from 22.3 bp over 0.1 days to 8.5 bp over 0.5 days. Why does the pure square-root law disagree?
> The square-root law says peak impact depends on $Q/V$ and hardly on duration; the Almgren model makes temporary cost a function of trading rate.
> Both are empirical summaries over different samples and conditioning choices.

> [!question]- ms-impact-alpha-contamination | Your measured impact on your own fills looks huge. What could be wrong?
> Your orders are correlated with future returns (you trade on alpha), so the price drift after your trades is partly prediction, not impact.
> Control by comparing with orders not driven by the signal, or by modelling alpha and impact jointly.

> [!question]- ms-impact-capacity | With alpha $\alpha$ per unit traded and cost $kQ^{1/2}$ per unit, what position size maximises profit?
> $Q^* = (2\alpha/3k)^2$, from maximising $\alpha Q - kQ^{3/2}$.
> This is the square-root law's capacity constraint.

## In this repo and SDE-Interview-Prep

- Code: [market_impact.py](code/market_impact.py) reproduces every number above (`python market_impact.py`).
- Related in this repo: [Transaction Costs and Turnover](../09-Alpha-Research-and-Portfolio/13-Transaction-Costs-and-Turnover.md).

## Further reading

- Bouchaud, Bonart, Donier and Gould, *Trades, Quotes and Prices* (Cambridge University Press, 2018), chapters on the square-root law and propagator models.
- Toth et al. (2011), Anomalous Price Impact and the Critical Nature of Liquidity in Financial Markets, *Physical Review X* 1.
- Almgren, Thum, Hauptmann and Li (2005), Direct Estimation of Equity Market Impact, *Risk* 18(7).
- Bouchaud, Gefen, Potters and Wyart (2004), Fluctuations and Response in Financial Markets, *Quantitative Finance* 4(2).
- Lillo and Farmer (2004), The Long Memory of the Efficient Market, *Studies in Nonlinear Dynamics and Econometrics* 8(3).
- Jim Gatheral (2010), No-Dynamic-Arbitrage and Market Impact, *Quantitative Finance* 10(7).
- Obizhaeva and Wang (2013), Optimal Trading Strategy and Supply/Demand Dynamics, *Journal of Financial Markets* 16(1).
- Farmer, Gerig, Lillo and Waelbroeck (2013), How Efficiency Shapes Market Impact, *Quantitative Finance* 13(11).
