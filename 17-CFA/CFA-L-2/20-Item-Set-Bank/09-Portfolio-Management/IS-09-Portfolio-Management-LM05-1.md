---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 5
title: "Norhaven Bank: Limit Review of the Macro Desk"
los: [los-09-05-a, los-09-05-c, los-09-05-d, los-09-05-e, los-09-05-j]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Norhaven Bank: Limit Review of the Macro Desk

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ingrid Solberg, CFA, is head of market risk at Norhaven Bank, a commercial bank with a proprietary trading operation.
She is conducting the annual limit review of the macro desk run by Mathis Kerr.
The desk holds EUR 240 million of exposure, mapped through risk decomposition to two risk factors: 60% to a euro-area equity index and 40% to euro government bonds.
Norhaven measures desk risk with a parametric one-day VaR at the 1% level, assuming a normal distribution and 250 trading days per year.

The risk committee judged the three-year lookback period to be unrepresentatively calm.
It therefore keeps the lookback mean returns but replaces the lookback volatilities and correlation with long-run estimates, and the bank uses only the committee inputs for limit calculations.

Exhibit 1: Risk-factor inputs (annual)

| Input | Equity factor | Government bond factor |
|---|---|---|
| Expected return | 9.0% | 3.5% |
| Standard deviation, lookback sample | 15.8% | 5.1% |
| Standard deviation, committee estimate | 22.0% | 7.0% |
| Correlation with the other factor, lookback sample | 0.05 | 0.05 |
| Correlation with the other factor, committee estimate | -0.15 | -0.15 |

The desk's one-day 1% VaR limit is EUR 5.0 million.
Kerr proposes raising the equity weight to 70% and cutting the bond weight to 30%, leaving total exposure unchanged at EUR 240 million.

Solberg next reviews the desk's recent record.
Over the last 60 trading days, no daily loss exceeded the desk's VaR, yet the desk lost EUR 14.6 million cumulatively, almost all of it on days with losses between EUR 3 million and EUR 4 million.
Kerr comments: "Zero breaches in 60 days proves our VaR model is conservative, so the committee should raise my limit."

Solberg drafts a summary for the board risk committee, which asks how often the desk should expect a loss at least as large as its VaR in a 250-day trading year and what those days look like.

She also proposes three new controls for the desk:

- Control 1: Gross notional exposure to any single sovereign issuer may not exceed EUR 60 million.
- Control 2: Under the bank's hypothetical "euro-area fragmentation" scenario, the desk's estimated loss may not exceed EUR 25 million.
- Control 3: If the desk's cumulative loss over any rolling 20-day window exceeds EUR 12 million, the desk must halve its positions.

Finally, the bank's capital planning team asks for an annual 1% VaR for the desk at the current 60/40 weights.
Kerr suggests they take the one-day 1% VaR and multiply it by the square root of 250, "since risk scales with the square root of time."
Solberg insists the calculation be rebuilt from the annual inputs.

## Questions

1. Using the inputs the bank uses for limit calculations, the desk's current one-day 1% VaR is closest to: (LOS: los-09-05-c)
   - A. EUR 3.21 million.
   - B. EUR 3.40 million.
   - C. EUR 4.56 million.
2. The incremental VaR (one-day, 1%) of Kerr's proposed reallocation is closest to: (LOS: los-09-05-e)
   - A. a decrease of EUR 0.76 million.
   - B. an increase of EUR 0.76 million.
   - C. an increase of EUR 5.31 million.
3. Solberg's board summary most accurately states that the desk should expect a one-day loss at least as large as its VaR on approximately: (LOS: los-09-05-a)
   - A. 2.5 trading days a year, and losses on those days can be much larger than the VaR.
   - B. 12.5 trading days a year, and losses on those days can be much larger than the VaR.
   - C. 2.5 trading days a year, and losses on those days will not exceed the VaR by more than one standard deviation.
4. The desk's record over the last 60 trading days is best explained by: (LOS: los-09-05-d)
   - A. the parametric method ignoring the left tail of the return distribution.
   - B. the vulnerability of VaR to trending, in which losses accumulate without a single breach.
   - C. the model overstating risk, as Kerr concludes, because at least one breach should have occurred in 60 days.
5. Which of Solberg's proposed controls most directly addresses the pattern in the desk's recent record? (LOS: los-09-05-j)
   - A. Control 1, a position limit.
   - B. Control 2, a scenario limit.
   - C. Control 3, a stop-loss limit.
6. The annual 1% VaR that Solberg's method produces for the current portfolio is closest to: (LOS: los-09-05-c)
   - A. EUR 56.8 million.
   - B. EUR 72.1 million.
   - C. EUR 73.1 million.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Use the committee inputs. $E(R_p) = 0.60(0.090) + 0.40(0.035) = 0.0540 + 0.0140 = 0.0680$.
> Variance terms: $0.60^2(0.22)^2 = 0.017424$; $0.40^2(0.07)^2 = 0.000784$; $2(0.60)(0.40)(-0.15)(0.22)(0.07) = -0.0011088$; sum $0.0170992$, so $\sigma_p = 0.130764$.
> Daily scaling: $0.0680/250 = 0.000272$ and $0.130764/\sqrt{250} = 0.130764/15.811388 = 0.008270$.
> VaR $= [2.33(0.008270) - 0.000272] \times 240{,}000{,}000 = (0.019270 - 0.000272) \times 240{,}000{,}000 = 0.018998 \times 240{,}000{,}000 = \text{EUR } 4{,}559{,}436$, about EUR 4.56 million.
> A is wrong because it applies the 5% cutoff $z = 1.65$: $(0.013646 - 0.000272) \times 240\text{m} = \text{EUR } 3{,}209{,}733$.
> B is wrong because it uses the lookback volatilities and correlation the committee rejected: $\sigma_p = 0.097962$, daily $0.006195$, VaR $= (2.33 \times 0.006195 - 0.000272) \times 240\text{m} = \text{EUR } 3{,}399{,}341$.
> 2. **B.** Incremental VaR is the VaR after the change minus the VaR before it, with the whole portfolio recomputed.
> At 70/30: $E(R_p) = 0.0630 + 0.0105 = 0.0735$; variance $= 0.023716 + 0.000441 - 0.0009702 = 0.0231868$, so $\sigma_p = 0.152272$.
> Daily: $0.0735/250 = 0.000294$ and $0.152272/15.811388 = 0.009631$.
> New VaR $= (2.33 \times 0.009631 - 0.000294) \times 240\text{m} = 0.022145 \times 240\text{m} = \text{EUR } 5{,}314{,}835$.
> IVaR $= 5{,}314{,}835 - 4{,}559{,}436 = +\text{EUR } 755{,}399$, an increase of about EUR 0.76 million that would also take the desk above its EUR 5.0 million limit.
> A is wrong because it reverses the sign: shifting weight to the more volatile factor, whose correlation with bonds is only mildly negative, raises portfolio risk.
> C is wrong because it reports the new VaR itself rather than the change in VaR.
> 3. **A.** A one-day 1% VaR is the minimum loss expected on 1% of trading days, so over 250 days the expected count is $0.01 \times 250 = 2.5$ days.
> VaR says nothing about how large losses are once the threshold is crossed, so those days can be much worse (the average of such losses is what CVaR measures).
> B is wrong because it uses the 5% convention: $0.05 \times 250 = 12.5$ days.
> C is wrong because it treats VaR as a bound on the tail; the maximum possible loss is the entire position.
> 4. **B.** The desk lost EUR 14.6 million by losing EUR 3 million to EUR 4 million repeatedly, just under a VaR of about EUR 4.56 million, which is the trending limitation: a portfolio can accumulate large losses without ever breaching a daily VaR.
> A is wrong because the parametric method does model the left tail (it may understate its frequency, but that would produce breaches, not zero breaches with large cumulative losses).
> C is wrong because at 1% the expected number of breaches in 60 days is only $0.01 \times 60 = 0.6$, so zero breaches is entirely consistent with an accurate model and is no evidence of conservatism.
> 5. **C.** A stop-loss limit forces a reduction in size after a realized loss over a specified period, which is the direct answer to trending losses that stay under the VaR limit day after day.
> A is wrong because a position limit caps market value or notional against concentration; it does not respond to accumulated losses.
> B is wrong because a scenario limit caps the estimated loss under a hypothetical event, not realized losses as they accumulate.
> 6. **A.** Rebuild from annual inputs rather than scaling the finished VaR: $2.33 \times 0.130764 = 0.304680$; $0.304680 - 0.0680 = 0.236680$; $0.236680 \times 240{,}000{,}000 = \text{EUR } 56{,}803{,}178$, about EUR 56.8 million.
> B is wrong because it follows Kerr: $4{,}559{,}436 \times \sqrt{250} = 4{,}559{,}436 \times 15.811388 = \text{EUR } 72{,}091{,}011$, which scales the mean by $\sqrt{250}$ instead of 250.
> C is wrong because it omits the expected return offset: $0.304680 \times 240\text{m} = \text{EUR } 73{,}123{,}178$.

## Distractor design

1. A: wrong threshold (5% z of 1.65 on a 1% question); B: misread exhibit (lookback volatilities and correlation instead of committee estimates).
2. A: sign error on the incremental VaR; C: new VaR reported instead of the before-and-after difference.
3. B: wrong convention (5% frequency applied to a 1% VaR); C: VaR misread as a cap on tail losses.
4. A: invented limitation (parametric VaR does model the left tail); C: breach-count inference without computing the expected number of breaches (0.6 in 60 days).
5. A: position limit confused with a loss-triggered control; B: scenario limit (hypothetical loss) confused with realized-loss control.
6. B: finished daily VaR multiplied by $\sqrt{250}$ (mixes scaling laws of mean and volatility); C: expected return omitted from the VaR formula.
