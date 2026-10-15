---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 1
title: "Kestrel Mobile Games: Capitalised Growth Under Review"
los: [los-05-01-d, los-05-01-e, los-05-01-f, los-05-01-h]
difficulty: 4
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Kestrel Mobile Games: Capitalised Growth Under Review

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Keiko Brandt, CFA, is a portfolio manager at Larchmont Capital, a long-only US equity fund.
She is reviewing Kestrel Mobile Games Inc., a listed publisher of free-to-play mobile games, which trades at USD 38.00 per share with 80 million shares outstanding.

Kestrel capitalises the cost of paid advertising used to acquire new players (user acquisition costs) and amortises it over the expected life of a player.
Its listed peers expense user acquisition costs as incurred.
Kestrel reports EBITDA with the amortisation of capitalised user acquisition costs added back, and its management reports "free cash flow to equity" that excludes capitalised user acquisition spending, which the cash flow statement classifies as investing.

Exhibit 1: Kestrel selected data, fiscal year 2025 (USD millions unless stated)

| Item | Value |
|---|---|
| Reported EBITDA | 520 |
| User acquisition costs capitalised during 2025 | 210 |
| Amortisation of capitalised user acquisition costs, 2025 | 150 |
| Total debt | 1,100 |
| Cash and equivalents | 180 |
| Management-reported free cash flow to equity | 300 |
| Dividends paid (USD 0.80 per share) | 64 |

Exhibit 2: Listed mobile game peers (all expense user acquisition costs)

| Measure | Median | Mean |
|---|---|---|
| EV/EBITDA | 11.5x | 12.8x |
| P/E | 19.0x | 21.4x |

Larchmont's policy is to measure leverage with total debt, to use peer median multiples, and to bridge from enterprise value to equity value with net debt.

Brandt first reviews Kestrel's bank covenant, which caps debt to EBITDA at 3.25x.
She wants to know how leverage looks when, as in the Livent case, amortisation of capitalised operating costs is not added back to EBITDA.

Brandt then reverse-engineers the market price.
She uses a constant-growth model, value per share $= \text{FCFE}_0 (1+g) / (r - g)$, with a required return on equity of 9.0%.
She defines FCFE so that all cash spent acquiring players is treated as an operating outflow, and she solves for the perpetual growth rate that equates model value with the market price.
Her own forecast of long-term FCFE growth is 4.5%, reflecting her view that the returns to current player acquisition will regress toward the industry average as competitors bid up advertising prices.

Next, Brandt estimates a relative value per share for Kestrel from the peer EV/EBITDA multiple, with Kestrel's EBITDA restated to the same accounting basis as its peers.

Finally, Brandt learns that Ridgeline Partners, a private equity sponsor, has approached Kestrel's board about acquiring 100% of the company, refinancing its debt, and suspending the dividend to fund expansion.
Kestrel's chief financial officer, Victor Hale, tells Brandt that any bid should be judged with a dividend discount model.
"We have paid a quarterly dividend for nine consecutive years at a stable payout ratio," he says.
"That record is long, public and reliable, so the inputs could not be better."
Brandt replies that the dividend record is indeed reliable, but that it does not answer the question Ridgeline will be asking.

## Questions

1. Kestrel's 2025 debt to EBITDA, measured under Larchmont's policy with amortisation of capitalised user acquisition costs not added back, is closest to: (LOS: los-05-01-e)
   - A. 2.49x.
   - B. 2.97x.
   - C. 3.55x.
2. The perpetual FCFE growth rate implied by Kestrel's market price and the conclusion it supports, given Brandt's 4.5% forecast, are closest to: (LOS: los-05-01-d)
   - A. 3.87%; the shares are undervalued.
   - B. 6.04%; the shares are overvalued.
   - C. 5.87%; the shares are overvalued.
3. Brandt's relative value per share for Kestrel and the most accurate interpretation of it are: (LOS: los-05-01-f)
   - A. USD 33.06; Kestrel is relatively overvalued, which does not by itself establish that the shares trade above intrinsic value.
   - B. USD 41.69; Kestrel is relatively undervalued, which does not by itself establish that the shares trade below intrinsic value.
   - C. USD 38.10; Kestrel is fairly valued relative to its peers.
4. For valuing Kestrel from Ridgeline's standpoint, the most appropriate model and the criterion that most directly argues against Hale's proposal are: (LOS: los-05-01-h)
   - A. a dividend discount model, because the dividend record satisfies the data availability and quality criterion.
   - B. a free cash flow model, because of the criterion of consistency with the purpose of the valuation and the valuer's perspective.
   - C. a free cash flow model, because of the criterion of appropriateness given the availability and quality of data.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Without the add-back, EBITDA $= 520 - 150 = 370$, and total debt to EBITDA $= 1{,}100 / 370 = 2.9730$x.
> Reported debt to EBITDA is $1{,}100 / 520 = 2.1154$x, so the add-back understates leverage by about 0.86 turns, and the true ratio is much closer to the 3.25x covenant than Kestrel's reported figure suggests.
> The amortisation of a capitalised operating cost is not a true non-cash charge, because the cash has already been spent, which is the Exhibit 3 warning sign of deferring expenses by capitalising them.
> A is wrong because it uses net debt instead of total debt, against Larchmont's policy ($(1{,}100 - 180) / 370 = 920 / 370 = 2.4865$x).
> C is wrong because it subtracts the amount capitalised during the year instead of the amortisation that the stated convention removes ($1{,}100 / (520 - 210) = 1{,}100 / 310 = 3.5484$x); 310 is the peer-comparable EBITDA needed in Question 3, not the Livent measure.
> 2. **C.** Brandt's FCFE treats all user acquisition cash as an operating outflow, so $\text{FCFE}_0 = (300 - 210) / 80 = 90 / 80 = 1.1250$ per share.
> Setting $P = \text{FCFE}_0 (1+g) / (r-g)$ and solving gives $g = (P r - \text{FCFE}_0) / (P + \text{FCFE}_0)$.
> $g = (38.00 \times 0.09 - 1.1250) / (38.00 + 1.1250) = (3.4200 - 1.1250) / 39.1250 = 2.2950 / 39.1250 = 0.0587$, or 5.87%.
> Check with the unrounded $g = 0.058658$: $1.1250 \times 1.058658 / (0.09 - 0.058658) = 1.190990 / 0.031342 = 38.00$.
> The price requires 5.87% perpetual growth, above the 4.5% Brandt considers achievable, so the market's expectations are too optimistic and the shares are overvalued; this is inferring market expectations.
> A is wrong because it deducts the amortisation (150) rather than the cash spent (210), giving $\text{FCFE}_0 = 150 / 80 = 1.8750$ and $g = (3.4200 - 1.8750) / 39.8750 = 0.0387$, which is below 4.5% and reverses the conclusion.
> B is wrong because it treats $\text{FCFE}_0$ as next year's FCFE, $g = r - \text{FCFE}_0 / P = 0.09 - 1.1250 / 38.00 = 0.09 - 0.0296 = 0.0604$; the conclusion happens to be the same, but the growth rate is misstated.
> Using management's unadjusted FCFE ($300 / 80 = 3.7500$) would imply $g = (3.4200 - 3.7500) / 41.7500 = -0.79\%$, an apparently deep undervaluation created entirely by the accounting choice.
> 3. **A.** Peers expense user acquisition costs as incurred, so the comparable EBITDA deducts the full cash spent: $520 - 210 = 310$.
> Enterprise value $= 11.5 \times 310 = 3{,}565.0$; equity $= 3{,}565.0 - (1{,}100 - 180) = 3{,}565.0 - 920 = 2{,}645.0$; per share $= 2{,}645.0 / 80 = 33.0625$.
> The price of 38.00 is $38.00 / 33.0625 - 1 = 14.93\%$ above the relative value, so Kestrel is relatively overvalued against peers.
> The method of comparables establishes intrinsic value only if the peer group is itself fairly valued, so the result is a relative verdict, not an absolute one.
> B is wrong because it applies the multiple to the Livent-convention EBITDA from Question 1, which still excludes the capitalised spend in excess of amortisation and is not on the peers' basis ($(11.5 \times 370 - 920) / 80 = 3{,}335.0 / 80 = 41.6875$).
> C is wrong because it uses the peer mean multiple against Larchmont's policy ($(12.8 \times 310 - 920) / 80 = 3{,}048.0 / 80 = 38.10$); the near match with the price is a coincidence of the wrong multiple, since Kestrel's market EV/EBITDA on the comparable basis is $3{,}960 / 310 = 12.77$x.
> 4. **B.** Ridgeline would own 100% of Kestrel and would set its financing and payout policy itself, and it intends to suspend the dividend.
> A controlling buyer can redirect free cash flow, so free cash flow is the model consistent with Ridgeline's purpose and perspective, and the dividends a minority holder receives are not what a controlling owner values.
> A is wrong because satisfying the data criterion does not make a model appropriate when the purpose and perspective of the valuation point elsewhere; Hale answers a data question when the issue is whose cash flows are being valued.
> C is wrong because Brandt concedes that the dividend record is long, public and reliable, so data availability and quality do not argue against the dividend discount model here.

## Distractor design

1. A: net debt used although policy specifies total debt (misread policy); C: amount capitalised subtracted instead of amortisation (wrong adjustment variant, borrowed from the peer-comparable basis).
2. A: amortisation deducted instead of cash spent (accrual versus cash); B: $\text{FCFE}_0$ used as $\text{FCFE}_1$ (period error).
3. B: Livent-convention EBITDA carried from Question 1 instead of the peer-comparable basis (wrong accounting basis); C: peer mean used instead of median (misread exhibit and policy).
4. A: data criterion accepted as sufficient (criterion misapplied); C: correct model with the criterion that the vignette explicitly rules out (wrong criterion).
