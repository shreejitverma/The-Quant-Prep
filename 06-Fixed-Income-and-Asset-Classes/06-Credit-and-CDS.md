---
type: concept
track: [quant-trader, quant-research, quant-risk]
tier: advanced
status: draft
prereqs: [discounting-and-yield-curves]
est_hours: 5
sources: [Dominic OKane - Modelling Single-name and Multi-name Credit Derivatives, Philipp Schonbucher - Credit Derivatives Pricing Models, ISDA Standard CDS Model]
---

# Credit Basics: Hazard Rates and CDS

## TL;DR

Credit risk reflects the probability that a borrower defaults on contractual debt obligations and the resulting loss severity.
Under structural models (Merton 1974), default occurs when firm assets fall below debt liabilities, viewing equity as a call option on firm value.
Under reduced-form models, default is governed by an exogenous Poisson process with intensity or hazard rate $\lambda(t)$, yielding survival probabilities $Q(t) = \exp(-\int_0^t \lambda(s) ds)$.
A Credit Default Swap (CDS) transfers credit risk: the protection buyer pays a periodic coupon (or fixed 100/500 bp coupon plus upfront) and receives par minus recovery from the protection seller upon default.
The credit triangle $\text{Spread} \approx \lambda \times (1 - R)$ provides a foundational mental anchor connecting default probability, recovery rate, and CDS spreads.

## Learning objectives

- Differentiate structural credit models (Merton) from reduced-form intensity models.
- Formulate the Poisson default process and derive survival probabilities from constant and piecewise hazard rates.
- Derive the fair par spread of a single-name CDS by equating the present value of the premium and protection legs.
- Calculate CDS upfront payments, Risky PV01 (RPV01), credit spread sensitivity (CS01), and Jump-to-Default (JTD).
- Apply the credit triangle approximation $s \approx \lambda(1 - R)$ and identify the limits of its validity.
- Explain the post-2009 Big Bang CDS contract standardization and the ISDA auction settlement mechanism.

## Core concepts

### 1. Structural vs Reduced-Form Credit Models

Modern credit modeling divides into two distinct theoretical frameworks.

#### Merton's Structural Model (1974)
Robert Merton modeled a firm whose total asset value $V(t)$ follows geometric Brownian motion under the physical or risk-neutral measure:
$$dV(t) = \mu V(t) dt + \sigma_V V(t) dW(t)$$
The firm is financed by equity $E(t)$ and a single zero-coupon debt obligation with face value $D$ maturing at time $T$.

At maturity $T$:
1. If $V(T) > D$, the firm pays off bondholders in full ($D$), and equity holders receive the residual $V(T) - D$.
2. If $V(T) \le D$, the firm defaults; equity holders walk away with 0 under limited liability, and bondholders seize total firm assets $V(T)$.

Equity is therefore an analytical European call option on firm assets with strike $D$:
$$E(0) = \text{BlackScholesCall}(V(0), D, \sigma_V, T, r)$$
Debt value is $D(0) = V(0) - E(0) = P(0, T) D - \text{BlackScholesPut}(V(0), D, \sigma_V, T, r)$.
The probability of default under the risk-neutral measure is:
$$\mathbb{Q}(\tau \le T) = \Phi(-d_2) = \Phi\left( -\frac{\ln(V(0) / D) + (r - \frac{1}{2}\sigma_V^2)T}{\sigma_V \sqrt{T}} \right)$$
The term $\frac{\ln(V(0) / D) + (\mu - \frac{1}{2}\sigma_V^2)T}{\sigma_V \sqrt{T}}$ is termed the **Distance to Default (DD)**.
While structural models provide deep economic intuition connecting equity volatility to bond spreads, they struggle to reprice short-term credit spreads because Brownian motion paths cannot jump to default unexpectedly over short horizons ($\lim_{T \to 0} \text{Spread}(T) = 0$).

#### Reduced-Form Intensity Models
Reduced-form models treat default as an unpredictable stopping time $\tau$ governed by a jump process with default intensity (hazard rate) $\lambda(t)$.
The internal balance sheet of the firm is unobserved; instead, default is an exogenous surprise event.
Because default can strike unexpectedly at any instant $t > 0$, reduced-form models fit observed short-term credit spreads and are the market standard for pricing and hedging credit derivatives.

### 2. Hazard Rates and Survival Probabilities

Let $\tau$ be the random default time of a reference entity.
The **hazard rate** (or default intensity) $\lambda(t)$ is the instantaneous conditional default probability density given survival up to time $t$:
$$\lambda(t) = \lim_{\Delta t \to 0} \frac{\mathbb{P}(t < \tau \le t + \Delta t \mid \tau > t)}{\Delta t}$$

The cumulative probability of survival $Q(t) = \mathbb{P}(\tau > t)$ satisfies the differential equation:
$$\frac{dQ(t)}{dt} = -\lambda(t) Q(t), \quad Q(0) = 1$$
Integrating yields the survival probability curve:
$$Q(t) = \exp\left( -\int_0^t \lambda(s) ds \right)$$
The cumulative default probability is $F(t) = 1 - Q(t)$.

For a constant hazard rate $\lambda$:
$$Q(t) = e^{-\lambda t}$$
Default time $\tau$ is an exponentially distributed random variable with expected lifetime $\mathbb{E}[\tau] = \frac{1}{\lambda}$.

### 3. Credit Default Swaps (CDS) Mechanics

A Credit Default Swap is a bilateral over-the-counter derivative that provides insurance against default of a reference entity (corporate or sovereign).
1. **Protection Buyer:** Pays a periodic coupon (the CDS spread) on notional $N$ until maturity $T$ or until default occurs.
2. **Protection Seller:** Receives premium payments and agrees to compensate the buyer for default losses if a credit event occurs prior to $T$.

#### Settlement Mechanisms
- **Physical Settlement (Historical):** The buyer delivers defaulted physical bonds with par value $N$ to the seller in exchange for $N$ cash.
- **Cash Settlement via ISDA Auction (Modern):** Since the 2009 Big Bang, nearly all CDS settle via credit event auctions run by Creditex and Markit.
The auction establishes a market-clearing recovery rate $R \in [0, 1]$.
The protection seller pays $(1 - R) \times N$ in cash to the buyer.
For senior unsecured corporate debt, the standard assumed recovery rate is $R = 40\%$ ($0.40$); for sovereign debt, $R = 25\%$ or $40\%$.

### 4. CDS Pricing and Valuation

Consider a CDS with quarterly payment dates $t_1, t_2, \dots, t_n$ ($\Delta t_i \approx 0.25$).
Let $P(0, t)$ be the risk-free discount factor curve and $R$ be the expected recovery rate.
The loss given default is $\text{LGD} = 1 - R$.

#### The Premium Leg (Fee Leg)
The protection buyer pays running spread $s$ at each coupon date if the entity survives.
If default occurs between $t_{i-1}$ and $t_i$, the buyer pays accrued interest up to the default time (modeled as mid-period default):
$$\text{PV}_{\text{premium}}(s) = s \sum_{i=1}^n \Delta t_i P(0, t_i) \left[ Q(t_i) + \frac{1}{2}\left(Q(t_{i-1}) - Q(t_i)\right) \right]$$
The term inside the brackets reflects full coupon payment on survival plus half-coupon accrual on default.
The **Risky PV01 (RPV01)** is the present value of 1 basis point ($0.0001$) running spread per unit notional:
$$\text{RPV01} = \frac{\text{PV}_{\text{premium}}(s)}{s}$$

#### The Protection Leg (Contingent Leg)
Upon default at time $\tau \in (t_{i-1}, t_i]$, the seller pays $1 - R$.
Discretizing into mid-period payouts:
$$\text{PV}_{\text{protection}} = (1 - R) \sum_{i=1}^n P(0, t_{i, \text{mid}}) \left( Q(t_{i-1}) - Q(t_i) \right)$$
where $t_{i, \text{mid}} = 0.5(t_{i-1} + t_i)$.

#### Fair Par Spread
The fair par CDS spread $s^*$ is the contract spread that sets the initial value of the CDS to zero:
$$\text{PV}_{\text{protection}} = \text{PV}_{\text{premium}}(s^*)$$
$$s^* = \frac{\text{PV}_{\text{protection}}}{\text{RPV01}}$$

### 5. Contract Standardization and Upfront Payments

Prior to 2009, CDS contracts were traded at par ($s = s^*$) with zero upfront cash exchange.
This created operational complexity: unwinding trades required bilateral offsetting contracts with differing coupons.

Under the 2009 ISDA Big Bang protocol, all standard single-name CDS trade with fixed standardized coupons:
- **100 bps (1.0%):** Standard for Investment Grade (IG) reference entities.
- **500 bps (5.0%):** Standard for High Yield (HY) reference entities.

Because the fixed coupon $c$ differs from the prevailing market par spread $s^*$, the buyer and seller exchange an **upfront payment** at inception:
$$\text{Upfront Payment} = \text{PV}_{\text{protection}} - c \times \text{RPV01} \approx (s^* - c) \times \text{RPV01}$$
If the market par spread $s^* = 150\text{ bps}$ and the standard coupon is $100\text{ bps}$, the protection buyer pays an upfront fee of approximately $(150 - 100)\text{ bps} \times \text{RPV01} \approx 50\text{ bps} \times 4.3 \approx 2.15\%$ of notional.

### 6. Risk Metrics: CS01 and Jump-to-Default

#### Credit Spread Sensitivity (CS01)
CS01 (or Spread DV01) measures the change in mark-to-market value of a CDS contract for a 1 basis point parallel increase in credit spread:
$$\text{CS01} = \frac{\partial V}{\partial s} \approx \text{RPV01} \times 1\text{ bp}$$
A long protection position has positive CS01 (profits when credit spreads widen).

#### Jump-to-Default (JTD)
JTD measures the instantaneous P&L if the reference entity defaults immediately:
$$\text{JTD}_{\text{buyer}} = (1 - R) - \text{Upfront Paid} - \text{Accrued Coupon}$$
For an unhedged long protection position with $R = 40\%$ and upfront fee $2.0\%$, immediate default yields $+58.0\%$ of notional.

### 7. The Credit Triangle

The credit triangle is a first-order rule of thumb connecting par CDS spread $s$, hazard rate $\lambda$, and recovery rate $R$:
$$\text{Spread} \approx \lambda \times (1 - R)$$
Rearranging yields the market-implied hazard rate:
$$\lambda \approx \frac{\text{Spread}}{1 - R}$$
For example, if a 5-year CDS trades at $150\text{ bps}$ ($0.0150$) with $R = 40\%$ ($\text{LGD} = 0.60$):
$$\lambda \approx \frac{0.0150}{0.60} = 0.0250 = 2.50\% \text{ per year}$$
The 5-year survival probability is approximately $Q(5) \approx e^{-0.025 \times 5} = e^{-0.125} \approx 88.25\%$.

## Worked examples

### Example 1: CDS Hazard Rate Bootstrapping
Let $P(0, t) = e^{-0.04t}$ (flat 4% discount curve) and recovery rate $R = 40\%$.
A desk observes par CDS quotes:
- 1-year: $100\text{ bps}$ ($0.0100$)
- 3-year: $120\text{ bps}$ ($0.0120$)
- 5-year: $150\text{ bps}$ ($0.0150$)

Using our reference implementation [`credit_bootstrap.py`](code/credit_bootstrap.py):
1. **1-Year Hazard Rate:** Bootstrapped $\lambda_1 = 0.0166$ ($1.66\%$).
2. **5-Year Cumulative Survival:** $Q(5.0) = 88.04\%$.
3. **5-Year RPV01:** $\text{RPV01} = 4.28$.
4. **5-Year Upfront Fee on 100 bp standard coupon:**
$$\text{Upfront} = \text{PV}_{\text{protection}} - 0.0100 \times \text{RPV01} = 0.0642 - 0.0428 = 0.0214 \quad (2.14\% \text{ of notional})$$
Buying 5-year protection on $\$10\text{ million}$ notional requires paying an upfront cash fee of $\$214,000$ plus $100\text{ bps}$ per annum quarterly.

### Example 2: CDS-Bond Basis Arbitrage
A 5-year senior unsecured corporate bond trades at a yield of $5.80\%$, while the 5-year benchmark swap rate is $4.00\%$, implying a bond Z-spread of $180\text{ bps}$.
The 5-year single-name CDS on the same corporate entity trades at $150\text{ bps}$.

Calculate the CDS-bond basis:
$$\text{Basis} = \text{CDS Spread} - \text{Bond Z-Spread} = 150\text{ bps} - 180\text{ bps} = -30\text{ bps}$$
The basis is negative ($-30\text{ bps}$).
A negative basis indicates that the cash bond is trading cheap relative to the synthetic CDS market.
A relative value desk executes a **negative basis trade**:
1. Buy the physical corporate bond yielding $5.80\%$.
2. Finance the bond in the repo market at $\text{SOFR} + 20\text{ bps} = 4.20\%$.
3. Buy CDS protection at $150\text{ bps}$.
Net carry:
$$\text{Net Spread} = 180\text{ bps (bond spread)} - 150\text{ bps (CDS cost)} - 20\text{ bps (repo haircut)} = +10\text{ bps}$$
The desk locks in positive net carry with default risk hedged by the CDS.

### Example 3: Jump-to-Default and Delta Sizing
A credit hedge fund is long $\$50\text{ million}$ of a distressed bond trading at $70$ cents on the dollar ($P = 70$).
The recovery rate in bankruptcy is expected to be $R = 40\%$.
How much CDS protection must the fund buy to immunize against immediate jump-to-default?

If default occurs immediately:
- The bond drops from $70$ to $40$, creating a loss of $\$30$ per $\$100$ face value:
$$\text{Bond Loss} = \$50\text{M} \times (0.70 - 0.40) = \$15\text{ million}$$
- A CDS protection contract delivers $(1 - R) = 60\%$ on notional $N_{\text{CDS}}$:
$$\text{CDS Payout} = N_{\text{CDS}} \times 0.60$$
Equating bond loss to CDS payout:
$$N_{\text{CDS}} \times 0.60 = \$15\text{ million} \implies N_{\text{CDS}} = \frac{\$15\text{M}}{0.60} = \$25\text{ million}$$
The fund requires $\$25\text{ million}$ of CDS notional to hedge jump-to-default risk, half of the physical bond par value.

## Pitfalls

- **Confusing physical recovery with CDS auction recovery:** CDS recovery is determined by a 2-stage credit event auction; if deliverable bond supply is scarce, the auction price can clear significantly above fair fundamental liquidation value, reducing CDS payouts.
- **Neglecting accrued interest on default:** Omitting the accrued coupon payment paid by the protection buyer upon mid-period default causes an error in fair par spread of 2 to 5 bps.
- **Assuming constant recovery across credit cycles:** Recovery rates are procyclical; during recessions and systemic crises, realized recovery rates collapse from 40% to 15-20%, causing protection buyers to experience unhedged shortfall.
- **Using Merton models for short-dated credit spreads:** Structural diffusion models predict zero default probability over short horizons; attempting to force Merton to match 6-month spreads requires unrealistically high asset volatility.
- **Mismatch in CDS vs bond documentation:** Seniority, restructuring clauses (e.g. Modified Restructuring Mod-R vs No Restructuring XR), and entity succession events can cause a CDS contract not to trigger on bond debt renegotiation.

## Interview questions

> [!question]- fi-credit-cds-triangle | What is the credit triangle and what does it approximate?
> $\text{Spread} \approx \lambda \times (1 - R)$.
> It approximates the fair CDS par spread as the product of the hazard rate (annual default intensity) $\lambda$ and the loss given default $\text{LGD} = 1 - R$.

> [!question]- fi-credit-cds-merton-shortcoming | Why does Merton's structural model fail to explain short-term credit spreads?
> Asset values follow continuous diffusion paths with no jumps.
> Over a short horizon $T \to 0$, the probability that asset value drops from $V_0 > D$ below default barrier $D$ approaches zero faster than $T$, forcing short-term credit spreads to zero, whereas real-world short spreads are positive.

> [!question]- fi-credit-cds-upfront-formula | How is the upfront fee of a standardized CDS calculated?
> $\text{Upfront} = \text{PV}_{\text{protection}} - c \times \text{RPV01} \approx (s^* - c) \times \text{RPV01}$.
> It equals the difference between the market par spread $s^*$ and the standardized contract coupon $c$ (100 bps or 500 bps), multiplied by the risky PV01.

> [!question]- fi-credit-cds-rpv01-definition | Define Risky PV01 (RPV01) in CDS contracts.
> RPV01 is the present value of 1 basis point ($0.0001$) running spread paid periodically over the life of the trade, conditional on survival and incorporating accrued interest paid on default.

> [!question]- fi-credit-cds-cs01-vs-dv01 | Contrast CS01 and interest rate DV01 for a CDS contract.
> DV01 measures price sensitivity to a parallel shift in the risk-free discount curve $P(0, t)$.
> CS01 measures price sensitivity to a 1 bp increase in the reference entity's credit spread (hazard rate).

> [!question]- fi-credit-cds-negative-basis | What is the CDS-bond basis and what does a negative basis indicate?
> $\text{Basis} = \text{CDS Spread} - \text{Bond Z-Spread}$.
> A negative basis means the bond spread exceeds the CDS spread, indicating that the cash bond trades cheap relative to the synthetic CDS market, presenting a negative basis trade opportunity.

> [!question]- fi-credit-cds-restructuring-clauses | What are the common restructuring clauses in CDS documentation?
> Full Restructuring (CR), Modified Restructuring (MR / Mod-R, common in US IG), Modified-Modified Restructuring (MMR / Mod-Mod-R, common in Europe), and No Restructuring (XR, standard in North America CDX).

> [!question]- fi-credit-cds-auction-settlement | How does the ISDA credit event auction establish cash settlement?
> The auction aggregates physical orders to buy and sell deliverable bonds and establishes a single market-clearing price $R$.
> Cash settlement pays $(1 - R)$ without requiring physical delivery of certificates, preventing delivery short squeezes.

> [!question]- fi-credit-cds-jtd-formula | Write the formula for Jump-to-Default for a protection buyer.
> $\text{JTD} = (1 - R) - \text{Upfront Paid} - \text{Accrued Coupon}$.
> It represents the net cash received if the reference entity files for bankruptcy today.

> [!question]- fi-credit-cds-hazard-rate-shape | What does an inverted hazard rate curve indicate?
> An inverted hazard rate curve (short-term spreads higher than long-term spreads) indicates severe near-term distress or imminent liquidity crisis, as market participants price immediate default probability higher than long-term survival.

## Further reading

- Dominic O'Kane, *Modelling Single-name and Multi-name Credit Derivatives*, John Wiley & Sons, 2008.
- Philipp Schönbucher, *Credit Derivatives Pricing Models: Models, Pricing and Implementation*, Wiley Finance, 2003.
- Robert Merton, *On the Pricing of Corporate Debt: The Risk Structure of Interest Rates*, The Journal of Finance, 1974.
- Markit, *ISDA Standard CDS Model Documentation*, 2009.

## In this repo and SDE-Interview-Prep

- Code: [`code/credit_bootstrap.py`](code/credit_bootstrap.py) (Hazard rate bootstrap, upfront fee, RPV01, and CS01).
- Prereq: [Discounting and Yield Curves](01-Discounting-and-Yield-Curves.md).
- Next: [Credit Advanced: CDS Indices and Tranches](23-Credit-Advanced-CDS-Indices-and-Tranches.md).
