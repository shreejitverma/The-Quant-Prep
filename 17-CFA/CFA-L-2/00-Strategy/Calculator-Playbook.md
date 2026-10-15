---
type: cfa-strategy
tags: [cfa/l2, cfa/strategy, cfa/calculator]
updated: 2026-08-26
---
# Calculator Playbook: BA II Plus for Level II

Source for the general guidance: "Mastering Your Calculator for the CFA Exam" (CFA Institute).
Only the TI BA II Plus (and Professional) and the HP 12C (and Platinum) are permitted; this playbook is for the BA II Plus.
The guide's exam-day rules: bring spare batteries or a backup calculator, clear memory before the exam, set decimals to at least 4 places, and use only functions you have practiced.

## Setup once, check before every session

| Setting | Keys | Target |
|---|---|---|
| Full reset | 2ND, RESET (the +/- key), ENTER | clears all worksheets and memory |
| Decimal places | 2ND, FORMAT (the . key), 9, ENTER | 9 (floating); never round intermediate values |
| Payments per year | 2ND, P/Y (the I/Y key), 1, ENTER | P/Y = 1 and C/Y = 1, so I/Y is the periodic rate you enter |
| Payment timing | 2ND, BGN (the PMT key); 2ND, SET toggles | END for ordinary annuities; BGN only for annuities due, then switch back |
| Chain vs AOS | 2ND, FORMAT, scroll to Chn or AOS | Chn (chain) is the default and is what the keystrokes below assume |
| Clear TVM | 2ND, CLR TVM (the FV key) | before every TVM problem |
| Clear worksheet | 2ND, CLR WORK (the CE/C key) inside CF, BOND, DATA | before every cash flow or statistics problem |

Indicator check: if BGN shows in the display, an annuity-due mode is on.

## Time value of money

Enter N, I/Y, PV, PMT, FV with the correct signs (cash out negative, cash in positive), then CPT the unknown.

| Problem | Keystrokes |
|---|---|
| PV of a growing perpetuity (Gordon growth) | no TVM; compute D1 / (r - g) directly: D1, /, (r - g), = |
| Bond price, semiannual | N = periods, I/Y = yield/2, PMT = coupon/2, FV = 100, CPT PV |
| Yield of a bond | N, PV (negative price), PMT, FV, CPT I/Y, then x 2 for the bond-equivalent yield |
| Implied growth or required return | store known values, CPT I/Y |
| Two-stage DDM | CF worksheet: CF0 = 0, C01..C0n = dividends, last cash flow includes the terminal value, NPV with I = r |

## Cash flow worksheet (NPV, IRR, FCFF and FCFE valuation)

CF, 2ND CLR WORK, CF0 = initial flow, ENTER, down arrow, C01 = flow, ENTER, down arrow, F01 = frequency, ENTER, down arrow, repeat; then NPV, I = rate, ENTER, down arrow, CPT; or IRR, CPT.
Terminal value: add it into the final cash flow before entering.
Mid-year or uneven timing is not supported; convert to period-end flows.

## Spot, forward, and bootstrapping (Fixed Income LM1-LM2, Derivatives LM1)

| Task | Steps |
|---|---|
| Forward rate from two spots | (1 + z2)^2 / (1 + z1) - 1: enter 1 + z2, y^x, 2, /, 1 + z1, =, -, 1, = |
| Discount factor | 1 / (1 + z)^n: 1 + z, y^x, n, =, 1/x |
| Swap fixed rate from discount factors | (1 - DFn) / sum of DFs: compute each DF with 1/x and store in memory STO 1..9, then RCL |
| Binomial tree node value | (0.5 x Vup + 0.5 x Vdown + coupon) / (1 + r): compute the bracket first, then divide |

Memory: STO n stores the display in memory n (0-9); RCL n recalls; 2ND, MEM shows all.

## Statistics worksheet (Quant)

2ND, DATA, 2ND CLR WORK, enter X01, Y01 pairs (down arrow between); then 2ND, STAT, 2ND SET to choose LIN (linear regression) or 1-V (one variable); scroll for n, mean, sample standard deviation (Sx), population (sigma x), a (intercept), b (slope), r (correlation).
Use for quick simple regression checks and standard deviations; multiple regression is never computed on the exam, only interpreted from output.

## Bond worksheet (only when dates are given)

2ND, BOND: SDT (settlement date as MM.DDYY), CPN (annual coupon rate), RDT (redemption date), RV = 100, ACT or 360, 2/Y or 1/Y, YLD or PRI, CPT the other.
Level II rarely needs it; the spot-rate and tree methods above are more common.

## Interest conversion

2ND, ICONV: NOM (nominal), C/Y, CPT EFF, or the reverse.
Use for continuous vs annual comparisons only if the vignette mixes conventions; most Level II problems state the periodicity.

## Common mode errors and the symptom they produce

| Error | Symptom |
|---|---|
| P/Y left at 12 | TVM answers wildly off; I/Y was divided by 12 |
| BGN mode on | PV and PMT answers off by one period's interest |
| Decimals at 2 | rounding errors on multi-step problems, especially forward rates and trees |
| Sign convention mixed | CPT gives "Error 5" (no solution) or a negative rate |
| Forgetting CLR TVM | a leftover FV or PMT from the previous problem contaminates the answer |
| Entering the annual yield with semiannual periods | price too low; halve the yield and double the periods |

## Drill

Every formula card in the Slides decks under `70-Slides/` shows the keystroke sequence on its answer slide; run each deck against the clock in the final week.

Related: [[Distinction-Strategy]], [[Exam-Day-Playbook]].
