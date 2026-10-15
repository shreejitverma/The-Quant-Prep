---
type: cfa-itemset
topic: "Corporate Issuers"
topic_code: "04"
topic_slug: "04-Corporate-Issuers"
lm: 3
title: "Northmere Pension Equity Risk Premium Review"
los: [los-04-03-c, los-04-03-d, los-04-03-e]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/corporate-issuers]
---

# Northmere Pension Equity Risk Premium Review

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

Helena Voss is chief investment officer of the Northmere Public Employees Pension Plan (Northmere), a US dollar-based defined benefit plan with a 30-year liability horizon.
Northmere's investment policy statement (IPS) was amended this year and now contains two compliance clauses on capital market assumptions.

Clause 7.2: "Any historical equity risk premium used by the plan shall be the geometric mean excess return of the domestic equity index over long-term government bonds."

Clause 7.3: "Long-horizon required returns shall be anchored on the 10-year government bond yield, not on money market rates."

Before the annual asset allocation review, Voss asks the plan's consultant, Marcus Adeyemi, CFA, to produce forward-looking equity risk premium (ERP) estimates and to check the plan's historical estimate against the IPS.
The government yield curve is currently inverted.

**Exhibit 1: Market and forecast data**

| Item | Value |
|---|---|
| 10-year nominal government bond yield | 4.35% |
| 10-year inflation-linked government bond yield | 1.80% |
| 3-month government bill yield | 5.10% |
| Current 12-month CPI inflation | 3.80% |
| Index forward dividend yield | 2.10% |
| Index trailing dividend yield | 2.00% |
| Consensus nominal earnings growth of index companies | 6.00% per year |
| Forecast real GDP growth | 2.30% per year |
| Expected change in the market P/E | -0.40% per year |
| Expected net share repurchases, % of shares outstanding | 1.20% per year |

Adeyemi derives expected inflation from government bond yields using the exact ratio form, and he uses the 10-year nominal yield as the expected risk-free return.
He also computes a constant growth DDM estimate of the ERP from the forward dividend yield and the consensus earnings growth forecast.

**Exhibit 2: Mean annual domestic returns over 40 years**

| Series | Arithmetic mean | Geometric mean |
|---|---|---|
| Domestic equity index | 10.8% | 9.4% |
| 3-month government bills | 3.9% | 3.8% |
| Long-term government bonds | 5.9% | 5.5% |

At the review meeting, trustee Graham Pike argues that Northmere should use "the rate we can actually earn today", which he defines as the current 3-month bill yield plus the geometric mean excess return of equities over bills from Exhibit 2.

Northmere also plans a direct allocation to Country Z, an emerging market.
Adeyemi must estimate the cost of equity for Kovar Telecom (Kovar), a Country Z company whose shares are also listed in New York.
Northmere's methodology uses the 10-year US government yield as the risk-free rate, a developed-market ERP of 4.00%, and a beta measured against the developed-market index.
It then adds a country risk premium equal to the sovereign yield spread scaled by the ratio of Country Z equity-market volatility to bond-market volatility, weighted by the company's revenue exposure to Country Z.

**Exhibit 3: Country Z and Kovar data**

| Item | Value |
|---|---|
| Country Z 10-year government US dollar bond yield | 7.90% |
| Annualized volatility, Country Z equity index | 27% |
| Annualized volatility, Country Z government bond index | 15% |
| Kovar beta against the developed-market index | 1.10 |
| Kovar beta against a global all-country index | 0.35 |
| Share of Kovar revenue from Country Z | 70% |

On 9 October, Adeyemi emails Voss: "If we switched Kovar to a single-factor global CAPM, its beta of only 0.35 would give a much lower required return, and that would correctly reflect the diversification benefit Kovar offers a world investor."

## Questions

1. Adeyemi's Grinold-Kroner estimate of the ERP is closest to: (LOS: los-04-03-c)
   - A. 2.60%
   - B. 3.35%
   - C. 4.15%
2. Compared with the Grinold-Kroner estimate from the same exhibit, Adeyemi's constant growth DDM estimate of the ERP is best described as: (LOS: los-04-03-c)
   - A. about 0.40 percentage points higher, mainly because the DDM assumes a constant P/E.
   - B. about 0.40 percentage points higher, mainly because the DDM counts net share repurchases twice.
   - C. about 1.20 percentage points lower, mainly because the DDM omits net share repurchases.
3. The historical ERP that complies with Clause 7.2 is closest to: (LOS: los-04-03-c)
   - A. 3.9%
   - B. 4.9%
   - C. 5.6%
4. Relative to the long-horizon required return on an average-risk domestic stock that complies with both Clause 7.2 and Clause 7.3, Pike's proposed required return is: (LOS: los-04-03-c)
   - A. higher by 0.75 percentage points.
   - B. higher by 1.70 percentage points.
   - C. higher by 2.45 percentage points.
5. Using Northmere's methodology, Kovar's required return on equity is closest to: (LOS: los-04-03-e)
   - A. 11.24%
   - B. 13.22%
   - C. 15.14%
6. Adeyemi's 9 October statement is best described as: (LOS: los-04-03-d)
   - A. correct, because a global beta captures the risk a world-diversified investor actually bears.
   - B. incorrect, because the low correlation of Country Z returns with world markets depresses the global beta and understates Kovar's risk, which motivates a two-factor international CAPM with a currency factor.
   - C. incorrect, because the global CAPM overstates required returns for emerging market stocks by double counting currency risk.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Expected inflation from the ratio form: $i = 1.0435/1.0180 - 1 = 0.025049$, or 2.5049%.
> Net repurchases of 1.20% mean $\Delta S = -1.20\%$, so $-\Delta S = +1.20$.
> $\text{ERP} = \{2.10 + (-0.40) + [2.5049 + 2.30 + 1.20]\} - 4.35 = 7.7049 - 4.35 = 3.3549\%$, or about 3.35%.
> Real GDP growth is the correct $g$; the 6.00% consensus is nominal and would double count inflation, and current CPI of 3.80% is not a long-horizon inflation expectation.
> A (2.60%) is wrong because it subtracts the 5.10% bill yield instead of the 10-year yield: $7.7049 - 5.10 = 2.6049\%$.
> C (4.15%) is wrong because it adds the expected P/E contraction instead of subtracting it: $2.10 + 0.40 + 6.0049 - 4.35 = 4.1549\%$.
> 2. **A.** DDM ERP $= 2.10 + 6.00 - 4.35 = 3.75\%$, which exceeds the Grinold-Kroner 3.3549% by $0.3951$, about 0.40 points.
> The growth components nearly coincide: Grinold-Kroner EPS growth is $2.5049 + 2.30 + 1.20 = 6.0049\%$ against the 6.00% consensus.
> The gap is therefore almost entirely the $-0.40$ repricing term, which the constant growth DDM excludes because it assumes the P/E stays constant so that prices grow with earnings.
> B is wrong because the DDM counts repurchases once, not twice: they reach the estimate only through the consensus per-share earnings growth, and nothing in the dividend yield term repeats them.
> C is wrong on both direction and size: the DDM estimate is higher, and the consensus per-share growth already embeds the effect of repurchases.
> 3. **A.** Clause 7.2 requires the geometric mean over long-term government bonds: $9.4 - 5.5 = 3.9\%$.
> B (4.9%) is wrong because it uses arithmetic means over bonds: $10.8 - 5.9 = 4.9\%$.
> C (5.6%) is wrong because it uses the geometric mean over bills: $9.4 - 3.8 = 5.6\%$.
> 4. **C.** Compliant estimate: $4.35 + 3.9 = 8.25\%$.
> Pike's estimate: $5.10 + (9.4 - 3.8) = 5.10 + 5.6 = 10.70\%$.
> Difference $= 10.70 - 8.25 = 2.45$ percentage points.
> Both of Pike's choices push the estimate up: the bill-based premium is larger because the curve was normally upward sloping over the sample, and today's bill yield exceeds the 10-year yield because the curve is inverted.
> A (0.75) is wrong because it captures only the risk-free switch: $5.10 - 4.35 = 0.75$.
> B (1.70) is wrong because it captures only the premium switch: $5.6 - 3.9 = 1.70$.
> 5. **B.** Sovereign yield spread $= 7.90 - 4.35 = 3.55\%$.
> Volatility-adjusted CRP $= 3.55 \times 27/15 = 6.39\%$.
> Exposure-weighted CRP $= 0.70 \times 6.39 = 4.473\%$.
> $r_e = 4.35 + 1.10(4.00) + 4.473 = 4.35 + 4.40 + 4.473 = 13.223\%$, or about 13.22%.
> A (11.24%) is wrong because it uses the raw spread without the volatility scaling: $8.75 + 0.70 \times 3.55 = 11.235\%$.
> C (15.14%) is wrong because it omits the 70% exposure weight: $8.75 + 6.39 = 15.14\%$.
> 6. **B.** Emerging market stocks often have low correlations with a world index, so the single-factor global CAPM produces low or even negative betas that understate their risk.
> The international CAPM adds a wealth-weighted currency factor to the global market factor to address this weakness.
> A is wrong because the low beta reflects low correlation, not an absence of risk, and it ignores currency and country risks that a world investor still bears.
> C is wrong because the global CAPM tends to understate, not overstate, emerging market required returns, and the single-factor version has no currency term at all.

## Distractor design

- Q1: A uses the short rate as the expected risk-free return (spot vs long-horizon rate); C reverses the sign of the repricing term (sign error).
- Q2: B attributes the gap to double counting buybacks, which the DDM counts once through consensus per-share growth (wrong formula variant); C reverses the direction of the gap and assumes buybacks are missing (sign error).
- Q3: B uses arithmetic instead of geometric means (wrong mean); C uses bills instead of long bonds (wrong risk-free proxy).
- Q4: A and B each capture only one of Pike's two upward-biasing choices, missing that the two effects compound.
- Q5: A omits the equity-to-bond volatility scaling (bond spread used as equity premium); C omits the revenue exposure weight lambda.
- Q6: A reads low correlation as low risk; C reverses the direction of the global CAPM bias and invents a currency term.
