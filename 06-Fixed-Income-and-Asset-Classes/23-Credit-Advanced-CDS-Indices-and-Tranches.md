---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: solid
prereqs: [credit-and-cds]
est_hours: 5
sources: [David X. Li - On Default Correlation - A Copula Function Approach - Journal of Fixed Income 2000, Oldrich Vasicek - The Distribution of Loan Portfolio Value - Risk 2002, John Hull and Alan White - Valuation of a CDO and an n-th to Default CDS Without Monte Carlo Simulation - Journal of Derivatives 2004, S&P Dow Jones Indices - Markit CDX HY and IG Rules 2022 and iTraxx Europe and Crossover Rulebook, Markit - The CDS Big Bang - 2009, Bruce Tuckman and Angel Serrat - Fixed Income Securities 3rd edition chapter 19]
---

# Credit Advanced: CDS Indices and Tranches

## TL;DR

- CDX and iTraxx indices are equally weighted baskets of single-name CDS (125 names for CDX NA IG and iTraxx Europe, 100 for CDX NA HY, up to 75 for iTraxx Crossover) that roll into a new series every 20 March and 20 September and trade with a fixed coupon plus an upfront.
- The index should be compared with its duration-weighted intrinsic spread, not the simple average of constituent spreads: on a dispersed five-name example the two differ by $6.6$ bp and the basis changes sign.
- Tranches $[A, D]$ take portfolio losses between attachment $A$ and detachment $D$; the one-factor Gaussian copula and its large homogeneous pool limit (Vasicek) give their expected losses in closed form or by one-dimensional quadrature.
- Mezzanine tranche losses are not monotone in correlation, so compound correlation can have two solutions or none; base correlation quotes equity tranches $[0, K]$ only, which are monotone.
- The Gaussian copula has zero tail dependence: at correlation $0.3$ the probability of a second default given a first falls from $0.143$ at the 5% quantile to $0.015$ at the 0.1% quantile.

## Learning objectives

- Master CDX (North America) and iTraxx (Europe/Asia) index construction, rolling conventions, and upfront quoting mechanics.
- Formulate the CDS index basis against the duration-weighted intrinsic spread and identify its drivers.
- Structure standardized synthetic CDO tranches across equity, mezzanine, senior and super-senior layers.
- Derive the one-factor Gaussian copula model and the conditional default probability under systemic market factor realizations.
- Compute expected tranche losses using numerical integration over the portfolio loss distribution, in the large-pool limit and for a finite pool.
- Contrast compound correlation against base correlation, explaining why compound correlation fails for mezzanine tranches.
- Analyze the failure modes of the Gaussian copula, specifically zero tail dependence.

## Core concepts

### 1. CDX and iTraxx indices

| Index | Constituents (per the index rules) |
| :--- | :--- |
| CDX NA IG | 125 North American investment grade entities |
| CDX NA HY | 100 North American high yield entities |
| iTraxx Europe | 125 European investment grade entities |
| iTraxx Crossover | up to 75 European sub-investment grade entities |

- New series start on 20 March and 20 September (or the next business day); a March series matures on 20 June and a September series on 20 December of the maturity year, with 5 years the most liquid tenor.
- At each roll the constituent list is rebuilt by the published rules (rating and liquidity criteria); names that no longer qualify drop out of the new series, while old series keep trading as off-the-run.
- Each series has a fixed running coupon; recent series use 100 bp for CDX IG and iTraxx Europe and 500 bp for CDX HY and iTraxx Crossover, with the difference to the market spread paid upfront.
- The 2009 "Big Bang" (North America) and "Small Bang" (Europe) protocols brought single-name CDS onto standard coupons and hardwired auction settlement, Determination Committees and a fixed look-back for credit events (Markit 2009).
- After a constituent's credit event, its $1/N$ share is settled at the auction price, the protection seller paying $(1 - \text{FP})/N$ of notional, and the index continues on the remaining $(N - 1)/N$ notional as a new version of the series.

**Upfront and price.**
With a flat hazard curve calibrated to the quoted spread $S$ (the ISDA standard model convention), protection leg $= S \times \text{RPV01}$, so
$$\text{Upfront} = (S - C) \times \text{RPV01},$$
paid by the protection buyer when $S > C$, plus accrued coupon since the last coupon date.
CDX HY is quoted as a price, $100 - \text{Upfront}\%$.

### 2. Intrinsic spread and the index basis

The index trades against the portfolio of its constituents' CDS; the comparable single number is the intrinsic spread that makes the two portfolios' coupon streams equal in value:
$$S_{\text{intrinsic}} \approx \frac{\sum_i S_i \, \text{RPV01}_i}{\sum_i \text{RPV01}_i}.$$
Wider names have shorter risky annuities, so the intrinsic spread is below the simple average whenever spreads are dispersed; a basis measured against the simple average is biased negative.
The basis $S_{\text{index}} - S_{\text{intrinsic}}$ can take either sign; it moves with relative liquidity and hedging flows (the index is used to hedge first), with the cost of trading 125 single names, and with differences in contract terms between index and single-name CDS.

### 3. Synthetic tranches

A tranche $[A, D]$ absorbs portfolio loss (fraction of the original notional) between $A$ and $D$:
$$L_{[A, D]}(t) = \frac{\min\left(\max(L(t) - A, 0), D - A\right)}{D - A}.$$
The protection seller receives a running spread (equity tranches traditionally traded as upfront plus 500 bp running) on the outstanding tranche notional and pays the incremental tranche losses.
The standard index tranches before the crisis were 0-3%, 3-7%, 7-10%, 10-15%, 15-30% and 30-100% for CDX IG, and 0-3%, 3-6%, 6-9%, 9-12% and 12-22% for iTraxx Europe (Hull and White 2004); the standard set has changed since, so check the current one.

### 4. The one-factor Gaussian copula

Li (2000) introduced the Gaussian copula for joint default times: each name's default time keeps its own marginal, calibrated to its CDS curve, and dependence comes from correlated normals.
The one-factor version used for tranches follows Vasicek's loan-portfolio model:
$$X_i = \sqrt{\rho} M + \sqrt{1 - \rho} Z_i, \qquad \tau_i \le t \iff X_i \le \Phi^{-1}(p_i(t)),$$
with $M, Z_i$ independent standard normals, so $X_i \sim N(0, 1)$ and $\text{corr}(X_i, X_j) = \rho$.
Conditional on $M = m$ defaults are independent with
$$p_i(t \mid m) = \Phi\left(\frac{\Phi^{-1}(p_i(t)) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right).$$

**Finite pools.**
For a homogeneous pool of $N$ names the number of defaults given $m$ is binomial$(N, p(t \mid m))$; for heterogeneous pools the conditional loss distribution is built by recursion (Andersen, Sidenius and Basu 2003; Hull and White 2004), then integrated over $m$.

**Large homogeneous pool (LHP).**
As $N \to \infty$ the conditional loss is deterministic, $L(m) = (1 - R)\, p(t \mid m)$, and since it decreases in $m$ the loss distribution is Vasicek's:
$$P(L \le x) = \Phi\left(\frac{\sqrt{1 - \rho}\, \Phi^{-1}\left(\frac{x}{1 - R}\right) - \Phi^{-1}(p)}{\sqrt{\rho}}\right).$$
Tranche expected loss follows either by integrating over $m$, $\mathbb{E}[L_{[A,D]}] = \int L_{[A,D]}(L(m)) \phi(m) dm$, or from the distribution, $\mathbb{E}[\min(\max(L - A, 0), D - A)] = \int_A^D P(L > x) dx$; the script computes both and checks they agree.

### 5. Compound and base correlation

**Compound correlation** is the single $\rho$ that reprices one tranche.
Equity expected loss falls monotonically as $\rho$ rises (correlation spreads the loss distribution, and the equity payoff is concave in $L$), but mezzanine loss first rises and then falls: at low $\rho$ losses cluster near the mean and stay below the attachment, at high $\rho$ the pool either survives or loses far beyond the detachment.
So a mezzanine price can have two compound correlations or, above the maximum, none (Example 4).

**Base correlation** quotes only equity tranches $[0, K]$, each with its own correlation $\rho(K)$, and prices $[A, D]$ as a difference of two base tranches:
$$\mathbb{E}\left[\text{Loss}_{[A, D]}\right] = \frac{D \, \mathbb{E}\left[\text{Loss}_{[0, D]}; \rho(D)\right] - A \, \mathbb{E}\left[\text{Loss}_{[0, A]}; \rho(A)\right]}{D - A}.$$
(With one $\rho$ for both legs this is an identity; base correlation's content is that the two legs use different correlations.)
A base correlation is unique when it exists, because equity loss is monotone in $\rho$.
The resulting curve $\rho(K)$, rising with $K$ in the market, is the correlation skew.
Its weaknesses: interpolating $\rho(K)$ between standard strikes can produce negative expected losses for thin tranches (an arbitrage), the curve is not consistent across maturities, and pricing bespoke portfolios requires mapping their strikes onto the index curve.

### 6. Where the Gaussian copula fails

The bivariate Gaussian copula with $\rho < 1$ has zero lower tail dependence:
$$\lambda_L = \lim_{u \to 0} P(U_1 \le u \mid U_2 \le u) = 0.$$
Example 6 shows how fast the conditional probability falls at $\rho = 0.3$.
Copulas with positive tail dependence (Student-$t$, Clayton) or models with random factor loadings, random recovery or jumps generate more clustering of defaults for the same pairwise correlation and fit the skew better.

In 2008 the largest losses on super senior positions came from CDOs of asset-backed securities, especially subprime mortgage bonds, not from corporate index tranches: for example, UBS reported that retained super senior positions of ABS CDOs were a large share of its write-downs (UBS, *Shareholder Report on UBS's Write-Downs*, April 2008).
For such structures the problems went beyond the copula: the inputs (default probabilities and correlations of mortgage bonds calibrated to a benign period) and the concentration of correlated collateral mattered as much as the dependence function.

## Worked examples

### Example 1: CDX HY upfront
$\$50$ million of 5-year CDX HY protection, coupon $500$ bp, market spread $420$ bp, $\text{RPV01} = 4.15$:
$$\text{Upfront} = (0.0420 - 0.0500) \times 4.15 = -3.32\%,$$
so the seller pays the buyer $\$1,660,000$ (the buyer will overpay $80$ bp a year in coupon), and the quoted price is $100 + 3.32 = 103.32$.

### Example 2: intrinsic spread
Five equally weighted names at $40, 60, 80, 150, 400$ bp, recovery $40\%$, rates $4\%$, flat hazard $S/(1 - R)$ and continuous premium:
the simple average is $146$ bp; the risky annuity is $4.46$ at $40$ bp but $3.88$ at $400$ bp, and the duration-weighted intrinsic spread is $139.4$ bp.
An index quoted at $140$ bp looks $6.0$ bp tight to the simple average but is $0.6$ bp wide to intrinsic.

### Example 3: copula and LHP losses
$p = 5\%$ (5-year), $R = 40\%$, $\rho = 0.30$; threshold $\Phi^{-1}(0.05) = -1.6449$.
- At $M = -2.5$: $p(m) = \Phi\left(\frac{-1.6449 + \sqrt{0.3} \times 2.5}{\sqrt{0.7}}\right) = 37.09\%$ and the pool loses $0.6 \times 37.0949\% = 22.26\%$, wiping out both $[0, 3\%]$ and $[7\%, 10\%]$.
- At $M = -2.0$: $p(m) = 25.57\%$, loss $15.34\%$.
- Unconditionally, expected pool loss is $p(1 - R) = 3.00\%$, and the LHP tranche expected losses are $54.11\%$ for $[0, 3\%]$, $19.58\%$ for $[3\%, 7\%]$, $8.78\%$ for $[7\%, 10\%]$ and $34.38\%$ for $[0, 7\%]$.
Integrating the Vasicek distribution instead of the factor gives the same numbers to $10^{-4}$, an independent check.

### Example 4: compound and base correlation
Expected loss of $[3\%, 7\%]$ against correlation: $6.18\%$ at $0.01$, $17.16\%$ at $0.10$, $19.58\%$ at $0.30$, $17.77\%$ at $0.50$, $10.24\%$ at $0.90$; on a $0.01$ grid it peaks at $19.67\%$ near $\rho = 0.26$.
A mezzanine expected loss of $17\%$ is matched by two compound correlations, $0.097$ and $0.557$; one above $19.67\%$ by none.
Base correlation instead: with $\rho(3\%) = 0.20$ and $\rho(7\%) = 0.30$, $\mathbb{E}[L_{[0,3\%]}] = 62.77\%$ and $\mathbb{E}[L_{[0,7\%]}] = 34.38\%$, so
$$\mathbb{E}[L_{[3\%,7\%]}] = \frac{0.07 \times 34.38\% - 0.03 \times 62.77\%}{0.04} = 13.09\%.$$
In reverse, an equity expected loss of $50\%$ implies a base correlation of $0.353$.

### Example 5: 125 names versus the LHP
For a homogeneous 125-name pool with the same inputs, conditional binomial losses give $52.14\%$ for $[0, 3\%]$, $20.09\%$ for $[3\%, 7\%]$ and $9.21\%$ for $[7\%, 10\%]$, against $54.11\%$, $19.58\%$ and $8.78\%$ in the LHP limit.
Idiosyncratic default risk, which the LHP removes, moves loss from the equity to the senior layers.

### Example 6: tail dependence in numbers
For the Gaussian copula with $\rho = 0.3$, $P(U_1 \le u \mid U_2 \le u)$ is $0.1427$ at $u = 5\%$, $0.0556$ at $1\%$ and $0.0149$ at $0.1\%$: the further into the tail, the closer joint extremes come to independence.

## Pitfalls

- **Simple-average basis:** comparing the index with the simple average of constituent spreads builds in a negative bias that grows with dispersion (Example 2).
- **Quoting one "implied correlation" for a mezzanine tranche:** it may not exist or may not be unique; say whether it is compound or base.
- **Interpolated base correlations:** thin tranches priced off an interpolated base correlation curve can have negative expected loss; check tranchelet losses for monotonicity.
- **Using the LHP for small or concentrated pools:** with 125 names the LHP already misstates equity loss by about two points (Example 5); with fewer names or uneven notionals use the recursion.
- **Forgetting defaults after the trade:** after a credit event the index notional and coupons fall to $(N - 1)/N$, and the tranche attachments of an index tranche shift as losses erode subordination.
- **Funding the upfront:** upfronts on wide indices and equity tranches are large cash amounts whose financing belongs in the trade's P&L.

## Interview questions

> [!question]- fi-cdx-itraxx-composition | What are the differences between CDX and iTraxx indices regarding constituent count, geography, and standard roll dates?
> CDX covers North America (CDX NA IG with 125 investment grade names, CDX NA HY with 100 high yield names); iTraxx covers Europe and Asia (iTraxx Europe with 125 investment grade names, iTraxx Crossover with up to 75 sub-investment grade names).
> Both roll into new series on 20 March and 20 September, the new 5-year series maturing on 20 June or 20 December.

> [!question]- fi-cdx-standard-cds-coupons | Why did CDS indices adopt standardized fixed coupons of 100 bps and 500 bps, and how are market differences settled?
> Index contracts have always paid a fixed coupon set per series; standard levels (100 bp for investment grade, 500 bp for high yield and crossover in recent series) and the 2009 Big Bang standard single-name coupons make contracts fungible, which supports netting and central clearing.
> The difference between market spread and coupon is paid upfront, about $(S - C) \times \text{RPV01}$: $-3.32\%$ for a 420 bp CDX HY at a 500 bp coupon.

> [!question]- fi-cdx-credit-index-basis | Define the CDS index basis and explain why an index often trades tighter than the weighted sum of its single-name components.
> The basis is the index spread minus the intrinsic spread, the risky-annuity-weighted average of constituent spreads; it can be of either sign and moves with liquidity, hedging flows and contract differences.
> Part of the apparent tightness against a simple average is not a basis at all: wide names have short risky annuities, so in Example 2 the intrinsic spread is $139.4$ bp against a simple average of $146$ bp, and an index at $140$ bp is actually $0.6$ bp wide.

> [!question]- fi-cdx-default-event-index-settlement | What happens to a CDS index when one of its constituent reference entities declares bankruptcy?
> An auction sets the final price FP of the defaulted name's obligations, and protection sellers pay $(1 - \text{FP})/N$ of the index notional.
> The name leaves the index, which continues as a new version of the same series with $(N - 1)/N$ of the notional and the same coupon rate on that reduced notional.

> [!question]- fi-cdx-one-factor-copula-formulation | In the one-factor Gaussian copula model, explain how the latent variable $X_i = \sqrt{\rho} M + \sqrt{1 - \rho} Z_i$ induces correlation while preserving marginal distributions.
> $X_i$ is standard normal because $\rho + (1 - \rho) = 1$, and $\text{cov}(X_i, X_j) = \rho$ through the shared $M$.
> Setting the default threshold at $\Phi^{-1}(p_i(t))$ reproduces each name's marginal default probability, so correlation is added without touching the single-name calibration.

> [!question]- fi-cdx-lhp-approximation-vasicek | How does the Large Homogeneous Portfolio (LHP) approximation simplify portfolio loss modeling under the Gaussian copula?
> As $N \to \infty$ idiosyncratic risk diversifies away, so the loss given $M = m$ is the deterministic $(1 - R)\Phi\left(\frac{\Phi^{-1}(p) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right)$ and the loss distribution is Vasicek's closed form.
> Tranche expected losses become one-dimensional integrals: $54.11\%$, $19.58\%$, $8.78\%$ for $[0,3]$, $[3,7]$, $[7,10]$ at $p = 5\%$, $\rho = 0.3$, $R = 40\%$.

> [!question]- fi-cdx-compound-correlation-deficiency | Why does compound correlation fail as a robust pricing metric for synthetic CDO mezzanine tranches?
> Mezzanine expected loss is not monotone in correlation: in Example 4 it rises from $6.18\%$ at $\rho = 0.01$ to a peak of $19.67\%$ near $0.26$ and falls to $10.24\%$ at $0.9$.
> So a price can correspond to two correlations ($17\%$ is matched by $0.097$ and $0.557$) or, above the peak, to none, and the number cannot be interpolated to other tranches.

> [!question]- fi-cdx-base-correlation-concept | Explain how the base correlation curve resolves the non-monotonicity problem of compound correlation.
> It quotes only equity tranches $[0, K]$, whose expected loss falls monotonically in correlation, so each $\rho(K)$ is unique when it exists; $[A, D]$ is priced as $D \cdot \mathbb{E}[L_{[0,D]}; \rho(D)] - A \cdot \mathbb{E}[L_{[0,A]}; \rho(A)]$ over $D - A$.
> With $\rho(3\%) = 0.20$ and $\rho(7\%) = 0.30$ this gives $13.09\%$ for $[3\%, 7\%]$; the price of that consistency is possible arbitrage when the curve is interpolated.

> [!question]- fi-cdx-gaussian-copula-tail-dependence | What is the asymptotic tail dependence coefficient of a bivariate Gaussian copula with correlation $\rho < 1$, and why was this fatal in 2008?
> Zero: $P(U_1 \le u \mid U_2 \le u) \to 0$ as $u \to 0$; at $\rho = 0.3$ it is $0.1427$ at $u = 5\%$ but $0.0149$ at $0.1\%$.
> A model with no clustering of extreme defaults beyond the pairwise correlation understates the probability that losses reach senior layers; the 2008 senior losses also reflected the inputs and the correlated mortgage collateral of ABS CDOs, not the copula alone.

> [!question]- fi-cdx-super-senior-tranche-risk | Why were super-senior CDO tranches [30% - 100%] considered risk-free before 2008, and why did they incur catastrophic losses?
> Losing 30% of a diversified corporate portfolio needs default rates far beyond historical experience, so super seniors were treated as near riskless; corporate index super seniors lost market value as spreads widened, but the heavy realized losses were on super seniors of ABS CDOs.
> Those were backed by subprime mortgage bonds whose defaults were highly correlated through house prices, so the subordination was much thinner in effect than diversification models suggested; UBS's April 2008 report attributes a large share of its write-downs to such positions.

> [!question]- fi-cdx-intrinsic-spread | Why is the intrinsic spread of a CDS index below the simple average of its constituents' spreads?
> The index coupon stream is worth the sum of the constituents' coupon streams, so the matching spread weights each name by its risky annuity, and wide names have shorter annuities (they are likely to default sooner).
> In Example 2 the risky annuity falls from $4.46$ at $40$ bp to $3.88$ at $400$ bp, pulling the intrinsic spread to $139.4$ bp against a $146$ bp simple average.

> [!question]- fi-cdx-lhp-vs-finite-pool | How does a 125-name pool differ from the large homogeneous pool limit for tranche pricing?
> The finite pool keeps idiosyncratic default risk, which makes the loss distribution wider for a given factor value: equity expected loss falls (here $52.14\%$ against $54.11\%$) and senior expected loss rises ($9.21\%$ against $8.78\%$ for $[7\%, 10\%]$).
> Conditional on the factor the default count is binomial, so the exact homogeneous answer is a one-dimensional integral of a binomial sum.

> [!question]- fi-cdx-equity-monotone | Why does equity tranche expected loss fall as correlation rises?
> The equity payoff $\min(L, K)$ is concave in portfolio loss, and higher correlation spreads the loss distribution while keeping its mean $p(1 - R)$ fixed, so the expected value of a concave payoff falls.
> At high correlation the pool more often has no losses at all, which is good for equity, and the bad scenarios lose more than the tranche can absorb.

> [!question]- fi-cdx-upfront-direction | A CDX HY series has a 500 bp coupon and trades at 420 bp. Who pays the upfront and how much on 50 million with RPV01 4.15?
> The protection seller pays the buyer $\$1,660,000$ ($3.32\%$), because the buyer will pay a 500 bp coupon for protection worth 420 bp a year.
> The price quote is $103.32$, above 100 because the index is tighter than its coupon.

> [!question]- fi-cdx-base-corr-implied | Given an equity [0, 3%] expected loss of 50% with p = 5%, R = 40% in the LHP model, what base correlation does the market imply?
> About $0.353$, found by bisection because equity expected loss is strictly decreasing in $\rho$.
> At $\rho = 0.30$ the model gives $54.11\%$ and at $\rho = 0.20$ it gives $62.77\%$, so a lower expected loss needs a higher correlation.

## Further reading

- David X. Li, *On Default Correlation: A Copula Function Approach*, Journal of Fixed Income, 2000.
- Oldrich Vasicek, *The Distribution of Loan Portfolio Value*, Risk, December 2002.
- John Hull and Alan White, *Valuation of a CDO and an n-th to Default CDS Without Monte Carlo Simulation*, Journal of Derivatives, 2004.
- Leif Andersen, Jakob Sidenius, and Susanta Basu, *All Your Hedges in One Basket*, Risk, November 2003.
- Markit, *The CDS Big Bang: Understanding the Changes to the Global CDS Contract and North American Conventions*, March 2009.
- S&P Dow Jones Indices, *Markit CDX HY and IG Rules* (2022) and the *iTraxx Europe and Crossover* rulebook.
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, 3rd edition, Wiley, 2012, chapter 19 (Corporate Bonds and Credit Default Swaps).
- Damiano Brigo and Fabio Mercurio, *Interest Rate Models - Theory and Practice*, 2nd edition, Springer, 2006, section 21.1 (FtD, CDO tranches and copulas).

## In this repo and SDE-Interview-Prep

- Single-name CDS mechanics and hazard rate bootstrapping: [Credit and CDS](06-Credit-and-CDS.md).
- Code: [`code/fi_credit_tranches.py`](code/fi_credit_tranches.py) asserts every number here, with the LHP losses computed two independent ways and the finite pool by conditional binomial.
- Prepayment and mortgage-backed securitizations: [Mortgages and Securitized Products](22-Mortgages-and-Securitized-Products.md).
