---
type: cfa-lm
topic: "Corporate Issuers"
topic_code: "04"
topic_slug: "04-Corporate-Issuers"
volume: 4
lm: 3
title: "Cost of Capital: Advanced Topics"
pages: "99-153"
weight_band: "5-10%"
difficulty: 3
los_count: 6
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/corporate-issuers]
---

# LM3: Cost of Capital: Advanced Topics

Difficulty 3 of 5: four of the six LOS are qualitative compare-and-explain material, but the module hides the exam's favorite computations (Grinold-Kroner, the country spread model, matrix pricing, synthetic ratings, unlever-relever betas), every one of which has a sign trap or an input-selection trap.

## LOS map

- **explain** top-down and bottom-up factors that impact the cost of capital (V4 p.99) ^los-04-03-a
    - Examiner asks: given a two-country or two-company exhibit of credit spreads, rate volatility, tax rates, asset mix, leverage ratios, customer concentration and embedded options, identify which issuer has the lower cost of capital and justify with two or three factors.
- **compare** methods used to estimate the cost of debt. (V4 p.99) ^los-04-03-b
    - Examiner asks: pick the right estimation route for a given debt profile (traded YTM, matrix pricing, synthetic rating from IC and D/E, bank loan rate, lease implicit rate), then execute a matrix-pricing interpolation or read a synthetic rating off a schedule.
- **explain** historical and forward-looking approaches to estimating an equity risk premium (V4 p.99) ^los-04-03-c
    - Examiner asks: name the four historical-approach decisions, state the direction of survivorship bias or a short-rate-plus-arithmetic-mean choice, or compute a Gordon growth or Grinold-Kroner ERP from an input table.
- **compare** methods used to estimate the required return on equity (V4 p.99) ^los-04-03-d
    - Examiner asks: compute the cost of equity under two or three of DDM, BYPRP, CAPM and Fama-French from one exhibit and explain why the estimates differ or which one is implausible.
- **estimate** the cost of debt or required return on equity for a public company and a private company (V4 p.99) ^los-04-03-e
    - Examiner asks: run the Gretna-style mini case: matrix price the debt, cost the preferred as a perpetuity, then compare CAPM, five-factor and BYPRP equity estimates against the preferred yield sanity check.
- **evaluate** a company's capital structure and cost of capital relative to peers (V4 p.99) ^los-04-03-f
    - Examiner asks: run the Precision-style mini case: synthetic rating from IC and D/E versus the industry, unlever the peer beta and relever it to the subject, add SP, IP, SCRP and CRP, and roll everything into a WACC.

## Core intuition

Every valuation and every capital budgeting decision discounts cash flows at a rate, and this module is about where that rate comes from when nothing about it is directly observable.
The WACC blends the after-tax cost of debt, the cost of preferred and the cost of common equity at target-structure weights (V4 p.100).
The cost of debt is nearly observable, because bonds trade and coupons are contracts; the cost of equity is never observable, because equity promises nothing, so it must be modeled (V4 p.100).
That asymmetry organizes the whole module: a hierarchy of increasingly indirect methods for debt, and a menu of models for equity that all decompose into a risk-free rate plus premia for risks borne (V4 p.111, p.129).

> [!abstract] Idea 1: every cost of capital is a risk-free rate plus compensation for risks, split into top-down and bottom-up layers
> The pre-tax cost of debt is the risk-free rate plus a credit spread; the cost of equity is the risk-free rate plus beta times the ERP, or plus a stack of premia (V4 p.100).
> Top-down, external factors (capital availability, market conditions, legal and regulatory maturity, tax jurisdiction) set the level of the risk-free rate, aggregate spreads and the ERP for everyone in the market (V4 p.101).
> Bottom-up, company-specific factors (volatility of revenues, earnings and cash flow, asset nature and liquidity, financial strength and leverage, security features) set where a particular issuer sits inside that market through its credit spread and its beta (V4 p.101, p.103).

The top-down layer is the economics of who supplies capital and on what terms.
Deep, liquid, well-regulated markets with common law protections, stable currencies and predictable monetary policy make investors feel safe, and safe investors accept lower spreads and lower ERPs (V4 p.101, p.102).
Recessions widen credit spreads and raise the ERP; expansions tighten and lower them, which is why issuance clusters in good times (V4 p.101, p.102).
A higher marginal tax rate makes the same coupon cheaper after tax, so tax jurisdiction alone changes the after-tax cost of debt without changing the pre-tax yield at all (V4 p.102).

The bottom-up layer is the economics of the issuer's own cash flow risk.
Subscription revenue, a diversified customer base, low operating leverage and low financial leverage make cash flows predictable, and predictable cash flows mean a lower probability of default, a narrower spread and a lower beta (V4 p.104).
Tangible, fungible, liquid assets can be pledged or sold, so they support cheaper debt; intangible-heavy balance sheets cannot, so they push the cost of capital up (V4 p.105).
Collateralizing assets cuts the cost of the secured debt but can raise the cost of equity, because creditors now stand ahead of shareholders in a liquidation (V4 p.105).
Security features price exactly like the options they contain: a call benefits the issuer so investors demand more yield, a put or a conversion right benefits investors so they accept less yield at issuance, cumulative preferred is safer than non-cumulative so it yields less, and inferior-rights share classes cost more (V4 p.106, p.107).
The cheap coupon on putable or convertible debt is not free money: it can turn into expensive refinancing when rates rise and bonds are put back, or into equity dilution on conversion (V4 p.106, p.107).
ESG risks (carbon exposure, safety liabilities, weak governance, entrenchment devices) work through the same channel, either as a higher required return or as haircuts to forecast cash flows, but not both (V4 p.104).

Estimating the cost of debt is then a decision tree keyed to how observable the debt is (V4 p.111).
Liquid straight bonds: read the YTM, preferring the most liquid issue.
Illiquid but rated debt: matrix price off the YTMs of same-rating bonds at surrounding maturities and interpolate.
Unrated debt: build a synthetic rating from fundamentals such as interest coverage and D/E, then use that rating class's spread over the benchmark (V4 p.111, p.112).
Bank debt: use the rate on recent borrowings if conditions and the risk profile have not changed; amortizing loans carry less default risk than bullet structures, so they price cheaper (V4 p.113).
Leases: a finance lease is a secured amortizing loan, and its implicit rate is the discount rate equating the present value of lease payments plus residual value to the asset's fair value plus the lessor's direct costs; when those lessor-side inputs are unknown, fall back to the incremental borrowing rate or to the non-traded-debt methods (V4 p.113).
Foreign-market debt: match the currency of the cash flows and add a country risk premium derived from country risk ratings and median rates relative to a benchmark country (V4 p.115).

> [!abstract] Idea 2: the ERP is the single most consequential estimate in the module, and every approach to it is a different way of guessing the future
> The historical approach assumes the past mean excess return is what investors expected and will expect, which requires stationarity and dies by survivorship bias (V4 p.117, p.119, p.120).
> The forward-looking approach asks what today's prices and forecasts imply: surveys ask people, the Gordon growth DDM backs the ERP out of the market's dividend yield and growth, and macro models such as Grinold-Kroner rebuild the expected equity return from income, repricing, inflation, real growth and share-count change (V4 p.121, p.122, p.123).
> Neither family is right; each has named biases the exam expects you to identify and sign (V4 p.119, p.125).

The historical approach forces four choices: which index, which sample period, which mean, and which risk-free proxy (V4 p.117).
Long windows shrink the standard error but drag in unrepresentative regimes; short windows are current but noisy (V4 p.118).
The arithmetic mean is consistent with single-period models such as CAPM but is outlier-sensitive and overstates terminal wealth; the geometric mean compounds to actual terminal wealth and is generally preferred (V4 p.118, p.119).
A short government bill is a true zero-coupon risk-free return but mismatches equity's infinite duration; a long government bond matches duration but embeds reinvestment risk, and industry practice favors the long bond (V4 p.119).
With a normal upward-sloping curve, an ERP measured over bills is mechanically larger than one measured over bonds, so pairing the bill-based premium with a currently high short rate double-inflates the required return (V4 p.119, p.146, p.152).
Survivorship bias, including backfilled index histories built only from firms that lived to construction date, inflates the historical mean; one-sided disasters that depressed returns without offsetting booms deflate it (V4 p.120, p.153).

The forward-looking family trades those data biases for model and forecast risk.
The Gordon growth version is one line: expected dividend yield plus expected earnings growth minus the risk-free rate, valid when the P/E is constant so earnings, dividends and prices grow together (V4 p.121, p.122).
Grinold-Kroner drops that constancy assumption by adding an explicit repricing term and decomposing earnings growth into inflation plus real growth minus dilution from net share issuance, so buybacks (negative change in shares) add to expected return (V4 p.123).
Expected inflation itself comes from the market: the ratio of nominal to inflation-protected yields at the same maturity (V4 p.124).
A rise in expected inflation roughly cancels out of the ERP because it lifts both the expected equity return and the risk-free rate; a fall in expected income lowers the ERP directly (V4 p.124, p.125).
Surveys are quick but suffer sampling, response, recency and confirmation biases; macro models need a market that is a large share of the economy, so Grinold-Kroner is wrong for small developing markets (V4 p.121, p.125).

> [!abstract] Idea 3: the cost of equity models form a ladder from traded to private to cross-border, and each rung adds premia for what the previous rung could observe
> Public dividend payer: DDM reads the required return straight from price, dividend and growth (V4 p.127).
> Public with traded debt: BYPRP anchors on the bond yield and adds an equity-over-bond premium (V4 p.128).
> Public with return history: CAPM and Fama-French regress excess returns on priced factors (V4 p.130, p.131).
> Private: no return history, so borrow a peer beta (expanded CAPM) or drop beta entirely (build-up) and add size, industry and company-specific premia; illiquidity is handled as a discount for lack of marketability on value, not as a premium in the rate (V4 p.132, p.133, p.134).
> Emerging market: add a country risk premium via the country spread model, scaled by the firm's exposure lambda and by relative equity-to-bond volatility, or move to a global or international CAPM (V4 p.135, p.136).

The private-company premia have economic content, not just labels.
Small size means harder access to capital, uncertain growth and riskier operations, so the size premium is inversely related to size and is best drawn from the lowest market-cap decile, adjusted downward because that decile includes distressed fallen angels a healthy private firm does not resemble (V4 p.132, p.133).
The company-specific premium prices concentration: customers, geography, key people, governance, all judged qualitatively and quantitatively against peers (V4 p.133).
In the build-up approach the ERP is not beta adjusted, so risk-free plus ERP is the required return on an average-risk large-cap stock, and the premia move you down the size and specificity ladder from there (V4 p.134).
Cross-border, the sovereign yield spread approximates country risk, but it is a bond-market number pressed into equity service, which is why Damodaran scales it by the ratio of equity to bond volatility and why the analyst then multiplies by the firm's actual exposure to the risky country (V4 p.135, p.136, p.137).
The global CAPM tends to produce low or even negative betas for emerging market stocks because their correlation with world markets is low, which motivates the two-factor international CAPM with a global index and a wealth-weighted currency index (V4 p.136).

The two mini cases assemble everything, and they are the template for the item set.
Gretna (public, thinly traded BBB debt, redeemable preferred, cyclical engine maker): matrix price the debt to 5.8%, cost the preferred at 70/980 = 7.14%, and notice the CAPM equity estimate of 7.11% is below the preferred yield, which is impossible for a residual claim, so trust the five-factor and BYPRP numbers instead (V4 p.141, p.143, p.144, p.145).
Precision (private, emerging market, software): synthetic A rating from IC 7.63 and D/E 21.2%, cost of debt 5.41% + 1.46% + 2% CRP, unlever the industry beta 1.25 to 1.019 and relever to 1.19, then expanded CAPM and build-up equity costs in the mid-20s and a WACC near 21% (V4 p.147, p.148, p.149, p.150).
The lesson the examiner wants: every input is a choice, the choices have signed biases, and a good analyst cross-checks estimates against each other and against instruments that actually trade.

## Formulas and derivations

**Formula 1: WACC** (V4 p.100)
$$
\text{WACC} = w_d r_d (1 - t) + w_p r_p + w_e r_e
$$
^f-04-03-1

- $w_d, w_p, w_e$: target-structure weights of debt, preferred and common equity, non-negative and summing to 1; $r_d$: pre-tax cost of debt; $t$: marginal (not effective) tax rate; $r_p$, $r_e$: costs of preferred and common equity.
- Holds because each capital provider must earn its own required return on the share of firm value it finances; only debt gets the $(1-t)$ shield because only interest is deductible, and only while the issuer has taxable income and deduction capacity (V4 p.100, p.116).
- If the interest deduction is capped and already exhausted, marginal new debt gets no shield and $r_d$ enters pre-tax (V4 p.116).

**Formula 2: cost of debt decomposition** (V4 p.100)
$$
r_d = r_f + \text{Credit spread}
$$
^f-04-03-2

- $r_f$: benchmark risk-free rate matching the debt's currency and maturity; the spread compensates for default risk, covenants, callability, leverage policy, asset nature and liquidity.
- Holds by no-arbitrage against the government curve: any corporate yield can be quoted as the risk-free rate plus what the market charges for the issuer's specific risks (V4 p.100).

**Formula 3: CAPM required return on equity** (V4 p.100, p.130)
$$
r_e = r_f + \hat{\beta}\,(\text{ERP})
$$
^f-04-03-3

- $\hat{\beta}$: sensitivity of the stock's excess return to the market's excess return; ERP: expected market return over the risk-free rate.
- Derivation: in a one-factor world the only priced risk is covariance with the market, so expected return is linear in beta; beta is estimated from the market model regression (Formula 13) and the ERP from the historical or forward-looking approaches.
- Preferred equity has a stated dividend and a senior claim, so its effective risk premium is smaller than common's, and $r_p < r_e$ always (V4 p.101).

**Formula 4: rate implicit in the lease (RIIL)** (V4 p.113)
$$
\sum_{t=1}^{n} \frac{PMT_t}{(1+r)^t} + \frac{RV_n}{(1+r)^n} = \text{Fair value of asset} + \text{Lessor's direct costs}
$$
^f-04-03-4

- $PMT_t$: lease payments; $RV_n$: residual value accruing to the lessor at end of term; $r$: the implicit lease rate under IFRS 16 and ASC 842.
- Holds because the lessor prices the lease to recover the asset's fair value plus its initiation costs from the payment stream and the residual; the lessee's side is a secured amortizing loan, so leases usually cost less than unsecured borrowing (V4 p.113).
- If residual value or lessor costs are unknown, substitute the incremental borrowing rate (IBR) on a collateralized loan of the same term, or fall back to non-traded-debt methods (V4 p.113, p.114).

> [!tip] Calculator
> Example 4 inputs: `15 N`, `9 +/- ... ` use `PMT = 9`, `PV = -105`, `FV = 10`, `CPT I/Y` gives 4.08 (annual payments, so no P/Y adjustment).

**Formula 5: historical ERP** (V4 p.117)
$$
\widehat{\text{ERP}}_{hist} = \overline{R_{m} - R_{f}}
$$
^f-04-03-5

- Mean (arithmetic or geometric) of a broad market-value-weighted index return minus a government return over the sample.
- Valid only under stationarity: the return-generating process of the past must still describe the future (V4 p.117, p.120).
- Four decisions: index, period, mean type (geometric preferred, less outlier-sensitive, matches terminal wealth), risk-free proxy (long bond favored for duration match) (V4 p.117, p.118, p.119).

**Formula 6: Gordon growth model and the DDM required return** (V4 p.121, p.127)
$$
V_0 = \frac{D_1}{r_e - g} \quad\Longleftrightarrow\quad r_e = \frac{D_1}{P_0} + g
$$
^f-04-03-6

- $D_1$: next-period dividend; $g$: constant perpetual growth of earnings, dividends and price; requires a traded price and stable, predictable dividends (V4 p.127).
- Derivation: the perpetuity-with-growth sum $\sum D_1 (1+g)^{t-1}/(1+r_e)^t$ converges to $D_1/(r_e-g)$ for $r_e > g$; invert for $r_e$.
- Implicit assumption: constant P/E, because price can only outgrow earnings if the multiple expands (V4 p.122).

**Formula 7: DDM-implied (Gordon growth) ERP** (V4 p.122)
$$
\text{ERP} = E\!\left(\frac{D_1}{V_0}\right) + E(g) - r_f
$$
^f-04-03-7

- Apply Formula 6 to a broad index (expected index dividend yield plus consensus earnings growth), then subtract the current risk-free rate.
- Some analysts add buybacks to the yield term to capture total payout, but must then rethink $g$ (V4 p.122).

**Formula 8: multistage index DDM for fast-growing markets** (V4 p.123)
$$
\text{Equity index price} = PV_{0,\text{Stage 1}} + PV_{0,\text{Stage 2}} + PV_{0,\text{Stage 3}}
$$
^f-04-03-8

- Fast growth, transition, mature stages; solve for the IRR $r_e$ that equates the three present values to the index level, then subtract the risk-free proxy for the ERP (V4 p.123).

**Formula 9: Grinold-Kroner ERP** (V4 p.123)
$$
\text{ERP} = \left[\underbrace{DY}_{\text{income}} + \underbrace{\Delta(P/E)}_{\text{repricing}} + \underbrace{i + g - \Delta S}_{\text{EPS growth}}\right] - E(r_f)
$$
^f-04-03-9

- $DY$: expected index dividend yield; $\Delta(P/E)$: expected per-year change in the multiple (commonly 0 unless the market looks mis-valued); $i$: expected inflation; $g$: real GDP growth as the proxy for real EPS growth; $\Delta S$: expected percent change in shares outstanding, so net buybacks make $\Delta S$ negative and $-\Delta S$ positive; $E(r_f)$: expected risk-free return, matched to a long horizon (V4 p.123, p.124).
- Derivation: expected equity return = income + capital gain; capital gain = repricing + EPS growth; EPS growth in nominal terms = inflation + real growth - dilution; subtract the risk-free rate to leave the premium.
- A rise in $i$ leaves the ERP roughly unchanged because $E(r_f)$ rises with it; a fall in $DY$ lowers the ERP one for one (V4 p.125).
- Not appropriate where the stock market is a small share of the economy (V4 p.125).

> [!tip] Calculator
> Pure addition; the skill is input selection.
> Practice Problem 4 keystrokes: `1 + 1 + 4 + 4 - 0 = 10`, `- 7 = 3.0`.
> Always take long-term inflation (not the current spot rate) and the long-bond yield (not the bill) for a long-horizon ERP (V4 p.151, p.153).

**Formula 10: TIPS-implied expected inflation** (V4 p.124)
$$
i = \frac{1 + YTM_{\text{Treasury}}}{1 + YTM_{\text{TIPS}}} - 1 \approx YTM_{\text{Treasury}} - YTM_{\text{TIPS}}
$$
^f-04-03-10

- Same-maturity nominal and inflation-protected government yields; the Fisher relation makes the ratio the market's compensated inflation expectation (V4 p.124).

**Formula 11: multiyear DDM with a terminal price** (V4 p.128)
$$
P_0 = \sum_{t=1}^{n} \frac{D_t}{(1+r_e)^t} + \frac{P_n}{(1+r_e)^n}
$$
^f-04-03-11

- Solve for $r_e$ as the IRR of the cash flow vector; the curriculum example uses $(-40, 1, 1.25, 1.35, 46.5)$ and gets 6.015% (V4 p.128).

> [!tip] Calculator
> CF worksheet: `CF0 = -40`, `C01 = 1`, `C02 = 1.25`, `C03 = 1.35`, `C04 = 46.5` (final dividend 1.50 plus terminal price 45), `IRR CPT` gives 6.015.

**Formula 12: bond yield plus risk premium (BYPRP)** (V4 p.128)
$$
r_e = r_d + RP
$$
^f-04-03-12

- $r_d$: YTM on the company's long-term traded debt; $RP$: historical mean excess of equity index returns over corporate bond index returns.
- Holds because equity is junior to debt in the same capital structure, so it must earn the debt yield plus compensation for the extra risk; the weakness is that $RP$ is arbitrary and traded debt is required (V4 p.128, p.129).

**Formula 13: market model beta regression** (V4 p.130)
$$
(r_{i,t} - r_{f,t}) = b_0 + b_1 (r_{m,t} - r_{f,t}) + \varepsilon_t
$$
^f-04-03-13

- $\hat{b}_1$ proxies $\beta_i$ in the CAPM; choices of index, estimation window and risk-free proxy all move the estimate; a variant regresses raw returns without subtracting $r_f$ (V4 p.130).

**Formula 14: Fama-French three-factor model** (V4 p.130)
$$
r_e = r_f + \beta_1 \text{ERP} + \beta_2 \text{SMB} + \beta_3 \text{HML}
$$
^f-04-03-14

- SMB: small-minus-big size premium; HML: high-minus-low book-to-market value premium; betas come from regressing the stock's excess returns on the three factors (V4 p.130, p.131).
- The market beta here normally differs from the CAPM beta because the added factors absorb part of the covariance (V4 p.132).

**Formula 15: Fama-French five-factor model** (V4 p.131)
$$
r_e = r_f + \beta_1 \text{ERP} + \beta_2 \text{SMB} + \beta_3 \text{HML} + \beta_4 \text{RMW} + \beta_5 \text{CMA}
$$
^f-04-03-15

- Adds RMW (robust-minus-weak profitability premium) and CMA (conservative-minus-aggressive investment premium) (V4 p.131).
- A negative factor beta times a positive premium subtracts from the required return, as with Gretna's RMW beta of -0.19 (V4 p.142, p.145).

**Formula 16: expanded CAPM for private companies** (V4 p.133)
$$
r_e = r_f + \beta_{peer}(\text{ERP}) + SP + SCRP
$$
^f-04-03-16

- $\beta_{peer}$: beta estimated from public same-industry peers, unlevered and relevered to the subject's capital structure (Formula 21); $SP$: size premium, inversely related to size, ideally from the lowest-decile micro-caps with a downward adjustment for the distressed firms that population contains; $SCRP$: company-specific premium for concentration, key-person and governance risks (V4 p.132, p.133).
- Illiquidity is not added here; it is applied to value as a discount for lack of marketability (V4 p.132).

**Formula 17: build-up approach** (V4 p.134)
$$
r_e = r_f + \text{ERP} + SP + IP + SCRP
$$
^f-04-03-17

- No beta: the ERP enters with an implicit beta of 1.0, so $r_f + \text{ERP}$ is the required return on an average-risk large-cap stock, then the size premium (beta-adjusted) steps down to micro-cap and the industry and specific premia finish the build (V4 p.134).
- Use when comparable public companies are unavailable or dubious (V4 p.134).

**Formula 18: country spread model for an emerging market ERP** (V4 p.135)
$$
\text{ERP} = \text{ERP}_{\text{developed market}} + \lambda \times \text{CRP}
$$
^f-04-03-18

- $\lambda$: the company's exposure to the local country (fraction of sales or operations); CRP: country risk premium, often proxied by the sovereign yield spread of the local country's developed-currency bond over the developed sovereign (V4 p.135).
- Weakness: a bond spread is being used to price equity risk (V4 p.135).

**Formula 19: Damodaran volatility-adjusted CRP** (V4 p.136)
$$
\text{CRP} = \text{Sovereign yield spread} \times \frac{\sigma_{\text{Equity}}}{\sigma_{\text{Bond}}}
$$
^f-04-03-19

- $\sigma_{\text{Equity}}, \sigma_{\text{Bond}}$: volatilities of the local country's equity and bond markets; scales the bond spread up to equity-market risk; requires the local market to have both return histories (V4 p.136).
- Then multiply by $\lambda$ for the subject company's actual exposure, as in Example 12 (V4 p.137).

**Formula 20: international CAPM (ICAPM)** (V4 p.136)
$$
E(r_e) = r_f + \beta_G \left[E(r_{gm}) - r_f\right] + \beta_C \left[E(r_c) - r_f\right]
$$
^f-04-03-20

- $r_{gm}$: global index (MSCI ACWI, FTSE All-World); $r_c$: wealth-weighted foreign currency index whose return is expected currency appreciation plus each country's risk-free rate; $\beta_G$ is lower for locally oriented companies, $\beta_C$ reflects exchange-rate sensitivity of cash flows (V4 p.136).
- Motivated because the single-factor global CAPM yields low or negative betas for emerging markets whose correlation with world returns is low (V4 p.136).

**Formula 21: unlevering and relevering beta** (V4 p.149)
$$
\beta_{Asset} = \beta_{peer}\left[\frac{1}{1 + (1 - t_{peer})\frac{D_{peer}}{E_{peer}}}\right], \qquad
\beta_{subject} = \beta_{Asset}\left[1 + (1 - t_{subject})\frac{D_{subject}}{E_{subject}}\right]
$$
^f-04-03-21

- Strip the peer's financial leverage at the peer's tax rate and D/E, then re-apply the subject's; each firm's own tax rate and own D/E, never mixed (V4 p.149).
- Holds because equity beta scales with the equity's leveraged exposure to the same operating assets; the tax term reflects the debt shield's risk absorption.

**Formula 22: cost of preferred equity** (V4 p.144)
$$
r_p = \frac{D_p}{P_p}
$$
^f-04-03-22

- Perpetuity yield: the stated dividend (rate times par) over the current price; it is Formula 6 with $g = 0$ (V4 p.144).
- Gretna: $70 / 980 = 7.14\%$, the module's sanity-check floor for the common equity estimate (V4 p.144, p.145).

**Formula 23: matrix pricing interpolation** (V4 p.143, p.144)
$$
YTM_{m} = \overline{YTM}_{short} + (m - m_{short}) \times \frac{\overline{YTM}_{long} - \overline{YTM}_{short}}{m_{long} - m_{short}}
$$
^f-04-03-23

- Average the YTMs of same-rating liquid bonds at each quoted maturity, then interpolate linearly to the subject maturity $m$; add a bump for the subject bond's extra illiquidity (V4 p.143, p.144).

> [!tip] Calculator
> Each semiannual YTM first: Bond 1 `N = 8, PV = -99.5, PMT = 2.5, FV = 100, CPT I/Y` gives 2.570, times 2 is 5.140.
> Then per-year increment: `(6.011 - 5.166) / 4 = 0.211` and step out from the 4-year average.

## Worked examples

### Example 1: external factors and cost of capital (V4 p.102, p.103)

Setup: two same-industry companies raise capital in different countries; Country A has wide spreads, high rate volatility, high inflation, low capital availability, 15% tax; Country B the reverse with 25% tax.

Part 1: Country B issuers have the lower cost of capital.
Narrow spreads, low rate volatility, low inflation and abundant capital all lower both debt and equity costs, and the higher 25% tax rate makes the interest shield worth more, cutting the after-tax cost of debt (V4 p.103).

Part 2: raising Country A's tax rate from 15% to 25% lowers the after-tax cost of debt there, provided issuers have taxable income to absorb the deduction (V4 p.103).

Part 3: the buried assumption is deductibility.
If interest is not deductible in Country A, the tax change does nothing to WACC; if it is and there is taxable income, WACC falls (V4 p.103). ^ex-04-03-1

### Example 2: company-specific factors and cost of capital (V4 p.107, p.108)

Setup: common-size balance sheets and metrics for two companies; Company 1 has cash plus securities 20%, intangibles 10%, PP&E 46%, net debt/EBITDA 2.1, IC 12.6, low operating leverage, top-five customers 15% of sales, putable debt; Company 2 has 17% liquid assets, 24% intangibles, 2.5 leverage, IC 7.9, high operating leverage, 27% concentration, callable debt.

Company 1 has the lower cost of capital, on five counts (V4 p.108).
More liquid assets (20% versus 17%) and far fewer intangibles (10% versus 24%), plus 46% PP&E available as collateral.
Lower financial leverage: net debt/EBITDA 2.1 versus 2.5 and IC 12.6 versus 7.9.
Lower operating leverage and a diversified customer base (15% versus 27% concentration) mean steadier earnings.
Putable debt prices below callable debt because the put benefits the investor while the call benefits the issuer (V4 p.106, p.108). ^ex-04-03-2

### Example 3: knowledge check, cost of capital factors (V4 p.109, p.110)

Q1: sign each factor's effect on the cost of capital.
High operating leverage: raises it (more earnings volatility per unit of revenue change).
High earnings predictability: lowers it.
High supply of available capital in the region: lowers it (better terms for issuers).
Weak legal and regulatory systems: raises it (investors demand compensation for weak protections) (V4 p.110).

Q2: subscription model, tangible asset base, no customer above 1% of revenue (Company 2) beats pay-per-use, intangible-heavy, 60% five-customer concentration (Company 1) on all three characteristics, so Company 2 has the lower cost of capital and can support more debt (V4 p.110).

Q3: favorable debt-issuance conditions are low benchmark rates (expansionary monetary policy) and tight credit spreads (economic expansion), because $r_d = r_f + \text{spread}$ (V4 p.110).

Q4: put features and conversion features lower the cost of debt at issuance, because both give investors a valuable option they pay for by accepting a lower yield (V4 p.111). ^ex-04-03-3

### Example 4: synthetic credit ratings (V4 p.112)

Setup: a proprietary schedule maps IC and D/E ranges to rating classes; Gamma Company (non-traded debt) has IC 1.5 and D/E 43%.

Part 1: the two ratios conflict.
IC of 1.5 falls in the B band (1.4 < IC < 2.0); D/E of 43% falls in the BBB band (42% < D/E < 44%), so no single rating drops out (V4 p.112).

Part 2: break the tie with trend analysis and judgment.
If IC has been trending up, nudge toward BB rather than B; the model is an input to judgment, not a substitute (V4 p.112, p.113).
Also remember an issuer's rating can differ from its issues' ratings, since collateral, seniority and convertibility can lift a specific bond above the issuer rating (V4 p.113). ^ex-04-03-4

### Example 5: leasing costs (V4 p.114, p.115)

Setup: G&S Airlines, unsecured IBR 6%, cost of equity 11%; 15-year lease, EUR9.0m annual payments in arrears, asset fair value EUR100m, lessor direct costs EUR5m, residual value EUR10m at year 15.

Part 1: implied lease rate.
Time-0 outflow $= 100 + 5 = 105$; inflows $= 9$ per year for 15 years plus $10$ at year 15 (year 15 total 19).
Solve $105 = \sum_{t=1}^{15} 9/(1+r)^t + 10/(1+r)^{15}$ for $r$: $r = 4.08\%$ (V4 p.114, p.115).
Python check: `brentq` on the NPV gives 0.04080, or 4.08%, matching the curriculum.

Part 2: lease versus buy.
At 4.08% the lease beats the 6% unsecured IBR (it is secured financing) and beats dilutive equity at 11%; the lease also avoids ownership risks but adds leverage to the balance sheet (V4 p.115). ^ex-04-03-5

### Example 6: cost of debt summary knowledge check (V4 p.116, p.117)

Q1: to cost a lease you need the lease payments, the residual value, the asset's fair value, the lessor's direct costs, and the lease term, exactly the Formula 4 inputs (V4 p.116).

Q2: if the issuer has exhausted a cap on interest deductibility, do not tax-adjust the cost of new debt; the marginal borrowing gets no shield, so the pre-tax and after-tax costs coincide (V4 p.116).

Q3: for non-traded debt, use matrix pricing off similar-maturity, similar-rating traded bonds, or a synthetic rating from fundamentals (IC and leverage ratios) followed by the rating class's YTM or spread (V4 p.116, p.117). ^ex-04-03-6

### Example 7: ERP estimation using the historical approach (V4 p.120, p.121)

Q1: a very short-term government bill is justified because it is effectively a zero-coupon bond whose stated yield is truly earned (no coupon reinvestment risk); the disadvantage is a duration mismatch with infinite-life equity (V4 p.120).

Q2: the key assumption behind using any historical ERP in a pricing model is stationarity: the return-generating process is unchanged going forward (V4 p.120).

Q3: the geometric mean is preferred because it is less sensitive to outliers and compounds to the expected terminal value of wealth (V4 p.120).

Q4: two analysts' estimates.
Smith (Russell 3000, 35 years, 30-year bond, arithmetic): $12.96\% - 6.25\% = 6.71\%$.
Muller (S&P 500, 65 years, 3-month bill, geometric): $11.23\% - 3.11\% = 8.12\%$ (V4 p.121).
Python check: `12.96-6.25 = 6.71`, `11.23-3.11 = 8.12`.

Q5: both are valid; they just resolve the four decisions (index, period, mean, risk-free proxy) differently, and the spread between them is the estimation risk the exam wants you to respect (V4 p.121). ^ex-04-03-7

### Example 8: ERP estimation using the constant growth DDM (V4 p.122)

Setup: FTSE 100, forward dividend yield 1.94% (range 1.5% to 3.5%), expected long-term earnings growth 5.0% (4% to 6%), long Gilt yield 1.63% (1.5% to 2.5%).

Part 1 (Formula 7): $\text{ERP} = 1.94\% + 5.0\% - 1.63\% = 5.31\%$ (V4 p.122).
Python check: `1.94+5.0-1.63 = 5.31`.

Part 2: at the forecast extremes the ERP spans $1.5 + 4 - 2.5 = 3\%$ to $3.5 + 6 - 1.5 = 8\%$, so a simulation over the analyst distribution is warranted; the range dwarfs most other WACC input uncertainties (V4 p.122). ^ex-04-03-8

### Example 9: ERP estimation using the forward-looking approach (V4 p.124, p.125)

Part 1 (Formula 10): 10-year Treasury 2.3%, TIPS 0.66%.
$i = 1.023/1.0066 - 1 = 0.0163$, or about 1.6% (V4 p.124).
Python check: `1.023/1.0066-1 = 0.01629`.

Part 2 (Formula 9): two scenarios.
Scenario 1: $\{2.2 + 0 + [1.6 + 3.0 - (-0.7)]\} - 2.5 = \{2.2 + 5.3\} - 2.5 = 5.0\%$.
Scenario 2: $\{2.0 + 1.0 + [3.0 + 2.0 - 0.0]\} - 3.0 = 8.0 - 3.0 = 5.0\%$ (V4 p.124, p.125).
Python check: `2.2+0+1.6+3.0+0.7-2.5 = 5.0`, `2.0+1.0+3.0+2.0-3.0 = 5.0`.
Note: the curriculum's lead-in sentence for Scenario 1 says "the ERP estimate is 3.6%", but its own displayed computation and the correct arithmetic give 5.0%; 5.0% is right, and the buyback term $-\Delta S = +0.7$ is the step that produces it.

Part 3: higher expected inflation leaves the ERP roughly unchanged (raises $i$ and $E(r_f)$ together); lower expected income lowers the ERP through $DY$ (V4 p.125).

Part 4: Grinold-Kroner is inappropriate where the stock market is not a sufficiently large share of the economy, as in many developing countries (V4 p.125). ^ex-04-03-9

### Example 10: ERP summary knowledge check (V4 p.126, p.127)

Q1: the four historical-approach decisions are the index, the time period, the mean measure, and the risk-free proxy (V4 p.126).

Q2: the long bond's YTM is not truly risk free (coupon reinvestment), but it is still used as the approximation for the bond's expected return and matches equity duration better (V4 p.126).

Q3: both approaches from one table.
Historical: $9.96\% - 3.15\% = 6.81\%$ (geometric index mean minus geometric short-bond mean).
Grinold-Kroner: $\{1.8 - 1.2 + (1.9 + 2.7 - 0.0)\} - 0.96 = 5.20 - 0.96 = 4.24\%$ (V4 p.126, p.127).
Python check: `9.96-3.15 = 6.81`, `1.8-1.2+1.9+2.7-0.96 = 4.24`.
Note the negative repricing term: expected P/E contraction of 1.2% per year subtracts inside the bracket.

Q4: macro-model limitations: the forecasts (inflation, real EPS growth) come from financial and economic models that carry modeling error and behavioral biases (V4 p.127). ^ex-04-03-10

### Example 11: cost of equity estimation using the BYPRP approach (V4 p.129)

Setup: company bond yield 4.3%; historical equity-over-corporate-bond premium 6.1%.

Formula 12: $r_e = 0.043 + 0.061 = 0.1040$, or 10.40% (V4 p.129).
Python check: `0.043+0.061 = 0.104`.

Considerations: the premium may be non-stationary, the company may lack traded debt, and with multiple issues there is no prescription beyond common practice (use the long-term bond's YTM) (V4 p.129). ^ex-04-03-11

### Example 12: cost of equity estimation using the Fama-French five-factor model (V4 p.131)

Setup: betas 1.2 (market), 0.10 (SMB), -0.20 (HML), 0.5 (RMW), 0.2 (CMA); premiums 6.5%, 1.8%, 4.0%, 2.0%, 1.0%; $r_f = 3.82\%$.

Formula 15:
$r_e = 0.0382 + (1.2)(0.065) + (0.10)(0.018) + (-0.2)(0.04) + (0.5)(0.02) + (0.2)(0.01)$.
$= 0.0382 + 0.078 + 0.0018 - 0.008 + 0.01 + 0.002 = 0.1220$, or 12.2% (V4 p.131).
Python check: `0.0382+0.078+0.0018-0.008+0.01+0.002 = 0.1220`.
The negative HML beta subtracts 80 bps: a growth-tilted stock is short the value factor (V4 p.131). ^ex-04-03-12

### Example 13: CRP with the Damodaran adjustment (V4 p.137)

Setup: Makinassi is headquartered in Country X (sovereign spread 1.5%, equity vol 2.0%, bond vol 1.0%) with 40% of sales in Country Y (spread 3.2%, equity vol 4.0%, bond vol 2.5%).

Step 1: relevant sovereign yield spread $= 3.2\% - 1.5\% = 1.7\%$.
Step 2 (Formula 19): $\text{CRP} = 0.017 \times 0.04/0.025 = 0.0272$, using Country Y's own equity and bond volatilities.
Step 3 (exposure): $\lambda \times \text{CRP} = 0.40 \times 0.0272 = 0.01088$, so add 1.088% to Makinassi's cost of equity (V4 p.137).
Python check: `0.017*0.04/0.025 = 0.0272`, `0.4*0.0272 = 0.01088`. ^ex-04-03-13

### Example 14: knowledge check, required return on equity (V4 p.138, p.139, p.140)

Q1: CAPM is a one-factor model (market only); the Fama-French models add size, value and, in the five-factor version, profitability and investment factors (V4 p.138).

Q2: DDM direction-of-effect table (all else constant): a higher current dividend or higher growth raises $r_e$; a higher share price lowers it; the decreases mirror those signs (a lower price raises $r_e$) (V4 p.138).

Q3: three-factor premium: $r_e - r_f = 0.003 + (1.2)(0.05) - (0.4)(0.01) + (0.2)(0.04) = 0.067$; with $r_f = 2\%$, $r_e = 0.087$, or 8.7% (V4 p.139).
Python check: `0.003+0.06-0.004+0.008 = 0.067`, `+0.02 = 0.087`.

Q4: $D_0 = 2.50$, $P_0 = 50$, $g = 5\%$: $r_e = 2.50(1.05)/50 + 0.05 = 0.0525 + 0.05 = 0.1025$, or 10.25% (V4 p.139).
Python check: `2.625/50+0.05 = 0.1025`.
The trap is using $D_0/P_0 = 5\%$; the model needs $D_1$.

Q5 and Q6: an upward growth revision raises both the yield term (through $D_1$) and $g$, so $r_e$ rises; a price decline raises the dividend yield, so $r_e$ rises (V4 p.139).

Q7: CAPM: $r_e = 0.06 + 0.8(0.10 - 0.06) = 0.092$, or 9.2% (V4 p.140).
Q8: Fama-French three-factor with intercept: $r_e - 0.06 = 0.01 + 0.75(0.04) + 0.15(0.05) + 0.05(0.02) = 0.0485$, so $r_e = 10.85\%$ (V4 p.140).
Python check: `0.01+0.03+0.0075+0.001 = 0.0485`, `+0.06 = 0.1085`.
Q9: the SMB and HML exposures add $0.0075 + 0.001 = 0.0085$, or 0.85%, which the single-factor CAPM cannot capture (V4 p.140). ^ex-04-03-14

### Example 15: Mini-case 1, Gretna Engines (V4 p.140 to p.146)

Setup: small-cap public engine maker, cyclical, high operating leverage; capital structure 20% debt (7% coupon, 7 years, semiannual, BBB, thinly traded), 15% preferred (7% rate, redeemable at par 1,000, price 980), 65% common.
Four liquid BBB comparables: 5% coupon 4-year at 99.50; 7% coupon 4-year at 106.46; 6% coupon 8-year at 100; 8% coupon 8-year at 112.42.
CAPM beta 0.91; FF5 betas 0.95, 0.45, 0.14, -0.19, 0.30 against premiums 5.5%, 1.8%, 3.9%, 3.1%, 3.7%; $r_f = 2.1\%$ (20-year); BYPRP premium 6.2% (V4 p.141, p.142).

Q1, business-model risk factors: cyclical revenue and earnings volatility, relatively illiquid assets (inventory and production PP&E), and high operating leverage (V4 p.142).

Q2, matrix pricing (Formula 23).
Semiannual YTMs: Bond 1: N 8, PV -99.5, PMT 2.5, FV 100 gives 2.570% x 2 = 5.140%.
Bond 2: N 8, PV -106.46, PMT 3.5 gives 2.595% x 2 = 5.191%.
Bond 3: N 16, PV -100, PMT 3 gives 3.000% x 2 = 6.000%.
Bond 4: N 16, PV -112.42, PMT 4 gives 3.010% x 2 = 6.021% (V4 p.143).
Averages: 4-year $(5.140 + 5.191)/2 = 5.166\%$; 8-year $(6.000 + 6.021)/2 = 6.011\%$.
Increment: $(6.011 - 5.166)/4 = 0.211\%$ per year.
Interpolated: 5-year 5.377%, 6-year 5.588%, 7-year 5.799%, so about 5.8%, plus a touch more for Gretna's illiquidity (V4 p.144).
Python check: semiannual roots give 5.1399%, 5.1907%, 6.0000%, 6.0209%; averages 5.1653% and 6.0104%; 7-year 5.7992%.

Q3, preferred (Formula 22): $r_p = 70/980 = 7.14\%$ (V4 p.144).
Python check: `70/980 = 0.07143`.

Q4, refinancing the preferred with debt: the new 35%-debt structure's marginal debt should price above the current 5.8% debt estimate (more leverage, still senior) but below the 7.14% preferred cost it replaces (V4 p.144).

Q5, timing: management's willingness to redeem at par (above the 980 market price) signals it reads the risk-free rate as low and spreads as tight (V4 p.144, p.145).

Q6, lowering the new issue's cost: secure it with PP&E collateral, or embed a put or a conversion feature investors will pay for in yield (V4 p.145).

Q7, three equity estimates (Formulas 3, 15, 12).
CAPM: $0.021 + 0.91(0.055) = 0.0711$, or 7.11%.
FF5: $0.021 + 0.95(0.055) + 0.45(0.018) + 0.14(0.039) - 0.19(0.031) + 0.30(0.037) = 0.0920$, or 9.20%.
BYPRP: $0.058 + 0.062 = 0.120$, or 12.0% (V4 p.145).
Python check: `0.021+0.05005 = 0.07105`; `0.021+0.05225+0.0081+0.00546-0.00589+0.0111 = 0.09202`; `0.058+0.062 = 0.12`.

Q8, the sanity check: common equity is junior to preferred, so $r_e$ must exceed $r_p = 7.14\%$; the CAPM's 7.11% is below it and therefore not realistic (V4 p.145, p.146).

Q9, KM's ERP choices: a short-term bill basis (under a normal curve) and an arithmetic mean both push the historical ERP estimate up, so her 5.5% is likely high relative to a long-bond, geometric-mean estimate (V4 p.146). ^ex-04-03-15

### Example 16: Mini-case 2, Precision Irrigation (V4 p.146 to p.150)

Setup: private emerging-market software target; total debt 18.4, total assets 105.2, EBITDA 12.2, interest 1.6, tax 20%; industry averages: debt 296.4, assets 1,276.2, EBITDA 177.4, interest 23.5, beta 1.25, tax 25%.
Synthetic schedule: A rating for 7 < IC < 9 and 20% < D/E < 25%, spread 1.46%; 10-year government yield 5.41%; premiums ERP 6%, SP 5%, IP 1%, SCRP 6%; CRP 2%; current structure is the target (V4 p.147, p.148).

Q1, after-tax cost of debt.
IC $= 12.2/1.6 = 7.63$; D/E $= 18.4/(105.2 - 18.4) = 0.2120$.
Both land in the A band, so the spread is 1.46%.
$r_d = 5.41\% + 1.46\% + 2.00\% \text{ (CRP)} = 8.87\%$; after tax $8.87\% \times (1 - 0.20) = 7.096\%$ (V4 p.148).
Python check: `12.2/1.6 = 7.625`, `18.4/86.8 = 0.21198`, `5.41+1.46+2 = 8.87`, `8.87*0.8 = 7.096`.

Q2, why the SP sits near the high end: Precision's 105.2m of assets is less than a tenth of the 1,276.2m industry average, and the SP is inversely related to size (V4 p.148).

Q3, SCRP directionality.
Higher: intangible-heavy assets (47% versus 32%), less cash (9% versus 14%), 70% of revenue from five nearby customers (customer and geographic concentration), founder-CEO with no succession plan (key-person risk).
Lower: 60% subscription (recurring) revenue, and leverage below the industry (D/E 0.2120 versus $296.4/(1276.2 - 296.4) = 0.3025$; IC 7.63 versus $177.4/23.5 = 7.55$) (V4 p.148, p.149).

Q4, two equity estimates.
Unlever the industry beta (Formula 21) at the industry tax rate and D/E: $\beta_{Asset} = 1.25 \times \frac{1}{1 + (1 - 0.25)(0.3025)} = 1.019$.
Relever at Precision's tax rate and D/E: $\beta_{Precision} = 1.019 \times [1 + (1 - 0.20)(0.2120)] = 1.19$.
Expanded CAPM plus IP and CRP: $r_e = 5.41\% + 1.19(6\%) + 5\% + 1\% + 6\% + 2\% = 26.55\%$ (26.56% without rounding the beta) (V4 p.149, p.150).
Build-up as the curriculum computes it: $r_e = 5.41\% + 6\% + 5\% + 6\% + 2\% = 24.41\%$ (V4 p.150).
Python check: `1.25/(1+0.75*0.3025) = 1.0188`, `1.0188*(1+0.8*0.21198) = 1.1916`, `5.41+7.15+14 = 26.56`, `5.41+19 = 24.41`.
Note two curriculum inconsistencies: the solution's own headline calls the build-up answer "25.41%" while its displayed sum is 24.41%; the 25.41% figure is what Formula 17 gives if the 1% IP from Exhibit 20 is included, and the displayed computation simply omits IP.
The subsequent WACC uses 24.41%, so follow the displayed arithmetic on the exam unless the question explicitly lists an IP to include.

Q5, WACC (Formula 1) with the build-up estimate.
$w_d = 18.4/105.2 = 0.1749$; $w_e = 86.8/105.2 = 0.8251$.
$\text{WACC} = 0.1749 \times 0.0887 \times (1 - 0.20) + 0.8251 \times 0.2441 = 0.0124 + 0.2014 = 0.2138$, or 21.38% (V4 p.150).
Python check: `0.17490*0.0887*0.8+0.82510*0.2441 = 0.21382`.
The solution's lead sentence says "21.13%", but its own displayed computation gives 21.38%; 21.38% is correct for the stated inputs. ^ex-04-03-16

## Item-set patterns

> [!warning] Trap 1: Grinold-Kroner input selection
> The vignette supplies current inflation and long-term inflation, a short rate and a 10-year rate, forecast public company earnings growth and forecast real GDP growth.
> Correct: for a long-horizon ERP use long-term inflation as $i$, real GDP growth as $g$, and the long-bond yield as $E(r_f)$, with $\Delta S = 0$ unless net issuance is given (V4 p.123, p.124, p.153).
> Distractors: the 6% current inflation, the 9% short rate, and the 5% nominal earnings-growth forecast (which double counts inflation against $i$) each generate a wrong but computable answer (V4 p.151).

> [!warning] Trap 2: the sign of the dilution term
> $\Delta S$ is the change in shares outstanding, and it enters as $-\Delta S$.
> Correct: net buybacks mean $\Delta S < 0$, so they add to expected EPS growth, as in Scenario 1 where $-(-0.7) = +0.7$ (V4 p.124).
> Distractor: subtracting 0.7 instead of adding it, giving 3.6% instead of 5.0%; the curriculum's own stray "3.6%" shows how tempting this is.

> [!warning] Trap 3: historical ERP bias direction
> A backfilled index history, a market disaster window, or a bill-plus-arithmetic-mean choice is described and the question asks the bias direction.
> Correct: backfilling with surviving firms biases the ERP up; an unrepresentative disaster with no offsetting boom biases it down; a short-rate basis under a normal curve and an arithmetic mean each bias it up (V4 p.120, p.146, p.153).
> Distractors: assuming any disruption biases upward, or reasoning from the current rate level instead of the sample-period relationship.

> [!warning] Trap 4: pairing the ERP basis with the wrong current risk-free rate
> The curve is inverted: short rate 9%, 10-year 7%, and the historical ERP was defined against short rates.
> Correct: a bill-based ERP is already high (normal-curve sample), and adding today's 9% short rate stacks a second upward push, so long-term required return estimates are biased upward (V4 p.152, p.153).
> Distractor: "no effect" reasoning that treats the ERP and the risk-free proxy as independent choices.

> [!warning] Trap 5: matrix pricing mechanics
> Four semiannual-pay comparables at two maturities bracket the subject bond's maturity.
> Correct: solve each semiannual YTM, double it, average within maturity, interpolate linearly per year, then note the illiquid subject deserves a slightly higher yield (V4 p.143, p.144).
> Distractors: forgetting to double the semiannual rate, averaging all four bonds into one number, or interpolating with the raw 4-period difference instead of the per-year increment.

> [!warning] Trap 6: synthetic rating with conflicting ratios
> IC implies one rating class and D/E implies another (Gamma: B versus BBB).
> Correct: acknowledge the conflict, look at ratio trends, and apply judgment; also distinguish issuer ratings from issue ratings that collateral or seniority can lift (V4 p.112, p.113).
> Distractor: mechanically picking the rating from whichever ratio appears first in the exhibit.

> [!warning] Trap 7: the preferred-yield sanity check
> Cost of equity estimates from CAPM, FF5 and BYPRP are given alongside a traded preferred yielding 7.14%.
> Correct: common equity is junior to preferred, so any common equity estimate below the preferred yield (Gretna's 7.11% CAPM) is unrealistic and should be discarded (V4 p.145, p.146).
> Distractor: averaging the three estimates anyway, or preferring the CAPM because it is "the standard model".

> [!warning] Trap 8: expanded CAPM versus build-up
> Both private-company recipes appear with the same premium exhibit.
> Correct: expanded CAPM multiplies the ERP by a relevered peer beta and has no IP in the curriculum's Formula 16 as applied (though the Precision solution adds one); build-up applies the ERP at an implicit beta of 1.0 and includes the IP (V4 p.133, p.134, p.150).
> Distractors: beta-multiplying in the build-up, forgetting SP or SCRP, and adding a separate illiquidity premium when illiquidity belongs in the discount for lack of marketability (V4 p.132).

> [!warning] Trap 9: unlever-relever bookkeeping
> Peer beta, peer D/E and tax rate, subject D/E and tax rate all appear in one exhibit.
> Correct: unlever with the peer's $(1-t)$D/E, relever with the subject's, as in $1.25 \to 1.019 \to 1.19$ (V4 p.149).
> Distractors: relevering with the peer's tax rate, skipping the unlevering step entirely, or using book equity where the schedule defines D/E off assets minus debt.

> [!warning] Trap 10: country risk premium assembly
> A sovereign yield spread, equity and bond volatilities, and a sales-exposure percentage are all given.
> Correct: spread times $\sigma_E/\sigma_B$ gives the CRP; multiply by $\lambda$ (exposure) before adding to the cost of equity; for cost of debt, add the CRP without the volatility scaling (V4 p.136, p.137, p.148).
> Distractors: stopping at the raw spread, inverting the volatility ratio, or forgetting the 40% exposure weight (2.72% instead of 1.088%).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Cost-of-Capital-Advanced-Topics-Practice-Problems]]

## Cross-links

- [[LM01-Analysis-of-Dividends-and-Share-Repurchases]]: payout policy sets the dividend yield and the buyback flows that feed the DDM-implied ERP and the $\Delta S$ term of Grinold-Kroner, and share repurchases change leverage and therefore the relevered beta.
- [[LM04-Corporate-Restructuring]]: the WACC built here is the discount rate for restructuring and acquisition evaluation, and leverage changes from LBOs or divestitures rerun this module's spread, rating and beta machinery.
- [[LM02-Discounted-Dividend-Valuation]]: the Gordon growth and multistage models are developed fully there; this module inverts them to extract required returns and market-implied ERPs.
- [[LM06-Private-Company-Valuation]]: the expanded CAPM, build-up approach, size and company-specific premia and the discount for lack of marketability reappear there as the valuation inputs for private targets.
- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: the choice of risk-free proxy, the slope of the curve that signs the bill-versus-bond ERP bias, and the TIPS breakeven inflation reading all come from term-structure analysis.

## Self-test

Vignette A for Q1 to Q3: Riva, an analyst, is estimating a long-horizon ERP for a developed market.
The 10-year nominal government yield is 4.2% and the 10-year inflation-protected yield is 1.9%.
Her forward-looking inputs are: expected index dividend yield 2.4%, expected repricing 0.5% per year, expected real GDP growth 2.5%, and expected net buybacks of 1.0% of shares per year.
She uses the 10-year nominal yield as the expected risk-free return.
Her colleague prefers a historical estimate from a 40-year index series that was launched 25 years ago with 15 years of backfilled returns.

> [!question] Q1
> The market-implied expected inflation rate from the government yields is closest to:
> A. 1.9%.
> B. 2.26%.
> C. 2.30%.

> [!question] Q2
> Riva's Grinold-Kroner ERP estimate is closest to:
> A. 2.46%.
> B. 3.96%.
> C. 4.46%.

> [!question] Q3
> Relative to an unbiased estimate, the colleague's historical ERP is most likely:
> A. biased upward because of survivorship in the backfilled years.
> B. biased downward because backfilled data raise the return variance.
> C. unbiased if the arithmetic mean is used.

Vignette B for Q4 to Q6: Precision-style target Karst Systems has non-traded 6-year debt, EBITDA of 14.0m, interest expense of 2.0m, total debt of 38.0m and total assets of 133.0m.
A synthetic rating schedule assigns A for 6 < IC < 9 with a 1.6% spread and BBB for 4 < IC < 6 with a 2.3% spread, with matching D/E bands of 25% to 35% for A and 35% to 45% for BBB.
Liquid same-rating bonds give an average 4-year YTM of 5.2% and an average 8-year YTM of 6.4%.
The 10-year government yield is 4.1%, the analyst adds a 1.5% country risk premium to debt, the marginal tax rate is 25%, and Karst is at its cap for interest deductibility.

> [!question] Q4
> Using IC and the debt-to-equity ratio (equity measured as assets minus debt), Karst's synthetic rating is best described as:
> A. A on both ratios.
> B. A on interest coverage but BBB on leverage.
> C. BBB on both ratios.

> [!question] Q5
> The matrix-pricing estimate of the 6-year YTM is closest to:
> A. 5.5%.
> B. 5.8%.
> C. 6.1%.

> [!question] Q6
> Using a 1.6% credit spread, the cost of debt the analyst should carry into Karst's WACC is closest to:
> A. 5.4%.
> B. 7.2%.
> C. 5.7%.

Vignette C for Q7 to Q10: Karst's equity is being costed with peer data: the public peer group has beta 1.4, D/E 0.50 and a 25% tax rate; Karst has D/E 0.25 and a 30% tax rate.
The risk-free rate is 3%, the ERP is 5%, the size premium is 4%, the industry premium is 2%, and the company-specific premium is 3%.
For country risk, the local sovereign spread is 2.5%, local equity volatility is 30%, local bond volatility is 15%, and 60% of Karst's revenue is exposed to the local country.

> [!question] Q7
> Karst's relevered beta is closest to:
> A. 1.02.
> B. 1.20.
> C. 1.65.

> [!question] Q8
> The expanded CAPM estimate of Karst's cost of equity (before country risk) is closest to:
> A. 15.1%.
> B. 16.0%.
> C. 18.2%.

> [!question] Q9
> The build-up estimate of Karst's cost of equity (before country risk) is closest to:
> A. 15.0%.
> B. 17.0%.
> C. 19.0%.

> [!question] Q10
> The country risk premium Karst's cost of equity should carry, after the Damodaran volatility adjustment and exposure weighting, is closest to:
> A. 1.5%.
> B. 3.0%.
> C. 5.0%.

> [!success]- Answer key
> Q1: B.
> $i = 1.042/1.019 - 1 = 0.02257$, or about 2.26% (Formula 10).
> Python check: `1.042/1.019-1 = 0.022571`.
> A is the real yield itself; C is the simple difference $4.2 - 1.9 = 2.3$, acceptable as an approximation but the ratio form is the precise answer and the question says "closest to" with both offered, so take the exact 2.26%.
>
> Q2: C.
> Net buybacks of 1.0% mean $\Delta S = -1.0\%$, so $-\Delta S = +1.0$.
> $\text{ERP} = \{2.4 + 0.5 + [2.26 + 2.5 + 1.0]\} - 4.2 = 8.66 - 4.2 = 4.46\%$ (Formula 9).
> Python check: `2.4+0.5+2.26+2.5+1.0-4.2 = 4.46`.
> A subtracts the buyback term (wrong sign on $\Delta S$); B omits the repricing term.
>
> Q3: A.
> Fifteen backfilled years were assembled from firms that survived to launch, so losers are missing and the measured premium is too high (V4 p.120).
> B invents a variance mechanism that does not bias the mean direction; C confuses the mean-type choice with the sample-selection problem, which no mean type cures.
>
> Q4: B.
> IC $= 14.0/2.0 = 7.0$, inside the A band (6 to 9).
> D/E $= 38/(133 - 38) = 38/95 = 0.40$, or 40%, inside the BBB band (35% to 45%).
> Python check: `14/2 = 7.0`, `38/95 = 0.40`.
> The ratios conflict, exactly the Gamma situation, so the analyst must weigh trends and judgment before picking a spread (V4 p.112).
> A misreads the D/E band; C misreads the IC band; a candidate who computes D/E off total assets ($38/133 = 29\%$) wrongly concludes A on both ratios.
>
> Q5: B.
> Increment $= (6.4 - 5.2)/4 = 0.3\%$ per year; 6-year $= 5.2 + 2(0.3) = 5.8\%$ (Formula 23).
> Python check: `5.2+2*0.3 = 5.8`.
> A steps out only one year; C steps out three.
>
> Q6: B.
> $r_d = 4.1 + 1.6 + 1.5 = 7.2\%$, and because Karst has exhausted its interest deductibility cap there is no tax adjustment, so 7.2% enters the WACC (V4 p.116, p.148).
> Python check: `4.1+1.6+1.5 = 7.2`.
> A applies the 25% tax shield the cap makes unavailable ($7.2 \times 0.75 = 5.4$); C omits the country risk premium ($4.1 + 1.6 = 5.7$).
>
> Q7: B.
> $\beta_{Asset} = 1.4 / [1 + (1 - 0.25)(0.50)] = 1.4/1.375 = 1.018$; $\beta_{Karst} = 1.018 \times [1 + (1 - 0.30)(0.25)] = 1.018 \times 1.175 = 1.196$ (Formula 21).
> Python check: `1.4/1.375 = 1.01818`, `*1.175 = 1.19636`.
> A stops at the asset beta; C relevers the peer beta without unlevering first ($1.4 \times 1.175 = 1.645$).
>
> Q8: B.
> $r_e = 3 + 1.196(5) + 4 + 3 = 15.98\%$ (Formula 16).
> Python check: `3+5.98+7 = 15.98`.
> A uses the unlevered asset beta ($3 + 5.09 + 7 = 15.1$); C uses the never-unlevered 1.645 beta ($3 + 8.23 + 7 = 18.2$).
>
> Q9: B.
> $r_e = 3 + 5 + 4 + 2 + 3 = 17.0\%$ (Formula 17), with no beta on the ERP and the industry premium included.
> Python check: `3+5+4+2+3 = 17`.
> A drops the industry premium; C beta-multiplies the ERP with the relevered beta and keeps everything else, double counting systematic risk.
>
> Q10: B.
> $\text{CRP} = 2.5\% \times (30/15) = 5.0\%$; exposure-weighted premium $= 0.60 \times 5.0\% = 3.0\%$ (Formulas 18, 19).
> Python check: `2.5*2 = 5.0`, `*0.6 = 3.0`.
> A halves instead of doubling (inverted volatility ratio times exposure); C forgets the 60% exposure weight.

## Flashcards

#flashcards/cfa-l2/04-Corporate-Issuers/lm03

Top-down factors affecting the cost of capital::Capital availability, market conditions (rates, inflation, credit spreads, ERP), legal and regulatory environment including country risk, and tax jurisdiction (V4 p.101).
Bottom-up factors affecting the cost of capital::Revenue, earnings and cash flow volatility; asset nature and liquidity; financial strength, profitability and leverage; security features (V4 p.103).
Effect of a higher marginal tax rate on the cost of debt::Larger interest tax shield, so a lower after-tax cost of debt, provided interest is deductible and taxable income exists (V4 p.102).
Callable bond yield at issuance versus option-free::Higher, because the call benefits the issuer and investors demand compensation (V4 p.106).
Putable and convertible bond yields at issuance versus option-free::Lower, because the put and conversion rights benefit investors, who pay via yield (V4 p.106).
Cumulative versus non-cumulative preferred cost::Cumulative is safer for investors, so it carries the lower required return (V4 p.107).
Cost of capital effect of multiple share classes::Shares with inferior cash flow or voting rights carry a higher cost of equity (V4 p.107).
How does collateralizing assets move the costs of debt and equity?::Lowers the secured debt's cost but can raise the cost of equity because creditors gain a prior claim in liquidation (V4 p.105).
Cost of debt method for liquid straight bonds::Use the YTM on the company's traded debt, preferring the most liquid issue (V4 p.111).
Cost of debt method for illiquid but rated debt::Matrix pricing from YTMs of similar-maturity, same-rating bonds, interpolated to the subject maturity (V4 p.111, p.143).
Cost of debt method when no rating exists::Build a synthetic rating from fundamentals such as IC and D/E, then apply that class's YTM or spread over the benchmark (V4 p.112).
Micro-problem: IC bands give B but D/E bands give BBB; what now?::The ratios conflict, so examine ratio trends and apply judgment; a synthetic rating is an input, not an answer (V4 p.112).
Why do amortizing bank loans cost less than bullet loans?::Principal repaid over the term lowers default risk relative to repaying everything at maturity (V4 p.113).
Rate implicit in the lease (RIIL) definition::The discount rate equating PV of lease payments plus PV of residual value to the asset's fair value plus the lessor's direct costs (V4 p.113).
Fallback when lessor inputs for the RIIL are unknown::Use the incremental borrowing rate on a collateralized loan of the same term, or non-traded-debt methods (V4 p.113, p.114).
Micro-problem: lease PMT 9 for 15 years, FV+costs 105, residual 10; implied rate?::About 4.08 percent; keystrokes N 15, PMT 9, PV -105, FV 10, CPT I/Y (V4 p.115).
Country risk rating components::Economic conditions, political risk, exchange rate risk, and securities market development and regulation (V4 p.115).
Sovereign risk versus country risk::Sovereign risk is default risk on government debt; country risk adds political stability, competitiveness and development factors beyond it (V4 p.115).
The four decisions of the historical ERP approach::Equity index, sample period, mean type, risk-free proxy (V4 p.117).
Key assumption behind any historical ERP::Stationarity, meaning the return-generating process of the sample still holds in the future (V4 p.117, p.120).
Arithmetic versus geometric mean for the ERP::Arithmetic matches single-period pricing models but is outlier-sensitive and overstates terminal wealth; geometric is preferred, less outlier-sensitive, matches compound terminal wealth (V4 p.118, p.119).
Short bill versus long bond as risk-free proxy::Bill is a true known return but mismatches equity duration; long bond matches duration but has coupon reinvestment risk; practice favors the long bond (V4 p.119).
Direction of survivorship bias in historical ERP::Upward, because failed companies leave the index and only winners remain, including in backfilled histories (V4 p.120).
Which two estimation choices inflate a historical ERP?::Measuring the premium over short-term bills under a normal curve, and using the arithmetic mean (V4 p.146).
Three forward-looking ERP methods::Survey-based estimates, dividend discount model estimates, macroeconomic model estimates (V4 p.121).
Survey ERP weaknesses::Sampling and response biases plus behavioral biases such as recency and confirmation (V4 p.125).
Gordon growth ERP formula::Expected index dividend yield plus expected earnings growth minus the current risk-free rate (V4 p.122).
Hidden assumption of the constant growth DDM ERP::A constant P/E, so earnings, dividends and prices grow at the same rate; expansion or contraction needs an explicit adjustment (V4 p.122).
Grinold-Kroner five factors::Dividend yield, expected repricing (change in P/E), expected inflation, real economic growth, minus the change in shares outstanding, all minus the expected risk-free rate (V4 p.123).
Sign of the shares term in Grinold-Kroner::Minus delta-S, so net buybacks (negative delta-S) add to the expected return (V4 p.123).
Micro-problem: DY 2.2, repricing 0, i 1.6, g 3.0, delta-S -0.7, rf 2.5; ERP?::2.2 + 0 + 1.6 + 3.0 + 0.7 - 2.5 = 5.0 percent (V4 p.124).
TIPS-implied inflation formula::(1 + nominal YTM) divided by (1 + TIPS YTM), minus 1, approximately the yield difference (V4 p.124).
Effect of higher expected inflation on the Grinold-Kroner ERP::Roughly none, because i and the expected risk-free rate rise together (V4 p.125).
When is Grinold-Kroner inappropriate?::Developing markets where the stock market is a small share of the economy (V4 p.125).
BYPRP formula and premium source::Cost of equity equals the long-term bond YTM plus a premium from the historical mean excess of equity over corporate bond returns (V4 p.128).
BYPRP weaknesses::The premium is relatively arbitrary, traded debt is required, and multiple issues leave the bond choice unprescribed (V4 p.129).
Fama-French three-factor components::Market ERP plus SMB (small minus big size premium) plus HML (high minus low book-to-market value premium) (V4 p.130).
Two factors the five-factor model adds::RMW, robust-minus-weak profitability, and CMA, conservative-minus-aggressive investment (V4 p.131).
Why does the market beta differ between CAPM and Fama-French?::The added factors absorb part of the return covariance, shifting the market coefficient (V4 p.132).
Micro-problem: rf 2.1, beta 0.91, ERP 5.5; CAPM cost of equity?::2.1 + 0.91 times 5.5 = 7.11 percent, and it fails the sanity check against a 7.14 percent preferred yield (V4 p.145).
Three premia added for private company equity::Size premium, industry risk premium, specific-company risk premium (V4 p.132).
Where does private-company illiquidity belong?::In the discount for lack of marketability applied to value, not as a premium in the required return (V4 p.132).
Expanded CAPM recipe::Relevered peer beta times ERP on top of the risk-free rate, plus size and specific-company premia (V4 p.133).
Build-up approach recipe::Risk-free rate plus un-beta-adjusted ERP plus size, industry and specific-company premia; implicit beta of one (V4 p.134).
When is build-up preferred over expanded CAPM?::When comparable public companies are unavailable or of questionable comparability (V4 p.134).
Why adjust a historical size premium downward for a healthy private firm?::The small-cap decile includes formerly large distressed firms whose risk a healthy private company does not share (V4 p.133).
Country spread model for ERP::Developed market ERP plus lambda times the country risk premium, lambda being the company's exposure to the local country (V4 p.135).
Damodaran CRP adjustment::Sovereign yield spread times the ratio of local equity volatility to local bond volatility (V4 p.136).
Micro-problem: spread 1.7 percent, equity vol 4, bond vol 2.5, exposure 40 percent; equity CRP?::1.7 times 4 over 2.5 = 2.72 percent, times 0.40 = 1.088 percent (V4 p.137).
Why does the global CAPM fail for emerging markets?::Low correlation with world returns produces low or negative betas, understating risk (V4 p.136).
ICAPM two factors::A global market index premium and a wealth-weighted foreign currency index premium (V4 p.136).
Unlever-relever beta procedure::Divide the peer beta by one plus (1 minus peer tax) times peer D/E, then multiply by one plus (1 minus subject tax) times subject D/E (V4 p.149).
Micro-problem: peer beta 1.25, peer tax 25 percent, peer D/E 0.3025, subject tax 20 percent, subject D/E 0.2120; subject beta?::Asset beta 1.019, relevered 1.19 (V4 p.149, p.150).
Cost of preferred equity formula::Annual stated dividend divided by current preferred price, the zero-growth DDM (V4 p.144).
Matrix pricing interpolation step::Average same-rating YTMs at each maturity, divide the YTM gap by the year gap, and step out per year to the subject maturity (V4 p.144).
When is the cost of debt not tax-adjusted?::When the interest deductibility limit is already reached, because marginal debt gets no shield (V4 p.116).

## Common mistakes

1. Deciding a cost-of-capital comparison on one factor when the exhibit gives five; the solution the graders reward cites asset liquidity, leverage, operating leverage, concentration and security features together (V4 p.108).
2. Treating a call feature as investor-friendly; calls raise the issuance yield, while puts and conversion rights lower it (V4 p.106).
3. Tax-adjusting the cost of debt when interest is not deductible or the deduction cap is exhausted (V4 p.103, p.116).
4. Using nominal earnings growth forecasts as the Grinold-Kroner $g$ alongside a separate inflation term, double counting inflation; $g$ is real growth (V4 p.124, p.153).
5. Getting the $\Delta S$ sign wrong: buybacks shrink shares, so they add to expected EPS growth through $-\Delta S$ (V4 p.123, p.124).
6. Pairing a bill-based historical ERP with a long-horizon valuation, or with today's short rate when the curve is inverted; both choices bias the required return upward (V4 p.146, p.152, p.153).
7. Calling every historical data problem an upward bias; unrepeated disasters with no offsetting booms bias the historical ERP downward (V4 p.153).
8. Forgetting to double semiannual YTMs, or interpolating matrix prices with the total yield gap instead of the per-year increment (V4 p.143, p.144).
9. Using $D_0/P_0$ instead of $D_1/P_0$ in DDM required-return problems (V4 p.139).
10. Accepting a common equity estimate below the company's traded preferred yield; the residual claim must earn more than the senior preferred (V4 p.145, p.146).
11. Mixing the peer's tax rate or D/E into the relevering step, or skipping the unlevering entirely (V4 p.149).
12. Beta-multiplying the ERP in the build-up approach, or forgetting that the expanded CAPM does apply a beta (V4 p.133, p.134).
13. Adding an illiquidity premium to a private company's required return instead of applying a discount for lack of marketability to value (V4 p.132).
14. Using the raw sovereign yield spread as an equity CRP without the equity-to-bond volatility scaling, or forgetting the exposure weight lambda (V4 p.136, p.137).
15. Copying curriculum totals without checking the arithmetic; this module's own solutions misstate the Precision build-up (24.41%, printed once as 25.41%) and WACC (21.38%, printed once as 21.13%), and Example 8's lead-in prints 3.6% for a 5.0% computation (V4 p.124, p.150).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "04-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
