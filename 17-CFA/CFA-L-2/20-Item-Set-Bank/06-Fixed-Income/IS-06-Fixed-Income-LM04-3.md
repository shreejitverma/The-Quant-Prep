---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 4
title: "Castlebrook Savings Bank: Quarterly Credit Risk Report"
los: [los-06-04-b, los-06-04-c, los-06-04-d]
difficulty: 3
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Castlebrook Savings Bank: Quarterly Credit Risk Report

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ines Moreau, CFA, prepares the quarterly credit risk report for the board risk committee of Castlebrook Savings Bank, a regional lender with a retail loan book and a treasury portfolio of corporate bonds.
Her head of credit, Daniel Achebe, reviews each section before it goes to the committee.

The largest treasury holding is a 10-year senior unsecured note of Veloria Telecom, rated A.
The note yields 4.85% to maturity, and its expected modified duration at the end of one year is 6.40.
Moreau measures the effect of possible rating migration over the next year with the transition probabilities in Exhibit 1 and the credit spreads in Exhibit 2.
Because the note is investment grade, the bank's policy ignores the probability of default in this calculation.

Exhibit 1: One-year transition probabilities (%), selected rows

| From / To | AAA | AA | A | BBB | BB | B | CCC, CC, C | D |
|---|---|---|---|---|---|---|---|---|
| A | 0.08 | 2.20 | 88.10 | 7.90 | 1.05 | 0.45 | 0.14 | 0.08 |
| BBB | 0.03 | 0.25 | 5.10 | 85.40 | 6.80 | 1.60 | 0.60 | 0.22 |

Exhibit 2: Credit spreads on 10-year corporate bonds

| Rating | AAA | AA | A | BBB | BB | B | CCC, CC, C |
|---|---|---|---|---|---|---|---|
| Spread | 0.55% | 0.80% | 1.05% | 1.60% | 3.20% | 5.90% | 9.80% |

Veloria's issuer rating is A, but its subordinated notes, which the bank does not hold, carry a BBB rating from the same agency.
Achebe asks Moreau to explain the gap between the issuer rating and the issue rating in the report.

The retail section covers consumer lending.
One borrower, Karen Olsen, saw her FICO score fall from 748 to 721 during the quarter.
Her file shows three events: her card issuer cut her credit limit from USD 12,000 to USD 6,000 while her balance stayed at USD 4,500; she checked her own score online three times; and she turned 50.
She made every payment on time.

The final section reviews two default models proposed by an external consultant for the bank's commercial loan book.

Model X estimates each borrower's asset value and asset volatility from its share price and equity volatility, sets a default barrier equal to short-term debt plus half of long-term debt, and measures the probability of default as the portion of the future asset value distribution below that barrier.

Model Y estimates each borrower's default intensity with a logit regression on its leverage ratio, cash-to-assets ratio, the national unemployment rate, and GDP growth.

To illustrate Model X for the committee, Moreau uses Brenna Logistics, a borrower with a single zero-coupon debt issue of EUR 450 million due in one year.
In one scenario, Brenna's asset value at maturity is EUR 380 million.
Achebe suggests she present the payoffs with the put-based reading, in which debtholders own a default-free bond and have written a put on the company's assets.

## Questions

1. If the Veloria note is downgraded to BB over the next year, its percentage price change is closest to: (LOS: los-06-04-c)
   - A. -20.48%.
   - B. -13.76%.
   - C. +13.76%.
2. The expected one-year return on the Veloria note, adjusted for rating migration, is closest to: (LOS: los-06-04-c)
   - A. 3.45%.
   - B. 4.25%.
   - C. 5.45%.
3. The most appropriate explanation of the lower rating on Veloria's subordinated notes is that: (LOS: los-06-04-b)
   - A. the agency has placed the subordinated notes on watch with a negative outlook, pending a downgrade of the issuer.
   - B. the subordinated notes have a higher probability of default than the senior notes of the same issuer.
   - C. the agency has notched the issue rating down from the issuer rating to reflect lower expected recovery given subordination.
4. Which event in Olsen's file most likely explains the decline in her FICO score? (LOS: los-06-04-b)
   - A. The cut in her credit limit.
   - B. Checking her own score three times.
   - C. Turning 50.
5. Which statement about the consultant's models is most accurate? (LOS: los-06-04-d)
   - A. Model X is a reduced-form model, because its inputs come from observable equity market data.
   - B. Model Y's main weakness is that it offers no economic explanation of why default occurs.
   - C. Model X's main weakness is that option pricing makes it too complex to compute.
6. In the Brenna scenario, under the put-based reading, the payoff to debtholders and the payoff on the put at maturity (EUR millions) are closest to: (LOS: los-06-04-d)
   - A. debtholders 380; put 70.
   - B. debtholders 450; put 70.
   - C. debtholders 380; put 0.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Percentage price change $= -MD \times \Delta\text{spread} = -6.40 \times (3.20\% - 1.05\%) = -6.40 \times 2.15\% = -13.76\%$.
> A is wrong because it multiplies duration by the destination spread level, $-6.40 \times 3.20\% = -20.48\%$, instead of the spread change.
> C is wrong because it drops the minus sign; a wider spread lowers the price.
> 2. **B.** Use the A row, because the note is currently rated A, and ignore the default column per policy.
> Price changes $-6.40 \times (s_i - 1.05\%)$: AAA $+3.20\%$; AA $+1.60\%$; A $0$; BBB $-3.52\%$; BB $-13.76\%$; B $-31.04\%$; CCC, CC, C $-56.00\%$.
> Weighted: $(0.0008)(3.20) + (0.0220)(1.60) + (0.8810)(0) + (0.0790)(-3.52) + (0.0105)(-13.76) + (0.0045)(-31.04) + (0.0014)(-56.00)$.
> $= 0.0026 + 0.0352 + 0 - 0.2781 - 0.1445 - 0.1397 - 0.0784 = -0.6029\%$.
> Expected return $= 4.85\% - 0.6029\% = 4.2471\%$, about 4.25%.
> A is wrong because it weights the destination spread levels instead of the spread changes (sum $-1.3972\%$, return $3.4528\%$).
> C is wrong because it adds the migration drag to the YTM instead of subtracting it ($4.85\% + 0.6029\% = 5.4529\%$).
> 3. **C.** Agencies rate the issuer on its senior unsecured obligations and then notch individual issues for priority of claim; subordinated debt recovers less in default, so its issue rating sits below the issuer rating.
> This is how ratings fold loss given default in, which is why they are credit ratings and not just default ratings.
> A is wrong because watch and outlook status signal a possible future change to a rating; they do not explain a standing gap between two issues of the same issuer.
> B is wrong because cross-default provisions mean all of an issuer's debt shares the same probability of default; the issues differ in severity, not in the likelihood of the event.
> 4. **A.** Debt burden (30% weight) includes the ratio of balances to credit limits; with a USD 4,500 balance, utilization rose from $4{,}500/12{,}000 = 37.5\%$ to $4{,}500/6{,}000 = 75\%$, which lowers the score.
> B is wrong because self-checks are soft inquiries and do not enter the score; only hard inquiries from credit applications count.
> C is wrong because age is not a scoring factor; only the length of credit history is.
> 5. **B.** Model Y is reduced-form: default intensity is regressed on observable company and macro variables.
> Its weakness is that it treats default as a statistical surprise and gives no economic explanation of why default happens.
> A is wrong because Model X, with an asset value, asset volatility and a default barrier, is the structural model; using equity market data to infer asset values does not make it reduced-form.
> C is wrong because computing power makes option pricing no harder than regression; the real weakness of structural models is that asset values and the default barrier are not observable.
> 6. **A.** Debtholders own a default-free bond paying $K = 450$ and have written a put struck at $K$ on the assets.
> With $A(T) = 380 < K$, the put pays $\max(450 - 380, 0) = 70$, so debtholders receive $450 - 70 = 380$, the whole asset value, and equity receives $\max(380 - 450, 0) = 0$.
> The 70 is the value of shareholders' limited liability, transferred from debtholders.
> B is wrong because it credits debtholders with the default-free bond and ignores that they wrote the put.
> C is wrong because it reports the payoff on the call (equity), which is zero in this scenario, as the put payoff.

## Distractor design

1. A: destination spread level used instead of the spread change; C: sign of the duration relationship dropped.
2. A: destination spread levels weighted instead of spread changes; C: migration drag added to YTM instead of subtracted (sign).
3. A: outlook or watch status confused with notching; B: issue notching attributed to POD instead of LGD.
4. B: soft inquiry treated as a hard inquiry; C: borrower age confused with length of credit history.
5. A: structural model mislabeled because it uses equity prices; C: complexity named instead of the unobservable inputs weakness.
6. B: written put ignored (default-free bond payoff given to debtholders); C: call payoff substituted for the put payoff.
