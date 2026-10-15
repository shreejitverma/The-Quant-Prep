---
type: cfa-itemset
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
lm: 2
title: "Brenmoor Life Frontier Bond Allocation"
los: [los-02-02-c, los-02-02-e, los-02-02-g, los-02-02-i]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/economics]
---

# Brenmoor Life Frontier Bond Allocation

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Daniel Okafor, CFA, is a portfolio manager in the general account of Brenmoor Life Assurance, a mid-sized insurer that matches long-dated annuity liabilities with inflation-linked government bonds.
The asset-liability committee has approved a small allocation to the real-return sovereign bonds of two frontier economies, the Republic of Lusavia and the Republic of Marenta.
Okafor must recommend how to split the allocation between them.

Okafor's first task is to estimate each country's potential GDP growth rate.
He prefers the labor productivity growth accounting method because reliable capital stock data are not available for either country.
To smooth cyclical noise, he takes the geometric mean of the two most recent subperiod growth rates for each input.

**Exhibit 1: Annual average growth rates by subperiod**

| Measure | Lusavia 2010-2017 | Lusavia 2018-2025 | Marenta 2010-2017 | Marenta 2018-2025 |
|---|---|---|---|---|
| Hours worked | 1.9% | 1.3% | 0.4% | 0.2% |
| Labor productivity | 3.6% | 2.8% | 1.7% | 1.5% |
| Total factor productivity (TFP) | 1.4% | 1.2% | 0.9% | 0.8% |
| Population | 2.3% | 2.0% | 0.5% | 0.3% |

Okafor next considers a structural reform in Lusavia.
Lusavia's parliament has passed a mandatory retirement savings scheme that is expected to raise the gross national saving rate permanently from 20% to 25% of GDP.
Okafor's economic adviser, Selin Arda, models Lusavia with a Cobb-Douglas production function and a labor share of national income of 64%.
She assumes that TFP growth, labor force growth, and depreciation are unaffected by the reform.

**Exhibit 2: Demographic and labor market profile, 2025**

| Item | Lusavia | Marenta |
|---|---|---|
| Population under age 15 | 29% | 14% |
| Population over age 65 | 6% | 22% |
| Female labor force participation rate | 71% | 58% |
| Unemployment rate | 6.4% | 5.1% |

Marenta's government has announced a national childcare subsidy and a flexible-hours law.
Its labor ministry projects that female participation will rise from 58% to 66% over the next six years and then stabilize.

At a committee meeting on 2 February 2026, Okafor's colleague Ruth Delacroix presents her view of the two countries.
She states: "Marenta's childcare program will permanently raise its potential GDP growth rate by the amount the labor force grows during the program. And Lusavia's 2.0% population growth will, by itself, raise the growth rate of Lusavia's GDP per capita."

Okafor also reviews how potential growth feeds into bond pricing.
The inflation-linked bonds pay a real coupon, so their prices move inversely with real yields.
Brenmoor's investment policy notes that "real yields reflect both the real interest rate required to clear saving and investment and the sovereign's credit quality."
Okafor plans to hold the bonds for at least ten years and does not intend to hedge either country's real rate exposure.

In his draft memo dated 6 February 2026, Okafor writes that the country with the faster potential growth rate should, all else equal, offer a different level of real yield from the slower-growing country, and that the committee should understand the reason before approving the split.
Arda agrees to add a section on the long-run effect of Lusavia's saving reform on output per worker, measured against the path Lusavia would have followed without the reform.

## Questions

1. Using Okafor's method and Exhibit 1, Lusavia's potential GDP growth rate is closest to: (LOS: los-02-02-e)
   - A. 2.90%.
   - B. 4.80%.
   - C. 5.35%.
2. Under the neoclassical model and Arda's assumptions, once Lusavia reaches its new steady state, output per worker will be higher than on its pre-reform path by closest to: (LOS: los-02-02-i)
   - A. 8.36%.
   - B. 13.37%.
   - C. 41.72%.
3. Based on the potential growth estimates, relative to Marenta, Lusavia's real interest rates are most likely to be: (LOS: los-02-02-c)
   - A. higher, because faster expected income growth means savers must be paid more to postpone consumption and fund capital accumulation.
   - B. lower, because faster potential growth improves sovereign credit quality, which lowers the real rate required to clear saving and investment.
   - C. about the same, because in the long run real rates are set by the global capital market regardless of domestic growth.
4. Regarding the two claims in Delacroix's statement, which is most likely correct? (LOS: los-02-02-g)
   - A. The claim about Marenta only.
   - B. The claim about Lusavia only.
   - C. Neither claim.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Potential GDP growth equals long-term labor force growth plus long-term labor productivity growth, with each input the geometric mean of the subperiod rates.
> Hours worked: $[(1.019)(1.013)]^{1/2} - 1 = 1.5996\%$.
> Labor productivity: $[(1.036)(1.028)]^{1/2} - 1 = 3.1992\%$.
> Potential growth $= 1.5996\% + 3.1992\% = 4.7988\% \approx 4.80\%$.
> A is wrong because it adds TFP growth in place of labor productivity growth: $1.5996\% + [(1.014)(1.012)]^{1/2} - 1 = 1.5996\% + 1.3000\% = 2.8995\%$; TFP excludes the capital deepening that labor productivity growth contains.
> C is wrong because it uses population growth as the labor input: $[(1.023)(1.020)]^{1/2} - 1 = 2.1499\%$, and $2.1499\% + 3.1992\% = 5.3491\%$; labor input is hours worked, not population.
> 2. **B.** The required investment rate $\theta/(1-\alpha) + \delta + n$ is unchanged by the reform, so the steady-state output-to-capital ratio $\Psi = (1/s)[\theta/(1-\alpha) + \delta + n]$ scales with $1/s$: $(Y/K)_{new}/(Y/K)_{old} = 0.20/0.25 = 0.8000$.
> With $\alpha = 1 - 0.64 = 0.36$: $k_{new}/k_{old} = 0.8000^{1/(0.36-1)} = 1.25^{1.5625} = 1.4172$.
> $y_{new}/y_{old} = 1.4172^{0.36} = 1.25^{0.5625} = 1.1337$, so output per worker is 13.37% higher; its steady-state growth rate is unchanged at $\theta/(1-\alpha)$.
> A is wrong because it applies $\alpha$ directly to the saving ratio, $1.25^{0.36} = 1.0836$, skipping the step from the output-to-capital ratio to the capital-to-labor ratio.
> C is wrong because it reports the rise in capital per worker (41.72%) rather than output per worker, forgetting that diminishing returns scale output by $k^{\alpha}$.
> 3. **A.** Marenta's potential growth is $[(1.004)(1.002)]^{1/2} - 1 + [(1.017)(1.015)]^{1/2} - 1 = 0.3000\% + 1.6000\% = 1.8999\%$, far below Lusavia's 4.7988%.
> Faster potential growth means consumers expect rapidly rising real incomes, so a higher real interest rate is needed to induce the saving that funds the faster capital accumulation.
> B is wrong because it mixes up two channels: better credit quality lowers the credit spread, but the real interest rate that clears saving and investment rises with potential growth.
> C is wrong because the curriculum links domestic potential growth directly to the level of real interest rates; nothing in the vignette makes the rate purely global.
> 4. **C.** Marenta's claim is wrong because a rise in participation is a move to a new level of labor input, not a permanent change in its growth rate: labor force growth rises only while participation climbs from 58% to 66%, then potential growth returns to its prior rate once participation stabilizes.
> Lusavia's claim is wrong because population growth raises aggregate GDP growth but does not, by itself, raise the growth rate of GDP per capita.
> A is wrong because it extrapolates a six-year participation transition indefinitely.
> B is wrong because it credits population growth with per capita gains; Lusavia's young age structure and unemployment rate are decoys that do not rescue the claim as stated.

## Distractor design

1. A substitutes TFP growth for labor productivity growth; C uses population growth instead of hours worked as the labor input.
2. A raises the saving ratio to the power $\alpha$ and skips the capital-to-labor step; C reports the capital-per-worker ratio instead of the output-per-worker ratio.
3. B confuses the credit-spread channel with the real-rate channel; C denies the link between potential growth and real interest rates.
4. A treats a participation-rate transition as a permanent growth-rate change; B credits aggregate population growth with per capita growth.
