---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 2
title: "Harrowgate Shipping: A Compliance Review of an Irregular Dividend Model"
los: [los-05-02-b, los-05-02-i, los-05-02-o]
difficulty: 4
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Harrowgate Shipping: A Compliance Review of an Irregular Dividend Model

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Oliver Brandt is an equity analyst at Ellery & Marsh, a London private bank.
He has drafted a client memo on Harrowgate Shipping Holdings plc, a listed dry-bulk shipping company, for Dr. Anika Rao, a client who is considering buying the shares and holding them for one year.
Before any memo reaches a client, it is reviewed by Sarah Kwame, CFA, the bank's supervisory analyst, who checks that the methods and conclusions are supportable.

Harrowgate has agreed to sell six of its oldest vessels.
The board has announced that the proceeds will fund a one-off special dividend of GBP 4.00 per share in year 3, in addition to the regular dividend, and that the regular payout ratio will be reduced once the smaller fleet is operating.
Brandt builds a pro forma forecast of earnings and payout for the next four years.

Exhibit 1: Harrowgate pro forma forecast (per share, GBP)

| | Year 1 | Year 2 | Year 3 | Year 4 |
|---|---|---|---|---|
| Earnings per share | 3.20 | 3.40 | 2.60 | 2.80 |
| Regular payout ratio | 50% | 50% | 45% | 50% |
| Special dividend | 0.00 | 0.00 | 4.00 | 0.00 |
| Book value per share, end of year | 24.10 | 25.80 | 23.23 | 24.63 |

After year 4, Brandt expects the fleet to be renewed at a steady pace and dividends to grow at 3% a year indefinitely.
He estimates Harrowgate's required return at 10.0% from the CAPM, using a risk-free rate of 3.5%, a beta of 1.30 and an equity risk premium of 5.0%.
Harrowgate's shares trade at GBP 21.40, and the median trailing P/E of listed dry-bulk peers is 9.0.
Brandt's one-year target price, based on his model, is GBP 22.35.

Brandt's memo, dated 9 September 2026, includes two statements about his method.

Statement 1: "Because Harrowgate's dividends include a one-off special dividend followed by a cut in the regular payout, I forecast each dividend individually in a spreadsheet and apply the Gordon growth model only from year 5 onward."

Statement 2: "I also solved my model for the discount rate that equates the forecast dividends with today's GBP 21.40 price, and I recommend using that internal rate of return as the required return when valuing Harrowgate in the same model."

Kwame's review note, dated 10 September 2026, adds a comment of her own.

Kwame: "A spreadsheet model of this kind removes the need for a required return estimate, because every dividend in the explicit horizon is forecast directly."

Kwame asks Brandt to confirm three figures before the memo is released: the return Dr. Rao can expect over her one-year horizon if his target price is reached, the intrinsic value of the shares at his 10.0% required return, and the expected return implied by the current market price.

## Questions

1. If Brandt's target price is reached, Dr. Rao's expected one-year holding period return is closest to: (LOS: los-05-02-b)
   - A. 4.44%.
   - B. 11.41%.
   - C. 11.92%.
2. Using Brandt's forecasts and a required return of 10.0%, the intrinsic value of a Harrowgate share today is closest to: (LOS: los-05-02-b)
   - A. GBP 20.49.
   - B. GBP 21.36.
   - C. GBP 21.77.
3. Which of the following is most accurate? (LOS: los-05-02-o)
   - A. Brandt's Statement 1.
   - B. Brandt's Statement 2.
   - C. Kwame's comment.
4. The expected return on Harrowgate implied by its current market price and Brandt's dividend forecasts is closest to: (LOS: los-05-02-i)
   - A. 9.67%.
   - B. 10.14%.
   - C. 10.48%.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** $D_1 = 0.50 \times 3.20 = 1.60$.
> Holding period return $= (D_1 + P_1)/P_0 - 1 = (1.60 + 22.35)/21.40 - 1 = 23.95/21.40 - 1 = 0.11916$, or 11.92%.
> The target price is Brandt's own model value at $t = 1$, $1.70/1.10 + 5.17/1.10^2 + (1.40 + 20.60)/1.10^3 = 22.3471$, so the 1.92% above the 10.0% required return is the correction of the undervaluation found in Question 2.
> A is wrong because it counts only the price appreciation, $(22.35 - 21.40)/21.40 = 4.44\%$, and omits the dividend yield of 7.48%.
> B is wrong because it divides the total gain by the ending price, $(1.60 + 22.35 - 21.40)/22.35 = 2.55/22.35 = 11.41\%$, rather than by the purchase price.
> 2. **C.** Dividends: $D_1 = 1.60$, $D_2 = 0.50 \times 3.40 = 1.70$, $D_3 = 0.45 \times 2.60 + 4.00 = 5.17$, $D_4 = 0.50 \times 2.80 = 1.40$.
> PVs at 10%: $1.4545 + 1.4050 + 3.8843 + 0.9562 = 7.7000$.
> Terminal value at $t = 4$: $D_5 = 1.40 \times 1.03 = 1.442$; $V_4 = 1.442/(0.10 - 0.03) = 20.60$; PV $= 20.60/1.4641 = 14.0701$.
> $V_0 = 7.7000 + 14.0701 = 21.7701$, or GBP 21.77, above the 21.40 price.
> Calculator: C01 = 1.60, C02 = 1.70, C03 = 5.17, C04 = 1.40 + 20.60 = 22.00, I = 10, NPV = 21.77.
> A is wrong because it discounts $V_4$ five periods ($20.60/1.6105 = 12.7910$, total 20.49).
> B is wrong because it builds the terminal value from $D_4$ instead of $D_5$ ($1.40/0.07 = 20.00$, PV 13.6603, total 21.36).
> 3. **A.** When dividends follow no stylized pattern (here a special dividend in year 3 and a payout change), a spreadsheet lets the analyst forecast each dividend individually and apply a Gordon (or multiple-based) terminal value only once growth becomes stable, which is exactly Brandt's method.
> B is wrong because reusing the price-implied IRR as the discount rate in the same model is circular: it reproduces the market price by construction and cannot reveal mispricing.
> C is wrong because a spreadsheet model still discounts every forecast dividend and the terminal value at a required return; forecasting dividends explicitly does not remove the need for $r$.
> 4. **B.** Solve $21.40 = \sum_{t=1}^{4} D_t/(1+r)^t + D_5/[(r - 0.03)(1+r)^4]$ for $r$ by trial.
> At 10.0% the value is 21.7701, above price, so the IRR is higher; at 10.5% it is 20.5071, below price.
> At 10.14% the value is 21.3991, which matches the 21.40 price (bisection gives 0.10140).
> Because the price is below the 10.0% model value, the implied return exceeds the 10.0% required return, consistent with an undervaluation call.
> A is wrong because it solves the model with the terminal value discounted five periods, which gives an IRR of 9.67%.
> C is wrong because it is the Gordon shortcut at the long-run rate, $1.60/21.40 + 0.03 = 0.0748 + 0.03 = 10.48\%$, which ignores the irregular dividends in years 1 to 4.

## Distractor design

1. A: dividend yield omitted from the holding period return; B: return measured on ending price instead of purchase price.
2. A: terminal value discounted $n + 1$ periods; B: terminal value built from $D_n$ instead of $D_{n+1}$.
3. B: circular use of the price-implied IRR as the discount rate; C: explicit forecasting confused with eliminating the required return.
4. A: IRR solved with the terminal value discounted one period too many; C: Gordon approximation $D_1/P_0 + g_L$ used for an irregular stream.
