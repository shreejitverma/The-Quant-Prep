---
type: cfa-itemset
topic: "Portfolio Management"
topic_code: "09"
topic_slug: "09-Portfolio-Management"
lm: 4
title: "Kestrel University Endowment: Two-Factor APT Arbitrage"
los: [los-09-04-a, los-09-04-b, los-09-04-c, los-09-04-f]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/portfolio-management]
---

# Kestrel University Endowment: Two-Factor APT Arbitrage

> [!info] Timer
> 18 minutes for 6 questions (or 12 for 4). Record confidence 1-5 before opening the answer key.

## Vignette

The Kestrel University Endowment has a perpetual horizon and distributes 4.5% of its trailing average value each year to the university.
The university's operating revenue comes mainly from tuition and a state appropriation that has not fallen in any of the last four recessions.
Imogen Achterberg, CFA, chairs the endowment's investment committee.
Rafael Okonjo, a quantitative analyst on her staff, has been asked to evaluate four well-diversified equity portfolios offered by external managers using a two-factor arbitrage pricing theory (APT) model.

The two factors are business cycle risk and inflation risk.
Okonjo estimates each portfolio's sensitivities to the two factors and obtains consensus one-year expected returns from the managers' research.
He notes that the one-year Treasury bill yields 3.0% and that the 10-year Treasury note yields 4.1%.
All four portfolios hold enough securities that asset-specific risk can be treated as zero.

**Exhibit 1: Well-diversified portfolios, one-year horizon**

| Portfolio | Business cycle sensitivity | Inflation sensitivity | Expected return | CAPM beta |
|---|---|---|---|---|
| P1 | 1.20 | 0.40 | 7.20% | 1.15 |
| P2 | 0.60 | 1.00 | 3.90% | 0.70 |
| P3 | 0.50 | 0.70 | 3.95% | 0.62 |
| P4 | 0.90 | 0.70 | 5.90% | 0.94 |

Okonjo uses Portfolios P1 and P2, together with the Treasury bill as the risk-free rate, to estimate the factor risk premiums.
He then checks P3 and P4 against the resulting APT equation.

At the committee meeting, Achterberg and Okonjo each comment on the model.

Achterberg (9 May): "The APT is attractive to us because it needs fewer and weaker assumptions than the CAPM. It assumes that a factor model describes returns, that diversification can eliminate asset-specific risk, and that no arbitrage opportunities exist among well-diversified portfolios. It does not require that investors choose portfolios using only means, variances, and correlations."

Okonjo (9 May): "The APT itself establishes that business cycle risk and inflation risk are the two priced factors, which is why I built a two-factor model rather than a three-factor one."

If any portfolio is mispriced, Okonjo wants to show the committee a trade that exploits the mispricing with a $20 million position on each side and no net investment.
He also wants to report the expected return on a portfolio that has a sensitivity of 1.0 to inflation risk and 0.0 to business cycle risk, because the committee asked how to interpret the inflation risk premium.

Finally, the committee debates the endowment's strategic factor exposures.
One trustee argues that the endowment should simply hold the market portfolio and Treasury bills in proportions set by its risk tolerance.
A second trustee argues that the endowment should overweight inflation-sensitive assets, because a positive sensitivity to inflation must earn a positive premium.
Achterberg argues that the endowment's situation differs from that of the typical investor, whose employment income falls in recessions, and that the factor view should shape the policy portfolio.

## Questions

1. Regarding the statements made on 9 May, which is most likely correct? (LOS: los-09-04-a)
   - A. Only Achterberg's statement.
   - B. Only Okonjo's statement.
   - C. Both statements.
2. Using P1, P2, and the Treasury bill, the business cycle risk premium and the inflation risk premium are closest to: (LOS: los-09-04-c)
   - A. 4.00% and -1.50%.
   - B. 4.00% and 1.50%.
   - C. 5.88% and 0.38%.
3. Relative to the APT equation Okonjo estimates, Portfolio P4 is: (LOS: los-09-04-c)
   - A. undervalued, because its APT expected return is 5.55%.
   - B. overvalued, because its APT expected return is 7.65%.
   - C. overvalued, because its APT expected return is 6.60%.
4. The trade that exploits the mispricing in Exhibit 1, and its expected profit, is closest to: (LOS: los-09-04-b)
   - A. Buy $20 million of P4, short $10 million each of P1 and P2; expected profit $70,000.
   - B. Short $20 million of P4, buy $10 million each of P1 and P2; expected profit $70,000.
   - C. Buy $20 million of P4, short $20 million of P3; expected profit $390,000.
5. The expected return on the portfolio with an inflation sensitivity of 1.0 and a business cycle sensitivity of 0.0, and the best explanation of the committee's question, is: (LOS: los-09-04-c)
   - A. 1.50%; investors accept a return below the risk-free rate because positive inflation sensitivity hedges inflation.
   - B. 4.50%; investors demand compensation above the risk-free rate for bearing inflation risk.
   - C. -1.50%; the expected return on a pure factor portfolio equals its factor risk premium.
6. Regarding the strategic factor exposures, whose argument is most consistent with a multifactor view of the endowment? (LOS: los-09-04-f)
   - A. Achterberg's, because the endowment can bear business cycle risk more cheaply than the typical investor and can tilt toward it to earn the premium.
   - B. The first trustee's, because only market risk is priced and every investor should hold the market portfolio and the risk-free asset.
   - C. The second trustee's, because inflation-sensitive assets earn a positive premium for bearing inflation risk.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Achterberg lists the three APT assumptions correctly and correctly contrasts them with the CAPM's mean-variance requirement.
> Okonjo's statement is wrong because the APT does not specify the identity or even the number of priced factors; the choice of business cycle and inflation is the analyst's modeling decision, not a result of the theory.
> B is wrong because it accepts the claim that APT identifies the factors.
> C is wrong for the same reason.
> 2. **A.** Subtract the risk-free rate from each expected return and solve two equations in two unknowns.
> P1: $0.072 - 0.030 = 0.042 = 1.20\lambda_1 + 0.40\lambda_2$.
> P2: $0.039 - 0.030 = 0.009 = 0.60\lambda_1 + 1.00\lambda_2$.
> Solving gives $\lambda_1 = 0.0400$ and $\lambda_2 = -0.0150$, so the APT equation is $E(R_p) = 0.03 + 0.04\beta_{p,BC} - 0.015\beta_{p,INFL}$.
> Check with P3: $0.03 + 0.04(0.50) - 0.015(0.70) = 0.0395$, matching Exhibit 1, so P3 is fairly priced.
> B is wrong because it drops the negative sign on the inflation premium, a sign error in the elimination step.
> C is wrong because it omits the risk-free rate and solves $0.072 = 1.20\lambda_1 + 0.40\lambda_2$ and $0.039 = 0.60\lambda_1 + 1.00\lambda_2$, giving 0.05875 and 0.00375.
> 3. **A.** $E(R_{P4}) = 0.03 + 0.04(0.90) - 0.015(0.70) = 0.03 + 0.0360 - 0.0105 = 0.0555$.
> P4 offers 5.90%, more than the 5.55% its factor risk requires, so it is undervalued.
> B is wrong because it uses $+0.015$ for the inflation premium: $0.03 + 0.0360 + 0.0105 = 0.0765$.
> C is wrong because it omits the inflation factor: $0.03 + 0.0360 = 0.0660$.
> 4. **A.** Find weights on P1 and P2 that replicate P4's two sensitivities: $1.20w_1 + 0.60w_2 = 0.90$ and $0.40w_1 + 1.00w_2 = 0.70$ give $w_1 = 0.50$ and $w_2 = 0.50$, which sum to 1.0, so no Treasury bill position is needed.
> The 50/50 mix has sensitivities (0.90, 0.70) and expected return $0.5(0.072) + 0.5(0.039) = 0.0555$.
> Buy the undervalued P4 and short the matched mix: net investment is zero, net factor sensitivities are zero, and expected profit is $\$20{,}000{,}000 \times (0.0590 - 0.0555) = \$70{,}000$.
> B is wrong because it uses the right replicating weights in the wrong direction, shorting the cheap side; it would expect to lose $70,000.
> C is wrong because P3 matches only P4's inflation sensitivity (0.70); the position keeps a business cycle exposure of $0.90 - 0.50 = 0.40$, so the $390,000 is not riskless.
> 5. **A.** A pure inflation factor portfolio has $E(R) = R_F + \lambda_{INFL} = 0.030 - 0.015 = 0.0150$.
> The inflation premium is negative because an asset whose return rises with unexpected inflation hedges inflation, and investors accept a lower expected return to hold such a hedge.
> B is wrong because it flips the sign of the premium: $0.030 + 0.015 = 0.045$.
> C is wrong because it reports the premium alone; the premium is the expected return on the pure factor portfolio minus the risk-free rate.
> 6. **A.** Multifactor models let an investor tilt toward priced risks it bears at a comparative advantage.
> The endowment has a perpetual horizon and a sponsor whose revenue does not fall in recessions, so it can harvest the business cycle premium that the average investor, whose labor income is procyclical, demands.
> B is wrong because it is the CAPM two-fund prescription, which ignores the endowment's different exposure to other priced risks.
> C is wrong because the inflation premium in this model is negative; overweighting inflation-sensitive assets lowers expected return in exchange for an inflation hedge.

## Distractor design

- Q1: B and C = belief that APT specifies the identity and number of factors.
- Q2: B = sign error on the inflation premium; C = risk-free rate omitted from the APT equations.
- Q3: B = inflation premium sign flipped; C = inflation factor omitted from the expected-return equation.
- Q4: B = right weights, wrong direction (shorts the underpriced portfolio); C = replication matches only one of two sensitivities.
- Q5: B = premium sign flipped; C = factor premium confused with the pure factor portfolio's expected return.
- Q6: B = CAPM two-fund prescription applied to an investor with a comparative advantage; C = negative inflation premium read as positive.
