---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 2
title: "Tasman Hardwood Imports: Currency Options on a Euro Invoice"
los: [los-07-02-f, los-07-02-g, los-07-02-h, los-07-02-k]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Tasman Hardwood Imports: Currency Options on a Euro Invoice

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Liam Kovac, CFA, is a treasury analyst at Tasman Hardwood Imports, an Australian company that reports in Australian dollars (AUD).
Tasman has ordered kiln-drying equipment from a German manufacturer and must pay EUR 3,000,000 in six months.
The chief financial officer, Ruth Delaney, wants to cap the AUD cost of the invoice while keeping the benefit if the euro weakens.
Kovac has obtained quotes from Jonah Whitford, a derivatives salesperson at Coral Sea Bank, for six-month European call options on the euro covering the full invoice.
All interest rates in Exhibit 1 are annualized and continuously compounded.

**Exhibit 1: EUR option inputs**

| Item | Value |
|---|---|
| Spot exchange rate | AUD 1.6500 per EUR |
| Exercise price | AUD 1.6800 per EUR |
| Time to expiration | 0.50 years |
| AUD risk-free rate | 4.10% |
| EUR risk-free rate | 2.30% |
| Six-month forward exchange rate | AUD 1.6649 per EUR |
| Implied volatility used in the model | 9.0% |
| Historical volatility, past 12 months | 11.0% |
| $N(d_1)$ at 9.0% volatility | 0.4562 |
| $N(d_2)$ at 9.0% volatility | 0.4311 |

Kovac values the options with the Black-Scholes-Merton (BSM) model adjusted for the carry benefit of the underlying currency.
Delaney asks him to express the option position as an equivalent combination of euro holdings and AUD money-market borrowing or lending, because Tasman's board approves only hedges it can describe in cash terms.
She adds that any euros in such a portfolio would be held on deposit at the EUR risk-free rate until the invoice date.

In a memo dated 11 August, Kovac makes three statements about the model.

- Statement 1: "BSM assumes that the AUD/EUR exchange rate follows geometric Brownian motion, so its continuously compounded returns are normally distributed and the rate does not jump."
- Statement 2: "BSM treats the interest earned on euro holdings as a yield paid continuously at a constant rate, which is why the EUR rate enters the model as the carry benefit."
- Statement 3: "Because BSM allows volatility to change over the option's life, we can use today's 9.0% implied volatility even though historical volatility has been 11.0%."

Delaney questions whether the forward rate in Exhibit 1 should replace the spot rate in the model.
Kovac answers that the spot rate and the two interest rates already imply that forward rate, so the carry-adjusted BSM model uses the spot rate directly.

On 12 August, Whitford tells Kovac that Coral Sea Bank also writes the matching European put on the euro, with the same exercise price and expiry.
He notes that the bank's risk team hedges its written options in delta terms, and he asks Kovac to confirm the delta of one matching put from Exhibit 1.
Whitford also says that a rise in the EUR interest rate would, other things equal, lower the value of Tasman's calls.

## Questions

1. The BSM value of calls on EUR 3,000,000 is closest to: (LOS: los-07-02-h)
   - A. AUD 64,468.
   - B. AUD 103,713.
   - C. AUD 129,534.
2. The portfolio that replicates Tasman's call position is closest to: (LOS: los-07-02-g)
   - A. buy EUR 1,352,951 and borrow AUD 2,128,656.
   - B. buy EUR 1,352,951 and borrow AUD 2,147,901.
   - C. buy EUR 1,368,600 and borrow AUD 2,128,656.
3. Which of Kovac's statements is inconsistent with the assumptions of the BSM model? (LOS: los-07-02-f)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.
4. The delta of one matching European put on the euro is closest to: (LOS: los-07-02-k)
   - A. -0.5376.
   - B. -0.5438.
   - C. -0.5490.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** For a currency option the underlying is the spot rate quoted in domestic currency per unit of foreign currency (AUD per EUR), the domestic AUD rate is the risk-free rate, and the foreign EUR rate is the carry benefit $\gamma = r^f$.
> $c = Se^{-r^f T}N(d_1) - Xe^{-rT}N(d_2)$ with $e^{-0.023 \times 0.5} = 0.988566$ and $e^{-0.041 \times 0.5} = 0.979709$.
> Currency leg: $1.6500(0.988566)(0.4562) = 0.744123$; bond leg: $1.6800(0.979709)(0.4311) = 0.709552$.
> $c = 0.744123 - 0.709552 = 0.034571$ per EUR, or $0.034571 \times 3{,}000{,}000 = $ AUD 103,713 (full-precision BSM gives 0.034621 per EUR; the difference is rounding in the $N(\cdot)$ values).
> A is wrong because it swaps the domestic and foreign rates, $1.65e^{-0.0205}(0.4562) - 1.68e^{-0.0115}(0.4311) = 0.737461 - 0.715972 = 0.021489$, AUD 64,468.
> C is wrong because it omits the carry benefit on the currency leg, $1.65(0.4562) - 0.709552 = 0.043178$, AUD 129,534.
> 2. **A.** A BSM call is a leveraged position in the underlying: hold $e^{-r^f T}N(d_1)$ units of the foreign currency per option, financed by borrowing $e^{-rT}XN(d_2)$ in domestic currency.
> Euros: $0.988566 \times 0.4562 \times 3{,}000{,}000 = $ EUR 1,352,951, which grow on deposit at the EUR rate, just as dividend-paying shares require fewer shares in the replication.
> Borrowing: $0.709552 \times 3{,}000{,}000 = $ AUD 2,128,656.
> Net cost: $1{,}352{,}951 \times 1.65 - 2{,}128{,}656 = 2{,}232{,}370 - 2{,}128{,}656 = $ AUD 103,713, the call value from Question 1.
> B is wrong because it discounts the strike at the EUR rate rather than the AUD rate, $1.68 \times 0.988566 \times 0.4311 \times 3{,}000{,}000 = $ AUD 2,147,901.
> C is wrong because it holds $N(d_1) \times 3{,}000{,}000 = $ EUR 1,368,600, ignoring that the euro deposit earns the foreign rate.
> 3. **C.** BSM assumes the volatility of the underlying's return is known and constant over the option's life; using implied volatility is a practical input choice, not a feature of the model.
> A is wrong because geometric Brownian motion, with normally distributed continuously compounded returns and no jumps, is a BSM assumption.
> B is wrong because BSM assumes any yield on the underlying is paid continuously at a constant rate, which is exactly how the foreign interest rate enters a currency option.
> 4. **A.** Put delta is $-e^{-r^f T}N(-d_1)$, with $N(-d_1) = 1 - 0.4562 = 0.5438$.
> $\text{Delta}_p = -0.988566 \times 0.5438 = -0.5376$.
> Carry-adjusted parity gives the same result: $\text{Delta}_c - e^{-r^f T} = 0.988566(0.4562) - 0.988566 = 0.4510 - 0.9886 = -0.5376$.
> B is wrong because it drops the carry factor, $-N(-d_1) = -0.5438$.
> C is wrong because it uses the no-carry parity relation, $\text{Delta}_c - 1 = 0.4510 - 1 = -0.5490$.
> Whitford's remark about the EUR rate is also consistent with the model: a higher carry benefit lowers call values and raises put values.

## Distractor design

1. A: domestic and foreign rates swapped (misread exhibit); C: carry benefit omitted from the currency leg (wrong formula variant).
2. B: strike discounted at the foreign rate instead of the domestic rate (rate mix-up); C: currency holding sized at $N(d_1)$ without the carry adjustment (wrong formula variant).
3. A: geometric Brownian motion misread as an inconsistent assumption (assumption misread); B: continuous constant carry yield misread as inconsistent (assumption misread).
4. B: carry factor omitted from put delta (wrong formula variant); C: no-carry delta parity applied to a currency option (wrong formula variant).
