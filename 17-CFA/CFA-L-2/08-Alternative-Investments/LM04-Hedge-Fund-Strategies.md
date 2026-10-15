---
type: cfa-lm
topic: "Alternative Investments"
topic_code: "08"
topic_slug: "08-Alternative-Investments"
volume: 8
lm: 4
title: "Hedge Fund Strategies"
pages: "165-266"
weight_band: "5-10%"
difficulty: 3
los_count: 9
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/alternative-investments]
---

# LM4: Hedge Fund Strategies

Difficulty 3 of 5: the arithmetic (merger-arb payoffs, convertible conversion prices, layered fees, conditional betas) is short, but the module packs six strategy families with near-identical "risk, liquidity, leverage, benchmarking" scaffolding, so the exam risk is matching a vignette to the right strategy, the right leverage level, and the right crisis behavior without mixing the families up.

## LOS map

- **discuss** how hedge fund strategies may be classified (V8 p.165, p.168) ^los-08-04-a
    - Examiner asks: classify a described fund into equity, event-driven, relative value, opportunistic, specialist, or multi-manager, or identify the three taxonomy criteria (instruments, trading philosophy, risk types) a data vendor combines.
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of equity-related hedge fund strategies (V8 p.165, p.171) ^los-08-04-b
    - Examiner asks: size a beta-weighted pairs trade (short leg = long value divided by the beta ratio), or match net exposure bands (L/S 40-60% net long, dedicated short 60-120% short, short-biased 30-60% net short, EMN near zero with high leverage).
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of event-driven hedge fund strategies (V8 p.165, p.183) ^los-08-04-c
    - Examiner asks: compute the stock-for-stock merger-arb payoff on success (the spread) and on failure (prices revert to pre-announcement), and recognize the profile as riskless bond plus short put.
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of relative value hedge fund strategies (V8 p.165, p.191) ^los-08-04-d
    - Examiner asks: identify an off-the-run vs on-the-run duration-matched government trade as a carry trade exposed mainly to liquidity risk, or work the convertible arbitrage setup (conversion price = bond price / conversion ratio, locked-in profit = share price minus conversion price).
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of opportunistic hedge fund strategies (V8 p.165, p.200) ^los-08-04-e
    - Examiner asks: distinguish time-series momentum (absolute signals, can be net long or short everything) from cross-sectional momentum (relative ranking, roughly market neutral), and global macro (discretionary, anticipatory) from managed futures (systematic).
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of specialist hedge fund strategies (V8 p.165, p.208) ^los-08-04-f
    - Examiner asks: pick the volatility implementation matching a stated need (exchange options, OTC options, VIX futures, variance or volatility swaps), or spot the wrong life-settlement characteristic (the trap says high surrender value or death when actuarially predicted).
- **discuss** investment characteristics, strategy implementation, and role in a portfolio of multi-manager hedge fund strategies (V8 p.165, p.215) ^los-08-04-g
    - Examiner asks: compute the double-layered net-of-fee return of a fund-of-funds investor including fee netting risk, or pick multi-strategy vs FoF given stated preferences on fees, transparency, tactical speed, and operational risk.
- **describe** how factor models may be used to understand hedge fund risk exposures (V8 p.165, p.222) ^los-08-04-h
    - Examiner asks: interpret a conditional linear factor model table, adding the incremental crisis beta (D factor) to the normal beta to get total crisis exposure, and explain what a significant negative DVIX loading means.
- **evaluate** the impact of an allocation to a hedge fund strategy in a traditional investment portfolio (V8 p.165, p.235) ^los-08-04-i
    - Examiner asks: from a table of Sharpe, Sortino, standard deviation, and maximum drawdown for combined 48/32/20 (or similar) portfolios, select the strategy that best fits the committee's stated considerations, using Sortino when large negative events matter.

## Core intuition

A hedge fund is defined less by what it buys than by what it is allowed to do.
Seven characteristics separate hedge funds from traditional funds: light legal and regulatory constraints, flexible mandates, a large investment universe, aggressive investment styles, liberal use of leverage, liquidity constraints on investors (lock-ups, gates, exit windows), and high fee structures with management plus incentive fees (V8 p.167, p.168).
Those liquidity constraints are not just friction; they are the source of an illiquidity premium.
Privately placed hedge funds outperform similar-strategy liquid alts by roughly 100 bps to 200 bps per year, because a manager who cannot be redeemed daily can hold positions a mutual fund format cannot (V8 p.168, p.166).
Liquid alts offer daily liquidity, transparency, lower fees, and no incentive fees in most countries, and they underperform for exactly those reasons (V8 p.166, p.167).

Classification is a taxonomy problem, and the curriculum's answer is a six-bucket, practice-based risk factor grouping: equity, event-driven, relative value, opportunistic, specialist, and multi-manager (V8 p.170).
Vendors (HFR, Lipper, Morningstar CISDM, Eurekahedge, Credit Suisse) each slice differently using combinations of instruments, trading philosophy (systematic vs discretionary), and risk types (directional, event driven, relative value); fewer than 1% of managers report to all providers, so no index is all-encompassing (V8 p.168, p.169, p.170).
Index construction quirks are testable: HFRX includes closed funds and so regularly outperforms HFRI (open funds only) but is not replicable, and the Credit Suisse index is AUM-weighted so it tilts to large multi-strategy funds (V8 p.170).

> [!abstract] Idea 1: every single-manager strategy is a position on one risk premium, plus a view on when it fails
> Equity strategies hold equity beta in varying doses; event-driven strategies sell insurance on corporate events (bond plus short put payoff); relative value strategies earn credit, liquidity, or volatility premiums that reverse violently in crises; opportunistic strategies need trends and volatility; specialist strategies earn niche premiums (volatility, mortality, catastrophe) largely uncorrelated with markets; multi-manager strategies are portfolios of all the above (V8 p.170, p.171, p.185, p.191, p.201, p.213, p.222).
> The exam's favorite move is to describe the failure mode and ask which strategy it belongs to.

The equity family is ordered by net exposure.
Long/short equity, about 30% of all hedge funds, runs 40-60% net long (gross 70-90% long vs 20-50% short), aiming for long-only-like returns at roughly half the standard deviation, with alpha from stock picking and only secondary (and usually poor) market timing (V8 p.172, p.173, p.174).
Sector specialists earn a deeper information edge in complex sectors (TMT, financials, biotech); generalists reallocate flexibly but risk missing subtleties (V8 p.174).
Dedicated short sellers run 60-120% short and short-biased managers about 30-60% net short, hunting overvalued companies with deteriorating fundamentals, weak governance, or fraud, using tools like CDS spreads, put implied volatility, the Altman Z-score (bankruptcy) and Beneish M-score (fraudulent statements) (V8 p.175, p.177, p.178).
Their returns are lumpy, more volatile than L/S equity, negatively correlated with everything else, and low-leverage because shorting supplies its own volatility; the short position grows when it moves against you, the opposite of a long (V8 p.176, p.177).
Equity market neutral engineers portfolio beta to approximately zero (often also zero to sector, size, and value factors) and levers the residual stock-selection alpha, up to 300% long vs 300% short under prime broker portfolio margining, with forced downsizing after an excess drawdown as the key strategy risk (V8 p.179, p.181).
Pairs trading, stub trading (parent vs subsidiaries weighted by ownership percentages), and multi-class share trading are the canonical EMN structures, all betting on mean reversion of co-integrated prices; statistical arbitrage is the same idea at shorter horizons (V8 p.179, p.180).
EMN returns are steadier and preferred in non-trending or declining markets, and EMN is often a replacement for fixed income when yields are unattractively low (V8 p.181).

Event-driven strategies price binary corporate outcomes.
A soft-catalyst approach positions before any announcement; a hard-catalyst approach reacts to an announced event and is less volatile and less risky (V8 p.183).
Merger arbitrage buys the target and, in a stock-for-stock deal, shorts the acquirer in the offer ratio, earning the 3-7% spread if the deal closes; 70-90% of announced US mergers do close, and recycling capital 3 to 4 times a year with 3 to 5 times leverage produces net annualized returns of 7-12% (V8 p.184, p.185).
When deals fail, prices revert and losses run 20-40%, so the payoff profile is a riskless bond plus a short put, with an embedded long call for a White Knight higher bid (V8 p.185).
Cross-border deals (two governmental approvals) and vertical integration (antitrust) carry higher risk and wider spreads; hostile deals close less often than friendly ones (V8 p.184, p.185).
Distressed securities managers buy what constrained institutions must sell: below-investment-grade paper of firms in or near bankruptcy, trading below work-out value (V8 p.187, p.188).
Liquidation pays claimants in strict priority (senior secured, junior secured, unsecured, convertible debt, preferred, common); reorganization renegotiates claims, often cancelling existing equity while fulcrum securities, partially-in-the-money claims not repaid in full, convert into ownership of the reorganized company (V8 p.188, p.189).
The strategy is long-biased, illiquid (long lock-ups, gates, Level 3 mark-to-model pricing with return smoothing), modestly levered (1.2 to 1.7 times NAV), and cyclical, best early in a recovery after dislocation (V8 p.187, p.189).

Relative value strategies harvest small, high-correlation mispricings with big leverage.
Fixed-income arbitrage exploits differences in duration, credit quality, liquidity, and optionality, typically duration-neutral, at 4 to 5 times leverage (up to 12 to 15 times inside some market-neutral multi-strategy books) financed through repo with haircuts (V8 p.191, p.192, p.193).
The classic carry trade buys off-the-run and shorts duration-matched on-the-run governments; rates and credit are hedged, liquidity risk remains, and the payoff resembles a short put: steady carry plus convergence, but severe losses if the spread gaps wider and margin calls force sales (V8 p.194).
Yield curve trades (calendar spreads for steepening or flattening) and L/S credit trades are the other archetypes; L/S credit is naturally more volatile (V8 p.193, p.194).
Convertible bond arbitrage rests on one structural fact: convertibles are complex, thinly traded, often non-rated, and issued in bursts, so their embedded call options trade at implied volatility below the equity's historical volatility (V8 p.196).
The arbitrageur buys the cheap embedded option and hedges everything else: short delta-adjusted stock (delta near 1 when in-the-money, near 0 when out), CDS for credit, rate derivatives for duration (V8 p.196, p.197).
Positive gamma means the hedged book gets synthetically longer as the stock rises and shorter as it falls, so rebalancing sells high and buys low; the strategy profits when realized volatility exceeds the implied volatility paid, net of costs (V8 p.197, p.198).
Typical books run 300% long vs 200% short; the strategy dies in credit crises when volatility spikes, liquidity vanishes, and redemption-pressured hedge funds are the market makers (V8 p.197, p.198).

> [!abstract] Idea 2: opportunistic strategies are long trendiness; relative value strategies are short it
> Global macro and managed futures need directional trends and volatility, so mean-reverting low-volatility markets (the QE decade) are their bane; relative value counts on mean reversion and dies when trends turn into dislocations (V8 p.191, p.201, p.202, p.204).
> Managed futures deliver positive right-tail skewness in stress (short equity futures, long bond futures in 2007-2009), the mirror image of the negative skew of insurance-selling strategies (V8 p.204, p.206).
> Global macro is discretionary, heterogeneous, anticipatory, and often early; managed futures are systematic, pattern-driven, and crowd-prone (execution slippage and herding as trend-follower AUM grows) (V8 p.200, p.201, p.206).

Global macro expresses top-down themes across currencies, rates, equities, and commodities, mostly through derivatives; margin-to-equity of 15-25% controls face amounts of 6 to 7 times fund assets (V8 p.200, p.201).
Its diversification across many simultaneous positions is weaker than it looks because risk-on/risk-off regimes correlate asset classes (V8 p.202).
Managed futures (Lintner 1983) trade futures and options on futures across asset classes; 85-90% of capital sits in short-term government collateral, 10-15% margins the positions, and futures margin of 0.1% to 10% of notional embeds the leverage (V8 p.204, p.205).
Signals are momentum or breakout with volatility filters; position sizing shrinks with an asset's volatility and its correlation to the rest of the book, and exits use price targets, momentum reversals, time stops, or trailing stops (V8 p.205).
Time-series momentum goes long past winners and short past losers on absolute returns, so it can be net long or short the whole sector; cross-sectional momentum ranks assets within a class, longs the top half and shorts the bottom half, and stays roughly market neutral with lower volatility (V8 p.205, p.206, p.207).

Specialist strategies earn premiums that need special skills.
Volatility trading exploits geography (time-zone arbitrage in yen options), asset pairs (Nikkei vs S&P implied), term structure, smile, and skew (V8 p.208, p.209).
Equity volatility is about 80% negatively correlated with equity returns, so long volatility is a natural equity hedge, at the cost of premium bleed and roll-down on an upward-sloping volatility term structure (V8 p.208, p.209).
Four implementation paths: exchange-traded options (tenors to about two years, longer-dated for vega, shorter-dated for gamma), OTC options (custom tenor and strike, counterparty and liquidity risk), VIX futures and options (pure volatility view, no delta hedging, but mean reversion and curve roll-down), and volatility or variance swaps (forward contracts on realized volatility or variance, struck at fair value so no initial exchange) (V8 p.209, p.210).
Swaps give pure volatility exposure without delta hedging, which is the recurring exam phrase (V8 p.210).
Reinsurance and life settlements monetize actuarial edges: a life settlement buys a policy from its holder (above surrender value), pays the ongoing premiums, and collects the death benefit; the ideal pool has low surrender values, low ongoing premiums, and high probability of earlier-than-actuarial death (V8 p.212, p.213).
Catastrophe reinsurance wants geographic and peril diversity, a loan loss reserve buffer, and sufficient premium income; both niches are essentially uncorrelated with financial markets (V8 p.213).

Multi-manager investing is a fee-and-information problem.
A fund-of-funds diversifies across external managers, offering access (entry near $100,000 vs $15-20 million to build a 15-20 fund portfolio directly), due diligence, negotiated concessions in side letters, and bridge leverage, at the price of a second fee layer (historically 1% and 10% on top of underlying 1-2% and 10-20%, now compressing toward 50 bps plus 5%) and slower tactical response (V8 p.215, p.216, p.217).
The structural flaw is netting risk: the FoF investor pays incentive fees to each winning underlying fund even when losers drag the aggregate to flat or negative (V8 p.218).
Multi-strategy funds run the teams in-house, so capital moves faster, transparency is complete, and the general partner absorbs netting risk, with investor-level incentive fees charged only on netted total performance (unless a pass-through fee model shifts part of that cost back to investors in place of a management fee) (V8 p.218).
The cost is concentrated operational risk under one roof, higher leverage, and occasional left-tail implosions (Ritchie Capital, 2005); multi-strategy funds have generally outperformed FoFs but with more variance, higher serial autocorrelation (Rho above 20%), and quarterly redemption gates (V8 p.218, p.219, p.232).

> [!abstract] Idea 3: the conditional factor model exists because hedge fund risk is regime-dependent
> A linear factor model with crisis dummy terms separates normal-period betas from incremental crisis betas; total crisis exposure is the sum of the two (V8 p.223, p.229).
> Stepwise regression on TASS and CISDM data (2000-2016) kept SNP500, CREDIT, USD, and VIX and dropped BOND and CMDTY for multicollinearity; the crisis window is June 2007 to February 2009 (V8 p.223, p.224, p.226, p.228).
> The headline findings: L/S equity carries significant equity beta (0.24 to 0.58) that persists in crises; EMN is close to neutral everywhere; multi-manager funds show no significant negative DSNP500, so diversification across hedge fund strategies did not cut crisis risk; and exposures that look absent in calm markets (short volatility, short USD) surface exactly when they hurt (V8 p.229, p.230, p.233, p.234).

Averages mask heterogeneity, so the curriculum also counts the percentage of funds with significant exposures: 70%+ of L/S equity funds have positive equity beta in normal times, under 40% show any incremental crisis equity exposure (mixed signs, evidence of deleveraging and hedging rather than bottom-picking), about one-third have (mostly negative) CREDIT exposure, and roughly 40% of Europe L/S funds went significantly short USD and short VIX in the crisis, the exact wrong exposures when volatility spikes and the dollar rallies (V8 p.230, p.231).
For multi-manager funds the same pattern is starker: only 2% of FoF-equity funds have negative VIX exposure overall, but 60% pick up significant negative DVIX in crises, a footprint of embedded leverage (V8 p.234).

The portfolio payoff of all this: adding a 20% allocation of a strategy portfolio to a 60/40 mix (making it 48/32/20) almost always lowers standard deviation and raises Sharpe and Sortino ratios, and cuts maximum drawdown in about a third of cases, so hedge funds act as both risk-adjusted return enhancers and diversifiers (V8 p.235).
The best diversifiers are the strategies the conditional model showed carry little equity or credit risk in crises and little serial autocorrelation: systematic futures (highest combined Sharpe at 0.83, SD 6.94%), equity market neutral, global macro, and merger arbitrage (smallest drawdowns, 5-6% region) (V8 p.236, p.237, p.238, p.239).
L/S equity, event-driven/distressed, and convertible arbitrage add return but keep high drawdowns because their equity and credit risks bind in stress (V8 p.238, p.239).
Use the Sortino ratio, not Sharpe, when the strategy has large negative events, because Sharpe penalizes upside and downside variability alike while Sortino penalizes only downside deviation below the target (V8 p.236, p.259).

## Formulas and derivations

**Beta-weighted pairs sizing (EMN pairs trade)** (V8 p.183)
$$
\text{Short leg value} = \frac{\text{Long leg value}}{\beta_{\text{short}} / \beta_{\text{long}}}
$$
^f-08-04-1

- Long leg value: dollars allocated to the undervalued stock; betas are the two stocks' market betas; the result is the dollar value to short of the overvalued stock.
- It holds because beta neutrality requires equal beta-dollar exposures: $\beta_L V_L = \beta_S V_S$, so $V_S = V_L \beta_L / \beta_S$.
- Curriculum case: long KO $1{,}000{,}000$ at beta 0.55, short PEP $= 1{,}000{,}000/(0.65/0.55) = \$846{,}154$ at beta 0.65 (V8 p.183, Python confirms 846,153.85).
- Index weights given in the vignette are decoys; only betas matter (V8 p.183).

> [!tip] Calculator
> `0.65 / 0.55 =` gives 1.1818; `1000000 / 1.1818 =` displays 846,153.85.

**Stub trading hedge ratio** (V8 p.180)
$$
\text{Shares of subsidiary bought per parent share shorted} = \text{Ownership percentage}
$$
^f-08-04-2

- If parent A owns 90% of B and 75% of C, each short share of A is offset by long 0.90 shares of B and 0.75 shares of C.
- The ratio replicates the parent's look-through economic exposure to the subsidiaries so only relative mispricing remains.

**Merger arbitrage payoff if the deal closes (stock-for-stock)** (V8 p.184, p.186)
$$
\text{Payoff}_{\text{success}} = \text{Short proceeds from acquirer} - \text{Cost of target shares}
$$
^f-08-04-3

- Buy target shares and short acquirer shares in the offer ratio (e.g., offer of 1 A per 2 T: short 1 share of A per 2 shares of T bought); at completion the target shares convert and deliver into the short, locking the spread.
- Curriculum case: buy 20,000 T at $19 ($380,000), short 10,000 A at $42 ($420,000), spread $= \$40{,}000$ (V8 p.186, p.187, Python confirms).
- The spread exists because deals take months and can fail; it is the insurance premium for bearing event risk (V8 p.185).

**Merger arbitrage payoff if the deal fails** (V8 p.185, p.187)
$$
\text{Loss}_{\text{fail}} = (\text{Short proceeds} - \text{Cost to cover at pre-deal price}) + (\text{Target value at pre-deal price} - \text{Cost of target shares})
$$
^f-08-04-4

- Prices revert to pre-announcement levels: the target falls back, the acquirer rises back, and both legs lose.
- Curriculum case: cover 10,000 A at $45 (spend $450,000 vs $420,000 received, lose $30,000) and T falls to $15 (worth $300,000 vs $380,000 paid, lose $80,000): total $-\$110{,}000$ (V8 p.187, Python confirms).
- The two payoffs together are a riskless bond with face equal to the spread plus a short binary put paying out the failure loss, with an extra long call on a White Knight bid (V8 p.185).

> [!tip] Calculator
> Failure leg: `420000 - 450000 = STO 1` then `300000 - 380000 = + RCL 1 =` displays -110,000.

**Conversion value and conversion price of a convertible bond** (V8 p.195, p.196)
$$
\text{Conversion value} = \text{Stock price} \times \text{Conversion ratio}, \qquad \text{Conversion price} = \frac{\text{Convertible bond price}}{\text{Conversion ratio}}
$$
^f-08-04-5

- Conversion ratio: shares received per bond; convertible bond price in currency (price percent of par times par).
- A convertible is straight debt plus a call on the stock; the call is in-the-money when the share price exceeds the conversion price, and the bond then trades like equity, otherwise like a straight bond (V8 p.195, p.196).
- Curriculum case: price 120% of par 1,000, ratio 50, so bond price EUR 1,200 and conversion price EUR 24 against a EUR 30 share (V8 p.198, p.199, Python confirms).

**Convertible arbitrage locked-in profit per share (bond near conversion value)** (V8 p.199, p.262)
$$
\text{Profit per share} = \underbrace{(S_{\text{new}} - \text{Conversion price})}_{\text{long stock via convertible}} + \underbrace{(S_0 - S_{\text{new}})}_{\text{short stock}} = S_0 - \text{Conversion price}
$$
^f-08-04-6

- $S_0$: share price when the short is established; $S_{\text{new}}$: any later share price; the $S_{\text{new}}$ terms cancel, so the profit is independent of where the stock goes (for small moves, ignoring carry).
- Carry adjustments per share: subtract borrow cost and the dividend owed to the lender, add the coupon per share (coupon amount divided by conversion ratio) (V8 p.199).
- Curriculum case: $30 - 24 = 6$ per share gross; borrow EUR 2 plus dividend EUR 1 less coupon EUR 1 ($= 50/50$) cuts it to EUR 4 (V8 p.199, Python confirms all three price scenarios give 6).

**Fund-of-funds net-of-fee return (two fee layers)** (V8 p.220)
$$
r_{\text{net,fund}} = r_{\text{gross}} - m_{\text{HF}} - p_{\text{HF}}\max(0, r_{\text{gross}} - m_{\text{HF}}), \qquad r_{\text{net,FoF}} = \bar{r}_{\text{net,fund}} - m_{\text{FoF}} - p_{\text{FoF}}\max(0, \bar{r}_{\text{net,fund}} - m_{\text{FoF}})
$$
^f-08-04-7

- $m$: management fee; $p$: incentive fee rate; incentive fees apply only to gains net of the management fee; $\bar{r}_{\text{net,fund}}$ is the weighted average of underlying net returns; losing funds pay no incentive fee but their losses still drag the average (netting risk) (V8 p.218, p.220).
- Curriculum case: both funds gross 20% with 2/20 gives fund-level net $20 - 2 - 3.6 = 14.4\%$, then FoF at 1/10 gives $14.4 - 1 - 1.34 = 12.06\%$ (V8 p.220, Python confirms).
- With one fund at $-5\%$: UF investor nets $-7.0\%$, FoF gross $3.7\%$, FoF net $2.43\%$, and fees eat 67.6% of the 7.5% gross (V8 p.220, p.221, Python confirms).

> [!tip] Calculator
> Fund level: `20 - 2 = STO 1 x 0.2 = STO 2 RCL 1 - RCL 2 =` gives 14.4.
> FoF level: `14.4 - 1 = STO 1 x 0.1 = STO 2 RCL 1 - RCL 2 =` gives 12.06.

**Conditional linear factor model for hedge fund returns** (V8 p.223)
$$
\begin{aligned}
(\text{Return on } HF_i)_t = \alpha_i &+ \beta_{i,1}(\text{Factor 1})_t + \dots + \beta_{i,K}(\text{Factor K})_t \\
&+ D_t\beta_{i,1}(\text{Factor 1})_t + \dots + D_t\beta_{i,K}(\text{Factor K})_t + (\text{error})_{i,t}
\end{aligned}
$$
^f-08-04-8

- $\beta_{i,k}$: exposure to factor $k$ in normal times; $D_t\beta_{i,k}$: incremental exposure during crisis periods, where the dummy $D_t = 1$ from June 2007 to February 2009 and 0 otherwise; $\alpha_i$: manager skill intercept; error has zero mean and standard deviation $\sigma_i$ (V8 p.223).
- The four retained factors are SNP500 (S&P 500 total return), CREDIT (Baa minus Aaa yield spread), USD (US Dollar Index return), and VIX (first difference of month-end VIX); BOND and CMDTY were dropped by stepwise regression because CREDIT and SNP500 gave higher adjusted R-squared (V8 p.223, p.226).
- Unexplained return splits into alpha, omitted factors, and random error (V8 p.223).
- Desired crisis exposures flip sign versus normal times: long equity and credit, short USD and VIX in normal markets; short equity and credit, long USD and VIX in crises (V8 p.226, p.227).

**Total crisis-period factor exposure** (V8 p.229, p.231)
$$
\beta_{\text{crisis,total}} = \beta_{\text{normal}} + \beta_{D}
$$
^f-08-04-9

- $\beta_D$ is the coefficient on the crisis dummy interaction (the D-prefixed factor); the crisis dummy adds to, not replaces, the normal beta.
- Curriculum cases: US L/S equity $0.58 + 0.03 = 0.61$; the short-biased fund $-0.572 + 0.236 = -0.336$, still significantly negative but less short into the crisis (V8 p.229, p.231, Python confirms).

**Volatility swap payoff at expiry** (V8 p.210)
$$
\text{Payoff}_{\text{vol}} = \text{Notional}_{\text{vega}} \times (\sigma_{\text{realized}} - \sigma_{\text{strike}})
$$
^f-08-04-10

- A forward contract on future realized volatility; the strike is set at fair volatility so initial value is zero and no notional is exchanged up front; the floating-leg receiver is paid when realized volatility exceeds the strike (V8 p.210).
- Gives pure volatility exposure with no delta hedging, unlike options whose volatility exposure depends on the underlying price (V8 p.210).

**Variance swap payoff at expiry (variance notional arithmetic)** (V8 p.210)
$$
\text{Payoff}_{\text{var}} = \text{Notional}_{\text{variance}} \times \left(\sigma_{\text{realized}}^2 - \sigma_{\text{strike}}^2\right)
$$
^f-08-04-11

- Variance is the square of volatility, so payoffs are convex in volatility: a variance swap pays more than a vega-equivalent volatility swap when volatility spikes far above the strike and loses less when it collapses (V8 p.210).
- The strike is fair variance at inception (zero initial value); the prespecified notional multiplies the difference between realized variance and strike variance at expiry, with no initial exchange (V8 p.210).
- Both swaps are used to bet on realized volatility, trade realized against implied, or hedge volatility exposure of other positions, with OTC-tailored maturities and strikes under ISDA documentation (V8 p.210).

**Sortino ratio** (V8 p.227, p.236)
$$
\text{Sortino ratio} = \frac{\bar{r} - r_{\text{target}}}{\text{Downside deviation}}
$$
^f-08-04-12

- Replaces the Sharpe ratio's standard deviation with downside deviation below a threshold (losses when the threshold is zero), so it penalizes only downside variability (V8 p.227, p.236).
- Preferred over Sharpe for strategies with large negative events; high first-order serial autocorrelation (Rho) signals smoothed returns from illiquid holdings and understated risk (V8 p.227, p.259).

**Portfolio variance screen** (V8 p.259)
$$
\sigma_{\max}^2 = \sigma_{\text{current}}^2 \times \text{Allowed fraction}, \qquad \sigma_{\max} = \sqrt{\sigma_{\max}^2}
$$
^f-08-04-13

- Variance is the square of standard deviation, so a "variance below 90% of current" constraint means $\sigma_{\max} = \sqrt{0.9}\,\sigma_{\text{current}}$, not $0.9\,\sigma_{\text{current}}$.
- Curriculum case: $7.95^2 \times 0.9 = 56.88$, so $\sigma_{\max} = 7.54\%$ (V8 p.259, Python confirms 7.542).

> [!tip] Calculator
> `7.95 x^2 x 0.9 = sqrt(x)` displays 7.54.

## Worked examples

**Example 1: Long/Short Equity Investing Dilemma** (V8 p.174, p.175)
The Larson family office wants L/S equity managers skilled at shorting, refuses to pay hedge fund fees for long-biased beta, and will pay for differentiated risk-adjusted performance.
Recommendation: prefer sector-specialist L/S managers (technology, financials, biotech/health care), because deep-dive specialist analysis is more likely to produce original views and true alpha, while generalists may lack a dependable information edge relative to their fees and natural long beta.
Risks: specialist funds are harder to analyze, fewer in number, and can leave the office with concentrated single-sector or short-side exposure at the wrong time in the macro cycle, while generalists can reallocate across sectors as opportunities move. ^ex-08-04-1

**Example 2: Candidate for Short-Biased Hedge Fund Strategy** (V8 p.178, p.179)
Generic Inc. trades at P/E 30 vs industry 20 (50% higher), P/B 3.5 vs 2.5 (40% higher), with 3% trailing EPS growth vs 18%, double the industry leverage, and a binary drug trial one month out.
Fundamentals say short, but the stock is thinly traded with a 60% short-interest ratio and a 20% annual borrow cost ("special"), so a short squeeze on good trial news could be devastating; Stone correctly declines the outright short.
Option alternatives: buy puts outright; buy a long put calendar spread (buy a put expiring after the results, sell a put expiring before, financing part of the cost); buy the stock, lend it at the attractive 20% rate, and hedge with out-of-the-money puts (protective put); or sell expensive out-of-the-money calls to fund out-of-the-money puts (short risk reversal, synthetic short exposure). ^ex-08-04-2

**Example 3: Equity Market-Neutral Pairs Trading** (V8 p.182, p.183)
Chang allocates $1 million long KO (beta 0.55) against a short in PEP (beta 0.65) whose valuation has stretched beyond historical ranges.
Beta-weighted sizing: short PEP value $= -\$1{,}000{,}000/(0.65/0.55) = -\$846{,}154$ (Python: 846,153.85).
Check: $846{,}154 \times 0.65 = 550{,}000 = 1{,}000{,}000 \times 0.55$, so beta-dollar exposures match and only the relative performance of PEP vs KO drives the P&L.
The S&P 500 index weights in the table are irrelevant to the sizing; profits come if valuations mean-revert within the three-month window. ^ex-08-04-3

**Example 4: Merger Arbitrage Strategy Payoffs** (V8 p.186, p.187)
Stock-for-stock offer of 1 A share per 2 T shares; pre-announcement A $45, T $15; post-announcement A $42, T $19; manager buys 20,000 T and shorts 10,000 A (the offer ratio).
Success: cost of T $= 20{,}000 \times 19 = \$380{,}000$; short proceeds $= 10{,}000 \times 42 = \$420{,}000$; spread $= \$40{,}000$ (Python confirms).
Failure: cover A at $45 costing $450,000 (lose $30,000 on the short) and T reverts to $15, worth $300,000 (lose $80,000 on the long); total loss $= (420{,}000 - 450{,}000) + (-380{,}000 + 300{,}000) = -\$110{,}000$ (Python confirms).
Equivalent position: a riskless bond with face $40,000 plus a short binary put that pays out $110,000 on deal failure. ^ex-08-04-4

**Example 5: Capital Structure Arbitrage in the Energy Crisis of 2015-2016** (V8 p.190, p.191)
Oil fell from above $60 to below $30, junior unsecured E&P debt collapsed on forced institutional selling after downgrades, but retail-held equities stayed benignly priced, leaving equity-implied enterprise value inconsistent with debt priced for bankruptcy.
The divergence came from the structural difference in natural holders: mandate-constrained institutions had to sell downgraded debt, while less-informed retail equity holders bought the dip.
Trade: buy the undervalued junior unsecured debt hedged with short equity (or long puts); if bankruptcy comes, equity goes to zero while the debt has recovery value or becomes the fulcrum security converting to new equity; if oil recovers (it closed 2017 above $60), the debt rebounds more than the equity rises; the position wins across outcomes. ^ex-08-04-5

**Example 6: Fixed-Income Arbitrage: Treasuries vs Inflation Swap + TIPS** (V8 p.194, p.195)
In stressed November 2XXX, Landers buys 5-year TIPS (receive 3.74% real plus inflation accrual, cost $1,000,000), shorts 5-year Treasuries (pay 2.56%, proceeds $1,000,000), and receives fixed 1.36% on an inflation swap while paying inflation, at zero cost.
Net: receive $3.74 - 2.56 + 1.36 = 2.54\%$ with all inflation flows cancelled and zero net outlay (Python confirms), versus the normal 25-35 bps premium of hedged TIPS over Treasuries.
It is near risk-free in cash flow terms but operationally fragile: it needs interbank repo access to borrow the Treasuries, bank credit approval for the inflation swap, and it faces shrinking credit lines and the risk of losing the borrow precisely in the distressed periods when the mispricing appears; such extreme arbitrage rarely persists. ^ex-08-04-6

**Example 7: Convertible Arbitrage Strategy** (V8 p.198, p.199)
QXR convertible: price 120% of par 1,000 (EUR 1,200), coupon 5%, ratio 50, so conversion price $= 1{,}200/50 = $ EUR 24 vs share price EUR 30; QXR's P/E, P/B, and P/CF are all 50% above industry averages.
Setup: shares overvalued, convertible undervalued, so buy the convertible and short the shares.
Payoff is invariant (Python confirms): at EUR 24, long via convertible 0, short $+6$; at EUR 36, long $+12$, short $-6$; at EUR 30, long $+6$, short 0; total EUR 6 per share in every scenario.
Carry: borrow cost EUR 2 plus EUR 1 dividend owed to the lender, offset by EUR 1 coupon per share ($50/50$), so net profit falls to EUR 4 per share. ^ex-08-04-7

**Example 8: Global Macro Strategy** (V8 p.203)
Overheating EM countries run twin deficits, central banks defend currencies, and one leading EM central bank is about to exhaust its FX reserves.
Chu should anticipate devaluation and contagion: buy puts on EM currencies, EM government bond futures, and EM equity indexes, in-the-money for high-conviction trades and out-of-the-money where conviction is lower, so losses are capped at premiums if the thesis fails.
Add flight-to-safety wings: calls on developed market reserve currencies and calls on highly rated DM government bond futures. ^ex-08-04-8

**Example 9: Cross-Sectional and Time-Series Momentum** (V8 p.207, p.208)
Two managed futures funds trade gold, silver, platinum, and palladium on trailing 6-month signals with volatility-weighted positions.
CSM: rank the four metals, go long the top two and short the bottom two on relative risk-adjusted returns; the book is roughly net zero, the legs quasi-hedge each other, and top-half metals can have negative absolute returns in bear markets (and vice versa).
TSM: go long every metal with positive trailing 6-month returns and short every metal with negative returns, judged in isolation, so the fund can end up long all four or short all four.
Consequence: the TSM fund is more volatile and far more sensitive to strong sector trends; the CSM fund runs lower volatility and stays market neutral in normal periods. ^ex-08-04-9

**Example 10: Long Volatility Strategy Payoff** (V8 p.211, p.212)
Ortiz buys one-year 10% out-of-the-money index puts in January for $100 per contract at 12% implied volatility; by April the index is up 20% and the puts have halved to $50; by July a crisis drops the index 25% below April (10% below January) and implied volatility hits 30%.
July assessment: six months of time decay hurt, but the puts moved from 10% out-of-the-money to at-the-money, and implied volatility rose 2.5 times; volatility changes have their greatest price impact on at-the-money options, so Ortiz has a large mark-to-market gain despite the earlier 50% drawdown.
If markets then move sideways to January: the at-the-money premium erodes through theta and volatility value dissipates, and Ortiz ultimately loses the whole $100 unless she actively delta hedges with index futures, buying and selling around the position to harvest gamma against the decay. ^ex-08-04-10

**Example 11: Investing in Life Settlements** (V8 p.214)
SingStar analyzes a pool of policies heavily originated by NextLife, an insurer known for weak underwriting (low premiums on unhealthy lives) and low surrender values; sampled insureds developed early-onset Alzheimer's, with life expectancy about 10 years shorter than average.
Valuation: forecast the cash flows (ongoing premiums to keep policies active, favorably low given NextLife's pricing; death benefits, favorably early given the biometric profile), discount at a risk-adjusted rate, and bid relative to the minimum price and expected competition.
If the biometric, actuarial, and financial forecasts hold, returns are attractive and uncorrelated with financial markets, because nothing in the payoff depends on market behavior. ^ex-08-04-11

**Example 12: Fund-of-Funds: Net-of-Fee Returns** (V8 p.220, p.221)
SVFOF charges 1 and 10 over two equally weighted funds each charging 2 and 20; fees are paid year-end without compounding.
Both funds gross 20%: fund-level net $= 20 - 2 - 0.20(20 - 2) = 20 - 2 - 3.6 = 14.4\%$; FoF net $= 14.4 - 1 - 0.10(14.4 - 1) = 14.4 - 1 - 1.34 = 12.06\%$ (Python confirms); fees consume $(2 + 3.6 + 1 + 1.34)/20 = 39.7\%$ of gross.
PF grosses 20%, UF loses 5%: PF investor nets 14.4%; UF investor nets $-5 - 2 - 0 = -7.0\%$ (no incentive fee on a loss); FoF gross $= 0.5(14.4) + 0.5(-7.0) = 3.7\%$; FoF net $= 3.7 - 1 - 0.10(3.7 - 1) = 2.43\%$ (Python confirms).
Netting risk shown explicitly: original gross was $0.5(20) + 0.5(-5) = 7.5\%$, and fees of $0.5(2 + 3.6 + 2 + 0) + (1 + 0.27) = 5.07\%$ absorb 67.6% of it, because PF's incentive fee is owed even though UF lost money (Python confirms). ^ex-08-04-12

**Example 13: Funds-of-Funds or Multi-Strategy Funds, Which to Choose?** (V8 p.221, p.222)
Mona wants diversification, flexibility, transparency, and maximum net-of-fee returns into a volatile period.
Multi-strategy advantages: generally better performance, fast tactical reallocation inside one structure (valuable in dynamic markets), full position-level transparency, and investor-friendly fees with netting risk absorbed (at least partly) by the GP; disadvantages: concentrated manager-specific operational risk and higher leverage, hence higher return variance.
FoF advantages: potentially more diverse strategy mix, lower leverage and somewhat less return variance, diversified operational risk across independent funds; disadvantages: less transparency, slower tactical reaction, and a double fee layer with netting risk borne by the investor, a substantial net-return drag. ^ex-08-04-13

**Example 14: Dedicated Short-Biased Hedge Fund** (V8 p.231)
BAM's conditional model estimates: normal SNP500 $-0.572$ (t $= -9.65$) and VIX $-0.164$ (t $= -2.19$) are significant; crisis increments DSNP500 $+0.236$ (t $= 1.74$, significant at 10%) with the rest insignificant.
Interpretation: the significant negative equity beta fits a short-biased mandate; the significant negative VIX loading means short volatility exposure, consistent with selling puts against short positions to harvest premium.
Crisis equity beta $= -0.572 + 0.236 = -0.336$ (Python confirms): still significantly negative, but BAM covered part of its short book into market weakness, harvesting gains rather than pressing the short. ^ex-08-04-14

**Example 15: Combining a Hedge Fund Strategy with a Traditional Portfolio** (V8 p.239, p.240)
Evergreen's IC wants a 20% strategy allocation that maximizes risk-adjusted return, limits downside, keeps liquidity, and avoids fee layering; the 60/40 base shows mean 6.96%, SD 8.66%, Sharpe 0.62, Sortino 1.13, drawdown 14.42%.
Least suitable: FoF-equity, because the combined Sharpe (0.62) and Sortino (1.11) show no improvement, maximum drawdown of 21.63% is 50% worse than the base, liquidity suffers from two levels of lock-ups and gates, and the FoF structure adds a second fee layer plus netting risk.
Most suitable: sovereign debt fixed-income arbitrage, with the highest combined Sharpe (0.75) and Sortino (1.39), the lowest drawdown (12.68%), good liquidity from developed-market sovereign paper, and a single fee layer with no netting risk. ^ex-08-04-15

## Item-set patterns

> [!warning] Trap: merger-arb payoff computed at the wrong prices
> The vignette gives pre-announcement and post-announcement prices for both companies.
> Correct: enter at post-announcement prices; success pays short proceeds minus long cost; failure reverts both legs to pre-announcement prices (V8 p.187, p.261).
> Distractor A uses the failure loss as the answer to the success question (or vice versa); distractor B computes the payoff using pre-announcement prices ($412,500 instead of $225,000 in the Aqua/Taurus problem), tempting because those prices appear first in the vignette.

> [!warning] Trap: hedging the merger-arb book with the wrong options
> Vignette: manager is long target T, short acquirer A, and fears deal failure.
> Correct: buy out-of-the-money calls on A (protects the short as A rebounds) and out-of-the-money puts on T (protects the long as T falls) (V8 p.186, p.256).
> The reversed combination (puts on A, calls on T) is tempting because puts feel like protection on whatever is mentioned first; the bond-plus-short-put-plus-long-call description is the payoff profile, not a hedge, and appears as a third distractor (V8 p.257).

> [!warning] Trap: conversion price vs conversion value
> The vignette gives price as a percent of par plus a conversion ratio and asks for the arbitrage profit.
> Correct: conversion price = (par times price percent)/ratio; locked-in profit per share = current share price minus conversion price, identical whether the stock rises, falls, or is flat (V8 p.196, p.199, p.262).
> Distractors claim the profit is higher if the share price falls (feels right because the position is short stock) or rises (long gamma intuition misapplied); both ignore that the two legs cancel for small moves.

> [!warning] Trap: carry trade vs yield curve trade vs L/S credit
> A government bond trade buying off-the-run and shorting duration-matched on-the-run paper is a carry trade whose residual risk is liquidity, not rates or credit (V8 p.194, p.257).
> "Yield curve trade" tempts because two bonds sit at slightly different curve points; "L/S credit" tempts because two different issues are involved, but same-issuer duration-matched governments have no credit differential.
> Flag words: off-the-run vs on-the-run means carry/liquidity; steepening or flattening means yield curve; investment-grade vs high-yield means L/S credit.

> [!warning] Trap: TSM vs CSM vs global macro classification
> A rules-based futures strategy ranking a cross-section of same-class assets and going long winners/short losers to a net zero holding is cross-sectional momentum managed futures, not global macro (V8 p.206, p.258).
> "Global macro" tempts whenever macro data (yield spreads) feed the signal; "time-series momentum" tempts because momentum is mentioned, but TSM judges each asset in isolation on absolute returns and can be net long or net short the whole class.
> The phrase "net holding is market neutral" is the CSM fingerprint.

> [!warning] Trap: which volatility position helps in a crisis
> The vignette asks for a specialist strategy that keeps the Sharpe ratio high when equities fall.
> Correct: long volatility, e.g., longer-dated out-of-the-money options on VIX futures, because equity volatility is about 80% negatively correlated with equity returns (V8 p.208, p.258).
> Selling volatility tempts because it earns steady premiums in normal times, but the seller is the insurer who pays out in the crisis; cross-asset relative value volatility tempts as sophisticated but carries idiosyncratic macro risks that can bite in a crisis (V8 p.259).

> [!warning] Trap: FoF vs multi-strategy attribute swap
> The vignette voice praises an FoF for tactical speed or blames a multi-strategy fund for double fees.
> Correct mapping: multi-strategy = faster tactical reallocation, full transparency, GP absorbs netting risk, but concentrated operational risk and higher leverage; FoF = more diverse strategy mix and diversified operational risk, but double fee layer, investor-borne netting risk, less transparency, slower reaction (V8 p.218, p.219, p.259).
> The pass-through fee model is the nuance distractor: under it the multi-strategy investor implicitly pays part of the netting cost in place of a management fee (V8 p.218).

> [!warning] Trap: reading the conditional factor table as replacement rather than increment
> The D-prefixed crisis coefficients are additions to the normal betas, so total crisis exposure = normal beta + D beta ($-0.572 + 0.236 = -0.336$; $0.58 + 0.03 = 0.61$) (V8 p.229, p.231).
> Distractors treat the D coefficient alone as the crisis exposure, or claim a fund with insignificant normal VIX exposure has no volatility risk when the significant negative DVIX shows short volatility emerging exactly in the crisis (V8 p.234).

> [!warning] Trap: Sharpe vs Sortino vs drawdown for suitability
> When the committee expects large negative events, rank on the Sortino ratio; maximum drawdown is a tiebreaker or a separate stated constraint, not the risk-adjusted return measure (V8 p.236, p.259, p.260).
> A variance ceiling stated as "variance below 90% of current" converts to a standard deviation ceiling via the square root ($\sqrt{0.9} \times 7.95 = 7.54$), not by multiplying the standard deviation by 0.9 (V8 p.259).
> The merger arbitrage row with the smallest drawdown is the classic tempting wrong answer when its Sortino is lower (V8 p.260).

> [!warning] Trap: life settlement characteristics reversed
> The fund wants low surrender value offered to the insured, low ongoing premiums, and high probability of death earlier than standard actuarial predictions (V8 p.213, p.262).
> Distractors flip one word: high surrender value (raises the purchase price), or death "within the period predicted by actuarial methods" (that is the priced-in base case, not an edge).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM04-Hedge-Fund-Strategies-Practice-Problems]]

## Cross-links

- [[LM01-Introduction-to-Commodities-and-Commodity-Derivatives]]: managed futures and global macro trade the commodity futures curves built there; volatility and variance swaps here mirror the commodity swap taxonomy, and the collateralized-futures return decomposition explains why 85-90% of a managed futures account sits in government collateral.
- [[LM04-Using-Multifactor-Models]]: the conditional linear factor model is a multifactor return model with regime dummies; factor betas, alpha, and stepwise factor selection here apply the machinery developed there.
- [[LM05-Measuring-and-Managing-Market-Risk]]: Sharpe vs Sortino, maximum drawdown, serial autocorrelation as an illiquidity flag, and crisis-conditional exposures feed directly into the risk measurement toolkit of that module.
- [[LM02-Valuation-of-Contingent-Claims]]: convertible arbitrage delta hedging and gamma trading, merger arbitrage's bond-plus-short-put payoff, protective puts, calendar spreads, and risk reversals all rest on the option pricing and Greeks developed there.

## Self-test

Vignette: Arlette Fontaine, CIO of the Beaumont family office, is building a 20% hedge fund sleeve onto a 60/40 portfolio.
She interviews five managers.
Manager V runs balanced long/short books of co-integrated stock pairs at 280% long vs 280% short, targeting zero beta, size, and sector exposure, rebalancing intraday with trading-cost hurdle models.
Manager W buys announced-deal targets and shorts acquirers in the offer ratio, concentrating in friendly domestic deals at 4x leverage.
Manager X buys convertibles at implied volatility below the stock's historical volatility, shorting delta-adjusted stock, and running 300% long vs 200% short.
Manager Y trades 40 futures markets systematically, long any market with positive trailing 12-month returns and short any with negative returns, sized inversely to volatility.
Manager Z buys pools of life policies from brokers and writes catastrophe reinsurance.
Fontaine's committee requires: crisis diversification, no fee layering, and Sortino-maximizing risk-adjusted returns.

**Q1.** Manager V's strategy most likely requires which vehicle structure, and why?
A. Mutual fund, because the strategy is liquid and diversified
B. Limited partnership, because leverage exceeds regulated-vehicle limits
C. UCITS, because EMN qualifies as a liquid alt in Europe

**Q2.** During a crisis, Manager V's most likely hidden exposure is:
A. long equity beta from residual net long positioning.
B. short volatility tail risk from mean-reversion positioning plus forced deleveraging under prime broker portfolio margining.
C. long credit spreads from the bond legs of the pairs.

**Q3.** Manager W's return profile is best characterized as:
A. a riskless bond plus a long put on the target.
B. a riskless bond plus a short put, plus a long call on a higher White Knight bid.
C. a long straddle on deal completion.

**Q4.** A deal in W's book: acquirer offers 1 share (trading at $80 post-announcement, $84 pre) per 4 target shares (target at $19 post, $15 pre); W buys 40,000 target shares and shorts 10,000 acquirer shares.
The success and failure payoffs are closest to:
A. +$40,000 / -$120,000
B. +$40,000 / -$200,000
C. +$60,000 / -$160,000

**Q5.** Manager X profits primarily when:
A. realized equity volatility exceeds the implied volatility purchased, net of hedging costs.
B. implied volatility falls and the convertible's bond floor rises.
C. credit spreads widen while the stock is unchanged.

**Q6.** Manager X's 300%/200% long/short structure exists because:
A. regulations cap short exposure at two-thirds of long exposure.
B. the short stock hedge is sized to the convertible's delta, which is below 1.
C. the strategy is net long credit and must underhedge equity.

**Q7.** In a quarter where 30 of Manager Y's 40 markets trend upward strongly, Y's book will most likely be:
A. net long and highly directional, unlike a cross-sectional version which would stay near market neutral.
B. market neutral, because momentum strategies always balance longs and shorts.
C. net short, because volatility weighting forces contrarian sizing.

**Q8.** Which manager best satisfies the committee's crisis-diversification requirement through returns structurally uncorrelated with financial markets?
A. Manager Z, because mortality and catastrophe outcomes do not depend on market behavior
B. Manager X, because delta hedging removes market exposure
C. Manager W, because deal spreads are idiosyncratic

**Q9.** Fontaine's analyst runs the conditional factor model on Manager W: SNP500 beta 0.15 (significant), DSNP500 0.21 (significant), DCREDIT 0.18 (significant).
The correct interpretation is:
A. W's crisis equity exposure is 0.21 and credit exposure hedges the book.
B. W's total crisis equity beta is 0.36 and rising credit exposure into widening spreads compounds losses, confirming merger arbitrage's left-tail character.
C. W is market neutral in crises since 0.15 and 0.21 nearly offset DCREDIT.

**Q10.** The committee's "no fee layering" and Sortino requirements together most strongly rule out:
A. allocating through a fund-of-funds to access managers V through Z.
B. allocating directly to Manager Y.
C. allocating to a multi-strategy fund with GP-absorbed netting.

> [!success]- Answer key
> Q1: B.
> EMN leverage (up to 300%/300% under portfolio margining) exceeds regulatory leverage limits for mutual fund vehicles, so limited partnerships are the preferred vehicle (V8 p.181).
> A and C fail because the liquid alts that qualify for mutual fund/UCITS formats are generally lower-leverage long/short and managed futures strategies, not highly levered EMN (V8 p.167, p.181).
> Q2: B.
> Quantitative EMN mean-reversion books carry effective short volatility tail risk in extreme stress, and prime brokers can force portfolio downsizing after an excess drawdown, the key strategy risk (V8 p.180, p.181).
> A is wrong because V targets zero beta; C is wrong because there are no bond legs in a stock pairs book.
> Q3: B.
> Merger arbitrage sells insurance on the deal: collect the spread if it closes (bond), pay out reversion losses if it fails (short put), with an embedded long call on a higher competing bid (V8 p.185).
> A reverses the option sign; C describes a volatility position, not an event insurance sale.
> Q4: B.
> The exchange ratio is 1 acquirer share per 4 target shares, so 40,000 target shares are hedged with 10,000 short acquirer shares.
> Success: the 40,000 target shares convert into exactly the 10,000 acquirer shares that close the short, so the payoff is the spread locked at announcement, $10{,}000 \times 80 - 40{,}000 \times 19 = 800{,}000 - 760{,}000 = +\$40{,}000$.
> Failure: both legs revert to their pre-announcement prices, so the long loses $40{,}000 \times (15 - 19) = -\$160{,}000$ and the short loses $10{,}000 \times (80 - 84) = -\$40{,}000$, a total of $-\$200{,}000$.
> A understates the failure loss by reverting only the target leg partially; C misprices the success spread by valuing the converted shares at the pre-announcement price (method per V8 p.187).
> Q5: A.
> The strategy buys cheap implied volatility and gamma-trades the hedge; it wins when realized volatility beats the implied volatility paid, net of costs (V8 p.198).
> B is wrong because falling implied volatility hurts the long option; C is wrong because unhedged spread widening hurts the long convertible.
> Q6: B.
> The short equity exposure needed is the delta-adjusted equivalent of the long convertibles, and deltas below 1 make the short leg smaller than the long leg (V8 p.197).
> A invents a regulation; C describes a credit-oriented style choice, not the structural reason.
> Q7: A.
> Time-series momentum takes absolute-return signals market by market, so a broadly trending quarter leaves the book heavily net long; cross-sectional momentum would still hold half long, half short by rank (V8 p.206, p.207).
> Q8: A.
> Life settlement and catastrophe payoffs depend on mortality timing and natural events, neither related to financial market behavior (V8 p.213).
> B is wrong because delta hedging leaves credit, liquidity, and volatility exposures; C is wrong because deal failure risk clusters in market stress (V8 p.185).
> Q9: B.
> Crisis exposures are increments: total crisis equity beta $= 0.15 + 0.21 = 0.36$, and a positive DCREDIT means returns fall as spreads widen, exactly the left-tail pattern of event-driven strategies (V8 p.185, p.229).
> A misreads the increment as the total; C adds unrelated coefficients.
> Q10: A.
> A fund-of-funds adds a second fee layer and investor-borne netting risk, directly violating the no-layering requirement (V8 p.218, p.220).
> B is fine (single fee layer); C is attractive on fees since the GP absorbs netting (V8 p.218).

## Flashcards

#flashcards/cfa-l2/08-Alternative-Investments/lm04

Seven distinguishing hedge fund characteristics::Light legal/regulatory constraints, flexible mandates, large investment universe, aggressive styles, liberal leverage, investor liquidity constraints (lock-ups and gates), high fees (management plus incentive) (V8 p.167, p.168).
Liquid alts vs traditional hedge funds::Liquid alts give daily liquidity, transparency, lower fees, and no incentive fees, and underperform similar hedge funds by about 100-200 bps a year, evidence of an illiquidity premium (V8 p.166, p.168).
Three criteria used to classify hedge fund strategies::Instruments traded, trading philosophy (systematic vs discretionary), and types of risk assumed (V8 p.168).
The six strategy buckets in this module::Equity, event-driven, relative value, opportunistic, specialist, multi-manager (V8 p.170).
Why HFRX outperforms HFRI::HFRX includes funds closed to new investment (typically superior managers), so it outperforms but is not replicable (V8 p.170).
L/S equity typical exposures::40-60% net long, from gross 70-90% long vs 20-50% short; targets long-only returns at about half the standard deviation (V8 p.173).
What share of all hedge funds is L/S equity?::About 30% (V8 p.172).
Are L/S equity managers good market timers?::Generally no; they are too net long at highs and not net long enough at lows, so stock selection defines skill (V8 p.172).
Dedicated short vs short-biased exposure bands::Dedicated short 60-120% short at all times; short-biased about 30-60% net short with some value or index long offsets (V8 p.177).
Two accounting screens used by short sellers::Altman Z-score for bankruptcy potential and Beneish M-score for potentially fraudulent statements (V8 p.178).
Alternative uptick rule::After a stock falls 10% or more from the prior close, US short sales may execute only above the current best bid (V8 p.176).
Activist short selling legality conditions::Not manipulation if the research is not erroneous, not sold for fees, and done in the limited partners' best interests (V8 p.175).
EMN portfolio construction (four steps)::Screen a liquid, shortable universe; analyze with fundamental or momentum models; construct with beta/sector/dollar neutrality constraints; set leverage weighing costs and drawdown risk (V8 p.182).
EMN maximum leverage and its key risk::Up to 300% long vs 300% short via prime broker portfolio margining; forced downsizing after an excess drawdown (V8 p.181).
Stub trading::Long or short a parent against its subsidiaries weighted by ownership percentages (short 1 A, buy 0.90 B and 0.75 C if A owns 90% and 75%) (V8 p.180).
When are EMN managers most useful in an allocation?::Non-trending or declining markets; also as a substitute for fixed income when yields are unattractively low (V8 p.181).
Soft-catalyst vs hard-catalyst event investing::Soft positions before any announcement; hard reacts to announced events and is less volatile and less risky (V8 p.183).
Merger arbitrage sizing in a stock-for-stock deal::Buy the target and short the acquirer in the offer ratio, so target shares convert exactly into the short at closing (V8 p.184).
Typical merger-arb spread and annualized net returns::3-7% spreads per deal; 7-12% net annualized with capital recycled 3-4 times a year and leverage of 3-5 times (V8 p.184).
Share of announced US mergers that close::Roughly 70-90% (V8 p.184).
Merger arbitrage payoff profile::Riskless bond plus a short put, with an embedded long call on a White Knight higher bid (V8 p.185).
Which deals carry wider merger spreads?::Cross-border deals (two governmental approvals) and vertical integrations facing antitrust scrutiny; hostile deals also close less often than friendly ones (V8 p.184, p.185).
Merger-arb hedge against deal failure using options::Buy out-of-the-money calls on the acquirer (covers the short) and out-of-the-money puts on the target (protects the long) (V8 p.186).
Bankruptcy liquidation payment priority::Senior secured, junior secured, unsecured, convertible debt, preferred stock, common stock (V8 p.188).
Fulcrum securities::Partially-in-the-money claims not expected to be repaid in full whose holders end up owning the reorganized company (V8 p.189).
Distressed securities leverage and liquidity profile::Long-biased, 1.2-1.7 times NAV leverage, long lock-ups and gates, Level 3 mark-to-model pricing with return smoothing (V8 p.187, p.189).
When is distressed investing most attractive?::Early stages of an economic recovery after a period of market dislocation (V8 p.189).
Classic fixed-income arbitrage carry trade::Long off-the-run, short duration-matched on-the-run governments; rates and credit hedged, liquidity risk remains; payoff resembles a short put (V8 p.194).
Fixed-income arbitrage leverage norms::4-5 times assets to equity, up to 12-15 times inside some market-neutral multi-strategy funds, financed via repo with haircuts (V8 p.192, p.193).
Convertible bond decomposition::Straight debt plus a long call with exercise price equal to strike times conversion ratio (V8 p.195).
Conversion price formula::Convertible bond price divided by the conversion ratio (V8 p.196).
Why do convertibles trade at cheap implied volatility?::They are complex, thinly traded, small-issue, often non-rated securities, and pricing cheapens further when new issuance is heavy (V8 p.196).
Convertible arbitrage classic setup::Buy the undervalued convertible, short delta-adjusted stock; positive gamma means selling more stock as it rises and buying as it falls (V8 p.197).
Convertible arbitrage book structure::About 300% long vs 200% short; the short is smaller because it is sized to the convertible's delta (V8 p.197).
Convertible arbitrage works best when::Issuance is high, volatility is moderate, and market liquidity is reasonable; it fares worst in acute credit weakness and illiquidity (V8 p.197).
Global macro implementation profile::Top-down, discretionary or systematic, anticipatory and often contrarian; margin-to-equity of 15-25% controls 6-7 times fund assets (V8 p.201).
Why is global macro diversification weaker than it looks?::Risk-on/risk-off conditions driven by central banks correlate positions across asset classes (V8 p.202).
Managed futures capital structure::85-90% of capital in short-term government collateral; 10-15% margins the futures; futures margins run 0.1%-10% of notional vs 50% for US equities (V8 p.204, p.205).
Time-series vs cross-sectional momentum::{{TSM}} trades absolute past returns per asset and can be net long or short everything; {{CSM}} ranks assets within a class, long top half, short bottom half, roughly market neutral (V8 p.206).
Managed futures return skewness::Positive right-tail skewness in periods of market stress, useful for balancing negatively skewed strategies (V8 p.204, p.206).
Four exit methodologies of managed futures managers::Price target, momentum reversal, time-based, trailing stop-loss (or combinations) (V8 p.205).
Equity volatility correlation with equity returns::Approximately 80% negative, making long volatility a natural equity hedge (V8 p.208).
Four paths to implement a volatility strategy::Exchange-traded options, OTC options (custom, counterparty risk), VIX futures/options (pure vol view, no delta hedging), volatility or variance swaps (V8 p.209, p.210).
Vega vs gamma across option tenors::Longer-dated options have more vega (absolute volatility exposure); shorter-dated options have more gamma (delta sensitivity) (V8 p.209).
Variance swap vs volatility swap::Both are forwards on realized outcomes struck at fair value; the variance swap pays notional times (realized variance minus strike variance), variance being the square of volatility (V8 p.210).
Volatility roll down::With an upward-sloping volatility term structure, the passage of time accelerates option price decay, hurting long volatility positions (V8 p.209).
Three life settlement characteristics a fund wants::Low surrender value offered, low ongoing premiums, high probability of death earlier than standard actuarial predictions (V8 p.213).
Three conditions for attractive catastrophe reinsurance::Policy diversity by geography and type, a sufficient loan loss reserve buffer, and enough premium income (V8 p.213).
FoF fee norms, historical and current::Historically 1% and 10% on top of underlying 1-2% and 10-20%; compressing toward 50 bps plus 5% or a 1% flat fee (V8 p.215).
Fee netting risk::An FoF investor pays incentive fees to winning underlying funds even when losers make the aggregate return flat or negative; multi-strategy GPs absorb it except under pass-through fee models (V8 p.218).
Typical minimums, direct vs FoF::Most hedge funds require $500,000 to $5 million minimums ($1 million typical); an FoF can be accessed for about $100,000 (V8 p.216).
Multi-strategy vs FoF scorecard::Multi-strategy has faster tactical shifts, full transparency, GP-absorbed netting, but concentrated operational risk and higher leverage; FoF has diverse strategies and diversified operational risk but double fees, netting risk, opacity, slow reaction (V8 p.219).
The conditional factor model's four retained factors::SNP500, CREDIT (Baa minus Aaa), USD, VIX (first difference); BOND and CMDTY dropped via stepwise regression for multicollinearity (V8 p.223, p.226).
Crisis window used in the conditional model::June 2007 to February 2009, when the dummy equals 1 (V8 p.223).
Total crisis exposure in a conditional model::Normal beta plus the D-factor increment (US L/S equity 0.58 + 0.03 = 0.61) (V8 p.229).
What does a significant negative DVIX mean?::The fund gets shorter volatility in crises, losing as the VIX spikes; 60% of FoF-equity funds showed this despite only 2% having negative VIX exposure normally (V8 p.234).
Did multi-manager funds hedge the global financial crisis?::No; no significant negative DSNP500 appeared, so diversification across hedge fund strategies did not reduce crisis risk (V8 p.233).
What does high Rho (serial autocorrelation) signal?::Smoothed returns from illiquid holdings, hence understated volatility; multi-strategy funds run Rho above 20% (V8 p.227, p.232).
Sharpe vs Sortino::Sharpe penalizes upside and downside variability (standard deviation); Sortino penalizes only downside deviation below a target, better for strategies with large negative events (V8 p.236).
Best combined-portfolio Sharpe among 48/32/20 mixes::Systematic futures at 0.83 with the lowest SD (6.94%); merger arbitrage and global macro gave the smallest maximum drawdowns near 5-6% (V8 p.236, p.239).
Which strategies fail to cut drawdowns when added to 60/40?::L/S equity, event-driven/distressed, and convertible arbitrage, because their equity and credit exposures bind in crises (V8 p.238, p.239).
A 90% variance constraint on an 8% SD portfolio allows what SD?::sqrt(0.9) x 8 = 7.59%; take the square root of the variance cap, never 90% of the SD (V8 p.259).

Merger arb quick numeric: buy 22,500 T at 20, short 15,000 A at 45 (offer 2 A per 3 T); success payoff?
?
Proceeds 675,000 minus cost 450,000 = 225,000; on failure with reversion to T 15 / A 50, lose 112,500 + 75,000 = 187,500 (V8 p.261).

Convertible quick numeric: bond at 115% of par 1,000, ratio 50, stock 28; locked profit per share?
?
Conversion price = 1,150/50 = 23; profit = 28 - 23 = 5 per share regardless of small stock moves (V8 p.262).

FoF fees quick numeric: fund grosses 20% at 2/20, FoF charges 1/10; investor net?
?
Fund net = 20 - 2 - 0.2(18) = 14.4%; FoF net = 14.4 - 1 - 0.1(13.4) = 12.06% (V8 p.220).

## Common mistakes

1. Computing the merger-arb payoff from pre-announcement prices instead of the post-announcement prices at which the position was established (the EUR 412,500 distractor) (V8 p.261).
2. Reversing the failure-case hedge: the protection is calls on the acquirer and puts on the target, because the short acquirer leg loses as its price rebounds (V8 p.256, p.257).
3. Claiming convertible arbitrage profits more when the stock falls (or rises); near conversion value the legs cancel and the profit equals share price minus conversion price either way (V8 p.262).
4. Forgetting the carry adjustments in convertible arbitrage: borrow cost and dividends owed reduce profit, the coupon per share (coupon divided by conversion ratio) adds back (V8 p.199).
5. Labeling the off-the-run vs on-the-run trade a yield curve or credit trade; it is a carry trade whose surviving risk is liquidity (V8 p.194, p.257).
6. Confusing TSM and CSM: absolute-signal TSM can be net long or short an entire sector; ranked CSM stays near market neutral, and "net holding is market neutral" identifies CSM (V8 p.206, p.258).
7. Treating the D coefficients of the conditional factor model as total crisis exposure rather than increments to be added to the normal beta (V8 p.229, p.231).
8. Assuming exposures absent in calm markets stay absent: negative DVIX and DUSD loadings emerge in crises, especially for FoF and levered strategies (V8 p.234).
9. Ranking on Sharpe or maximum drawdown when the committee expects large negative events; the Sortino ratio is the stated risk-adjusted measure, with drawdown as a separate constraint (V8 p.259, p.260).
10. Converting a variance constraint by multiplying standard deviation by the percentage instead of taking the square root of the scaled variance (V8 p.259).
11. Crediting FoFs with tactical speed or multi-strategy funds with diversified operational risk; each attribute belongs to the other structure (V8 p.259).
12. Flipping life settlement criteria: the fund wants low surrender value, low premiums, and earlier-than-actuarial mortality, not high surrender value or on-schedule mortality (V8 p.262).
13. Believing selling volatility hedges a crisis; the seller is the insurer who pays out when volatility spikes, and only long volatility protects (V8 p.258, p.259).
14. Expecting multi-manager diversification to protect in crises; the conditional model shows no significant negative crisis equity exposure, and liquidity, volatility, and credit risks magnified by leverage dominate (V8 p.233).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "08-04" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
