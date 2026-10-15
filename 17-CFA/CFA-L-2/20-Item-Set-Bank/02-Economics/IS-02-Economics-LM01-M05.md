---
type: cfa-itemset
topic: "Economics"
topic_code: "02"
topic_slug: "02-Economics"
lm: 1
title: "Lindenhof Macro Rand Carry Post-Mortem"
los: [los-02-01-h, los-02-01-i, los-02-01-j, los-02-01-k]
difficulty: 3
minutes: 12
source: mock-05
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/economics]
---

# Lindenhof Macro Rand Carry Post-Mortem

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Lindenhof Macro is a Frankfurt-based hedge fund that reports in euros (EUR).
One year ago, portfolio manager Johanna Richter opened a carry trade that borrowed EUR for one year and invested the proceeds in one-year South African rand (ZAR) deposits.
The position was unwound today, and Richter has asked analyst Thabo Nkosi to prepare a post-mortem for the investment committee.
The fund's systems carry no direct ZAR/EUR history, so Nkosi must work from the dealer rates in Exhibit 1.

**Exhibit 1: Spot Rates (mid-market)**

| Currency pair | At initiation | Today (unwind) |
|---|---|---|
| ZAR/USD | 17.85 | 19.62 |
| USD/EUR | 1.0820 | 1.1040 |
| JPY/USD | 149.30 | 142.10 |

**Exhibit 2: One-Year Deposit Rates at Initiation**

| Currency | Rate |
|---|---|
| ZAR | 8.25% |
| USD | 5.05% |
| EUR | 3.40% |
| JPY | 0.20% |

For nine months the trade performed as expected, and the rand strengthened modestly against the euro.
In the final quarter, a spike in global volatility triggered a rush of leveraged investors out of high-yield currencies, and the rand fell sharply before the position could be closed.

Nkosi also assembles the South African balance of payments data in Exhibit 3.

**Exhibit 3: South Africa, Selected External Accounts (% of GDP)**

| Item | Prior year | Holding year |
|---|---|---|
| Current account balance | -1.6% | -3.9% |
| Net foreign portfolio inflows | +2.1% | +5.4% |
| External debt | 41% | 44% |

Most of the portfolio inflows went into rand-denominated government bonds.
In a draft of the post-mortem, Nkosi writes: "The rand strengthened during the first nine months even though the current account deficit more than doubled, which shows that the current account has no bearing on the value of the rand."
Richter asks him to replace that sentence with an explanation that is consistent with the curriculum's view of how balance of payments flows affect exchange rates.

Richter also wants a long-run fair value estimate before she decides whether to re-enter the trade.
A 2014 study commissioned by the fund concluded that the rand was at its purchasing power parity value against the euro in 2014, at ZAR/EUR 14.40.
Since then, the South African consumer price index has risen from 100.0 to 162.8, and the euro area index has risen from 100.0 to 128.6.
Nkosi is asked to express the rand's misvaluation today as the percentage by which its market value in EUR differs from its PPP value in EUR.

Finally, two policy announcements were made this morning.
The European Central Bank cut its policy rate by 50 basis points, while euro area finance ministers committed to a joint programme of fiscal consolidation.
The South African Reserve Bank raised its repo rate by 75 basis points, while the South African Treasury announced a multi-year infrastructure programme financed by government bond issuance.
Nkosi notes that both economies have floating exchange rates and allow capital to move freely.
Richter asks for the most likely short-run effect of the two sets of announcements on the ZAR/EUR rate.
She adds that she will consider the long-run implications of South Africa's rising debt separately.

## Questions

1. The realized all-in return on the EUR-funded rand carry trade, net of the funding cost, is closest to: (LOS: los-02-01-i)
   - A. -3.48%.
   - B. -4.92%.
   - C. -6.88%.
2. Based on relative purchasing power parity, the rand today is best described as: (LOS: los-02-01-h)
   - A. undervalued by about 15.8%.
   - B. undervalued by about 10.8%.
   - C. overvalued by about 18.8%.
3. The explanation that Nkosi should most appropriately substitute for the sentence in his draft is that: (LOS: los-02-01-j)
   - A. a current account deficit raises the demand for the deficit country's currency, so the rand's strength was the expected result of the wider deficit.
   - B. investment and financing flows dominate in the short run because asset prices adjust quickly, while a persistent deficit weighs on the rand mainly over the long run.
   - C. rising external debt raises the market's estimate of a deficit country's long-run equilibrium exchange rate, which supported the rand during the first nine months.
4. Under the Mundell-Fleming model, the most likely short-run effect of this morning's announcements on the ZAR/EUR rate is that it will: (LOS: los-02-01-k)
   - A. rise.
   - B. fall.
   - C. move in an indeterminate direction.

## Answer key

> [!success]- Answers and reasoning
> 1. **C.** Build ZAR/EUR $= (\text{ZAR/USD}) \times (\text{USD/EUR})$ so that the USD cancels: initiation $17.85 \times 1.0820 = 19.3137$; today $19.62 \times 1.1040 = 21.6605$ (Python: 21.66048) (V2 p.40).
> The rand's price in EUR is $1/19.3137$ at initiation and $1/21.6605$ today, so the gross return in EUR $= \dfrac{1/21.6605}{1/19.3137} \times 1.0825 - 1 = 19.3137 \times 1.0825/21.6605 - 1 = -3.4782\%$.
> Net of the 3.40% EUR funding cost: $-3.4782\% - 3.40\% = -6.8782\% \approx -6.88\%$.
> Check on EUR 1,000,000: buy ZAR 19,313,700, grow it to ZAR 20,907,080.25, convert back to EUR 965,217.77, and repay EUR 1,034,000, a loss of EUR 68,782.23.
> The rand fell $19.3137/21.6605 - 1 = -10.83\%$ against the euro, more than the 4.85% yield spread, which is the crash risk that gives carry returns their negative skew (V2 p.38, p.39).
> A is wrong because it is the gross return and forgets to subtract the EUR funding cost.
> B is wrong because it runs the trade through the ZAR/USD rate alone, $17.85 \times 1.0825/19.62 - 1 = -1.5157\%$, less 3.40% gives $-4.9157\%$, ignoring the euro's move against the dollar from 1.0820 to 1.1040.
> 2. **A.** Relative PPP moves the 2014 fair value by the ratio of the price level changes: PPP ZAR/EUR today $= 14.40 \times 162.8/128.6 = 14.40 \times 1.265941 = 18.2295$ (V2 p.30).
> Today's market rate is 21.6605, so one euro buys more rand in the market than PPP warrants and the rand is cheap.
> Market value of the rand in EUR relative to its PPP value $= (1/21.6605)/(1/18.2295) - 1 = 18.2295/21.6605 - 1 = -15.84\%$, an undervaluation of about 15.8%.
> Such deviations are a long-run anchor rather than a short-run signal, since PPP has little explanatory power at a one-year horizon but strong power at five years and beyond (V2 p.31, p.32).
> B is wrong because it adds the cumulative inflation differential instead of taking the ratio of the price indexes: $14.40 \times (1 + 0.628 - 0.286) = 19.3248$, giving $19.3248/21.6605 - 1 = -10.78\%$; the additive approximation drops the cross-product term, which becomes large over a multi-year horizon with high cumulative inflation.
> C is wrong because it computes $21.6605/18.2295 - 1 = +18.82\%$, which is the euro's overvaluation measured on the wrong base, and then reads the higher ZAR/EUR rate as a stronger rand.
> 3. **B.** Persistent current account deficits tend to weaken a currency over the long run, but in the short run the capital account dominates because financial asset prices and portfolio positions adjust almost instantly while goods prices, production, and trade demand respond with long lags (V2 p.40, p.41).
> Net portfolio inflows rising from 2.1% to 5.4% of GDP more than financed the wider 3.9% deficit, which explains the rand's early strength without implying that the current account is irrelevant.
> A is wrong because a current account deficit increases the supply of the deficit country's currency under the flow supply and demand channel, which puts downward, not upward, pressure on the rand.
> C is wrong because under the debt sustainability channel a rising external debt ratio leads markets to revise the deficit country's long-run equilibrium value downward, not upward.
> 4. **B.** Both economies have high capital mobility, so each policy mix works through real interest rates and capital flows (V2 p.49).
> The euro area pairs expansionary monetary policy with restrictive fiscal policy, which lowers real rates and depreciates the EUR.
> South Africa pairs restrictive monetary policy with expansionary fiscal policy, which raises real rates and appreciates the ZAR.
> Both effects push the ZAR/EUR rate, the price of one euro in rand, down, so it falls.
> A is wrong because it reads a stronger rand as a higher ZAR/EUR rate, reversing the quote direction.
> C is wrong because it applies the low capital mobility table, in which mixed monetary and fiscal combinations are indeterminate (V2 p.50); the portfolio balance concern about rising South African debt is a long-run effect that Richter has set aside.

## Distractor design

1. A: forgets the funding cost (gross versus net); B: runs the trade through the ZAR/USD leg only, so the USD does not cancel (wrong cross rate).
2. B: adds the cumulative inflation differential instead of using the price index ratio (wrong formula variant); C: measures the misvaluation on the wrong base and misreads the quote direction (base and sign).
3. A: reverses the flow supply and demand effect of a deficit (sign); C: reverses the debt sustainability effect (sign).
4. A: misreads the direction of the ZAR/EUR quote (quote direction); C: applies the low capital mobility table to open economies (misread exhibit assumption).
