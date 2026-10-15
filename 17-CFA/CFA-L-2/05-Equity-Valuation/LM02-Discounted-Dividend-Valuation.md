---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 2
title: "Discounted Dividend Valuation"
pages: "49-123"
weight_band: "10-15%"
difficulty: 3
los_count: 16
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM2: Discounted Dividend Valuation

Difficulty 3 of 5: sixteen LOS but one engine, the present value of dividends; the arithmetic is BA II Plus friendly, and the marks are lost on model selection, on using D0 instead of D1, on discounting the terminal value one period too many, and on reading PVGO and justified P/E backwards from price.

## LOS map

- **compare** dividends, free cash flow, and residual income as inputs to discounted cash flow models and identify investment situations for which each measure is suitable (V5 p.49) ^los-05-02-a
    - Examiner asks: given a payout history and an ownership perspective, pick DDM, FCFE/FCFF or residual income, and state the one fact in the vignette that rules out the other two.
- **calculate** and interpret the value of a common stock using the dividend discount model (DDM) for single and multiple holding periods (V5 p.49) ^los-05-02-b
    - Examiner asks: discount a short list of dividends plus a terminal price at the required return, or back out the expected holding period return from D1, P1 and P0.
- **calculate** the value of a common stock using the Gordon growth model and explain the model's underlying assumptions (V5 p.49) ^los-05-02-c
    - Examiner asks: compute D0(1 + g)/(r - g) with r from the CAPM, and state that r must exceed g and that growth must be constant forever.
- **calculate** the value of non-callable fixed-rate perpetual preferred stock (V5 p.49) ^los-05-02-d
    - Examiner asks: dividend rate times par divided by the capitalization rate, or invert it to find the capitalization rate from the market price.
- **describe** strengths and limitations of the Gordon growth model and justify its selection to value a company's common shares (V5 p.49) ^los-05-02-e
    - Examiner asks: which of three sector reports or company profiles fits a single-stage model (stable payout, growth at or below nominal GDP, no supernormal phase, repurchases forecastable).
- **calculate** and interpret the implied growth rate of dividends using the Gordon growth model and current stock price (V5 p.49) ^los-05-02-f
    - Examiner asks: solve P0 = D0(1 + g)/(r - g) for g and compare it with the analyst's or sustainable growth rate to call the stock over- or undervalued.
- **calculate** and interpret the present value of growth opportunities (PVGO) and the component of the leading price-to-earnings ratio (P/E) related to PVGO (V5 p.49) ^los-05-02-g
    - Examiner asks: PVGO = P0 - E1/r for three stocks, then rank PVGO or PVGO/E1, remembering that the ranking by dollars and the ranking by P/E component can differ.
- **calculate** and interpret the justified leading and trailing P/Es using the Gordon growth model (V5 p.49) ^los-05-02-h
    - Examiner asks: (1 - b)/(r - g) versus (1 - b)(1 + g)/(r - g), compared with the actual P/E, with the payout ratio taken from the forward policy rather than last year's.
- **estimate** a required return based on any DDM, including the Gordon growth model and the H-model (V5 p.49) ^los-05-02-i
    - Examiner asks: r = D1/P0 + g for Gordon, r = (D0/P0)[(1 + gL) + H(gS - gL)] + gL for the H-model, and IRR by trial for a two-stage stream.
- **evaluate** whether a stock is overvalued, fairly valued, or undervalued by the market based on a DDM estimate of value (V5 p.49) ^los-05-02-j
    - Examiner asks: compare model value with price, sometimes inside a stated fair value band of plus or minus 10% or 20%, or compare implied growth with sustainable growth.
- **explain** the growth phase, transition phase, and maturity phase of a business (V5 p.49) ^los-05-02-k
    - Examiner asks: match FCFE sign, payout ratio and ROE relative to r to each phase, and map a company description to the model that fits its phases.
- **explain** the assumptions and justify the selection of the two-stage DDM, the H-model, the three-stage DDM, or spreadsheet modeling to value a company's common shares (V5 p.50) ^los-05-02-l
    - Examiner asks: three company descriptions (abrupt drop, linear decline, three distinct stages, irregular dividends) and which model fits each.
- **describe** terminal value and explain alternative approaches to determining the terminal value in a DDM (V5 p.50) ^los-05-02-m
    - Examiner asks: Gordon growth terminal value from D(n+1), or a P/E multiple applied to E(n) derived from D(n) and the payout ratio, and what the terminal value represents.
- **calculate** and interpret the value of common shares using the two-stage DDM, the H-model, and the three-stage DDM (V5 p.50) ^los-05-02-n
    - Examiner asks: full two-stage table with V(n) at t = n, the H-model with H equal to half the transition period, and the three-stage variant with the H-model applied at the end of stage 1.
- **explain** the use of spreadsheet modeling to forecast dividends and to value common shares (V5 p.50) ^los-05-02-o
    - Examiner asks: why a spreadsheet is used when dividends follow no stylized pattern, and what drives the terminal value in a pro forma model (P/E times forecast EPS).
- **calculate** and interpret the sustainable growth rate of a company and demonstrate the use of DuPont analysis to estimate a company's sustainable growth rate (V5 p.50) ^los-05-02-p
    - Examiner asks: g = b x ROE, or the PRAT product from a data table using beginning equity, and a sensitivity grid across payout and ROE.

## Core intuition

A share is a claim on a stream of cash that leaves the company and reaches the shareholder.
For a minority holder who cannot force a distribution, that cash is dividends, so the natural valuation is the present value of expected dividends discounted at the return the holder requires for bearing the risk (V5 p.50, p.53).
Everything in the module is a special case of one equation: value equals the sum of expected cash flows divided by (1 + r) to the power of their timing (V5 p.51).
The difficulty is never the discounting; it is that the stream is infinite and unknown, so the analyst must compress the forecast into a pattern that can be written down and defended (V5 p.61).

> [!abstract] Idea 1: the definition of cash flow chooses the model, and the ownership perspective chooses the definition
> Dividends fit a dividend-paying company whose payout bears an understandable, consistent relationship to earnings, seen by an investor without control (V5 p.54).
> Free cash flow fits a non-payer, a payer whose dividends differ substantially from FCFE, or an investor with a control perspective who could redirect the cash (V5 p.56, p.57).
> Residual income fits a non-payer as an alternative to FCF, or a company whose free cash flows are negative within the forecast horizon, because it front-loads value recognition through book value (V5 p.58).

### Why dividends, and when not

Reinvested earnings are not ignored by a DDM; they are the source of future dividends, so discounting every future dividend captures them (V5 p.53).
Dividends are smoother than earnings, so DDM values reflect long-run intrinsic value rather than short-run noise (V5 p.53).
The catch is that dividend policy must be readable.
AB InBev's payout ranged from 18% to 542% because of serial acquisitions, so a DDM would be fitting noise; Diageo's payout sat between 50% and 60% for fifteen years with EPS and DPS growing at 6.8% and 6.3%, so the DDM is appropriate (V5 p.55).
Non-dividend payers can be valued with a DDM in theory by forecasting when dividends start, but in practice the timing and size of initiation are unknowable, so analysts move to a company-level measure (V5 p.53, p.82).
Free cash flow to the firm is cash from operations minus capital expenditure; FCFE further nets payments to debtholders; FCFE is what the company could pay as dividends, which is why a control investor cares about it (V5 p.56).
Free cash flow fails when heavy investment keeps it negative for years, because the present value of negatives is negative and the horizon to positive cash flow is long; residual income, book value plus the present value of earnings above the required return on beginning equity, brings recognition of value closer to the present in that case (V5 p.57, p.58).
Residual income needs a detailed reading of accrual accounting and can be error-prone when disclosure quality is poor, so where the DDM works, analysts prefer it as the simpler tool (V5 p.58).

### From a finite holding period to the infinite sum

A one-year holder receives D1 and P1, so V0 = (D1 + P1)/(1 + r) (V5 p.59).
But P1 is itself the present value at t = 1 of D2, P2 and so on; substituting repeatedly pushes the selling price to the horizon, where its present value vanishes, and leaves the value as the sum of all future dividends (V5 p.60, p.61).
This is the reason a finite-horizon investor still cares about dividends after the sale: they set the price at which the sale happens (V5 p.61).
Two practical approaches follow: assign the whole stream to a stylized growth pattern, or forecast a few years individually and then either apply a pattern or a price multiple at the terminal point (V5 p.61).

### Gordon growth: a geometric series, with r > g as the price of admission

If dividends grow at a constant g forever, each term in the sum is the previous term times (1 + g)/(1 + r) (V5 p.62).
A geometric series with first term a = D1/(1 + r) and ratio m = (1 + g)/(1 + r) sums to a/(1 - m), which simplifies to D1/(r - g) (V5 p.62).
The sum converges only if m is below one, which is r > g; at r = g or r < g the dividends grow at least as fast as they are discounted and the value is infinite, which is nonsense economically, so a permanent growth rate above the required return is never a legitimate input (V5 p.62, p.63).
The growth rate must also be plausible forever, which in practice means at or below the economy's nominal growth rate, real GDP growth plus expected inflation (Canada 1.6% + 2% = 3.6%); a company expected to grow faster than that for a while needs a multistage model with a mature final stage (V5 p.63, p.64).

> [!abstract] Idea 2: in the Gordon model, price, dividends and earnings all grow at g, the dividend yield is constant, and total return splits into dividend yield plus g
> Multiply V0 = D1/(r - g) by (1 + g) and you get V1 = D2/(r - g), so value grows at g whenever r is constant (V5 p.69).
> Hence r = D1/P0 + g when price equals value: the required return is the forward dividend yield plus the capital gains yield (V5 p.76).
> The same identity, solved for g, gives the growth rate the market is pricing, which is compared with the analyst's own g to judge mispricing (V5 p.71, p.72).

Value is very sensitive to the spread r - g.
For MSEX, moving r and g by 25 bps each in opposite directions takes value from $33.92 to $53.02, a 56% range, while the point estimate is $41.39 (V5 p.68).
The exam's way of testing this is the sensitivity grid and the fair value band: a model value within 5% or so of the price is called fairly valued, and a stated band of plus or minus 10% or 20% converts a point estimate into an interval (V5 p.66, p.88, p.110).

Perpetual non-callable preferred stock is the Gordon model with g = 0: V0 = D/r, where r is called the capitalization rate; a callable issue would need the call option valued as well (V5 p.68).
Negative growth is allowed: a depleting mine with dividends shrinking 4% a year is worth D1/(r + 0.04) (V5 p.69).

### Repurchases and the implied growth rate

Share repurchases reduce shares outstanding, are not treated as a commitment, and are harder to forecast than dividends; at market prices they are wealth-neutral to remaining holders (V5 p.70).
A DDM stays valid for a repurchasing company if the analyst reflects the effect of buybacks on the per-share growth rate of dividends, which is why a sector report expressing confidence in forecasting repurchases is a green light for the Gordon model (V5 p.70, p.71, p.121).

### PVGO: the value of growth is what price pays above assets in place

A company that earns exactly its cost of equity on reinvested earnings adds nothing by reinvesting: the present value of 1.10 received in a year at 10% is 1.00, the amount given up (V5 p.72).
Only projects with ROE above r (with ROE measured on market value of equity) create value, so investors decompose value into the no-growth value E1/r, a perpetuity of constant earnings paid out in full, and the present value of growth opportunities, the forecast total NPV of future projects plus the value of the real options to time, scale or abandon them (V5 p.72, p.73, p.74).
Dividing by E1 turns the decomposition into a P/E decomposition: 1/r is the no-growth P/E and PVGO/E1 is the growth component (V5 p.74).
For MSEX at $43.20 with E1 = $1.52 and r = 6.8%, no-growth value is about $22.4, so almost half of the price is the market's valuation of growth; for Macy's the computed PVGO was negative, which means either the market expects value destruction or the inputs (E1 too high, r too low) are wrong (V5 p.73).

### Justified P/E: the Gordon model in multiple form

Divide P0 = D1/(r - g) by E1 and the ratio D1/E1 is the payout ratio (1 - b), so the justified leading P/E is (1 - b)/(r - g) (V5 p.74, p.75).
Divide P0 = D0(1 + g)/(r - g) by E0 instead and the justified trailing P/E is (1 - b)(1 + g)/(r - g), which is the leading P/E times (1 + g) (V5 p.75).
The analyst can therefore state a valuation opinion in P/E language: if the actual trailing P/E of 34.3 is below the justified 42.0, the stock is undervalued, and the same information in price terms is a Gordon value above the market price (V5 p.76).
For multistage models the justified leading P/E is simply the model value divided by next year's EPS; the closed forms exist but are not worth their complexity (V5 p.76).

### Multistage models follow the life cycle

Growth phase: rapidly expanding markets, high margins, supernormal EPS growth, negative FCFE because of heavy investment, low or zero payout (V5 p.77, p.78).
Transition phase: growth slows as competition compresses margins or markets saturate, capital needs fall, FCFE turns positive, payout rises or dividends begin (V5 p.78).
Mature phase: investments just earn the cost of capital, ROE approaches r, growth, payout and ROE stabilize; this is the stage the Gordon model can value, and it is the terminal stage of every multistage DDM (V5 p.78).

> [!abstract] Idea 3: every multistage model is a short list of explicit dividends plus one terminal value, and the terminal value usually carries most of the answer
> The terminal value V(n) is the price the stock should sell for at t = n, computed with the Gordon model from D(n + 1), or as a P/E multiple times forecast E(n) (V5 p.79, p.80, p.81).
> It sits at t = n, so it is discounted n periods, not n + 1, and it is built from the dividend of period n + 1, not period n (V5 p.79, p.82).
> In Meditec the terminal value is 93% of value, in the technology example 88%, in Rhinestone 94.8%; a terminal value is only as good as its r and gL (V5 p.80, p.86, p.88, p.94).

The two-stage model holds gS for n years and then drops abruptly to gL; it fits a patent or first-mover advantage with a known end (V5 p.79, p.80).
The H-model smooths the drop: growth declines linearly from gS to gL over 2H years, and the value is approximated by the Gordon value at gL plus an add-on for the extra dividends, D0 H (gS - gL)/(r - gL) (V5 p.83).
The add-on comes from averaging: excess growth averages (gS - gL)/2 over 2H years, so total excess dividends are roughly 2H D0 (gS - gL)/2 = D0 H (gS - gL), capitalized at r - gL; the individual timing is not modeled, which is why the H-model is an approximation that deteriorates for long transitions and large growth gaps (V5 p.84, p.85).
Applied to Meditec with a linear decline instead of an abrupt one, the value falls from EUR94.21 to EUR78.13 because the H-model pays less than the full 9% in most transition years (V5 p.84).
The three-stage model comes in two flavours: three constant rates, or a constant first stage followed by an H-model for stages two and three, evaluated at the end of stage one and then discounted back (V5 p.85, p.86).
Bloomberg's implementation fixes growth plus transition at 17 years and gives explosive-growth companies 3 years of growth and 14 of transition, slow growers 9 and 8 (V5 p.89).

### Spreadsheets, required returns and where g comes from

When dividends follow no pattern, an asset sale in year 5, a cut in year 6, a spreadsheet lists each dividend and applies the Gordon model only to the tail (V5 p.90, p.91).
Full pro forma models drive dividends from sales growth, margins, interest on debt, taxes and payout policy, then value the shares with a P/E on terminal EPS (V5 p.99, p.100).
Given price and all inputs except r, any DDM yields an IRR, interpreted as the market-implied expected return; for Gordon it is D1/P0 + g, for the H-model there is a closed form, and for anything else it is trial and error or Goal Seek (V5 p.92, p.93).
Reusing that IRR as the discount rate in the same DDM is circular (V5 p.92).
Finally, the mature growth rate is not a free parameter: g = b x ROE, the retention rate times the return on reinvested equity, holds exactly when ROE is measured on beginning equity and the capital structure is constant (V5 p.94, p.96).
Expanding ROE by DuPont gives the PRAT model, profit margin times retention times asset turnover times leverage, which lets the analyst forecast a mature ROE from benchmark components rather than from an unsustainable history, as with IBM's 52% ROE built on 7.35 times leverage (V5 p.96, p.98, p.99).
Mature ROE can also be set equal to r or to the industry median (V5 p.91).

## Formulas and derivations

**Present value model** (V5 p.51)
$$
V_0 = \sum_{t=1}^{n} \frac{CF_t}{(1+r)^t}
$$
^f-05-02-1

- $V_0$: value today; $CF_t$: expected cash flow at $t$; $r$: required return (flat term structure assumed); $n \to \infty$ for equities (V5 p.52).
- Risky cash flows are handled by discounting their expected value at a risk-adjusted rate (V5 p.51).
- The value at any date $k$ is the present value at $k$ of all later cash flows, so $V_0 = \sum_{t \le k} CF_t/(1+r)^t + V_k/(1+r)^k$ (V5 p.52).

> [!tip] Calculator
> Example 1: `CF` `2nd CLR WORK`, CF0 = 0, C01 = 100, C02 = 150, C03 = 200 (F = 1 each), `NPV`, I = 10, `CPT` gives 365.14.

**Single holding period DDM** (V5 p.59)
$$
V_0 = \frac{D_1 + P_1}{1+r}
$$
^f-05-02-2

- $D_1$: dividend paid at the end of year 1; $P_1$: expected price at $t = 1$; dividends are assumed paid as one sum at period end throughout the module (V5 p.59).
- Reason: the one-year holder's only cash flows are the dividend and the sale proceeds.
- Example 3: $(0.46 + 23.00)/1.08 = 21.72$ (V5 p.59).

**Expected holding period return from the single-period model** (V5 p.101)
$$
r = \frac{D_1 + P_1}{P_0} - 1 = \frac{D_1}{P_0} + \frac{P_1 - P_0}{P_0}
$$
^f-05-02-3

- Set $V_0 = P_0$ and solve Formula 2 for $r$: dividend yield plus price appreciation.
- This is the return the market implies if the price is fair; if price differs from value, the realized return also depends on how fast the mispricing corrects (V5 p.69, p.92).

**Finite holding period DDM** (V5 p.60)
$$
V_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r)^t} + \frac{P_n}{(1+r)^n}
$$
^f-05-02-4

- $P_n$: expected terminal price at $t = n$; the analyst forecasts dividends for two to five years and a terminal price by some method (V5 p.60).
- Adding a year adds one dividend term and moves the price one year out; substituting $P_1 = (D_2 + P_2)/(1+r)$ into Formula 2 gives the two-period case, and repeating gives Formula 4 (V5 p.60).

> [!tip] Calculator
> Example 4: `CF`, CF0 = 0, C01 = 2.00, C02 = 2.10, C03 = 2.20, C04 = 3.50, C05 = 43.75 (the year 5 dividend plus the 40.00 price), `NPV`, I = 10, `CPT` gives 34.76.

**General dividend discount model** (V5 p.61)
$$
V_0 = \sum_{t=1}^{\infty} \frac{D_t}{(1+r)^t}
$$
^f-05-02-5

- Reason: as $n \to \infty$, $P_n/(1+r)^n \to 0$ because $P_n$ itself is the present value at $n$ of later dividends (V5 p.60, p.61).
- Even a finite-horizon investor depends on all future dividends, directly through those received and indirectly through the selling price (V5 p.61).
- Every model that follows is a way of writing $D_t$ for all $t$ with a handful of parameters (V5 p.61).

**Clean surplus relation and residual income** (V5 p.57)
$$
BV_t = BV_{t-1} + E_t - D_t, \qquad RI_t = E_t - r \times BV_{t-1}
$$
^f-05-02-6

- $BV$: book value of equity; $E_t$: earnings; residual income is earnings above the required return on beginning equity (V5 p.57).
- Holds only if everything that touches book value passes through the income statement apart from ownership transactions (V5 p.58).
- Worked figure: equity 200 million, $r = 8\%$, earnings 18 million gives $RI = 18 - 16 = 2$ million; value under the RI model is book value plus the present value of expected residual income (V5 p.57).

**CAPM and bond-yield-plus-risk-premium required return** (V5 p.64, p.67)
$$
r = R_F + \beta_i \left[E(R_M) - R_F\right], \qquad r = \text{Pretax cost of debt} + \text{Risk premium}
$$
^f-05-02-7

- $E(R_M) - R_F$: equity risk premium; an adjusted beta moves the raw beta toward one (V5 p.65, p.66).
- Sonoco: $3.0 + 0.95 \times 4.5 = 7.3\%$; MSEX with adjusted beta $3 + 0.80 \times 4.5 = 6.6\%$; MSEX bond yield plus premium $4.8 + 2.5 = 7.3\%$ (V5 p.64, p.66, p.67).
- A low $R^2$ on beta (under 20% for MSEX) is a warning that the CAPM estimate is imprecise, which weakens any valuation conclusion (V5 p.65, p.67).

**Constant growth dividend** (V5 p.62)
$$
D_t = D_{t-1}(1+g) = D_0 (1+g)^t
$$
^f-05-02-8

- $D_0$: the dividend just paid; $D_1 = D_0(1+g)$ is the numerator of the Gordon model, never $D_0$ (V5 p.62, p.63).
- Example: $D_0 = 10$, $g = 5\%$ gives $D_5 = 10 \times 1.05^5 = 12.76$ (V5 p.62).

**Gordon growth model** (V5 p.62)
$$
V_0 = \frac{D_0(1+g)}{r-g} = \frac{D_1}{r-g}, \qquad r > g
$$
^f-05-02-9

- Substitute Formula 8 into Formula 5: $V_0 = \sum_{t \ge 1} D_0(1+g)^t/(1+r)^t$, a geometric series with first term $a = D_1/(1+r)$ and ratio $m = (1+g)/(1+r)$ (V5 p.62).
- Sum $= a/(1-m) = \dfrac{D_1/(1+r)}{1 - (1+g)/(1+r)} = \dfrac{D_1/(1+r)}{(r-g)/(1+r)} = \dfrac{D_1}{r-g}$, valid only for $|m| < 1$, that is $r > g$ (V5 p.62).
- Assumptions: constant $g$ forever, $r > g$, $r$ and $g$ reflect long-term expectations; suitable when growth is comparable to or below nominal GDP growth and the payout policy is stable (V5 p.63, p.64).
- Sensitivity: value rises without bound as $r - g \to 0$, so always report a grid of $r$ and $g$ (V5 p.63, p.68).

> [!tip] Calculator
> Example 5: `1.64 × 1.045 =` gives 1.7138; `0.073 - 0.045 =` gives 0.028; `1.7138 ÷ 0.028 =` gives 61.21.
> Store the spread with `STO 1` and recall it for the sensitivity grid.

**Non-callable fixed-rate perpetual preferred** (V5 p.68)
$$
V_0 = \frac{D}{r}
$$
^f-05-02-10

- $D$: fixed annual dividend = dividend rate $\times$ par; $r$: capitalization rate; Formula 9 with $g = 0$ (V5 p.68).
- Inverted, $r = D/P_0$ gives the capitalization rate implied by the market price (V5 p.121).
- KSU-P: $0.04 \times 25 = 1.00$, $1.00/0.055 = 18.18$ (V5 p.69).

**Growth of value and constant yields in the Gordon model** (V5 p.69, p.70)
$$
V_1 = V_0(1+g) = \frac{D_2}{r-g}, \qquad \frac{D_1}{P_0} = r - g \text{ (constant over time)}
$$
^f-05-02-11

- Multiply $V_0 = D_1/(r-g)$ by $(1+g)$ and use $D_2 = D_1(1+g)$; so value, dividends and (with constant payout) earnings all grow at $g$ (V5 p.69).
- $g$ is the capital gains yield when price equals value; with mispricing the actual appreciation depends on how the gap closes (V5 p.69).
- Example: price 50, $D_1 = 1$, $g = 5.5\%$: dividend yield 2%, capital gains yield 5.5%, total 7.5%, all constant through time (V5 p.70).

**Implied dividend growth rate** (V5 p.71, p.72)
$$
P_0 = \frac{D_0(1+g)}{r-g} \;\Rightarrow\; g = \frac{P_0 r - D_0}{P_0 + D_0}
$$
^f-05-02-12

- Cross-multiply: $P_0 r - P_0 g = D_0 + D_0 g$, collect $g$: $g(P_0 + D_0) = P_0 r - D_0$ (V5 p.72).
- If $D_1$ is given rather than $D_0$, use $g = r - D_1/P_0$ directly.
- Example 10: $(40 \times 0.122 - 2)/(40 + 2) = 2.88/42 = 6.86\%$; compare with the analyst's 5% to conclude the market is pricing faster growth (V5 p.72).

> [!tip] Calculator
> `40 × 0.122 - 2 =` gives 2.88; `÷ 42 =` gives 0.0686.

**PVGO decomposition of value** (V5 p.73)
$$
V_0 = \frac{E_1}{r} + \text{PVGO}
$$
^f-05-02-13

- $E_1/r$: no-growth value per share, the perpetuity of constant earnings paid out in full, also the value of assets in place; PVGO: present value of growth opportunities, the NPV of future projects plus real option value (V5 p.73, p.74).
- With $P_0 = V_0$, $\text{PVGO} = P_0 - E_1/r$ is the market's estimate of the value of growth (V5 p.73).
- Reinvestment creates value only when the return on new investment exceeds $r$; a no-growth company should pay out everything (V5 p.72, p.73).
- MSEX: $43.20 - 1.52/0.068 = 43.20 - 22.35 = 20.85$, about 48% of price; the text prints 22.42 and 20.78, a rounding difference (V5 p.73).

**P/E decomposition into no-growth and growth components** (V5 p.74)
$$
\frac{P_0}{E_1} = \frac{1}{r} + \frac{\text{PVGO}}{E_1}
$$
^f-05-02-14

- Divide Formula 13 by $E_1$; $1/r$ is the P/E of a no-growth company (V5 p.74).
- MSEX: P/E $43.20/1.52 = 28.4$, no-growth P/E $1/0.068 = 14.7$, growth component $20.78/1.52 = 13.67$ (V5 p.74).
- Practice Problem 15: the ranking of PVGO/E1 across stocks can differ from the ranking of PVGO in dollars (V5 p.119, p.120).

**Justified leading P/E** (V5 p.75)
$$
\frac{P_0}{E_1} = \frac{D_1/E_1}{r-g} = \frac{1-b}{r-g}
$$
^f-05-02-15

- $b$: retention rate; $1 - b$: dividend payout ratio $D_t/E_t$, assumed constant (V5 p.74).
- Divide $P_0 = D_1/(r-g)$ by $E_1$ (V5 p.75).
- Use the expected future payout, not last year's, when the vignette gives both (V5 p.111, p.120).

**Justified trailing P/E** (V5 p.75)
$$
\frac{P_0}{E_0} = \frac{D_0(1+g)/E_0}{r-g} = \frac{(1-b)(1+g)}{r-g}
$$
^f-05-02-16

- Divide $P_0 = D_0(1+g)/(r-g)$ by $E_0$; the trailing multiple is the leading multiple times $(1+g)$ (V5 p.75).
- L'Oreal: payout $3.85/7.08 = 0.5438$, $r = 5.6\%$, $g = 4.25\%$: leading $0.5438/0.0135 = 40.28$, trailing $0.5438 \times 1.0425/0.0135 = 42.00$ versus actual 34.3, so undervalued (V5 p.75, p.76).
- For multistage models, justified leading P/E = model value divided by $E_1$ (V5 p.76).

> [!tip] Calculator
> `3.85 ÷ 7.08 =` gives 0.5438; `÷ 0.0135 =` gives 40.28; `× 1.0425 =` gives 42.00.

**Required return from the Gordon model** (V5 p.76)
$$
r = \frac{D_0(1+g)}{P_0} + g = \frac{D_1}{P_0} + g
$$
^f-05-02-17

- Solve Formula 9 for $r$ with $V_0 = P_0$; technically an IRR; dividend yield plus capital gains yield (V5 p.76).
- NextEra: $5.275/169.83 + 0.055 = 3.11\% + 5.50\% = 8.60\%$ (V5 p.76).
- Do not feed this $r$ back into the same DDM; that is circular (V5 p.92).

**Two-stage terminal value** (V5 p.79)
$$
V_n = \frac{D_{n+1}}{r - g_L} = \frac{D_0 (1+g_S)^n (1+g_L)}{r - g_L}
$$
^f-05-02-18

- $g_S$: supernormal growth for $n$ years; $g_L$: mature growth thereafter; $D_{n+1} = D_n(1+g_L)$ is the first dividend of stage 2 (V5 p.79).
- $V_n$ is the Gordon value of the stage-2 stream as of the start of stage 2, that is at $t = n$ (V5 p.80).
- Meditec: $0.55 \times 1.09^{10} \times 1.05/(0.0588 - 0.05) = 155.36$ (V5 p.79, p.80).

**Two-stage DDM** (V5 p.79)
$$
V_0 = \sum_{t=1}^{n} \frac{D_0 (1+g_S)^t}{(1+r)^t} + \frac{D_0 (1+g_S)^n (1+g_L)}{(1+r)^n (r - g_L)}
$$
^f-05-02-19

- Formula 4 with $P_n$ replaced by $V_n$ from Formula 18 (V5 p.79).
- The transition from $g_S$ to $g_L$ is abrupt; suited to a temporary advantage such as a patent or first-mover position (V5 p.80).
- The same $r$ is normally used for both stages for simplicity (V5 p.81).

> [!tip] Calculator
> CF worksheet: CF0 = 0, C01 = $D_1$, ..., C0n = $D_n + V_n$ (add the terminal value to the last dividend), `NPV`, I = $r$, `CPT`.
> Meditec check: C01 to C09 = the dividends, C10 = 1.302 + 155.358 = 156.660, I = 5.88 gives 94.21.
> Alternative for many equal-growth years: PV of $V_n$ via `TVM`: N = n, I/Y = r, FV = $V_n$, `CPT PV`.

**Terminal value from a price multiple** (V5 p.81)
$$
V_n = \left(\frac{P}{E}\right)_{\text{trailing}} \times E_n, \qquad E_n = \frac{D_n}{1-b}
$$
^f-05-02-20

- The multiple is applied to the fundamental at $t = n$; when only $D_n$ and the payout ratio are known, back out $E_n$ first (V5 p.81).
- P&G: $E_4 = 3.2639/0.60 = 5.4398$, $V_4 = 22 \times 5.4398 = 119.68$ (V5 p.81).
- Alternatives include a multiple of book value per share (V5 p.61, p.81).

**Valuing a non-dividend-paying stock** (V5 p.82)
$$
V_{n-1} = \frac{D_n}{r-g}, \qquad V_0 = \frac{V_{n-1}}{(1+r)^{n-1}}
$$
^f-05-02-21

- The first dividend $D_n$ is paid at $t = n$ and values the stock at $t = n-1$, one period earlier, because the Gordon numerator is the next dividend (V5 p.82).
- Example 15: $V_4 = 1.00/(0.11 - 0.05) = 16.67$, $V_0 = 16.67/1.11^4 = 10.98$ (V5 p.82).
- Equivalently $V_0 = [D_n/(r-g)]/(1+r)^{n-1}$; discounting $n$ periods is the classic error (V5 p.119).

> [!tip] Calculator
> `1 ÷ 0.06 =` gives 16.67; `TVM`: N = 4, I/Y = 11, FV = 16.67, `CPT PV` gives 10.98.

**H-model** (V5 p.83)
$$
V_0 = \frac{D_0(1+g_L)}{r-g_L} + \frac{D_0 H (g_S - g_L)}{r-g_L} = \frac{D_0(1+g_L) + D_0 H (g_S - g_L)}{r - g_L}
$$
^f-05-02-22

- $H$: half-life of the high-growth period, so the linear decline from $g_S$ to $g_L$ lasts $2H$ years; $g_S$: initial growth; $g_L$: growth after year $2H$ (V5 p.83).
- Derivation: the first term is the Gordon value if growth were $g_L$ from now on; the excess growth in the transition averages $(g_S - g_L)/2$, so over $2H$ years the extra dividends total $2H \times D_0 (g_S - g_L)/2 = D_0 H (g_S - g_L)$; capitalizing that extra amount at $r - g_L$ gives the second term (V5 p.84).
- Because the timing of the extra dividends is not discounted individually, the model is an approximation that overstates value for long transitions and large $g_S - g_L$; move to an explicit spreadsheet in those cases (V5 p.84, p.85).
- When $g_S = g_L$ the second term vanishes and the H-model is the Gordon model (V5 p.92).

> [!tip] Calculator
> Example 16: `1.77 × 1.04 =` gives 1.8408; `1.77 × 5 × 0.03 =` gives 0.2655; `1.8408 + 0.2655 =` gives 2.1063; `÷ 0.04 =` gives 52.66 (the text rounds the numerator to 2.11 and reports 52.75).

**Three-stage DDM with three constant rates** (V5 p.85, p.86)
$$
V_0 = \sum_{t=1}^{n_1} \frac{D_0(1+g_1)^t}{(1+r)^t} + \sum_{t=n_1+1}^{n_2} \frac{D_{n_1}(1+g_2)^{t-n_1}}{(1+r)^t} + \frac{D_{n_2}(1+g_3)}{(r-g_3)(1+r)^{n_2}}
$$
^f-05-02-23

- $g_1, g_2, g_3$: growth in stages 1, 2, 3; $n_1$, $n_2$: ends of stages 1 and 2; the terminal value uses $D_{n_2+1}$ and sits at $t = n_2$ (V5 p.86).
- Every dividend is explicit, so the CF worksheet with $n_2$ entries and $V_{n_2}$ added to the last is the exam method (V5 p.86).
- Technology example: 14% for 2 years, 12% for 5, 6.75% after; $V_7 = 358.59$, value 222.82, 88% from the terminal value (V5 p.86).

**Three-stage DDM with a linearly declining second stage** (V5 p.86, p.88)
$$
V_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r)^t} + \frac{V_n}{(1+r)^n}, \qquad V_n = \frac{D_n(1+g_L) + D_n H (g_S - g_L)}{r - g_L}
$$
^f-05-02-24

- Stage 1: constant $g_S$ for $n$ years, dividends discounted individually; stages 2 and 3: the H-model applied at $t = n$ with $D_n$ in place of $D_0$ and $H$ equal to half the transition length (V5 p.86).
- Four steps: gather inputs, PV the stage-1 dividends, compute the H-value at the start of stage 2 and discount it to today, sum (V5 p.86).
- Rhinestone: $D_5 = 0.9436$, $V_5 = 66.998 + 14.154 = 81.152$, PV 55.231, plus 3.042 of stage-1 dividends gives 58.27 (V5 p.88).

> [!tip] Calculator
> CF worksheet: C01 to C04 = $D_1$ to $D_4$, C05 = $D_5 + V_5$ = 0.9436 + 81.1524 = 82.0960, `NPV`, I = 8, `CPT` gives 58.27.

**Required return from the H-model** (V5 p.92)
$$
r = \frac{D_0}{P_0}\left[(1+g_L) + H(g_S - g_L)\right] + g_L
$$
^f-05-02-25

- Solve Formula 22 for $r$ with $V_0 = P_0$: multiply through by $(r - g_L)$ and divide by $P_0$ (V5 p.92).
- Reduces to Formula 17 when $g_S = g_L$ (V5 p.92).
- Example: $D_0 = 1$, $P_0 = 20$, $g_S = 10\%$ declining over 10 years ($H = 5$) to 6%: $(1/20)(1.06 + 5 \times 0.04) + 0.06 = 0.05 \times 1.26 + 0.06 = 12.3\%$ (V5 p.92).

> [!tip] Calculator
> `0.10 - 0.06 = × 5 + 1.06 =` gives 1.26; `× 1 ÷ 20 =` gives 0.063; `+ 0.06 =` gives 0.123.

**IRR of any DDM** (V5 p.92, p.93)
$$
P_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r)^t} + \frac{D_{n+1}}{(r-g_L)(1+r)^n} \quad \text{solve for } r
$$
^f-05-02-26

- No closed form for two-stage or spreadsheet streams; use trial and error, starting from the Gordon approximation $D_1/P_0 + g_L$ and moving up if the early growth exceeds $g_L$ (V5 p.92).
- JNJ: first guess 7.8%; at 8% value 140.07 (above the 136.61 price), at 8.5% value 119.92 (below), so the IRR is just above 8%, 8.08% by Goal Seek (V5 p.92, p.93).
- The same equation solved for $g_L$ instead of $r$ gives the implied terminal growth consistent with price (V5 p.124).

> [!tip] Calculator
> The BA II Plus IRR needs a finite stream, so put the Gordon terminal value in the last cash flow at a trial $r$, then iterate: CF0 = -136.61, C01 to C05 = $D_1$ to $D_5$, C06 = $D_6 + D_7/(r - 0.05)$, `IRR CPT`; recompute C06 at the new $r$ until it stops moving.

**Sustainable growth rate** (V5 p.94)
$$
g = b \times ROE
$$
^f-05-02-27

- $b$: earnings retention rate = 1 - payout ratio; ROE ideally on beginning-of-period equity; strictly, $b$ times the return on new investment, approximated by ROE (V5 p.94, p.96).
- Reason: with no new share issues and constant leverage, equity grows by retained earnings, $bE$, which is $b \times ROE$ of beginning equity; constant ROE then makes earnings and dividends grow at the same rate (V5 p.94, p.95).
- Example 22: ROE 25%, $b = 60\%$: $g = 15\%$; equity 1,000,000 becomes 1,150,000, income 250,000 becomes 287,500, dividends 100,000 become 115,000, all up 15% (V5 p.95).
- Lower payout raises growth, the dividend displacement of earnings, though evidence shows higher-payout companies have sometimes grown faster (V5 p.95).

**DuPont decomposition of ROE** (V5 p.96)
$$
ROE = \frac{NI}{\text{Equity}} = \frac{NI}{\text{Sales}} \times \frac{\text{Sales}}{\text{Total assets}} \times \frac{\text{Total assets}}{\text{Equity}}
$$
^f-05-02-28

- Profit margin times asset turnover (together ROA) times the equity multiplier (V5 p.96).
- Leverage raises ROE only when the company borrows at a rate below what it earns on assets (V5 p.96).
- IBM's 52% ROE came from 7.35 times leverage on a 11% margin and 0.65 turnover versus a benchmark of 2.07, 10.5% and 0.62 (V5 p.98).

**PRAT model of sustainable growth** (V5 p.96)
$$
g = \frac{NI - \text{Dividends}}{NI} \times \frac{NI}{\text{Sales}} \times \frac{\text{Sales}}{\text{Total assets}} \times \frac{\text{Total assets}}{\text{Equity}}
$$
^f-05-02-29

- P: profit margin; R: retention; A: asset turnover; T: leverage; ROA and the two financial policies determine growth (V5 p.96).
- Holds exactly with beginning equity; databases often use average assets and equity, and Practice Problem 34 mixes average assets with beginning equity (V5 p.96, p.123).
- IBM mature forecast: $0.105 \times 0.62 \times 2.0 = 13.0\%$ ROE, $g = 0.50 \times 13.0\% = 6.5\%$ (V5 p.98, p.99).

> [!tip] Calculator
> Practice Problem 34: `43923 - 1518 = ÷ 43923 =` gives 0.9654; `× 43923 ÷ 423474 =` gives 0.1001; `× 423474 ÷ 486203 =` gives 0.0872; `× 486203 ÷ 397925 =` gives 0.1066.
> Shortcut: retention times NI divided by beginning equity, `42405 ÷ 397925 =` gives 0.1066, because the middle ratios cancel.

## Worked examples

### Example 1: value as the present value of future cash flows (V5 p.52)

Setup: cash flows of 100, 150 and 200 at $t = 1, 2, 3$; discount rate 10%.

$V_0 = 100/1.10 + 150/1.10^2 + 200/1.10^3 = 90.909 + 123.967 + 150.263 = 365.14$.
$V_1 = 150/1.10 + 200/1.10^2 = 136.364 + 165.289 = 301.65$.
Consistency: $V_0 = (100 + 301.653)/1.10 = 90.909 + 274.230 = 365.14$.
The value at any date is the present value of the cash flows after that date, so discounting $CF_1$ and $V_1$ is the same as discounting all three flows (V5 p.52).
Python check: `100/1.1+150/1.1**2+200/1.1**3 = 365.139`, `150/1.1+200/1.1**2 = 301.653`. ^ex-05-02-1

### Example 2: AB InBev and Diageo, is the DDM appropriate (V5 p.54, p.55)

Setup: fifteen years of EPS, DPS and payout for BUD and DEO.

Part 1, AB InBev.
Dividends ranged from $0.35 to $4.33 and payout from 18% to 542%, driven by serial mergers (Interbrew-AmBev, Anheuser-Busch in 2008, SABMiller in 2016), and the 2018 dividend was cut to prioritize debt paydown.
Dividends bear no consistent relation to profitability, so a DDM is inappropriate; a company-level cash flow definition is preferred (V5 p.55).

Part 2, Diageo.
EPS and DPS grew at compound rates of 6.8% and 6.3% with payout mostly between 50% and 60%, and the company targets dividend cover of 1.8 to 2.2 times (payout 45% to 56%).
Dividend-paying with an understandable, consistent policy, so the DDM is appropriate (V5 p.55).
Python check: `1/2.2 = 0.4545`, `1/1.8 = 0.5556`. ^ex-05-02-2

### Example 3: DDM value with a single holding period (V5 p.59)

Setup: Carrefour, $D_1 = 0.46$, $P_1 = 23.00$, $r = 8\%$.

$V_0 = (0.46 + 23.00)/1.08 = 23.46/1.08 = 21.72$ (Formula 2).
Python check: `23.46/1.08 = 21.722`. ^ex-05-02-3

### Example 4: stock price for a five-year forecast horizon (V5 p.60)

Setup: dividends 2.00, 2.10, 2.20, 3.50, 3.75; $P_5 = 40.00$; $r = 10\%$.

PV of dividends: $1.818 + 1.736 + 1.653 + 2.391 + 2.328 = 9.926$.
PV of price: $40/1.10^5 = 24.837$.
$V_0 = 9.926 + 24.837 = 34.76$ (Formula 4).
Calculator: CF0 = 0, C01 = 2.00, C02 = 2.10, C03 = 2.20, C04 = 3.50, C05 = 43.75, NPV at I = 10 gives 34.76.
Python check: `sum([2/1.1,2.1/1.1**2,2.2/1.1**3,3.5/1.1**4,3.75/1.1**5]) = 9.926`, `40/1.1**5 = 24.837`, total `34.762`. ^ex-05-02-4

### Example 5: Sonoco, Gordon growth model (1) (V5 p.64, p.65)

Setup: $D_0 = 4 \times 0.41 = 1.64$, $g = 4.5\%$, beta 0.95, ERP 4.5%, $R_F = 3\%$, price 59.55.

Part 1: $r = 3.0 + 0.95 \times 4.5 = 7.3\%$ (Formula 7).
$V_0 = 1.64 \times 1.045/(0.073 - 0.045) = 1.7138/0.028 = 61.21$ (Formula 9).

Part 2: price 59.55 is 1.66, or 2.7%, below 61.21, so Sonoco appears slightly undervalued (V5 p.65).
Python check: `1.64*1.045/0.028 = 61.207`, `(61.21-59.55)/61.21 = 0.0271`. ^ex-05-02-5

### Example 6: Middlesex Water, Gordon growth model (2) (V5 p.65 to p.67)

Setup: $D_0 = 0.911$, $g = 4.5\%$, raw beta 0.70 and adjusted beta 0.80 with $R^2$ under 20%, pretax cost of debt 4.8%, Kim's $r = 6.8\%$, price 43.20.

Part 1: $V_0 = 0.911 \times 1.045/(0.068 - 0.045) = 0.952/0.023 = 41.39$.

Part 2: 41.39 is 4.2% below 43.20, a difference under 5%, so fairly valued (V5 p.66).

Part 3: the Gordon model fits because ROE is stable (regulated water utility), payout is a predictable 60% to 70%, 4.5% growth is comparable with roughly 4.3% US nominal GDP growth over 1998 to 2018, and no period of very high or low growth is forecast (V5 p.66).

Part 4: CAPM with adjusted beta, $3 + 0.80 \times 4.5 = 6.6\%$ (V5 p.66).

Part 5A: $0.911 \times 1.045/(0.066 - 0.045) = 0.952/0.021 = 45.33$.
Part 5B: bond yield plus risk premium $4.8 + 2.5 = 7.3\%$; $0.952/(0.073 - 0.045) = 0.952/0.028 = 34.00$ (V5 p.67).

Part 6: at 6.6% the value is 4.9% above price, still fairly valued; at 7.3% the value is 21% below price, significantly overvalued, but the 2.5% premium has no specific support and beta explains under 20% of return variance.
Uncertainty in $r$ lowers confidence in an overvalued call; on balance the stock is relatively fairly valued (V5 p.67).
Python check: `0.911*1.045/0.023 = 41.391`, `0.911*1.045/0.021 = 45.333`, `0.911*1.045/0.028 = 34.000`, `(45.33-43.2)/43.2 = 0.049`, `(34-43.2)/43.2 = -0.213`. ^ex-05-02-6

### Example 7: MSEX sensitivity, Gordon growth model (3) (V5 p.67, p.68)

Setup: vary $r$ and $g$ by 25 bps around 6.8% and 4.5%.

| | g = 4.25% | g = 4.50% | g = 4.75% |
|---|---|---|---|
| r = 6.55% | 41.29 | 46.44 | 53.02 |
| r = 6.80% | 37.24 | 41.39 | 46.55 |
| r = 7.05% | 33.92 | 37.33 | 41.49 |

The widest spread (7.05% less 4.25%) gives the smallest value 33.92; the narrowest (6.55% less 4.75%) gives 53.02, 56% larger.
Two-thirds of the grid is below the 43.20 price, but all but four cells are within 10% of it, supporting fairly valued or slightly overvalued (V5 p.68).
Python check: `0.911*1.0425/(0.0705-0.0425) = 33.92`, `0.911*1.0475/(0.0655-0.0475) = 53.02`, `53.02/33.92-1 = 0.563`. ^ex-05-02-7

### Example 8: non-callable fixed-rate perpetual preferred (V5 p.69)

Setup: KSU-P, 4% on $25 par, $r = 5.5\%$.

$D = 0.04 \times 25 = 1.00$; $V_0 = 1.00/0.055 = 18.18$ (Formula 10).
Python check: `1/0.055 = 18.182`. ^ex-05-02-8

### Example 9: Gordon growth with negative growth (V5 p.69)

Setup: Afton Mines, $D_1 = 4.25$, $g = -4\%$, $r = 9\%$.

$V_0 = 4.25/[0.09 - (-0.04)] = 4.25/0.13 = 32.69$.
The negative growth widens the spread, and the 4.25 is already $D_1$, so no $(1+g)$ factor is applied (V5 p.69).
Python check: `4.25/0.13 = 32.692`. ^ex-05-02-9

### Example 10: the growth rate implied by the current price (V5 p.71, p.72)

Setup: beta 1.1, $R_F = 5.6\%$, ERP 6%, $D_0 = 2.00$, $g = 5\%$, price 40.

Part 1: $r = 5.6 + 1.1 \times 6 = 12.2\%$; $V_0 = 2.00 \times 1.05/(0.122 - 0.05) = 2.10/0.072 = 29.17$.

Part 2: $40 = 2.00(1+g)/(0.122 - g)$; $4.88 - 40g = 2 + 2g$; $42g = 2.88$; $g = 6.86\%$ (Formula 12).
The market prices growth of 6.86% against the analyst's 5%, so the analyst's inputs imply the stock is overvalued (V5 p.72).
Python check: `2.1/0.072 = 29.167`, `(40*0.122-2)/42 = 0.0686`. ^ex-05-02-10

### Example 11: justified P/E for L'Oreal (V5 p.75, p.76)

Setup: price 242.70, trailing EPS 7.08, $D_0 = 3.85$, $g = 4.25\%$, $R_F = 2\%$, ERP 5%, beta 0.72.

Part 1: $r = 2.0 + 0.72 \times 5.0 = 5.6\%$; payout $1 - b = 3.85/7.08 = 0.5438$.
Justified leading P/E $= 0.5438/(0.056 - 0.0425) = 0.5438/0.0135 = 40.28$ (Formula 15).
Justified trailing P/E $= 0.5438 \times 1.0425/0.0135 = 42.00$ (Formula 16).

Part 2: actual trailing P/E $= 242.70/7.08 = 34.3 < 42.0$, so undervalued.
In price terms, $3.85 \times 1.0425/(0.056 - 0.0425) = 297.31$, above 242.70; the text prints the denominator as $0.05 - 0.0425$, a typo, since $0.056 - 0.0425$ reproduces 297.31 (V5 p.76).
Python check: `3.85/7.08 = 0.5438`, `0.5438/0.0135 = 40.28`, `0.5438*1.0425/0.0135 = 41.99`, `242.7/7.08 = 34.28`, `3.85*1.0425/0.0135 = 297.31`. ^ex-05-02-11

### Example 12: expected return from the Gordon model, NextEra (V5 p.76, p.77)

Setup: annualized dividend 5.00, $g = 5.5\%$, price 169.83.

$D_1 = 5.00 \times 1.055 = 5.275$; $r = 5.275/169.83 + 0.055 = 0.0311 + 0.055 = 8.60\%$ (Formula 17).
Components: dividend yield 3.11%, capital gains yield 5.50% (V5 p.77).
Python check: `5.275/169.83+0.055 = 0.0861`. ^ex-05-02-12

### Example 13: Carl Zeiss Meditec, two-stage DDM (V5 p.79, p.80)

Setup: $D_0 = 0.55$, $g_S = 9\%$ for 10 years, $g_L = 5\%$, $r = 1.2 + 0.90 \times 5.2 = 5.88\%$, price 80.55.

| t | $D_t$ | PV at 5.88% |
|---|---|---|
| 1 | 0.600 | 0.5662 |
| 2 | 0.653 | 0.5829 |
| 3 | 0.712 | 0.6001 |
| 4 | 0.776 | 0.6178 |
| 5 | 0.846 | 0.6360 |
| 6 | 0.922 | 0.6547 |
| 7 | 1.005 | 0.6740 |
| 8 | 1.096 | 0.6938 |
| 9 | 1.195 | 0.7143 |
| 10 | 1.302 | 0.7353 |

$V_{10} = 0.55 \times 1.09^{10} \times 1.05/(0.0588 - 0.05) = 1.3671/0.0088 = 155.36$ (Formula 18); PV $= 155.36/1.0588^{10} = 87.74$.
Sum of dividend PVs 6.475; $V_0 = 6.475 + 87.74 = 94.21$, versus the 80.55 price.
About 93% of value is the terminal value, so the answer is only as good as $g_L$ and $r$ (V5 p.80).
Python check: two-stage function gives `sumPVdiv = 6.4750`, `V10 = 155.358`, `PV = 87.7395`, `total = 94.2145`. ^ex-05-02-13

### Example 14: P&G, DDM combined with a P/E terminal value (V5 p.81)

Setup: price 96.47, $D_0 = 2.79$, $g = 4\%$ for 4 years, payout 60% and trailing P/E 22 at year 4, $r = 6.5\%$.

Dividends: 2.9016, 3.0177, 3.1384, 3.2639; PVs 2.7245, 2.6606, 2.5981, 2.5371, sum 10.52.
$E_4 = 3.2639/0.60 = 5.4398$; $V_4 = 22 \times 5.4398 = 119.68$ (Formula 20); PV $= 119.68/1.065^4 = 93.03$.
$V_0 = 10.52 + 93.03 = 103.55$, above the 96.47 price (V5 p.81).
Calculator: C01 = 2.9016, C02 = 3.0177, C03 = 3.1384, C04 = 3.2639 + 119.6765 = 122.9404, I = 6.5, NPV = 103.55.
Python check: `sum PV = 10.520`, `E4 = 5.4398`, `V4 = 119.677`, `PV V4 = 93.027`, `total = 103.548`. ^ex-05-02-14

### Example 15: valuing a non-dividend-paying stock (V5 p.82)

Setup: first dividend 1.00 at $t = 5$, growth 5% after, $r = 11\%$.

$V_4 = D_5/(r - g) = 1.00/(0.11 - 0.05) = 16.67$ (Formula 21).
$V_0 = 16.67/1.11^4 = 10.98$.
The value sits at $t = 4$ because the Gordon numerator is the next dividend; discounting five periods would give 9.89 and is the trap (V5 p.82).
Python check: `1/0.06 = 16.667`, `16.667/1.11**4 = 10.979`. ^ex-05-02-15

### Example 16: valuing a stock with the H-model (V5 p.84, p.85)

Setup: price 41.70, $D_0 = 1.77$, $g_S = 7\%$ declining linearly over 10 years ($H = 5$) to $g_L = 4\%$, $r = 8\%$.

Part 1: $V_0 = [1.77 \times 1.04 + 1.77 \times 5 \times (0.07 - 0.04)]/(0.08 - 0.04) = (1.8408 + 0.2655)/0.04 = 2.1063/0.04 = 52.66$ (Formula 22).
The text rounds the numerator to $1.84 + 0.27 = 2.11$ and reports 52.75; the unrounded answer is 52.66, and either rounds to the same exam choice.

Part 2: with normal growth from now, value is the first term only, $1.8408/0.04 = 46.02$ (text 46); the supernormal period adds $0.2655/0.04 = 6.64$ (text 6.75).

Part 3: 52.75 is about 26% above 41.70, so undervalued (V5 p.85).
Python check: `(1.77*1.04+1.77*5*0.03)/0.04 = 52.6575`, `1.8408/0.04 = 46.02`, `0.2655/0.04 = 6.64`, `52.75/41.7-1 = 0.265`. ^ex-05-02-16

### Example 17: three-stage DDM with three distinct stages (V5 p.85, p.86)

Setup: $D_0 = 3.30$, 14% for 2 years, 12% for 5 years, 6.75% thereafter, $r = 9\%$, price 194.98.

| t | $D_t$ | PV at 9% |
|---|---|---|
| 1 | 3.7620 | 3.4514 |
| 2 | 4.2887 | 3.6097 |
| 3 | 4.8033 | 3.7090 |
| 4 | 5.3797 | 3.8111 |
| 5 | 6.0253 | 3.9160 |
| 6 | 6.7483 | 4.0238 |
| 7 | 7.5581 | 4.1346 |

$V_7 = 7.5581 \times 1.0675/(0.09 - 0.0675) = 8.0683/0.0225 = 358.59$ (Formula 23); PV $= 358.59/1.09^7 = 196.16$.
Dividend PVs sum to 26.66; $V_0 = 26.66 + 196.16 = 222.82$, 14% above the price; the terminal value is 88% of the total (V5 p.86).
Calculator: C01 to C06 as above, C07 = 7.5581 + 358.5908 = 366.1489, I = 9, NPV = 222.82.
Python check: `V7 = 358.591`, `PV = 196.161`, `sum div PV = 26.656`, `total = 222.817`, `196.16/222.82 = 0.880`. ^ex-05-02-17

### Example 18: Rhinestone Energy, three-stage DDM with declining stage 2 (V5 p.87 to p.89)

Setup: price 56.18, $D_0 = 0.56$, 11% for 5 years, then linear decline over 10 years to 6.5%, adjusted beta 1.2, ERP 4.2%, $R_F = 3\%$, fair value band plus or minus 20%.

Part 1: $r = 3 + 1.2 \times 4.2 = 8.04\%$, stated to one decimal as 8% (V5 p.87).

Part 2: stage-1 dividends 0.6216, 0.6900, 0.7659, 0.8501, 0.9436 with PVs 0.5756, 0.5915, 0.6080, 0.6249, 0.6422, sum 3.0422.
$D_5 = 0.56 \times 1.11^5 = 0.9436$, $H = 5$.
$V_5 = 0.9436 \times 1.065/0.015 + 0.9436 \times 5 \times 0.045/0.015 = 66.998 + 14.154 = 81.152$ (Formula 24).
PV of $V_5 = 81.152/1.08^5 = 55.231$.
$V_0 = 3.042 + 55.231 = 58.27$ (V5 p.88).

Part 3: stage 1 is $3.042/58.273 = 5.2\%$ of value; stages 2 and 3 are 94.8% (V5 p.88).

Part 4: band $58.27 \pm 11.65$ runs 46.62 to 69.92; the 56.18 price is inside, so fairly valued (V5 p.88).

Part 5: flat dividend in year 2 (0.6216 again), then 11% growth resumes, so $D_5 = 0.8501$.
PVs 0.5756, 0.5329, 0.5477, 0.5629, 0.5786, sum 2.798.
$V_5 = 0.8501 \times 1.065/0.015 + 0.8501 \times 5 \times 0.045/0.015 = 73.110$; PV $= 49.758$; $V_0 = 52.56$ (V5 p.89).
Python check: `V5 = 81.1524`, `PV = 55.2310`, `total = 58.2731`, `3.0422/58.2731 = 0.0522`, flat case `V5 = 73.1103`, `total = 52.5553`. ^ex-05-02-18

### Example 19: Yang Co., varying dividend assumptions (V5 p.90, p.91)

Setup: $D_1 = 21$, then minus 10% a year for three years, $D_5 = 60$ after an asset sale, $D_6 = D_7 = 40$, 5% growth after year 7, $r = 12\%$.

| t | $D_t$ | PV at 12% |
|---|---|---|
| 1 | 21.00 | 18.75 |
| 2 | 18.90 | 15.07 |
| 3 | 17.01 | 12.11 |
| 4 | 15.31 | 9.73 |
| 5 | 60.00 | 34.05 |
| 6 | 40.00 | 20.27 |
| 7 | 40.00 | 18.09 |

$V_7 = 40 \times 1.05/(0.12 - 0.05) = 42/0.07 = 600$; PV $= 600/1.12^7 = 271.41$.
$V_0 = 128.06 + 271.41 = 399.48$ (V5 p.91).
Calculator: C01 = 21, C02 = 18.9, C03 = 17.01, C04 = 15.31, C05 = 60, C06 = 40, C07 = 640, I = 12, NPV = 399.48.
Python check: `sum div PV = 128.058`, `600/1.12**7 = 271.410`, `total = 399.468`. ^ex-05-02-19

### Example 20: a sustainable growth rate calculation (V5 p.91)

Setup: payout 25%, mature ROE set equal to $r = 9\%$.

$g = b \times ROE = 0.75 \times 9\% = 6.75\%$ (Formula 27).
Setting ROE = $r$ encodes the mature-phase assumption that new investment just earns the cost of equity (V5 p.91).
Python check: `0.75*0.09 = 0.0675`. ^ex-05-02-20

### Example 21: expected return for varying dividends, JNJ (V5 p.92, p.93)

Setup: $D_0 = 3.60$, 7% for 6 years, 5% after, price 136.61.

First approximation from Gordon at $g_L$: $3.60 \times 1.07/136.61 + 0.05 = 7.8\%$; the true IRR must be higher because early growth exceeds 5%.
At $r = 8\%$: PV of $D_1$ to $D_6$ (3.8520 to 5.4025) is 20.91; $D_7 = 5.6726$; PV of $V_6 = [5.6726/0.03]/1.08^6 = 119.16$; total 140.07, above price.
At $r = 8.5\%$: 20.58 + 99.34 = 119.92, below price.
IRR is slightly above 8%; Goal Seek gives 8.08% (V5 p.93).
Python check: at 8% `20.911 + 119.160 = 140.071`, at 8.5% `20.579 + 99.345 = 119.924`, bisection IRR `0.0808`. ^ex-05-02-21

### Example 22: showing g = b x ROE (V5 p.95)

Setup: ROE 25%, retention 60%, opening equity 1,000,000, income 250,000, dividends 100,000.

$g = 0.60 \times 25\% = 15\%$.
Next year's equity $= 1{,}000{,}000 + 0.60 \times 250{,}000 = 1{,}150{,}000$; income $= 0.25 \times 1{,}150{,}000 = 287{,}500$, up $37{,}500/250{,}000 = 15\%$.
Retained $0.60 \times 287{,}500 = 172{,}500$; dividends $0.40 \times 287{,}500 = 115{,}000$, up 15% from 100,000.
With constant ROE on reinvested earnings and no new shares, dividends keep growing at 15% (V5 p.95).
Python check: `0.25*1150000 = 287500`, `115000/100000-1 = 0.15`. ^ex-05-02-22

### Example 23: ROA, financial policies and the dividend growth rate (V5 p.97)

Setup: Baggai ROA 10%, retention 30%, equity multiplier 1.25; Mondale ROA 10%, retention 2/3, multiplier 2.00.

Part 1: Baggai $g = 0.30 \times 10\% \times 1.25 = 3.75\%$; Mondale $g = (2/3) \times 10\% \times 2.00 = 13.33\%$ (Formula 29 with ROA = margin times turnover).

Part 2: identical ROA, so the entire gap comes from Mondale's higher retention and higher leverage (V5 p.97).
Python check: `0.3*0.1*1.25 = 0.0375`, `(2/3)*0.1*2 = 0.1333`. ^ex-05-02-23

### Example 24: forecasting growth with the PRAT formula, IBM (V5 p.97 to p.99)

Setup: 2018 ROE 52% (margin 11.0%, turnover 0.65, leverage 7.35), ten-year average retention 62%; benchmark ROE 13.5% (margin 10.5%, turnover 0.62, leverage 2.07); analyst forecasts benchmark margin and turnover, leverage 2.0, payout 50%.

Applying $g = 0.62 \times 52\%$ would give an implausible 32% given falling sales, earnings and capex.
Mature ROE $= 10.5\% \times 0.62 \times 2.0 = 13.0\%$ (Formula 28); $g = 0.50 \times 13.0\% = 6.5\%$ (V5 p.99).
IBM's ROE exceeded the benchmark almost entirely through leverage, which is what the analyst normalizes (V5 p.98).
Python check: `0.105*0.62*2 = 0.1302`, `0.5*0.1302 = 0.0651`. ^ex-05-02-24

### Example 25: Hoshino Distributors, dividends from detailed pro forma assumptions (V5 p.99, p.100)

Setup: sales 100 in year 1 growing 20%, 15%, 10%, 10%; EBIT margin 20%, 20%, 18%, 16%, 16%; interest 10% of current debt; tax 40%; payout 20%, 20%, 30%, 40%, 50%; assets 80% of sales; year-1 debt 40 and equity 40; debt = assets minus equity; equity grows by prior-year retained earnings; 4 million shares; $r = 15\%$; year-5 value 10 times earnings (millions).

| | Y1 | Y2 | Y3 | Y4 | Y5 |
|---|---|---|---|---|---|
| Sales | 100.00 | 120.00 | 138.00 | 151.80 | 166.98 |
| EBIT | 20.00 | 24.00 | 24.84 | 24.29 | 26.72 |
| Interest | 4.00 | 4.83 | 5.35 | 5.64 | 6.18 |
| EBT | 16.00 | 19.17 | 19.49 | 18.65 | 20.54 |
| Taxes | 6.40 | 7.67 | 7.80 | 7.46 | 8.22 |
| Net income | 9.60 | 11.50 | 11.69 | 11.19 | 12.32 |
| Dividends | 1.92 | 2.30 | 3.51 | 4.48 | 6.16 |
| Total assets | 80.00 | 96.00 | 110.40 | 121.44 | 133.58 |
| Debt | 40.00 | 48.32 | 53.52 | 56.38 | 61.81 |
| Equity | 40.00 | 47.68 | 56.88 | 65.06 | 71.77 |

Mechanics for year 2: equity $= 40 + (9.60 - 1.92) = 47.68$; assets $= 0.8 \times 120 = 96$; debt $= 96 - 47.68 = 48.32$; interest $= 4.83$; EBT $= 24 - 4.83 = 19.17$; NI $= 11.50$; dividends $= 2.30$.
DPS: 0.480, 0.575, 0.877, 1.120, 1.540; PVs at 15%: 0.417, 0.435, 0.577, 0.640, 0.766, sum 2.84.
$EPS_5 = 12.32/4 = 3.08$; $P_5 = 10 \times 3.08 = 30.80$; PV $= 30.80/1.15^5 = 15.31$.
$V_0 = 2.84 + 15.31 = 18.15$ per share (V5 p.100).
Python check (full rebuild of the model): `sum PV DPS = 2.834`, `EPS5 = 3.080`, `PV P5 = 15.315`, `total = 18.150`; year-4 debt and equity come out 56.37 and 65.07 before rounding. ^ex-05-02-25

## Item-set patterns

> [!warning] Trap 1: D0 versus D1 in the Gordon numerator
> The vignette says "the dividend just paid" or "the current annual dividend" and gives $g$; the answer set includes $D_0/(r-g)$.
> Correct: grow the dividend once, $D_0(1+g)/(r-g)$; but if the vignette says "expected to pay next year", the figure is already $D_1$ and must not be grown again (Afton Mines, Practice Problem 11).
> Distractors: $D_0/(r-g)$ (the no-growth numerator) and $D_0(1+g)^2/(r-g)$ (grown twice), both tempting because the arithmetic looks complete (V5 p.63, p.69).

> [!warning] Trap 2: which period the terminal value sits in
> A two-stage table gives $D_1$ to $D_n$ and asks for value; the terminal value is built from $D_{n+1}$ and discounted $n$ periods, not $n+1$.
> For a stock that starts paying at $t = n$, the Gordon value sits at $t = n - 1$ and is discounted $n - 1$ periods.
> Distractors: $V_n$ computed with $D_n$ instead of $D_{n+1}$, or $V_n$ discounted one extra period (19.58 versus the correct 21.54 in Practice Problem 11) (V5 p.79, p.82, p.119).

> [!warning] Trap 3: the H in the H-model is half the transition, and the decline starts from the current dividend
> The vignette says growth declines linearly "over the next 10 years"; $H = 5$, not 10.
> Correct: $V_0 = [D_0(1+g_L) + D_0 H(g_S - g_L)]/(r - g_L)$; the required-return version is $(D_0/P_0)[(1+g_L) + H(g_S - g_L)] + g_L$.
> Distractors: using $2H$ for $H$ (roughly doubles the growth add-on), using $D_1$ in place of $D_0$, and using $g_S$ in the first term (V5 p.83, p.92, p.122).

> [!warning] Trap 4: PVGO ranking versus growth component of P/E ranking
> An exhibit lists $r$, $E_1$ and price for three stocks and asks first for the largest PVGO, then for the largest growth component of the leading P/E.
> Correct: PVGO $= P_0 - E_1/r$ in currency; growth component $= \text{PVGO}/E_1$; the rankings can differ (BKKQ wins on PVGO, CPMN on PVGO/E1).
> Distractors: assuming the two rankings coincide, or ranking by P/E itself, or computing $E_1/r$ with $E_0$ (V5 p.73, p.74, p.119, p.120).

> [!warning] Trap 5: leading versus trailing justified P/E and which payout ratio to use
> The vignette gives last year's payout and an expected future payout, plus price, $E_0$ and $E_1$.
> Correct: leading P/E $= (1-b)/(r-g)$ with the expected payout; trailing $= (1-b)(1+g)/(r-g)$; compare leading with $P_0/E_1$ and trailing with $P_0/E_0$, never cross.
> Distractors: using the most recent 70% payout instead of the expected 60% (20.0 versus 17.1 in Practice Problem 22), or the trailing formula when the question says leading (17.7) (V5 p.75, p.120).

> [!warning] Trap 6: fairly valued means inside the stated band, and the band is around value, not price
> The analyst "considers a security within plus or minus 10% of intrinsic value to be fairly valued".
> Correct: band $= V_0 \pm 0.10 V_0$; the price is compared with that band; a price below the lower bound means undervalued.
> Distractors: building the band around the price, or calling any gap "overvalued" without checking the band, or reading undervalued as "price above value" (V5 p.88, p.110, p.120).

> [!warning] Trap 7: implied growth versus sustainable growth
> A mature company's price implies growth of 5.3%; ROE and payout give $g = b \times ROE = 4.9\%$.
> Correct: implied $g$ above the sustainable or analyst $g$ means the market is paying for growth the company cannot deliver, so the stock is overvalued; implied below means undervalued.
> Distractors: reversing the sign of the conclusion, or using the payout ratio instead of retention in $b \times ROE$ (3.3% instead of 4.9%) (V5 p.72, p.119).

> [!warning] Trap 8: model selection from a company description
> Three company blurbs: patent expiry then a "steady decline over three years", dividends "held flat for six years then GDP growth", "27% for two years then 12% for ten years then mature".
> Correct: linear decline in stage 2 means a three-stage model with an H-model tail; an abrupt step means the general two-stage or three-stage form; a stable payout with three distinct stages means the three-stage model.
> Distractors: picking the H-model for any company with a transition, or the Gordon model for a company whose stated growth exceeds nominal GDP for years (V5 p.85, p.86, p.121).

> [!warning] Trap 9: the DDM is not ruled out by a dividend suspension, and FCF is not ruled out by a takeover
> Statements such as "a DDM cannot be applied if dividends are suspended for a few years" or "FCF is inappropriate if the firm becomes a takeover candidate".
> Correct: a multistage DDM with zero dividends in stage 1 is valid (Example 15); a control perspective, which a takeover implies, is exactly when FCF is preferred; the DDM is favoured when payout is consistent with earnings.
> Distractors: both statements sound like textbook limitations and reverse the actual rules (V5 p.53, p.57, p.82, p.118).

> [!warning] Trap 10: DuPont data with mixed averaging
> The exhibit gives net income, sales, average total assets, beginning equity and dividends and asks for sustainable growth.
> Correct: multiply retention, margin, turnover and leverage as given; the assets cancel, so $g$ equals retained earnings over beginning equity (10.66%).
> Distractors: ROE alone (11.04%), retention times ROE with a leverage ratio using ending equity, or using payout instead of retention (V5 p.96, p.123).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM02-Discounted-Dividend-Valuation-Practice-Problems]]

## Cross-links

- [[LM01-Equity-Valuation-Applications-and-Processes]]: supplies the intrinsic value versus price framework, the required return estimates (CAPM, adjusted beta, bond yield plus risk premium) and the definition of expected return when price differs from value that this module discounts dividends with.
- [[LM03-Free-Cash-Flow-Valuation]]: takes the FCFF and FCFE definitions sketched here (cash from operations less capex, less net payments to debt) and builds the company-level models used when dividends are absent or unrelated to FCFE, or when the investor has control.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: the justified leading and trailing P/E derived here from the Gordon model are the fundamental multiples in that module, and the P/E times terminal EPS approach to terminal value is developed there.
- [[LM05-Residual-Income-Valuation]]: residual income, book value plus the present value of earnings above the required return, is the third cash flow definition introduced here and is the model of choice when free cash flow is negative within the horizon.
- [[LM01-Analysis-of-Dividends-and-Share-Repurchases]]: dividend policy, payout stability and the wealth-neutrality of buybacks at market prices determine whether a dividend stream is forecastable and how repurchases feed the per-share growth rate used in a DDM.
- [[LM03-Cost-of-Capital-Advanced-Topics]]: the cost of equity that discounts every dividend here is estimated there, including the DDM-implied cost of equity, which is this module's required return from the Gordon and H-models seen from the issuer's side.

## Self-test

Vignette A for Q1 to Q4: Meridian Utilities just paid an annual dividend of 2.40 and expects dividends to grow at 4% indefinitely.
Beta is 0.9, the risk-free rate 3% and the equity risk premium 5%.
The stock trades at 68.00 and consensus EPS for next year is 5.20.

> [!question] Q1
> The Gordon growth value of Meridian is closest to:
> A. 68.57.
> B. 71.31.
> C. 74.17.

> [!question] Q2
> Using the market price, the present value of growth opportunities per share is closest to:
> A. -1.33.
> B. 1.98.
> C. 69.33.

> [!question] Q3
> The justified leading P/E and the actual leading P/E, respectively, are closest to:
> A. 13.7 and 13.1.
> B. 14.3 and 13.1.
> C. 13.7 and 14.3.

> [!question] Q4
> The dividend growth rate implied by the 68.00 price is closest to:
> A. 3.67%.
> B. 3.84%.
> C. 4.00%.

Vignette B for Q5 to Q7: Orlen Devices just paid 1.00; an analyst forecasts 20% growth for three years and 5% thereafter, with a required return of 10%.
A colleague argues that growth will instead decline linearly from 20% to 5% over the same three years.
A third company, Pallon, pays no dividend now but is expected to pay 2.00 at the end of year 4, growing 6% a year thereafter; its required return is 11%.

> [!question] Q5
> The two-stage DDM value of Orlen is closest to:
> A. 28.36.
> B. 29.54.
> C. 30.84.

> [!question] Q6
> Using the colleague's assumption and the H-model, the value of Orlen is closest to, and the reason it differs from Q5 is:
> A. 25.50, because the H-model pays less than 20% in years 2 and 3.
> B. 30.00, because the H-model adds the full three years of excess growth.
> C. 21.00, because the H-model ignores supernormal growth.

> [!question] Q7
> The value of Pallon today is closest to:
> A. 26.35.
> B. 29.25.
> C. 31.00.

Vignette C for Q8 to Q10: Pallas Foods trades at 50.00 and just paid 1.50; its dividend growth of 9% is expected to decline linearly over eight years to 4%.
Sable Corp reports net income 120, sales 1,500, average total assets 2,000, beginning equity 800 and dividends 45.
Tarn Ltd just paid 2.00; dividends will grow 12% for two years, then decline linearly over six years to 4%; the required return is 9%.

> [!question] Q8
> The expected return on Pallas implied by its price under the H-model is closest to:
> A. 7.12%.
> B. 7.72%.
> C. 8.32%.

> [!question] Q9
> Sable's sustainable growth rate using the PRAT decomposition is closest to:
> A. 5.63%.
> B. 9.38%.
> C. 15.00%.

> [!question] Q10
> The value of Tarn using a three-stage DDM with an H-model second stage is closest to:
> A. 48.09.
> B. 58.22.
> C. 68.36.

> [!success]- Answer key
> Q1: B.
> $r = 3 + 0.9 \times 5 = 7.5\%$; $V_0 = 2.40 \times 1.04/(0.075 - 0.04) = 2.496/0.035 = 71.31$ (Python: `2.4*1.04/0.035 = 71.314`).
> A uses $D_0$ in the numerator ($2.40/0.035 = 68.57$); C grows the dividend twice (V5 p.62, p.63).
>
> Q2: A.
> No-growth value $= E_1/r = 5.20/0.075 = 69.33$; PVGO $= 68.00 - 69.33 = -1.33$ (Python: `68-5.2/0.075 = -1.333`).
> Negative PVGO means the market expects reinvestment below the cost of equity, or the inputs ($E_1$ too high or $r$ too low) are wrong.
> B uses the model value 71.31 instead of price; C is the no-growth value itself (V5 p.73).
>
> Q3: A.
> Payout $= D_1/E_1 = 2.496/5.20 = 0.48$; justified leading P/E $= 0.48/0.035 = 13.71$; actual leading P/E $= 68/5.20 = 13.08$ (Python: `0.48/0.035 = 13.714`, `68/5.2 = 13.077`).
> B reports the trailing justified multiple $0.48 \times 1.04/0.035 = 14.26$; C swaps the pair, reporting the trailing justified multiple as the actual (V5 p.75).
>
> Q4: B.
> $g = (P_0 r - D_0)/(P_0 + D_0) = (68 \times 0.075 - 2.40)/(68 + 2.40) = 2.70/70.40 = 3.84\%$ (Python: `(68*0.075-2.4)/70.4 = 0.03835`).
> A is $D_1/P_0 = 2.496/68 = 3.67\%$, the dividend yield, not the growth rate; C is the analyst's own assumption, which the price does not support (V5 p.71, p.72).
>
> Q5: C.
> $D_1 = 1.20$, $D_2 = 1.44$, $D_3 = 1.728$; $V_3 = 1.728 \times 1.05/(0.10 - 0.05) = 36.288$.
> $V_0 = 1.20/1.10 + 1.44/1.10^2 + (1.728 + 36.288)/1.10^3 = 1.091 + 1.190 + 28.562 = 30.84$ (Python: `30.843`).
> Calculator: C01 = 1.20, C02 = 1.44, C03 = 38.016, I = 10, NPV = 30.84.
> A discounts $V_3$ four periods (28.36); B builds $V_3$ from $D_3$ instead of $D_4$ ($1.728/0.05 = 34.56$, total 29.54) (V5 p.79, p.82).
>
> Q6: A.
> $H = 1.5$: $V_0 = [1.00 \times 1.05 + 1.00 \times 1.5 \times (0.20 - 0.05)]/0.05 = (1.05 + 0.225)/0.05 = 25.50$ (Python: `1.275/0.05 = 25.5`).
> The linear decline means growth averages 12.5% over the three years rather than 20%, so fewer dividends are paid than under the abrupt two-stage assumption.
> B uses $H = 3$, the full transition length; C drops the H term and reports the Gordon value at 5% (V5 p.83, p.84).
>
> Q7: B.
> $V_3 = D_4/(r - g) = 2.00/(0.11 - 0.06) = 40.00$; $V_0 = 40/1.11^3 = 29.25$ (Python: `40/1.11**3 = 29.248`).
> A discounts four periods (26.35); C grows the first dividend once more before capitalizing it ($2.12/0.05 = 42.4$, PV 31.00) (V5 p.82).
>
> Q8: B.
> Eight-year decline gives $H = 4$: $r = (1.50/50)[(1.04) + 4(0.09 - 0.04)] + 0.04 = 0.03 \times 1.24 + 0.04 = 7.72\%$ (Python: `0.03*1.24+0.04 = 0.0772`).
> A is the Gordon expected return at the mature rate, $1.50 \times 1.04/50 + 0.04 = 7.12\%$, which ignores the supernormal years; C uses $H = 8$ (V5 p.92).
>
> Q9: B.
> Retention $= (120 - 45)/120 = 0.625$; margin $= 120/1{,}500 = 0.08$; turnover $= 1{,}500/2{,}000 = 0.75$; leverage $= 2{,}000/800 = 2.5$; $g = 0.625 \times 0.08 \times 0.75 \times 2.5 = 9.375\%$ (Python: `0.625*0.08*0.75*2.5 = 0.09375`).
> Shortcut: retained earnings over beginning equity $= 75/800 = 9.375\%$.
> A multiplies ROE by the payout ratio ($0.375 \times 15\%$); C is ROE itself without retention (V5 p.96, p.123).
>
> Q10: B.
> $D_1 = 2.24$, $D_2 = 2 \times 1.12^2 = 2.5088$; six-year decline gives $H = 3$.
> $V_2 = 2.5088 \times 1.04/0.05 + 2.5088 \times 3 \times (0.12 - 0.04)/0.05 = 52.18 + 12.04 = 64.23$.
> $V_0 = 2.24/1.09 + (2.5088 + 64.23)/1.09^2 = 2.055 + 56.169 = 58.22$ (Python: `58.224`).
> Calculator: C01 = 2.24, C02 = 66.734, I = 9, NPV = 58.22.
> A drops the H-model add-on and uses only the Gordon term at $t = 2$; C uses $H = 6$, doubling the add-on (V5 p.86, p.88).

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm02

Three cash flow definitions for DCF equity models::Dividends, free cash flow (FCFF or FCFE), residual income (V5 p.53).
When is the DDM the suitable definition of returns?::Company pays dividends, dividend policy bears an understandable and consistent relation to profitability, and the investor takes a non-control perspective (V5 p.54).
When is free cash flow the suitable definition?::Company does not pay dividends, or dividends differ substantially from FCFE, or free cash flows align with profitability within a comfortable horizon, or the investor takes a control perspective (V5 p.57).
When is residual income the suitable definition?::Non-dividend payer as an alternative to FCF, or expected free cash flows are negative within the forecast horizon (V5 p.58).
Why does a DDM not ignore reinvested earnings?::Reinvested earnings are the basis for future dividends, and the DDM discounts all future dividends (V5 p.53).
FCFF versus FCFE in one line::FCFF is cash from operations less capital expenditure, a predebt measure; FCFE further nets interest and principal paid less new debt issued, a postdebt measure (V5 p.56).
Residual income definition (DDM context)::Earnings for the period in excess of the required return on beginning-of-period book equity, RI = E minus r times beginning BV (V5 p.57).
Clean surplus relation (DDM context)::Book value at t equals book value at t minus 1 plus earnings minus dividends, valid when all balance sheet changes other than ownership transactions pass through income (V5 p.57, p.58).
Single holding period DDM::V0 = (D1 + P1)/(1 + r) (V5 p.59).
Expected holding period return from D1, P1 and P0::r = (D1 + P1)/P0 minus 1, dividend yield plus price appreciation (V5 p.101).
Why does a finite-horizon investor's value depend on all future dividends?::The selling price at the horizon is the present value of the dividends after the sale (V5 p.61).
Two broad approaches to forecasting the dividend stream::Assign the whole stream to a stylized growth pattern, or forecast a finite number individually and apply a pattern or a price multiple at the terminal point (V5 p.61).
Gordon growth model::V0 = D0(1 + g)/(r minus g) = D1/(r minus g), requiring r greater than g (V5 p.62).
Derivation of the Gordon model in one sentence::Geometric series with first term D1/(1 + r) and ratio (1 + g)/(1 + r), summing to a/(1 minus m) = D1/(r minus g) when the ratio is below one (V5 p.62).
What happens in the Gordon model if r is at or below g?::The series does not converge and the value is infinite, which is economically meaningless, so such inputs are invalid (V5 p.62, p.63).
Growth rate benchmark for using the Gordon model::Earnings growth comparable to or lower than the economy's nominal GDP growth, real growth plus expected inflation (V5 p.63, p.64).
Micro-problem: D0 = 3, g = 5%, r = 9%; value?::3 times 1.05 divided by 0.04 = 78.75; keystrokes 3 × 1.05 ÷ 0.04 = (V5 p.63).
Value of non-callable fixed-rate perpetual preferred::V0 = D/r, with D = dividend rate times par and r the capitalization rate (V5 p.68).
Micro-problem: preferred pays 6% on 50 par, capitalization rate 8%; value?::3/0.08 = 37.50; for the implied rate from a 42 price, 3/42 = 7.14% (V5 p.68, p.121).
Gordon model with negative growth::Still valid; V0 = D1/(r minus g) with g negative widens the spread, as in Afton Mines 4.25/0.13 = 32.69 (V5 p.69).
In the Gordon model, at what rate do value, dividends and earnings grow?::All at g when r and the payout ratio are constant, so the dividend yield and capital gains yield are constant through time (V5 p.69, p.70).
Implied dividend growth rate from price::g = (P0 r minus D0)/(P0 + D0), from P0 = D0(1 + g)/(r minus g) (V5 p.72).
Micro-problem: price 30, D0 = 1.50, r = 10%; implied g?::(3.00 minus 1.50)/(31.50) = 4.76%; keystrokes 30 × 0.1 − 1.5 = ÷ 31.5 = (V5 p.72).
Implied growth above the analyst's growth means the stock is::Overvalued; the market prices more growth than the analyst expects (V5 p.72, p.119).
PVGO decomposition::V0 = E1/r + PVGO; E1/r is the no-growth value or value of assets in place (V5 p.73).
Two determinants of PVGO::The value of the company's investment opportunities (positive NPV projects) and the value of its real options to time, scale or abandon projects (V5 p.74).
Micro-problem: price 50, E1 = 4, r = 10%; PVGO and its share of price?::50 minus 40 = 10, which is 20% of price (V5 p.73).
Leading P/E decomposition::P0/E1 = 1/r + PVGO/E1; the first term is the no-growth P/E (V5 p.74).
Justified leading P/E from the Gordon model::(1 minus b)/(r minus g), where 1 minus b is the payout ratio (V5 p.75).
Justified trailing P/E from the Gordon model::(1 minus b)(1 + g)/(r minus g), the leading multiple times (1 + g) (V5 p.75).
Micro-problem: payout 60%, r = 10%, g = 4%; justified leading and trailing P/E?::0.6/0.06 = 10.0 and 0.6 times 1.04/0.06 = 10.4 (V5 p.75).
Justified leading P/E under a multistage model::Model value divided by next year's expected EPS (V5 p.76).
Required return from the Gordon model::r = D1/P0 + g, dividend yield plus capital gains yield; technically an IRR (V5 p.76).
Why not reuse the DDM-implied required return in the same DDM?::It is circular; the IRR reproduces the price by construction (V5 p.92).
Three growth phases and their FCFE and payout signatures::Growth phase has supernormal EPS growth, negative FCFE and low or zero payout; transition has slowing growth, positive FCFE and rising payout; maturity has ROE near r and stable growth, payout and ROE (V5 p.77, p.78).
Two-stage DDM terminal value::Vn = D(n+1)/(r minus gL) = D0(1 + gS)^n (1 + gL)/(r minus gL), located at t = n and discounted n periods (V5 p.79).
What share of value does the terminal value typically represent in a multistage DDM?::Often more than three-quarters, 93% for Meditec and 88% for the technology example (V5 p.80, p.86, p.94).
Terminal value from a multiple in a multistage DDM::Vn = trailing P/E times En, with En = Dn/(1 minus b) when only the dividend and payout are given (V5 p.81).
Valuing a stock whose first dividend Dn arrives at t = n::V(n minus 1) = Dn/(r minus g), then discount n minus 1 periods (V5 p.82).
Micro-problem: first dividend 1.50 at t = 3, g = 5%, r = 11%; value?::V2 = 1.50/0.06 = 25; V0 = 25/1.11^2 = 20.29; TVM N = 2, I/Y = 11, FV = 25, CPT PV (V5 p.82).
H-model formula::V0 = [D0(1 + gL) + D0 H (gS minus gL)]/(r minus gL), with H half the length of the linear decline (V5 p.83).
Intuition for the H-model add-on::Excess growth averages (gS minus gL)/2 over 2H years, so extra dividends total D0 H (gS minus gL), capitalized at r minus gL without individual discounting, hence an approximation (V5 p.84).
When does the H-model approximation break down?::Long supernormal periods (large H) or large gaps between gS and gL; use an explicit spreadsheet instead (V5 p.85).
Micro-problem: D0 = 1, gS = 10% declining over 6 years to 4%, r = 9%; H-model value?::H = 3: (1.04 + 3 times 0.06)/0.05 = 1.22/0.05 = 24.40 (V5 p.83).
Two versions of the three-stage DDM::Three distinct constant growth rates, or a constant first stage followed by a linearly declining second stage valued as an H-model (V5 p.85, p.86).
Four steps of the three-stage model with H-model second stage::Gather inputs; PV the stage-1 dividends; apply the H-model at the start of stage 2 using Dn and discount to today; sum (V5 p.86).
Required return from the H-model::r = (D0/P0)[(1 + gL) + H(gS minus gL)] + gL, which collapses to the Gordon form when gS = gL (V5 p.92).
Micro-problem: D0 = 1, P0 = 25, gS = 10% declining over 6 years to 5%; expected return?::(1/25)(1.05 + 3 times 0.05) + 0.05 = 0.04 times 1.20 + 0.05 = 9.8% (V5 p.92).
How is the IRR found for a two-stage or spreadsheet DDM?::Trial and error or Goal Seek, starting from the Gordon approximation D1/P0 + gL and raising r if early growth exceeds gL (V5 p.92, p.93).
Sustainable growth rate::g = b times ROE, retention rate times return on equity, exact with beginning equity and constant capital structure (V5 p.94, p.96).
Three ways to estimate mature-phase ROE::DuPont decomposition forecasts, setting ROE equal to r, or the industry median ROE (V5 p.91).
DuPont three-way ROE::Net margin times asset turnover times equity multiplier (V5 p.96).
PRAT model::g = profit margin times retention times asset turnover times leverage; ROA and financial policies determine growth (V5 p.96).
Micro-problem: margin 5%, turnover 1.5, leverage 2.0, payout 40%; sustainable g?::ROE = 15%, g = 0.6 times 15% = 9%; keystrokes 0.05 × 1.5 × 2 × 0.6 = (V5 p.96, p.97).
Fair value band rule::Compare price with value plus or minus the stated percentage of value; inside is fairly valued, below is undervalued, above is overvalued (V5 p.88, p.110).
Which sector report supports the Gordon model for a repurchasing company?::One expressing confidence in forecasts of the magnitude and timing of repurchases, so the per-share dividend growth rate can be adjusted (V5 p.70, p.121).
Trap answer when a company suspends dividends for three years::Claiming a DDM cannot apply; a multistage DDM with zero first-stage dividends works (V5 p.82, p.118).
Trap answer when a company is a takeover candidate::Claiming FCF is inappropriate; a control perspective is exactly when FCF valuation is preferred (V5 p.57, p.118).
{{Vn is built from D(n+1) and discounted n periods}}, never from Dn and never discounted n + 1 periods (V5 p.79, p.82).
{{H equals half}} the length of the linear decline in growth, so a 10-year transition means H = 5 (V5 p.83).

## Common mistakes

1. Using $D_0$ where $D_1$ belongs in the Gordon numerator, or growing a dividend that the vignette already states as "next year's" (V5 p.63, p.69, p.118).
2. Accepting a perpetual growth rate at or above $r$ or far above nominal GDP growth; the model is invalid, and the fix is a multistage model with a plausible mature rate (V5 p.62, p.64, p.121).
3. Building the terminal value from $D_n$ instead of $D_{n+1}$, or discounting $V_n$ for $n + 1$ periods (V5 p.79, p.82, p.119).
4. For a stock that starts paying at $t = n$, discounting the Gordon value $n$ periods rather than $n - 1$ (V5 p.82, p.119).
5. Setting $H$ equal to the full transition length rather than half of it, or using $D_1$ or $g_S$ in the first H-model term (V5 p.83, p.118, p.122).
6. Treating the H-model as exact; it approximates the discounted stream and overstates value when $H$ or $g_S - g_L$ is large (V5 p.84, p.85).
7. Ranking PVGO/$E_1$ by PVGO in dollars; the two rankings can differ when earnings levels differ (V5 p.119, p.120).
8. Using last year's payout ratio for the justified P/E when the vignette gives an expected future payout, or comparing a leading justified multiple with a trailing actual multiple (V5 p.111, p.120, p.121).
9. Reading implied growth backwards: implied growth above the analyst's or sustainable growth means overvalued (V5 p.72, p.119).
10. Building the fair value band around price instead of intrinsic value, or ignoring the band when one is stated (V5 p.88, p.110, p.120).
11. Multiplying ROE by the payout ratio instead of the retention rate in $g = b \times ROE$ (V5 p.94, p.123).
12. Projecting a historical ROE inflated by leverage into the mature phase instead of normalizing the DuPont components, as with IBM (V5 p.97, p.98).
13. Reusing a DDM-implied required return as the discount rate in the same model, which is circular (V5 p.92).
14. Ruling out a DDM because dividends are suspended for a few years, or ruling out FCF because the company may be acquired (V5 p.57, p.82, p.118).
15. Selecting the Gordon model for a company with a stated supernormal phase, or the H-model for a company whose growth steps down abruptly rather than declining linearly (V5 p.80, p.85, p.121).
16. Forgetting that the terminal value usually dominates the answer, so a valuation is only as reliable as $g_L$ and $r$; always show a sensitivity grid (V5 p.68, p.80, p.94).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-02" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
