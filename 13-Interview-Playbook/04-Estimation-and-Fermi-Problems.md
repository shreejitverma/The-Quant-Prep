---
type: concept
track: [quant-trader]
tier: core
status: solid
prereqs: []
est_hours: 2
sources: [Lawrence Weinstein and John A. Adam - Guesstimation (Princeton University Press 2008), Sanjoy Mahajan - Street-Fighting Mathematics (MIT Press 2010), Agustin Lebron - The Laws of Trading (2019)]
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

### What is being scored

Nobody expects you to know the number of piano tuners in Chicago.
The interviewer scores the structure of the decomposition, the reasonableness of each input, the arithmetic, and whether you know how uncertain you are.
In trading interviews the question commonly arrives as "make me a market on X", which adds a second skill: quoting a width that will not be picked off.

### Decomposition

Pick a chain of factors whose product is the target, each of which you can estimate from everyday knowledge.

- **Top-down (demand side):** population $\times$ fraction who use it $\times$ frequency.
- **Bottom-up (supply side):** number of suppliers $\times$ capacity per supplier.
- **Physical:** volume of container $/$ volume per item $\times$ packing fraction.

Doing two decompositions and seeing whether they agree within a factor of 2 or 3 is the best available check.

### Useful anchors

| Quantity | Value to use |
| :--- | :--- |
| Seconds in a year | $3.16 \times 10^7 \approx \pi \times 10^7$ |
| Hours in a year | $8760$ |
| Trading days in a year (US convention) | $252$, and $\sqrt{252} \approx 15.9 \approx 16$ |
| World population | about $8 \times 10^9$ |
| US population | about $3.3 \times 10^8$ |
| Earth's circumference | about $40{,}000$ km |
| Human lifespan in developed countries | about 80 years |

Keep the list short and memorise it; any figure you are unsure of should be labelled an assumption.

### Intervals and the geometric mean

If you believe a quantity lies between $L$ and $U$ with $U/L$ large, the natural midpoint is $\sqrt{LU}$, because your uncertainty is multiplicative.
For each factor give a low and high value; the product's interval in log space has half-width $\sqrt{\sum_i \sigma_i^2}$ when the factor errors are independent, where $\sigma_i$ is the log half-width of factor $i$.
Four factors each good to a factor of 2 give $2^{\sqrt 4} = 4$ overall, and nine such factors give $2^3 = 8$.
If the errors are correlated (all driven by the same optimistic assumption) they add linearly and the interval is much wider.

### From interval to market

A market is a bid and an ask around your estimate.

- Centre it on your best estimate (the median of your belief, which for a log-normal belief is the geometric mean).
- Set the width from your uncertainty: wide enough that a knowledgeable counterparty cannot trade against you at a large edge, narrow enough to be useful.
  Many interviewers will push for tighter; tighten when you have a reason, not because you are asked.
- If the interviewer lifts your offer or hits your bid, treat it as information: they may know the answer, so move your fair value toward their side before quoting again.
- Keep track of what you have bought and sold; the same bookkeeping as in [Trading Games in Interviews](05-Trading-Games-in-Interviews.md).

## Worked examples

### Example 1: piano tuners in Chicago

Demand side.
Chicago has about 2.7 million people, or about $2.7 \times 10^6 / 2.5 \approx 1.1$ million households.
Assume 1 in 20 households has a piano: about $54{,}000$ pianos, plus perhaps $10\%$ more in schools, churches and venues, so about $60{,}000$.
Assume each is tuned once a year: $60{,}000$ tunings per year.

Supply side.
A tuner does about 4 tunings a day (2 hours each including travel) for 250 days: $1000$ tunings a year.

Answer: about $60{,}000 / 1000 = 60$ tuners.
Uncertainty: the piano fraction (1 in 10 to 1 in 40) and tuning frequency (every 1 to 3 years) dominate; each is good to about a factor of 2, so a reasonable 80% interval is about 25 to 150.

### Example 2: golf balls in a school bus

A bus interior is about $8 \times 2.5 \times 2$ m, or $40\ \text{m}^3 = 4 \times 10^7\ \text{cm}^3$.
A golf ball has diameter $4.27$ cm, so volume $\tfrac{4}{3}\pi (2.135)^3 \approx 41\ \text{cm}^3$.
Randomly packed spheres fill about $64\%$ of space.
$4 \times 10^7 \times 0.64 / 41 \approx 630{,}000$.
Seats and fittings take perhaps a quarter of the space, giving about $470{,}000$, so say "about half a million, within a factor of 1.5".
The quick check $\text{(cm}^3\text{ per ball incl. gaps)} \approx 64$ means about $4 \times 10^7 / 64 \approx 600{,}000$ before seats, which agrees.

### Example 3: a market on heartbeats in a lifetime

Estimate: 70 beats per minute $\times$ 60 $\times$ 24 $\times$ 365 $\times$ 80 years $\approx 2.9 \times 10^9$.
Uncertainty: the average rate is 60 to 80 (a factor of about 1.15 either way) and lifespan 70 to 90 (about 1.13), so a 90% interval of about $2.3$ to $3.7$ billion.
Quote "2.7 at 3.1 billion" to start: centred on $2.9$, width about $\pm 7\%$, inside the interval so each side has positive expected value against an uninformed counterparty.
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
> About $3.16 \times 10^7$, conveniently $\pi \times 10^7$. $365.25 \times 86{,}400 = 31{,}557{,}600$.

> [!question]- int-est-geometric-mean-bounds | You believe a quantity is between 100 and 10,000. What single estimate do you give?
> About 1,000, the geometric mean $\sqrt{100 \times 10{,}000}$. The uncertainty is multiplicative, so the arithmetic mean (about 5,000) overweights the top of the range.

> [!question]- int-est-combining-factor-errors | A Fermi estimate multiplies four independent factors, each uncertain by a factor of 2. How uncertain is the product?
> Roughly a factor of 4. Log errors add in quadrature: $\sqrt{4} \times \ln 2 = \ln 4$. A factor $2^4 = 16$ would assume every error goes the same way.

> [!question]- int-est-daily-vol-from-annual | A stock has $16\%$ annual volatility. Typical one-day standard deviation?
> About $1\%$. Divide by $\sqrt{252} \approx 15.9$.

> [!question]- int-est-piano-tuners | Estimate the number of piano tuners in Chicago.
> About 50 to 60, with an interval of roughly 25 to 150. About 1.1 million households, 1 in 20 with a piano plus institutions gives about 60,000 pianos tuned yearly, and a tuner does about 1,000 tunings a year.

> [!question]- int-est-golf-balls-bus | Estimate how many golf balls fit in a school bus.
> About half a million. Interior about $40\ \text{m}^3$, ball volume about $41\ \text{cm}^3$, packing fraction about $0.64$ gives about $630{,}000$, less roughly a quarter for seats.

> [!question]- int-est-heartbeats-lifetime | Estimate the number of heartbeats in a human lifetime.
> About $3 \times 10^9$. $70 \times 60 \times 24 \times 365 \times 80 \approx 2.9 \times 10^9$; a 90% interval of roughly 2.3 to 3.7 billion.

> [!question]- int-est-hours-in-year | How many hours are in a (non-leap) year?
> 8760. $365 \times 24$.

> [!question]- int-est-market-after-lifted | You quote 2.7 at 3.1 on an estimate and the interviewer lifts your offer. What do you do next?
> Raise your fair value toward or above 3.1 and quote a new, possibly wider market, such as 3.0 at 3.4. The trade is information: a counterparty who may know the answer found your offer cheap.

> [!question]- int-est-two-decompositions | Why do two independent decompositions of the same Fermi quantity matter?
> Agreement within a factor of 2 or 3 is the only internal evidence that no factor is badly wrong. Disagreement tells you which assumption to revisit before you commit to a market.

> [!question]- int-est-which-mean-to-centre | For a log-normally distributed belief, where should a market be centred?
> Near the median, $e^{\mu}$, which is the geometric mean of symmetric log bounds. The mean $e^{\mu + \sigma^2/2}$ is higher; if the settlement is linear in the quantity and you care about expected P&L, skew the centre up toward the mean.

## Further reading

- Lawrence Weinstein and John A. Adam, *Guesstimation* (Princeton University Press, 2008).
- Sanjoy Mahajan, *Street-Fighting Mathematics* (MIT Press, 2010), chapters on dimensions and approximation.
- Agustin Lebron, *The Laws of Trading* (2019), on quoting markets under uncertainty and adverse selection.
- [Market Making Games and Trading Simulations](../08-Market-Making/10-Market-Making-Games.md).
