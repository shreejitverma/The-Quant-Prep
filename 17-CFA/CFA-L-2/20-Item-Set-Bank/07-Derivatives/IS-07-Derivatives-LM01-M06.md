---
type: cfa-itemset
topic: "Derivatives"
topic_code: "07"
topic_slug: "07-Derivatives"
lm: 1
title: "Brightwater Endowment: Trimming Equity Beta with a Quarterly Equity Swap"
los: [los-07-01-e, los-07-01-g]
difficulty: 4
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/derivatives]
---

# Brightwater Endowment: Trimming Equity Beta with a Quarterly Equity Swap

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Brightwater Endowment supports a private university and holds a large passive allocation to the Calder 500 equity index.
The investment committee wants to reduce equity exposure for one year without selling shares, which would disrupt a securities lending program.
Omar Siddiqui, CFA, the endowment's director of risk, and Leah Brandt, an investment associate, evaluate the overlay.

A dealer offers a one-year equity swap with quarterly resets on a notional of USD 40,000,000, equal to par.
Brightwater would pay the Calder 500 price return (dividends excluded) and receive a fixed rate.
The dealer states that the fixed rate will equal the rate on a one-year, quarterly-reset plain vanilla interest rate swap priced off today's MRR curve, with settlements at 90, 180, 270, and 360 days.
All rates are add-on rates on an actual/360 basis.

Exhibit 1: MRR spot rates at swap initiation

| Days | 90 | 180 | 270 | 360 |
|---|---|---|---|---|
| MRR | 4.80% | 4.70% | 4.62% | 4.55% |

Brightwater enters the swap at the rate implied by Exhibit 1 when the Calder 500 stands at 5,120.00.
The equity return for each period is measured from the index level at the previous reset.

Exhibit 2: Calder 500 during the first quarter

| Item | Value |
|---|---|
| Index level at initiation | 5,120.00 |
| Index level at the first reset (day 90) | 5,248.64 |
| Dividends paid by index constituents during the quarter, in index points | 14.20 |
| Endowment's internal expected annual equity return | 7.50% |

Brandt must report the net settlement at the first reset to the endowment's custodian.

Two months after the first reset, which is five months after initiation, the Calder 500 trades at 5,195.00.
Three quarterly settlements remain, in 30, 120, and 210 days.

Exhibit 3: MRR spot rates five months after initiation

| Days | 30 | 120 | 210 |
|---|---|---|---|
| MRR | 4.95% | 4.88% | 4.79% |

Siddiqui asks Brandt for the swap's fair value to Brightwater on that date for the endowment's quarterly statements.
He also asks at what Calder 500 level the swap would be worth exactly zero on that date, because the committee wants to know how far the index would have to rise before the overlay shows a loss.
Brandt notes that the fixed leg can be treated as a fixed-rate bond with par equal to the notional, and the equity leg as an equity position that is trued back to the notional at every reset.

## Questions

1. Based on Exhibit 1, the annualized fixed rate on the one-year interest rate swap, and therefore on the equity swap, is closest to: (LOS: los-07-01-e)
   - A. 1.12%.
   - B. 4.48%.
   - C. 5.94%.
2. At the first reset, Brightwater's net settlement on the equity swap is closest to: (LOS: los-07-01-g)
   - A. a payment of USD 557,285.
   - B. a payment of USD 668,222.
   - C. a receipt of USD 785,861.
3. Five months after initiation, the value of the equity swap to Brightwater is closest to: (LOS: los-07-01-g)
   - A. -USD 643,476.
   - B. -USD 351,253.
   - C. USD 643,476.
4. Five months after initiation, the Calder 500 level at which the swap's value to Brightwater would be zero is closest to: (LOS: los-07-01-g)
   - A. 5,150.04.
   - B. 5,248.64.
   - C. 5,279.43.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** PV factors: $1/[1 + 0.0480(90/360)] = 0.988142$, $1/[1 + 0.0470(180/360)] = 0.977040$, $1/[1 + 0.0462(270/360)] = 0.966510$, $1/[1 + 0.0455(360/360)] = 0.956480$, sum 3.888172.
> Periodic rate $= (1 - 0.956480)/3.888172 = 1.1193\%$; annualized $\times 360/90 = 4.4772\%$.
> The equity swap's fixed rate is the same because its fixed leg is replicated by the same fixed-rate bond.
> A is wrong because it reports the quarterly periodic rate without annualizing.
> C is wrong because it drops the final PV factor from the annuity sum, $(1 - 0.956480)/2.931692 \times 4 = 5.9378\%$.
> 2. **A.** The contract pays the price return only, measured over the quarter and never annualized: $R_E = 5{,}248.64/5{,}120.00 - 1 = 2.5125\%$.
> The fixed leg accrues by $AP = 90/360$: $1.1193\%$ per quarter.
> Net to Brightwater, which receives fixed and pays equity: $40{,}000{,}000 \times (0.011193 - 0.025125) = -557{,}285$, a payment.
> B is wrong because it adds the 14.20 points of dividends to the equity return, $R_E = 2.7898\%$, although the contract excludes dividends: $-668{,}222$.
> C is wrong because it nets the full annual fixed rate against a quarterly equity return, $40{,}000{,}000 \times (0.044772 - 0.025125) = +785{,}861$.
> The expected equity return is a decoy.
> 3. **C.** Exhibit 3 PV factors: $1/[1 + 0.0495(30/360)] = 0.995892$, $1/[1 + 0.0488(120/360)] = 0.983994$, $1/[1 + 0.0479(210/360)] = 0.972818$, sum 2.952703.
> Fixed coupon per quarter $= 40{,}000{,}000 \times 0.011193 = 447{,}715$, so $V_{FIX} = 447{,}715 \times 2.952703 + 40{,}000{,}000 \times 0.972818 = 40{,}234{,}684$ (1.005867 per 1 of par).
> The equity leg grows from the first reset, not from initiation: $(5{,}195.00/5{,}248.64) \times 40{,}000{,}000 = 0.989780 \times 40{,}000{,}000 = 39{,}591{,}208$.
> Brightwater receives fixed and pays equity, so $V_{EQ,t} = 40{,}234{,}684 - 39{,}591{,}208 - 0 = +643{,}476$.
> A is wrong because it reports the value to the dealer, which receives the equity return.
> B is wrong because it grows the equity leg from the initiation level, $(5{,}195.00/5{,}120.00) \times 40{,}000{,}000 = 40{,}585{,}938$, giving $-351{,}253$; the leg was trued back to notional at the first reset.
> 4. **C.** Setting $V_{EQ,t} = 0$ requires the equity leg to equal the fixed leg: $(S_t/5{,}248.64) \times 40{,}000{,}000 = 40{,}234{,}684$.
> $S_t = 5{,}248.64 \times 1.005867 = 5{,}279.43$.
> A is wrong because it uses the initiation level as the base, $5{,}120.00 \times 1.005867 = 5{,}150.04$.
> B is wrong because it assumes the fixed leg is worth par between resets and ignores the accrued fixed coupon embedded in $V_{FIX}$.

## Distractor design

1. A: periodic rate not annualized by $1/AP$; C: final PV factor dropped from the annuity sum.
2. B: misread exhibit, dividends added to a price-return contract; C: annual fixed rate not scaled by the accrual period.
3. A: value reported for the wrong party (sign); B: equity leg grown from initiation instead of the last reset.
4. A: initiation level used instead of the last reset level; B: fixed leg assumed to be at par between resets.
