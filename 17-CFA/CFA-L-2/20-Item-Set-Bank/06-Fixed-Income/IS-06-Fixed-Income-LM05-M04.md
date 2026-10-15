---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Ashcombe Teachers' Pension Plan: Building a CDS Program"
los: [los-06-05-b, los-06-05-c, los-06-05-d]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Ashcombe Teachers' Pension Plan: Building a CDS Program

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Farah Idowu, CFA, is a senior credit analyst at Ashcombe Teachers' Pension Plan, a US public pension plan that has recently begun to use single-name credit default swaps.
All of Ashcombe's contracts are documented under the Standard North American Contract, with standardized coupons of 1% for investment-grade and 5% for high-yield reference entities.
Idowu works with Rafael Gant, an external consultant from Tidewater Risk Advisors, who has built a simple CDS pricing model for the plan.

Gant's model values a CDS as two legs.
The protection leg is the present value of expected losses.
The expected loss in each year equals loss given default times the probability that default occurs in that year, and that probability equals the year's hazard rate times the probability of surviving to the start of the year.
The premium leg is the present value of the annual coupons, each paid at year-end only if the reference entity has survived the year.
Defaults are assumed to occur at year-end, and all cash flows are discounted at a flat risk-free rate of 3.0% with annual compounding.

Ashcombe plans to buy three-year protection on Quillon Packaging, an investment-grade issuer, and Gant assumes an expected recovery rate of 40%.

Exhibit 1: Quillon Packaging annual hazard rates from Gant's model

| Year | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|
| Hazard rate | 1.5% | 2.2% | 2.8% | 3.3% | 3.7% |

Ashcombe has also sold $18 million of five-year protection on Meriden Holdings, a diversified health care company.
Last month, Meriden spun off its generic drugs division as a separately listed company, Castell Generics, which assumed about 40% of Meriden's outstanding bonds.
Meriden has made every scheduled payment on its debt and has not filed for bankruptcy.
Gant tells Idowu: "The spinoff changed who owes the bonds our contract covers, so the Meriden CDS will be settled in about 30 days, and we should budget for a payment to the protection buyer."

Finally, Idowu reviews Ridgeway Airlines, a high-yield carrier whose senior unsecured bonds Ashcombe holds.
Ridgeway faces a large aircraft lease payment and a bond maturity within the next 18 months, but its new fleet is expected to lower its operating costs substantially after that.
Idowu therefore expects Ridgeway's near-term credit risk to rise relative to its long-term credit risk.
She implements the CDS curve trade consistent with her view, using $30 million of notional on the two-year contract and $12 million of notional on the ten-year contract.

Exhibit 2: Ridgeway Airlines CDS

| Maturity | Spread at trade date (bps) | Spread three months later (bps) | Effective spread duration |
|---|---|---|---|
| 2 years | 180 | 330 | 1.9 |
| 5 years | 260 | 345 | 4.4 |
| 10 years | 310 | 350 | 8.0 |

Idowu assumes that the effective spread durations do not change over the three months.

## Questions

1. Using Gant's model and Exhibit 1, the present value of the protection leg of the Quillon contract per 100 of notional is closest to: (LOS: los-06-05-c)
   - A. 3.58.
   - B. 3.66.
   - C. 3.82.
2. At initiation of the Quillon contract, Ashcombe will most likely: (LOS: los-06-05-c)
   - A. pay an upfront payment of about 0.86% of notional, at a price of about 99.14.
   - B. pay an upfront payment of about 0.75% of notional, at a price of about 99.25.
   - C. receive an upfront payment of about 0.86% of notional, at a price of about 100.86.
3. Gant's statement about the Meriden spinoff is most likely: (LOS: los-06-05-b)
   - A. correct, because a change in the obligor of the covered bonds is a credit event.
   - B. incorrect, because the spinoff is a succession event, and the Determinations Committee may split the contract between Meriden and Castell.
   - C. incorrect, because a corporate reorganization has no effect on a single-name CDS, which continues to reference Meriden alone.
4. The result of Idowu's Ridgeway curve trade after three months is closest to: (LOS: los-06-05-d)
   - A. a gain of $471,000.
   - B. a gain of $1,239,000.
   - C. a loss of $471,000.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The CDS runs three years, so only the year 1 to 3 hazard rates are used; the year 4 and 5 rates are decoys.
> Loss given default $= 1 - 0.40 = 0.60$, and each year's default probability is the prior survival probability times the hazard rate.
> Year 1: $\text{POD} = 1.0000 \times 0.015 = 0.015000$, expected loss $= 0.60 \times 0.015000 \times 100 = 0.9000$, discounted at $1/1.03 = 0.970874$ gives $0.8738$.
> Year 2: survival to the start of the year $= 0.985000$, $\text{POD} = 0.985000 \times 0.022 = 0.021670$, expected loss $= 1.3002$, discounted at $1/1.03^2 = 0.942596$ gives $1.2256$.
> Year 3: survival $= 0.985 \times 0.978 = 0.963330$, $\text{POD} = 0.963330 \times 0.028 = 0.026973$, expected loss $= 1.6184$, discounted at $1/1.03^3 = 0.915142$ gives $1.4811$.
> PV of the protection leg $= 0.8738 + 1.2256 + 1.4811 = 3.5804$, about 3.58 per 100.
> B is wrong because it treats each hazard rate as the unconditional default probability, skipping the survival weighting: $0.60 \times 100 \times (0.015/1.03 + 0.022/1.03^2 + 0.028/1.03^3) = 3.6555$.
> C is wrong because it omits discounting: $0.9000 + 1.3002 + 1.6184 = 3.8186$.
> 2. **A.** The premium leg pays the 1% investment-grade coupon (1.00 per 100) at each year-end only if Quillon has survived that year.
> Survival probabilities are $0.985000$, $0.963330$, and $0.936357$ at the ends of years 1, 2, and 3.
> PV of the premium leg $= 1.00 \times (0.985000 \times 0.970874 + 0.963330 \times 0.942596 + 0.936357 \times 0.915142) = 0.9563 + 0.9080 + 0.8569 = 2.7212$.
> Upfront payment $= \text{PV(protection leg)} - \text{PV(premium leg)} = 3.5804 - 2.7212 = 0.8592$, about 0.86% of notional.
> It is positive, so the protection buyer, Ashcombe, pays the seller, and the price is $100 - 0.86 = 99.14$.
> The sign is consistent with the spread shortcut: with hazard rates of 1.5% to 2.8% and 60% loss given default, the fair spread (roughly 0.9% to 1.7%) is mostly above the 1% coupon, so the buyer must top up the coupon.
> B is wrong because it values the premium leg as a risk-free annuity, ignoring that coupons are contingent on survival: $1.00 \times (0.970874 + 0.942596 + 0.915142) = 2.8286$, so $3.5804 - 2.8286 = 0.7518$ and a price of 99.25.
> C is wrong because it reverses the payer; a positive upfront is paid by the buyer, and the price is below 100, not above it.
> 3. **B.** A spinoff that leaves it unclear who is responsible for the referenced debt is a succession event, not a credit event.
> The regional Determinations Committee rules on succession events, and the CDS can be modified or split across the successor entities, here Meriden and Castell Generics.
> No bankruptcy, failure to pay, or restructuring has occurred, so there is no settlement and no payment to the protection buyer.
> A is wrong because a change of obligor through a corporate reorganization is not one of the credit events; Meriden has paid every obligation and has not filed for bankruptcy.
> C is wrong because succession events do affect the contract; the committee exists precisely to decide how the CDS follows the reorganized debt.
> 4. **A.** Rising near-term risk relative to long-term risk is a flattening view, so Idowu buys two-year protection (short near-term credit) and sells ten-year protection (long long-term credit), a flattener that is bearish in the short run.
> Two-year leg, protection bought: spread change $= 330 - 180 = 150$ bps, gain $= 0.0150 \times 1.9 \times 30{,}000{,}000 = 855{,}000$.
> Ten-year leg, protection sold: spread change $= 350 - 310 = 40$ bps, loss $= 0.0040 \times 8.0 \times 12{,}000{,}000 = 384{,}000$.
> Net result $= 855{,}000 - 384{,}000 = 471{,}000$, a gain of about 471,000 dollars.
> The five-year row of Exhibit 2 is a decoy; no position is held at that maturity.
> B is wrong because it treats the sold ten-year protection as also gaining when its spread widens: $855{,}000 + 384{,}000 = 1{,}239{,}000$; a protection seller is long credit and loses on widening.
> C is wrong because it reverses the legs (a steepener: buy ten-year and sell two-year protection), which loses $855{,}000 - 384{,}000 = 471{,}000$.

## Distractor design

1. B: hazard rates used as unconditional default probabilities (survival weighting skipped); C: expected losses not discounted.
2. B: premium leg valued as a risk-free annuity, ignoring that coupons are contingent on survival; C: upfront payer reversed, price placed above 100.
3. A: succession event confused with a credit event; C: reorganizations assumed to leave the CDS untouched, ignoring the Determinations Committee's succession ruling.
4. B: protection-seller leg given the buyer's sign, so the legs are added instead of netted; C: flattener legs swapped into a steepener.
