---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [bonds-duration-and-convexity, curve-risk-and-hedging]
est_hours: 5
sources: [Bruce Tuckman and Angel Serrat - Fixed Income Securities 3rd edition - Wiley 2012 - chapters 3 5 and 6, Antti Ilmanen - Expected Returns - Wiley 2011]
---

# Fixed Income P&L Attribution and Relative Value

## TL;DR

- Over a horizon, a financed bond earns carry (coupon income, pull to par, minus financing) and roll-down (repricing at the lower yield of a shorter maturity on an unchanged curve), then gains or loses from curve moves through delta and convexity; whatever full revaluation shows beyond these terms is the residual.
- On a 1-month, $\$100$ million 10-year example, carry plus roll-down is $\$40,578$, enough to absorb a yield rise of only $0.50$ bp; a $+5$ bp move costs $\$402,306$, and DV01 plus convexity explain it to within $\$1.66$.
- Curve trades are DV01-neutral; a 50-50 butterfly is neutral to parallel moves only, and a regression-weighted one is neutral to the fitted co-movement but not to parallel moves.
- Asset swaps convert a fixed bond into a floater: par-par spread $= (P_{\text{swap curve}} - P_{\text{mkt}}) / (100 \times A)$, and the market-value spread is the par-par spread times $100/P$.
- Mean reversion signals on curve spreads fail when regimes change; carry, financing (repo specials) and liquidity decide whether convergence pays.

## Learning objectives

- Formulate the fixed income P&L attribution equation across carry, roll-down, delta, twist, butterfly, spread, and convexity components.
- Calculate carry and roll-down returns under unchanged yield curve assumptions, and check an attribution against full revaluation.
- Construct curve steepener and flattener positions under bull and bear market regimes.
- Design duration-neutral and regression-weighted butterfly trades (e.g., 2s-5s-10s and 5s-10s-30s).
- Structure par-par and market-value asset swaps to isolate asset-swap spreads (ASW).
- Compute empirical hedge ratios using PCA or yield regression beta and quantify their residual exposures.

## Core concepts

### 1. The attribution framework

For a position revalued from $t$ to $t + \Delta t$:
$$\Delta \text{P\&L} = \underbrace{\text{coupon income} + \text{pull to par} - \text{financing}}_{\text{carry}} + \text{roll-down} + \underbrace{\sum_i -\text{DV01}_i \Delta y_i + \tfrac{1}{2}\text{Conv}_{\$} (\Delta y)^2}_{\text{curve moves}} + \text{spread} + \epsilon.$$
- **Carry:** the P&L if yields stay where they are for the bond: coupon accrual, plus the move in clean price toward par at an unchanged yield, minus repo interest on the dirty price.
- **Roll-down:** the gain from repricing at the yield of a shorter maturity on an unchanged curve, $\approx -\text{DV01} \times (y(T - \Delta t) - y(T))$ in bp; positive on an upward-sloping curve.
- **Curve moves:** first-order key-rate (or factor) DV01s times yield changes, plus the convexity term; parallel, slope and curvature terms are a projection of the same key-rate changes onto factors, not separate risks.
- **Spread:** for credit or swap-spread positions, $-\text{DV01} \times \Delta s$.
- **Residual $\epsilon$:** full revaluation minus the sum of the terms; small and stable when the attribution is right, large when a risk is missing.

For bonds the time effect is entirely carry plus roll-down; theta as a separate line belongs to options, where it must not double count the same passage of time.
Carry plus roll-down divided by DV01 is the breakeven yield rise over the horizon, the standard way to compare positions.

### 2. Curve trades

A curve trade weights the legs so that their DV01s offset, $N_1 \text{DV01}_1 = N_2 \text{DV01}_2$ per unit notional.
- **Steepener:** long the short maturity, short the long maturity; it gains when $y(T_2) - y(T_1)$ rises.
  A bull steepener (front yields fall more) typically comes with expected rate cuts; a bear steepener (long yields rise more) with rising term premium or inflation expectations.
- **Flattener:** the opposite position; a bear flattener (front yields rise more) typically comes with expected hikes, a bull flattener (long yields fall more) with demand for duration or slowing growth.

### 3. Butterflies

A butterfly trades a body $T_2$ against wings $T_1 < T_2 < T_3$, with fly spread $2y(T_2) - y(T_1) - y(T_3)$; a rising fly means the body cheapens against the wings.
A long butterfly (long wings, short body) gains when the fly spread rises.

**50-50 DV01 weighting:** each wing carries half of the body's DV01.
It is neutral to parallel moves, but not to a twist unless the body sits at the midpoint of the wings: for a linear twist of $k$ bp per year of maturity about the body, the P&L is $-\frac{1}{2}\text{DV01}_b\, k\,(T_1 + T_3 - 2T_2)$, which for 2s5s10s ($2 + 10 - 10 = 2$) is not zero.

**Regression weighting:** estimate $\Delta y_2 = \beta_1 \Delta y_1 + \beta_3 \Delta y_3 + \epsilon$ from history and hold wing DV01s of $\beta_1 \text{DV01}_b$ and $\beta_3 \text{DV01}_b$; the trade then carries only the residual $\epsilon$ if the betas are stable.
Unless $\beta_1 + \beta_3 = 1$ it is not neutral to a parallel move; PCA weighting instead neutralises the first two factors exactly.
With the body fixed a butterfly has only two free wing weights, so neutralising a third factor needs a fourth instrument.

### 4. Asset swaps

An asset swap packages a fixed-rate bond with a swap paying the bond's coupons and receiving floating plus a spread.

**Par-par:** the investor pays par for the package (the bond price plus an upfront of $100 - P$ to the swap counterparty) and receives floating plus $s$ on 100.
At inception the swap's value to the investor must equal the upfront, which gives
$$s_{\text{par-par}} = \frac{P_{\text{swap curve}} - P_{\text{mkt}}}{100 \times A},$$
with $P_{\text{swap curve}}$ the bond's cash flows discounted on the swap curve and $A$ the floating-leg annuity.
The spread measures how cheap the bond is relative to the swap curve, in running terms.

**Market-value (proceeds):** the swap notional equals the dirty price, so no upfront is exchanged; spreading the same price difference over a notional of $P$ gives $s_{\text{MV}} = s_{\text{par-par}} \times 100 / P$, and at maturity the notionals are exchanged back ($P$ against 100).
The two differ in counterparty exposure: the par-par investor has prepaid $100 - P$ to the swap counterparty for a discount bond.

### 5. Relative value signals and risks

$Z(t) = (\text{spread}(t) - \mu)/\sigma$ over a rolling window flags a fly or asset swap spread far from its recent average; a high fly Z-score means the body is cheap, and the trade is to buy the body against the wings.
- **Regime change:** policy, supply or index changes can move the mean, so a Z-score keeps signalling as losses grow.
- **Carry:** a mean-reversion trade that carries negatively must converge fast enough to pay for it; compare expected convergence with carry plus roll-down.
- **Financing:** a bond that goes special in repo lowers financing cost for longs and raises the cost of shorts (the short lends cash at the low special rate to borrow the bond).
- **Liquidity:** on-the-run issues trade rich to off-the-runs; spreads that cross a roll from one benchmark to the next are not like for like.

## Worked examples

### Example 1: one month of P&L, attributed and revalued
$\$100$ million face of a 10-year note, $4.25\%$ semi-annual coupon, bought on a coupon date at a $4.20\%$ yield (price $100.4049$), financed in repo at $4.00\%$ for 30 days; around 10 years the curve rises $4$ bp per year of maturity, so after one month the note rolls down to $4.1967\%$; then yields rise $5$ bp.
- Coupon income $\$354,166.67$; pull to par at an unchanged yield $-\$5,785.64$ (a premium bond accretes toward par); financing $-\$334,682.89$; net carry $\$13,698.13$.
- Roll-down $\$26,880.09$; carry plus roll-down $\$40,578.22$.
- DV01 at the rolled-down point $\$80,653.08$ per bp, so carry plus roll-down covers a yield rise of only $0.50$ bp over the month.
- Rate move by full revaluation $-\$402,306.10$; the attribution gives delta $-\$403,265.42$ plus convexity $\$960.98$, leaving an unexplained residual of $-\$1.66$ (third-order terms).
- Total P&L $-\$361,727.88$, which equals the sum of the components.

### Example 2: 2s5s10s butterflies
DV01 per $\$100,000$ notional: $\$19.50$ (2y), $\$44.20$ (5y), $\$81.50$ (10y); short $\$100$ million of the 5y body, DV01 $\$44,200$.
- **50-50:** each wing $\$22,100$ of DV01: $\$113,333,333$ of 2y and $\$27,116,564$ of 10y; parallel DV01 zero.
- **Twist:** a steepening of $1$ bp per year of maturity about the 5y moves the 2y by $-3$ bp and the 10y by $+5$ bp; the 2y wing makes $\$66,300$, the 10y wing loses $\$110,500$, net $-\$44,200$.
- **Regression:** with illustrative betas $\beta_2 = 0.40$, $\beta_{10} = 0.65$ the wings carry $\$17,680$ and $\$28,730$ of DV01 ($\$90,666,667$ of 2y and $\$35,251,534$ of 10y), and the package has $\$2,210$ of net parallel DV01 because $0.40 + 0.65 \ne 1$.

### Example 3: asset swap spreads
Flat annual swap curve with a $4.10\%$ par rate (swap annuity $5.9799$); a 7-year $4.00\%$ annual bond at a $4.45\%$ yield, on a coupon date, so price $97.3434$; on the swap curve the same cash flows are worth $99.4020$.
$$s_{\text{par-par}} = \frac{99.40201 - 97.34343}{100 \times 5.97994} = 34.42 \text{ bp}, \qquad s_{\text{MV}} = 34.42 \times \frac{100}{97.3434} = 35.36 \text{ bp},$$
against a yield spread of $35.00$ bp.
The script checks the par-par spread independently: projecting the floating leg from the curve's forwards, the swap is worth exactly the $100 - P$ upfront.

## Pitfalls

- **Parallel neutrality is not curve neutrality:** a 50-50 2s5s10s fly loses $\$44,200$ per $1$ bp per year of steepening about the body (Example 2).
- **Regression hedges leave parallel risk:** wing betas that do not sum to one leave net DV01 ($\$2,210$ in Example 2) that must be hedged or accepted.
- **Ignoring carry and roll-down:** a convergence trade with negative carry plus roll-down needs convergence faster than the bleed; quote both in bp of breakeven.
- **Attribution without full revaluation:** a sum of Greeks that does not reconcile to the revalued P&L hides missing risks; track the residual daily.
- **Repo specials:** shorting a special issue costs the difference between general collateral and special repo for as long as the short is held.
- **Settlement mismatches:** US Treasuries settle T+1 and USD swaps start T+2; hedges must use matching start dates or carry an extra day of exposure.
- **Benchmark rolls:** comparing an off-the-run with a new on-the-run issue mixes a liquidity premium into the spread.

## Interview questions

> [!question]- fi-rv-pnl-carry-vs-rolldown | Explain the distinction between Carry and Roll-down in fixed income performance attribution.
> Carry is the P&L if the bond's own yield does not change: coupon income plus pull to par minus financing; roll-down is the extra gain from repricing at the lower yield of a shorter maturity when the curve itself does not change.
> In Example 1 the month's carry is $\$13,698.13$ and the roll-down $\$26,880.09$.

> [!question]- fi-rv-bull-vs-bear-steepeners | Contrast a Bull Steepener with a Bear Steepener in terms of macro drivers and relative yield shifts.
> Bull steepener: yields fall, front end more, typically when the market prices rate cuts.
> Bear steepener: yields rise, long end more, typically with rising term premium, inflation expectations or supply, while the front end is anchored by policy.

> [!question]- fi-rv-butterfly-spread-definition | Define a yield curve butterfly spread (body vs. wings) and explain what a widening butterfly indicates.
> $\text{Fly} = 2y(T_2) - y(T_1) - y(T_3)$ with body $T_2$ between wings $T_1$ and $T_3$.
> A widening fly means the body yield rose relative to the wings: the body cheapened and the curve became more humped at the body.

> [!question]- fi-rv-fifty-fifty-dv01-limitation | Why is a 50-50 DV01 weighted butterfly vulnerable to yield curve slope changes (twist risk)?
> It is neutral only to equal yield changes; under a linear twist about the body the wings move by $k(T_1 - T_2)$ and $k(T_3 - T_2)$, which cancel only if the body is the midpoint of the wings.
> For 2s5s10s ($T_1 + T_3 - 2T_2 = 2$) a 1 bp per year steepening about the 5y costs $\$44,200$ when the body DV01 is $\$44,200$.

> [!question]- fi-rv-regression-beta-butterfly | How does regression beta weighting improve butterfly immunization compared to simple 50-50 DV01?
> Regress body yield changes on wing yield changes, $\Delta y_2 = \beta_1 \Delta y_1 + \beta_3 \Delta y_3 + \epsilon$, and hold wing DV01s of $\beta_1$ and $\beta_3$ times the body DV01, so the trade carries only $\epsilon$ if the betas hold.
> The cost: unless $\beta_1 + \beta_3 = 1$ the trade has net parallel DV01 ($\$2,210$ with betas $0.40$ and $0.65$ in Example 2), and the betas themselves move.

> [!question]- fi-rv-asset-swap-spread-asw | What is an Asset Swap Spread (ASW), and what risks does it isolate?
> The spread over the floating index at which a bond swapped into a floater is fairly priced; par-par $s = (P_{\text{swap curve}} - P_{\text{mkt}}) / (100 A)$.
> It measures the bond's value relative to the swap curve in running terms, mixing credit, liquidity and funding, with the rate risk hedged by the swap (Example 3: $34.42$ bp).

> [!question]- fi-rv-par-par-vs-market-value-asw | Distinguish between a Par-Par Asset Swap and a Market-Value (Proceeds) Asset Swap.
> Par-par: the investor pays 100 for the package (price plus an upfront of $100 - P$) and the swap runs on 100; market value: the swap runs on the dirty price $P$, no upfront, and the notionals $P$ and 100 are exchanged at maturity.
> The same price difference spread over $P$ instead of 100 gives $s_{\text{MV}} = s_{\text{par-par}} \times 100/P$: $35.36$ bp against $34.42$ bp for a bond at $97.34$.

> [!question]- fi-rv-repo-specialness-impact | How does a bond trading "on special" in the repo market affect relative value trading strategies?
> Demand to borrow the bond pushes its repo rate below general collateral; the short lends cash at that low rate, paying the difference for as long as the short is held, while longs finance cheaply.
> Trades that short a special issue need the convergence to beat the specialness cost, and a squeeze can force them out early.

> [!question]- fi-rv-zscore-relative-value-risks | Why can relying solely on rolling Z-scores of curve spreads be dangerous for relative value hedge funds?
> They assume a stationary mean; policy changes, supply or index events can move the mean, and the Z-score keeps signalling while the position loses.
> Without carry, financing and liquidity in the decision, a statistically cheap trade can bleed for longer than capital allows.

> [!question]- fi-rv-box-trade-mechanics | What is a yield curve box trade, and how is it used to exploit spread dislocations?
> Two DV01-neutral curve trades on different tenor pairs, for example a 2s5s steepener with a 10s30s flattener, so the position is long $(y_5 - y_2) - (y_{30} - y_{10})$.
> It isolates a local kink, from supply or demand for a sector, while hedging parallel moves; it is exposed to any move that reshapes the two segments differently.

> [!question]- fi-rv-attribution-residual | Your P&L attribution shows a growing daily residual. What do you check?
> That the full revaluation and the Greeks use the same curves and times, that the attribution includes every risk the position has (convexity, basis between curves, carry over weekends), and that sensitivities are recomputed at the current state.
> A complete attribution leaves a small residual: in Example 1 a 5 bp move is explained by DV01 and convexity to within $\$1.66$ out of $\$402,306$.

> [!question]- fi-rv-carry-breakeven | How do you express carry and roll-down so positions of different duration can be compared?
> Divide by DV01: the result is the yield rise over the horizon that would wipe out the carry and roll-down.
> In Example 1, $\$40,578.22$ over a DV01 of $\$80,653.08$ is a breakeven of $0.50$ bp for the month.

> [!question]- fi-rv-pull-to-par | Why is the pull to par negative in Example 1, and is it part of carry?
> The note was bought above par (coupon $4.25\%$ above the $4.20\%$ yield), so at an unchanged yield its clean price drifts toward par, $-\$5,785.64$ over the month.
> Yes: carry at an unchanged yield is coupon income plus pull to par minus financing, which together equal the yield accrual on the dirty price minus financing.

> [!question]- fi-rv-asw-mv-above-parpar | For a bond trading below par, is the market-value asset swap spread above or below the par-par spread, and why?
> Above: the same present-value difference $P_{\text{swap curve}} - P_{\text{mkt}}$ is spread over a notional of $P < 100$ instead of 100, so $s_{\text{MV}} = s_{\text{par-par}} \times 100/P$.
> For a premium bond the order reverses.

> [!question]- fi-rv-twist-formula | Derive the twist exposure of a 50-50 butterfly.
> With a twist $\Delta y(T) = k(T - T_2)$, the long wings each carry $\frac{1}{2}\text{DV01}_b$ and the body's yield does not move, so the P&L is $-\frac{1}{2}\text{DV01}_b k (T_1 - T_2) - \frac{1}{2}\text{DV01}_b k (T_3 - T_2) = -\frac{1}{2}\text{DV01}_b k (T_1 + T_3 - 2T_2)$.
> It vanishes only for a body at the midpoint, for example 2s6s10s, not 2s5s10s.

## Further reading

- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, 3rd edition, Wiley, 2012: chapter 3 (Returns, Spreads, and Yields), chapter 5 (Multi-Factor Risk Metrics and Hedges) and chapter 6 (Empirical Approaches to Risk Metrics and Hedging).
- Antti Ilmanen, *Expected Returns: An Investor's Guide to Harvesting Market Rewards*, Wiley, 2011.

## In this repo and SDE-Interview-Prep

- Code: [`code/fi_relative_value.py`](code/fi_relative_value.py) asserts every number here, including the full-revaluation check of the attribution and the leg-by-leg check of the asset swap spread.
- Discounting and yield curve foundations: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md).
- Duration, convexity, and immunization mathematics: [Bonds, Duration, and Convexity](02-Bonds-Duration-and-Convexity.md).
- Key-rate and factor hedging: [Curve Risk and Hedging](15-Curve-Risk-and-Hedging.md).
