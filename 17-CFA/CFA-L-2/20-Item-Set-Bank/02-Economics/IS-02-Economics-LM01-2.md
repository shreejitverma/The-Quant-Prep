---
type: cfa-itemset
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
lm: 1
title: "Tanjong Macro Partners Peso Carry Review"
los: [los-02-01-e, los-02-01-f, los-02-01-g, los-02-01-h, los-02-01-i]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/economics]
---

# Tanjong Macro Partners Peso Carry Review

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Tanjong Macro Partners is a Singapore-based global macro fund whose largest currency position over the past year was a carry trade funded in Swiss francs (CHF) and invested in one-year Mexican peso (MXN) deposits.
Portfolio manager Tomas Lindqvist has asked analyst Priya Raman to review the trade after it closed and to prepare forecasts for the coming year.
All returns on the carry trade are measured in CHF, the funding currency, and all deposit rates are one-year market reference rates.

Exhibit 1: Spot Rates (mid-market)

| Currency pair | At initiation | At unwind (one year later) |
|---|---|---|
| MXN/USD | 18.40 | 19.10 |
| USD/CHF | 1.1350 | 1.1720 |
| JPY/USD | 151.20 | 146.80 |

Exhibit 2: Rates and Inflation Expectations at Initiation (one-year, annual)

| Country | Deposit rate | Expected inflation |
|---|---|---|
| Mexico | 9.40% | 4.20% |
| United States | 4.50% | 2.60% |
| Switzerland | 0.95% | 1.10% |

At initiation, the one-year MXN/USD forward rate was 19.2628.
Raman's price survey at initiation found that a standardized consumption basket cost MXN 1,950 in Mexico and USD 100 in the United States.

Exhibit 3: Monthly Return Statistics of Three Currency Strategies, 2010-2025

| Strategy | Mean | Standard deviation | Skewness | Excess kurtosis |
|---|---|---|---|---|
| X | 0.21% | 1.9% | +0.35 | -0.10 |
| Y | 0.38% | 2.4% | -1.25 | +4.60 |
| Z | 0.30% | 2.2% | +0.02 | +0.05 |

In her first memo, Raman builds a one-year forecast of the MXN/USD rate as of initiation using only the inflation expectations in Exhibit 2, under the assumption that expected exchange rate changes offset expected inflation differentials.
She then decomposes the Mexico-US nominal yield spread into its real and inflation components using the Fisher effect and asks which pair of parity conditions the result contradicts.

Raman also writes: "My uncovered interest rate parity forecast of the MXN/USD rate is 19.2628, exactly equal to the one-year forward rate.
This equality confirms that uncovered interest rate parity holds for the peso and that the forward rate is an unbiased predictor of the future spot rate."

Lindqvist reviews the memo and responds in writing.
He says: "Our peso position has earned money in most years since 2010, which shows that uncovered interest rate parity held over that period.
I want you to confirm which of the strategies in Exhibit 3 is our carry book, since the risk committee has asked me to describe its return profile."

For the performance report, Raman must compute the realized all-in return on the CHF-funded MXN deposit, net of the CHF funding cost.
She notes that no MXN/CHF quote is available in Exhibit 1, so the cross rates at initiation and unwind must be built from the MXN/USD and USD/CHF rates, taking care that the US dollar cancels.

Finally, Lindqvist asks Raman to assess the peso's long-run fair value.
He wants to know whether the price survey indicates that the MXN was overvalued or undervalued against the USD at initiation relative to absolute purchasing power parity, and by how much, measured as the percentage by which the peso's market value in USD differed from its PPP value.
He adds that he will only act on the PPP signal if Raman can explain over what horizon PPP deviations have historically corrected.

## Questions

1. Raman's forecast of the MXN/USD rate one year after initiation, based on the inflation expectations in Exhibit 2, is closest to: (LOS: los-02-01-e)
   - A. 18.11.
   - B. 18.69.
   - C. 19.26.
2. The Mexico-US real yield spread implied by Exhibit 2, and the pair of parity conditions that it shows cannot both hold, are best described as: (LOS: los-02-01-f)
   - A. 3.30%; uncovered interest rate parity and ex ante purchasing power parity.
   - B. 3.30%; covered interest rate parity and uncovered interest rate parity.
   - C. 6.50%; uncovered interest rate parity and ex ante purchasing power parity.
3. Raman's statement about her uncovered interest rate parity forecast is best described as: (LOS: los-02-01-g)
   - A. correct, because covered interest rate parity guarantees that the forward rate equals the expected future spot rate.
   - B. incorrect, because the equality is mechanical and an unbiased forward forecast still requires uncovered interest rate parity.
   - C. incorrect, because the forward rate equals the expected future spot rate only if real interest rate parity also holds.
4. The realized all-in return on the CHF-funded MXN carry trade, net of funding, is closest to: (LOS: los-02-01-i)
   - A. 1.11%.
   - B. 2.06%.
   - C. 7.88%.
5. In response to Lindqvist's request, Raman should most likely identify the carry book as: (LOS: los-02-01-i)
   - A. Strategy X, because carry profits accrue when uncovered interest rate parity holds.
   - B. Strategy Y, because carry profits accrue when uncovered interest rate parity fails, and crowded unwinds produce negative skew.
   - C. Strategy Y, because carry trades earn their profits when covered interest rate parity fails.
6. Based on the price survey, relative to absolute PPP at initiation, the MXN was: (LOS: los-02-01-h)
   - A. overvalued by about 5.98%, a deviation that historically has corrected mainly over horizons of five years or more.
   - B. overvalued by about 5.64%, a deviation that historically has corrected mainly over horizons of five years or more.
   - C. undervalued by about 5.98%, a deviation that historically has corrected mainly within one year.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Ex ante PPP: $\%\Delta S^e_{MXN/USD} = \pi^e_{MXN} - \pi^e_{USD} = 4.20\% - 2.60\% = 1.60\%$, so $S^e = 18.40 \times 1.016 = 18.6944 \approx 18.69$ (the exact ratio $18.40 \times 1.042/1.026 = 18.6869$ also rounds to 18.69).
>    A is wrong because it reverses the inflation differential, strengthening the high-inflation currency: $18.40 \times (1 - 0.016) = 18.1056$.
>    C is wrong because it uses the interest rate differential (uncovered interest rate parity, $18.40 \times 1.094/1.045 = 19.2628$) instead of the inflation differential, and matches the forward rate quoted in the vignette.
> 2. **A.** Fisher effect: real rate Mexico $= 9.40\% - 4.20\% = 5.20\%$; real rate US $= 4.50\% - 2.60\% = 1.90\%$; real spread $= 3.30\%$, equivalently nominal spread $4.90\%$ minus inflation differential $1.60\%$.
>    If uncovered interest rate parity ($\%\Delta S^e = i_f - i_d = 4.90\%$) and ex ante PPP ($\%\Delta S^e = \pi^e_f - \pi^e_d = 1.60\%$) both held, the expected change would be the same number, which forces real rates to be equal; a nonzero real spread means they cannot both hold (and the international Fisher effect fails).
>    B is wrong because covered and uncovered interest rate parity combine into forward rate parity, which says nothing about real rates, and covered parity is enforced by arbitrage.
>    C is wrong because it adds the inflation differential to the nominal spread instead of subtracting it: $4.90\% + 1.60\% = 6.50\%$.
> 3. **B.** Covered interest rate parity sets $F = 18.40 \times 1.094/1.045 = 19.2628$ by arbitrage, and the uncovered parity forecast applies the same ratio, so the two are equal by construction and the equality carries no evidence about expected spot rates.
>    Treating the forward rate as the forecast assumes forward rate parity, which requires uncovered interest rate parity and therefore enough risk-neutral investors; empirically, high-yield currencies have not depreciated by the full yield spread in the short to medium run.
>    A is wrong because covered parity alone fixes the forward rate relative to spot; equating it with the expected future spot rate requires uncovered parity as well.
>    C is wrong because forward rate parity needs covered plus uncovered interest rate parity, not real interest rate parity.
> 4. **A.** Build MXN/CHF $= (\text{MXN/USD}) \times (\text{USD/CHF})$: initiation $18.40 \times 1.1350 = 20.8840$; unwind $19.10 \times 1.1720 = 22.3852$.
>    Gross CHF return $= 20.8840 \times 1.094/22.3852 - 1 = 0.020634 = 2.0634\%$; net of 0.95% CHF funding: $2.0634\% - 0.95\% = 1.1134\% \approx 1.11\%$.
>    Check on CHF 1,000,000: buy MXN 20,884,000, grow to MXN 22,847,096, convert back to CHF 1,020,633.99, repay CHF 1,009,500, profit CHF 11,133.99.
>    B is wrong because it reports the gross return and forgets to subtract the CHF funding cost.
>    C is wrong because it divides instead of multiplying (MXN/USD divided by USD/CHF gives 16.2115 and 16.2969), so the dollar does not cancel; the resulting gross return of 8.8262% less funding gives 7.8762%.
> 5. **B.** Strategy Y shows the carry signature: a higher mean with negative skewness (-1.25) and large excess kurtosis (+4.60), meaning a peaked distribution with fat tails produced by many small gains and occasional crashes when leveraged positions unwind together.
>    Carry earns money because uncovered interest rate parity fails, so Lindqvist's claim that profitability shows parity held is backward; if uncovered parity held, the high-yield currency would depreciate by the yield spread and expected carry returns would be zero.
>    A is wrong because Strategy X has positive skew and thin tails, the opposite of carry, and carry profits require uncovered parity to fail.
>    C is wrong because covered interest rate parity is enforced by arbitrage and its failure would mean mispriced forwards, not carry profits.
> 6. **A.** Absolute PPP rate $= P_{MX}/P_{US} = 1{,}950/100 = 19.50$ MXN/USD, while the market rate is 18.40, so one peso buys more dollars in the market than PPP warrants.
>    Peso value in USD at market $= 1/18.40$; at PPP $= 1/19.50$; overvaluation $= 19.50/18.40 - 1 = 5.9783\% \approx 5.98\%$.
>    The one-year evidence shows little relation between inflation differentials and exchange rate changes, but at horizons of five years or more the relation is strong, so PPP is a long-run anchor.
>    B is wrong because it measures the dollar's undervaluation ($1 - 18.40/19.50 = 5.6410\%$) rather than the peso's overvaluation, using the wrong base.
>    C is wrong because it reverses the direction of the quote, reading a lower MXN/USD rate as a weaker peso, and it claims PPP deviations correct at short horizons.

## Distractor design

- Q1: A reverses the inflation differential (sign); C uses the interest rate differential or reads the forward rate from the vignette (wrong parity condition).
- Q2: B names the parity pair behind forward rate parity (wrong combination); C adds rather than subtracts the inflation differential (sign).
- Q3: A treats covered parity as sufficient for an unbiased forecast; C substitutes real interest rate parity for uncovered parity (wrong condition).
- Q4: B forgets the funding cost (gross versus net); C builds the cross rate by dividing so the USD does not cancel (wrong formula variant).
- Q5: A picks the positively skewed profile and ties carry to parity holding (sign of the relation); C attributes carry profits to covered parity failing (wrong condition).
- Q6: B uses the USD as the base of the percentage (wrong base); C misreads the quote direction and the PPP horizon (sign and horizon).
