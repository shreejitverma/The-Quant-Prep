---
type: cfa-lm
topic: "Corporate Issuers"
topic_code: "04"
topic_slug: "04-Corporate-Issuers"
volume: 4
lm: 1
title: "Analysis of Dividends and Share Repurchases"
pages: "3-65"
weight_band: "5-10%"
difficulty: 2
los_count: 14
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/corporate-issuers]
---

# LM1: Analysis of Dividends and Share Repurchases

Difficulty 2 of 5: fourteen LOS but only four calculation engines (effective tax rates, the target payout adjustment model, buyback EPS, buyback BVPS), each one three keystrokes deep; the danger is conceptual traps about wealth effects and signaling, not arithmetic.

## LOS map

- **describe** the expected effect of regular cash dividends, extra dividends, liquidating dividends, stock dividends, stock splits, and reverse stock splits on shareholders' wealth and a company's financial ratios (V4 p.4) ^los-04-01-a
    - Examiner asks: given a stock dividend or split, state that shareholder wealth, P/E, payout ratio, liquidity ratios and leverage ratios are unchanged, while a cash dividend lowers the current ratio and raises leverage.
- **compare** theories of dividend policy and explain implications of each for share value given a description of a corporate dividend action (V4 p.11) ^los-04-01-b
    - Examiner asks: match MM irrelevance, bird in the hand and tax aversion to a described dividend action, or identify which MM assumption a statement violates (homemade dividends, flotation costs, symmetric information).
- **describe** types of information (signals) that dividend initiations, increases, decreases, and omissions may convey (V4 p.13) ^los-04-01-c
    - Examiner asks: a company initiates or cuts a dividend and the question asks what the market most likely infers about future earnings, including the rare positive-cut case (Telstra, Skanska) and why mimicking is costly.
- **explain** how agency costs may affect a company's payout policy (V4 p.13) ^los-04-01-d
    - Examiner asks: which company should raise its dividend to curb overinvestment (weak governance, strong cash flow, few projects), and how paying dividends transfers wealth from bondholders and invites covenant restrictions.
- **explain** factors that affect dividend policy in practice (V4 p.20) ^los-04-01-e
    - Examiner asks: given a scenario (dividend cut amid volatile earnings, a debt covenant, high flotation costs), name which of the six factors is driving the decision.
- **calculate** and interpret the effective tax rate on a given currency unit of corporate earnings under double taxation, dividend imputation, and split-rate tax systems (V4 p.20) ^los-04-01-f
    - Examiner asks: corporate rate 40%, dividend rate 30%, compute the double-taxation effective rate 58%, or state that under imputation the effective rate is simply the shareholder's marginal rate.
- **compare** stable dividend with constant dividend payout ratio, and calculate the dividend under each policy (V4 p.26) ^los-04-01-g
    - Examiner asks: apply the target payout adjustment model with a previous dividend, expected earnings, a target ratio and an adjustment factor, or spot from a DPS table the quarter a company switched to a constant payout ratio.
- **describe** broad trends in corporate payout policies (V4 p.26) ^los-04-01-h
    - Examiner asks: whether the fraction of dividend payers is rising or falling in developed markets, and how repurchases have trended relative to dividends since the 1980s and through recessions.
- **compare** share repurchase methods (V4 p.31) ^los-04-01-i
    - Examiner asks: which method maximizes flexibility (open market), which is fastest (fixed price tender), which minimizes cost among tenders (Dutch auction), and which can transfer wealth (direct negotiation at a premium).
- **calculate** and compare the effect of a share repurchase on earnings per share when 1) the repurchase is financed with the company's surplus cash and 2) the company uses debt to finance the repurchase (V4 p.31) ^los-04-01-j
    - Examiner asks: compute post-buyback EPS with borrowed funds and apply the rule that EPS rises only when the earnings yield exceeds the after-tax cost of debt.
- **calculate** the effect of a share repurchase on book value per share (V4 p.31) ^los-04-01-k
    - Examiner asks: buy back at a market price above (below) BVPS and show BVPS falls (rises), with the divide-by-remaining-shares arithmetic.
- **explain** the choice between paying cash dividends and repurchasing shares (V4 p.37) ^los-04-01-l
    - Examiner asks: state that a repurchase at the market price is wealth-equivalent to a cash dividend of equal size absent tax and information differences, and list the five extra motives for repurchases.
- **calculate** and interpret dividend coverage ratios based on 1) net income and 2) free cash flow (V4 p.48) ^los-04-01-m
    - Examiner asks: compute payout, earnings coverage and the FCFE coverage ratio FCFE/(dividends + repurchases) from a CFO, FCInv and net borrowing table, and interpret a ratio below 1.
- **identify** characteristics of companies that may not be able to sustain their cash dividend (V4 p.48) ^los-04-01-n
    - Examiner asks: pick the company most at risk of a cut from clues like coverage near 1.0, an abnormally high dividend yield, borrowing to pay the dividend, or a past record of cuts.

## Core intuition

A dividend is a discretionary distribution declared by the board; on the ex-dividend date the share price is expected to drop by the amount of the dividend, because the buyer on that date no longer receives the payment (V4 p.4).
Payout policy is the broader set of principles governing both cash dividends and share repurchases, and the whole module is one long meditation on a single question: can the way a company hands cash back to its owners change the owners' wealth (V4 p.4)?

Start with what does nothing.
A stock dividend, a stock split and a reverse split reshuffle the number of claims on an unchanged asset base and unchanged earning power.
More shares each carrying proportionally less earnings, at an unchanged P/E, leaves total market value, each holder's ownership fraction and each holder's wealth exactly where they were (V4 p.7, p.8).
The shareholder's total cost basis is also unchanged; only the cost per share falls (V4 p.7).
Nothing real moved: no cash left the company, so liquidity ratios and leverage ratios are untouched (V4 p.8).
The only distinction between a 100% stock dividend and a two-for-one split is bookkeeping: the stock dividend transfers retained earnings into contributed capital, the split touches no equity account (V4 p.9).
A cash dividend is different in kind: cash and retained earnings actually leave, so the current and cash ratios fall and debt-to-equity and debt-to-assets rise (V4 p.8).
A liquidating dividend is a return of capital, not a distribution of earnings: the company is winding down, selling a business, or paying beyond accumulated retained earnings (V4 p.7).

> [!abstract] Idea 1: distributions rearrange claims; only real cash flows change ratios, and no distribution mechanism by itself creates wealth
> Stock dividends and splits change per-share magnitudes and nothing else (V4 p.8, p.9).
> Cash dividends and repurchases move real cash, so they shrink assets and equity and raise leverage (V4 p.8, p.34).
> A repurchase at the market price and a cash dividend of the same total are wealth-equivalent when taxes and information content do not differ (V4 p.38).

Now the theory war.
Miller and Modigliani argue that with no taxes, no transaction costs and symmetric information, dividend policy is irrelevant: the investment and financing decisions fix firm value, and paying a dividend financed by a new share issue just swaps value out the door and back in, dropping the price by exactly the dividend (V4 p.11).
The deep mechanism is the homemade dividend: an investor who wants income sells shares, and an investor who does not want income reinvests the dividend, so policy alternatives are only trades between dividend streams of equal present value (V4 p.12).
Note the precision of the claim: dividends matter to value, dividend policy does not.
The real world bites back through flotation costs of 4% to 10% on new equity, transaction costs and taxes on the homemade route, and volatile prices that force selling more shares in downturns (V4 p.12).
The bird in the hand school says a unit of dividend is less risky than a unit of expected capital gain, so payers enjoy a lower cost of equity; MM answer that paying today's dividend does not change the risk of future cash flows, it only lowers the ex-dividend price (V4 p.12).
The tax aversion school says that where dividends are taxed more heavily than capital gains, taxable investors prefer low payout and repurchases, taken to its extreme a zero payout (V4 p.12, p.13).

Signaling exists because information is asymmetric: managers know more, and cash is a credible messenger where words are cheap.
A dividend increase is costly to mimic, because a firm without the cash flows cannot sustain it for long, and that cost is exactly what makes the signal informative (V4 p.13, p.14).
Empirically, initiations and increases are associated with future earnings growth, omissions and cuts with future earnings problems (V4 p.13).
Consistent dividend growers share a profile: dominant positions, global operations, less volatile earnings, high returns on assets, low debt (V4 p.15).
But the sign can flip: Telstra cut 30% to reinvest and was ultimately read as prudent, BT cut its interim dividend and the shares rose 6.9% because the cut was prudent relative to a 71% collapse in operating cash flow (V4 p.15, p.16).
The eBay initiation shows the two-sided reading of the same act: confidence in cash generation, or confession that high-return reinvestment has run out (V4 p.16, p.17).

Agency costs give payout a disciplinary role.
Managers who control free cash they do not own may overinvest in negative NPV projects that grow their span of control; Jensen's free cash flow hypothesis says paying out free cash flow starves that temptation (V4 p.17).
That is why the market reaction to dividend changes is stronger for companies with greater overinvestment potential, and why investors push cash-rich, opportunity-poor, weakly governed companies to raise payout (V4 p.17, p.18).
The mirror-image conflict is with bondholders: dividends and repurchases thin the cash cushion behind fixed claims and raise default risk, so indentures cap distributions, demand EBITDA or EBIT coverage of interest, and forbid dividends financed by asset sales or new debt (V4 p.17, p.18).
The electric utility case is the elegant twist: utilities pay high dividends and then issue equity, using the equity market's pricing of the new shares to monitor both managers and rate-setting regulators (V4 p.18, p.19).

Six practical factors shape policy: investment opportunities, expected earnings volatility, financial flexibility, taxes, flotation costs, and contractual and legal restrictions (V4 p.20).
Growth firms with rapid, unpostponable opportunities hold cash and pay little; utilities pay much (V4 p.20).
Managers smooth dividends against volatile earnings, care more about changes than levels, and hate reversible increases (V4 p.21).
Flexibility explains precautionary cuts (Skanska) and the preference for repurchases, which create no expectation of continuation (V4 p.21, p.22).
Flotation costs make internal equity cheaper than new shares, so companies avoid dividend levels that would force issuance (V4 p.24).
Legal regimes range from mandated dividends (Brazil) to impairment-of-capital rules (US, Canada), and cumulative preference dividends in arrears block common dividends (V4 p.25).

> [!abstract] Idea 2: the tax system decides who really taxes the marginal unit of earnings
> Double taxation stacks the personal rate on the after-corporate-tax residual, so the effective rate is $t_c + (1 - t_c)t_d$ (V4 p.22).
> Imputation hands the shareholder a franking credit for corporate tax paid, so the effective rate collapses to the shareholder's own marginal rate, with a refund if that rate is below the corporate rate (V4 p.23).
> Split-rate taxes distributed earnings at a lower corporate rate than retained earnings, then taxes the dividend as ordinary income, so it is double taxation with a smaller first bite (V4 p.23, p.24).

Payout policies come in two testable flavors.
A stable dividend policy keys the dividend to long-term sustainable earnings and smooths through cycles; Lintner's target payout adjustment model formalizes it, moving the dividend a fraction of the way toward the target payout each year (V4 p.26, p.28).
The corollaries are exam gold: dividends can rise in a year earnings fall, and the payout ratio can drift away from target when earnings grow fast (V4 p.28, p.29).
A constant payout ratio policy applies a fixed percentage to current earnings, so the dividend inherits all the earnings volatility; it is rare in practice (V4 p.29).
Trend facts: the fraction of dividend payers has declined long-term in developed markets while aggregate amounts and payout ratios rose, payers are larger and more profitable with fewer growth options, repurchases have trended up since the early 1980s in the US and 1990s in Europe, and better governance and disclosure are associated with fewer initiations because the signaling role fades (V4 p.30, p.31).

Repurchases are the second distribution channel, and they use real corporate cash; repurchased shares become treasury shares or are canceled, and drop out of dividends, voting and EPS (V4 p.31).
Four methods, in order of importance: open market purchases (maximum flexibility, no obligation to complete, cost-effective timing), fixed price tender offers (fast, premium-priced), Dutch auctions (a tender across a price range that discovers the minimum clearing price, cheaper than fixed price, nearly as fast), and direct negotiation (premium deals with a large holder, greenmail in the ugly cases, discounts when the seller needs liquidity) (V4 p.32, p.33).
Unlike a declared dividend, an announced repurchase is not a commitment, and cash goes only to those who sell (V4 p.32).

> [!abstract] Idea 3: a buyback changes EPS through a race between the earnings yield and the cost of the money used
> Fund the buyback with borrowed money and EPS rises only if the earnings yield E/P exceeds the after-tax cost of debt; equal rates leave EPS unchanged (V4 p.36).
> Fund it with surplus cash and EPS rises only if that cash was earning less than its cost of capital, which near-zero-yield cash always satisfies (V4 p.36).
> A higher EPS is not higher wealth: leverage rises, the required return rises, and the same free cash flow supports the same value (V4 p.36, p.41).

The BVPS effect is pure averaging: buying back shares at a price above book value per share dilutes book value down, and buying below book value accretes it up (V4 p.37).
Wealth equivalence holds at the market price: paying a special dividend of the full free cash flow or repurchasing at the market price leaves every shareholder, seller or not, with the same total wealth (V4 p.38).
Pay a premium to one shareholder in a negotiated repurchase and the premium is a wealth transfer from everyone else (V4 p.39).
Companies still prefer repurchases for identifiable reasons: tax advantages where capital gains rates are lower or deferrable, undervaluation signaling, managerial flexibility, offsetting option dilution, and raising leverage (V4 p.40, p.41).
Repurchases are procyclical, collapsing in recessions when cash dries up, while dividends are cut far more reluctantly (V4 p.43, p.44).

Finally, dividend safety.
The traditional metrics are the payout ratio and its inverse, the coverage ratio; mature companies target payouts of 40% to 60%, coverage of about 1.7x to 2.5x, and coverage at 1.0 puts the dividend in jeopardy (V4 p.48).
But earnings are not cash: FCFE, which is CFO minus fixed capital investment plus net borrowing, is what actually funds distributions, so the sharper test is the FCFE coverage ratio against dividends plus repurchases (V4 p.49, p.50).
Below 1 the company is draining liquidity and the policy is unsustainable; supporting distributions by cutting productive capex or adding debt is the classic warning (V4 p.49, p.51).
Outside the accounts, an abnormally high dividend yield against the company's own history is the market pricing in a cut (Madden's high-yield universe, StarHub at 9.4% before its cut), and past cuts, high leverage and volatile earnings complete the risk profile (V4 p.52).

## Formulas and derivations

**Formula 1: dividend payout ratio and dividend coverage ratio** (V4 p.6, p.48)
$$
\text{Payout ratio} = \frac{\text{Dividends}}{\text{Net income}} = \frac{DPS}{EPS}, \qquad \text{Dividend coverage} = \frac{\text{Net income}}{\text{Dividends}}
$$
^f-04-01-1

Dividends and net income are common-share amounts over the same period; the two ratios are reciprocals.
Payout measures the share of earnings distributed; coverage measures the earnings cushion behind the dividend, with 1.7x to 2.5x typical for mature payers and 1.0 the jeopardy line (V4 p.48).

**Formula 2: expected ex-dividend price drop** (V4 p.4)
$$
P_{ex} = P_{cum} - D
$$
^f-04-01-2

$P_{cum}$ is the price with the dividend right attached and $D$ is the declared dividend per share.
The buyer on the ex-date forgoes a cash flow worth $D$, so arbitrage forces the price down by that amount, all else equal; this is also the MM mechanism by which a payout policy cannot add value (V4 p.11).

**Formula 3: per-share values after a stock dividend or split** (V4 p.7, p.9)
$$
\text{New per-share amount} = \frac{\text{Old per-share amount}}{1 + \text{stock dividend \%}} = \text{Old per-share amount} \times \frac{\text{old shares}}{\text{new shares}}
$$
^f-04-01-3

Applies to price, EPS, DPS and BVPS alike; a two-for-one split halves them, a 5% stock dividend divides them by 1.05, a 1-for-10 reverse split multiplies them by 10.
Total equity, total market value, P/E, payout ratio, dividend yield and every liquidity and leverage ratio are unchanged, because no resource entered or left the firm (V4 p.8, p.9).

**Formula 4: effective tax rate under double taxation** (V4 p.22, p.65)
$$
ETR = t_c + (1 - t_c)\,t_d = 1 - (1 - t_c)(1 - t_d)
$$
^f-04-01-4

$t_c$ is the corporate tax rate and $t_d$ the shareholder's tax rate on dividends, both as decimals.
Of one unit of pretax earnings, $(1 - t_c)$ survives corporate tax, and the shareholder keeps $(1 - t_d)$ of that, so the retained fraction is the product and the effective rate is its complement.

> [!tip] Calculator
> BA II Plus for $t_c = 40\%$, $t_d = 30\%$: 1 - 0.4 = × ( 1 - 0.3 ) = gives 0.42 kept, so ETR = 58%.
> Or additively: 0.4 + 0.6 × 0.3 = 0.58.

**Formula 5: effective tax rate under dividend imputation** (V4 p.23)
$$
ETR = t_{shareholder}, \qquad \text{Tax due (refund)} = t_{s} \times \text{Pretax income} - \text{Corporate tax paid}
$$
^f-04-01-5

The franking credit imputes corporate tax paid to the shareholder, so distributed profits end up taxed once at the shareholder's marginal rate.
A 15% shareholder facing a 30% corporate rate receives a credit for the 15-point difference; a 47% shareholder pays the 17-point difference (V4 p.23).

**Formula 6: effective tax rate under a split-rate system** (V4 p.23, p.24)
$$
ETR = t_{c,div} + (1 - t_{c,div})\,t_d
$$
^f-04-01-6

$t_{c,div}$ is the lower corporate rate on earnings allocated to dividends; retained earnings bear the higher rate.
Structurally identical to double taxation with the reduced first-layer rate: per 100 of distributed pretax earnings taxed at 20% corporate and 35% personal, the shareholder nets $(1 - 0.35) \times 80 = 52$ and the effective rate is $20\% + 80 \times 0.35\% = 48\%$ (V4 p.24).

**Formula 7: target payout adjustment model (Lintner)** (V4 p.28, p.29)
$$
D_1 = D_0 + \left(E_1 \times \text{Target payout} - D_0\right) \times A, \qquad A = \frac{1}{\text{years to adjust}}
$$
^f-04-01-7

$D_0$ is the previous dividend per share, $E_1$ expected earnings per share, and $A$ the adjustment factor.
$E_1 \times$ target payout is the destination dividend; the firm closes only the fraction $A$ of the gap each year, which is why dividends respond sluggishly to earnings and can still rise in a soft year as long as the implied dividend keeps moving toward target (V4 p.28).

> [!tip] Calculator
> BA II Plus for Example 10: 2.8 × 0.3 = − 0.4 = × 0.25 = + 0.4 = gives 0.51.
> Always key the target dividend first, subtract the old dividend, multiply by the adjustment factor, then add back the old dividend.

**Formula 8: dividend under a constant payout ratio policy** (V4 p.29, p.30)
$$
D_t = EPS_t \times \text{payout ratio}
$$
^f-04-01-8

The fixed ratio is applied to current earnings, so the dividend inherits the full volatility of earnings; Pampas paid exactly 25% of each quarter's EPS (V4 p.30).
Contrast with the stable policy, where the base is long-term sustainable earnings and short-term swings are smoothed away (V4 p.27).

**Formula 9: EPS after a debt-financed buyback** (V4 p.36)
$$
EPS_{after} = \frac{\text{Earnings} - \text{After-tax cost of borrowed funds}}{\text{Shares outstanding after buyback}}
$$
^f-04-01-9

The numerator subtracts the annual after-tax interest on the borrowing (amount borrowed times the after-tax rate); the denominator drops the repurchased shares.
For a surplus-cash buyback the interest term is instead the after-tax income the cash was earning, which for near-zero-yield cash is nothing, so EPS mechanically rises (V4 p.35).

> [!tip] Calculator
> BA II Plus for Selamat at 6%: 12 × 0.06 = gives 0.72; 6.6 − 0.72 = ÷ 2 = gives 2.94.

**Formula 10: the earnings-yield rule for buyback EPS** (V4 p.36)
$$
EPS \uparrow \iff \frac{E}{P} > r_d(1 - t), \qquad EPS \downarrow \iff \frac{E}{P} < r_d(1 - t)
$$
^f-04-01-10

$E/P$ is the earnings yield (the reciprocal of P/E) and $r_d(1 - t)$ the after-tax borrowing rate.
Each repurchased share removes $E/P$ of earnings claim per unit of price paid, while the borrowed unit costs $r_d(1 - t)$; the buyback accretes EPS when the claim removed exceeds the financing cost, and equality leaves EPS exactly unchanged (V4 p.36).
For internally financed buybacks, the analogous comparison is the earnings yield against the after-tax return the surplus cash was earning; EPS increases only if the funds would not earn their cost of capital if retained (V4 p.36).

**Formula 11: book value per share after a buyback** (V4 p.37)
$$
BVPS_{after} = \frac{\text{Book equity} - (\text{Shares bought} \times \text{Price paid})}{\text{Shares} - \text{Shares bought}}
$$
^f-04-01-11

Buying back at a price above the pre-buyback BVPS averages a high-cost removal into a lower book base, so BVPS falls; buying below BVPS raises it; buying exactly at BVPS leaves it unchanged (V4 p.37).
The direction test costs no arithmetic: compare market price with BVPS before computing anything.

**Formula 12: share price after a distribution at market price** (V4 p.38, p.39)
$$
P_{after} = \frac{\text{Market value of equity} - \text{Cash distributed}}{\text{Shares outstanding after}}
$$
^f-04-01-12

For a cash dividend, shares are unchanged and the price drops by the dividend; for a repurchase at the market price, shares fall by cash over price and the price is unchanged; either way one share's total wealth (cash plus ex-distribution value) is identical, which is the equivalence proposition (V4 p.38).
If the repurchase price exceeds the market price, remaining shareholders bear the premium: the post-repurchase price falls below the market price and the seller captures the difference (V4 p.39).

**Formula 13: free cash flow to equity** (V4 p.50)
$$
FCFE = CFO - FCInv + \text{Net borrowing}
$$
^f-04-01-13

CFO is cash flow from operations, FCInv is fixed capital investment (capital expenditures), and net borrowing is new debt less repayments (negative when debt is repaid).
FCFE is the cash actually available for distribution after the reinvestment the business needs, which is why safety analysis prefers it to accounting earnings (V4 p.49, p.50).

**Formula 14: FCFE coverage ratio** (V4 p.49)
$$
\text{FCFE coverage} = \frac{FCFE}{\text{Dividends} + \text{Share repurchases}}
$$
^f-04-01-14

Equal to 1 means every available unit of cash is being returned; well above 1 means the company is banking liquidity; significantly below 1 means distributions are funded by draining cash, cutting capex or borrowing, which is unsustainable (V4 p.49).

## Worked examples

### Example 1: AfriSage Technologies' dividend policy (V4 p.6, p.7)

AfriSage pays at least 35% of net income as an ordinary dividend; 632.5 million shares; EPS ZAR14.23 (2018) and ZAR12.65 (2017); DPS ZAR7.61 (2018) and ZAR10.68 (2017).
Step 1, payout ratios: $7.61 / 14.23 = 0.5348$, so 53.5% for 2018; $10.68 / 12.65 = 0.8443$, so 84.4% for 2017 (Python: `7.61/14.23 = 0.53478`, `10.68/12.65 = 0.84427`).
Step 2, minimum ordinary dividend for 2018 under the 35% floor: $14.23 \times 0.35 = 4.98$ per share (Python: `14.23*0.35 = 4.9805`).
Step 3, the extra dividend is the excess actually paid: $7.61 - 4.98 = 2.63$ per share.
Interpretation: the policy splits the observed dividend into a committed ordinary layer and a discretionary extra layer that flexes with excess capital. ^ex-04-01-1

### Example 2: Globus Maritime announces a reverse split (V4 p.10)

Globus, below NASDAQ's USD 1 minimum for 30 days, announces a 1-for-10 reverse split with the shares at USD 4.25.
Step 1, price after the reverse split: each new share replaces 10 old ones, so $10 \times 4.25 = 42.50$ (Python: `10*4.25 = 42.5`).
Step 2, the statement "shareholder wealth is negatively affected by a reverse stock split" is not generally correct: the reverse split by itself leaves market capitalization unchanged.
The price could rise if the market reads retained listing as good news, or fall for unrelated reasons like weak growth or thin float, but the split itself is wealth-neutral (V4 p.10). ^ex-04-01-2

### Example 3: historical examples of dividend initiations (V4 p.14)

Oracle initiated a USD 0.05 quarterly dividend in May 2009; the roughly USD 1 billion annual cost was small against USD 8 billion of operating cash flow and USD 9 billion of cash, and an analyst read the initiation as a signal that Oracle could ride out the downturn and gain share.
Eurotunnel initiated its first dividend in mid-2009 after a debt restructuring and insurance recovery, with the CEO calling it a return to normality and to expected profitability.
Takeaway: an initiation is credible evidence of management confidence because it commits cash, and both initiations conveyed value-relevant information beyond words (V4 p.13, p.14). ^ex-04-01-3

### Example 4: signaling with dividends and the costs of mimicking (V4 p.14, p.15)

Management of a company with poor prospects proposes a dividend increase so investors will infer good prospects.
Step 1, will it work long term? No.
Step 2, why: a company whose cash flows will not grow cannot maintain the higher dividend; it must later cut the dividend or raise new debt or equity to fund it, and both events trigger downward price revisions on average.
The cost of mimicking is precisely what makes the dividend increase informative when a genuinely strong company does it (V4 p.13, p.15). ^ex-04-01-4

### Example 5: dividend reductions and price increases (V4 p.16)

BT Group cut its interim dividend from 4.85p to 4.62p while net cash flow from operating activities fell 71% to GBP 754 million and revenue fell 2%, even as pretax profit rose to GBP 1.3 billion and adjusted EBITDA rose 2%.
The shares rose 6.9% to 257p as the market digested the cut.
Mechanism: with cash generation collapsing, a modest cut was read as prudent stewardship rather than distress, protecting an attractive yield near 6.4%; the case proves that context, not the direction of the change alone, sets the sign of the signal (V4 p.16).
Note the profit-versus-cash divergence: the earnings numbers rose while cash fell, and the market followed the cash. ^ex-04-01-5

### Example 6: agency issues and dividends (V4 p.18)

Companies A and B are all-equity competitors with 35% average payouts; B has weaker governance (CEO is also board chair) and now fewer profitable opportunities, while both have strong operating cash flow.
Answer: B, because a dividend increase may mitigate potential overinvestment agency problems.
Strong cash flow plus shrinking opportunities plus weak governance is exactly Jensen's free cash flow setup: managers may spend the surplus on negative NPV empire building, and a higher payout removes the fuel.
A is wrong because better growth prospects argue for retention, not higher payout; the underinvestment variant (C) is the bondholder conflict, not present in an all-equity firm (V4 p.17, p.18). ^ex-04-01-6

### Example 7: electric utilities, agency costs, and dividends (V4 p.18, p.19)

Utilities pay high dividends and then issue new equity, which looks irrational since new equity is expensive.
The resolution: the dividend-then-issue cycle forces the company to face the equity market repeatedly.
If regulators set rates too low or managers consume perks, the new shares price poorly, the utility cannot fund capacity growth, customers and voters feel it, and regulators are pressured back to fair rates.
The equity market becomes the monitor that arbitrates both the manager-shareholder and the regulator-shareholder conflicts, and the flotation cost is the price of that monitoring (V4 p.18, p.19). ^ex-04-01-7

### Example 8: a company that needs to reinvest all internally generated funds (V4 p.24, p.25)

Boar's Head Spirits pays no dividend, has operating cash flow of GBP 500 million, cost of capital 12%, positive NPV projects requiring GBP 800 million, and an above-average debt ratio it will not increase.
Step 1, the funding gap: $800 - 500 = 300$ million (Python: `800-500 = 300`).
Step 2, decision: no dividend initiation is expected.
Any dividend would come at the expense of rejecting positive NPV projects or would have to be financed with debt (ruled out) or new equity.
Issuing shares solely to pay dividends makes no sense once flotation costs exist, so the company should retain everything and consider issuing equity only to fund the project shortfall (V4 p.24, p.25). ^ex-04-01-8

### Example 9: Makinasi Appliances cuts its dividend (V4 p.25, p.26)

Makinasi cuts its quarterly dividend from USD 1.60 to USD 0.70 facing a forecast 19% sales decline, an expected loss up to USD 32.5 million after a USD 28.6 million loss the prior year, a bond rating cut from A to A-, and a planned USD 50 million bond issue.
Which factors dominate: expected volatility of future earnings and preservation of financial flexibility.
Paying the full dividend would have drained liquidity, forced more external funding, likely deepened the rating downgrade and raised the cost of debt, and signaled unseriousness about cost cutting.
Flotation costs also matter: funding a bigger dividend would eventually require new equity, whose flotation costs exceed those of debt (V4 p.26). ^ex-04-01-9

### Example 10: determining dividends using a target payout adjustment model (V4 p.28, p.29)

Luna Inc.: last year EPS USD 2.00 and dividend USD 0.40; expected EPS USD 2.80; target payout 30%; 4-year adjustment period.
Step 1, adjustment factor: $A = 1/4 = 0.25$.
Step 2, target dividend at expected earnings: $2.80 \times 0.30 = 0.84$.
Step 3, expected dividend: $0.40 + (0.84 - 0.40) \times 0.25 = 0.40 + 0.11 = 0.51$ (Python: `0.40+(2.80*0.3-0.40)*0.25 = 0.51`).
Interpretation: earnings are expected to grow 40% but the dividend grows 27.5% ($0.11/0.40$), and the realized payout falls from 20% ($0.40/2.00$) to 18.2% ($0.51/2.80$) because fast earnings growth outruns the partial adjustment (Python: `0.51/2.80 = 0.18214`). ^ex-04-01-10

### Example 11: Pampas Fertilizer changes to a constant payout ratio policy (V4 p.29, p.30)

Pampas paid a fixed ARS 1.50 quarterly dividend, then from 2018:Q3 switched to paying 25% of quarterly net income.
Step 1, identify the switch quarter from the DPS table: 2018:Q1 and Q2 show DPS 1.500 regardless of EPS (21.22 and 26.30), while from 2018:Q3 the DPS equals about a quarter of EPS (4.660 on 18.65, 1.961 on 7.84), so the first constant-payout quarter is 2018:Q3.
Step 2, verify 2019:Q4: $9.32 / 4 = 2.330$ against a reported DPS of 2.350 (Python: `9.32/4 = 2.33`).
The small difference is rounding, because EPS is reported to two decimals.
Interpretation: under the constant payout policy the dividend is as volatile as quarterly earnings, which suits a cyclical fertilizer producer that cannot promise a steadily rising level (V4 p.29). ^ex-04-01-11

### Example 12: BCII considers alternative repurchase methods (V4 p.33, p.34)

BCII wants to repurchase 5 million shares with the stock at CAD 37, weighing cost, flexibility and speed.
Open market: maximum flexibility, no obligation to execute or complete, opportunistic timing below intrinsic value makes it cost-effective, but it is slow.
Fixed price tender at CAD 40: fast (about 30 days) but costs a premium, $5\text{M} \times 40 = 200$ million, though the premium itself can signal management's confidence.
Dutch auction in a CAD 38 to 40 range: discovers the minimum clearing price; if it clears at CAD 38 the cost is $5\text{M} \times 38 = 190$ million, saving CAD 10 million versus the fixed tender (Python: `5*40-5*38 = 10`), and it is nearly as fast as a fixed price tender. ^ex-04-01-12

### Example 13: share repurchase using surplus cash (V4 p.34, p.35)

Takemiya has 10 million shares, net income JPY 100 million, share price JPY 120, and JPY 240 million of surplus cash earning about zero; buyback price is JPY 140 (a JPY 20 premium).
Step 1, current EPS: $100\text{M} / 10\text{M} = 10.00$.
Step 2, shares repurchased: $240\text{M} / 140 = 1.714$ million, leaving $10 - 1.714 = 8.286$ million shares (Python: `240/140 = 1.71429`).
Step 3, post-buyback EPS: $100\text{M} / 8.286\text{M} = 12.07$ (Python: `100/(10-240/140) = 12.06897`).
The curriculum rounds the share count to 8.3 million and reports EPS of about 12.00 and a 20% increase; the exact figures are 12.07 and 20.7%, and the difference is pure rounding.
Net income is unchanged because the cash was earning nothing; buying at the market price of 120 instead would retire 2 million shares and lift EPS to $100/8 = 12.50$, which is why paying a premium damps the accretion. ^ex-04-01-13

### Example 14: share repurchases using borrowed funds (V4 p.35, p.36)

Selamat borrows MYR 12 million to repurchase 200,000 shares at MYR 60; earnings after tax MYR 6.6 million; 2.2 million shares; EPS 3; E/P 5%.
Case 1, after-tax borrowing cost 5%: $EPS = (6.6 - 12 \times 0.05)/2.0 = (6.6 - 0.6)/2.0 = 3.00$ (Python: `(6.6-0.6)/2 = 3.0`).
EPS is unchanged because the after-tax cost of debt exactly equals the 5% earnings yield.
Case 2, after-tax borrowing cost 6%: $EPS = (6.6 - 12 \times 0.06)/2.0 = (6.6 - 0.72)/2.0 = 2.94$ (Python: `(6.6-0.72)/2 = 2.94`).
EPS falls because 6% exceeds the 5% earnings yield.
This is Formula 10 in action: the earnings yield is the breakeven after-tax borrowing rate for a debt-financed buyback (V4 p.36). ^ex-04-01-14

### Example 15: the effect of a share repurchase on book value per share (V4 p.37)

Companies A and B both trade at USD 20 with 10 million shares and announce USD 5 million buybacks; A has book equity USD 100 million (BVPS 10, price above book), B has USD 300 million (BVPS 30, price below book).
Step 1, shares bought by each: $5\text{M} / 20 = 250{,}000$, leaving 9.75 million shares.
Step 2, Company A: equity falls to $100 - 5 = 95$ million; $BVPS = 95 / 9.75 = 9.74$, down from 10 (Python: `95/9.75 = 9.74359`).
Step 3, Company B: equity falls to $300 - 5 = 295$ million; $BVPS = 295 / 9.75 = 30.26$, up from 30 (Python: `295/9.75 = 30.25641`).
Rule confirmed: repurchase above BVPS dilutes BVPS, repurchase below BVPS accretes it (V4 p.37). ^ex-04-01-15

### Example 16: the equivalence of share repurchases and cash dividends (V4 p.38)

RCII has 10 million shares at Rs 200 and Rs 500 million of free cash flow to distribute; taxation and information content are assumed identical across methods.
Cash dividend route: DPS $= 500\text{M} / 10\text{M} = 50$; ex-dividend price $= (10\text{M} \times 200 - 500\text{M}) / 10\text{M} = 1{,}500\text{M} / 10\text{M} = 150$; wealth per share $= 50 + 150 = 200$ (Python: `(2000-500)/10 = 150`).
Repurchase route: shares bought $= 500\text{M} / 200 = 2.5$ million; post-repurchase price $= 1{,}500\text{M} / 7.5\text{M} = 200$; wealth per share $= 200$ whether or not the holder sold (Python: `(2000-500)/7.5 = 200.0`).
Conclusion: the distribution mechanism at the market price neither creates nor destroys wealth (V4 p.38, p.39). ^ex-04-01-16

### Example 17: direct negotiation, a repurchase that transfers wealth (V4 p.39)

AfriCitrus trades at ZAR 200 with 10 million shares; the board considers buying ZAR 500 million of stock from activist Mzazi at ZAR 250, a ZAR 50 premium.
Step 1, shares repurchased: $500\text{M} / 250 = 2$ million.
Step 2, post-repurchase price: $(10\text{M} \times 200 - 500\text{M}) / 8\text{M} = 1{,}500\text{M} / 8\text{M} = 187.50$ (Python: `(2000-500)/8 = 187.5`).
Step 3, loss to each remaining share: $200 - 187.50 = 12.50$.
Total wealth is conserved, but the ZAR 100 million premium ($2\text{M} \times 50$) is transferred from the other shareholders to Mzazi, which is why the board declines and why greenmail harms remaining holders (V4 p.33, p.39). ^ex-04-01-17

### Example 18: share repurchase to increase financial leverage (V4 p.41, p.42)

DOHI has debt of AED 30 million, a 30% debt ratio (capital AED 100 million), and plans an AED 7 million repurchase.
Step 1, cash-funded: debt stays 30, capital falls to 93, debt ratio $= 30 / 93 = 32.3\%$ (Python: `30/93 = 0.32258`).
Step 2, debt-funded: debt rises to 37, capital stays 100, debt ratio $= 37 / 100 = 37.0\%$.
Step 3, value of equity, cash funding: equity at market is $70 - 7 = 63$; with net income unchanged and fewer shares, EPS rises, and at an unchanged P/E the market value of equity would be expected to rise above 63.
Step 4, debt funding with after-tax cost of debt above E/P: EPS falls, so at the same P/E equity value would be expected to fall below 63.
Step 5, with a looming rating downgrade, spreads widen and the market value of the debt also falls below 37; both values falling makes the post-repurchase capital structure proportions indeterminate.
Either financing route raises leverage; debt financing raises it more (V4 p.41, p.42). ^ex-04-01-18

### Example 19: ITOCHU announces a buyback to improve ROE (V4 p.42, p.43)

ITOCHU targeted a medium-to-long-term ROE of 13% or higher and repurchased in two tranches: 15,097,200 shares at an average JPY 1,987 (about JPY 30 billion) and 19,024,200 shares at an average JPY 1,997 (about JPY 38 billion), 34,121,400 shares at an average JPY 1,993 for about JPY 68 billion in total.
Verification: $15{,}097{,}200 \times 1{,}987 = 30.0$ billion and $19{,}024{,}200 \times 1{,}997 = 38.0$ billion, summing to 68.0 billion (Python: `15097200*1987 = 3.0e10`, `19024200*1997 = 3.799e10`).
Mechanism: a buyback shrinks equity while net income is unaffected, so ROE rises; SoftBank, Sony and other Japanese companies followed under activist pressure to improve shareholder returns and governance (V4 p.43). ^ex-04-01-19

### Example 20: Shenzhen Medical Devices' dividend policy decision (V4 p.45, p.46, p.47)

SMDL proposes a first annual dividend of JPY-equivalent CNY 0.40 per share against estimated EPS of CNY 3.20 (a 12.5% payout), with a stated intention to hold or grow the dividend toward a 25% target payout of long-term sustainable earnings; pro forma cash flows show CFO 135, investing outflow 84, debt repayment 4, repurchases 32, and the proposed dividend 15, leaving zero change in cash.
Question 1, critique of "a cash dividend means SMDL is no longer a growth company": initiations are on average followed by earnings growth, forecast sales and earnings growth are high (8% and 11%), the negative CNY 84 million investing flow shows plentiful positive NPV projects, and three years of repurchases mean investors already know cash is being returned, so the initiation is a weak negative signal at most.
Question 2, Director W is right that a 2% stock dividend leaves wealth unchanged: ownership fractions are constant and the price adjusts down exactly to offset the extra shares.
Question 3, the CNY 0.40 proposal is a stable dividend policy built on a target payout adjustment model: the dividend uses the full residual free cash flow (15 = 135 - 84 - 4 - 32), commits to a floor, and moves gradually toward the 25% target payout of sustainable earnings while leaving funds for profitable projects (V4 p.47).
Consistency check: 15 million total on 0.40 per share implies 37.5 million shares, and $0.40 / 3.20 = 12.5\%$ (Python: `15/0.40 = 37.5`, `0.40/3.20 = 0.125`). ^ex-04-01-20

### Example 21: traditional measures of dividend safety (V4 p.48)

Mature European SA: net income EUR 100 million, dividends EUR 40 million.
Payout ratio $= 40 / 100 = 40\%$; dividend coverage $= 100 / 40 = 2.5\text{x}$ (Python: `100/40 = 2.5`).
Interpretation: squarely inside the mature-company norms of 40% to 60% payout and 1.7x to 2.5x coverage, so the dividend looks safe on the traditional metric; the ratios are reciprocals, so quoting one determines the other (V4 p.48). ^ex-04-01-21

### Example 22: Lygon's coverage ratios (V4 p.49, p.50, p.51)

Lygon (A$ millions): net income 540, 458, 399, 341; CFO 837, 824, 679, 628; FCInv 554, 417, 296, 327; net borrowing (120), (39), 79, (7); dividends 121, 256, 277, 323; repurchases 0, 105, 277, 0 for 2015 to 2018.
Step 1, payout ratios: $121/540 = 22.4\%$, $256/458 = 55.9\%$, $277/399 = 69.4\%$, $323/341 = 94.7\%$ (Python: `[121/540, 256/458, 277/399, 323/341] = [0.2241, 0.5590, 0.6942, 0.9472]`).
Step 2, earnings coverage: $540/121 = 4.46\text{x}$, $458/256 = 1.79\text{x}$, $399/277 = 1.44\text{x}$, $341/323 = 1.06\text{x}$.
Step 3, FCFE by Formula 13: $837 - 554 - 120 = 163$; $824 - 417 - 39 = 368$; $679 - 296 + 79 = 462$; $628 - 327 - 7 = 294$ (Python: `[837-554-120, 824-417-39, 679-296+79, 628-327-7] = [163, 368, 462, 294]`).
Step 4, FCFE coverage of dividends plus repurchases: $163/121 = 1.35\text{x}$; $368/(256+105) = 1.02\text{x}$; $462/(277+277) = 0.83\text{x}$; $294/323 = 0.91\text{x}$ (Python: `[163/121, 368/361, 462/554, 294/323] = [1.347, 1.019, 0.834, 0.910]`).
Step 5, trends: earnings coverage decays from 4.5x to bare sufficiency at 1.06x; FCFE coverage falls below 1 in 2017 and stays below in 2018 even after repurchases stop, and note 2017's coverage is propped up by positive net borrowing of 79.
Step 6, sustainability: at 0.83x management should halt discretionary repurchases (it did), and with FCFE coverage still 0.91x in 2018 and income falling, a dividend cut should be on the table; distributions supported by shrinking capex and borrowing are not sustainable (V4 p.51). ^ex-04-01-22

## Item-set patterns

> [!warning] Trap 1: the stock dividend or split that "creates value"
> The vignette quotes a director claiming a stock dividend, split or reverse split changes shareholder wealth or improves ratios.
> Correct: all three are wealth-neutral and ratio-neutral (liquidity, leverage, P/E, payout, yield); only per-share magnitudes rescale, and the sole accounting difference is that a stock dividend moves retained earnings to contributed capital (V4 p.8, p.9).
> Distractors: "EPS falls so shareholders are worse off" (price falls proportionally), "the split reduces P/E" (price and EPS fall together), "a cash dividend leaves ratios unchanged" (it lowers the current ratio and raises leverage).

> [!warning] Trap 2: buyback EPS with the wrong comparison rate
> A debt-financed repurchase gives P/E or price and EPS, plus a pretax and an after-tax borrowing rate.
> Correct: invert P/E to the earnings yield and compare with the after-tax cost of debt; EPS rises if E/P is higher, is flat at equality, falls if lower (V4 p.36).
> Distractors: comparing against the pretax rate, comparing the coupon with the dividend yield, or assuming any buyback raises EPS because shares fall (the interest drag can dominate).

> [!warning] Trap 3: BVPS direction without reading the price-to-book relationship
> A buyback question gives book equity, shares and a market price.
> Correct: price above BVPS makes BVPS fall, price below makes it rise, price equal leaves it unchanged; then compute (equity minus cash paid) over remaining shares (V4 p.37).
> Distractors: dividing the new equity by the old share count, keeping old equity with the new share count, or asserting BVPS always falls because equity shrinks.

> [!warning] Trap 4: effective tax rate arithmetic
> A double taxation question gives a corporate and a personal dividend rate.
> Correct: $ETR = t_c + (1 - t_c)t_d$; for 40% and 30% that is 58% (V4 p.22, p.65).
> Distractors: adding the rates to 70% (ignores that the personal tax applies only to the after-corporate-tax residual), using only the personal rate, or applying the formula in an imputation country where the answer is simply the shareholder's marginal rate.

> [!warning] Trap 5: Lintner model omissions
> A stable-policy question gives previous dividend, expected EPS, target payout and an adjustment period.
> Correct: $D_1 = D_0 + (E_1 \times \text{target} - D_0) \times (1/\text{years})$ (V4 p.28).
> Distractors: the full target dividend $E_1 \times$ target (forgets partial adjustment), using last year's EPS instead of expected EPS, or forgetting to add the increment back to the previous dividend.

> [!warning] Trap 6: equivalence versus the negotiated premium
> One question asserts dividends and repurchases are wealth-equivalent; a neighboring one has a premium buyback from a single holder.
> Correct: equivalence holds only at the market price with identical taxes and information; a premium repurchase transfers the premium from remaining holders to the seller, and the post-buyback price falls below the market price (V4 p.38, p.39).
> Distractors: "repurchases always create value" (announcement effects are not mechanical value), "the premium is borne by the seller", or ignoring that non-tendering holders' relative stake rises.

> [!warning] Trap 7: the sign of a dividend signal
> A company cuts or initiates a dividend and the question asks for the most likely inference.
> Correct default: initiations and increases signal positive prospects, cuts and omissions signal trouble; but a cut framed by management as reinvestment or precaution with credible detail can be received positively (Telstra, Skanska, BT) (V4 p.15, p.16).
> Distractors: treating every cut as automatically negative when the vignette plants cash flow strength and a reinvestment plan, or treating an initiation as proof of fading growth without corroborating facts.

> [!warning] Trap 8: which agency conflict the payout touches
> A payout change is proposed and the options name manager-shareholder and shareholder-bondholder conflicts.
> Correct: higher payout mitigates the manager-shareholder overinvestment problem (Jensen) but worsens the shareholder-bondholder conflict by thinning the cash cushion and raising default risk, which is why covenants restrict distributions (V4 p.17, p.18).
> Distractors: swapping the two directions, or claiming dividends reduce default risk.

> [!warning] Trap 9: earnings coverage healthy while FCFE coverage collapses
> A four-year table gives net income, CFO, capex, net borrowing, dividends and repurchases.
> Correct: compute $FCFE = CFO - FCInv + \text{Net borrowing}$ and coverage of dividends plus repurchases; a ratio below 1, or one propped up by borrowing and capex cuts, flags unsustainability even when earnings coverage looks fine (V4 p.49, p.50).
> Distractors: the earnings-based coverage ratio, FCFE over dividends alone when repurchases exist, and sign errors on net borrowing (a repayment is negative).

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM01-Analysis-of-Dividends-and-Share-Repurchases-Practice-Problems]]

## Cross-links

- [[LM02-Discounted-Dividend-Valuation]]: the payout policies here are the inputs there; the target payout adjustment model, payout trends and dividend safety analysis determine the dividend stream and sustainable growth rate that DDM and the Gordon model capitalize.
- [[LM03-Cost-of-Capital-Advanced-Topics]]: the buyback EPS rule compares the earnings yield with the after-tax cost of debt, and the retain-versus-distribute decision turns on whether internal funds earn their cost of capital, both estimated with that module's machinery.
- [[LM04-Corporate-Restructuring]]: distributions and restructurings are competing uses of free cash flow; a debt-funded buyback changes leverage the same way the recapitalizations analyzed there do, and both are judged by signaling and value effects.
- [[LM02-Environmental-Social-and-Governance-ESG-Considerations-in-Investment-Analysis]]: the agency framework behind Jensen's free cash flow hypothesis is the same governance lens applied there; board independence and ownership structure determine whether payout discipline is needed.
- [[LM02-Employee-Compensation-Post-Employment-and-Share-Based]]: companies repurchase shares to offset dilution from option and share-based awards, so the EPS denominator effects computed here interact with that module's diluted share count mechanics.

## Self-test

Vignette A for Q1 to Q4: Kestrel Mining is listed in a dividend imputation country with a 30% corporate tax rate; its representative shareholder has a 40% marginal rate.
Kestrel's subsidiary operates where distributed corporate profits are taxed under a split-rate system: 25% corporate tax on distributed earnings, 40% on retained earnings, and a 30% personal dividend tax.
A peer, Osprey Metals, operates in a classical double taxation country with a 25% corporate rate and a 20% personal dividend rate.
Kestrel paid a dividend of 1.20 per share last year, expects EPS of 4.50, targets a 40% payout of sustainable earnings and adjusts over three years.

> [!question] Q1
> Per 100 of pretax earnings fully distributed, the additional tax Kestrel's shareholder must pay after the franking credit is closest to:
> A. 0.
> B. 10.
> C. 40.

> [!question] Q2
> The effective tax rate on Osprey's fully distributed earnings is closest to:
> A. 40%.
> B. 45%.
> C. 50%.

> [!question] Q3
> The effective tax rate on the subsidiary's distributed earnings under the split-rate system is closest to:
> A. 44.5%.
> B. 47.5%.
> C. 55.0%.

> [!question] Q4
> Under the target payout adjustment model, Kestrel's expected dividend per share this year is closest to:
> A. 1.40.
> B. 1.60.
> C. 1.80.

Vignette B for Q5 to Q8: Tarn Industrial has net income of 50 million, 10 million shares (EPS 5.00), a share price of 80 (P/E 16), and book equity of 400 million (BVPS 40).
It will repurchase 1 million shares at the market price of 80, funding the full 80 million with debt at an after-tax cost of 7%.
Separately, an adviser has floated repurchasing 1 million shares from an activist at a negotiated 88 per share instead.

> [!question] Q5
> Tarn's EPS after the debt-financed market-price buyback is closest to:
> A. 4.93.
> B. 5.00.
> C. 5.56.

> [!question] Q6
> The after-tax borrowing rate at which the buyback would leave Tarn's EPS exactly unchanged is closest to:
> A. 5.00%.
> B. 6.25%.
> C. 7.00%.

> [!question] Q7
> After the market-price buyback, Tarn's book value per share is closest to:
> A. 32.00.
> B. 35.56.
> C. 40.00.

> [!question] Q8
> If Tarn instead repurchased the 1 million shares from the activist at 88, the wealth effect on the remaining shareholders per share held is closest to:
> A. a loss of 0.89.
> B. zero.
> C. a gain of 0.89.

Vignette C for Q9 to Q10: Moraine Chemicals reports net income of 240, CFO of 350, fixed capital investment of 180, net debt repayment of 20 (net borrowing of negative 20), dividends of 150 and share repurchases of 60 (all millions).
Its dividend yield has risen to roughly twice its 10-year average while consensus earnings forecasts fall.

> [!question] Q9
> Moraine's FCFE coverage ratio of dividends plus repurchases is closest to:
> A. 0.71.
> B. 0.88.
> C. 1.60.

> [!question] Q10
> The observation that most strengthens the case that the market expects a dividend cut is:
> A. the earnings-based dividend coverage ratio of 1.6x.
> B. the dividend yield at twice its historical average alongside falling earnings forecasts.
> C. the presence of share repurchases in the same year as the dividend.

> [!success]- Answer key
> Q1: B.
> Imputation taxes distributed profits once at the shareholder's rate: gross tax $= 0.40 \times 100 = 40$, franking credit $= 30$, additional tax due $= 40 - 30 = 10$ (Python: `40-30 = 10`).
> A would need the shareholder rate to equal the corporate rate; C ignores the franking credit entirely (V4 p.23).
>
> Q2: A.
> $ETR = 1 - (1 - 0.25)(1 - 0.20) = 1 - 0.60 = 40\%$ (Python: `1-0.75*0.8 = 0.40`).
> B and C add mismatched combinations of the statutory rates instead of layering the personal tax on the after-corporate-tax residual (V4 p.22).
>
> Q3: B.
> $ETR = 25 + 75 \times 0.30 = 25 + 22.5 = 47.5\%$ (Python: `25+75*0.30 = 47.5`).
> A uses a 26% first layer or misreads the corporate rate; C wrongly uses the 40% retained-earnings rate as the first layer, but distributed earnings enjoy the lower 25% rate, which is the whole point of split-rate systems (V4 p.23, p.24).
>
> Q4: A.
> $D_1 = 1.20 + (4.50 \times 0.40 - 1.20) \times (1/3) = 1.20 + (1.80 - 1.20)/3 = 1.40$ (Python: `1.20+0.60/3 = 1.40`).
> B applies two-thirds of the gap; C jumps straight to the destination dividend of 1.80 with no partial adjustment (V4 p.28).
>
> Q5: A.
> After-tax interest $= 80 \times 0.07 = 5.6$; $EPS = (50 - 5.6)/9 = 4.93$ (Python: `44.4/9 = 4.9333`).
> B would require the after-tax cost to equal the earnings yield; C divides unchanged earnings by 9 million shares ($50/9 = 5.56$), forgetting the interest drag (V4 p.36).
>
> Q6: B.
> EPS is unchanged when the after-tax cost of debt equals the earnings yield: $E/P = 5.00/80 = 1/16 = 6.25\%$ (Python: `5/80 = 0.0625`).
> A is an arbitrary round rate; C is the actual borrowing cost, which being above 6.25% is exactly why Q5's EPS fell (V4 p.36).
>
> Q7: B.
> $BVPS = (400 - 80)/9 = 320/9 = 35.56$ (Python: `320/9 = 35.5556`).
> Direction check: price 80 is above BVPS 40, so BVPS must fall.
> A subtracts 80 from equity but divides by 10 million shares; C forgets any change (V4 p.37).
>
> Q8: A.
> Post-repurchase price $= (10 \times 80 - 88)/9 = (800 - 88)/9 = 79.11$; loss per remaining share $= 80 - 79.11 = 0.89$ (Python: `712/9 = 79.1111`).
> The 8 premium on 1 million shares (8 million total) is transferred from the 9 million remaining shares.
> B holds only for a repurchase at the market price; C reverses the direction of the transfer (V4 p.39).
>
> Q9: A.
> $FCFE = 350 - 180 - 20 = 150$; coverage $= 150/(150 + 60) = 0.71$ (Python: `150/210 = 0.7143`).
> B forgets the debt repayment ($330/210$ style errors or $185/210$); C is the earnings coverage $240/150 = 1.6$, the wrong metric for cash sustainability (V4 p.49, p.50).
>
> Q10: B.
> An abnormally high yield against the company's own history, with earnings forecasts falling, is the market pricing the shares for a cut, the StarHub pattern (V4 p.52).
> A points the other way: 1.6x earnings coverage looks adequate even though cash coverage is weak.
> C is neutral: pairing repurchases with dividends is normal payout policy, not a cut signal (V4 p.43).

## Flashcards

#flashcards/cfa-l2/04-Corporate-Issuers/lm01

Expected share price behavior on the ex-dividend date::Price drops by the amount of the dividend, all else equal, because the buyer no longer receives it (V4 p.4).
Three situations that make a dividend a liquidating dividend::Going out of business and distributing net assets, distributing proceeds of selling a portion of the business, or paying a dividend that exceeds accumulated retained earnings; all are a return of capital (V4 p.7).
Effect of a stock dividend on shareholder wealth and cost basis::Wealth, proportionate ownership and total cost basis unchanged; only per-share values and cost per share fall (V4 p.7, p.8).
Which ratios does a cash dividend change and how?::Cash and current ratios fall, debt-to-equity and debt-to-assets rise, because cash and retained earnings leave the firm (V4 p.8).
Which ratios do stock dividends and splits change?::None; liquidity ratios, leverage ratios, P/E, payout ratio and dividend yield are all unchanged (V4 p.8, p.9).
Accounting difference between a 100% stock dividend and a 2-for-1 split::The stock dividend transfers retained earnings to contributed capital; the split touches no equity account (V4 p.9).
Typical reason for a reverse stock split::Raise a very low share price into a marketable range, often to meet listing requirements or attract institutions; wealth effect neutral (V4 p.9, p.10).
State the MM dividend irrelevance conclusion and its three key assumptions::With no taxes, no transaction costs and symmetric information, dividend policy affects neither cost of capital nor shareholder wealth (V4 p.11).
What is a homemade dividend?::An investor sells enough shares to create the desired cash income stream, replicating any payout policy in perfect markets (V4 p.12).
The MM irrelevance claim is about {{dividend policy}}, not about {{dividends themselves}}; alternatives are trades between dividend streams of equal present value (V4 p.12).
Bird in the hand argument in one line::A unit of dividends is seen as less risky than a unit of expected capital gain, so payers should enjoy a lower cost of equity and higher price (V4 p.12).
MM's rebuttal to bird in the hand::Paying the dividend today does not change the risk of future cash flows; it only lowers the ex-dividend price (V4 p.12).
Tax aversion theory conclusion taken to its extreme::Where dividends are taxed more heavily than capital gains, taxable investors prefer zero payout with distributions via repurchases (V4 p.13).
Why are dividend increases credible signals?::They are costly to mimic; a firm without growing cash flows cannot sustain the higher dividend and must later cut or raise external funds (V4 p.13, p.14).
What do initiations and increases empirically foreshadow?::Future earnings growth and positive excess returns; omissions and cuts foreshadow earnings problems (V4 p.13).
Five characteristics of consistent dividend growers::Dominant or niche industry position, global operations, less volatile earnings, high return on assets, low debt ratios (V4 p.15).
When can a dividend cut be a positive signal?::When it credibly funds reinvestment or preserves flexibility amid uncertainty, as with Telstra and Skanska; BT's cut saw the shares rise 6.9% (V4 p.15, p.16).
Jensen's free cash flow hypothesis::Managers with free cash flow may overinvest in negative NPV projects; paying out free cash flow constrains that agency cost (V4 p.17).
Profile of the company investors push for higher payout on agency grounds::Strong operating cash flow, shrinking investment opportunities, weak corporate governance (V4 p.18).
How do dividends affect the shareholder-bondholder conflict?::They thin the cash cushion behind fixed claims, raise default risk and can transfer wealth to shareholders, so covenants restrict distributions (V4 p.17, p.18).
Why do regulated utilities pay high dividends and then issue equity?::The repeated equity issuance lets the market monitor managers and regulators; poor pricing of new shares pressures regulators to set fair rates (V4 p.18, p.19).
Six factors affecting dividend policy in practice::Investment opportunities, expected volatility of future earnings, financial flexibility, tax considerations, flotation costs, contractual and legal restrictions (V4 p.20).
Three Lintner survey findings about managers and dividends::Target payout based on long-run sustainable earnings, focus on dividend changes rather than levels, reluctance to make increases that might be reversed (V4 p.21, p.28).
Why do flotation costs discourage high dividends?::New equity costs roughly 4% to 10% of proceeds, so internal funds are cheaper and firms avoid dividend levels that force issuance (V4 p.12, p.24).
Impairment of capital rule::Legal restriction requiring net remaining assets to be at least a specified amount related to capital before a non-liquidating dividend can be paid (V4 p.25).
Effect of cumulative preference dividends in arrears::They must be paid before any common dividend can be paid (V4 p.25).
Effective tax rate under double taxation, corporate 35% and personal 15%?::35% + 65% times 15% = 44.75%, about 44.8%; keystrokes 0.65 × 0.15 = + 0.35 = (V4 p.22).
Effective tax rate on distributed earnings under imputation::The shareholder's own marginal rate; the franking credit refunds or tops up the difference from the corporate rate (V4 p.23).
Split-rate system in one line::Distributed earnings bear a lower corporate rate than retained earnings, then dividends are taxed as ordinary personal income (V4 p.23, p.24).
Micro-problem: split-rate 20% corporate on distributions, 35% personal; effective rate per 100 distributed?::20 + 80 × 0.35 = 48%; net dividend 52 (V4 p.24).
Stable dividend policy basis::Long-term forecast of sustainable earnings, so short-term earnings volatility does not transmit to the dividend (V4 p.27).
Target payout adjustment model formula::Expected dividend equals previous dividend plus (expected earnings times target payout minus previous dividend) times the adjustment factor, where the factor is one over the adjustment years (V4 p.28).
Micro-problem: previous DPS 0.40, expected EPS 1.50, target 50%, five-year adjustment; increase?::(0.75 minus 0.40) times 0.2 = 0.07 increase to 0.47; keystrokes 1.5 × 0.5 = − 0.4 = × 0.2 = (V4 p.28).
Under a stable policy with fast earnings growth, the realized payout ratio {{falls away from}} the target because the dividend adjusts only partially each year (V4 p.29).
Constant dividend payout ratio policy and its consequence::A fixed percentage of current earnings is paid, so dividends are as volatile as earnings; rarely adopted (V4 p.29).
Broad global payout trends::Fraction of dividend payers declining long term in developed markets, aggregate dividends and payout ratios rising, repurchases trending up since the 1980s (US) and 1990s (Europe), payers larger and more profitable with fewer growth options (V4 p.30, p.31).
Better governance and disclosure are associated with {{fewer}} dividend initiations and increases because the signaling role of dividends {{declines}} as information asymmetry falls (V4 p.31).
Four share repurchase methods in order of importance::Open market purchases, fixed price tender offer, Dutch auction, direct negotiation (V4 p.32, p.33).
Which repurchase method offers maximum flexibility and why?::Open market; no obligation to execute or complete, purchases timed opportunistically, most cost-effective (V4 p.32).
How does a Dutch auction set its price?::Shareholders submit price-quantity offers within the announced range; the company pays the lowest single price that clears the desired quantity to all qualifying bids (V4 p.33).
What is greenmail?::Repurchasing a would-be acquirer's block at a premium to market, typically to the detriment of remaining shareholders (V4 p.33).
Treasury shares versus canceled shares::Repurchased shares held for possible reissue versus retired; neither receives dividends, votes, nor counts in EPS (V4 p.31).
EPS effect of a buyback funded with surplus cash::EPS rises if the cash was earning less than its cost of capital; with near-zero-yield cash the reduction in shares dominates and EPS rises (V4 p.35, p.36).
EPS effect rule for a debt-financed buyback::EPS rises if the earnings yield exceeds the after-tax cost of debt, is unchanged at equality, falls below it (V4 p.36).
Micro-problem: EPS 3, price 60, borrow 12 million at 6% after tax, buy 200,000 of 2.2 million shares; new EPS?::(6.6 − 0.72) / 2 = 2.94, a decrease since 6% exceeds the 5% earnings yield; keystrokes 12 × 0.06 = then 6.6 − 0.72 = ÷ 2 = (V4 p.36).
Why is a higher post-buyback EPS not higher shareholder wealth?::Leverage and the required return rise, and with total free cash flow unchanged the value is unchanged; the EPS gain may be offset by lost dividend yield (V4 p.36, p.41).
BVPS direction rule for buybacks::Repurchase above book value per share lowers BVPS; below raises it; at book leaves it unchanged (V4 p.37).
Micro-problem: book equity 300 million, 10 million shares, buy 1 million at market 40; new BVPS?::(300 − 40) / 9 = 28.89, down from 30 because price exceeds BVPS; keystrokes 300 − 40 = ÷ 9 = (V4 p.37, p.66).
Conditions for dividend-repurchase wealth equivalence::Repurchase at the market price with identical taxation and identical information content; then seller and holder wealth match the cash dividend outcome (V4 p.38).
Effect of a negotiated repurchase at a premium::Wealth transfers from remaining shareholders to the selling shareholder by the amount of the premium; post-buyback price falls below market (V4 p.39).
Five reasons companies repurchase rather than pay dividends::Potential tax advantage, undervaluation signaling and price support, managerial flexibility, offsetting option dilution, increasing financial leverage (V4 p.40, p.41).
Which raises leverage more, a cash-funded or debt-funded buyback?::Debt-funded; DOHI's ratio went to 37% with debt versus 32% with cash from a 30% base (V4 p.41, p.42).
How do repurchases behave over the business cycle?::Procyclical; they surge in expansions and collapse in recessions (Russell 1000: 680 billion in 2007 to 223 billion in 2008-09) while dividends fall far less (V4 p.43, p.44).
Dividend payout and coverage ratio definitions::Payout is dividends over net income; coverage is net income over dividends; they are reciprocals (V4 p.6, p.48).
Normal payout and coverage ranges for large mature companies::Payout 40% to 60%, coverage about 1.7x to 2.5x over a business cycle; coverage at 1.0 puts the dividend in jeopardy absent one-off causes (V4 p.48).
FCFE formula::Cash flow from operations minus fixed capital investment plus net borrowing (V4 p.50).
FCFE coverage ratio and its interpretation::FCFE divided by dividends plus share repurchases; 1 means all available cash returned, above 1 builds liquidity, materially below 1 is unsustainable (V4 p.49).
Micro-problem: CFO 824, FCInv 417, net borrowing −39, dividends 256, repurchases 105; FCFE coverage?::FCFE = 368; coverage = 368/361 = 1.02x; keystrokes 824 − 417 = − 39 = then ÷ 361 = (V4 p.50).
Warning signs a dividend may be cut::Coverage near 1.0, FCFE coverage below 1, abnormally high dividend yield versus history, borrowing or capex cuts funding distributions, high leverage, past dividend cuts (V4 p.48, p.51, p.52).
Why watch extremely high dividend yields?::The market is pricing in a cut, bidding the shares down so the post-cut total return stays adequate; StarHub yielded 9.4% just before cutting (V4 p.52).

## Common mistakes

1. Claiming a stock dividend or split changes shareholder wealth, P/E or leverage; only per-share figures rescale and the total pie is untouched (V4 p.8, p.9).
2. Treating a reverse stock split as inherently bad news; it is wealth-neutral on its own and often preserves a listing (V4 p.10).
3. Adding corporate and personal tax rates for the double taxation effective rate (40% + 30% = 70%) instead of layering: $t_c + (1 - t_c)t_d = 58\%$ (V4 p.22, p.65).
4. Applying the double-taxation formula in an imputation country; there the effective rate is just the shareholder's marginal rate, with credits for corporate tax paid (V4 p.23).
5. Jumping straight to Expected earnings times Target payout in the Lintner model instead of adjusting only the fraction $1/n$ of the gap and adding it to the previous dividend (V4 p.28, p.65).
6. Comparing the earnings yield with the pretax borrowing rate (or comparing P/E with the coupon) when judging a debt-financed buyback; the rule uses the after-tax cost of debt against E/P (V4 p.36).
7. Assuming every buyback raises EPS; if the after-tax cost of the funds exceeds the earnings yield, EPS falls, and surplus cash buybacks accrete only because idle cash earns less than its cost of capital (V4 p.35, p.36).
8. Reading a higher post-buyback EPS as higher shareholder wealth; the required return rises with leverage and free cash flow is unchanged (V4 p.36, p.41).
9. Forgetting the BVPS direction rule: buying above book dilutes BVPS, below book accretes it, and the computation divides post-buyback equity by post-buyback shares, never mixing old and new (V4 p.37, p.63).
10. Believing dividend-repurchase equivalence holds at any repurchase price; a premium to one holder is a transfer from everyone else (V4 p.38, p.39).
11. Judging dividend safety on earnings coverage alone; FCFE coverage of dividends plus repurchases catches distributions funded by borrowing or capex cuts, and a sign error on net borrowing wrecks the FCFE (V4 p.49, p.50).
12. Treating all dividend cuts as negative signals; a credible reinvestment or precautionary story (Telstra, Skanska, BT) can make a cut good news (V4 p.15, p.16).
13. Saying a dividend increase worsens the manager-shareholder conflict or reduces bondholder risk; it does the opposite on both counts (V4 p.17, p.18, p.64).
14. Forgetting that announced open market repurchase programs are not commitments, unlike declared dividends, which is precisely their flexibility advantage (V4 p.32).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "04-01" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
