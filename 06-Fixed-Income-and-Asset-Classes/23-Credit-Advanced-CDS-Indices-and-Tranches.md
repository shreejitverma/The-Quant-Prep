---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: draft
prereqs: [credit-and-cds]
est_hours: 5
sources: [David X. Li - On Default Correlation A Copula Approach (2000), John Hull and Alan White - Valuation of a CDO and an n-th to Default CDS Without Monte Carlo Simulation (2004), Bruce Tuckman and Angel Serrat - Fixed Income Securities chapter 19, Darrell Duffie and Kenneth J. Singleton - Credit Risk Pricing Measurement and Management]
---

# Credit Advanced: CDS Indices and Tranches

## TL;DR

Credit default swap (CDS) indices such as CDX and iTraxx pool liquid single-name CDS contracts into standardized, roll-traded baskets with fixed coupons and upfront exchange.
Synthetic Collateralized Debt Obligations (CDOs) segment the loss distribution of these portfolios into prioritized tranches defined by attachment and detachment points.
Pricing multi-name credit derivatives requires modeling default correlation, historically pioneered by David Li's one-factor Gaussian copula.
Under the Large Homogeneous Portfolio (LHP) approximation, the portfolio loss distribution is expressed analytically conditioned on a systemic market factor.
However, market pricing revealed a severe correlation skew across tranches, leading from non-monotonic compound correlation to monotonic base correlation curves.
The 2008 financial crisis exposed catastrophic vulnerabilities in the Gaussian copula: thin-tailed normal distributions fail to capture tail dependence, causing systemic simultaneous defaults and wiping out tranches rated triple-A.

## Learning objectives

- Master CDX (North America) and iTraxx (Europe/Asia) index construction, rolling conventions, and upfront quoting mechanics.
- Formulate the CDS index basis ($S_{\text{index}} - \frac{1}{N}\sum S_i$) and identify its structural, liquidity, and dispersion drivers.
- Structure standardized synthetic CDO tranches across equity, junior mezzanine, senior mezzanine, senior, and super-senior layers.
- Derive the one-factor Gaussian copula model and the conditional default probability under systemic market factor realizations.
- Compute expected tranche losses using numerical integration over the portfolio loss distribution.
- Contrast compound correlation against base correlation, explaining why compound correlation fails for mezzanine tranches.
- Analyze the theoretical failure modes of the Gaussian copula in 2008, specifically zero asymptotic tail dependence and systemic contagion.

## Core concepts

### CDS Indices: CDX and iTraxx

A Credit Default Swap index represents a standardized, equally weighted portfolio of liquid single-name CDS contracts.
Indices trade over the counter under standardized ISDA rules, providing liquidity for hedging aggregate corporate credit risk.
The two dominant families are CDX and iTraxx:

- **CDX (North America and Emerging Markets):** Includes CDX North American Investment Grade (CDX NA IG, 125 investment grade entities) and CDX North American High Yield (CDX NA HY, 100 liquid high yield entities).
- **iTraxx (Europe and Asia-Pacific):** Includes iTraxx Europe (125 liquid European investment grade entities), iTraxx Crossover (75 sub-investment grade entities), and iTraxx Europe Subordinated Financials.

Indices roll semi-annually on March 20 and September 20 into a new on-the-run series.
A credit ratings and liquidity committee evaluates dealer volume to select constituent names.
Entities that suffer credit downgrades, mergers, or insolvencies are removed in the upcoming roll.
Off-the-run series continue trading until their original maturity (typically 3, 5, 7, or 10 years, with 5-year contracts commanding the highest liquidity).
If a constituent entity triggers a credit event during the index life, the entity is removed from the index.
The protection seller settles the single-name recovery payment for $1/N$ of the original notional, and the ongoing index notional reduces to $(N - 1)/N$.

### Index Quoting and Standard Coupons

Under post-2009 "Big Bang" conventions, CDS indices trade with standardized fixed coupons:
- Investment Grade indices (CDX IG, iTraxx Europe) trade at a fixed coupon of 100 basis points (1.00% per annum).
- High Yield and Crossover indices (CDX HY, iTraxx Crossover) trade at a fixed coupon of 500 basis points (5.00% per annum).

Market participants exchange an upfront fee at inception to reconcile the fixed running coupon with the market par spread $S_{\text{index}}$:

$$\text{Upfront Fee (\% of Notional)} \approx (S_{\text{index}} - C) \times \text{RPV01}_{\text{index}}$$

where $C$ is the standard fixed coupon and $\text{RPV01}_{\text{index}}$ is the risky present value of a basis point on the index survival annuity.
For CDX HY, prices are quoted on a dollar price convention:

$$\text{Dollar Price} = 100 - \text{Upfront Fee (\% of Notional)}$$

When credit risk rises, par spread expands above coupon, upfront fee becomes positive (paid by protection buyer to seller), and dollar price drops below 100.

### The CDS Index Basis

The index basis is the difference between the traded index par spread and the intrinsic weighted average par spread of the underlying single-name components:

$$\text{Basis} = S_{\text{index}} - \frac{1}{N}\sum_{i=1}^N S_i$$

In a frictionless market with zero arbitrage, the basis would equal zero.
In reality, the basis fluctuates significantly due to several structural factors:

- **Liquidity premium:** The index is substantially more liquid and centrally cleared than single names, often causing the index to trade at a tighter spread (negative basis).
- **Dispersion and convexity:** The relationship between CDS spread and default probability is non-linear; the average of non-linear survival functions does not equal the survival function of the average spread.
- **Funding and counterparty constraints:** Arbitrageurs executing basis trades (buying index protection and selling single-name protection, or vice versa) incur capital charges, bilateral collateral haircuts, and roll execution costs.
- **Default skew and jump-to-default:** Single-name CDS positions carry jump-to-default idiosyncratic risk that cannot be perfectly cross-hedged against an index without constant rebalancing.

### Synthetic CDO Tranche Architecture

A Synthetic Collateralized Debt Obligation (synthetic CDO) slices the credit loss distribution of a reference portfolio into prioritized risk tranches.
Each tranche is defined by an attachment point $A$ and a detachment point $D$ as a percentage of total portfolio notional:

$$\text{Tranche Notional} = (D - A) \times N_{\text{portfolio}}$$

Standardized 5-year tranche structures on CDX IG and iTraxx Europe:
- **Equity Tranche [0% - 3%]:** Absorbs the first 3% of cumulative portfolio defaults. Suffers the highest loss risk and commands upfront running fees.
- **Junior Mezzanine Tranche [3% - 7%]:** Absorbs losses between 3% and 7%.
- **Senior Mezzanine Tranche [7% - 10%]:** Absorbs losses between 7% and 10%.
- **Senior Tranche [10% - 15%] (or [15% - 30%]):** Absorbs losses above 10% (or 15%).
- **Super Senior Tranche [30% - 100%]:** Absorbs extreme tail losses.

If cumulative portfolio credit loss at time $t$ is $L(t)$ expressed as a fraction of portfolio initial notional, the cumulative loss absorbed by tranche $[A, D]$ is:

$$L_{[A, D]}(t) = \frac{\min(D, \max(A, L(t))) - A}{D - A}$$

The tranche protection seller receives a running tranche spread (plus any upfront fee) on the remaining tranche notional:

$$\text{Remaining Tranche Notional}(t) = 1 - L_{[A, D]}(t)$$

In return, the protection seller compensates the buyer for incremental losses $\Delta L_{[A, D]}(t)$ as they occur.

### One-Factor Gaussian Copula Model (Li 2000)

David Li proposed using copula functions to model joint default times without restricting marginal default distributions.
Marginal default probabilities $p_i(t) = P(\tau_i \le t)$ are calibrated directly to liquid market CDS curves.
To introduce default correlation, each firm $i$ is assigned a standardized latent credit variable $X_i$:

$$X_i = \sqrt{\rho_i} M + \sqrt{1 - \rho_i} Z_i$$

where:
- $M \sim \mathcal{N}(0, 1)$ is the common systemic market factor driving macro-economic conditions.
- $Z_i \sim \mathcal{N}(0, 1)$ is the idiosyncratic shock specific to firm $i$, mutually independent of $M$ and all other $Z_j$.
- $\rho_i \in [0, 1)$ is the asset correlation to the market factor (often assumed homogeneous, $\rho_i = \rho$).

Firm $i$ defaults prior to time $t$ if its latent variable falls below a default threshold $c_i(t)$:

$$\tau_i \le t \iff X_i \le c_i(t) \quad \text{where} \quad c_i(t) = \Phi^{-1}(p_i(t))$$

Conditioned on a realization of the market factor $M=m$, defaults across firms become mutually independent:

$$p_i(t \mid M=m) = P(X_i \le c_i(t) \mid M=m) = P\left(Z_i \le \frac{\Phi^{-1}(p_i(t)) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right) = \Phi\left(\frac{\Phi^{-1}(p_i(t)) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right)$$

### Large Homogeneous Portfolio (LHP) Approximation

When the reference portfolio consists of $N \to \infty$ identical credits with identical default probabilities $p(t)$, correlation $\rho$, and loss given default $LGD = (1 - R)$:
By the Law of Large Numbers, conditioned on $M=m$, the portfolio credit loss fraction $L(t \mid M=m)$ converges almost surely to its conditional expectation:

$$L(t \mid M=m) = (1 - R) \cdot p(t \mid M=m) = (1 - R) \cdot \Phi\left(\frac{\Phi^{-1}(p(t)) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right)$$

Because $p(t \mid M=m)$ is strictly decreasing in $m$, the unconditional cumulative distribution function of portfolio loss $F_L(x) = P(L(t) \le x)$ is obtained analytically (the Vasicek distribution):

$$F_L(x) = \Phi\left(\frac{\sqrt{1 - \rho} \Phi^{-1}\left(\frac{x}{1 - R}\right) - \Phi^{-1}(p(t))}{\sqrt{\rho}}\right)$$

The expected loss of any tranche $[A, D]$ can be evaluated by direct numerical quadrature across the systemic factor $m \sim \mathcal{N}(0, 1)$:

$$\mathbb{E}[L_{[A, D]}(t)] = \int_{-\infty}^{\infty} L_{[A, D]}(t \mid M=m) \phi(m) \, dm$$

### Implied Correlation: Compound vs. Base Correlation

Similar to Black-Scholes implied volatility, dealers back out the implied correlation $\rho$ that reconciles the Gaussian copula model with the market price of each tranche.
This revealed two fundamental pricing frameworks:

#### 1. Compound Correlation (Tranche-Specific)
Compound correlation is the single correlation parameter $\rho_{[A, D]}$ that prices tranche $[A, D]$ to its market spread.
However, compound correlation suffers from fatal mathematical limitations:
- **Non-monotonicity:** Mezzanine tranche value is non-monotonic with respect to correlation. When correlation is near zero, defaults are dispersed and mezzanine tranches avoid losses. When correlation is near one, all firms default together or not at all, so losses jump straight to equity or pass to super senior.
- **Multiple roots or non-existence:** A market mezzanine quote frequently corresponds to two valid implied correlations or none at all.
- **Inability to price bespoke tranches:** Off-market detachment points cannot be priced using compound correlation.

#### 2. Base Correlation (Standard Market Convention)
Base correlation resolves the shortcomings of compound correlation by defining every tranche relative to a zero attachment point $[0, K]$ (equity tranches):
Any intermediate tranche $[A, D]$ is decomposed as the difference between two base tranches:

$$\text{Loss}_{[A, D]}(t) = \frac{(D) \cdot \text{Loss}_{[0, D]}(t) - (A) \cdot \text{Loss}_{[0, A]}(t)}{D - A}$$

Base correlation $\rho(K)$ is the correlation of the equity tranche $[0, K]$.
Because the value of an equity tranche is strictly monotonically decreasing with respect to correlation (higher correlation pushes defaults into extreme tails, protecting equity), the base correlation is unique and always exists.
Plotting base correlation $\rho(K)$ against strike $K$ produces the **correlation skew** (or correlation smile), proving that a single flat correlation cannot fit market prices across tranches.

### The 2008 Crisis and the Copula Breakdown

In the 2008 global financial crisis, synthetic CDOs of subprime asset-backed securities (CDO-squared) collapsed catastrophically.
Senior and super-senior tranches rated AAA suffered near-total write-downs.
The failure was rooted in core mathematical flaws of the Gaussian copula:

1. **Zero Asymptotic Tail Dependence:** The Gaussian copula exhibits zero asymptotic tail dependence in extreme limits:

$$\lambda_L = \lim_{u \to 0} P(U_1 < u \mid U_2 < u) = 0 \quad (\text{for } \rho < 1)$$

Under a normal copula, the probability of joint extreme events decays exponentially to zero.
In credit panics, defaults are clustered, requiring copulas with positive lower tail dependence (such as the Student-t copula or Clayton copula).

2. **Static Calibration to Benign Data:** Tranche models were calibrated to short historical time series (2003-2006) during which US housing prices had never experienced nationwide simultaneous declines.
Implied correlations reflected benign market liquidity rather than systemic structural contagion.

3. **Ratings Arbitrage and CDO-Squared:** Financial engineers bundled BBB-rated subprime mortgage tranches into secondary CDO vehicles.
Relying on the Gaussian copula's diversification assumptions, rating agencies assigned AAA ratings to 75%+ of the resulting capital structure, concentrating immense tail risk into unregulated balance sheets.

## Worked examples

### Example 1: CDS Index Upfront and Dollar Price Calculation

A portfolio manager buys $50,000,000 notional of CDX NA HY 5-year protection.
The index has a standard fixed coupon of 500 bps (0.0500).
The current traded par spread of the index is 420 bps (0.0420).
The risky present value of a basis point on the index is $\text{RPV01} = 4.15$.

**Step 1: Compute the upfront fee as a fraction of notional:**

$$\text{Upfront Fraction} \approx (S_{\text{index}} - C) \times \text{RPV01} = (0.0420 - 0.0500) \times 4.15 = -0.0080 \times 4.15 = -0.0332 \quad (-3.32\%)$$

**Step 2: Determine cash flow direction:**
Because market spread (420 bps) is tighter than the fixed running coupon (500 bps), the protection buyer is overpaying on running payments.
Therefore, the protection seller pays an upfront fee of $3.32\%$ to the protection buyer at trade inception.

$$\text{Upfront Cash} = -0.0332 \times \$50,000,000 = -\$1,660,000 \quad (\text{received by buyer})$$

**Step 3: Compute the quoted dollar price:**

$$\text{Dollar Price} = 100 - \text{Upfront (\%)} = 100 - (-3.32) = 103.32$$

### Example 2: One-Factor Gaussian Copula Tranche Pricing

Consider a portfolio with default probability $p = 0.05$ over 5 years, recovery rate $R = 0.40$ ($LGD = 0.60$), and correlation $\rho = 0.30$.
Using the reference implementation in `code/credit_bootstrap.py`, evaluate the default probability under systemic market stress and compute tranche expected losses.

**Step 1: Compute the default threshold:**

$$c = \Phi^{-1}(0.05) \approx -1.6449$$

**Step 2: Evaluate conditional default probability under severe systemic shock ($M = -2.5$ standard deviations):**

$$p(M = -2.5) = \Phi\left(\frac{-1.6449 - \sqrt{0.30} \times (-2.5)}{\sqrt{1 - 0.30}}\right) = \Phi\left(\frac{-1.6449 + 1.3693}{\sqrt{0.70}}\right) = \Phi\left(\frac{-0.2756}{0.8367}\right) = \Phi(-0.3294) \approx 0.3709 \quad (37.09\%)$$

Under a 2.5-sigma market crash, the conditional default probability spikes from 5.0% to 37.1%.
Conditional portfolio loss is:

$$L(M = -2.5) = 0.60 \times 0.3709 = 0.2225 \quad (22.25\%)$$

**Step 3: Calculate tranche losses for Equity [0-3%] and Senior [7-10%] under this realization:**
- For Equity [0%, 3%]: Portfolio loss (22.25%) exceeds detachment (3%), so equity tranche is completely wiped out ($100\%$ loss).
- For Senior [7%, 10%]: Portfolio loss (22.25%) exceeds detachment (10%), so senior tranche is completely wiped out ($100\%$ loss).

**Step 4: Unconditional tranche expected losses (from the large homogeneous portfolio quadrature in `credit_bootstrap.py`):**
- Total expected portfolio loss: $\mathbb{E}[L] = p \times (1 - R) = 0.05 \times 0.60 = 3.00\%$.
- Equity tranche [0%, 3%] expected loss: $54.08\%$.
- Senior tranche [7%, 10%] expected loss: $8.67\%$.

## Pitfalls

- **Confusing Compound and Base Correlation:** Quoting a single "implied correlation" for a mezzanine tranche without specifying the base correlation method leads to severe ambiguity or non-invertible model states.
- **Ignoring Credit Event Removal:** When an index constituent defaults, its notional is settled and removed; continuing to model the index on full $100\%$ initial notional miscalculates subsequent running coupon cash flows.
- **Assuming Tail Independence in Crisis Scenarios:** Relying on the Gaussian copula for super-senior tranches severely underestimates joint default clustering.
- **Neglecting Upfront Payment Financing in Basis Trades:** An index basis trade requires paying or receiving large upfront cash balances that incur interest rate and collateral carry costs.
- **Homogeneous Portfolio Fallacy in Concentrated Portfolios:** Applying the Large Homogeneous Portfolio (LHP) analytical formula to a basket with fewer than 50 names or highly skewed notionals understates idiosyncratic concentration risk.

## Interview questions

> [!question]- fi-cdx-itraxx-composition | What are the differences between CDX and iTraxx indices regarding constituent count, geography, and standard roll dates?
> CDX covers North American corporate issuers (CDX NA IG has 125 investment grade names; CDX NA HY has 100 high yield names), while iTraxx covers European and Asian issuers (iTraxx Europe has 125 investment grade names; iTraxx Crossover has 75 sub-investment grade names). Both families roll semi-annually on March 20 and September 20 into a new on-the-run series.

> [!question]- fi-cdx-standard-cds-coupons | Why did CDS indices adopt standardized fixed coupons of 100 bps and 500 bps, and how are market differences settled?
> Standardized coupons were introduced in the 2009 "Big Bang" protocol to facilitate central clearing, fungibility, and liquid multilateral netting. Because running coupons are fixed at 100 bps (for IG) or 500 bps (for HY), any difference with the prevailing market par spread is settled via an upfront cash fee at trade inception approximately equal to $(S_{\text{index}} - C) \times \text{RPV01}$.

> [!question]- fi-cdx-credit-index-basis | Define the CDS index basis and explain why an index often trades tighter than the weighted sum of its single-name components.
> The index basis is $S_{\text{index}} - \frac{1}{N}\sum_{i=1}^N S_i$. The basis is frequently negative because the index provides superior liquidity, lower bid-ask spreads, and streamlined clearing compared to single names. Investors accept a lower spread on the index for instant portfolio diversification and lower transaction costs.

> [!question]- fi-cdx-default-event-index-settlement | What happens to a CDS index when one of its constituent reference entities declares bankruptcy?
> When a credit event occurs, an auction determines the final recovery price $R$ for the defaulted firm. The protection seller pays $(1 - R) \times \frac{1}{N}$ of the original index notional to the protection buyer. The defaulted entity is subsequently removed from the index, and the ongoing running coupon is paid on the reduced notional $(N - 1)/N$.

> [!question]- fi-cdx-one-factor-copula-formulation | In David Li's one-factor Gaussian copula model, explain how the latent variable $X_i = \sqrt{\rho} M + \sqrt{1 - \rho} Z_i$ induces correlation while preserving marginal distributions.
> The latent variables $X_i$ follow standard normal distributions $\mathcal{N}(0, 1)$ because $M$ and $Z_i$ are independent standard normal variables with variance $(\sqrt{\rho})^2 + (\sqrt{1 - \rho})^2 = \rho + (1 - \rho) = 1$. The correlation between any two distinct firms $i$ and $j$ is $\text{Cov}(X_i, X_j) = \rho$. The marginal default probability $p_i(t)$ is preserved by setting the default threshold to $c_i = \Phi^{-1}(p_i(t))$.

> [!question]- fi-cdx-lhp-approximation-vasicek | How does the Large Homogeneous Portfolio (LHP) approximation simplify portfolio loss modeling under the Gaussian copula?
> Under the LHP approximation, as the number of credits $N \to \infty$ with identical default probability $p$ and correlation $\rho$, the idiosyncratic shocks $Z_i$ diversify away completely conditional on the systemic factor $M$. By the Law of Large Numbers, the conditional portfolio loss becomes deterministic: $L(M=m) = (1 - R) \Phi\left(\frac{\Phi^{-1}(p) - \sqrt{\rho} m}{\sqrt{1 - \rho}}\right)$, enabling fast numerical integration without Monte Carlo simulation.

> [!question]- fi-cdx-compound-correlation-deficiency | Why does compound correlation fail as a robust pricing metric for synthetic CDO mezzanine tranches?
> Compound correlation is the implied correlation that matches the price of an isolated tranche $[A, D]$. For mezzanine tranches, the expected tranche loss is non-monotonic with respect to correlation: both very low correlation (defaults contained in equity) and very high correlation (few defaults or entire portfolio defaults) can produce identical expected losses for intermediate mezzanine layers. This produces non-unique dual solutions or instances where no real correlation root exists.

> [!question]- fi-cdx-base-correlation-concept | Explain how the base correlation curve resolves the non-monotonicity problem of compound correlation.
> Base correlation defines correlation exclusively for equity tranches $[0, K]$. Because the value of an equity tranche is strictly monotonically decreasing with respect to correlation, every base correlation is unique and guaranteed to exist. Any intermediate tranche $[A, D]$ is priced consistently as the difference between two base tranches $[0, D]$ and $[0, A]$.

> [!question]- fi-cdx-gaussian-copula-tail-dependence | What is the asymptotic tail dependence coefficient of a bivariate Gaussian copula with correlation $\rho < 1$, and why was this fatal in 2008?
> The lower tail dependence coefficient is zero: $\lim_{u \to 0} P(U_1 < u \mid U_2 < u) = 0$. In extreme negative events, the Gaussian copula treats defaults as asymptotically independent. In reality, credit defaults cluster severely during economic stress. The model therefore drastically underpredicted the simultaneous default of multiple senior assets, leading to severe underpricing of CDO tail risk.

> [!question]- fi-cdx-super-senior-tranche-risk | Why were super-senior CDO tranches [30% - 100%] considered risk-free before 2008, and why did they incur catastrophic losses?
> Super-senior tranches required cumulative portfolio credit losses to exceed 30% before absorbing any loss, which had never occurred in historical corporate portfolios. However, when applied to CDO-squared structures backed by subprime mezzanine mortgage paper, underlying default correlations converged toward 1 during the nationwide housing crash, completely breaching subordination buffers and wiping out super-senior tranches.

## Further reading

- David X. Li (2000), "On Default Correlation: A Copula Approach", *Journal of Fixed Income*.
- John Hull and Alan White (2004), "Valuation of a CDO and an n-th to Default CDS Without Monte Carlo Simulation", *Journal of Derivatives*.
- Bruce Tuckman and Angel Serrat, *Fixed Income Securities: Tools for Today's Markets*, Chapter 19: "Credit Default Swaps".
- Markit (2009), "The CDS Big Bang: Understanding the Changes to the Global CDS Contract and Market Conventions".
- Oldrich Vasicek (2002), "The Distribution of Loan Portfolio Value", *Risk*.

## In this repo and SDE-Interview-Prep

- Single-name CDS mechanics and hazard rate bootstrapping: [Credit and CDS](06-Credit-and-CDS.md).
- Reference implementation of Gaussian copula and synthetic CDO tranche losses: [credit_bootstrap.py](code/credit_bootstrap.py).
- Prepayment and mortgage-backed securitizations: [Mortgages and Securitized Products](22-Mortgages-and-Securitized-Products.md).
