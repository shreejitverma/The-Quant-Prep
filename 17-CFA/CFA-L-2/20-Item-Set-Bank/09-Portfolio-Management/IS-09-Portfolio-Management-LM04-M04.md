---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Saltmarsh Mutual Assurance: APT Without a Risk-Free Asset"
los: [los-09-04-a, los-09-04-b, los-09-04-c]
difficulty: 3
minutes: 12
source: mock-04
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Saltmarsh Mutual Assurance: APT Without a Risk-Free Asset

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Saltmarsh Mutual Assurance is a mid-sized property and casualty insurer domiciled in a small open economy whose currency is not widely traded.
The company invests its policyholder surplus in well-diversified local equity portfolios run by external managers.
Adaeze Obi, CFA, is Saltmarsh's chief investment officer, and Tomasz Wierzbicki is a quantitative analyst on her team.

The investment committee has asked Obi to test whether the four portfolios on its approved list are priced consistently with one another before it rebalances the surplus portfolio.
Wierzbicki proposes a one-factor arbitrage pricing theory (APT) model in which the factor is the unexpected change in national industrial production.
He explains that he will not treat any local asset as risk-free.
The one-year local government bond yields 4.20%, but the sovereign carries a speculative-grade rating and its credit default swap spread has widened sharply over the past year, so that yield includes compensation for default risk.

Wierzbicki estimates each portfolio's sensitivity to the industrial production factor from ten years of monthly data and collects consensus one-year expected returns.
All investors are assumed to agree on these expected returns, and each portfolio holds enough securities that asset-specific risk can be ignored.

**Exhibit 1: Approved local equity portfolios, one-year horizon**

| Portfolio | Industrial production sensitivity | Expected return | Return standard deviation | CAPM beta (local index) |
|---|---|---|---|---|
| Alder | 0.60 | 5.40% | 14.2% | 0.72 |
| Birch | 1.40 | 8.60% | 19.8% | 1.18 |
| Cedar | 1.20 | 7.40% | 17.5% | 0.91 |
| Dogwood | 1.80 | 10.20% | 23.6% | 1.35 |

Wierzbicki estimates the parameters of the pricing equation from Alder and Birch and then checks Cedar and Dogwood against it.
He notes that, without a risk-free asset, the intercept of the APT equation must be interpreted differently from the textbook case.

Obi wants to show the committee how any mispricing could be exploited.
She asks Wierzbicki to design a trade with a $5 million position on each side, no net investment, and no net exposure to the industrial production factor, using only the portfolios in Exhibit 1.
She also asks him to report the expected returns the model implies for two hypothetical well-diversified portfolios: one with no sensitivity to industrial production, and one with a sensitivity of exactly 1.0.

At the committee meeting, Obi and Wierzbicki each comment on the model.

Obi (14 March): "One drawback of the APT for us is that, like the CAPM, it requires investors to choose portfolios using only the means, variances, and correlations of returns. Its advantage is that it allows more than one factor."

Wierzbicki (14 March): "The APT does not need a risk-free asset. When none exists, the intercept of the pricing equation is the expected return on a well-diversified portfolio with zero sensitivity to every factor, and the model still rules out arbitrage among well-diversified portfolios."

A committee member asks whether the approved list should be trimmed if one of the portfolios turns out to be mispriced.
Obi replies that the committee should first understand how the mispricing would be exploited and what would happen to prices as other investors traded on it.

## Questions

1. The intercept of Wierzbicki's APT equation and the industrial production factor risk premium are closest to: (LOS: los-09-04-c)
   - A. 4.20% and 2.00%.
   - B. 3.00% and 4.00%.
   - C. 3.48% and 3.20%.
2. The trade that exploits the mispricing in Exhibit 1, and its expected profit, is closest to: (LOS: los-09-04-b)
   - A. Buy $5 million of Cedar, short $1.25 million of Alder and $3.75 million of Birch; expected profit $20,000.
   - B. Buy $5 million of Cedar, short $3.75 million of Alder and $1.25 million of Birch; expected profit $60,000.
   - C. Short $5 million of Cedar, buy $1.25 million of Alder and $3.75 million of Birch; expected profit $20,000.
3. The expected returns the model implies for the hypothetical portfolio with zero sensitivity and for the one with a sensitivity of 1.0 are closest to: (LOS: los-09-04-c)
   - A. 3.00% and 7.00%.
   - B. 4.20% and 8.20%.
   - C. 0.00% and 4.00%.
4. Regarding the statements made on 14 March, which is correct? (LOS: los-09-04-a)
   - A. Obi's only.
   - B. Wierzbicki's only.
   - C. Both statements.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** With no risk-free asset the APT equation is $E(R_p) = \lambda_0 + \lambda_1 \beta_{p,1}$, and two well-diversified portfolios give two equations in two unknowns.
> Alder: $5.40 = \lambda_0 + 0.60\lambda_1$; Birch: $8.60 = \lambda_0 + 1.40\lambda_1$.
> Subtracting, $3.20 = 0.80\lambda_1$, so $\lambda_1 = 3.20/0.80 = 4.0000\%$, and $\lambda_0 = 5.40 - 0.60 \times 4.00 = 3.0000\%$.
> The equation is $E(R_p) = 3.00\% + 4.00\% \times \beta_{p,1}$.
> A is wrong because it treats the defaultable 4.20% government bond yield as the risk-free rate and solves from Alder alone: $(5.40 - 4.20)/0.60 = 2.0000\%$.
> C is wrong because it takes the 3.20% return spread as the premium without dividing by the 0.80 sensitivity gap, then backs out $5.40 - 0.60 \times 3.20 = 3.4800\%$.
> 2. **C.** Check each portfolio against the line: Cedar's APT return is $3.00 + 4.00 \times 1.20 = 7.8000\%$, but it offers only 7.40%, so Cedar is overvalued; Dogwood's is $3.00 + 4.00 \times 1.80 = 10.2000\%$, exactly as offered.
> Replicate Cedar's sensitivity with Alder and Birch: $0.60w + 1.40(1 - w) = 1.20$ gives $w = 0.2500$ in Alder and $0.7500$ in Birch.
> The mix has sensitivity $0.25 \times 0.60 + 0.75 \times 1.40 = 1.2000$ and expected return $0.25 \times 5.40 + 0.75 \times 8.60 = 1.3500 + 6.4500 = 7.8000\%$.
> Short $5 million of the overvalued Cedar and use the proceeds to buy $1.25 million of Alder and $3.75 million of Birch: net investment is zero, net sensitivity is $1.20 - 1.20 = 0$, and expected profit is $\$5{,}000{,}000 \times (0.0780 - 0.0740) = \$20{,}000$.
> A is wrong because it uses the right weights in the wrong direction, buying the overvalued side; its expected result is a $20,000 loss.
> B is wrong because it swaps the weights: 75% Alder and 25% Birch has sensitivity $0.75 \times 0.60 + 0.25 \times 1.40 = 0.8000$ and expected return 6.2000%, so the apparent $\$5{,}000{,}000 \times (0.0740 - 0.0620) = \$60{,}000$ carries a net factor exposure of $1.20 - 0.80 = 0.40$ and is not an arbitrage.
> A 50/50 mix of Alder and Dogwood would also replicate Cedar (sensitivity 1.20, expected return 7.80%), but that trade is not offered.
> 3. **A.** A well-diversified portfolio with zero factor sensitivity earns the intercept, $\lambda_0 = 3.00\%$, which is why the intercept plays the role of the risk-free rate when none exists.
> A portfolio with sensitivity 1.0 earns $\lambda_0 + \lambda_1 = 3.00 + 4.00 = 7.0000\%$; the premium is its expected return minus the zero-sensitivity return.
> B is wrong because it anchors the line at the defaultable 4.20% government yield: $4.20$ and $4.20 + 4.00 = 8.20\%$.
> C is wrong because it assumes a zero-sensitivity portfolio earns nothing and equates the factor premium with the expected return of the unit-sensitivity portfolio.
> 4. **B.** Wierzbicki is correct: the APT's three assumptions are that a factor model describes returns, that diversification eliminates asset-specific risk, and that no arbitrage opportunities exist among well-diversified portfolios; a risk-free asset is not required, and without one the intercept $\lambda_0$ is the expected return on a well-diversified portfolio with zero sensitivity to all factors.
> Obi is wrong because the APT does not assume mean-variance decision making; that is a CAPM assumption, and the APT's fewer, weaker assumptions are one of its attractions.
> A is wrong because it accepts the CAPM mean-variance assumption as part of the APT.
> C is wrong for the same reason.

## Distractor design

1. A: defaultable government yield used as the risk-free rate (misread exhibit decoy); C: return spread not divided by the sensitivity difference.
2. A: right replicating weights, wrong direction (buys the overvalued portfolio); B: weights swapped, so sensitivities do not match and factor risk remains.
3. B: defaultable yield used as the zero-sensitivity return; C: zero-sensitivity return set to zero and premium confused with the unit-sensitivity portfolio's expected return.
4. A and C: CAPM mean-variance assumption attributed to the APT.
