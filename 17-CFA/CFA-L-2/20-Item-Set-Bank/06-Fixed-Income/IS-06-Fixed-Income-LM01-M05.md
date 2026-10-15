---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 1
title: "Larchmont Treasury Fund: Riding the Curve and Re-Measuring Its Risk"
los: [los-06-01-d, los-06-01-c, los-06-01-i, los-06-01-k]
difficulty: 4
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Larchmont Treasury Fund: Riding the Curve and Re-Measuring Its Risk

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Solenne Dufour, CFA, manages the Larchmont Treasury Fund, a CAD 400 million fund that holds only Canadian government zero-coupon bonds.
A large share of the fund is earmarked for a known distribution in exactly two years.
Dufour is considering replacing part of her two-year zero-coupon holding with a longer bond that she would sell at the two-year horizon.

Exhibit 1: Canadian government spot rates (annual compounding)

| Maturity (years) | 1 | 2 | 3 | 4 | 5 | 6 | 10 |
|---|---|---|---|---|---|---|---|
| Spot rate | 1.90% | 2.40% | 2.85% | 3.20% | 3.45% | 3.65% | 4.10% |

The three-month Treasury bill yields 1.72%, and the fund's management fee is 0.15% a year; Dufour ignores both in her analysis.

Dufour's candidate is the six-year government zero-coupon bond.
Her base case is that the spot curve in Exhibit 1 will be unchanged two years from today.
She compares the six-year zero, sold after two years, with the maturity-matched two-year zero held to maturity.

Her colleague, Rhys Albright, is unconvinced.
"Your base case is only one outcome," he says.
"Tell me how high the four-year spot rate can be two years from today before your trade does worse than simply holding the two-year zero."
Dufour agrees to compute that breakeven four-year rate from Exhibit 1.

Dufour decides to proceed and switches CAD 100 million of market value from the two-year zero into the six-year zero.

Exhibit 2: Fund holdings at market value (CAD millions)

| Holding | Before the switch | After the switch |
|---|---|---|
| Two-year zero | 220 | to be computed |
| Six-year zero | 100 | to be computed |
| Ten-year zero | 80 | 80 |
| Total | 400 | 400 |

The fund's risk analyst, Kwame Asante, measures curve risk with key rate durations at the 2-, 6- and 10-year points.
For each key rate, he uses the market value weight of the zero at that maturity multiplied by its maturity, the approximation the fund's risk system applies to zero-coupon bonds.
Asante's stress scenario for the risk committee is a bear steepening in which, after the switch, the 2-year key rate rises 10 bps, the 6-year key rate rises 30 bps, and the 10-year key rate rises 45 bps.

The fund's economist, Beatrix Holm, adds two statements to the committee pack.

Statement 1: "Research on government yields finds that monetary policy explains most of the variation in short- and intermediate-term yields, whereas inflation expectations explain most of the variation in long-term yields."

Statement 2: "The finance ministry plans to shorten the average maturity of its new bond issuance."
"By adding duration supply to the market, this should raise the bond risk premium and push long-term yields higher."

Dufour wants each statement checked before the pack is circulated.

## Questions

1. Under Dufour's base case, the annualized two-year horizon return on the six-year zero-coupon bond is closest to: (LOS: los-06-01-d)
   - A. 2.40%.
   - B. 3.65%.
   - C. 4.56%.
2. The breakeven four-year spot rate two years from today that answers Albright's question is closest to: (LOS: los-06-01-c)
   - A. 4.01%.
   - B. 4.28%.
   - C. 4.56%.
3. Under Asante's stress scenario, the change in the fund's value is closest to: (LOS: los-06-01-i)
   - A. -CAD 5.84 million.
   - B. -CAD 6.35 million.
   - C. -CAD 7.44 million.
4. Which of Holm's statements is correct? (LOS: los-06-01-k)
   - A. Statement 1 only.
   - B. Statement 2 only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Buy the six-year zero at $100/(1.0365)^6 = 100/1.239983 = 80.6462$.
> With the curve unchanged, in two years it is a four-year zero priced at the four-year spot rate: $100/(1.032)^4 = 100/1.134276 = 88.1620$.
> Annualized return $= (88.1620/80.6462)^{1/2} - 1 = (1.093194)^{1/2} - 1 = 4.5559\%$, about 4.56%.
> The result equals the forward rate that rolls out of the pricing, $f_{4,2} = [(1.0365)^6/(1.032)^4]^{1/2} - 1 = 4.56\%$, and it beats the 2.40% maturity-matched return because a static upward-sloping curve lets the bond roll down to a lower yield.
> A is wrong because it is the return on the maturity-matched two-year zero, which is also the return every bond earns over two years if spot rates evolve as the forward curve implies, not if the curve stays static.
> B is wrong because it assumes the bond is sold at its original 3.65% yield, which equates the horizon return with the six-year yield and ignores the rolldown gain.
> 2. **B.** The six-year zero underperforms the two-year zero when its two-year growth factor falls below $(1.024)^2 = 1.048576$.
> Breakeven: $\frac{100/(1+z_4^*)^4}{100/(1.0365)^6} = (1.024)^2$, so $(1+z_4^*)^4 = (1.0365)^6/(1.024)^2 = 1.239983/1.048576 = 1.182540$.
> $z_4^* = 1.182540^{1/4} - 1 = 4.2807\%$, about 4.28%, which is the implied forward rate $f_{2,4}$ for a four-year loan beginning in two years.
> Check: at 4.28% the sale price is $100/1.182540 = 84.5637$ and $(84.5637/80.6462)^{1/2} - 1 = 2.40\%$.
> The trade therefore beats maturity matching as long as the four-year spot rate in two years stays below today's forward rate, a rise of up to about 108 bps from today's 3.20%: rolling down the curve is a bet that future spot rates will be lower than the forward curve implies.
> A is wrong because it uses the wrong end date, $f_{2,2} = [(1.032)^4/(1.024)^2]^{1/2} - 1 = (1.081730)^{1/2} - 1 = 4.01\%$, the forward for a loan ending in year 4 rather than year 6.
> C is wrong because it swaps the subscripts and computes $f_{4,2} = 4.56\%$, the rate for a two-year loan beginning in four years, which is the Question 1 static-curve return rather than a breakeven.
> 3. **C.** After the switch the holdings are $220 - 100 = 120$, $100 + 100 = 200$ and $80$, with weights 0.30, 0.50 and 0.20.
> Key rate durations: $KeyDur_2 = 0.30 \times 2 = 0.60$, $KeyDur_6 = 0.50 \times 6 = 3.00$, $KeyDur_{10} = 0.20 \times 10 = 2.00$; they sum to an effective duration of 5.60.
> $\%\Delta P = -[0.60(0.0010) + 3.00(0.0030) + 2.00(0.0045)] = -[0.0006 + 0.0090 + 0.0090] = -0.0186$, or $-1.86\%$.
> Value change $= -0.0186 \times 400 = -\text{CAD } 7.44$ million.
> A is wrong because it uses the pre-switch holdings (weights 0.55, 0.25, 0.20; KRDs 1.10, 1.50, 2.00): $-[0.0011 + 0.0045 + 0.0090] = -1.46\%$, or $-5.84$ million, which misses the extra 6-year exposure the switch created.
> B is wrong because it applies the 5.60 effective duration to the average shift of $(10 + 30 + 45)/3 = 28.33$ bps: $-5.60 \times 0.002833 \times 400 = -6.35$ million, which ignores shaping risk in a non-parallel scenario.
> 4. **A.** Statement 1 is correct: monetary policy explains about two-thirds of the variation in short- and intermediate-term government yields, and inflation explains about two-thirds of the variation in long-term yields.
> Statement 2 is incorrect: shortening the maturity structure of government debt reduces, not adds, the duration supplied to investors, which tends to lower the bond risk premium and long-term yields; a lengthening maturity structure (like larger deficits) raises them.
> B is wrong because it accepts a statement with the supply effect reversed and rejects a correct statement on the drivers of yields.
> C is wrong because Statement 2 misstates the direction in which the maturity structure of government debt moves the bond risk premium.

## Distractor design

1. A: maturity-matched or forward-consistent return used instead of the static-curve return (wrong scenario); B: sale at the original yield, horizon return equated with YTM (rolldown gain ignored).
2. A: forward with the wrong end date, $f_{2,2}$ from $z_4$ and $z_2$ (period); C: subscripts swapped, $f_{4,2}$ instead of $f_{2,4}$ (spot vs forward notation).
3. A: pre-switch holdings used to weight the key rate durations (misread exhibit); B: effective duration times the average shift (shaping risk ignored).
4. B: supply effect of the debt maturity structure reversed (sign); C: accepts the reversed supply effect alongside the correct statement.
