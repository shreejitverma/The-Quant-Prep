---
type: cfa-lm
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
volume: 5
lm: 6
title: "Private Company Valuation"
pages: "405-464"
weight_band: "10-15%"
difficulty: 3
los_count: 9
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/equity-valuation]
---

# LM6: Private Company Valuation

Difficulty 3 of 5: nine LOS and light arithmetic, but the marks live in the details; candidates lose points by using the control premium as the DLOC instead of 1 - 1/(1 + premium), adding discounts instead of chaining them multiplicatively, growing the wrong numerator in the capitalized cash flow method, and mixing up which premia belong to the expanded CAPM versus the build-up approach.

## LOS map

- **contrast** important public and private company features for valuation purposes (V5 p.405) ^los-05-06-a
    - Examiner asks: given a company description, identify which factor (size, life-cycle stage, disclosure quality, owner-manager overlap, illiquidity, concentrated control, sale restrictions) is or is not a source of valuation difference versus a public company, and whether it is company-specific or stock-specific.
- **describe** uses of private business valuation and explain key areas of focus for financial analysts (V5 p.405) ^los-05-06-b
    - Examiner asks: match a valuation situation (VC round, buyout, IPO, impairment test, stock option grant, shareholder dispute) to transaction, compliance, or litigation, and name which of the three focus areas (normalization, discount rate, discount or premium) a given fact pattern touches.
- **explain** cash flow estimation issues related to private companies and adjustments required to estimate normalized earnings (V5 p.405) ^los-05-06-c
    - Examiner asks: adjust reported SG&A, depreciation, and taxes for above- or below-market owner compensation, non-operating assets, or missing market rent, and state the direction normalized earnings move.
- **explain** factors that require adjustment when estimating the discount rate for private companies (V5 p.405) ^los-05-06-d
    - Examiner asks: why a private target's WACC exceeds the optimal (less debt access), why the buyer's cost of capital must not be used, and what a size premium or projection-risk adjustment does to the rate.
- **compare** models used to estimate the required rate of return to private company equity (for example, the CAPM, the expanded CAPM, and the build-up approach) (V5 p.405) ^los-05-06-e
    - Examiner asks: compute all three from one input table and explain a difference between two of them, remembering that the build-up approach drops beta (implicitly one) and adds an industry risk premium.
- **explain** and evaluate the effects on private company valuations of discounts and premiums based on control and marketability (V5 p.405) ^los-05-06-f
    - Examiner asks: which discounts apply given the valuation basis and the stake being valued, then the number: DLOC = 1 - 1/(1 + control premium) and total discount = 1 - (1 - DLOC)(1 - DLOM).
- **explain** the income, market, and asset-based approaches to private company valuation and factors relevant to the selection of each approach (V5 p.405) ^los-05-06-g
    - Examiner asks: pick the approach or method (FCFF DCF, CCM, EEM, GPCM, GTM, prior transaction) that fits a company's data availability, life-cycle stage, and the interest being valued.
- **calculate** the value of a private company using income-based methods (V5 p.405) ^los-05-06-h
    - Examiner asks: a full chain from normalized EBITDA to FCFF to a CCM or DCF value to equity value after subtracting debt, or an EEM residual income capitalized at r minus g.
- **calculate** the value of a private company using market-based methods and describe the advantages and disadvantages of each method (V5 p.405) ^los-05-06-i
    - Examiner asks: apply a composite or segment multiple to sales or EBITDA, subtract debt for equity value, apply the total discount, and critique GPCM versus GTM versus prior transaction data.

## Core intuition

The machinery of this module is the same DCF and multiples toolkit used for public companies; what changes is the input quality and the question being asked (V5 p.406).
A public company hands the analyst audited statements, an observable share price, and a standard perspective: a non-controlling outsider comparing intrinsic value with the market price (V5 p.407).
A private company hands the analyst reviewed or compiled statements, no market price, an owner who is also the manager, and a buyer whose identity changes the answer (V5 p.407, p.414).
Everything in the module is a response to those four gaps.

> [!abstract] Idea 1: three adjustments convert a public-company valuation into a private-company valuation
> First, normalize the numerator: restate earnings and cash flow as they would look under efficient, arm's length ownership (V5 p.413, p.414).
> Second, adjust the denominator: build a required return that reflects size, limited debt access, and company-specific risk that beta from public comparables does not carry (V5 p.413, p.423).
> Third, adjust the result for the stock-specific position being valued: add a premium for control or subtract discounts for lack of control and lack of marketability (V5 p.413, p.429).
> The exam tests each step alone and the full chain in Examples 12 and 13 order: normalize, discount, then discount again (V5 p.447, p.452).

### What makes a private company different

Company-specific factors describe the business: earlier or later life-cycle stage, smaller size, concentrated ownership, limited disclosures, and overlap between owners and managers (V5 p.407).
Stock-specific factors describe the shares: illiquidity, concentrated control, and restrictions on sale (V5 p.407, p.408).
The distinction matters because stock-specific factors are generally negative for value, while company-specific factors can cut either way; a founder-controlled early-stage firm may have more growth potential than any public rival (V5 p.408, p.409).
Smaller size usually means a higher required return: fewer and less diversified lines of business and customers, weaker distribution, and reduced access to capital (V5 p.407).
Owner-manager overlap largely removes the principal-agent problem and allows a longer strategic horizon, which is why private equity buyers take companies private to restructure them (V5 p.408).
Concentrated control is double-edged: it enables decisive action, but it also enables above-market compensation or related-party transactions that transfer value away from minority shareholders (V5 p.408).
The result is that the spectrum of risk and return requirements for private companies is wider than for public companies, and valuation estimates diverge more, depending on the purpose of the valuation and the analyst's perspective (V5 p.409).

### Why the purpose of the valuation matters

Valuations are commissioned for transactions (VC and private equity financing, debt raises, IPOs, acquisitions and divestitures, bankruptcy, share-based compensation), for compliance (financial reporting such as impairment testing, and tax), and for litigation (damages, shareholder disputes, divorce); each practice area demands its own expertise (V5 p.410, p.411, p.412).
Different definitions of value attach to different purposes (V5 p.412).
Fair market value is the arm's length standard used for financial and tax reporting: the price between independent, willing, informed parties, which is also the benchmark that defines a related-party distortion (V5 p.412, p.415).
Fair value is the closely related financial reporting standard used when estimating the value of an equity interest for accounting purposes (V5 p.440).
Investment value is the value to a specific buyer, including any synergies that buyer alone can capture; it is why a strategic acquirer can rationally pay more than fair market value (V5 p.412, p.430).
Intrinsic value is the analyst's estimate of the value the asset ought to trade at given its expected cash flows, the quantity every DCF in this module produces (V5 p.407, p.412).
An acquirer's investment value can exceed fair market value, and an exam vignette that mixes the two standards is testing whether you notice (V5 p.412).

> [!abstract] Idea 2: the same company has several defensible values because the interest being valued differs
> A controlling, marketable interest, a controlling interest in a private firm, a non-controlling minority interest, and a non-marketable minority interest sit on a ladder of value, from a synergistic buyer's investment value at the top down through a financial buyer's control value, the public-equivalent marketable minority value, and the discounted non-marketable minority value (V5 p.429, p.430).
> Moving down the ladder is done in discrete steps: first from controlling to non-controlling (DLOC), then from marketable to non-marketable (DLOM), and the two discounts compound multiplicatively (V5 p.433).

### Normalization: restating the numerator

Private financial statements may be audited, reviewed (limited assurance), or merely compiled (no assurance); anything short of an audit usually requires adjustment (V5 p.414).
Normalized earnings in the private context means removing non-recurring, non-economic items and ongoing anomalies that prevent comparison with public entities (V5 p.414, p.415).
The recurring culprits are related-party transactions: transactions between parties sharing economic interests, recorded away from the fair market value at which independent parties would deal (V5 p.415).
Above-market owner compensation, personal-use assets (ranches, condominiums, aircraft), excess benefits, and life insurance overstate expenses and understate earnings; removing them raises normalized EBIT and, with it, the tax charge computed on adjusted income (V5 p.416, p.417).
The reverse also happens: an owner who underpays herself, or who takes value as dividends instead of salary, leaves reported expenses understated, and the analyst must insert a market compensation charge that lowers normalized earnings (V5 p.417, p.421).
Real estate deserves its own step: if the company uses owned property, the analyst separates it, removes its revenues and expenses, charges a market rent to operations, and treats the property as a non-operating asset, because business operations and real estate carry different risk and growth (V5 p.418).
If the company uses property owned by a related party rent-free, a market rental expense must be inserted even though no cash leaves (V5 p.418, p.421).
Cash flow estimation then inherits public-company machinery, FCFF for the enterprise and FCFE for equity, but with two private twists: managers who both know more and may be biased (optimistic for impairment testing, pessimistic for option grants), and genuinely uncertain futures (IPO, sale, continued operation, failure) that call for scenario analysis and probability-weighted values (V5 p.419, p.421).

### The denominator: required returns without a market price

The CAPM assumes a diversified marginal investor and a market beta; private company owners hold concentrated stakes and private shares have no return history, so both assumptions fail (V5 p.424).
Analysts respond in two ways: bolt premia onto the CAPM, or abandon beta altogether (V5 p.424).
The expanded CAPM keeps beta (estimated from guideline public companies, unlevered and relevered to the subject's capital structure) and adds a small-stock premium and a company-specific risk premium (V5 p.424, p.440).
The build-up approach starts from the risk-free rate and adds the whole equity risk premium unscaled by beta (implicitly beta = 1), a small-stock premium, an industry risk premium, and a company-specific premium; it is the tool of choice when no credible comparables exist (V5 p.424).
Four further factors push private discount rates around: size premia (with the caveat that the smallest-cap public data may reflect distress irrelevant to the subject), less debt access which forces more equity into the WACC and raises it, the rule that an acquisition must be discounted at the target's rate rather than the buyer's lower rate, and judgmental additions for projection risk (V5 p.423).
The acquirer point is subtle and examinable: if the buyer discounts target cash flows at its own lower cost of capital, or prices in the optimal capital structure it will install later, it hands the seller value the buyer itself creates (V5 p.423, p.429).

> [!abstract] Idea 3: DLOC is derived from a control premium, and discounts chain multiplicatively
> Control premium data come from acquisitions of public companies, so the discount for lack of control is the premium run backwards: DLOC = 1 - 1/(1 + control premium), which is always smaller than the premium itself (V5 p.431).
> A 30% control premium gives a 23.1% DLOC, not 30%, and the total discount with a 20% DLOM is 1 - 0.769 x 0.80 = 38.5%, not 50% and not 43.1% (V5 p.434).
> Whether the DLOC applies at all depends on the basis of the value being discounted: a DCF built on control cash flows and an optimal capital structure is a control value and needs the DLOC for a minority stake, while a value built on non-control cash flows already reflects the lack of control (V5 p.431, p.433).

### Discounts and premiums in practice

The ladder from Exhibit 6 runs: strategic control value (synergistic premium), financial control value (control premium without synergies), marketable minority value (the public-comparable level), and non-marketable minority value after the DLOM (V5 p.429, p.430).
A strategic buyer pays for synergies it can execute; a financial buyer pays for control without synergies (V5 p.430).
DLOM evidence comes from restricted stock transactions, pre-IPO share sales, and option pricing: price an at-the-money put struck at the forward price on the closest public comparable, and the put premium as a percentage of the stock price estimates the DLOM (V5 p.432).
The put approach lets the analyst dial in perceived risk through volatility, but a put protects price without providing liquidity and still lets the holder keep upside, so it is an imperfect model of non-marketability (V5 p.432, p.433).
Discount sizes are fact-specific: a company headed for an IPO or strategic sale merits modest discounts, while a stake with no dividends and no liquidity event in sight merits large ones (V5 p.430).
Other discounts exist for key person risk, heterogeneous portfolios, and non-voting shares (V5 p.433).

### Choosing among income, market, and asset-based approaches

The income approach is public-style DCF plus two special cases: the capitalized cash flow method, a single growing perpetuity for stable firms with no projections and thin market evidence, and the excess earnings method, residual income for firms whose value sits in intangibles (V5 p.434, p.436, p.438).
The market approach prices the subject against guideline public companies (GPCM), against acquisitions of whole companies (GTM), or against prior transactions in the subject's own stock; because it rests on actual market evidence it is the most used and, to many, conceptually preferable (V5 p.440).
The asset-based approach values assets minus liabilities and suits holding structures and liquidations rather than going concerns with intangible value (V5 p.435, p.411).
Selection is driven by data availability, the analyst's confidence in it, and the company's life-cycle stage and industry (V5 p.434).
EV-based multiples dominate price multiples in private work because they accommodate capital structure changes over the valuation period, and betas and multiples imported from public comparables must be unlevered at the comparable's debt and tax profile and relevered at the subject's (V5 p.440).
When the subject spans several businesses, composite multiples are built by weighting segment multiples by sales or EBITDA shares, with care where a segment's fundamental is negative (V5 p.442, p.443).
The transaction evidence behind GTM needs screening for synergies in the price, contingent and non-cash consideration, stale transaction dates, and differences in size, country, tax status, and leverage (V5 p.444, p.445).

## Formulas and derivations

**WACC** (V5 p.422, p.423)
$$
r_{WACC} = w_d r_d + w_e r_e, \qquad r_d = r(1 - t)
$$
^f-05-06-1

- $w_d, w_e$: debt and equity weights as a percentage of total market value of capital; $r_d$: after-tax cost of debt from pre-tax rate $r$ and tax rate $t$; $r_e$: cost of equity (V5 p.422, p.423).
- For a sale, use the optimal capital structure a buyer would install, not the actual one; a private firm with too little debt has a WACC above the optimal level (V5 p.426, p.423).
- FLI: current structure $0.02 \times 6.225\% + 0.98 \times 13\% = 12.9\%$; optimal $0.10 \times 6.225\% + 0.90 \times 13\% = 12.3\%$ (V5 p.427).

**CAPM cost of equity** (V5 p.423)
$$
r_e = r_f + \beta (r_m - r_f)
$$
^f-05-06-2

- $r_f$: risk-free rate; $r_m - r_f$: equity risk premium; $\beta$: systematic risk versus the market (V5 p.423).
- Often inappropriate for private firms: owners are undiversified, so beta understates the risk they bear, and small firms with no prospect of going public may not be comparable to listed peers (V5 p.424).
- FLI: $3.8\% + 1.1 \times 5\% = 9.3\%$ (V5 p.425).

**Expanded CAPM** (V5 p.424)
$$
r_e = r_f + \beta (r_m - r_f) + P_{size} + P_{company}
$$
^f-05-06-3

- $P_{size}$: small-stock premium; $P_{company}$: company-specific risk premium, a subjective estimate from industry and company analysis against guideline public companies (V5 p.424).
- Keeps beta from comparables, so the equity risk premium is scaled by beta before the premia are added (V5 p.424).
- FLI: $3.8 + 5.5 + 3.0 + 1.0 = 13.3\%$, where $5.5\% = 1.1 \times 5\%$ (V5 p.426).

**Build-up approach** (V5 p.424)
$$
r_e = r_f + ERP + P_{size} + P_{industry} + P_{company}
$$
^f-05-06-4

- No beta anywhere: the full equity risk premium enters unscaled, implicitly assuming $\beta = 1$, and an industry risk premium (or discount) substitutes for the industry tilt beta would have carried (V5 p.424).
- Used when comparable public companies are unavailable or of questionable comparability (V5 p.424).
- FLI: $3.8 + 5.0 + 3.0 + 0.0 + 1.0 = 12.8\%$; the 0.5% gap to the expanded CAPM is exactly the missing $(\beta - 1) \times ERP = 0.1 \times 5\%$ (V5 p.426, p.429).

**Scenario (decision-tree) valuation** (V5 p.420)
$$
V_0 = \frac{\sum_i p_i \, V_{i,t=n}}{(1 + WACC)^n}, \qquad V_{i,t=n} = \frac{FCFF_{n+1,i}}{WACC - g_i}
$$
^f-05-06-5

- $p_i$: path probability of scenario $i$ (multiply probabilities along the tree); $V_{i,t=n}$: constant-growth firm value at the resolution date under scenario $i$; failure scenarios contribute zero (V5 p.420).
- Nano Beta: $0.32 \times 2{,}100 + 0.32 \times 392.3 = 797.5$ million at $t = 2$, then $797.5/1.15^2 = 603.1$ million today (V5 p.420).
- The scenarios can differ in growth as well as level, which is why broad applicability is worth more than four times limited applicability (V5 p.421).

**Discount for lack of control** (V5 p.431)
$$
DLOC = 1 - \frac{1}{1 + \text{Control premium}}
$$
^f-05-06-6

- Control premium: the premium paid over the marketable minority value in acquisitions of public companies; strategic-buyer premiums exceed financial-buyer premiums because of synergies (V5 p.431, p.444).
- Derivation: if control value $= (1 + CP) \times$ minority value, then minority value $=$ control value $/(1 + CP)$, so the discount off control value is $1 - 1/(1 + CP)$ (V5 p.431).
- The DLOC is always smaller than the premium: a 15% premium gives $1 - 1/1.15 = 13.0\%$, a 30% premium gives 23.1% (V5 p.431, p.434).

> [!tip] Calculator
> `1.30 1/x +/- + 1 =` gives 0.2308; or `1 - (1 ÷ 1.30) =` on the BA II Plus: `1.30 1/x = 0.7692`, `1 - 0.7692 = 0.2308`.

**DLOM from an at-the-money-forward put** (V5 p.432)
$$
DLOM = \frac{P_{put}}{S_0}, \qquad K = S_0 e^{rT}
$$
^f-05-06-7

- $P_{put}$: Black-Scholes premium of a put on the closest public comparable, struck at the forward price $K$; $S_0$: current stock price; $T$: assumed horizon to liquidity (V5 p.432).
- Shipline: $K = 50 e^{0.05 \times 0.5} = 51.27$, premium 8.40, $DLOM = 8.40/50 = 16.8\%$ (V5 p.432).
- Weaknesses: a put protects price, not liquidity, and leaves the upside intact, so it does not exactly model non-marketability; the strength is that volatility directly expresses perceived risk (V5 p.432, p.433).

**Total discount for control and marketability** (V5 p.433)
$$
\text{Total discount} = 1 - (1 - DLOC)(1 - DLOM)
$$
^f-05-06-8

- Discounts apply in sequence, controlling to non-controlling and then marketable to non-marketable, so they compound instead of adding (V5 p.433).
- Everfloat: $1 - 0.87 \times 0.832 = 27.6\%$; additive would say 29.8% and is wrong (V5 p.433).
- Apply the DLOC only when the base value is on a control basis; a DCF using non-control cash flows or a non-optimal capital structure already reflects lack of control (V5 p.431).

**FCFF valuation with terminal value** (V5 p.435, p.447)
$$
IV_t = \sum_{i=1}^{n} \frac{FCFF_{t+i}}{(1 + WACC)^i} + \frac{E(S_{t+n})}{(1 + WACC)^n}, \qquad E(S_{t+n}) = \frac{FCFF_{t+n+1}}{WACC - g}
$$
^f-05-06-9

- $E(S_{t+n})$: terminal firm value, from a capitalized cash flow, an excess earnings capitalization, or a market multiple (V5 p.435).
- FCFF suits controlling investors with influence over distribution and debt policy; subtract the market value of debt to reach equity value (V5 p.435, p.436).
- The terminal numerator is the year $n$ cash flow grown one year at the terminal growth rate, not at the stage-one rate (V5 p.448).

**Top-down FCFF** (V5 p.412, p.447)
$$
FCFF = EBITDA(1 - t) + Dep \times t - \Delta \text{LT assets} - \Delta \text{Working capital}
$$
^f-05-06-10

- Algebraically identical to $EBIT(1 - t) + Dep - \Delta \text{LT assets} - \Delta WC$ because $EBITDA(1-t) + Dep \times t = (EBIT + Dep)(1-t) + Dep \times t = EBIT(1-t) + Dep$ (V5 p.412).
- $\Delta$LT assets is capital expenditure (net of any depreciation already added back in the variant used); work from normalized, not reported, figures (V5 p.447, p.448).
- FLI: $16.3m \times 0.83 + 0.9m \times 0.17 - 1.2m - 0.5m = 11.982$ million (V5 p.448).

**Capitalized cash flow method, FCFF basis** (V5 p.436)
$$
\text{Firm value}_t = \frac{FCFF_{t+1}}{WACC - g} = \frac{FCFF_t (1 + g)}{WACC - g}
$$
^f-05-06-11

- A single growing perpetuity: appropriate when no projections exist and market pricing evidence is limited; also the standard terminal value engine (V5 p.436).
- Subtract the market value of debt for equity value; face value is acceptable only when debt is small and operations stable (V5 p.436, p.437).
- Same convergence condition as the Gordon model: requires $WACC > g$ and a constant capital structure (V5 p.436).

> [!tip] Calculator
> LPE practice problem: `600,000 × 1.04 = 624,000`, `0.08 - 0.04 = 0.04`, `624,000 ÷ 0.04 = 15,600,000`.
> The most common wrong key sequence skips the `× 1.04`.

**Reinvestment rate implied by the CCM** (V5 p.436)
$$
RIR = \frac{g}{WACC}
$$
^f-05-06-12

- The fraction of after-tax operating income plowed into working capital and long-term assets to sustain growth $g$; the perpetuity assumes value-neutral reinvestment at the WACC, so $g = RIR \times WACC$ (V5 p.436).
- Vinuvia: $5\%/15\% = 33.33\%$ (V5 p.445).

**CCM from projected EBIT** (V5 p.436)
$$
\text{Firm value}_t = \frac{EBIT_{t+1}(1 - t)(1 - RIR)}{WACC - g}
$$
^f-05-06-13

- Substitutes $FCFF_{t+1} = EBIT_{t+1}(1 - t)(1 - RIR)$: after-tax operating income less the reinvestment needed for growth (V5 p.436).
- Ties Formula 11 and Formula 12 together; useful when only an EBIT forecast exists (V5 p.436).

**Capitalized FCFE** (V5 p.436)
$$
IV_t = \frac{FCFE_{t+1}}{r_e - g}
$$
^f-05-06-14

- Values equity directly at the cost of equity; $r_e - g$ is called the capitalization rate (V5 p.436).
- No debt subtraction afterwards, because FCFE is already after payments to debtholders (V5 p.436).

**Excess earnings (residual income)** (V5 p.438)
$$
RI_t = \text{Normalized income} - (WC \times r_{WC}) - (FA \times r_{FA})
$$
^f-05-06-15

- $WC$: fair market value of working capital, the lowest-risk asset with the lowest required return $r_{WC}$; $FA$: fixed assets at fair market value with higher $r_{FA}$; what remains is the income earned by intangibles (V5 p.438).
- Conceptually the residual income model with the capital charge split by asset class (V5 p.434, p.438).
- Digigraf: $120{,}000 - 200{,}000 \times 5\% - 800{,}000 \times 11\% = 22{,}000$ (V5 p.439).

**EEM residual value and firm value** (V5 p.438)
$$
RV_t = \frac{RI_t (1 + g)}{r_{RI} - g}, \qquad \text{Firm value}_t = FMV_{\text{tangible}} + RV_t
$$
^f-05-06-16

- $r_{RI}$: the highest of the three rates, because intangibles are illiquid, firm-specific, and risky; $g$: residual income growth (V5 p.438).
- Digigraf: $22{,}000 \times 1.03/(0.12 - 0.03) = 251{,}778$; firm value $200{,}000 + 800{,}000 + 251{,}778 = 1{,}251{,}778$ (V5 p.439).
- Rarely used for whole businesses (and then only small ones) because three subjective discount rates are needed, but the residual income concept is standard for intangible valuations in financial reporting (V5 p.439).

**Unlevering a guideline company beta** (V5 p.440)
$$
\beta_{unlevered} = \frac{\beta_{levered}}{1 + (1 - t)\dfrac{Debt}{Equity}}
$$
^f-05-06-17

- $t$ and $Debt/Equity$ are the public comparable's; unlevering strips the comparable's financial leverage out of its observed equity beta (V5 p.440).
- Quik Chip: $1.21/(1 + 0.784 \times 0.50) = 0.8693$ (V5 p.442).

**Relevering at the subject's capital structure** (V5 p.441)
$$
\beta^*_{levered} = \beta_{unlevered}\left[1 + (1 - t^*)\left(\frac{Debt}{Equity}\right)^{*}\right]
$$
^f-05-06-18

- $t^*$ and $(Debt/Equity)^*$ are the private subject's; because private firms usually carry less debt than public comparables, the relevered beta lands below the comparables' beta (V5 p.441, p.463).
- Quik Chip: $0.8693 \times (1 + 0.82 \times 0.25) = 1.047$; the curriculum's printed 0.8693 on this line is a typo, the arithmetic gives 1.047 (V5 p.442).

**Composite multiple across business lines** (V5 p.443, p.452)
$$
EV_t = \sum_{i=1}^{n} w_i \left(\frac{EV_i}{Sales_i}\right)(\text{Sales})_i, \qquad w_i = \frac{\text{Business line sales}}{\text{Total sales}}
$$
^f-05-06-19

- Weight each segment's peer multiple by the subject's segment share of the fundamental (sales weights for EV/Sales, EBITDA weights for EV/EBITDA); equivalently, apply each segment multiple to that segment's fundamental and sum (V5 p.443, p.453).
- Everfloat: EV/Sales $= 0.7 \times 2.8 + 0.25 \times 1.1 + 0.05 \times 8.0 = 2.635$; EV/EBITDA $= 0.75 \times 8.2 + 0.30 \times 8.1 - 0.05 \times 20.0 = 7.58$ (V5 p.443).
- A negative-EBITDA segment drags the composite down and implies negative segment value; the fix is to price that segment on a sales multiple instead (V5 p.443, p.454).

## Worked examples

### Knowledge check: Thunder, Sun and Moon, Privacy Group (V5 p.409, p.410)

Part 1: Thunder Corporation, a small private household products company, is owned by non-employee shareholders and run by professional management with no public debt access.
Least likely source of valuation difference: principal-agent issues (B), because ownership and control are separated exactly as at a public company; size (C) and debt market access (A) are genuine differences (V5 p.409).

Part 2: Sun and Moon Ltd. has five owner-manager partners, two with 35% stakes and three with 10%.
Per-share value can differ across partners because of concentrated control (C): the two 35% partners can form a 70% control bloc by coordinating with one other person, while a 10% partner needs at least two others; stake size alone is not concentrated ownership (A), and every partner manages, so owner-manager overlap (B) does not discriminate (V5 p.409).

Part 3: Privacy Group (private) and PT Corp. (public) are otherwise identical family-controlled firms.
The valuation difference comes from illiquidity of shares (B): both have family control and minimal agency problems, but only PT's shareholders can sell into a liquid market (V5 p.410). ^ex-05-06-1

### Knowledge check: practice areas and areas of focus (V5 p.413, p.414)

Part 1: share-based payments to employees are valued in the transaction practice area (A), because issuing securities to employees is a transaction between the company and its employees (V5 p.413).
Part 2: an analyst moving from public to private coverage must adjust both cash flows and the discount rate (C): normalization fixes the numerator, discount rate adjustments fix the denominator (V5 p.414).
Part 3: a senior executive's personal use of company assets flows through the income statement, so it primarily affects the numerator of the valuation (B) (V5 p.414). ^ex-05-06-2

### Example 1: normalizing earnings for Fyt for Life (V5 p.416, p.417)

Setup: Xin, sole shareholder and CEO, was paid SGD 1.5 million against a market rate of 500,000; ranch and condominium (non-operating) cost 300,000 of SG&A and 100,000 of depreciation; reported revenues 50.0m, COGS 30.0m, SG&A 5.0m, D&A 1.0m, tax 17%.

Adjustments: cut SG&A by 1,000,000 (excess compensation) and 300,000 (non-operating property costs); cut D&A by 100,000 (property depreciation).
Normalized statement: SG&A $5.0 - 1.3 = 3.7$m; EBITDA $20.0 - 3.7 = 16.3$m; D&A 0.9m; EBIT 15.4m; taxes $15.4 \times 0.17 = 2.618$m; operating income after taxes $15.4 - 2.618 = 12.782$m, up from the reported 11.62m (V5 p.417).
Note the tax charge is recomputed on adjusted income: normalization raises taxes as well as earnings (V5 p.417).
Python check: `20-1.3-0.9 = 15.4`, `15.4*0.83 = 12.782`. ^ex-05-06-3

### Example 2: Chandra Consolidated and the use of real estate (V5 p.418, p.419)

Setup: Chandra Holdings (real estate) lets Chandra Shops (luxury retail) use ground-floor space with no rental agreement and no payments.

Part 1: insert a market rental charge for comparable retail space as an expense on Shops' income statement and as rental income on Holdings' income statement; without it, Shops' true opportunity cost of space is understated (V5 p.418).
Part 2: normalization lowers Shops' earnings and its valuation and raises Holdings' earnings and valuation; a minority-stake buyer in Shops would otherwise overpay for earnings subsidized by free rent (V5 p.419). ^ex-05-06-4

### Example 3: scenario analysis to value Nano Beta (V5 p.419 to p.421)

Setup: preliminary EMA approval in one year (80%), then final approval with broad applicability (40%) or limited applicability (40%) or failure (20%); WACC 15%; broad: FCFF 200m growing 5%; limited: FCFF 50m growing 2%; failure worth zero.

Scenario values at $t = 2$ (Formula 5): broad $= 200 \times 1.05/(0.15 - 0.05) = 2{,}100$m; limited $= 50 \times 1.02/(0.15 - 0.02) = 392.31$m.
Path probabilities: $0.80 \times 0.40 = 0.32$ each.
Future firm value $= 0.32 \times 2{,}100 + 0.32 \times 392.31 = 797.54$m.
$V_0 = 797.54/1.15^2 = 603.05$m (V5 p.420).
Python check: `(0.32*2100+0.32*392.3077)/1.15**2 = 603.054`. ^ex-05-06-5

### Knowledge check: FLI dividends, related-party building, Nano Beta reweighted (V5 p.421, p.422)

Part 1: if Xin takes zero salary and a 1.5m dividend instead, reported expenses omit CEO pay entirely; normalization must insert the 500,000 market compensation, so normalized earnings fall (B); dividends are a distribution, not an expense, so they never substitute for compensation (A is wrong) (V5 p.421).
Part 2: if FLI manufactures rent-free in a building owned by Xin's family, insert a market rental expense, reducing normalized income (C); ignoring it (A) or fixing only the balance sheet (B) leaves operating costs understated (V5 p.421).
Part 3: reweight Nano Beta to 60% preliminary approval with 60%/20% broad/limited splits: broad path $0.6 \times 0.6 = 0.36$, limited $0.6 \times 0.2 = 0.12$.
Future value $= 0.36 \times 2{,}100 + 0.12 \times 392.31 = 803.08$m; $V_0 = 803.08/1.3225 = 607.24$m, an increase of EUR 4.2 million (B) (V5 p.422).
Python check: `(0.36*2100+0.12*392.3077)/1.15**2 = 607.242`, `607.242-603.054 = 4.188`. ^ex-05-06-6

### Example 4: calculating FLI's discount rate (V5 p.424 to p.428)

Setup: $r_f = 3.8\%$, ERP 5%, beta 1.1 from comparables, small-stock premium 3%, company-specific premium 1%, industry premium 0 (build-up only), pre-tax debt cost 7.5%, tax 17%, debt/total capital: comparables 20%, optimal 10%, actual 2%.

Part 1, CAPM (Formula 2): $3.8 + 1.1 \times 5 = 9.3\%$.
Part 2, expanded CAPM (Formula 3): $3.8 + 5.5 + 3.0 + 1.0 = 13.3\%$.
Part 3, build-up (Formula 4): $3.8 + 5.0 + 3.0 + 0.0 + 1.0 = 12.8\%$; no beta scaling, and with beta near one any industry adjustment would be small.
Part 4, weights: for a sale, use the optimal structure, because an acquirer would establish it; but FLI's optimal debt weight (10%) sits below the comparables' 20% because small size raises operating risk and debt cost and cuts debt access (V5 p.426).
Part 5, WACC at actual structure with $r_e = 13\%$: $r_d = 7.5 \times 0.83 = 6.225\%$; $0.02 \times 6.225 + 0.98 \times 13 = 12.86 \approx 12.9\%$.
Part 6, WACC at optimal structure: $0.10 \times 6.225 + 0.90 \times 13 = 0.62 + 11.70 = 12.3\%$ (V5 p.427).
Python check: `0.02*6.225+0.98*13 = 12.86`, `0.10*6.225+0.90*13 = 12.32`. ^ex-05-06-7

### Knowledge check: FLI cost of capital queries (V5 p.428, p.429)

Part 1: the expanded CAPM (13.3%) exceeds the CAPM (9.3%) mainly because of the 3% size premium (A); the company-specific premium adds only 1%, and industry premia appear in neither model (V5 p.428).
Part 2: the build-up result is lower than the expanded CAPM despite more premia because the industry premium was zero and the build-up approach does not scale the ERP by beta; with beta 1.1 the expanded CAPM carries an extra $0.1 \times 5\% = 0.5\%$ (C) (V5 p.428, p.429).
Part 3: pricing FLI off the optimal-structure WACC (12.3%) rather than the actual (12.9%) raises the price and transfers to the seller value the buyer itself will create by fixing the capital structure after the deal (B); FLI has too little debt, not too much, and projection risk has nothing to do with it (V5 p.429). ^ex-05-06-8

### Example 5: Everfloat control premium (V5 p.431)

Setup: unadjusted (control-basis) value GBP 1.65 billion; control premium 15%; value a non-controlling minority interest.

$DLOC = 1 - 1/1.15 = 0.130$ (Formula 6).
Adjusted value $= 1.65 \times (1 - 0.13) = 1.4355$ billion (V5 p.431).
Python check: `1-1/1.15 = 0.13043`, `1.65*0.87 = 1.4355`; with the unrounded DLOC the value is 1.4348 billion, the curriculum rounds the DLOC to 13.0% first. ^ex-05-06-9

### Example 6: Everfloat DLOM from a put option (V5 p.432)

Setup: closest comparable Shipline PLC at GBP 50, no dividends, six-month horizon, risk-free 5%, implied volatility 60%.

Strike at the six-month forward: $K = 50 e^{0.05 \times 0.5} = 51.27$ (Formula 7).
Black-Scholes put premium: 8.40.
$DLOM = 8.40/50 = 16.8\%$, dividing by the spot price, not the strike (V5 p.432).
Python check: `50*exp(0.025) = 51.266`, `8.40/50 = 0.168`. ^ex-05-06-10

### Example 7: Everfloat total discount (V5 p.433)

With DLOC 13% and DLOM 16.8% (Formula 8):
Total discount $= 1 - (1 - 0.13)(1 - 0.168) = 1 - 0.87 \times 0.832 = 0.276$.
The discounts chain multiplicatively because they apply in sequence: control to non-control, then marketable to non-marketable (V5 p.433).
Python check: `1-0.87*0.832 = 0.27616`. ^ex-05-06-11

### Knowledge check: Starbeam discounts (V5 p.433, p.434)

Part 1: Starbeam's recent valuation was done on its current basis: 100% management-owned (control) and private (already non-marketable), so it embeds a control premium and a DLOM; valuing a proposed non-controlling stake therefore needs only a DLOC (B); adding another DLOM (C) would double count (V5 p.433).
Part 2: a financial buyer of a controlling stake must still offer a financial control premium (A) to entice management to give up control; with no synergies available there is no basis for a synergistic premium (V5 p.434).
Part 3: control premium 30%, DLOM 20%: $DLOC = 1 - 1/1.30 = 0.231$; total discount $= 1 - 0.769 \times 0.80 = 0.385$ (C).
Distractor A (44%) treats the 30% premium as the DLOC and compounds; distractor B (43.1%) is another premium-as-discount arithmetic; both die on Formula 6 (V5 p.434).
Python check: `1-1/1.3 = 0.23077`, `1-(1-0.23077)*0.8 = 0.38462`. ^ex-05-06-12

### Example 8: Vinuvia Limitada's capitalized cash flow (V5 p.437)

Setup: FCFF 15.0m (BRL), FCFE 14.5m; $r_e = 15\%$, pre-tax debt 10%, tax 34%; capital 90% equity, 10% debt; assets 50m; FCFF growth 5%.

Part 1: $WACC = 0.1 \times 10\% \times 0.66 + 0.9 \times 15\% = 0.66 + 13.5 = 14.16\%$.
$FCFF_{t+1} = 15.0 \times 1.05 = 15.75$m.
Firm value $= 15.75/(0.1416 - 0.05) = 171.94$m (Formula 11).
Equity value $= 171.94 - 5.0 = 166.94$m, using book debt ($0.1 \times 50$m) because debt is small and operations stable (V5 p.437).
Part 2 with $g = 2\%$: $FCFF_{t+1} = 15.0 \times 1.02 = 15.3$m; firm value $= 15.3/(0.1416 - 0.02) = 125.82$m; equity $= 120.82$m.
The printed fraction shows 15,750,000 in the numerator, but the stated answer BRL 120,822,368 only follows from the correct numerator $15.0 \times 1.02 = 15.3$m and is the equity value after subtracting the 5m of debt; a 3 point growth cut removes 27.6% of equity value (V5 p.437).
Python check: `15.75/0.0916 = 171.943`, `15.3/0.1216 = 125.822`, `(166.943-120.822)/166.943 = 0.276`. ^ex-05-06-13

### Example 9: Digigraf EEM (V5 p.439)

Setup: working capital 200,000, fixed assets 800,000 (both near fair value), normalized earnings 120,000 (EUR); $r_{WC} = 5\%$, $r_{FA} = 11\%$, $r_{RI} = 12\%$, $g = 3\%$.

$RI = 120{,}000 - 200{,}000 \times 0.05 - 800{,}000 \times 0.11 = 120{,}000 - 10{,}000 - 88{,}000 = 22{,}000$ (Formula 15).
$RV = 22{,}000 \times 1.03/(0.12 - 0.03) = 22{,}660/0.09 = 251{,}778$ (Formula 16).
Firm value $= 200{,}000 + 800{,}000 + 251{,}778 = 1{,}251{,}778$.
The residual income is grown one year at 3% before capitalizing because 22,000 is the most recent year's figure (V5 p.439).
Python check: `22000*1.03/0.09 = 251777.8`. ^ex-05-06-14

### Example 10: Quik Chip guideline public companies (V5 p.441, p.442)

Setup: nine quick-service restaurant comparables; mean beta 1.21, mean debt/equity 50.0%, mean tax 21.6%; mean multiples P/E 22.6, EV/EBITDA 12.1, EV/EBIT 17.3, EV/Sales 2.0; Quik Chip has $D/E = 25\%$, tax 18%.

Part 1: unlever (Formula 17): $\beta_u = 1.21/[1 + (1 - 0.216) \times 0.50] = 1.21/1.392 = 0.8693$.
Relever (Formula 18): $\beta^* = 0.8693 \times [1 + (1 - 0.18) \times 0.25] = 0.8693 \times 1.205 = 1.047$.
The curriculum prints 0.8693 as the relevered result, which is a typo; the relevered beta is 1.047, below the comparables' 1.21 because Quik Chip carries less debt (V5 p.442).
Part 2: with sales 250m and EBIT 35m (EUR): $EV_{EV/EBIT} = 17.3 \times 35 = 605.5$m; $EV_{EV/Sales} = 2.0 \times 250 = 500$m.
The EBIT-based estimate is higher because Quik Chip's EBIT margin (14%) beats the peers' implied 11.6% ($= 2.0/17.3$), and a sales multiple ignores that superior profitability (V5 p.442).
Python check: `1.21/(1+0.784*0.5) = 0.86925`, `0.86925*1.205 = 1.04745`, `2.0/17.3 = 0.1156`. ^ex-05-06-15

### Example 11: Everfloat composite multiples (V5 p.442, p.443)

Setup: revenue 700/250/50 (GBP m), EBITDA 187.5/75/-12.5 across Marine Navigation, Logistics Services, Energy Solutions; segment peer multiples EV/Sales 2.8/1.1/8.0, EV/EBITDA 8.2/8.1/20.0.

Part 1, sales-weighted EV/Sales (Formula 19): $0.70 \times 2.8 + 0.25 \times 1.1 + 0.05 \times 8.0 = 1.96 + 0.275 + 0.40 = 2.635$.
Part 2, EBITDA-weighted EV/EBITDA: $0.75 \times 8.2 + 0.30 \times 8.1 + (-0.05) \times 20.0 = 6.15 + 2.43 - 1.00 = 7.58$.
Energy Solutions' negative EBITDA enters with a negative weight; the stated alternative is to value that segment on a sales multiple and the others on EBITDA (V5 p.443).
Python check: `0.7*2.8+0.25*1.1+0.05*8 = 2.635`, `0.75*8.2+0.3*8.1-0.05*20 = 7.58`. ^ex-05-06-16

### Knowledge check: Vinuvia RIR, Digigraf corrected, guideline choice (V5 p.445, p.446)

Part 1: with a 5% perpetual growth rate and 15% WACC as stated, the CCM's implied reinvestment rate is $g/WACC = 5/15 = 33.33\%$ (A) (Formula 12) (V5 p.445).
Part 2: rerun Digigraf with $r_{WC} = 4\%$, $r_{FA} = 10\%$, $r_{RI} = 11\%$: $RI = 120{,}000 - 8{,}000 - 80{,}000 = 32{,}000$ (the solution's "EUR 32,000,000" is a typo for 32,000); $RV = 32{,}000 \times 1.03/(0.11 - 0.03) = 412{,}000$; value $= 200{,}000 + 800{,}000 + 412{,}000 = 1{,}412{,}000$ (C) (V5 p.446).
Part 3: the least useful screening characteristic for guideline public companies is a similar debt ratio (A): leverage differences are handled by unlevering and relevering, while similar growth prospects and risk are exactly what comparability means (V5 p.446).
Python check: `32000*1.03/0.08 = 412000`. ^ex-05-06-17

### Example 12: FLI valuation using the income approach (V5 p.447 to p.449)

Step 1: Khan blends the expanded CAPM (13.3%) and build-up (12.8%) into $r_e = 13.0\%$, then averages debt-ratio assumptions for a WACC of 12.55% (the summary table's 12.8% for the actual-structure WACC against Example 4's 12.9% is a rounding inconsistency in the curriculum) (V5 p.447, p.448).
Step 2: base FCFF from normalized figures (Formula 10): $16{,}300{,}000 \times 0.83 + 900{,}000 \times 0.17 - 1{,}200{,}000 - 500{,}000 = 11{,}982{,}000$ SGD; note the table's first "EBIT 16,300,000" row is the EBITDA line mislabeled (V5 p.448).
Step 3: five-year FCFF paths at 2%/5%/8% growth, terminal value at 3% perpetual growth off year 5.
Downside: $FCFF_5 = 11.982 \times 1.02^5 = 13.229$m; $TV = 13.229 \times 1.03/(0.1255 - 0.03) = 13.626/0.0955 = 142.680$m; the intermediate 141,295,059 printed first grows the terminal numerator at 2% instead of 3% and is superseded by the correct 142,680,302 (V5 p.448).
Base: $FCFF_5 = 15.292$m, $TV = 164.934$m; optimistic: $FCFF_5 = 17.605$m, $TV = 189.881$m.
Discounting flows and terminal value at 12.55%: EV 124.03/140.20/158.16m; equity after subtracting 2.5m market value of debt: 121.53/137.70/155.66m (V5 p.449).
Step 4: an 18% DLOM (option-based) and no DLOC, because Xin's controlling-interest value was not seen as embedding a control premium: equity value $\times 0.82 = 99.65/112.92/127.64$m (V5 p.449).
Python check: `11.982*1.02**5 = 13.2291`, `13.2291*1.03/0.0955 = 142.680`, NPV at 12.55% downside `= 124.028`, `121.528*0.82 = 99.653`. ^ex-05-06-18

### Knowledge check: Macro Associates (V5 p.450, p.451)

Part 1: the selling partner's above-market compensation overstates costs, so normalization lowers costs and raises EBIT above the reviewed statements (B) (V5 p.450).
Part 2: the build-up method suits the missing-comparables problem because it adds a standard equity risk premium without any beta adjustment (A); it assumes beta of one, not zero, and the company-specific premium appears in the expanded CAPM too, so it cannot be the differentiator (V5 p.450, p.451).
Part 3: the CCM's advantage over the EEM is one discount rate (the WACC) instead of three separate rates for working capital, fixed assets, and residual income (C); neither method needs public comparables, and intangible-asset valuation is the EEM's strength, not the CCM's (V5 p.451). ^ex-05-06-19

### Example 13: Everfloat valuation using the market approach (V5 p.452 to p.454)

Perspective: non-controlling, non-marketable minority interest.
Step 1 and 2: segment shares: revenue 70/25/5%, EBITDA 75/30/-5%; composite EV/Sales 2.635 and EV/EBITDA 7.58 from Example 11 (V5 p.453).
Step 3: $EV_{EV/Sales} = 2.635 \times 1{,}000$m $= 2{,}635$m GBP; by segment: $700 \times 2.8 + 250 \times 1.1 + 50 \times 8.0 = 1{,}960 + 275 + 400 = 2{,}635$m, so each term doubles as a stand-alone segment value; $EV_{EV/EBITDA} = 7.58 \times 250 = 1{,}895$m (V5 p.453, p.454).
Step 4: apply the total discount of 27.6% from Example 7: $2{,}635 \times 0.724 = 1{,}907.7$m and $1{,}895 \times 0.724 = 1{,}372.0$m; averaging gives 1,639.9m (V5 p.454).
Python check: `2635*0.724 = 1907.74`, `1895*0.724 = 1371.98`, `(1907.74+1371.98)/2 = 1639.86`. ^ex-05-06-20

### Knowledge check: Everfloat market approach questions (V5 p.454 to p.456)

Part 1: least valuable division by EV/Sales: Logistics Services at $250 \times 1.1 = 275$m versus Marine Navigation $700 \times 2.8 = 1{,}960$m and Energy Solutions $50 \times 8.0 = 400$m (B) (V5 p.455).
Part 2: the most valid concern with the composite EV/EBITDA multiple is that Energy Solutions' negative EBITDA implies the division has negative value, meaning someone would need to be paid to take it (A); the EV/EBITDA estimate being lower than EV/Sales and Logistics' high EBITDA share are facts, not flaws (V5 p.455).
Part 3: if most public marine equipment companies have divisional mixes similar to Everfloat's, use only those companies as comparables (C): they already mirror the whole portfolio, so per-segment comparables become unnecessary (V5 p.455, p.456). ^ex-05-06-21

## Item-set patterns

> [!warning] Trap 1: the control premium is not the DLOC
> The vignette hands you a control premium (say 30%) and asks for the discount on a minority stake.
> Correct: $DLOC = 1 - 1/1.30 = 23.1\%$ (V5 p.431).
> Distractors: 30% used directly as the discount, and a total discount computed from it (44% instead of 38.5% with a 20% DLOM); both look right because premium and discount feel symmetric, but the discount is taken off the larger control value (V5 p.434).

> [!warning] Trap 2: adding DLOC and DLOM
> The vignette gives both discounts and asks for the total.
> Correct: $1 - (1 - DLOC)(1 - DLOM)$, sequential and multiplicative (V5 p.433).
> Distractor: $DLOC + DLOM$, tempting because two deductions "should" add; it overstates the discount (29.8% versus 27.6% for Everfloat) and one option is always built from it (V5 p.433).

> [!warning] Trap 3: which discounts apply depends on the basis of the starting value
> The vignette describes how the starting value was built (control cash flows or not, optimal capital structure or not, already private) and asks which discounts to layer on.
> Correct: DLOC only if the base is a control value; DLOM for a private, non-marketable position, unless it is already embedded in the base (Starbeam's 100% owner-managed valuation already included both a control element and a DLOM, so the minority stake needed only a DLOC) (V5 p.431, p.433).
> Distractors: mechanically applying both discounts, or none; each maps to skipping the basis question.

> [!warning] Trap 4: expanded CAPM versus build-up, the missing beta and the extra industry premium
> The vignette gives one input table and asks for the difference between the two estimates.
> Correct: build-up $= r_f + ERP + P_{size} + P_{industry} + P_{company}$ with no beta; expanded CAPM $= r_f + \beta \times ERP + P_{size} + P_{company}$ with no industry premium; the difference is $(1 - \beta) \times ERP + P_{industry}$ (V5 p.424).
> Distractors: scaling the build-up ERP by beta, forgetting the industry premium, or attributing the difference to different market return assumptions (V5 p.428, p.461).

> [!warning] Trap 5: normalization direction
> The vignette mixes above-market pay, below-market pay, zero pay plus dividends, and rent-free related-party assets.
> Correct: excess expense removed raises normalized earnings; missing market-rate expense inserted (under-paid CEO, free building use) lowers them; dividends are never an expense substitute (V5 p.417, p.421, p.463).
> Distractors: "no adjustment needed because the cash amounts offset" and adjustments in the wrong direction; each rides on confusing distributions with compensation.

> [!warning] Trap 6: CCM numerator and the debt subtraction
> The vignette gives base-year FCFF, WACC, and g, then asks for EV or equity value.
> Correct: grow the numerator one year, $FCFF_0(1+g)/(WACC - g)$, and subtract debt only when asked for equity value (V5 p.436, p.463).
> Distractors: $FCFF_0/(WACC - g)$ (no growth), the right EV offered as "equity value" (no debt subtraction), and a figure with debt subtracted when EV was asked; the LPE problem set uses all three (V5 p.461).

> [!warning] Trap 7: put-option DLOM divided by the wrong number
> The vignette lists several puts at different strikes and a current stock price.
> Correct: pick the strike equal to the forward price $S_0 e^{rT}$ (at-the-money forward), then divide that premium by the spot price (V5 p.432).
> Distractors: premium divided by the strike (12.5% instead of 12.6% for JNK) and the wrong strike picked (spot instead of forward); both differ from the answer by amounts small enough to appear as adjacent options (V5 p.459, p.463).

> [!warning] Trap 8: whose discount rate, whose capital structure
> The vignette has a large public acquirer valuing a small private target, sometimes with a suboptimal target debt ratio.
> Correct: discount target cash flows at the target's rate; using the buyer's lower rate, or an optimal-structure WACC the seller never achieved, transfers the buyer's own value creation to the seller (V5 p.423, p.429).
> Distractors: "the buyer's WACC is appropriate because it funds the deal" and "the lower optimal WACC is the right base for the offer"; both sound like synergy pricing but are wealth transfers.

> [!warning] Trap 9: composite multiples weighted by the wrong fundamental
> The vignette gives segment multiples and segment financials.
> Correct: weight EV/Sales by sales shares and EV/EBITDA by EBITDA shares, or equivalently apply each segment multiple to that segment's own fundamental and sum; a negative-EBITDA segment gets a negative weight or a sales multiple instead (V5 p.443, p.453).
> Distractors: equal weights, sales weights on the EBITDA multiple, and dropping the loss-making segment; each produces a plausible-looking EV on the answer sheet.

> [!warning] Trap 10: relevered beta relative to the comparables
> The vignette says the private target has less debt than the public comparables and asks about its beta.
> Correct: unlever at the comparables' D/E and tax rate, relever at the target's lower D/E, so the target beta lands below the comparables' levered beta (V5 p.440, p.462, p.463).
> Distractors: using the comparables' beta unadjusted (equal), or reasoning that private means riskier so beta must be higher; extra private-company risk belongs in the size and company-specific premia, not in beta.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM06-Private-Company-Valuation-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: supplies the growing-perpetuity engine and the r > g condition behind the CCM, the EEM capitalization, and every terminal value in this module.
- [[LM03-Free-Cash-Flow-Valuation]]: defines FCFF and FCFE, the WACC versus cost-of-equity discounting rule, and the firm-to-equity bridge that private valuation reuses on normalized numbers.
- [[LM04-Market-Based-Valuation-Price-and-Enterprise-Value-Multiples]]: the method of comparables, EV construction, and multiple selection that the GPCM and GTM import, plus why EV multiples beat price multiples when capital structure will change.
- [[LM05-Residual-Income-Valuation]]: the residual income concept that the excess earnings method reimplements with per-asset-class capital charges.
- [[LM03-Cost-of-Capital-Advanced-Topics]] (04-Corporate-Issuers): the expanded CAPM, build-up method, size and company-specific premia, and beta unlevering and relevering in their full cost-of-capital treatment.
- [[LM04-Corporate-Restructuring]] (04-Corporate-Issuers): the acquisition context for control premiums, synergies, and why targets are valued at their own cost of capital.
- [[LM04-Hedge-Fund-Strategies]] (08-Alternative-Investments): activist and event-driven strategies that buy influence or control in companies, where control premiums and illiquidity discounts price the position.

## Self-test

Vignette A for Q1 to Q5: Berner Precision GmbH is a private Swiss toolmaker wholly owned by its founder-CEO, who pays herself EUR 1.8 million against a market rate of EUR 0.6 million.
The company owns a lakeside villa unrelated to operations: EUR 0.3 million of its running costs sit in SG&A and EUR 0.1 million of depreciation sits in D&A.
Reported figures: EBITDA EUR 10.0 million, D&A EUR 1.5 million, tax rate 20%, capital expenditures EUR 1.6 million, increase in working capital EUR 0.4 million.
An analyst gathers: risk-free rate 3%, ERP 5%, relevered comparable beta 1.2, small-stock premium 2.5%, company-specific premium 1.5%, industry risk premium 0.5%, pre-tax cost of debt 6%, target weights 90% equity and 10% debt, debt outstanding EUR 5 million, perpetual FCFF growth 4%.

> [!question] Q1
> Normalized EBITDA is closest to:
> A. EUR 10.0 million.
> B. EUR 11.2 million.
> C. EUR 11.5 million.

> [!question] Q2
> Base-year FCFF from the normalized figures is closest to:
> A. EUR 6.48 million.
> B. EUR 7.48 million.
> C. EUR 9.48 million.

> [!question] Q3
> The required return on equity under the expanded CAPM is closest to:
> A. 12.5%.
> B. 13.0%.
> C. 13.5%.

> [!question] Q4
> Relative to the expanded CAPM estimate, the build-up estimate is:
> A. 0.5% lower, because the unscaled ERP loses more than the industry premium adds.
> B. 0.5% higher, because the industry premium is an extra factor.
> C. identical, because beta is close to one.

> [!question] Q5
> Using the expanded CAPM cost of equity and the target weights, the CCM equity value is closest to:
> A. EUR 86.4 million.
> B. EUR 90.1 million.
> C. EUR 95.1 million.

Vignette B for Q6 to Q10: Meridian Cranes Ltd. is a private crane manufacturer.
An analyst has estimated a marketable, controlling-interest value of GBP 240 million from a DCF built on control cash flows and an optimal capital structure.
Acquisition data for comparable public companies show a 20% control premium for financial buyers.
The closest public comparable trades at GBP 40.00; with a six-month horizon and a 4% risk-free rate, a put struck at the six-month forward price is valued at GBP 6.20.
Meridian has two segments: Sales of 600 (peer EV/Sales 2.0) and 400 (peer EV/Sales 0.9), in GBP millions.
A colleague proposes valuing Meridian from three recent acquisitions of whole crane companies by strategic buyers.

> [!question] Q6
> The DLOC implied by the control premium is closest to:
> A. 16.7%.
> B. 20.0%.
> C. 23.1%.

> [!question] Q7
> The DLOM from the put option approach is closest to:
> A. 14.9%.
> B. 15.2%.
> C. 15.5%.

> [!question] Q8
> The value of a non-controlling, non-marketable minority interest basis for Meridian (total value, before pro rata allocation) is closest to:
> A. GBP 162.7 million.
> B. GBP 169.0 million.
> C. GBP 202.8 million.

> [!question] Q9
> The composite EV/Sales multiple and the resulting EV are closest to:
> A. 1.45 and GBP 1,450 million.
> B. 1.56 and GBP 1,560 million.
> C. 2.00 and GBP 2,000 million.

> [!question] Q10
> The most accurate criticism of the colleague's proposal to price Meridian from the three strategic acquisitions is that the transaction multiples:
> A. reflect minority trades and need a control premium added.
> B. embed synergies and a control premium, overstating a stand-alone or minority value.
> C. cannot be used because private transaction data are never disclosed.

> [!success]- Answer key
> Q1: C.
> Excess compensation $1.8 - 0.6 = 1.2$m and villa operating costs 0.3m come out of SG&A: $10.0 + 1.2 + 0.3 = 11.5$m (Formula and logic of Example 1, V5 p.417).
> A makes no adjustment; B removes only the compensation excess and leaves the non-operating villa costs in.
> Q2: B.
> Normalized D&A $= 1.5 - 0.1 = 1.4$m; $FCFF = 11.5 \times 0.8 + 1.4 \times 0.2 - 1.6 - 0.4 = 9.2 + 0.28 - 2.0 = 7.48$m (Formula 10; Python: `11.5*0.8+1.4*0.2-2.0 = 7.48`).
> A uses reported EBITDA of 10.0 with reported D&A ($10 \times 0.8 + 1.5 \times 0.2 - 2.0 = 6.3$, nearest bait); C forgets capex and working capital only partially.
> Q3: B.
> $3 + 1.2 \times 5 + 2.5 + 1.5 = 13.0\%$ (Formula 3).
> A is the build-up answer; C adds the industry premium into the expanded CAPM, which does not use one.
> Q4: A.
> Build-up $= 3 + 5 + 2.5 + 0.5 + 1.5 = 12.5\%$; the unscaled ERP gives up $(1.2 - 1) \times 5 = 1.0\%$ while the industry premium adds back only 0.5%, netting 0.5% lower (Formula 4; V5 p.424, p.429).
> B has the net sign wrong; C wrongly assumes the two effects cancel.
> Q5: B.
> $r_d = 6 \times 0.8 = 4.8\%$; $WACC = 0.9 \times 13 + 0.1 \times 4.8 = 12.18\%$ (Formula 1).
> $EV = 7.48 \times 1.04/(0.1218 - 0.04) = 7.7792/0.0818 = 95.10$m; equity $= 95.10 - 5 = 90.10$m (Formula 11; Python: `7.48*1.04/0.0818-5 = 90.100`).
> A capitalizes without growing the numerator and then subtracts debt ($7.48/0.0818 - 5 = 86.44$); C stops at EV without subtracting debt.
> Q6: A.
> $DLOC = 1 - 1/1.20 = 16.7\%$ (Formula 6).
> B uses the premium as the discount; C converts a 30% premium nobody quoted.
> Q7: C.
> The put is already struck at the forward ($40 e^{0.02} = 40.81$), so $DLOM = 6.20/40.00 = 15.5\%$ (Formula 7; Python: `6.20/40 = 0.155`).
> B divides by the forward price 40.81 ($= 15.2\%$); A divides by the strike-plus-premium and is bait for over-adjusters.
> Q8: B.
> The 240m is a marketable control value, so both discounts apply: total discount $= 1 - (1 - 0.1667)(1 - 0.155) = 29.6\%$; value $= 240 \times 0.8333 \times 0.845 = 169.0$m (Formula 8; Python: `240*(1/1.2)*0.845 = 169.0`).
> A applies $1 - (0.20 + 0.155) = 32.2\%$ additively after misreading the DLOC ($240 \times 0.678 = 162.7$); C applies only the DLOM.
> Q9: B.
> Sales weights 0.6 and 0.4: composite $= 0.6 \times 2.0 + 0.4 \times 0.9 = 1.56$; $EV = 1.56 \times 1{,}000 = 1{,}560$m (Formula 19; Python: `0.6*2+0.4*0.9 = 1.56`).
> A equal-weights the multiples ($(2.0 + 0.9)/2 = 1.45$); C uses the larger segment's multiple alone.
> Q10: B.
> GTM multiples from strategic acquisitions embed synergies and a control premium, so applying them unadjusted overstates a stand-alone or minority value (V5 p.444).
> A describes GPCM trading data, not acquisition data; C is false because transaction data are compiled from filings and databases, merely with reliability caveats (V5 p.444).

## Flashcards

#flashcards/cfa-l2/05-Equity-Valuation/lm06

Company-specific factors distinguishing private companies::Life-cycle stage, smaller size, concentrated ownership, limited disclosures, owner-manager overlap (V5 p.407).
Stock-specific factors distinguishing private company shares::Illiquidity, concentrated control, restrictions on sale; generally negative for value (V5 p.407, p.408).
Why can company-specific factors be positive for value?::An early-stage founder-controlled firm may have greater growth potential than public rivals, while stock-specific factors only subtract (V5 p.408, p.409).
Effect of owner-manager overlap on agency costs::It largely removes the principal-agent problem and allows longer-horizon strategic decisions (V5 p.408).
Three practice areas of private company valuation::Transactions, compliance (financial and tax reporting), litigation (V5 p.412).
Where are share-based payments to employees valued?::In the transaction practice area, as securities transactions between the company and employees (V5 p.413).
Fair market value in one line::The arm's length price between independent, willing, informed parties, the standard for financial and tax reporting (V5 p.412, p.415).
Investment value in one line::Value to a specific buyer including synergies only that buyer can capture; explains why a strategic acquirer can pay above fair market value (V5 p.412, p.430).
Three areas of focus in any private valuation::Normalize earnings and cash flow (numerator), adjust the discount rate (denominator), then apply discounts or premiums (stock level) (V5 p.413).
Audited versus reviewed versus compiled statements::Audit gives the highest assurance; a review gives limited assurance via an opinion letter; compiled statements carry no auditor opinion; less than an audit usually needs adjustment (V5 p.414).
Related party versus arm's length transaction::Related parties share economic interests and may deal away from fair market value; arm's length parties deal independently at or near fair market value (V5 p.415).
Normalization for above-market owner compensation::Reduce the expense to the market rate, raising normalized EBIT and the recomputed tax charge (V5 p.417).
Normalization when the owner takes no salary but a large dividend::Insert market-rate compensation expense, lowering normalized earnings; dividends never substitute for compensation cost (V5 p.421).
Normalization for company-owned real estate used in operations::Separate the property, remove its revenues and expenses, charge market rent to operations, and treat the property as a non-operating asset (V5 p.418).
Why separate real estate from operations?::Business operations and real estate have different risk levels and growth expectations (V5 p.418).
Managerial bias directions in private forecasts::Overstated values for goodwill impairment testing, understated values for incentive stock option grants (V5 p.421).
Expanded CAPM::r_f plus beta times ERP plus small-stock premium plus company-specific premium (V5 p.424).
Build-up approach::r_f plus full ERP plus small-stock premium plus industry risk premium plus company-specific premium, with no beta (implicitly beta of one) (V5 p.424).
When is the build-up approach preferred?::When comparable public companies are unavailable or of questionable comparability (V5 p.424).
The two structural differences between build-up and expanded CAPM::{{Build-up adds an industry risk premium}} and {{does not scale the ERP by beta}} (V5 p.428, p.429).
Micro-problem: rf 3.8%, ERP 5%, beta 1.1, size 3%, company 1%; expanded CAPM?::3.8 + 5.5 + 3 + 1 = 13.3%; keystrokes 1.1 × 5 + 3.8 + 3 + 1 = (V5 p.426).
Why a size premium needs care::Smallest-cap public data may reflect financial or operating distress irrelevant to the subject company (V5 p.423).
Effect of limited debt access on private WACC::More equity in the structure, and since equity costs more than debt the WACC sits above the optimal level (V5 p.423, p.462).
Whose cost of capital prices an acquisition?::The target's, based on target cash flow risk and capital structure; the buyer's lower rate would gift the seller the buyer's value creation (V5 p.423, p.429).
Which capital structure weights for valuing a company for sale?::The optimal structure an acquirer would establish, though a small private firm's optimal debt weight is below large public comparables' (V5 p.426).
DLOC formula::1 minus 1 divided by (1 plus control premium) (V5 p.431).
Micro-problem: control premium 25%; DLOC?::1 - 1/1.25 = 20%; keystrokes 1.25 1/x +/- + 1 = (V5 p.431).
When does a DCF value already reflect lack of control?::When it is built on non-control cash flows and/or a discount rate without an optimal capital structure (V5 p.431).
Strategic versus financial buyer::Strategic buyer captures synergies and pays the larger premium; financial buyer pays for control without synergies (V5 p.430, p.444).
Three data sources for DLOM estimates::Restricted stock transactions, pre-IPO share sales, and put option pricing (V5 p.432).
Put option DLOM recipe::Price an at-the-money put struck at the forward price on the closest comparable, divide the premium by the current stock price (V5 p.432).
Two weaknesses of the put-based DLOM::A put protects price without providing liquidity, and it leaves the holder the upside, so it is not a true marketability model (V5 p.432, p.433).
Total discount formula::1 minus (1 minus DLOC) times (1 minus DLOM); sequential, multiplicative, never additive (V5 p.433).
Micro-problem: DLOC 23.1%, DLOM 20%; total discount?::1 - 0.769 × 0.80 = 38.5%; the additive 43.1% is the trap (V5 p.434).
Other valuation discounts besides DLOC and DLOM::Key person discounts, portfolio (non-homogeneous asset) discounts, non-voting share discounts (V5 p.433).
What shrinks both discounts?::A near-term liquidity event such as a pursued IPO or strategic sale (V5 p.430).
Three private valuation approaches::Income (DCF including CCM and EEM), market (GPCM, GTM, prior transaction), asset-based (assets minus liabilities) (V5 p.434, p.435, p.440).
Which approach is used most and why?::The market approach, because it rests on actual market transaction evidence (V5 p.440).
When does the CCM fit best?::A stable private company with no projections available and limited market pricing evidence; also the standard terminal value engine (V5 p.436).
CCM firm value formula::FCFF next year divided by (WACC minus g), then subtract market value of debt for equity (V5 p.436).
Reinvestment rate implied by CCM::g divided by WACC (V5 p.436, p.445).
Capitalization rate in the FCFE version::r_e minus g, the denominator applied to next year's FCFE (V5 p.436).
When is face value of debt an acceptable proxy for market value?::When debt is a small fraction of financing and operations are stable; otherwise match against public debt of similar type, tenor, credit, and industry (V5 p.436).
Excess earnings method in one line::Deduct required returns on working capital and fixed assets from normalized earnings, capitalize the residual as intangible value, add back tangible asset values (V5 p.438).
Ranking of EEM required returns::Working capital lowest, fixed assets higher, residual income on intangibles highest (V5 p.438).
Micro-problem: normalized income 120k, WC 200k at 4%, FA 800k at 10%; residual income?::120,000 - 8,000 - 80,000 = 32,000 (V5 p.446).
Where is the EEM actually used?::Intangible asset valuation for financial reporting and very small businesses; rarely whole companies, because it needs three subjective rates (V5 p.439).
Top-down FCFF formula used in this module::EBITDA(1 - t) + Depreciation × t - change in LT assets - change in working capital, equal to EBIT(1 - t) + Depreciation - capex - change in WC (V5 p.412, p.447).
GPCM versus GTM versus prior transaction::GPCM uses trading multiples of comparable public companies; GTM uses acquisition multiples of whole companies; prior transaction method uses actual trades in the subject's own stock (V5 p.440).
Why prefer EV multiples over price multiples for private firms?::EV accommodates capital structure changes over the valuation period (V5 p.440).
Beta unlevering rule::Divide the comparable's levered beta by 1 + (1 - t)(D/E) using the comparable's tax rate and leverage, then relever with the subject's (V5 p.440, p.441).
Direction of the relevered beta for a low-debt private firm::Below the public comparables' levered beta, because the subject carries less debt (V5 p.441, p.463).
Composite multiple construction::Weight each segment's peer multiple by the subject's segment share of that fundamental; sales weights for EV/Sales, EBITDA weights for EV/EBITDA (V5 p.443, p.453).
Handling a negative-EBITDA segment in a composite::Its weight is negative and implies negative segment value; better to price that segment on a sales multiple (V5 p.443, p.454).
Factors when estimating a control premium from transaction data::Type of transaction (strategic versus financial), industry "in play" timing effects, and form of consideration (stock deals may reflect overvalued acquirer shares) (V5 p.444).
GTM data caveats::Synergies and control in the price, contingent consideration, non-cash consideration, few available transactions, staleness between transaction and valuation dates (V5 p.444, p.445).
Which discounts for a minority stake when the base valuation already includes a DLOM?::Only the DLOC; layering another DLOM double counts (V5 p.433).
Scenario valuation of an early-stage company::Value each outcome at its resolution date with a growing perpetuity, weight by path probabilities, discount at the WACC; failure paths contribute zero (V5 p.420).

## Common mistakes

1. Using the control premium itself as the DLOC instead of $1 - 1/(1 + CP)$; a 30% premium is a 23.1% discount (V5 p.431, p.434).
2. Adding DLOC and DLOM instead of chaining them multiplicatively with $1 - (1 - DLOC)(1 - DLOM)$ (V5 p.433).
3. Applying a DLOC to a value that was never on a control basis, or a second DLOM to a valuation that already embeds one, as in Starbeam (V5 p.431, p.433).
4. Normalizing in the wrong direction: excess owner pay raises normalized earnings, but below-market or zero pay (with dividends instead) requires inserting a market compensation expense that lowers them (V5 p.417, p.421, p.463).
5. Leaving non-operating assets' costs in the income statement, or forgetting the market rent charge when the company uses owned or related-party property (V5 p.418, p.421).
6. Forgetting to recompute taxes on normalized income after expense adjustments (V5 p.417).
7. Capitalizing the base-year cash flow without growing it: the CCM numerator is $FCFF_0(1 + g)$, and the terminal numerator grows at the terminal rate, not the stage-one rate (V5 p.436, p.448, p.463).
8. Reporting EV when equity value is asked, or vice versa: subtract the market value of debt from firm value, and never subtract debt from a capitalized FCFE (V5 p.436, p.463).
9. Scaling the build-up ERP by beta, or putting an industry risk premium into the expanded CAPM (V5 p.424, p.428).
10. Using the buyer's cost of capital or a not-yet-real optimal capital structure to price a target, paying the seller for the buyer's own improvements (V5 p.423, p.429).
11. Dividing the put premium by the strike instead of the spot, or pricing the put at the spot strike instead of the forward (V5 p.432, p.463).
12. Using comparables' levered betas without unlevering at their leverage and relevering at the subject's lower debt ratio (V5 p.440, p.441, p.463).
13. Weighting a composite EV/EBITDA multiple with sales shares, or dropping a negative-EBITDA segment instead of handling it explicitly (V5 p.443, p.453).
14. Treating GTM acquisition multiples as if they were minority trading multiples: they embed control and often synergies (V5 p.444).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "05-06" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
