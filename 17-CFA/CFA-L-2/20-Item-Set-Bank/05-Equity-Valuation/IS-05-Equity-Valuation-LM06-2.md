---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 6
title: "Alder & Voss Logistics: A Minority Shareholder Dispute"
los: [los-05-06-d, los-05-06-e, los-05-06-f, los-05-06-h]
difficulty: 4
minutes: 18
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Alder & Voss Logistics: A Minority Shareholder Dispute

> [!info] Timer
> 18 minutes for 6 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Alder & Voss Logistik GmbH is a private German freight-forwarding company with three shareholders.
Konrad Alder, the founder and managing director, owns 60%, a cousin owns 25%, and Ines Voss, a former partner who left the company last year, owns 15%.
Voss has asked a court to order the company to buy her shares at fair market value, defined by the court as the value of a non-controlling, non-marketable interest.
Each side has retained a valuation expert, and the court has appointed Dieter Brandt, CFA, to reconcile their reports.

Brandt first builds his own required return on equity.
He identifies six listed freight forwarders as guideline public companies, although he doubts how comparable they are to a company one-twentieth their size.

Exhibit 1: Required return inputs

| Input | Value |
|---|---|
| Risk-free rate | 4.0% |
| Equity risk premium | 5.5% |
| Average levered beta, guideline companies | 1.30 |
| Average debt-to-equity ratio, guideline companies | 60% |
| Average tax rate, guideline companies | 25% |
| Alder & Voss debt-to-equity ratio | 20% |
| Alder & Voss tax rate | 22% |
| Small-stock premium | 2.8% |
| Industry risk premium | 0.8% |
| Company-specific risk premium | 2.0% |
| Alder & Voss debt outstanding | EUR 18.0 million |

He computes one estimate using the expanded CAPM with the guideline beta unlevered and relevered at Alder & Voss's capital structure, and a second using the build-up approach.

The expert retained by Voss, Petra Lind, values 100% of the equity at EUR 84.0 million using a DCF model.
Her model uses projected cash flows that assume the removal of Alder's above-market compensation and a capital structure that an acquirer of the whole company would establish.
To reach the value of Voss's stake, Lind cites acquisition data showing an average control premium of 25% for comparable companies and a restricted stock study supporting a discount for lack of marketability of 22%.

The expert retained by Alder, Hugo Marsh, instead capitalizes the free cash flow to equity that the company is expected to generate next year, EUR 9.6 million, under its current policies and current capital structure.
He applies Brandt's build-up cost of equity and a perpetual growth rate of 3.5%.
Marsh's report states that his result "reflects the position of an investor with no influence over management."

Brandt records two statements made at a joint experts' meeting.

Lind: "Alder & Voss has borrowed far less than the guideline companies because banks lend less to a company of its size. Its WACC at the current capital structure is therefore above its WACC at an optimal structure."

Marsh: "The size premium should be taken from the smallest decile of listed German companies, where the historical premium is 6.1%. Alder & Voss is small, and the smallest companies are the right benchmark."

## Questions

1. Brandt's expanded CAPM estimate of the required return on equity is closest to: (LOS: los-05-06-e)
   - A. 13.73%.
   - B. 14.50%.
   - C. 15.95%.
2. Compared with his expanded CAPM estimate, Brandt's build-up estimate is: (LOS: los-05-06-e)
   - A. 0.60% higher.
   - B. 0.80% higher.
   - C. 0.85% lower.
3. Regarding the statements recorded at the joint experts' meeting, which is most likely correct? (LOS: los-05-06-d)
   - A. Lind's statement only.
   - B. Marsh's statement only.
   - C. Both statements.
4. Using Lind's valuation and discount data, the value of Voss's 15% stake is closest to: (LOS: los-05-06-f)
   - A. EUR 7.37 million.
   - B. EUR 7.86 million.
   - C. EUR 9.83 million.
5. Marsh's equity value for 100% of Alder & Voss is closest to: (LOS: los-05-06-h)
   - A. EUR 64.76 million.
   - B. EUR 82.76 million.
   - C. EUR 85.66 million.
6. To convert Marsh's equity value to the value of Voss's 15% stake under the court's definition, Brandt should most appropriately apply: (LOS: los-05-06-f)
   - A. both a DLOC and a DLOM.
   - B. a DLOC only.
   - C. a DLOM only.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Unlever at the guideline companies' leverage and tax rate: $\beta_u = 1.30 / [1 + (1 - 0.25) \times 0.60] = 1.30 / 1.45 = 0.8966$.
> Relever at Alder & Voss's: $\beta^* = 0.8966 \times [1 + (1 - 0.22) \times 0.20] = 0.8966 \times 1.156 = 1.0364$.
> Expanded CAPM: $4.0\% + 1.0364 \times 5.5\% + 2.8\% + 2.0\% = 4.0\% + 5.7003\% + 4.8\% = 14.5003\%$, or about 14.50%.
> A is wrong because it stops at the unlevered beta ($4.0\% + 0.8966 \times 5.5\% + 4.8\% = 13.731\%$) and never relevers at the subject's structure.
> C is wrong because it uses the guideline companies' levered beta of 1.30 unadjusted ($4.0\% + 7.15\% + 4.8\% = 15.95\%$), ignoring that Alder & Voss carries less debt.
> 2. **A.** Build-up: $4.0\% + 5.5\% + 2.8\% + 0.8\% + 2.0\% = 15.10\%$, with the equity risk premium unscaled by beta.
> Difference: $15.10\% - 14.5003\% = 0.5997\%$, so the build-up estimate is about 0.60% higher.
> Decomposition: the industry premium adds 0.80%, and the unscaled premium removes $(1.0364 - 1) \times 5.5\% = 0.2003\%$, netting $+0.5997\%$.
> B is wrong because it counts only the industry premium, either ignoring the beta effect or scaling the build-up premium by beta.
> C is wrong because it compares the build-up result with an expanded CAPM based on the unadjusted beta ($15.10\% - 15.95\% = -0.85\%$).
> 3. **A.** Limited access to debt forces a higher equity weight, and because equity costs more than debt the current-structure WACC exceeds the optimal WACC, so Lind is correct.
> Marsh is incorrect because the premium measured for the very smallest listed companies may reflect financial or operating distress that is irrelevant to a sound private company, so it can overstate the size premium.
> B and C are wrong because they accept Marsh's benchmark without that caveat.
> 4. **B.** Lind's DCF uses control cash flows and an optimal capital structure, so it is a control value, and the stake is non-controlling and non-marketable.
> $DLOC = 1 - 1/1.25 = 0.2000$; total discount $= 1 - (1 - 0.20)(1 - 0.22) = 1 - 0.80 \times 0.78 = 0.3760$.
> Stake value $= 84.0 \times 0.15 \times (1 - 0.3760) = 12.60 \times 0.624 = 7.8624$ million.
> A is wrong because it uses the 25% control premium as the DLOC ($12.60 \times 0.75 \times 0.78 = 7.371$).
> C is wrong because it applies only the DLOM ($12.60 \times 0.78 = 9.828$), ignoring that the base value is on a control basis.
> 5. **B.** The EUR 9.6 million is already next year's FCFE, so it is capitalized directly at $r_e - g$.
> $V = 9.6 / (0.1510 - 0.035) = 9.6 / 0.1160 = 82.7586$ million.
> No debt is subtracted, because FCFE is already after payments to debtholders.
> A is wrong because it subtracts the EUR 18.0 million of debt from an FCFE-based equity value ($82.7586 - 18.0 = 64.7586$).
> C is wrong because it grows a cash flow that is already a next-year figure ($9.6 \times 1.035 / 0.1160 = 85.6552$).
> 6. **C.** Marsh's value uses cash flows under current policies and the current capital structure, from the position of an investor with no influence, so it already reflects lack of control.
> The stake is still non-marketable, so only a DLOM is needed.
> A is wrong because applying a DLOC to a value that is not on a control basis double counts the lack of control.
> B is wrong because it omits the marketability discount that the court's definition requires.

## Distractor design

1. A: unlevered beta used without relevering (formula variant stopped halfway); C: guideline levered beta used unadjusted (leverage mismatch).
2. B: beta effect in the build-up comparison ignored (industry premium only); C: difference computed against the unadjusted-beta expanded CAPM (carried-forward error from Q1 option C).
3. B and C: size premium from distressed smallest-decile data accepted without adjustment.
4. A: control premium used as the DLOC (premium versus discount); C: DLOC omitted despite a control-basis starting value (basis error).
5. A: debt subtracted from an FCFE value (firm versus equity confusion); C: next-year cash flow grown again (period error).
6. A: DLOC applied to a non-control basis value (double counting); B: DLOM omitted (marketability ignored).
