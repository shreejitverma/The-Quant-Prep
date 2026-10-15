---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 5
title: "Great Lakes Commerce Bank: Hedging a Loan Concentration"
los: [los-06-05-a, los-06-05-d, los-06-05-e]
difficulty: 3
minutes: 12
source: bank
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Great Lakes Commerce Bank: Hedging a Loan Concentration

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Samuel Orr is head of portfolio management at Great Lakes Commerce Bank, a regional bank in Cleveland.
The bank's largest single commercial exposure is $40 million of term loans to Tamarack Industries, an investment-grade manufacturer rated BBB.
The loans are illiquid, and selling them would damage a long client relationship, so the credit committee has asked Orr to reduce the exposure temporarily using CDS.

Priya Nandakumar, a credit analyst, prepares a briefing on the proposed contract.
She makes three statements to the committee.

Statement 1: "Tamarack has only $300 million of debt outstanding, so the total notional of CDS written on Tamarack cannot exceed that amount, and dealers may therefore limit how much protection we can buy."

Statement 2: "Our contract will carry the standardized 1% coupon because Tamarack is investment grade, and because Tamarack's spread is above that coupon we will pay an upfront premium at initiation."

Statement 3: "The contract pays only if Tamarack defaults on the specific senior unsecured bond named as the reference obligation."

On 15 March 2026, the bank buys $40 million of protection on Tamarack maturing on 20 June 2031, when Tamarack's five-year credit spread is 210 bps.
The contract's effective spread duration is 4.4.
Three weeks later, a competitor wins a large contract away from Tamarack and Tamarack's five-year spread widens to 285 bps.
The committee asks Orr what the hedge is now worth, assuming the duration is unchanged.

Nandakumar also runs a small proprietary credit book for the bank's treasury.
She is following two US retailers after a data breach at a shared payment processor.
Brightwell Stores has an independent board and a well-funded cybersecurity program; Carrow Outlets has a founder-controlled board and had been criticized by regulators for weak data controls.
Before the breach, Brightwell's five-year CDS spread was 140 bps and Carrow's was 230 bps.
After the breach, they widened to 205 bps and 310 bps, respectively.
Nandakumar expects Brightwell's spread to return to 140 bps, but because of its weaker governance, she expects Carrow's to narrow only to 290 bps.

Exhibit 1: Duquesne Materials instruments

| Instrument | Quote |
|---|---|
| Five-year fixed-rate senior unsecured bond, trading near par, no embedded options | Yield 7.40% |
| Five-year CDS spread | 3.35% |
| Five-year floating-rate term loan | MRR + 3.90% |
| Market reference rate (MRR) | 3.60% |

Nandakumar believes the pricing of Duquesne's credit risk in the bond market and in the CDS market will converge over the next year.
She wants to exploit the difference using the bond and the CDS, hedging interest rate risk with Treasury futures.

## Questions

1. Which of Nandakumar's statements about the CDS contract is most accurate? (LOS: los-06-05-a)
   - A. Statement 1
   - B. Statement 2
   - C. Statement 3
2. After Tamarack's spread widens to 285 bps, the value change on the bank's CDS position is closest to: (LOS: los-06-05-d)
   - A. a gain of $1,320,000.
   - B. a loss of $1,320,000.
   - C. a gain of $3,256,000.
3. The long/short trade most consistent with Nandakumar's view on the two retailers, and the change in the spread differential between them if her forecasts are correct, is: (LOS: los-06-05-d)
   - A. buy protection on Brightwell and sell protection on Carrow; 45 bps.
   - B. buy protection on Carrow and sell protection on Brightwell; 45 bps.
   - C. buy protection on Carrow and sell protection on Brightwell; 85 bps.
4. The Duquesne trade and the profit captured on convergence are best described as: (LOS: los-06-05-e)
   - A. buy the bond and buy protection; about 4.05%.
   - B. sell protection and short the bond; about 0.45%.
   - C. buy the bond and buy protection; about 0.45%.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** CDS coupons are standardized at 1% for investment-grade reference entities, and when the credit spread (210 bps) exceeds the coupon (100 bps), the protection buyer pays the seller an upfront premium, here about $(0.0210 - 0.0100) \times 4.4 = 4.84\%$ of notional.
> A is wrong because total CDS notional can exceed the reference entity's debt outstanding; protection buyers need not be creditors.
> C is wrong because a single-name CDS covers every obligation of Tamarack ranked equal to or higher than the reference obligation, and a failure to pay on other obligations can also be a credit event; the payout is set by the cheapest-to-deliver covered obligation.
> 2. **A.** The bank bought protection, so it is short Tamarack credit and gains when the spread widens.
> Gain $= \Delta\text{spread} \times \text{duration} \times \text{notional} = (0.0285 - 0.0210) \times 4.4 \times 40{,}000{,}000 = 0.0075 \times 4.4 \times 40{,}000{,}000 = 1{,}320{,}000$.
> This gain offsets part of the decline in the value of the bank's Tamarack loans, which is the purpose of the hedge.
> B is wrong on sign: it treats the protection buyer as long credit, as a bondholder would be.
> C is wrong because it uses the new spread minus the standardized coupon, the upfront-premium formula, instead of the change in spread: $(0.0285 - 0.0100) \times 4.4 \times 40{,}000{,}000 = 3{,}256{,}000$.
> 3. **B.** Nandakumar expects Carrow (weak governance) to underperform Brightwell (strong governance), so she buys protection on Carrow (short Carrow credit) and sells protection on Brightwell (long Brightwell credit).
> The differential is $310 - 205 = 105$ bps now and $290 - 140 = 150$ bps if she is right, so it widens by $150 - 105 = 45$ bps, the trade's profit in spread terms before costs.
> Equivalently, the Brightwell short-protection leg gains $205 - 140 = 65$ bps and the Carrow long-protection leg loses $310 - 290 = 20$ bps, net $45$ bps.
> A is wrong because it reverses the legs and would lose 45 bps.
> C is wrong because it adds the two spread moves ($65 + 20 = 85$ bps) instead of netting them; Carrow's narrowing hurts the protection bought on Carrow.
> 4. **C.** Bond credit spread $= 7.40\% - 3.60\% = 3.80\%$, compared with a CDS spread of 3.35%.
> Basis $= 3.35\% - 3.80\% = -0.45\%$, a negative basis: credit risk is priced higher in the bond market, so the bond is cheap and protection is cheap.
> Buy the bond and buy protection, hedging rates with Treasury futures, and capture about 45 bps on convergence.
> A is wrong because it subtracts the CDS spread from the raw bond yield without removing MRR ($7.40\% - 3.35\% = 4.05\%$).
> B is wrong because selling protection and shorting the bond is the positive-basis trade and would lose the 45 bps as the spreads converge.

## Distractor design

1. A: CDS notional wrongly capped at debt outstanding (buyers assumed to be creditors); C: coverage limited to the named reference obligation instead of equal-or-higher seniority.
2. B: protection buyer treated as long credit (sign); C: upfront-premium formula (spread minus coupon) used instead of the change in spread.
3. A: long/short legs reversed; C: both legs' spread moves added instead of netted.
4. A: CDS spread subtracted from the raw yield (MRR not removed); B: basis sign reversed, so the positive-basis legs are applied.
