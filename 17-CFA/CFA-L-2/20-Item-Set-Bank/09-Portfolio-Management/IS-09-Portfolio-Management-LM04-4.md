---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Etxeberria Account: Bond Fund Styles and Factor Hedges"
los: [los-09-04-c, los-09-04-e, los-09-04-f]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Etxeberria Account: Bond Fund Styles and Factor Hedges

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Marisol Etxeberria, 46, is a senior engineer at a manufacturer of mining and construction equipment.
About 40% of her annual compensation is a bonus tied to company sales, and her employer has cut staff in each of the last two recessions.
Her private wealth advisor, Graham Yeo, CFA, is restructuring her $4.0 million investment account.

Etxeberria wants to add a bond fund and has asked Yeo about the Calloway Short-Duration Core Fund, which its sponsor markets as a short-duration, investment-grade fund.
Yeo runs a returns-based style analysis in which the fund's returns are regressed on six fixed-income sector returns, with the style weights constrained to sum to 100%.
He then applies his firm's forward-looking expected sector returns to the estimated style weights.

**Exhibit 1: Calloway Short-Duration Core Fund, style weights and sector returns**

| Sector | Style weight | Expected return, next year | Trailing 12-month return |
|---|---|---|---|
| Government, short | 15% | 2.10% | 1.20% |
| Government, intermediate | 10% | 3.00% | -0.40% |
| Government, long | 25% | 3.90% | -3.10% |
| Investment-grade credit | 30% | 4.60% | 1.50% |
| MBS and securitized | 8% | 4.10% | 0.60% |
| High yield | 12% | 6.80% | 7.90% |

The fund's stated average duration is 2.4 years, and its expense ratio is 0.35%.

Etxeberria's account also holds $1.5 million of cyclical equities, mostly industrial and materials stocks, which Yeo estimates have a combined sensitivity of 1.40 to a business cycle factor.
Yeo's firm uses a five-factor macroeconomic model and publishes factor portfolios that can be bought or sold short.

**Exhibit 2: Factor portfolios, sensitivities to the five macroeconomic factors**

| Portfolio | Confidence risk | Time horizon risk | Inflation risk | Business cycle risk | Market timing risk |
|---|---|---|---|---|---|
| K | 0.00 | 0.00 | 0.00 | 1.00 | 0.00 |
| L | 0.30 | 0.00 | 0.00 | 1.00 | 0.50 |
| M | 0.00 | 1.00 | 0.00 | 0.00 | 0.00 |

Etxeberria does not want to sell the cyclical equities before the end of the tax year, but she wants their business cycle exposure neutralized without adding exposure to any other factor.

In a planning note, Yeo's junior associate writes that Etxeberria "should follow the standard CAPM prescription and hold the market portfolio combined with cash, because her job has no bearing on which risks she should bear in her portfolio."
Yeo disagrees and asks the associate to reconsider in light of the multifactor models used by the firm.

## Questions

1. The expected return on the Calloway fund implied by its style weights and the firm's sector forecasts, before expenses, is closest to: (LOS: los-09-04-c)
   - A. 0.81%.
   - B. 3.75%.
   - C. 4.11%.
2. Are the fund's style weights consistent with its short-duration, investment-grade mandate? (LOS: los-09-04-e)
   - A. Yes, because 88% of the style weight is in government, investment-grade credit, and securitized sectors.
   - B. No, because the fund has 12% high-yield exposure and as much weight in long government bonds as in short and intermediate government bonds combined.
   - C. No on credit quality, because of the high-yield exposure, but yes on duration, because government sectors make up 50% of the style weights.
3. Considering multiple risk dimensions, the most appropriate advice for Etxeberria's strategic factor exposures is to: (LOS: los-09-04-f)
   - A. tilt toward business-cycle-sensitive assets, because she earns the business cycle premium on them.
   - B. tilt away from business-cycle-sensitive assets, accepting a lower expected return, because her employment income already exposes her to recession risk.
   - C. hold the market portfolio and cash in proportions set by her risk tolerance, as the associate recommends.
4. To neutralize the business cycle exposure of her cyclical equities as she requests, Yeo should: (LOS: los-09-04-e)
   - A. sell short $1.5 million of Portfolio K.
   - B. sell short $2.1 million of Portfolio K.
   - C. sell short $2.1 million of Portfolio L.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** The portfolio expected return is the style-weight-weighted average of the forward-looking sector returns.
> $0.15(2.10) + 0.10(3.00) + 0.25(3.90) + 0.30(4.60) + 0.08(4.10) + 0.12(6.80)$.
> $= 0.3150 + 0.3000 + 0.9750 + 1.3800 + 0.3280 + 0.8160 = 4.1140\%$.
> A is wrong because it applies the style weights to the trailing 12-month returns instead of the expected returns: $0.8110\%$.
> B is wrong because it drops the high-yield sector as inconsistent with the mandate and rescales the rest: $(4.1140 - 0.8160)/0.88 = 3.7477\%$; the style weights describe the exposures the fund actually has.
> 2. **B.** Style analysis catches mandate violations from the factor loadings alone.
> The 12% high-yield weight is below-investment-grade exposure that a true investment-grade fund would not have.
> Long government bonds carry 25% of the weight against $15\% + 10\% = 25\%$ in short and intermediate government combined, a tilt toward long-duration returns that contradicts a short-duration mandate and the stated 2.4-year duration.
> A is wrong because it treats a mostly investment-grade profile as compliant while ignoring both the high-yield weight and the duration tilt.
> C is wrong because a large government weight says nothing about short duration; the government exposure here is tilted to the long end.
> 3. **B.** Multifactor thinking asks which priced risks an investor bears at a comparative advantage or disadvantage relative to the average investor.
> Etxeberria's bonus and job security fall in recessions, so her human capital is already heavily exposed to business cycle risk, and she should demand more than the average premium to add more; tilting away from procyclical assets is appropriate even though it lowers expected return.
> A is wrong because the premium exists precisely because investors like her are hurt in recessions; the tilt suits an investor with no procyclical income, not her.
> C is wrong because it is the CAPM two-fund answer, which ignores the other priced risks that differ across investors.
> 4. **B.** The dollar factor exposure to neutralize is $\$1{,}500{,}000 \times 1.40 = \$2{,}100{,}000$.
> Portfolio K is the pure business cycle factor portfolio (sensitivity 1.00 to business cycle, 0.00 to all other factors), so shorting $2.1 million of K offsets the exposure without adding any other factor bet.
> A is wrong because it matches dollar amounts rather than factor exposures, leaving $\$1.5$ million $\times (1.40 - 1.00) = \$0.6$ million of business cycle exposure.
> C is wrong because Portfolio L also loads 0.30 on confidence risk and 0.50 on market timing risk, so shorting it would add unwanted exposures of $-0.63$ million and $-1.05$ million to those factors.

## Distractor design

- Q1: A = trailing returns used instead of expected returns (misread exhibit); B = inconsistent sector dropped and weights rescaled.
- Q2: A = mostly investment-grade profile read as full compliance; C = government weight confused with short duration.
- Q3: A = factor premium pursued without regard to comparative disadvantage; C = CAPM two-fund prescription.
- Q4: A = dollar amount matched instead of factor exposure; C = portfolio with the right target loading but non-zero loadings on other factors.
