---
type: concept
track: [quant-trader, quant-research]
tier: core
status: solid
prereqs: [spread-models-roll-and-glosten-milgrom]
est_hours: 3
sources: [Easley Lopez de Prado and O'Hara (2012) Flow Toxicity and Liquidity in a High-Frequency World. Review of Financial Studies 25(5) 1457-1493, Andersen and Bondarenko (2014) VPIN and the Flash Crash. Journal of Financial Markets 17 1-46, Easley Kiefer O'Hara and Paperman (1996) Liquidity Information and Infrequently Traded Stocks. Journal of Finance 51(4) 1405-1436, Glosten and Milgrom (1985) Journal of Financial Economics 14(1) 71-100, Cartea Jaimungal and Penalva (2015) Algorithmic and High-Frequency Trading. Cambridge University Press]
---

# Adverse Selection and Order Flow Toxicity

## TL;DR

- Adverse selection is the tendency of your passive fills to be followed by prices moving against you, because the people who choose to trade with you know something, or know it sooner.
- Measure it with markouts: for a fill with side $d$ at price $p$, the markout at horizon $\tau$ is $d(m_{t+\tau} - p)$; plot it against $\tau$ and read the shape.
- The effective spread a taker pays splits into the realized spread the maker keeps and the price impact the maker loses: $\text{effective} = \text{realized} + \text{impact}$.
- PIN and VPIN estimate the share of informed flow from order imbalance; VPIN is popular but critics show it is largely a function of volume and volatility and its flash-crash record depends on implementation choices.
- Toxicity differs by counterparty, venue, order size and market state, so segment flow and price each segment to its own markout rather than to the blended average.

## Learning objectives

- Measure adverse selection with markouts at several horizons.
- Explain VPIN and its critiques.
- Segment flow by toxicity and price it differently.

## Core concepts

### Where adverse selection comes from

A resting quote is a free option given to the rest of the market: anyone may trade against it, and they choose when.
They exercise it when your price is wrong from their point of view.
The sources, roughly from slowest to fastest:

- Fundamental information: a trader who knows more about value than the market.
- Short-horizon statistical signals: order book imbalance, trade flow, cross-asset lead-lag.
- Latency: a related instrument (the future, the ETF, another venue) has already moved and your quote has not; see [Latency Arbitrage and Speed](10-Latency-Arbitrage-and-Speed.md).

Glosten and Milgrom show that even a zero-cost, risk-neutral market maker must quote a spread when some traders are informed, because the ask must equal the expected value conditional on a buy.
With value $V_H$ or $V_L$ equally likely, a fraction $\mu$ of informed traders and uninformed traders who buy or sell with probability one half, the initial quotes are

$$
\text{ask} = \bar V + \mu \frac{V_H - V_L}{2}, \qquad \text{bid} = \bar V - \mu \frac{V_H - V_L}{2}.
$$

The half-spread equals the informed share times the half-range of value: it prices adverse selection, nothing else.
See [Spread Models: Roll and Glosten-Milgrom](03-Spread-Models-Roll-and-Glosten-Milgrom.md).

### Markouts

For fill $i$ at time $t_i$, price $p_i$, side $d_i$ ($+1$ if you bought) and size $n_i$, with reference price $m_t$ (the mid or your fair value), the markout at horizon $\tau$ is

$$
M_i(\tau) = d_i \big( m_{t_i + \tau} - p_i \big).
$$

At $\tau = 0$ it is the edge at fill (half-spread captured against the reference); as $\tau$ grows it includes the adverse move.
Report the size-weighted average $\sum_i n_i M_i(\tau) / \sum_i n_i$ in ticks or basis points, at a grid such as 100 ms, 1 s, 10 s, 60 s and 5 min.

How to read the curve:

- A drop inside the first second that then flattens: short-horizon informed or latency-driven flow.
- A steady drift that keeps going: longer-horizon informed flow; you are trading against someone with a real view.
- A dip followed by partial recovery: temporary impact from liquidity demand; you are being paid to absorb it, and a longer horizon shows it.
- Flat near the spread captured: benign flow.

Reference choice matters.
Mid-based markouts are simple and model-free; theo-based markouts isolate what your pricing model missed.
In large-tick instruments the mid jumps by half ticks, so use the microprice or a fine-grained theo; see [Order Book Imbalance and the Microprice](11-Order-Book-Imbalance-and-Microprice.md).

### Effective, realized and impact

For a taker trade with side $d$ (from the taker's view) at price $p$, mid $m_t$ at trade time and $m_{t+\tau}$ later:

$$
\underbrace{d(p - m_t)}_{\text{effective half-spread}} = \underbrace{d(p - m_{t+\tau})}_{\text{realized half-spread}} + \underbrace{d(m_{t+\tau} - m_t)}_{\text{price impact}}.
$$

The realized half-spread is what the maker kept after $\tau$; the price impact is what adverse selection took.
This is the maker's markout seen from the taker's side.

### PIN

Easley, Kiefer, O'Hara and Paperman model each day as having an information event with probability $\alpha$; on event days informed traders arrive at rate $\mu$ on the informed side, while uninformed buyers and sellers arrive at rates $\varepsilon_b$ and $\varepsilon_s$ every day.
With equal uninformed rates $\varepsilon_b = \varepsilon_s = \varepsilon$ (the form Easley, Lopez de Prado and O'Hara restate as their equation 6), the probability that a given trade is informed is

$$
\text{PIN} = \frac{\alpha \mu}{\alpha \mu + 2\varepsilon},
$$

and with unequal rates the denominator becomes $\alpha\mu + \varepsilon_b + \varepsilon_s$, the expected arrival rate of all orders.

The parameters are estimated by maximum likelihood from daily buy and sell counts, which makes PIN slow and unsuited to intraday use.

### VPIN

Easley, Lopez de Prado and O'Hara (2012) proposed a volume-clock version.

1. Split the tape into buckets of equal volume $V$.
2. Classify volume as buys or sells by bulk volume classification over the one-minute time bars $i$ inside bucket $\tau$: $V_\tau^B = \sum_i V_i \, \Phi(\Delta P_i / \sigma_{\Delta P})$ and $V_\tau^S = V - V_\tau^B$.
3. Average the absolute imbalance over the last $n$ buckets:

$$
\text{VPIN} = \frac{1}{nV} \sum_{\tau=1}^{n} \big| V_\tau^S - V_\tau^B \big|.
$$

The authors report that the CDF of VPIN crossed 0.9, an extreme reading, at least two hours before the 6 May 2010 flash crash, and propose it as a toxicity warning.

Critiques that interviewers expect you to know:

- Andersen and Bondarenko (2014) find VPIN a poor predictor of short-run volatility, find that it reached its all-time high after, not before, the flash crash, and attribute its predictive content mainly to a mechanical relation with trading intensity.
- In their reply, "Reflecting on the VPIN dispute", they report no incremental predictive power for future volatility once volume and volatility are controlled for, and show that VPIN's properties depend strongly on the trade classification; the main paper also shows sensitivity to the starting point of the sample.
- Bulk volume classification can misclassify trade direction compared with signing trades against the prevailing quote, and the imbalance measure mixes informed flow with plain liquidity demand.

In practice VPIN-style imbalance is one feature among many; the ground truth for a market maker remains the markouts of its own fills.

### Segmenting and pricing flow

The blended markout hides a mixture.
Segment fills along any dimension you can observe at quote time, estimate the markout curve for each, and price each segment to its own adverse selection.

- Counterparty or client, where it is disclosed (RFQ platforms, bilateral streams, retail wholesaling).
- Venue and order type, for example separating IOC sweeps that hit several venues at once from single-venue fills, and comparing their markouts.
- Order size relative to displayed depth.
- Market state: signal value, time since the last price change, moves in a leading instrument, time of day, proximity to scheduled news.

In an anonymous order book you cannot price by counterparty, but you can condition width, skew and size on market state, which is the lit-market version of segmentation.
Where flow is disclosed, dealers can tier pricing by client, and FX liquidity providers have used last-look windows, which Principle 17 of the FX Global Code (version updated December 2024) requires them to disclose: "Market Participants employing last look should be transparent regarding its use and provide appropriate disclosures to Clients."

### Statistics of markouts

A 60-second markout is dominated by price noise: its standard deviation per fill is roughly $\sigma\sqrt{\tau}$, often many times the mean you are trying to detect.
For a mean of size $\Delta$ with per-fill standard deviation $s$ to sit 1.96 standard errors from zero (the two-sided 5% level), you need about $n \approx (1.96\, s / \Delta)^2$ fills.
Fills that are close in time share the same future price path, so they are not independent: cluster standard errors by time bucket or bootstrap by day.

## Worked examples

All fills, prices and model parameters below are hypothetical inputs; [micro_05_adverse_selection.py](code/micro_05_adverse_selection.py) asserts every number.

### Example 1: a markout table

Five of your passive fills, prices in dollars, tick 0.01, total size 1,000 shares.

| Fill | Side | Size | Price | Mid at fill | Mid +1 s | Mid +60 s |
| ---: | :--- | ---: | ---: | ---: | ---: | ---: |
| 1 | Buy | 200 | 25.00 | 25.005 | 25.000 | 24.99 |
| 2 | Sell | 100 | 25.02 | 25.015 | 25.020 | 25.03 |
| 3 | Buy | 300 | 25.01 | 25.015 | 25.015 | 25.02 |
| 4 | Sell | 200 | 25.03 | 25.025 | 25.030 | 25.04 |
| 5 | Buy | 200 | 24.99 | 24.995 | 24.985 | 24.97 |

Per-fill markouts in cents: at fill every fill earns +0.5 (half a tick).
At 1 s: 0, 0, +0.5, 0, -0.5; size-weighted total $300 \times 0.5 - 200 \times 0.5 = +0.5$ dollars, or +0.05 cents per share.
At 60 s: -1, -1, +1, -1, -2; total $-2 - 1 + 3 - 2 - 4 = -6$ dollars, or -0.6 cents per share.
The half-tick captured at fill is more than lost by 60 seconds, and the curve is still falling, which points to informed flow at a horizon longer than a second.
The unweighted average at 60 s would be -0.8 cents; use size weights for P&L and report both when sizes differ a lot.

### Example 2: effective, realized and impact

A taker buys at 25.02 when the mid is 25.015; ten seconds later the mid is 25.03.
Effective half-spread $= 25.02 - 25.015 = 0.005$.
Realized half-spread $= 25.02 - 25.03 = -0.010$.
Price impact $= 25.03 - 25.015 = 0.015$.
Check: $-0.010 + 0.015 = 0.005$.
The maker who sold was paid half a cent and lost a cent and a half, net -1 cent per share.

### Example 3: Glosten-Milgrom quotes and updating

$V_L = 99$, $V_H = 101$, $\mu = 0.2$.
A buy occurs with probability $0.2 + 0.8/2 = 0.6$ when $V = V_H$ and $0.4$ when $V = V_L$.
Initial quotes: ask $= 100 + 0.2 \times 1 = 100.20$, bid $99.80$.
After one buy, $P(V_H) = 0.5 \times 0.6 / (0.5 \times 0.6 + 0.5 \times 0.4) = 0.6$.
The next ask is $99 + 2 \times \frac{0.6 \times 0.6}{0.6 \times 0.6 + 0.4 \times 0.4} = 99 + 2 \times 0.6923 = 100.385$ and the next bid is $99 + 2 \times \frac{0.6 \times 0.4}{0.6 \times 0.4 + 0.4 \times 0.6} = 100.00$.
Each trade moves the quotes toward the side it came from: the order flow itself is the information.

### Example 4: PIN

$\alpha = 0.4$, $\mu = 50$ informed trades on an event day, $\varepsilon_b = \varepsilon_s = 100$.

$$
\text{PIN} = \frac{0.4 \times 50}{0.4 \times 50 + 200} = \frac{20}{220} \approx 0.091.
$$

About 9% of trades are expected to be informed.
In the Glosten-Milgrom approximation, a value uncertainty of plus or minus 1 dollar would then justify a half-spread of about 9 cents.

### Example 5: VPIN on five buckets

Bucket volume $V = 10{,}000$; for simplicity each bucket is one bar, with standardised price changes $0.5, -0.2, 1.5, 0.1, 2.0$.
Buy volumes $V\Phi(z)$: 6,915, 4,207, 9,332, 5,398, 9,772.
Absolute imbalances $|2V_B - V|$: 3,829, 1,585, 8,664, 797, 9,545.
$\text{VPIN} = 24{,}420 / 50{,}000 \approx 0.488$.
Notice the input is only the price change: large moves raise VPIN mechanically, which is the heart of the critique that it restates volatility.

### Example 6: how many fills to trust a markout

The 60-second markout has a per-fill standard deviation of 3 ticks and you want a mean of 0.1 ticks to sit 1.96 standard errors from zero.
$n \approx (1.96 \times 3 / 0.1)^2 \approx 3{,}457$ independent fills.
To detect a 0.3-tick difference between two venues, each with standard deviation 3, you need about $(1.96 \times 3\sqrt{2} / 0.3)^2 \approx 768$ fills per venue.
Correlated fills in bursts make the effective sample smaller, so these are lower bounds.

### Example 7: pricing two segments

70% of your fills come from segment A with a 10-second markout of -0.1 ticks, 30% from segment B at -1.6 ticks.
Half-spread 0.5 ticks and a net rebate of 0.1 ticks give 0.6 ticks of gross edge.
Blended adverse selection $= 0.7 \times 0.1 + 0.3 \times 1.6 = 0.55$, net edge $+0.05$ ticks per fill.
By segment: A earns $0.6 - 0.1 = 0.5$, B loses $0.6 - 1.6 = -1.0$.
If you can identify B at quote time, widening or declining B raises edge per fill from 0.05 to 0.5 at the cost of 30% of volume.
If you cannot identify B, the blended number is the right one, but it is fragile: break-even is at a B share of $(0.6 - 0.1)/(1.6 - 0.1) = 1/3$, so a rise from 30% to 33.3% turns the whole book negative.

The markout, Glosten-Milgrom, PIN and VPIN calculations are in [micro_05_adverse_selection.py](code/micro_05_adverse_selection.py).

## Pitfalls

- Reporting fill rate or spread captured at fill instead of markouts at several horizons.
- Using a single horizon: too short misses slow informed flow, too long is swamped by noise and inventory drift.
- Mixing sign conventions between maker and taker views; write $d$ explicitly.
- Using trade prices as the reference; bid-ask bounce creates spurious reversion.
- Treating fills as independent when computing standard errors.
- Presenting VPIN as a proven crash predictor rather than a contested imbalance measure.
- Pricing to the blended markout when a small, identifiable segment drives all the losses.
- Calling flow toxic because the 1-second markout is negative when it reverts by 60 seconds; that is temporary impact you are paid to absorb.

## Interview questions

> [!question]- ms-tox-markout-formula | Define the markout of a fill at horizon $\tau$ and its sign convention.
> $d(m_{t+\tau} - p)$, with $d = +1$ if you bought, $p$ the fill price and $m$ the mid or fair value.
> Positive means the fill made money against the reference by time $\tau$.

> [!question]- ms-tox-curve-shape-reading | Your markout curve dips at 1 second and recovers half the loss by 5 minutes. What does that say?
> Part of the move is temporary impact from liquidity demand, which you are paid to absorb; the unrecovered part is information.
> Judge the flow at the horizon over which you actually hold inventory, not only the dip.

> [!question]- ms-tox-effective-realized-impact | Taker buys at 25.02, mid then 25.015, mid ten seconds later 25.03. Effective, realized and impact?
> Effective 0.005, realized -0.010, impact 0.015.
> Effective equals realized plus impact: $-0.010 + 0.015 = 0.005$.

> [!question]- ms-tox-gm-half-spread | In Glosten-Milgrom with $V \in \{99, 101\}$ equally likely and 20% informed traders, what are the initial quotes?
> Bid 99.80, ask 100.20.
> The half-spread is $\mu (V_H - V_L)/2 = 0.2 \times 1$.

> [!question]- ms-tox-gm-update-after-buy | In the same model, after one buy where does the ask move?
> To about 100.385.
> The posterior on $V_H$ becomes 0.6, and the next ask is $E[V \mid \text{two buys}] = 99 + 2 \times 0.36/0.52$.

> [!question]- ms-tox-pin-formula | Write PIN and compute it for $\alpha = 0.4$, $\mu = 50$, $\varepsilon_b = \varepsilon_s = 100$.
> $\text{PIN} = \alpha\mu/(\alpha\mu + \varepsilon_b + \varepsilon_s) = 20/220 \approx 0.091$, which is $\alpha\mu/(\alpha\mu + 2\varepsilon)$ with equal rates.
> It is the expected share of trades that come from informed traders.

> [!question]- ms-tox-vpin-definition | How is VPIN computed?
> Split volume into equal buckets, classify each bucket's volume into buys and sells with bulk volume classification $V_B = V\Phi(\Delta P/\sigma)$, and average $|V_S - V_B|/V$ over the last $n$ buckets.
> It is a volume-clock order imbalance measure.

> [!question]- ms-tox-vpin-critique | What are the main critiques of VPIN?
> Andersen and Bondarenko find it a poor predictor of short-run volatility with no incremental power once volume and volatility are controlled for, and that it peaked after rather than before the flash crash; its properties depend on the trade classification and the sample start.
> Bulk volume classification also misclassifies trade direction and cannot separate informed flow from liquidity demand.

> [!question]- ms-tox-markout-sample-size | Per-fill 60 s markout standard deviation is 3 ticks. How many fills for a 0.1-tick mean to sit 1.96 standard errors from zero?
> About 3,500: $(1.96 \times 3 / 0.1)^2 \approx 3{,}457$, the count at which 0.1 ticks is 1.96 standard errors.
> More if fills cluster in time, because clustered fills share the same price path.

> [!question]- ms-tox-segment-blended | 70% of fills mark out at -0.1 ticks and 30% at -1.6; gross edge is 0.6 ticks. What is the net edge and what do you do?
> +0.05 ticks blended; +0.5 for the first segment and -1.0 for the second.
> Price the second segment wider or stop quoting it if you can identify it at quote time.

> [!question]- ms-tox-lit-segmentation | You cannot see counterparties in an anonymous order book. How do you still segment toxicity?
> Condition on observable state: signal values, sweep detection, time since the last price move, moves in a leading instrument, time of day and news proximity.
> Width, skew and size then vary with that state.

> [!question]- ms-tox-quote-as-option | Why is a resting limit order described as a free option?
> Anyone can trade against it at your price and they choose when, so they exercise it when your price is stale or wrong.
> The option's value to them is your adverse selection cost.

> [!question]- ms-tox-reference-price | Why prefer the mid or microprice over the last trade price as the markout reference?
> Trade prices bounce between bid and ask, which creates spurious reversion and noise.
> The microprice is better still in large-tick names where the mid moves in half-tick jumps.

> [!question]- ms-tox-markout-table-60s | Fills of 200, 100, 300, 200 and 200 shares mark out at -1, -1, +1, -1 and -2 cents at 60 s. Size-weighted and unweighted averages?
> Size-weighted $-6$ dollars over 1,000 shares, or $-0.6$ cents per share; unweighted $-0.8$ cents.
> Use size weights for P&L and report both when sizes differ a lot.

> [!question]- ms-tox-vpin-bvc-example | A bucket of 10,000 has a standardised price change of 2.0. What buy volume and imbalance does bulk volume classification assign?
> Buy volume $10{,}000\,\Phi(2.0) \approx 9{,}772$ and imbalance $|2V_B - V| \approx 9{,}545$.
> Only the price change enters, so a large move mechanically looks like one-sided flow.

> [!question]- ms-tox-segment-break-even | Segment A marks out at -0.1 ticks and B at -1.6 against 0.6 ticks of gross edge. At what share of B does the blended book break even?
> One third.
> $(1 - x)(0.1) + x(1.6) = 0.6$ gives $x = 0.5/1.5$, so moving from 30% to 33.3% B flow erases the edge.

## In this repo and The-Distinguished-Engineer

- Code: [`code/micro_05_adverse_selection.py`](code/micro_05_adverse_selection.py) prints and asserts every number on this page: markouts in exact rational arithmetic, Glosten-Milgrom quotes by enumerating every trader type and order path (not the closed-form half-spread), PIN exactly and by simulating Poisson trade counts, the normal CDF for bulk volume classification by Simpson integration, and the sample-size rule by simulating the sampling distribution of the mean.
- Related notes: [Spread Models: Roll and Glosten-Milgrom](03-Spread-Models-Roll-and-Glosten-Milgrom.md), [Order Book Imbalance and the Microprice](11-Order-Book-Imbalance-and-Microprice.md).

## Further reading

- Easley, Lopez de Prado and O'Hara (2012), Flow Toxicity and Liquidity in a High-Frequency World, *Review of Financial Studies* 25(5), 1457-1493 (equations 7 and 9 for bulk classification and VPIN).
- Andersen and Bondarenko (2014), VPIN and the Flash Crash, *Journal of Financial Markets* 17, 1-46, and Reflecting on the VPIN dispute, *Journal of Financial Markets* 17, 53-64.
- Easley, Kiefer, O'Hara and Paperman (1996), Liquidity, Information, and Infrequently Traded Stocks, *Journal of Finance* 51(4), 1405-1436.
- Glosten and Milgrom (1985), Bid, ask and transaction prices in a specialist market with heterogeneously informed traders, *Journal of Financial Economics* 14(1), 71-100.
- Global Foreign Exchange Committee, *FX Global Code* (updated December 2024), Principle 17.
- Cartea, Jaimungal and Penalva, *Algorithmic and High-Frequency Trading* (2015).
- Related notes: [Market Making P&L Attribution and Markouts](../08-Market-Making/09-Market-Making-PnL-Attribution-and-Markouts.md), [Quote Management: Skew, Width and Size](../08-Market-Making/05-Quote-Management-Skew-Width-and-Size.md).
