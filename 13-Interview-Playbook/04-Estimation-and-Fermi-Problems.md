---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: []
est_hours: 2
sources: [Lawrence Weinstein and John A. Adam - Guesstimation (Princeton University Press 2008), Sanjoy Mahajan - Street-Fighting Mathematics (MIT Press 2010), Agustin Lebron - The Laws of Trading (2019), US Census Bureau QuickFacts Chicago city Illinois - https://www.census.gov/quickfacts/chicagocityillinois, US Census Bureau Vintage 2025 population estimates, US Census Bureau 2020 Census apportionment results (April 26 2021) - https://www.census.gov/newsroom/press-releases/2021/2020-census-apportionment-results.html, UN World Population Prospects 2024, OECD Health at a Glance 2025, USGA and R&A Equipment Rules Appendix III, G. D. Scott and D. M. Kilgour - The density of random close packing of spheres (J. Phys. D 1969)]
---

# Estimation and Fermi Problems

## TL;DR

- Decompose the unknown into factors you can bound, estimate each, multiply, and cross-check with a second decomposition.
- Work in orders of magnitude; when you only know a range, use the geometric mean of the bounds ($\sqrt{100 \times 10000} = 1000$).
- Errors in a product add in log space: $k$ independent factors each uncertain by a factor $f$ give roughly a factor $f^{\sqrt{k}}$, not $f^k$.
- Always give an interval, and in a trading interview turn the interval into a two-sided market whose width reflects your uncertainty and the counterparty's information.
- Name the assumption that drives the answer and say how the estimate changes if it is wrong.

## Learning objectives

- Decompose an unknown quantity and bound it.
- Give a confidence interval and a market, not just a point estimate.

## Core concepts

### What to show

Nobody expects you to know the number of piano tuners in Chicago.
Show the structure of the decomposition, the reasonableness of each input, the arithmetic, and how uncertain you are.
In a trading interview the question may arrive as "make me a market on X", which adds a second skill: quoting a width that will not be picked off.

### Decomposition

Pick a chain of factors whose product is the target, each of which you can estimate from everyday knowledge.

- **Top-down (demand side):** population $\times$ fraction who use it $\times$ frequency.
- **Bottom-up (supply side):** number of suppliers $\times$ capacity per supplier.
- **Physical:** volume of container $/$ volume per item $\times$ packing fraction.

Doing two decompositions and seeing whether they agree within a factor of 2 or 3 is the best available check.

### Useful anchors

| Quantity | Value to use | Source |
| :--- | :--- | :--- |
| Seconds in a year | $3.16 \times 10^7$, within about $0.4\%$ of $\pi \times 10^7$ | $365.25 \times 86{,}400$ |
| Hours in a year | $8760$ | $365 \times 24$ |
| Trading days in a year | $252$, and $\sqrt{252} \approx 15.9 \approx 16$ | A market convention for annualising; the actual count varies by year and exchange |
| World population | about $8.2 \times 10^9$ ($8{,}162$ million on 1 July 2024) | UN, *World Population Prospects 2024* |
| US population | about $3.4 \times 10^8$ ($341.8$ million on 1 July 2025) | US Census Bureau, Vintage 2025 estimates |
| Earth's circumference | about $40{,}000$ km ($40{,}075$ km at the equator) | $2\pi \times 6378.137$ km, the WGS 84 equatorial radius |
| Life expectancy at birth, OECD average | about $81$ years (2023) | OECD, *Health at a Glance 2025* |

Keep the list short and memorise it; any figure you are unsure of should be labelled an assumption.
Population figures move every year, so say which year yours refers to.

### Intervals and the geometric mean

If you believe a quantity lies between $L$ and $U$ with $U/L$ large, the natural midpoint is $\sqrt{LU}$, because your uncertainty is multiplicative.
For each factor give a low and high value at the same confidence; the product's interval in log space has half-width $\sqrt{\sum_i \sigma_i^2}$ when the factor errors are independent and roughly log-normal, where $\sigma_i$ is the log half-width of factor $i$.
Four factors each good to a factor of 2 give $2^{\sqrt 4} = 4$ overall, and nine such factors give $2^3 = 8$; a seeded simulation of log-normal factors reproduces both.
If the errors are correlated (all driven by the same optimistic assumption) they add linearly and the interval is much wider.

### From interval to market

A market is a bid and an ask around your estimate.

- Centre it on your best estimate (the median of your belief, which for a log-normal belief is the geometric mean).
- Set the width from your uncertainty: wide enough that a knowledgeable counterparty cannot trade against you at a large edge, narrow enough to be useful.
  An interviewer may push for tighter; tighten when you have a reason, not because you are asked.
- If the interviewer lifts your offer or hits your bid, treat it as information: they may know the answer, so move your fair value toward their side before quoting again.
- Keep track of what you have bought and sold; the same bookkeeping as in [Trading Games in Interviews](05-Trading-Games-in-Interviews.md).

## Worked examples

### Example 1: piano tuners in Chicago

Inputs: Chicago had $2{,}746{,}388$ residents at the 2020 Census and about $1.15$ million households ($1{,}146{,}547$ in the Census Bureau's 2019-2023 American Community Survey estimate, from QuickFacts as of November 2026).
Everything else below is a labelled assumption.

Demand side.
Assume 1 in 20 households has a piano: about $57{,}000$ pianos, plus an assumed $10\%$ more in schools, churches and venues, so about $63{,}000$.
Assume each is tuned once a year: about $63{,}000$ tunings per year.

Supply side.
Assume a tuner does 4 tunings a day (2 hours each including travel) for 250 days: $1000$ tunings a year.

Answer: about $63{,}000 / 1000 = 63$, so say "about 60 tuners".
Uncertainty: the piano share (1 in 10 to 1 in 40) and the tuning interval (every 6 months to every 2 years) dominate.
Treat each as an 80% range, a factor of 2 either way; independent errors combine to a factor $2^{\sqrt 2} \approx 2.67$, so an 80% interval is about 24 to 170 (holding the tuner's workload fixed).

### Example 2: golf balls in a school bus

Assume a bus interior of about $8 \times 2.5 \times 2$ m, or $40\ \text{m}^3 = 4 \times 10^7\ \text{cm}^3$.
The Rules of Golf set a minimum ball diameter of $1.680$ in ($4.267$ cm), so a ball's volume is $\tfrac{4}{3}\pi (2.1335)^3 \approx 40.7\ \text{cm}^3$.
Randomly packed equal spheres fill about $64\%$ of space (Scott and Kilgour measured $0.637$ in 1969).
$4 \times 10^7 \times 0.64 / 40.7 \approx 630{,}000$, or about $64\ \text{cm}^3$ of bus per ball including gaps.
Assume seats and fittings take a quarter of the space, giving about $470{,}000$, so say "about half a million, within a factor of 1.5".

Cross-check with a different decomposition: stack balls in a cubic grid.
Along the edges fit $187$, $58$ and $46$ whole balls, so $498{,}916$ in total, at a packing fraction of $\pi/6 \approx 0.524$.
Random packing is $0.64 / 0.524 \approx 1.22$ times denser, giving about $610{,}000$, within $3\%$ of the first route.

### Example 3: a market on heartbeats in a lifetime

Assume an average of 70 beats per minute and an 80-year life (close to the OECD average life expectancy of $81$ years).
Estimate: $70 \times 60 \times 24 \times 365 \times 80 \approx 2.9 \times 10^9$.
Uncertainty: treat 60 to 80 beats per minute and 70 to 90 years as 90% ranges.
In log terms their half-widths are $\tfrac12 \ln(80/60)$ and $\tfrac12 \ln(90/70)$, which combine in quadrature to a factor of about $1.21$, so a 90% interval of about $2.4$ to $3.6$ billion.
Multiplying the extremes together instead gives $2.2$ to $3.8$ billion, which assumes both errors go the same way.
Quote "2.7 at 3.1 billion" to start: centred on $2.9$, width about $\pm 7\%$, with the bid below and the offer above the $2.94$ point estimate, so each side has positive expected edge against an uninformed counterparty.
If the interviewer immediately lifts 3.1, do not simply re-quote the same market; raise fair value to about $3.1$ and widen slightly, say "3.0 at 3.4", because the trade may be informed.

### Example 4: daily move from annual volatility

"A stock has $32\%$ annualised volatility; what is a typical daily move?"
Daily standard deviation is annual divided by $\sqrt{252} \approx 16$: $32\% / 16 = 2\%$.
On a $50$ stock that is about $1$ per day, and a $3$ move would be a 3-standard-deviation day.

## Pitfalls

- Giving a single number with no interval, or an interval with no reasoning behind its width.
- Decomposing into factors you cannot estimate any better than the original.
- False precision: "approximately 627,997 golf balls" signals you do not understand your own error bars.
- Adding factor errors linearly when they are independent (too wide) or in quadrature when they share a cause (too narrow).
- Anchoring on the first number that comes to mind and never cross-checking.
- In a market: quoting too tight to look confident, then failing to update after being traded against.

## Interview questions

> [!question]- int-est-seconds-in-year | Roughly how many seconds are in a year?
> About $3.16 \times 10^7$, within about $0.4\%$ of $\pi \times 10^7$. $365.25 \times 86{,}400 = 31{,}557{,}600$.

> [!question]- int-est-geometric-mean-bounds | You believe a quantity is between 100 and 10,000. What single estimate do you give?
> About 1,000, the geometric mean $\sqrt{100 \times 10{,}000}$. The uncertainty is multiplicative, so the arithmetic mean (about 5,000) overweights the top of the range.

> [!question]- int-est-combining-factor-errors | A Fermi estimate multiplies four independent factors, each uncertain by a factor of 2. How uncertain is the product?
> Roughly a factor of 4. Log errors add in quadrature: $\sqrt{4} \times \ln 2 = \ln 4$. A factor $2^4 = 16$ would assume every error goes the same way.

> [!question]- int-est-daily-vol-from-annual | A stock has $16\%$ annual volatility. Typical one-day standard deviation?
> About $1\%$. Divide by $\sqrt{252} \approx 15.9$.

> [!question]- int-est-piano-tuners | Estimate the number of piano tuners in Chicago.
> About 60, with an 80% interval of roughly 24 to 170.
> About 1.15 million households (Census Bureau), an assumed 1 in 20 with a piano plus 10% for institutions gives about 63,000 pianos tuned yearly, and an assumed 1,000 tunings per tuner a year gives 63.

> [!question]- int-est-golf-balls-bus | Estimate how many golf balls fit in a school bus.
> About half a million. Interior about $40\ \text{m}^3$, ball volume about $40.7\ \text{cm}^3$, packing fraction about $0.64$ gives about $630{,}000$, less roughly a quarter for seats.

> [!question]- int-est-heartbeats-lifetime | Estimate the number of heartbeats in a human lifetime.
> About $3 \times 10^9$. $70 \times 60 \times 24 \times 365 \times 80 \approx 2.9 \times 10^9$; with 60 to 80 beats per minute and 70 to 90 years as 90% ranges, a 90% interval of roughly 2.4 to 3.6 billion.

> [!question]- int-est-hours-in-year | How many hours are in a (non-leap) year?
> $8760$. $365 \times 24$.

> [!question]- int-est-market-after-lifted | You quote 2.7 at 3.1 on an estimate and the interviewer lifts your offer. What do you do next?
> Raise your fair value toward or above 3.1 and quote a new, possibly wider market, such as 3.0 at 3.4. The trade is information: a counterparty who may know the answer found your offer cheap.

> [!question]- int-est-two-decompositions | Why do two independent decompositions of the same Fermi quantity matter?
> Agreement within a factor of 2 or 3 is the only internal evidence that no factor is badly wrong. Disagreement tells you which assumption to revisit before you commit to a market.

> [!question]- int-est-which-mean-to-centre | For a log-normally distributed belief, where should a market be centred?
> Near the median, $e^{\mu}$, which is the geometric mean of symmetric log bounds. The mean $e^{\mu + \sigma^2/2}$ is higher; if the settlement is linear in the quantity and you care about expected P&L, skew the centre up toward the mean.

> [!question]- int-est-correlated-factor-errors | Four factors are each off by a factor of 2, all because of the same optimistic assumption. How far off can the product be?
> A factor of $2^4 = 16$.
> Errors with a common cause add linearly in log space, so quadrature (which gives 4) understates the risk.

> [!question]- int-est-golf-ball-lattice-check | Cross-check a golf-balls-in-a-bus estimate of 630,000 without reusing the packing-fraction division.
> Count a cubic grid: $187 \times 58 \times 46 = 498{,}916$ whole balls of $4.267$ cm fit along the edges of an $8 \times 2.5 \times 2$ m box.
> Cubic stacking fills $\pi/6 \approx 0.524$ of space and random packing about $0.64$, so scale by $1.22$ to about $610{,}000$, within $3\%$.

> [!question]- int-est-packing-fractions | What fraction of space do randomly packed equal spheres fill, and what is the densest possible?
> About $0.64$ for random close packing (Scott and Kilgour measured $0.637$ in 1969).
> The densest packing is face-centred cubic at $\pi/(3\sqrt 2) \approx 0.7405$ (Kepler's conjecture, proved by Hales in 2005); a cubic grid fills only $\pi/6 \approx 0.524$.

> [!question]- int-est-heartbeats-interval | Your heartbeat estimate is $2.9 \times 10^9$ with 60-80 bpm and 70-90 years as 90% ranges. Combine them into a 90% interval.
> About $2.4$ to $3.6$ billion.
> Log half-widths $\tfrac12\ln(4/3) \approx 0.144$ and $\tfrac12\ln(9/7) \approx 0.126$ combine to $\sqrt{0.144^2 + 0.126^2} \approx 0.19$, a factor of $1.21$ either way; multiplying the extremes ($2.2$ to $3.8$ billion) would assume both errors go the same way.

> [!question]- int-est-us-population-anchor | What is the US population to two significant figures, and why should you date it?
> About $3.4 \times 10^8$: the Census Bureau's Vintage 2025 estimate is $341.8$ million on 1 July 2025.
> Populations change every year, so an anchor should carry its year; the 2020 Census counted $331.4$ million residents on April 1 2020 (US Census Bureau apportionment release, April 26 2021).

## In this repo and The-Distinguished-Engineer

- Code: [`code/interview_04_estimation.py`](code/interview_04_estimation.py) prints and asserts every number on this page, separating cited inputs from labelled assumptions; independent routes are a seeded log-normal simulation of the product's quantiles for the quadrature rule and every interval, a cubic-lattice count for the golf balls, and the factor extremes multiplied directly for comparison.
- Related notes: [Trading Games in Interviews](05-Trading-Games-in-Interviews.md), [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md).

## Further reading

- US Census Bureau, QuickFacts for Chicago city, Illinois (2020 Census population; 2019-2023 American Community Survey households), retrieved November 2026; Vintage 2025 national population estimates (released January 2026).
- United Nations, *World Population Prospects 2024: Summary of Results* (2024).
- OECD, *Health at a Glance 2025: OECD Indicators* (2025), life expectancy at birth.
- USGA and The R&A, *Equipment Rules*, Appendix III (the ball): diameter not less than 1.680 inches (42.67 mm).
- G. D. Scott and D. M. Kilgour, "The density of random close packing of spheres", *Journal of Physics D: Applied Physics* 2 (1969), 863-866.
- T. C. Hales, "A proof of the Kepler conjecture", *Annals of Mathematics* 162 (2005), 1065-1185.
- Lawrence Weinstein and John A. Adam, *Guesstimation* (Princeton University Press, 2008).
- Sanjoy Mahajan, *Street-Fighting Mathematics* (MIT Press, 2010), chapters on dimensions and approximation.
- Agustin Lebron, *The Laws of Trading* (2019), on quoting markets under uncertainty and adverse selection.
- [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md).
