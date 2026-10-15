---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 6
title: "Harrow Ventures: A Series B Round and a Software Buyout"
los: [los-05-06-a, los-05-06-c, los-05-06-f, los-05-06-g, los-05-06-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Harrow Ventures: A Series B Round and a Software Buyout

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Naledi Mokoena, CFA, is a senior associate at Harrow Ventures, a US growth equity fund.
She is preparing two investment memos.

The first concerns Quillon Diagnostics Inc., a private developer of a rapid blood-screening device.
Quillon's two founders own 55% of the shares and run the company; its Series A investors own the rest.
Quillon has no revenue and is seeking a Series B investment from Harrow.
Mokoena models Quillon's value as a decision tree.

Exhibit 1: Quillon scenario assumptions

| Stage | Outcome | Probability | First-year FCFF, received at t = 3 (USD millions) | Perpetual growth |
|---|---|---|---|---|
| Regulatory clearance at t = 1 | Cleared | 70% | | |
| | Not cleared (value zero) | 30% | | |
| Commercial outcome at t = 2, if cleared | Wide adoption | 50% | 60.0 | 4% |
| | Niche adoption | 30% | 18.0 | 1% |
| | Failure (value zero) | 20% | | |

Mokoena discounts at a WACC of 18%.

Harrow expects Quillon to be sold or listed in about two years, so Mokoena estimates a DLOM for the Series B shares from puts on Voltra Medical, the closest listed comparable.
Voltra trades at USD 42.00 and pays no dividends, and the risk-free rate is 4.5%.

Exhibit 2: Two-year European puts on Voltra Medical

| Strike (USD) | Put premium (USD) |
|---|---|
| 42.00 | 7.25 |
| 46.00 | 9.38 |
| 50.00 | 11.72 |

A Harrow junior analyst, Theo Lindqvist, comments: "As a private company, Quillon has to be worth less than a listed peer with the same technology, because every feature that separates a private company from a public one reduces value."
He also suggests that Harrow value Quillon with the asset-based approach, because "we can see exactly what the lab equipment and patents cost."

The second memo concerns Tessaly Software Ltd., a profitable, stable developer of scheduling software for dental practices.
Harrow could acquire 100% of Tessaly from its founder, Mira Tessaly, who draws no salary and instead pays herself a dividend of USD 0.40 million a year.
A market-rate salary for her role would be USD 0.25 million.
Tessaly's reported net income, which contains no interest expense, is USD 1.5375 million, and its tax rate is 25%.
Most of Tessaly's value comes from its software and customer relationships, and Mokoena values it with the excess earnings method.

Exhibit 3: Tessaly excess earnings inputs

| Input | Value |
|---|---|
| Working capital at fair value | USD 1.5 million |
| Fixed assets at fair value | USD 4.0 million |
| Required return on working capital | 5% |
| Required return on fixed assets | 9% |
| Required return on intangible assets | 16% |
| Growth rate of residual income | 4% |

## Questions

1. Quillon's value today based on Mokoena's decision tree is closest to: (LOS: los-05-06-h)
   - A. USD 123.7 million.
   - B. USD 128.2 million.
   - C. USD 176.7 million.
2. The DLOM for Harrow's Series B shares, based on Exhibit 2, is closest to: (LOS: los-05-06-f)
   - A. 17.3%.
   - B. 20.4%.
   - C. 22.3%.
3. Lindqvist's comment about Quillon's private status is best described as: (LOS: los-05-06-a)
   - A. correct, because company-specific and stock-specific factors both reduce private company values.
   - B. incorrect, because stock-specific factors such as illiquidity generally increase private company values.
   - C. incorrect, because company-specific factors such as owner-manager overlap and growth potential can increase value.
4. Lindqvist's suggestion to value Quillon with the asset-based approach is: (LOS: los-05-06-g)
   - A. inappropriate, because Quillon's value lies in the probability-weighted cash flows of a going concern, not in the cost of its assets.
   - B. appropriate, because early-stage companies without revenue can only be valued from their balance sheets.
   - C. appropriate, because the asset-based approach is the preferred method for companies expected to be sold.
5. Tessaly's normalized earnings are closest to: (LOS: los-05-06-c)
   - A. USD 1.2875 million.
   - B. USD 1.3500 million.
   - C. USD 1.5375 million.
6. Using normalized earnings, Tessaly's firm value using the excess earnings method is closest to: (LOS: los-05-06-h)
   - A. USD 7.93 million.
   - B. USD 13.13 million.
   - C. USD 13.43 million.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** The first-year cash flows are already the t = 3 amounts, so each scenario value at t = 2 is a growing perpetuity without further growth.
> Wide: $60.0 / (0.18 - 0.04) = 428.5714$; niche: $18.0 / (0.18 - 0.01) = 105.8824$.
> Path probabilities: $0.70 \times 0.50 = 0.35$ and $0.70 \times 0.30 = 0.21$.
> Expected value at t = 2: $0.35 \times 428.5714 + 0.21 \times 105.8824 = 150.0000 + 22.2353 = 172.2353$.
> $V_0 = 172.2353 / 1.18^2 = 172.2353 / 1.3924 = 123.6967$ million.
> B is wrong because it grows the t = 3 cash flows one more year ($62.4/0.14$ and $18.18/0.17$), giving $128.1655$.
> C is wrong because it uses the conditional commercial probabilities without multiplying by the 70% clearance probability ($(0.50 \times 428.5714 + 0.30 \times 105.8824)/1.3924 = 176.7096$).
> 2. **C.** The two-year forward price is $42.00 \times e^{0.045 \times 2} = 45.9553$, so the USD 46.00 strike is the at-the-money-forward put.
> $DLOM = 9.38 / 42.00 = 0.2233$, or 22.3%.
> A is wrong because it uses the put struck at the spot price ($7.25 / 42.00 = 0.1726$) instead of the forward price.
> B is wrong because it divides the correct premium by the strike instead of the current stock price ($9.38 / 46.00 = 0.2039$).
> 3. **C.** Stock-specific factors (illiquidity, concentrated control, restrictions on sale) are generally negative for value, but company-specific factors can cut either way.
> Founders who own and manage the company face few agency problems, can take a long-term view, and an early-stage firm may have more growth potential than a public peer.
> A is wrong because it treats company-specific factors as uniformly negative.
> B is wrong because illiquidity reduces value.
> 4. **A.** Quillon is an early-stage going concern whose value depends on uncertain future cash flows, which is why scenario analysis under the income approach fits.
> The asset-based approach suits holding companies and liquidations and ignores the value of growth and development success.
> B is wrong because early-stage firms are routinely valued with scenario-weighted cash flows and financing-round prices, not only balance sheets.
> C is wrong because an expected sale raises the relevance of income and market approaches, not asset-based values.
> 5. **B.** Reported earnings omit any compensation expense, so a market-rate salary must be inserted, and the dividend is a distribution that needs no adjustment.
> After-tax cost of the salary: $0.25 \times (1 - 0.25) = 0.1875$; normalized earnings $= 1.5375 - 0.1875 = 1.3500$ million.
> A is wrong because it deducts the salary without the tax effect ($1.5375 - 0.25 = 1.2875$).
> C is wrong because it treats the USD 0.40 million dividend as a substitute for compensation and makes no adjustment.
> 6. **C.** Required returns: $1.5 \times 0.05 = 0.0750$ and $4.0 \times 0.09 = 0.3600$.
> Residual income $= 1.3500 - 0.0750 - 0.3600 = 0.9150$ million.
> Residual value $= 0.9150 \times 1.04 / (0.16 - 0.04) = 0.9516 / 0.12 = 7.9300$ million.
> Firm value $= 1.5 + 4.0 + 7.93 = 13.43$ million.
> A is wrong because it reports only the value of the intangibles and omits the working capital and fixed assets.
> B is wrong because it capitalizes the current residual income without growing it one year ($1.5 + 4.0 + 0.9150 / 0.12 = 13.125$).

## Distractor design

1. B: next-year cash flow grown again (period error); C: conditional probabilities used as path probabilities (probabilities not multiplied along the tree).
2. A: put struck at spot instead of the forward (spot versus forward); B: premium divided by the strike instead of the spot (wrong denominator).
3. A: company-specific factors assumed uniformly negative; B: direction of the illiquidity effect reversed.
4. B: overgeneralized limitation of early-stage valuation; C: approach selection tied to the wrong trigger.
5. A: compensation adjustment not tax-effected (before-tax versus after-tax); C: dividend treated as a substitute for compensation (distribution versus expense).
6. A: tangible asset values omitted (residual value reported as firm value); B: residual income not grown one year (period error).
