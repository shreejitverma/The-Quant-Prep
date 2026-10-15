---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 5
title: "Residual Income Valuation"
pages: "337-403"
weight_band: "10-15%"
difficulty: 3
los_count: 11
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM5: Residual Income Valuation

Difficulty 3 of 5: the algebra is light (book value plus a discounted stream), but the item sets hinge on three places where a candidate under time pressure picks the wrong denominator: the persistence factor formula, the two ways to compute the equity charge, and the clean surplus adjustment.

## LOS map

- **calculate** and interpret residual income, economic value added, and market value added (V5 p.337) ^los-05-05-a
    - Examiner asks: given total assets, a debt weight, a pretax cost of debt, a tax rate, a cost of equity and EBIT, compute net income minus the equity charge, or NOPAT minus the total capital charge, and confirm the two agree; compute EVA as NOPAT less WACC times total capital and MVA as market value of the company less book value of total capital.
- **describe** the uses of residual income models (V5 p.337) ^los-05-05-b
    - Examiner asks: which of equity valuation, internal performance measurement and executive compensation the commercial implementations are marketed for, and whether a positive RI company should sell above or below book value.
- **calculate** the intrinsic value of a common stock using the residual income model and compare value recognition in residual income and other present value models (V5 p.337) ^los-05-05-c
    - Examiner asks: build the book value roll-forward from EPS and DPS, compute each year's RI, discount, add B0, then show the DDM gives the same number while the RI model books most of the value in B0 rather than in the terminal year.
- **explain** fundamental determinants of residual income (V5 p.337) ^los-05-05-d
    - Examiner asks: identify book value and ROE relative to r as the drivers, and state that when ROE equals r the value equals book value.
- **explain** the relation between residual income valuation and the justified price-to-book ratio based on forecasted fundamentals (V5 p.337) ^los-05-05-e
    - Examiner asks: compute justified P/B as (ROE - g)/(r - g) or 1 + (ROE - r)/(r - g) and link P/B above one to positive expected RI.
- **calculate** and interpret the intrinsic value of a common stock using single-stage (constant-growth) and multistage residual income models (V5 p.337) ^los-05-05-f
    - Examiner asks: V0 = B0 + (ROE - r)B0/(r - g) from four inputs, or a three-year explicit stage plus a terminal term based on a P/B premium, a perpetuity of the final RI, or a persistence factor, then compare with price.
- **calculate** the implied growth rate in residual income, given the market price-to-book ratio and an estimate of the required rate of return on equity (V5 p.337) ^los-05-05-g
    - Examiner asks: back B0 out of price and P/B, then solve the single-stage model for g, or solve for the ROE that justifies the market P/B.
- **explain** continuing residual income and justify an estimate of continuing residual income at the forecast horizon, given company and industry prospects (V5 p.337) ^los-05-05-h
    - Examiner asks: match a company description (low payout, strong market leadership, extreme accruals) to a higher or lower persistence factor and state the direction of the effect on value.
- **compare** residual income models to dividend discount and free cash flow models (V5 p.337) ^los-05-05-i
    - Examiner asks: which model recognizes value earliest, why terminal value is a smaller share of value under RI, and why consistent assumptions make all three agree.
- **explain** strengths and weaknesses of residual income models and justify the selection of a residual income model to value a company's common stock (V5 p.337) ^los-05-05-j
    - Examiner asks: pick the statement that is a genuine strength or weakness, and choose RI over DDM or FCF for a firm with unpredictable dividends, negative near-term FCF or an uncertain terminal value.
- **describe** accounting issues in applying residual income models (V5 p.337) ^los-05-05-k
    - Examiner asks: what to do with a restructuring charge, persistent negative OCI, capitalized expenditures, operating leases or an unrecognized brand, and whether the adjustment hits book value, net income, or neither.

## Core intuition

An income statement charges for one kind of capital and not the other.
Interest expense is deducted before net income, so debtholders are paid inside the accounts; equity holders are never charged, the statement simply hands them whatever is left and lets them decide whether it was enough (V5 p.338).
Residual income fixes that omission by deducting an explicit rent on the equity capital, the equity charge, equal to the book value of equity times the required return on equity (V5 p.339).
A company with positive net income and negative residual income is profitable in an accounting sense and unprofitable in an economic sense: it earned something, but less than its owners could have earned elsewhere at the same risk (V5 p.339).
The idea is old (Marshall in 1890, General Motors in the 1920s) and travels under many names: economic profit, abnormal earnings, discounted abnormal earnings, the Edwards-Bell-Ohlson model, and the trademarked EVA (V5 p.338, p.341).

> [!abstract] Idea 1: value equals book value plus the present value of everything the firm earns above its cost of equity
> If a company earned exactly its cost of equity forever, its shares would be worth exactly book value, because every euro of equity earns exactly the rent investors demand.
> Anything above that is residual income, and the present value of the residual income stream is the premium over book value.
> Anything below it is a discount to book value.
> That is the whole model: $V_0 = B_0 + \sum PV(RI_t)$ (V5 p.343, p.346).

### Two ways to compute the same residual income

The equity route starts at net income and subtracts the equity charge $r \times$ equity (V5 p.339).
The capital route starts one line higher, at net operating profit after taxes (NOPAT, or EBIT times one minus the tax rate), and subtracts a charge for all capital: the equity charge plus the after-tax cost of debt times debt (V5 p.340).
The two agree when the after-tax interest inside net income equals the after-tax debt charge inside the capital charge, and when the weights come from book values of debt and equity (V5 p.340).
The reconciliation is worth seeing once: net income plus after-tax interest equals NOPAT; equity charge plus after-tax debt charge equals the total capital charge; so NOPAT less the total capital charge equals net income less the equity charge (V5 p.340).
A third framing compares rates instead of money: residual income equals (ROIC less the effective capital charge rate) times beginning capital, where ROIC is NOPAT over total capital (V5 p.340).
AXCI earned 7% on its capital against an effective charge of 8.45%, so it destroyed 1.45% of EUR 2 million, or EUR 29,000, regardless of which route you take (V5 p.340).

The commercial implementation EVA is NOPAT less the cost of capital times total capital, computed after a proprietary list of adjustments: capitalize and amortize R&D, suspend the capital charge on strategic investments, replace deferred taxes with cash taxes, add the LIFO reserve back to capital, treat operating leases as capital leases, and strip nonrecurring items (V5 p.341, p.342).
Market value added is the market value of the company less the accounting book value of total capital; a firm that keeps generating economic profit should build up positive MVA (V5 p.342).
The research on whether value-added measures explain returns better than ROE or earnings growth is mixed, and the commercial products are sold mostly for internal performance measurement and executive pay rather than for equity valuation (V5 p.342).

### Why the model works: clean surplus turns dividends into earnings and book value

The residual income model is not a competing theory of value; it is the dividend discount model rewritten (V5 p.346).
The clean surplus relation says ending book value equals beginning book value plus earnings minus dividends, provided nothing else touches equity except transactions with owners (V5 p.346).
Rearranged, each dividend is $D_t = E_t + B_{t-1} - B_t$.
Substitute that into the DDM and the book value terms telescope: every $B_{t-1}/(1+r)^{t}$ pairs with the $B_{t-1}/(1+r)^{t-1}$ from the previous period, leaving $B_0$ at the front and $E_t - rB_{t-1}$ in every numerator (V5 p.346).
That numerator is residual income, so $V_0 = B_0 + \sum RI_t/(1+r)^t$ is the DDM in a different order of recognition.
Because $E_t = ROE_t \times B_{t-1}$, the same sum can be written with $(ROE_t - r)B_{t-1}$ in the numerator, which exposes the two fundamental drivers: how much book capital the firm has and how far its return on that capital sits above the cost of equity (V5 p.346, p.347).
ROE here is measured on beginning book value, not the average that financial statement analysis uses (V5 p.347).

> [!abstract] Idea 2: the RI model recognizes value early, so the terminal value matters less
> In Example 3 the RI model books 6.00 of an 11.15 value in $B_0$ at time zero, while the DDM books 9.20 of it in the year 3 liquidating dividend (V5 p.346).
> In the perpetuity of Example 12, book value is 60% of value under RI, while the first five dividends deliver only 38% under the DDM (V5 p.360).
> The practical consequence is that RI valuations are less sensitive to the terminal value that dominates DDM and FCF valuations, and in some settings the terminal value can be set to zero (V5 p.353, p.361).

### Single-stage model and the justified P/B

If ROE and growth are constant, residual income grows at $g = b \times ROE$ and the sum collapses to a Gordon-style perpetuity: $V_0 = B_0 + (ROE - r)B_0/(r - g)$ (V5 p.350).
Divide by $B_0$ and you have the justified P/B, $1 + (ROE - r)/(r - g)$, which is algebraically the same as $(ROE - g)/(r - g)$ from the discounted dividend module (V5 p.350).
Three readings follow immediately.
ROE above r means P/B above one and value above book; ROE equal to r means value equals book; ROE below r means a discount to book, and if the shortfall has no prospect of ending, liquidation and redeployment of the assets may be the right answer (V5 p.352).
Philips at ROE 12%, r 8.5% and g 6.75% is worth 3 times book (13.22 becomes 39.66), and putting the market price of 35.40 into the same equation and solving for g gives the market-implied growth of 6.41% (V5 p.352).
Tobin's q is a cousin of P/B that uses the market value of debt plus equity over the replacement cost of total assets; it is theoretically appealing because replacement cost reflects inflation, but replacement costs are rarely observable (V5 p.350, p.351).

The single-stage model assumes the excess of ROE over r lasts forever.
Competition says otherwise: abnormally high ROE attracts entrants and abnormally low ROE drives exits, so ROE mean-reverts and residual income tends toward zero (V5 p.352).
That is the economic reason the multistage models exist.

### Continuing residual income: four assumptions and one trap

A multistage model forecasts residual income explicitly to horizon T and then needs a view on continuing residual income, the residual income after the horizon (V5 p.352).
The curriculum lists four standard assumptions: residual income continues indefinitely at a positive level, it drops to zero immediately after the terminal year, it declines to zero as ROE reverts to r, or it declines to some long-run mean level (V5 p.353, p.378).
Each maps to a terminal term.
A premium over book value at T, $(P_T - B_T)/(1+r)^T$, comes from any price model, for example a P/B multiple (V5 p.353, p.357).
A perpetuity of the final-year residual income, $RI_T/r$, is the Lee and Swaminathan choice and assumes growth after T is value-neutral (V5 p.354, p.355).
Zero means the horizon is long enough that ROE has already converged to r, which is the Zenlandia base case (V5 p.354).
The Dechow, Hutton and Sloan persistence model sits between: residual income decays geometrically at $\omega$ per year, and the terminal term is $RI_T/[(1 + r - \omega)(1+r)^{T-1}]$ (V5 p.355, p.356).

> [!abstract] Idea 3: omega is the fraction that survives, not the fraction that disappears
> $\omega = 1$ means residual income never fades and the terminal term is a plain perpetuity.
> $\omega = 0$ means residual income stops after the horizon and the terminal term is zero.
> $\omega = 0.62$, the Dechow et al. sample average, means residual income decays at 38% a year (V5 p.356).
> Higher $\omega$ always means a higher value.
> Lower persistence goes with extreme ROE, extreme special items and extreme accruals; higher persistence goes with low dividend payout, strong market leadership and high historical persistence in the industry (V5 p.356).

Note the indices in the persistence formula: the explicit sum runs to T - 1 and the terminal term uses $RI_T$ discounted by $(1+r)^{T-1}$, because the term $RI_T/(1 + r - \omega)$ is the value at T - 1 of the whole decaying stream starting with $RI_T$ (V5 p.355).
When $\omega = 1$ it reduces to $RI_T/[r(1+r)^{T-1}]$, which is exactly a perpetuity of $RI_T$ beginning at T, so the two conventions the curriculum uses (RI_T in the explicit stage plus $RI_T/r$ discounted T periods, or RI_T outside the explicit stage discounted as above) give the same number (V5 p.355, p.397).

### When to choose the RI model

RI models are strongest where the alternatives are weakest: no dividends or unpredictable dividends, negative near-term free cash flow, or a terminal value that cannot be forecast with confidence (V5 p.361).
They use accounting data that already exists, focus on economic profitability, and shift value recognition forward (V5 p.361).
Their weaknesses are the mirror image: the inputs are accounting numbers that management can manage, may need heavy adjustment, depend on the clean surplus relation holding or being repaired, and assume interest expense fairly reflects the cost of debt (V5 p.361).
They are least appropriate when clean surplus violations are large or when book value and ROE are not predictable (V5 p.362).
With fully consistent pro forma statements and the same required return, RI, DDM and FCFE give the same value; in practice they diverge because analysts cannot forecast each input equally well, which makes the RI model a consistency check on the others (V5 p.362).

### Accounting issues

Bauman's argument for why accounting choices should not matter is elegant: aggressive accounting raises today's book value and lowers future earnings by exactly offsetting present values, provided clean surplus holds (V5 p.362).
The argument fails in practice for two reasons: clean surplus does not hold, and analysts extrapolate historical earnings and ROE (V5 p.363).
Capitalizing a 50,000 expenditure instead of expensing it lifts ROE from 20% to 23.81% today; if that ROE is carried forward the model overvalues the firm, and for a growing company the overstatement can persist (V5 p.363).

Clean surplus violations are items that hit equity directly through other comprehensive income: unrealized fair value changes on certain financial instruments, foreign currency translation adjustments, some pension adjustments, part of the gains and losses on hedging instruments, and under IFRS only, revaluation surplus on PP&E and intangibles and own-credit-risk changes on certain liabilities (V5 p.364).
Book value is stated correctly because accumulated OCI sits in equity; net income, and therefore any ROE forecast built from it, is not (V5 p.364).
Frankel and Lee showed that bias arises only when the expected clean surplus violations do not net to zero, so the analyst's job is to examine the statement of changes in equity and judge whether the items will reverse (V5 p.364).
Nokia's translation differences of EUR 341 million and SAP's other components of equity of EUR 887 million were positive in 2018; if that trend persists, historical ROE understates future ROE and an upward adjustment is warranted, but exchange rates may reverse (V5 p.365, p.368).
Exhibit 13 shows the mechanical consequence: three forecasts with the same 12% ROE assumption produce residual income growth of 12%, 2.2% or 21.8% depending on the OCI assumed, and only the no-OCI forecast makes growth equal ROE times retention (V5 p.368, p.369).
Example 14 shows that the residual income model reproduces the DDM value only when OCI is included in the residual income, and that growth in residual income generally differs from growth in net income (V5 p.370, p.371, p.372).
Historical ROE should be computed at the aggregate level, net income over shareholders' equity, because buybacks and issuance distort per-share ROE (V5 p.364).

Book value itself may need repair for off-balance-sheet items and fair values: operating leases (which do not change equity but affect earnings forecasts), LIFO inventory, deferred taxes, reserves and allowances, and intangibles (V5 p.372).
Identifiable, separable intangibles belong in book value and are amortized if finite-lived, but most internally generated intangibles such as brands are never recognized (V5 p.372, p.373).
The Alpha and Beta example makes the point sharply: two firms worth 7,500 combined appear worth 7,000 after a fair-value cash acquisition, because amortizing the acquired license lowers ROE; adding the amortization back restores 7,500, and paying with shares changes book value and ROE in offsetting ways so the total is still 7,500 (V5 p.373, p.374).
Lundholm and Sloan generalize this: adding an omitted asset to book value and then amortizing it has no net effect on RI value, since the higher B0 is offset by the present value of future amortization plus the capital charge on the asset (V5 p.375).
R&D is expensed under US GAAP outside certain software cases and can be capitalized in part under IFRS; expensing lowers ROE now and raises it slightly later, and for a mature firm ROE already reflects R&D productivity without adjustment (V5 p.374, p.375).
Nonrecurring items (unusual items, US GAAP extraordinary items, restructuring charges, discontinued operations, accounting changes) must be removed from the earnings used to forecast residual income, but book value needs no adjustment because the gains and losses are already in the assets in place (V5 p.375).
Other aggressive practices, accelerating revenue, deferring expenses, and cookie jar reserves, inflate both earnings and book value and demand a judgment on management integrity (V5 p.375, p.376).
Internationally, Frankel and Lee found a plain RI model explained 70% of cross-sectional price variation across 20 countries, and named reliable earnings forecasts, systematic clean surplus violations and poor-quality accounting rules that delay recognition as the three considerations; where those fail, use a model less dependent on accounting data such as FCFE (V5 p.376).

## Formulas and derivations

**Residual income, equity charge approach** (V5 p.339)
$$
RI_t = NI_t - r \times B_{t-1}, \qquad \text{Equity charge} = r \times B_{t-1}
$$
^f-05-05-1

- $NI_t$: net income available to common shareholders (deduct preferred dividends first); $r$: required return on equity; $B_{t-1}$: beginning book value of common equity.
- Interest is already inside $NI$, so only the equity rent remains to be charged; a positive $NI$ with negative $RI$ is accounting profit without economic profit (V5 p.339).
- AXCI: $91{,}000 - 0.12 \times 1{,}000{,}000 = -29{,}000$ (V5 p.339).

**Residual income, capital charge approach** (V5 p.340)
$$
RI_t = NOPAT_t - \left[r \times B_{t-1} + r_d(1 - t) \times D_{t-1}\right] = (ROIC - \text{effective capital charge}) \times \text{Beginning capital}
$$
^f-05-05-2

- $NOPAT = EBIT(1 - t)$; $r_d$: pretax cost of debt; $D$: book value of debt; $ROIC = NOPAT / \text{total capital}$; effective capital charge $=$ total capital charge / total capital.
- Equals Formula 1 when the after-tax interest in net income equals the after-tax debt charge and the weights are book weights (V5 p.340).
- Reconciliation: $NI + r_d(1-t)D = NOPAT$ and equity charge $+ r_d(1-t)D =$ capital charge, so the differences match (V5 p.340).
- AXCI: $140{,}000 - (120{,}000 + 49{,}000) = -29{,}000$; or $(0.07 - 0.0845) \times 2{,}000{,}000 = -29{,}000$ (V5 p.340).

> [!tip] Calculator
> Practice Problem 1 in one pass: `300000 - 2000000 × 0.06 =` gives 180,000; `× 0.6 =` gives 108,000; `- 1000000 × 0.10 =` gives 8,000.

**Economic value added** (V5 p.341)
$$
EVA = NOPAT - (C\% \times TC)
$$
^f-05-05-3

- $C\%$: cost of capital (WACC); $TC$: total capital, both after the Stern Stewart adjustments (capitalized R&D, cash taxes, LIFO reserve, operating leases as capital leases, nonrecurring items) (V5 p.342).
- It is Formula 2 with a branded set of adjustments, so in general it gives a different number from the simple calculation (V5 p.342).
- Practice Problem 4: $100 - 0.11 \times (200 + 300) = 45$ (V5 p.393).

**Market value added** (V5 p.342)
$$
MVA = \text{Market value of the company} - \text{Accounting book value of total capital}
$$
^f-05-05-4

- Market value of the company $=$ market value of debt $+$ market value of equity (price times shares); book value of total capital is debt plus equity at book.
- A company that generates positive economic profit over time should have positive MVA (V5 p.342).
- Practice Problem 9: $55 + 30 \times 25.43 - 650 = 167.9$ million rand (V5 p.393).

**Per-share residual income** (V5 p.343, p.347)
$$
RI_t = E_t - r B_{t-1} = (ROE_t - r) \times B_{t-1}
$$
^f-05-05-5

- $E_t$: EPS for period $t$; $B_{t-1}$: beginning book value per share; $ROE_t = E_t / B_{t-1}$ on beginning book value, not average (V5 p.347).
- The second form holds because $E_t = ROE_t \times B_{t-1}$ by definition; it exposes the two drivers, book value and the spread of ROE over $r$ (V5 p.346).
- CNR 2019: $6.23 - 0.094 \times 24.32 = 6.23 - 2.29 = 3.94$ (V5 p.344).

**Clean surplus relation** (V5 p.346)
$$
B_t = B_{t-1} + E_t - D_t \quad \Longleftrightarrow \quad D_t = E_t + B_{t-1} - B_t
$$
^f-05-05-6

- Holds when earnings capture every change in equity other than owner transactions (issuance, buybacks, dividends).
- Violated when items go straight to equity through OCI; then comprehensive income $= NI + OCI$ is what satisfies the relation (V5 p.350, p.364).
- This is the identity that lets the DDM be rewritten as the RI model; without it, or without an OCI adjustment, the two models disagree (V5 p.346, p.371).

**General residual income model** (V5 p.343, p.346)
$$
V_0 = B_0 + \sum_{t=1}^{\infty} \frac{RI_t}{(1+r)^t} = B_0 + \sum_{t=1}^{\infty} \frac{E_t - rB_{t-1}}{(1+r)^t} = B_0 + \sum_{t=1}^{\infty} \frac{(ROE_t - r)B_{t-1}}{(1+r)^t}
$$
^f-05-05-7

- $V_0$: intrinsic value per share today; $B_0$: current book value per share; all three forms are identical given Formula 5.
- Derivation: start from $V_0 = \sum D_t/(1+r)^t$, substitute $D_t = E_t + B_{t-1} - B_t$ from Formula 6, and note that $-B_t/(1+r)^t + B_t/(1+r)^{t+1} = -rB_t/(1+r)^{t+1}$; the book values telescope to leave $B_0$ plus $\sum (E_t - rB_{t-1})/(1+r)^t$ (V5 p.346).
- Value exceeds book value exactly when the present value of expected residual income is positive (V5 p.346).
- Bugg: $6.00 + 1.40/1.10 + 1.80/1.10^2 + 3.175/1.10^3 = 11.15$, identical to the DDM (V5 p.345).

> [!tip] Calculator
> Put book value in as the time-zero flow: `CF` `2nd CLR WORK`, `CF0 = 6`, `C01 = 1.40`, `C02 = 1.80`, `C03 = 3.175`, `NPV` `I = 10` `CPT` gives 11.15.
> For a terminal premium or perpetuity, add it into the last cash flow before computing NPV.

**No-growth check: RI and DDM agree on a perpetuity** (V5 p.341, p.360)
$$
V_0 = B_0 + \frac{E - rB_0}{r} = \frac{E}{r}
$$
^f-05-05-8

- Applies when all earnings are paid out so book value is constant and $RI = E - rB_0$ is a level perpetuity.
- $B_0 + E/r - B_0 = E/r$, which is the no-growth DDM; the split of value differs (book value first, then RI) but the total does not (V5 p.360).
- AXCI: $0.91/0.12 = 7.58$ per share, so $P/B = 0.758$; Example 12: $6 + 0.40/0.10 = 10 = 1.00/0.10$ (V5 p.341, p.360).

**Justified price-to-book from fundamentals** (V5 p.350)
$$
\frac{P_0}{B_0} = \frac{ROE - g}{r - g} = 1 + \frac{ROE - r}{r - g}
$$
^f-05-05-9

- $g = b \times ROE$, the sustainable growth rate, with $b$ the retention ratio; requires constant ROE and growth and $r > g$.
- Derivation: Gordon model with $D_1 = (1-b)ROE \times B_0$ gives $P_0/B_0 = (1-b)ROE/(r-g)$; substitute $(1-b)ROE = ROE - g$; then $(ROE - g)/(r-g) = [(r - g) + (ROE - r)]/(r - g) = 1 + (ROE - r)/(r - g)$ (V5 p.350).
- P/B above one if and only if $ROE > r$, which is the same condition as positive residual income (V5 p.378).
- Practice Problem 28: $(0.15 - 0.03)/(0.12 - 0.03) = 1.33$ (V5 p.398).

**Single-stage (constant-growth) residual income model** (V5 p.350)
$$
V_0 = B_0 + \frac{ROE - r}{r - g} B_0
$$
^f-05-05-10

- The second term is the present value of a residual income stream that starts at $(ROE - r)B_0$ and grows at $g$: $RI_1/(r - g)$ with $RI_1 = (ROE - r)B_0$ (V5 p.350).
- Multiply Formula 9 by $B_0$ to get it, so justified price and single-stage RI value are the same number.
- ROE equal to $r$ gives $V_0 = B_0$; ROE below $r$ gives a discount to book (V5 p.352).
- Philips: $13.22 + (0.12 - 0.085)/(0.085 - 0.0675) \times 13.22 = 13.22 + 2 \times 13.22 = 39.66$ (V5 p.352).

> [!tip] Calculator
> `0.12 - 0.085 =` store; `0.085 - 0.0675 =` store; divide the first by the second (2.0); `× 13.22 + 13.22 =` gives 39.66.

**Implied growth and implied ROE from the market P/B** (V5 p.352, p.401)
$$
g = r - \frac{(ROE - r)B_0}{P_0 - B_0}, \qquad ROE = r + \left(\frac{P_0}{B_0} - 1\right)(r - g)
$$
^f-05-05-11

- Both are Formula 10 solved for a different unknown; $B_0$ may have to be recovered as price divided by P/B (V5 p.396).
- Derivation of $g$: $P_0 - B_0 = (ROE - r)B_0/(r - g)$, so $r - g = (ROE - r)B_0/(P_0 - B_0)$.
- Philips: $g = 0.085 - 0.035 \times 13.22/(35.40 - 13.22) = 0.0641$ (V5 p.352); Thales: $ROE = 0.082 + 2.68 \times 0.027 = 0.1544$ (V5 p.401).

**Tobin's q** (V5 p.350)
$$
q = \frac{\text{Market value of debt and equity}}{\text{Replacement cost of total assets}}
$$
^f-05-05-12

- Differs from P/B in the numerator (total capital, not equity), the denominator (total assets, not equity) and the measurement basis (replacement cost, which reflects inflation, not historical cost) (V5 p.351).
- Tobin argued $q$ averages to one across companies because economic rents average to zero; the practical obstacle is that replacement costs are rarely available (V5 p.351).

**Finite-horizon RI model with a terminal premium over book value** (V5 p.353)
$$
V_0 = B_0 + \sum_{t=1}^{T} \frac{E_t - rB_{t-1}}{(1+r)^t} + \frac{P_T - B_T}{(1+r)^T} = B_0 + \sum_{t=1}^{T} \frac{(ROE_t - r)B_{t-1}}{(1+r)^t} + \frac{P_T - B_T}{(1+r)^T}
$$
^f-05-05-13

- $P_T$: expected price at the horizon from any model (P/B multiple, P/E multiple, DDM); $B_T$: forecast book value at $T$; $P_T - B_T$ is the premium over book value.
- Why it holds: the value at $T$ of all residual income after $T$ is $P_T - B_T$ by Formula 7 applied at time $T$, so discounting that premium captures the continuing stage (V5 p.353).
- Long horizons let the analyst set the premium to zero because ROE will have converged to $r$ (V5 p.353).
- URS: $15 + 17.755 + (1.8 - 1) \times 39.475/1.0795^6 = 15 + 17.755 + 19.956 = 52.71$ (V5 p.358).

**Continuing residual income with a persistence factor** (V5 p.355)
$$
V_0 = B_0 + \sum_{t=1}^{T-1} \frac{E_t - rB_{t-1}}{(1+r)^t} + \frac{E_T - rB_{T-1}}{(1 + r - \omega)(1+r)^{T-1}}
$$
^f-05-05-14

- $\omega$: persistence factor, $0 \le \omega \le 1$; the explicit sum stops at $T - 1$ and the terminal term uses $RI_T$ discounted $T - 1$ periods.
- Derivation: assume $RI_{T+k} = \omega^k RI_T$; the value at $T-1$ is $\sum_{k \ge 0} \omega^k RI_T/(1+r)^{k+1} = \frac{RI_T}{1+r} \cdot \frac{1}{1 - \omega/(1+r)} = \frac{RI_T}{1 + r - \omega}$; discount that $T - 1$ periods.
- $\omega = 1$ gives $RI_T/[r(1+r)^{T-1}]$, a perpetuity of $RI_T$; $\omega = 0$ gives $RI_T/(1+r)^T$, a single final flow; Dechow et al. found $\omega = 0.62$, a 38% annual decay (V5 p.356).
- Zenlandia with $\omega = 0.60$, $T = 20$: $23.8664/[(1.12 - 0.60) \times 1.12^{19}] = 5.33$ (V5 p.356); TTCI with $\omega = 1$: $3.47/(0.087 \times 1.087^2) = 33.78$ (V5 p.397).

> [!tip] Calculator
> Zenlandia terminal term: `1.12 y^x 19 =` gives 8.6128; `× 0.52 =` gives 4.4786; `23.8664 ÷ 4.4786 =` gives 5.33.

**Four continuing-RI cases at the horizon** (V5 p.353, p.355, p.378)
$$
PV(\text{continuing RI}) =
\begin{cases}
\dfrac{RI_T}{r\,(1+r)^{T-1}} & \text{RI persists at the terminal level } (\omega = 1) \\[8pt]
\dfrac{RI_T}{(1 + r - \omega)(1+r)^{T-1}} & \text{RI fades toward zero } (0 < \omega < 1) \\[8pt]
\dfrac{RI_T}{(1+r)^{T}} & \text{RI drops to zero immediately after } T \ (\omega = 0) \\[8pt]
\dfrac{P_T - B_T}{(1+r)^T} & \text{premium over book value from a price forecast}
\end{cases}
$$
^f-05-05-15

- The first three are Formula 14 at its two limits and in between; the fourth is Formula 13.
- "Declines to zero as ROE reverts to r" is usually implemented by extending the explicit forecast until ROE equals $r$ and then using zero (Alphabet, Zenlandia base case) (V5 p.348, p.354).
- Ordering of value: perpetuity $>$ fading $>$ zero, holding the explicit stage fixed; a higher $\omega$ always raises value (V5 p.356).

**Growth of residual income under constant ROE and payout** (V5 p.350, p.400)
$$
g = b \times ROE, \qquad RI_{t+1} = RI_t (1 + g) \text{ only when ROE, payout and clean surplus all hold}
$$
^f-05-05-16

- $b$: retention ratio $= 1 -$ payout.
- Under those conditions book value, net income and residual income all grow at $g$, so $RI_T = RI_1(1+g)^{T-1}$ (Practice Problem 36) (V5 p.400).
- When OCI breaks clean surplus, or when EPS and DPS are forecast independently, RI growth differs from earnings growth: Mannistore Year 6 earnings grow 8% but residual income falls 2% (V5 p.372).

**Clean-surplus-adjusted residual income** (V5 p.350, p.371)
$$
\text{Comprehensive income} = NI + OCI, \qquad RI_t^{adj} = (NI_t + OCI_t) - rB_{t-1}
$$
^f-05-05-17

- Use when future OCI is material and not expected to net to zero; book value needs no change because AOCI is already in equity (V5 p.364, p.370).
- Mannistore Year 2: $2.48 - 1.00 - 0.10 \times 10.32 = 0.45$ instead of $1.45$, which is what makes the RI value equal the DDM value of 43.59 (V5 p.371).
- Alternatively adjust the ROE forecast: positive persistent translation gains argue for a higher ROE, persistent OCI losses for a lower one (V5 p.368, p.404).

**Capitalization effect on ROE** (V5 p.363)
$$
ROE_{cap} = \frac{E + X}{B + X} > ROE_{exp} = \frac{E}{B} \quad \text{whenever } ROE_{exp} < 1
$$
^f-05-05-18

- $X$: expenditure capitalized instead of expensed; both earnings and book value rise by $X$ in the year of capitalization.
- Example: $250{,}000/1{,}050{,}000 = 23.81\%$ against $200{,}000/1{,}000{,}000 = 20\%$; extrapolating the higher ROE overstates value, and for a growing company the overstatement can persist (V5 p.363).
- The mirror image (Lundholm and Sloan): adding an omitted asset to $B_0$ and amortizing it leaves RI value unchanged, because the higher $B_0$ is offset by the PV of amortization plus the PV of the capital charge on the asset (V5 p.375).

## Worked examples

### Example 1: AXCI, residual income two ways and the value it implies (V5 p.339, p.340, p.341)

Setup: total assets EUR 2 million, 50% debt and 50% equity, pretax cost of debt 7%, tax rate 30% (after-tax cost of debt 4.9%), cost of equity 12%, EBIT EUR 200,000.

Equity route (Formula 1).
Interest $= 0.07 \times 1{,}000{,}000 = 70{,}000$; pretax income $= 130{,}000$; tax $= 39{,}000$; net income $= 91{,}000$.
Equity charge $= 0.12 \times 1{,}000{,}000 = 120{,}000$.
$RI = 91{,}000 - 120{,}000 = -29{,}000$.

Capital route (Formula 2).
$NOPAT = 200{,}000 \times 0.70 = 140{,}000$.
Debt charge $= 0.07 \times 0.70 \times 1{,}000{,}000 = 49{,}000$; total capital charge $= 120{,}000 + 49{,}000 = 169{,}000$.
$RI = 140{,}000 - 169{,}000 = -29{,}000$.
Rate form: $ROIC = 140{,}000/2{,}000{,}000 = 7\%$; effective charge $= 169{,}000/2{,}000{,}000 = 8.45\%$; $(0.07 - 0.0845) \times 2{,}000{,}000 = -29{,}000$.

Valuation consequence (V5 p.341).
With 100,000 shares, $B_0 = 10$, EPS $= 0.91$, all earnings paid out and earnings flat forever, the firm destroys $0.29$ per share per year.
$PV = 0.29/0.12 = 2.42$, so $V_0 = 10 - 2.42 = 7.58$.
Cross-check with Formula 8: $E/r = 0.91/0.12 = 7.5833$, $P/B = 0.7583$.
Negative residual income means shares should trade below book value.
Python check: `(200000-70000)*0.7 = 91000`, `140000-169000 = -29000`, `0.91/0.12 = 7.5833`. ^ex-05-05-1

### Example 2: CNR, per-share residual income forecasts (V5 p.343, p.344)

Setup: adjusted beta 1.02, 10-year government yield 1.75%, ERP 7.5%; $B_0 = 24.32$; EPS 6.23 and 6.96; DPS 2.15 and 2.31 (the text says 2.32, the exhibit uses 2.31).

$r = 0.0175 + 1.02 \times 0.075 = 0.0940$.

2019: equity charge $= 0.094 \times 24.32 = 2.286$; $RI = 6.23 - 2.29 = 3.94$; $B_1 = 24.32 + 6.23 - 2.15 = 28.40$.
2020: equity charge $= 0.094 \times 28.40 = 2.670$; $RI = 6.96 - 2.67 = 4.29$; $B_2 = 28.40 + 6.96 - 2.31 = 33.05$.
The order matters: the charge always uses beginning book value, so the year 2 charge depends on the year 1 retention.
Python check: `0.0175+1.02*0.075 = 0.094`, `6.23-0.094*24.32 = 3.944`, `6.96-0.094*28.40 = 4.290`. ^ex-05-05-2

### Example 3: Bugg Properties, RI value equals DDM value (V5 p.345)

Setup: EPS 2.00, 2.50, 4.00; DPS 1.00, 1.25, 12.25 (liquidating); $B_0 = 6.00$; $r = 10\%$; company ceases after Year 3.

| Year | $B_{t-1}$ | EPS | DPS | $B_t$ | Charge $0.10 B_{t-1}$ | RI | PV of RI |
|---|---|---|---|---|---|---|---|
| 1 | 6.00 | 2.00 | 1.00 | 7.00 | 0.600 | 1.400 | 1.2727 |
| 2 | 7.00 | 2.50 | 1.25 | 8.25 | 0.700 | 1.800 | 1.4876 |
| 3 | 8.25 | 4.00 | 12.25 | 0.00 | 0.825 | 3.175 | 2.3854 |

$V_0 = 6.00 + 1.2727 + 1.4876 + 2.3854 = 11.15$.
DDM: $1.00/1.10 + 1.25/1.10^2 + 12.25/1.10^3 = 0.9091 + 1.0331 + 9.2036 = 11.15$.
Same total, different timing: RI puts 6.00 of the value at time zero, the DDM puts 9.20 in year 3 (V5 p.346).
Python check: `6+1.4/1.1+1.8/1.21+3.175/1.331 = 11.1458`, `1/1.1+1.25/1.21+12.25/1.331 = 11.1458`. ^ex-05-05-3

### Example 4: Bugg Properties with the ROE form (V5 p.347)

Same data through Formula 5's second form.
$ROE_1 = 2.00/6.00 = 0.3333$; spread $0.2333$; $RI_1 = 0.2333 \times 6.00 = 1.400$.
$ROE_2 = 2.50/7.00 = 0.3571$; spread $0.2571$; $RI_2 = 0.2571 \times 7.00 = 1.800$.
$ROE_3 = 4.00/8.25 = 0.4848$; spread $0.3848$; $RI_3 = 0.3848 \times 8.25 = 3.175$.
$V_0 = 6.00 + 1.2727 + 1.4876 + 2.3854 = 11.15$, identical to Example 3 because $(ROE_t - r)B_{t-1} = E_t - rB_{t-1}$ by construction.
Python check: `(2/6-0.1)*6 = 1.4`, `(4/8.25-0.1)*8.25 = 3.175`. ^ex-05-05-4

### Example 5: Alphabet, fading ROE with no dividends (V5 p.348, p.349)

Setup: price 1,037.39; $r = 8.2\%$; $B_0 = 255.40$; ROE 20.2% in 2019 falling 0.5 percentage points a year until it equals 8.2% in 2043, after which RI is zero; no dividends, buybacks offset issuance.

Year 1: $E = 0.202 \times 255.40 = 51.59$; charge $= 0.082 \times 255.40 = 20.94$; $RI = 30.65 = 255.40 \times (0.202 - 0.082)$; $PV = 30.65/1.082 = 28.33$; $B_1 = 306.99$.
Year 2: $E = 0.197 \times 306.99 = 60.48$; charge $25.17$; $RI = 35.30$; $PV = 30.16$; $B_2 = 367.47$.
The RI rises in money terms until 2035 (116.45) even as ROE falls, because book value compounds at the full ROE with nothing paid out, then falls to 29.65 in 2042 and to zero in 2043.
Sum of PVs 2019 to 2042 $= 716.85$; $V_0 = 255.40 + 716.85 = 972.25$, below the 1,037.39 price.
Continuing RI is set to zero because the horizon is long enough for ROE to reach $r$ (case 3 of Formula 15).
Python check: a loop with `E=roe*B; RI=E-0.082*B; B+=E; roe-=0.005` for 24 years gives `972.25`. ^ex-05-05-5

### Example 6: Philips, single-stage RI model (V5 p.351, p.352)

Setup: $B_0 = 13.22$; price 35.40; long-term ROE 12%; $g = 6.75\%$; $r = 8.5\%$.
Formula 10: $V_0 = 13.22 + (0.12 - 0.085)/(0.085 - 0.0675) \times 13.22 = 13.22 + (0.035/0.0175) \times 13.22 = 13.22 + 26.44 = 39.66$.
Justified P/B $= 3.0$; the curriculum's "almost 2.7 times book" refers to the market P/B $35.40/13.22 = 2.68$ (V5 p.352).
Python check: `13.22+0.035/0.0175*13.22 = 39.66`. ^ex-05-05-6

### Example 7: Philips, implied growth rate (V5 p.352)

Set price equal to value: $35.40 = 13.22 + 0.035 \times 13.22/(0.085 - g)$.
$35.40 - 13.22 = 22.18 = 0.4627/(0.085 - g)$, so $0.085 - g = 0.02086$ and $g = 6.41\%$.
The market prices in slightly less growth than Yoh's 6.75%, which is why price is below his 39.66.
Python check: `0.085-0.035*13.22/(35.40-13.22) = 0.06414`. ^ex-05-05-7

### Example 8: Zenlandia Chemical, multistage RI with zero terminal premium (V5 p.353, p.354)

Setup: price 95.6; $r = 12\%$; $B_{2019} = 28.8517$; EPS 7.162 and 8.356 with DPS 2.9995 and 3.2995 for 2020 and 2021; ROE 25% for 2022 to 2026 then 20% to 2039; retention 60% after 2021; RI zero after 2039.

2020: charge $= 0.12 \times 28.8517 = 3.4622$; $RI = 7.162 - 3.4622 = 3.6998$; $PV = 3.6998/1.12 = 3.30$; $B = 28.8517 + 7.162 - 2.9995 = 33.0142$.
2021: charge $3.9617$; $RI = 4.3943$; $PV = 3.50$; $B = 38.0707$.
2022: $E = 0.25 \times 38.0707 = 9.5177$; $D = 0.4 \times 9.5177 = 3.8071$; $RI = 9.5177 - 4.5685 = 4.9492$; $PV = 3.52$.
From 2027 ROE is 20% and $g = 0.6 \times 0.20 = 0.12 = r$, so every year's PV is the same 2.47 (RI grows at exactly the discount rate).
Sum of PVs 2020 to 2039 $= 57.56$; $V_0 = 28.85 + 57.56 = 86.41$.
Price 95.6 exceeds 86.41, so either the market expects more RI, a positive terminal premium, or a lower $r$; on her forecasts Rosato would call the shares overvalued.
Python check: the loop reproduces every row of Exhibit 5 and `86.41`. ^ex-05-05-8

### Example 9: Zenlandia, perpetuity of the 2039 residual income (V5 p.355)

$TV_{2039} = 23.8664/0.12 = 198.8867$; $PV = 198.8867/1.12^{20} = 20.6179$.
$V_0 = 86.41 + 20.62 = 107.03$, now above the 95.6 price, so the shares look undervalued if RI persists at the 2039 level.
This is the $\omega = 1$ case with the 2039 RI inside the explicit stage and the perpetuity starting in 2040.
Python check: `23.8664/0.12/1.12**20 = 20.618`. ^ex-05-05-9

### Example 10: Zenlandia, persistence factor 0.60 (V5 p.356)

$T = 20$ (2039), $RI_T = 23.8664$, $\omega = 0.60$.
Formula 14 terminal term: $23.8664/[(1 + 0.12 - 0.60) \times 1.12^{19}] = 23.8664/(0.52 \times 8.6128) = 23.8664/4.4786 = 5.33$.
The explicit stage now runs through 2038 only (T - 1 = 19 years): $B_0$ plus the PVs for 2020 to 2038 $= 28.85 + 55.08 = 83.93$.
$V_0 = 83.93 + 5.33 = 89.26$.
The curriculum prints the total as 86.26; $83.93 + 5.33 = 89.26$, so 86.26 is an arithmetic slip, and the conclusion (modestly overvalued at 95.6) is unchanged.
Compare the three terminal treatments: zero gives 86.41, $\omega = 0.6$ gives 89.26, perpetuity gives 107.03; the ordering is the lesson.
Python check: `23.8664/((1.12-0.6)*1.12**19) = 5.329`, `28.8517+55.08+5.33 = 89.26`. ^ex-05-05-10

### Example 11: URS Holdings, two-stage RI with a P/B terminal price (V5 p.357, p.358)

Setup: $B_0 = 15.00$; $r = 7.95\%$; EPS $= 25\%$ of beginning book value for six years; payout 30%; $P_6 = 1.8 \times B_6$.

| Year | $B_{t-1}$ | NI | Div | $B_t$ | RI | PV of RI |
|---|---|---|---|---|---|---|
| 1 | 15.000 | 3.750 | 1.125 | 17.625 | 2.558 | 2.369 |
| 2 | 17.625 | 4.406 | 1.322 | 20.709 | 3.005 | 2.579 |
| 3 | 20.709 | 5.177 | 1.553 | 24.334 | 3.531 | 2.807 |
| 4 | 24.334 | 6.083 | 1.825 | 28.592 | 4.149 | 3.055 |
| 5 | 28.592 | 7.148 | 2.144 | 33.595 | 4.875 | 3.325 |
| 6 | 33.595 | 8.399 | 2.520 | 39.475 | 5.728 | 3.620 |

Sum of PV of RI $= 17.755$.
Terminal premium $P_6 - B_6 = 0.8 \times 39.475 = 31.580$; $PV = 31.580/1.0795^6 = 19.956$.
$V_0 = 15.000 + 17.755 + 19.956 = 52.711$ (Formula 13).
DDM check: PV of six dividends $= 7.810$; $P_6 = 1.8 \times 39.475 = 71.054$, $PV = 44.901$; total $52.711$.
Python check: loop gives `sumPV 17.755`, `PV premium 19.956`, `V 52.711` both ways. ^ex-05-05-11

### Example 12: a perpetuity under the DDM and the RI model (V5 p.359, p.360)

Setup: EPS 1.00 forever, all paid out, $B = 6.00$, $r = 10\%$.
DDM: $V_0 = 1.00/0.10 = 10.00$.
RI: book value is constant at 6.00, so $RI = 1.00 - 0.10 \times 6.00 = 0.40$ every year; $V_0 = 6.00 + 0.40/0.10 = 10.00$ (Formula 8).
Recognition: under RI, 6.00 of 10.00 (60%) sits at time zero; under the DDM the first five dividends give $0.909 + 0.826 + 0.751 + 0.683 + 0.621 = 3.79$, only 38% of value.
Python check: `6+0.4/0.1 = 10`, `sum(1/1.1**t for t in 1..5) = 3.791`. ^ex-05-05-12

### Example 13: Nokia and SAP, reading clean surplus violations (V5 p.365 to p.368)

Nokia (IFRS, 2018): items bypassing the income statement sit in share issue premium, translation differences, fair value and other reserves, and the reserve for invested unrestricted equity; the translation adjustment for the year was $+402 - 61 = +341$ million, alongside pension remeasurements of $+293$, cash flow hedges $-43$ and FVOCI financial assets $-38$ in the fair value reserve.
SAP (2018): share premium and other components of equity; other components rose EUR 887 million, mostly translation.
Both adjustments are positive, so they would have raised income had they run through the income statement.
If the analyst expects the positive translation trend to continue and has anchored ROE on history, the future ROE estimate should be revised upward; if exchange rates reverse, no adjustment is warranted.
No arithmetic beyond the column totals; Python check: `402-61 = 341`. ^ex-05-05-13

### Example 14: Mannistore, RI value with and without the OCI adjustment (V5 p.370, p.371, p.372)

Setup: $r = 10\%$; beginning equity 8.58, 10.32, 11.51, 14.68, 17.86; NI 2.00, 2.48, 3.46, 3.47, 4.56; DPS 0.26, 0.29, 0.29, 0.29, 0.38; OCI of $-1.00$ in Year 2; $B_5 = 22.04$; $P_5 = 68.40$.

Part 1, DDM: $0.26/1.1 + 0.29/1.1^2 + 0.29/1.1^3 + 0.29/1.1^4 + 0.38/1.1^5 + 68.40/1.1^5 = 43.59$.
Part 2A, unadjusted RI: $2.00 - 0.858 = 1.14$; $2.48 - 1.032 = 1.45$; $3.46 - 1.151 = 2.31$ (printed as 2.30); $3.47 - 1.468 = 2.00$; $4.56 - 1.786 = 2.77$.
$V_0 = 8.58 + PV(RI) + (68.40 - 22.04)/1.1^5 = 8.58 + 35.85 = 44.42$ (the printed 35.84 uses the rounded 2.30).
Part 2B, adjusted RI (Formula 17): Year 2 becomes $2.48 - 1.00 - 1.032 = 0.45$; others unchanged.
$V_0 = 8.58 + 35.02 = 43.59$, equal to the DDM.
Part 3: 2A omits the clean surplus violation and overstates value by about 0.83; 2B is right.
Part 4: Year 6 NI $= 4.56 \times 1.08 = 4.92$, DPS $= 0.41$; $RI_6 = 4.92 - 0.10 \times 22.04 = 2.72$; growth in RI $= 2.72/2.77 - 1 = -1.8\%$, negative even though earnings grow 8%, because the equity charge on the enlarged book value grows faster than earnings.
Python check: `DDM 43.599`, `V_A 44.425`, `V_B 43.599`, `4.9248-2.204 = 2.7208`. ^ex-05-05-14

### Example 15: Exhibit 13, three OCI forecasts with the same ROE assumption (V5 p.368, p.369)

Setup: year $t-1$ equity 1,000, NI 120 (ROE 12%), OCI $-100$, no dividends, so equity at the start of $t$ is 1,020 with AOCI $-100$; $r = 10\%$; all forecasts use $NI = 0.12 \times$ beginning equity.

Forecast A (no future OCI): $NI_t = 122.40$, charge 102.00, $RI_t = 20.40$; equity becomes 1,142.40; $NI_{t+1} = 137.09$, charge 114.24, $RI_{t+1} = 22.85$; RI growth $= 12.0\%$, equal to ROE times retention of 100%.
Forecast B (OCI of $-100$ each year): equity at $t+1$ is $1{,}020 + 122.40 - 100 = 1{,}042.40$; $NI_{t+1} = 125.09$, charge 104.24, $RI_{t+1} = 20.85$; RI growth $= 2.2\%$.
Forecast C (OCI reverses, $+100$ in year $t$): equity at $t+1$ is 1,242.40; $NI_{t+1} = 149.09$, charge 124.24, $RI_{t+1} = 24.85$; RI growth $= 21.8\%$.
If instead ROE were measured on comprehensive income, Forecast B implies ROE of $(120 - 100)/1{,}000 = 2\%$, comprehensive income at $t$ of $22.40$, and $RI_t = 22.40 - 102 = -79.60$ rather than $+20.40$.
Lesson: ignoring expected OCI distorts both the level and the growth of residual income unless the violations net to zero.
Python check: `1142.4*0.12-114.24 = 22.85`, `1042.4*0.12-104.24 = 20.85`, `1242.4*0.12-124.24 = 24.85`. ^ex-05-05-15

### Example 16: capitalizing instead of expensing (V5 p.363)

Setup: book value 1,000,000; pretax earnings 200,000 after expensing 50,000; taxes ignored.
Expensed: $ROE = 200{,}000/1{,}000{,}000 = 20\%$.
Capitalized: earnings 250,000 and book value 1,050,000, $ROE = 23.81\%$ (Formula 18).
An analyst who extrapolates 23.81% overvalues the company; for a stable firm the ROE will drift down as the capitalized item is amortized while book value stays overstated, and for a growing firm with rising capitalized amounts the inflated ROE can persist.
Python check: `250000/1050000 = 0.2381`. ^ex-05-05-16

### Example 17: Alpha acquires Beta, intangibles and amortization (V5 p.373, p.374)

Setup: Alpha has equity 5,000 and NI 600 (ROE 12%); Beta has equity 1,000 and NI 150 (ROE 15%); both pay out everything, $r = 10\%$, $g = 0$.
Separate values (Formula 10): Alpha $= 5{,}000 + (0.12 - 0.10)/0.10 \times 5{,}000 = 6{,}000$; Beta $= 1{,}000 + 0.05/0.10 \times 1{,}000 = 1{,}500$; combined 7,500.
Cash acquisition at 1,500: the 500 excess is a 10-year license, so no goodwill; Alpha's equity stays 5,000 (cash 200, PP&E 4,300, license 500).
With amortization of 50: NI $= 600 + 150 - 50 = 700$, ROE 14%, value $= 5{,}000 + 0.04/0.10 \times 5{,}000 = 7{,}000$, below the 7,500 that a fair purchase should preserve.
Adding back the amortization: NI 750, ROE 15%, value $= 5{,}000 + 0.05/0.10 \times 5{,}000 = 7{,}500$.
Share-financed acquisition: equity 6,500, NI 750 excluding amortization, ROE $= 750/6{,}500 = 11.538\%$, value $= 6{,}500 + 0.01538/0.10 \times 6{,}500 = 7{,}500$; higher book value is offset by lower ROE.
Overpayment would show up as lower future residual income.
Python check: `5000+0.04/0.1*5000 = 7000`, `6500+(750/6500-0.1)/0.1*6500 = 7500`. ^ex-05-05-17

## Item-set patterns

> [!warning] Trap 1: the equity charge uses equity, the capital charge uses total capital
> The vignette gives total assets, a debt weight, a pretax cost of debt, a tax rate, a cost of equity and EBIT, then asks for residual income.
> Correct: either net income minus $r \times$ equity, or NOPAT minus [equity charge plus after-tax debt charge]; both give the same figure (V5 p.340, p.395).
> Distractors: charging the cost of equity against total assets (SSX 600 instead of 240), using the pretax cost of debt in the capital charge, or subtracting the equity charge from NOPAT (455 - 240 = 215 for SSX instead of 133.9).

> [!warning] Trap 2: pretax income already has interest deducted
> Practice Problem 2 gives pretax income, not EBIT.
> Correct: net income is pretax income times (1 - t); do not deduct interest again (V5 p.392).
> Distractor: computing interest from the debt balance and subtracting it a second time, which turns a -2.34 million residual income into something far more negative.

> [!warning] Trap 3: omega measures survival, not decay
> The vignette says an analyst uses a persistence factor of 0.10 while another assumes RI is constant into perpetuity.
> Correct: 0.10 means 90% of residual income disappears each year, so value is lower; 1.0 is the perpetuity case; higher omega means higher value (V5 p.356, p.397).
> Distractors: reading 0.10 as a 10% decay rate (which would make it almost a perpetuity), or applying the formula with $(1 + r)^T$ in the denominator instead of $(1 + r)^{T-1}$ and summing the explicit stage through $T$ instead of $T - 1$.

> [!warning] Trap 4: book value hidden inside price and P/B
> The exhibit gives price and P/B but not book value, then asks for implied growth or residual income.
> Correct: $B_0 = P_0 / (P/B)$, then solve Formula 11 (SSX: 48.80/2.10 = 23.24, g = 7.4%) (V5 p.396).
> Distractors: 5.8% and 11.0% come from using price in place of book value or from dropping the "minus $B_0$" on the left-hand side.

> [!warning] Trap 5: the terminal premium is $P_T - B_T$, not $P_T$
> A two-stage RI vignette says the terminal price will be some multiple of book value or of trailing earnings.
> Correct: discount the premium over book value, $P_T - B_T$, because $B_T$ has already been counted through the retained residual income (V5 p.353, p.402).
> Distractors: discounting the full $P_T$ (which double counts book value and reproduces the DDM terminal term), or forgetting the premium when the multiple is 1.0 times book, in which case the premium is zero (Amersheen Scenario 2).

> [!warning] Trap 6: which adjustment hits book value, which hits net income, which hits neither
> The vignette lists a restructuring charge, persistent negative OCI, an operating lease and an unrecognized brand.
> Correct: exclude the restructuring charge from the earnings used for forecasting and leave book value alone; reduce forecast ROE or add OCI to income for persistent OCI losses and leave book value alone because AOCI is already in equity; operating leases leave equity unchanged but affect earnings forecasts; an unrecognized brand is not added because Lundholm and Sloan show the adjustment is value-neutral (V5 p.364, p.372, p.375, p.404).
> Distractors: "upward adjustment to book value" for a restructuring charge, or "adjust the cost of equity".

> [!warning] Trap 7: RI recognizes value early, so its terminal value is small
> A statement in the vignette claims the terminal value is a larger share of value in RI models than in DCF models, or that RI models cannot be used without positive near-term FCF.
> Correct: both are false; book value captures a large share of value up front and the RI model is precisely the one to use with negative near-term FCF or no dividends (V5 p.353, p.361, p.395).
> Distractor: the true weakness is subtle, that the model assumes interest expense reflects the cost of debt, and candidates skip it because it sounds technical.

> [!warning] Trap 8: growth in RI is not growth in earnings
> The vignette gives an 8% growth rate for earnings and dividends beyond the horizon and asks for next year's residual income growth.
> Correct: compute $RI_{T+1} = E_{T+1} - rB_T$ explicitly; Mannistore's RI falls 2% while earnings rise 8% (V5 p.372).
> Distractor: applying 8% to residual income, which is only valid when ROE, payout and clean surplus are all constant (Foodsco) (V5 p.400).

> [!warning] Trap 9: ROE equal to r means value equals book, regardless of growth
> Question 2 in the Nkomo vignette: single-stage intrinsic value equals book value; what does that imply?
> Correct: ROE equals the cost of equity, so the second term of Formula 10 is zero for any $g < r$ (V5 p.393).
> Distractors: "growth is zero" or "ROE is below r" (which would give a value below book).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM05-Residual-Income-Valuation-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: the RI model is the DDM rewritten through the clean surplus relation, the justified P/B here is the Gordon model P/B, and $g = b \times ROE$ comes from the sustainable growth discussion there.
- [[LM03-Free-Cash-Flow-Valuation]]: FCFE and FCFF are the alternatives the selection LOS compares against; RI is preferred when near-term FCF is negative, FCF is preferred when cash flow is positive and predictable, and consistent pro formas make the three agree.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: justified P/B from fundamentals, the implied growth and implied ROE backed out of a market P/B, and Tobin's q all sit on the boundary between this module and multiples.
- [[LM01-Intercorporate-Investments]]: book value of equity, goodwill and the treatment of acquired intangibles determine $B_0$; the Alpha and Beta example is an acquisition-method allocation seen through an RI lens.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: pension remeasurements and share-based payment reserves are the OCI items that violate clean surplus and require the net income or ROE adjustment used here.
- [[LM03-Cost-of-Capital-Advanced-Topics]]: the required return on equity that sets the equity charge, and the WACC that sets the capital charge in EVA, are estimated there.

## Self-test

Vignette A for Q1 to Q3: Kestrel Ltd has total assets of 8,000, financed 40% with debt at a pretax cost of 5% and 60% with equity; the tax rate is 25%, the cost of equity 11%, and EBIT is 900 (all figures in millions).
Kestrel has 400 million shares and book value per share of 12.
Management expects EBIT to stay at 900 indefinitely and pays out all earnings.

> [!question] Q1
> Kestrel's residual income using the equity charge approach is closest to:
> A. 27.
> B. 147.
> C. 195.

> [!question] Q2
> Kestrel's total capital charge under the NOPAT approach is closest to:
> A. 528.
> B. 648.
> C. 688.

> [!question] Q3
> The intrinsic value per share of Kestrel using the residual income model is closest to:
> A. 12.07.
> B. 12.61.
> C. 13.35.

Vignette B for Q4 to Q6: Marlow Foods has book value per share of 18, a market price of 45, long-term ROE of 14%, long-term growth of 5%, and a cost of equity of 9%.

> [!question] Q4
> The single-stage RI value of Marlow is closest to:
> A. 28.00.
> B. 40.50.
> C. 81.00.

> [!question] Q5
> The growth rate implied by the market price is closest to:
> A. 4.0%.
> B. 5.7%.
> C. 6.4%.

> [!question] Q6
> Marlow's justified P/B is closest to:
> A. 1.56.
> B. 2.25.
> C. 2.50.

Vignette C for Q7 to Q9: Orrin Tech has book value per share of 30 and a cost of equity of 10%.
Forecast EPS is 6.00, 6.60 and 7.20 and forecast DPS is 2.00, 2.20 and 2.40 for Years 1 to 3.
Analyst Ruiz assumes residual income stays at its Year 3 level forever.
Analyst Sato assumes residual income fades with a persistence factor of 0.60 after Year 3.

> [!question] Q7
> Ruiz's intrinsic value is closest to:
> A. 60.62.
> B. 63.14.
> C. 68.97.

> [!question] Q8
> Sato's intrinsic value is closest to:
> A. 39.34.
> B. 40.42.
> C. 40.93.

> [!question] Q9
> Which statement about the persistence factor is most accurate?
> A. A factor of 0.60 means residual income declines by 60% each year after the horizon.
> B. A factor of 0.60 means 60% of the prior year's residual income survives each year, so it decays at 40% a year.
> C. A higher persistence factor produces a lower intrinsic value because more residual income is deferred.

Vignette D for Q10: Pell AG reports net income of 240 on beginning equity of 2,000, with other comprehensive income of $-60$ from currency translation that the analyst expects to persist; the cost of equity is 9%.

> [!question] Q10
> The clean-surplus-adjusted residual income for the year is closest to:
> A. 0.
> B. 60.
> C. 120.

> [!success]- Answer key
> Q1: A.
> Debt 3,200, equity 4,800; interest $= 160$; pretax income $740$; net income $555$; equity charge $= 0.11 \times 4{,}800 = 528$; $RI = 27$ (Python: `(900-160)*0.75-528 = 27`).
> B is net income less the after-tax debt charge; C is NOPAT less the equity charge only, which forgets to charge for debt while using a profit measure that is before interest.
>
> Q2: B.
> After-tax debt charge $= 160 \times 0.75 = 120$; total capital charge $= 528 + 120 = 648$; check: $NOPAT = 675$, $675 - 648 = 27$, matching Q1 (Python: `528+160*0.75 = 648`).
> A is the equity charge alone; C uses the pretax debt charge of 160.
>
> Q3: B.
> RI per share $= 27/400 = 0.0675$; perpetuity $= 0.0675/0.11 = 0.614$; $V_0 = 12 + 0.61 = 12.61$; check via Formula 8: EPS $= 555/400 = 1.3875$, $1.3875/0.11 = 12.61$ (Python: `12+0.0675/0.11 = 12.614`).
> A adds one year's RI without capitalizing it; C is a decoy above the E/r value.
>
> Q4: B.
> $V_0 = 18 + (0.14 - 0.09)/(0.09 - 0.05) \times 18 = 18 + 1.25 \times 18 = 40.50$ (Python: `18*(1+0.05/0.04) = 40.5`).
> A divides the spread by $r$ instead of $r - g$; C uses ROE rather than the spread in the numerator.
>
> Q5: B.
> $45 - 18 = 27 = 0.05 \times 18/(0.09 - g)$; $0.09 - g = 0.9/27 = 0.0333$; $g = 5.67\%$ (Python: `0.09-0.05*18/27 = 0.0567`).
> A and C bracket the answer; the market prices in slightly more growth than the analyst's 5%, consistent with 45 above 40.50.
>
> Q6: B.
> $P/B = (0.14 - 0.05)/(0.09 - 0.05) = 2.25$, equal to $40.50/18$ (Python: `0.09/0.04 = 2.25`).
> A is $ROE/r$; C is the market P/B $45/18$.
>
> Q7: B.
> Book values 30, 34, 38.4; RI $= 6.0 - 3.0 = 3.00$, $6.6 - 3.4 = 3.20$, $7.2 - 3.84 = 3.36$.
> With $\omega = 1$ and $T = 3$: terminal $= 3.36/(0.10 \times 1.1^2) = 27.77$; $V_0 = 30 + 2.727 + 2.645 + 27.769 = 63.14$; the same result follows from including Year 3 in the explicit stage and discounting $3.36/0.10$ three periods (Python: `30+3/1.1+3.2/1.21+3.36/(0.1*1.21) = 63.14`).
> A discounts the perpetuity three periods while leaving Year 3 out of the explicit stage; C forgets to discount the terminal term.
>
> Q8: C.
> Terminal $= 3.36/[(1.10 - 0.60) \times 1.1^2] = 3.36/(0.50 \times 1.21) = 5.554$; $V_0 = 30 + 2.727 + 2.645 + 5.554 = 40.93$ (Python: `30+2.727+2.645+3.36/(0.5*1.21) = 40.93`).
> A treats 0.60 as the decay rate ($\omega = 0.40$); B discounts by $(1.1)^3$ instead of $(1.1)^2$.
>
> Q9: B.
> $\omega$ is the fraction that persists, so 0.60 means a 40% annual decay; higher $\omega$ raises the terminal term and the value.
> A inverts the definition; C inverts the direction (V5 p.356).
>
> Q10: A.
> Adjusted RI $= (240 - 60) - 0.09 \times 2{,}000 = 180 - 180 = 0$ (Python: `180-180 = 0`).
> B is the unadjusted RI of $240 - 180 = 60$; C adds the OCI loss back instead of deducting it.
> Book value is not adjusted because the translation losses are already in accumulated OCI (V5 p.364, p.404).

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm05

Residual income definition::Net income minus the equity charge, where the equity charge is the required return on equity times beginning book value of equity (V5 p.339).
Why traditional financial statements need residual income::The income statement charges for debt through interest expense but never charges for equity capital, so positive net income can still destroy value (V5 p.338).
Capital charge approach to residual income::NOPAT minus [equity charge plus after-tax cost of debt times debt]; equals the equity approach when after-tax interest matches the debt charge and book weights are used (V5 p.340).
Rate form of residual income::(ROIC minus effective capital charge rate) times beginning capital, with ROIC equal to NOPAT over total capital (V5 p.340).
EVA formula::NOPAT minus (cost of capital times total capital), both after Stern Stewart adjustments (V5 p.341).
Five common EVA adjustments::Capitalize and amortize R&D, suspend the capital charge on strategic investments, cash taxes instead of deferred taxes, add the LIFO reserve to capital, treat operating leases as capital leases and adjust nonrecurring items (V5 p.342).
MVA formula::Market value of the company (debt plus equity) minus accounting book value of total capital (V5 p.342).
Main commercial use of EVA-type models::Internal performance measurement and executive compensation rather than equity valuation (V5 p.342).
Per-share residual income, two forms::$E_t - rB_{t-1}$ or $(ROE_t - r)B_{t-1}$, with ROE measured on beginning book value (V5 p.343, p.347).
Clean surplus relation::$B_t = B_{t-1} + E_t - D_t$; earnings capture every change in equity except owner transactions (V5 p.346).
General residual income model::$V_0 = B_0 + \sum RI_t/(1+r)^t$ (V5 p.343).
How the RI model is derived::Substitute $D_t = E_t + B_{t-1} - B_t$ into the DDM and let the book value terms telescope, leaving $B_0$ plus discounted $E_t - rB_{t-1}$ (V5 p.346).
Other names for the residual income model::Economic profit, abnormal earnings, discounted abnormal earnings model, Edwards-Bell-Ohlson model, excess earnings method in US tax valuation (V5 p.341, p.346).
Fundamental determinants of residual income::Book value of equity and the spread of ROE over the required return on equity (V5 p.350, p.378).
Single-stage RI model::$V_0 = B_0 + (ROE - r)B_0/(r - g)$ (V5 p.350).
Justified P/B from the RI model::$(ROE - g)/(r - g) = 1 + (ROE - r)/(r - g)$ (V5 p.350).
Condition for P/B above one::ROE above the required return, equivalently positive expected residual income (V5 p.378).
Implied growth from the single-stage model::$g = r - (ROE - r)B_0/(P_0 - B_0)$; recover $B_0$ as price divided by P/B if necessary (V5 p.352, p.396).
Micro-problem: B0 13.22, ROE 12%, r 8.5%, g 6.75%; value?::$13.22 + 0.035/0.0175 \times 13.22 = 39.66$; keystrokes 0.035 ÷ 0.0175 = 2, × 13.22 = 26.44, + 13.22 = 39.66 (V5 p.352).
Micro-problem: price 35.40, B0 13.22, ROE 12%, r 8.5%; implied g?::$0.085 - 0.035 \times 13.22/22.18 = 6.41\%$ (V5 p.352).
Tobin's q::Market value of debt and equity over replacement cost of total assets; differs from P/B in numerator, denominator and measurement basis (V5 p.350, p.351).
Why ROE mean-reverts::High ROE attracts entrants and competition, low ROE drives exits, so residual income tends toward zero over time (V5 p.352).
Continuing residual income::Residual income after the explicit forecast horizon (V5 p.352).
Four continuing-RI assumptions::Persists indefinitely at a positive level, zero from the terminal year forward, declines to zero as ROE reverts to r, declines to some mean level (V5 p.353).
Finite-horizon RI model with terminal premium::$V_0 = B_0 + \sum_{t=1}^{T} RI_t/(1+r)^t + (P_T - B_T)/(1+r)^T$ (V5 p.353).
Persistence factor model::$V_0 = B_0 + \sum_{t=1}^{T-1} RI_t/(1+r)^t + RI_T/[(1 + r - \omega)(1+r)^{T-1}]$ (V5 p.355).
What omega equal to 1 means::Residual income never fades; the terminal term is a perpetuity of $RI_T$ (V5 p.356).
What omega equal to 0 means::Residual income stops after the horizon; the terminal term collapses to the single flow $RI_T$ (V5 p.356).
Dechow, Hutton and Sloan average persistence::0.62, interpreted as residual income decaying 38% a year (V5 p.356).
Markers of lower residual income persistence::Extreme ROE, extreme special items, extreme accruals (V5 p.356).
Markers of higher residual income persistence::Low dividend payout, high historical persistence in the industry, strong market leadership (V5 p.356).
Micro-problem: RI_T 23.8664, r 12%, omega 0.60, T 20; PV of terminal term?::$23.8664/(0.52 \times 1.12^{19}) = 5.33$; keystrokes 1.12 y^x 19 = 8.6128, × 0.52 = 4.4786, 23.8664 ÷ 4.4786 = 5.33 (V5 p.356).
Micro-problem: RI_3 3.47, r 8.7%, RI constant forever; PV of terminal term?::$3.47/(0.087 \times 1.087^2) = 33.78$ (V5 p.397).
Where value is recognized in RI versus DDM::RI books most value in current book value and early residual income; the DDM books most in the terminal value (V5 p.346, p.360).
Four strengths of RI models::Small terminal value share, uses available accounting data, works without dividends or positive near-term FCF, works with unpredictable cash flows, focuses on economic profit (V5 p.361).
Four weaknesses of RI models::Accounting data can be manipulated, inputs may need heavy adjustment, requires clean surplus or adjustments, assumes interest expense reflects the cost of debt (V5 p.361).
When RI is most appropriate::No or unpredictable dividends, negative expected FCF within the forecast horizon, great uncertainty about terminal values (V5 p.361).
When RI is least appropriate::Significant clean surplus violations, or book value and ROE not predictable (V5 p.362).
Comprehensive income::Net income plus other comprehensive income; all equity changes other than owner transactions (V5 p.350, p.364).
Six items that commonly bypass the income statement::Unrealized fair value changes on some financial instruments, currency translation adjustments, certain pension adjustments, part of hedging gains and losses, IFRS revaluation surplus, IFRS own-credit-risk changes on liabilities (V5 p.364).
Effect of clean surplus violations on inputs::Book value is right because AOCI is in equity; net income and ROE are misstated for valuation purposes (V5 p.364).
When clean surplus violations bias valuation::Only when the present value of expected violations does not net to zero (V5 p.364).
Why compute historical ROE at the aggregate level::Share issuance and repurchases distort per-share ROE (V5 p.364).
Treatment of persistent negative OCI on available-for-sale securities::Reduce income by the OCI loss each year and lower ROE; leave book value unchanged (V5 p.404).
Treatment of a restructuring charge in an RI forecast::Exclude it from the earnings used to forecast; no book value adjustment (V5 p.375, p.394).
Nonrecurring items to review::Unusual items, extraordinary items (US GAAP only), restructuring charges, discontinued operations, accounting changes (V5 p.375).
Balance sheet items to review for fair value::Inventory (LIFO), deferred tax assets and liabilities, operating leases, reserves and allowances, intangible assets (V5 p.372).
Effect of operating leases on RI inputs::No effect on equity because the off-balance-sheet asset and liability offset, but they affect earnings forecasts (V5 p.372).
Capitalizing versus expensing 50,000 on 1,000,000 book and 200,000 earnings::ROE 20% expensed versus 23.81% capitalized; extrapolating the higher ROE overvalues the firm (V5 p.363).
Lundholm and Sloan result on omitted intangibles::Adding an omitted asset and amortizing it has no net effect on RI value; the higher $B_0$ is offset by the PV of amortization plus the capital charge (V5 p.375).
Alpha and Beta lesson::Amortizing an acquired intangible lowers ROE and understates combined value unless amortization is added back; paying with shares raises book value and lowers ROE with the same total (V5 p.373, p.374).
Bauman's balancing argument and why it fails::Aggressive accounting raises book value and lowers future earnings by offsetting PVs under clean surplus; it fails because clean surplus does not hold and analysts extrapolate past earnings (V5 p.362, p.363).
Frankel and Lee's three international considerations::Availability of reliable earnings forecasts, systematic clean surplus violations, poor-quality accounting rules that delay recognition (V5 p.376).
{{Growth in residual income equals growth in earnings only when ROE, payout and clean surplus are all constant}}; Mannistore's earnings grow 8% while RI falls 2% (V5 p.372, p.400).
{{Preferred dividends}} are deducted from net income before computing residual income for common shareholders (V5 p.339).

## Common mistakes

1. Charging the cost of equity against total assets or total capital instead of the book value of equity (V5 p.339, p.395).
2. Deducting interest a second time when the vignette gives pretax income rather than EBIT (V5 p.392).
3. Using the pretax cost of debt in the capital charge under the NOPAT approach, or subtracting only the equity charge from NOPAT (V5 p.340, p.396).
4. Reading the persistence factor as a decay rate; $\omega = 0.10$ means a 90% decay and a lower value, and a higher $\omega$ always raises value (V5 p.356, p.397).
5. Summing the explicit stage through $T$ and discounting the persistence terminal term by $(1+r)^T$; the formula sums to $T - 1$ and discounts by $(1+r)^{T-1}$ (V5 p.355).
6. Discounting the full terminal price $P_T$ instead of the premium $P_T - B_T$ in the finite-horizon model (V5 p.353, p.402).
7. Forgetting that a terminal price equal to book value makes the terminal term zero (V5 p.395).
8. Using $r$ instead of $r - g$ in the single-stage denominator, or ROE instead of ROE minus $r$ in the numerator (V5 p.350).
9. Using the price rather than book value when solving for implied growth; back $B_0$ out of price and P/B first (V5 p.396).
10. Assuming residual income grows at the earnings growth rate when payout, ROE or clean surplus are not constant (V5 p.372, p.400).
11. Adjusting book value for a nonrecurring charge or for persistent OCI losses; both leave book value alone and change the earnings or ROE used to forecast (V5 p.375, p.404).
12. Treating significant OCI as a reason to use an RI model; it is a clean surplus violation and argues against it (V5 p.362, p.395).
13. Claiming that terminal values are a larger share of value under RI than under DDM or FCF; the reverse is true (V5 p.353, p.361).
14. Computing ROE on average equity or on a per-share basis for the RI model; use beginning book value at the aggregate level (V5 p.347, p.364).
15. Extrapolating an ROE inflated by capitalized expenditures, cookie jar reserves or accelerated revenue without adjustment (V5 p.363, p.376).
16. Concluding a fair-value acquisition destroyed value because amortization of the acquired intangible lowered ROE (V5 p.374).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-05" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
