---
type: cfa-lm
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
volume: 6
lm: 3
title: "Valuation and Analysis of Bonds with Embedded Options"
pages: "119-197"
weight_band: "10-15%"
difficulty: 4
los_count: 17
status: not-started
mastery: 0
next_review: 2026-09-06
last_reviewed: ""
tags: [cfa/l2, cfa/fixed-income]
---

# LM3: Valuation and Analysis of Bonds with Embedded Options

Difficulty 4 of 5: seventeen LOS spanning callable, putable, capped, floored and convertible structures, every tree valuation must be executed node by node under time pressure, and the qualitative LOS (volatility, curve shape, OAS, one-sided durations, convexity) are tested through directional traps that punish any sign confusion.

## LOS map

- **describe** fixed-income securities with embedded options (V6 p.119) ^los-06-03-a
    - Examiner asks: classify a call feature as European, American or Bermudan from its exercise dates, identify who holds each option (call and cap are issuer options, put, floor, conversion and extension are investor options), or match an extendible bond to its equivalent putable bond.
- **explain** the relationships between the values of a callable or putable bond, the underlying option-free (straight) bond, and the embedded option (V6 p.119) ^los-06-03-b
    - Examiner asks: given two of the three values, back out the third with the correct sign, for example value of the call equals straight minus callable, or rank the prices of otherwise identical straight, callable, putable and convertible bonds.
- **describe** how the arbitrage-free framework can be used to value a bond with embedded options (V6 p.119) ^los-06-03-c
    - Examiner asks: order the three steps (generate the tree from the curve and volatility, apply the exercise decision at each node, run backward induction) or explain why one-period forward rates rather than spot rates are needed when options are present.
- **explain** how interest rate volatility affects the value of a callable or putable bond (V6 p.119) ^los-06-03-d
    - Examiner asks: volatility rises from 10% to 15%, is the callable bond worth more or less than the printed value, and the same question for the putable bond.
- **explain** how changes in the level and shape of the yield curve affect the value of a callable or putable bond (V6 p.119) ^los-06-03-e
    - Examiner asks: the curve flattens or inverts, what happens to the value of the embedded call and the embedded put, or rates fall in level, why does the callable bond rise less than the straight bond.
- **calculate** the value of a callable or putable bond from an interest rate tree (V6 p.119) ^los-06-03-f
    - Examiner asks: given a two-period binomial tree and an annual coupon, compute the Year 0 value applying calls or puts at par at Years 1 and 2, with the straight-bond value and the wrong-exercise value as distractors.
- **explain** the calculation and use of option-adjusted spreads (V6 p.119) ^los-06-03-g
    - Examiner asks: whether the OAS is added to the tree rates or subtracted from the coupon, and whether a bond with a higher OAS than comparable bonds is cheap or rich.
- **explain** how interest rate volatility affects option-adjusted spreads (V6 p.119) ^los-06-03-h
    - Examiner asks: holding price constant, the analyst raises the volatility assumption, does the OAS of the callable bond rise or fall.
- **calculate** and interpret effective duration of a callable or putable bond (V6 p.119) ^los-06-03-i
    - Examiner asks: plug PV minus, PV plus, PV zero and the shift size into the effective duration formula, with distractors that drop the factor 2 or use the wrong shift size.
- **compare** effective durations of callable, putable, and straight bonds (V6 p.119) ^los-06-03-j
    - Examiner asks: which bond's effective duration shortens when rates fall (callable) and which shortens when rates rise (putable), and why neither can exceed the straight bond's.
- **describe** the use of one-sided durations and key rate durations to evaluate the interest rate sensitivity of bonds with embedded options (V6 p.119) ^los-06-03-k
    - Examiner asks: for a callable near the money, is one-sided up-duration bigger than one-sided down-duration, or which key rate dominates for a 30-year bond callable in 10 years as the coupon rises.
- **compare** effective convexities of callable, putable, and straight bonds (V6 p.119) ^los-06-03-l
    - Examiner asks: which bond can have negative convexity (the callable, when the call is near the money) and why the putable bond's convexity is always positive.
- **calculate** the value of a capped or floored floating-rate bond (V6 p.119) ^los-06-03-m
    - Examiner asks: value a floater set in arrears on a tree, capping or flooring the coupon at each node, with the trap that the floor can bind at the Year 0 node.
- **describe** defining features of a convertible bond (V6 p.119) ^los-06-03-n
    - Examiner asks: adjust the conversion price and ratio for a stock split, decide whether a dividend above the threshold dividend forces a downward adjustment, or distinguish hard puts, soft puts and forced conversion.
- **calculate** and interpret the components of a convertible bond's value (V6 p.120) ^los-06-03-o
    - Examiner asks: compute conversion value, minimum value, market conversion price, market conversion premium per share and ratio, and premium over straight value, with the initial conversion price planted as a distractor.
- **describe** how a convertible bond is valued in an arbitrage-free framework (V6 p.120) ^los-06-03-p
    - Examiner asks: assemble the value of a callable putable convertible from its four components with the correct signs (plus stock call, minus issuer call, plus investor put).
- **compare** the risk–return characteristics of a convertible bond with the risk–return characteristics of a straight bond and of the underlying common stock (V6 p.120) ^los-06-03-q
    - Examiner asks: share price well below conversion price means busted convertible driven by rates and spreads, well above means equity-like driven by the share price, and between the two the bond trades as a hybrid.

## Core intuition

An embedded option is a contingency clause inside the bond's indenture that cannot be traded away from the bond (V6 p.120, p.121).
Everything in this module is one idea applied repeatedly: strip the bond into a straight bond plus options, value each piece arbitrage-free, and keep the signs straight by asking who owns the option.
The issuer owns the call and the cap, so those provisions take value away from the investor.
The investor owns the put, the floor, the conversion right and the extension right, so those provisions add value for the investor (V6 p.121, p.125, p.161, p.162).

Why does the issuer want a call?
When rates fall, the issuer can refinance the debt more cheaply, so it retires the expensive bond early (V6 p.120, p.121).
Why does the investor want a put?
When rates rise, the bond's price falls, and the put lets the investor hand the bond back at par and reinvest at the new higher yields (V6 p.122).
An extendible bond is the mirror image of a putable bond: keeping a 3.30% bond alive for an extra year when the forward rate is below 3.30% is exactly the same cash-flow decision as declining to put a three-year 3.30% bond in Year 2, which is why a three-year putable bond and a two-year extendible bond with the same coupon must trade at the same price (V6 p.122, p.141).

> [!abstract] Idea 1: the decomposition carries the whole module
> $V_{\text{callable}} = V_{\text{straight}} - V_{\text{call}}$ and $V_{\text{putable}} = V_{\text{straight}} + V_{\text{put}}$ (V6 p.125).
> Every qualitative question is answered by asking what happens to the option value and then applying the sign.
> Volatility up: both option values up, so callable down, putable up (V6 p.130, p.131).
> Curve flattens or inverts: call value up, put value down (V6 p.134, p.136).
> The option can never have negative value, so the callable never trades above the straight bond and the putable never trades below it.

Valuation is a present-value exercise, but with options the cash flows are contingent on future rates, so we need to know the bond's value at future decision dates, not just today.
That is why the framework works with one-period forward rates and a tree rather than with spot rates: spot rates give one number today, while forward rates give the value of the remaining cash flows at every future node where an exercise decision must be made (V6 p.126).
At zero volatility the tree collapses to a single path of forward rates.
The three-year 4.25% bond of Exhibit 1 is worth 102.114 discounted along that path; callable at par at Years 1 and 2 it is worth 101.707 because the issuer calls in Year 1 where the bond would otherwise be worth 100.417; putable at par it is worth 102.397 because the investor puts in Year 2 where it would otherwise be worth 99.700 (V6 p.126, p.127, p.128).

When volatility is switched on, rates branch up and down from every node with equal risk-neutral probability, and the dispersion of the branches is set by the volatility assumption through the fixed ratio $R_u = R_d e^{2\sigma\sqrt{t}}$ (V6 p.130, p.137).
The tree is calibrated so that it reprices the par curve exactly, which keeps the whole exercise arbitrage-free (V6 p.137).

> [!abstract] Idea 2: value node by node, and let the option holder act rationally at every node
> Work from maturity backward.
> At each node, discount the expected value of the two successor nodes plus the coupon at that node's one-period rate.
> Then apply the exercise test: the issuer calls whenever the computed value exceeds the call price (replace the value with the call price), and the investor puts whenever the computed value is below the put price (replace it with the put price) (V6 p.136, p.137, p.138, p.139).
> The exercise test happens before the value is passed one column to the left, which is exactly where distractors are built.

The economics of volatility follow immediately from the tree.
More volatility spreads the future rate states wider, which creates more states in which an option finishes in the money; an option is a claim on the favorable tail, so its value can only grow with dispersion (V6 p.130).
For the 30-year callable of Exhibit 5 the call is worth 4.60% of par at zero volatility and 14.78% at 30% volatility; the straight bond does not move, so the callable bond loses the whole difference (V6 p.131).
The putable mirror: the put is worth 2.30% of par at zero volatility and 10.54% at 30%, and the putable bond gains that value (V6 p.132).

Level and shape effects are about where the tree's forward rates sit relative to the coupon.
When the whole curve falls, the straight bond rises but the call goes deeper into the money, so the callable bond's rise is muted: on a 5% flat curve the callable is worth 86.90 (straight 92.27 minus call 5.37), and when the curve drops to 3% flat the straight gains 40% while the callable gains only 27% (V6 p.133).
An upward-sloping curve pushes the forward rates high, which keeps the call out of the money and the put in business; flattening or inversion drags forward rates down, multiplying the nodes where the issuer would call and starving the put of exercise opportunities (V6 p.134, p.136).
This is why the call option on the 30-year bond is worth about 8% of par on a 2%-to-4% upward curve, about 10% on a 4% flat curve and over 12% on an inverted curve (V6 p.134).

Most bonds carry default risk, and the industry-standard fix is to push the discount rates up by a constant spread (V6 p.144).
For an option-free bond that constant is the Z-spread; for a bond with options the same constant added to every one-period forward rate in the tree is the option-adjusted spread, found by trial and error so that the model value equals the market price (V6 p.145).
The OAS is "option adjusted" because the exercise rule at every node has already stripped the option effect out of the spread, leaving compensation for credit and liquidity only, which makes OAS comparable across bonds with and without options: higher OAS than comparable bonds means cheap, lower means rich (V6 p.146).
The trap is that the OAS is a model number: widen the assumed volatility and the call option eats more of the callable bond's value, so the constant spread needed to hit the same market price shrinks, from 138.2 bps at zero volatility to 1.2 bps at 30% volatility in Exhibit 16 (V6 p.147).

> [!abstract] Idea 3: with options, risk measures must come from the model, not from yield
> Modified duration assumes the cash flows do not move when rates move, which is false for bonds with options, so only effective (curve) duration and effective convexity are valid (V6 p.150).
> Reprice the bond off shifted curves at a constant OAS and difference the prices.
> The callable bond's duration collapses when rates fall (call goes in the money) and its convexity turns negative near the money; the putable bond's duration collapses when rates rise and its convexity stays positive (V6 p.152, p.153, p.158).

Because the price response is asymmetric, the two-sided average can mislead, and one-sided durations tell the true story: a currently callable 4.5% bond at 99.75 has one-sided up-duration 1.94 against one-sided down-duration 0.84, because no investor pays more than the call price for an immediately callable bond (V6 p.154, p.155).
Key rate durations expose which part of the curve matters: an option-free par bond responds only to its maturity-matched par rate, low-coupon or zero-coupon bonds can show negative short-maturity key rate durations, and for bonds with options the sensitivity migrates from the maturity date to the exercise date as the option goes deeper in the money (V6 p.155, p.156, p.157).

![[Callable-Putable-Price-Yield.excalidraw]]

Caps and floors on floaters are the same machinery with automatic exercise: the cap is an issuer option that truncates the coupon from above, the floor an investor option that props it up from below, so $V_{\text{capped}} = V_{\text{straight}} - V_{\text{cap}}$ and $V_{\text{floored}} = V_{\text{straight}} + V_{\text{floor}}$ (V6 p.161, p.162).
An uncapped, unfloored floater paying the reference rate set in arrears is always worth par at reset because the coupon equals the discount rate at every node; the value of the cap or floor is the deviation from 100 (V6 p.162, p.163).

The convertible bond swaps the interest rate option for an equity option: the investor holds a call on the issuer's stock, pays for it through a lower coupon, and gets a security whose floor is the straight bond value and whose upside is the stock (V6 p.166, p.172).
The key numbers are ratios of the same three inputs (bond price, share price, conversion ratio): conversion value is what the shares are worth now, market conversion price is the effective price paid per share through the bond, and the premium metrics measure what the investor pays for the downside protection (V6 p.168, p.169, p.170).
The risk-return profile slides along the share price: well below the conversion price the bond is busted and trades on rates and credit spreads, well above it trades like the stock, and in between it is a hybrid (V6 p.172, p.173).

## Formulas and derivations

**Value of a callable bond and the embedded call** (V6 p.125)
$$
V_{\text{callable}} = V_{\text{straight}} - V_{\text{call}}, \qquad V_{\text{call}} = V_{\text{straight}} - V_{\text{callable}}
$$
^f-06-03-1

- $V_{\text{straight}}$: arbitrage-free value of the identical option-free bond; $V_{\text{call}}$: value of the issuer's call option, always $\geq 0$.
- The investor is long the bond and short the call, so the call reduces the price the investor will pay.
- In practice the option is valued as the difference of the two bond values because the bond values are what the tree produces directly.

**Value of a putable bond and the embedded put** (V6 p.125)
$$
V_{\text{putable}} = V_{\text{straight}} + V_{\text{put}}, \qquad V_{\text{put}} = V_{\text{putable}} - V_{\text{straight}}
$$
^f-06-03-2

- The investor is long both the bond and the put, so the put raises the price.
- Sign discipline: subtract what the issuer holds, add what the investor holds; the same rule prices caps (subtract) and floors (add) on floaters and every convertible combination.

**Forward-rate indifference (curve equivalence)** (V6 p.126)
$$
(1 + z_2)^2 = (1 + z_1)(1 + F_{1,1}), \qquad (1 + z_3)^3 = (1 + z_2)^2 (1 + F_{2,1})
$$
^f-06-03-3

- $z_t$: spot rate for maturity $t$; $F_{t,1}$: one-year forward rate $t$ years from now.
- Investing at the spot rate for two years or rolling one-year investments at the forward must pay the same, or an arbitrage exists; this is what makes discounting one year at a time along forwards equal to spot discounting.
- With the Exhibit 1 curve (par 2.500%, 3.000%, 3.500%): $z_2 = 3.008\%$, $z_3 = 3.524\%$, $F_{1,1} = 3.518\%$, $F_{2,1} = 4.564\%$, and the three-year 4.25% straight bond is worth 102.114 either way (V6 p.126).

**Backward induction with the exercise rule** (V6 p.136, p.137, p.138)
$$
V_{\text{node}} = \frac{C + 0.5\,(V_{u} + V_{d})}{1 + r_{\text{node}}}, \qquad V_{\text{node}} \to \min(V_{\text{node}}, \text{Call price}) \text{ or } \max(V_{\text{node}}, \text{Put price})
$$
^f-06-03-4

- $C$: coupon paid at the end of the period; $V_u, V_d$: already-exercised values at the two successor nodes; $r_{\text{node}}$: one-period rate at the node; probabilities are 0.5 and 0.5 by construction.
- The issuer calls when continuation value exceeds the call price (calling is cheaper than leaving the debt outstanding); the investor puts when continuation value is below the put price.
- Replace the node value with the exercise price before discounting it back one more period; forgetting the replacement reproduces the straight-bond value, which is always a distractor.

> [!tip] Calculator
> One node of Exhibit 12: `98.791 + 99.738 = ÷ 2 = + 4.25 = ÷ 1.038695 =` gives 99.658.
> Chain the same keystroke pattern right to left; write the exercised value next to each node before moving left.

**Binomial tree rate link at volatility sigma** (V6 p.137)
$$
R_u = R_d \, e^{2\sigma\sqrt{t}}
$$
^f-06-03-5

- $R_u, R_d$: one-period forward rates in the up and down states of the same time slice; $\sigma$: annual interest rate volatility (decimal); $t$: years per time slice (1 here, so adjacent rates differ by the factor $e^{2\sigma}$).
- The tree is calibrated iteratively so that each slice both satisfies this ratio and reprices the par bond of that maturity at 100; rates from the calibration are frozen slice by slice (V6 p.137).
- Sanity check on any printed tree: at 10% volatility adjacent rates are in ratio $e^{0.20} = 1.2214$; at 15%, $e^{0.30} = 1.3499$.

**Z-spread pricing of a risky option-free bond** (V6 p.145)
$$
V = \sum_t \frac{CF_t}{\prod_{s \le t} \left(1 + F_{s} + Z\right)}
$$
^f-06-03-6

- $Z$: the constant zero-volatility spread added to every one-period forward rate $F_s$ so that the model value matches the market price.
- With $Z = 100$ bps on the Exhibit 1 forwards, the three-year 4.25% bond is worth 99.326 versus 102.114 default-free (V6 p.145).
- The Z-spread of an option-free bond is exactly its OAS at zero volatility (V6 p.145).

**Option-adjusted spread condition** (V6 p.145)
$$
\text{Market price} = V_{\text{tree}}\left(r_{\text{node}} + \text{OAS at every node, exercise rule applied}\right)
$$
^f-06-03-7

- OAS is found by trial and error: if the model value at a trial spread is above the market price, the spread is too small; below, too large (V6 p.145).
- Interpretation versus comparable bonds of the same characteristics and credit quality: higher OAS means underpriced (cheap), lower means overpriced (rich) (V6 p.146).
- OAS falls as assumed volatility rises for a callable bond (the option absorbs more of the price), so quoted OAS is only meaningful together with its volatility assumption (V6 p.146, p.147).

**Effective duration** (V6 p.150)
$$
\text{EffDur} = \frac{(PV_-) - (PV_+)}{2 \times (\Delta \text{Curve}) \times (PV_0)}
$$
^f-06-03-8

- $\Delta\text{Curve}$: parallel shift of the benchmark par curve in decimal; $PV_-$ and $PV_+$: full prices off the down-shifted and up-shifted curves, each revalued on a re-generated tree at the constant OAS implied by $PV_0$; $PV_0$: current full price.
- Procedure: (1) imply the OAS from the market price, (2) shift the curve down, rebuild the tree, revalue at that OAS to get $PV_-$, (3) shift up for $PV_+$, (4) apply the formula (V6 p.151).
- Interpretation: EffDur 1.97 means a 100 bps parallel rise cuts the price by about 1.97% (V6 p.151).
- Ordering: EffDur of callable $\leq$ straight and EffDur of putable $\leq$ straight; a deep in-the-money option makes the bond trade like a straight bond maturing on the first exercise date; a floater at MRR flat has EffDur close to the time to the next reset (V6 p.152, p.153, p.154).

> [!tip] Calculator
> Example 7 Bond X: `101.194 - 99.860 = ÷ ( 2 × .003 × 100.594 ) =` gives 2.21.
> The denominator is always 2 times shift times current price; distractors drop the 2 or double the shift.

**One-sided durations** (V6 p.154, p.155)
$$
\text{EffDur}_{\text{up}} = \frac{(PV_0) - (PV_+)}{(\Delta \text{Curve}) (PV_0)}, \qquad \text{EffDur}_{\text{down}} = \frac{(PV_-) - (PV_0)}{(\Delta \text{Curve}) (PV_0)}
$$
^f-06-03-9

- Same inputs as effective duration but each side taken alone, so the asymmetry created by the option is visible.
- Callable near the money: up-duration exceeds down-duration (1.94 vs 0.84 in Exhibit 21) because the call price caps the upside; putable near the money: down-duration exceeds up-duration (4.51 vs 1.49 in Exhibit 22) because the put price floors the downside (V6 p.155).

**Effective convexity** (V6 p.158)
$$
\text{EffCon} = \frac{(PV_-) + (PV_+) - 2 (PV_0)}{(\Delta \text{Curve})^2 \times (PV_0)}
$$
^f-06-03-10

- Same shifted prices as effective duration; measures how duration itself responds to rate moves.
- Straight bonds: low positive convexity; putable bonds: always positive, turning strongly positive when the put is near the money; callable bonds: convexity turns negative when the call is near the money because the upside is capped (V6 p.158).
- Curriculum example: $PV_0 = 100.785$ (OAS 40 bps), $PV_- = 101.381$, $PV_+ = 100.146$, EffCon $= (101.381 + 100.146 - 201.570)/(0.003^2 \times 100.785) = -47.41$; raw convexity is sometimes rescaled by 100 in practice (V6 p.158).

**Capped floater decomposition** (V6 p.161)
$$
V_{\text{capped floater}} = V_{\text{straight floater}} - V_{\text{cap}}
$$
^f-06-03-11

- The cap keeps the coupon from rising above the cap rate, protecting the issuer, so it is an issuer option and its value is subtracted.
- On the tree, the coupon set at each node (in arrears, paid one period later) is $\min(r_{\text{node}}, \text{cap})$; the straight floater is worth 100 at every reset, so the cap's value is $100 - V_{\text{capped}}$ (V6 p.162).

**Floored floater decomposition** (V6 p.162)
$$
V_{\text{floored floater}} = V_{\text{straight floater}} + V_{\text{floor}}
$$
^f-06-03-12

- The floor keeps the coupon from falling below the floor rate, protecting the investor, so its value is added.
- On the tree the coupon at each node is $\max(r_{\text{node}}, \text{floor})$; check the Year 0 node too, where a floor above today's rate is already binding (V6 p.163).

**Conversion price and conversion value** (V6 p.166, p.168, p.174)
$$
\text{Conversion price} = \frac{\text{Par value}}{\text{Conversion ratio}}, \qquad \text{Conversion value} = \text{Share price} \times \text{Conversion ratio}
$$
^f-06-03-13

- The conversion ratio is the number of shares per bond; corporate actions (splits, bonus issues, rights) adjust price and ratio in opposite directions so that par is preserved, and dividends above the threshold dividend adjust the conversion price downward (V6 p.167).
- Twitter example: ratio 17.5 per $1,000, conversion price $57.14, conversion value at issuance $40.10 \times 17.5 = \$701.75$ and on 15 June 2019 $35.14 \times 17.5 = \$614.95$ (V6 p.166, p.168).

**Minimum value of a convertible bond** (V6 p.168)
$$
V_{\text{conv}}^{\min} = \max\left(\text{Conversion value},\ V_{\text{straight}}\right)
$$
^f-06-03-14

- Below conversion value, buy the bond, convert, sell the shares; below straight value, the convertible out-yields the identical non-convertible bond; either way arbitrage forces the price back up (V6 p.169).
- The floor is a moving floor: the straight value falls when rates rise or the issuer's credit spread widens (V6 p.168).
- Twitter on 15 June 2019: $\max(614.95,\ 894.86) = \$894.86$ (V6 p.169).

**Market conversion price and premium per share** (V6 p.169)
$$
\text{Market conversion price} = \frac{\text{Convertible bond price}}{\text{Conversion ratio}}, \qquad \text{Premium per share} = \text{MCP} - \text{Share price}
$$
^f-06-03-15

- The market conversion price is the break-even price effectively paid per share by buying the bond and converting; use the current bond price, never the initial conversion price (V6 p.169, p.170).
- The premium per share is the cost of the downside protection provided by the straight-value floor, analogous to a call option premium except that the floor itself moves (V6 p.170).

**Market conversion premium ratio** (V6 p.170)
$$
\text{Market conversion premium ratio} = \frac{\text{Market conversion premium per share}}{\text{Underlying share price}}
$$
^f-06-03-16

- Expresses the premium as a percentage of the current share price; Twitter: $19.26 / 35.14 = 54.8\%$ (V6 p.170).
- A discount is theoretically possible when the two markets disconnect, for example under highly volatile share prices (V6 p.170).

**Premium over straight value** (V6 p.170)
$$
\text{Premium over straight value} = \frac{\text{Convertible bond price}}{\text{Straight value}} - 1
$$
^f-06-03-17

- A downside-risk gauge: the higher the premium, the less protection per unit of price and the less attractive the convertible, all else equal (V6 p.170).
- Flawed because the straight value itself moves with rates and spreads (V6 p.171).
- Twitter: $952.25 / 894.86 - 1 = 6.41\%$ (V6 p.170).

**Convertible bond decompositions** (V6 p.172)
$$
V_{\text{conv}} = V_{\text{straight}} + V_{\text{stock call}}, \qquad V_{\text{call.\,put.\,conv}} = V_{\text{straight}} + V_{\text{stock call}} - V_{\text{issuer call}} + V_{\text{investor put}}
$$
^f-06-03-18

- Each component is valued separately in the arbitrage-free framework; no matter how many options are embedded, the procedure is the same tree with exercise decisions at each node (V6 p.172).
- Sign check by holder: the investor owns the stock call and the put (add), the issuer owns the bond call (subtract).

> [!tip] Calculator
> Practice Q35 in one pass: `978 + 147 - 43 + 26 =` gives 1,108.
> Convertible metrics chain: `1230 ÷ 23.26 = STO 1` (market conversion price 52.88), `- 52 =` (premium per share 0.88).

## Worked examples

All numbers below were recomputed in Python; where the last digit differs from the printed exhibit by 0.001 it is a node-rounding artifact and is flagged.

### Example 1: Types of Embedded Options (V6 p.124)

Q1: Investors in putable bonds most likely seek to take advantage of higher interest rates, improvements in the issuer's credit rating, or movements in the issuer's stock price?
A (higher interest rates) is correct.
When rates rise the bond's continuation value falls below par; the investor puts at par and reinvests the proceeds at the new higher yield.
Credit improvements help any bondholder and are not the put's purpose, and stock price movements drive conversion options, not puts.
Q2: The conversion option is a right held by the issuer, the bondholders, or both jointly?
B (the bondholders) is correct.
The conversion option is a call on the issuer's stock held by the investor; the issuer's lever over conversion is the separate bond call used to force conversion. ^ex-06-03-1

### Example 2: Default-Free Callable and Putable Bonds (V6 p.129)

Three identical five-year sovereign bonds: Bond A option-free, Bond B callable at par in Years 2 and 3, Bond C callable at par in Years 2 and 3 and putable at par in Year 1.
Q1: Bond B versus Bond A: lower.
$V_{\text{callable}} = V_{\text{straight}} - V_{\text{call}}$ and the call has positive value, so B must be worth less; the issuer's right to refinance caps the investor's upside.
Q2: Bond C versus Bond B: higher.
C is B plus an investor put, and $V_{\text{put}} \geq 0$, so C is worth more.
Q3: If rates are expected to rise, Bond C will most likely be put by the bondholders.
Rising rates push continuation values below par at the put date, so the put goes in the money; the call would go further out of the money, and expecting no exercise ignores the put's purpose. ^ex-06-03-2

### Example 3: Callable Bond with Interest Rate Volatility (V6 p.138, p.139)

Base case: three-year 4.25% annual coupon bond callable at par at Years 1 and 2, par curve 2.500%/3.000%/3.500%, volatility 10%, tree rates Year 0: 2.5000%, Year 1: 3.8695%/3.1681%, Year 2: 5.5258%/4.5242%/3.7041% (V6 p.136).
Full backward induction (recomputed):
Year 2 values: $104.25/1.055258 = 98.791$; $104.25/1.045242 = 99.738$; $104.25/1.037041 = 100.526 \to$ called, reset to 100.
Year 1 up: $(4.25 + 0.5 \times (98.791 + 99.738))/1.038695 = 99.658$, not called.
Year 1 down: $(4.25 + 0.5 \times (99.738 + 100))/1.031681 = 100.922 \to$ called, reset to 100.
Year 0: $(4.25 + 0.5 \times (99.658 + 100))/1.025 = 101.540$ (my unrounded run gives 101.541; the curriculum's 101.540 uses the rounded node values).
Call value $= 102.114 - 101.540 = 0.574$, versus 0.407 at zero volatility, confirming that option value grows with volatility (V6 p.138).
Q1: At 15% volatility the callable bond's value is less than 101.540.
Higher volatility raises the call value that is subtracted from the unchanged straight value.
Q2: Callable at 102 instead of 100, the value is closest to 102.114.
No node value in Exhibit 12 exceeds 102, so the call is never exercised, the option is worthless, and the callable bond equals the straight bond at 102.114. ^ex-06-03-3

### Example 4: Putable Bond with Interest Rate Volatility (V6 p.140, p.141)

Same bond putable at par at Years 1 and 2, same tree.
Year 2 values: 98.791 and 99.738 are below 100 $\to$ put, reset to 100; 100.526 stays.
Year 1 up: $(4.25 + 0.5 \times (100 + 100))/1.038695 = 100.366$, not put.
Year 1 down: $(4.25 + 0.5 \times (100 + 100.526))/1.031681 = 101.304$, not put.
Year 0: $(4.25 + 0.5 \times (100.366 + 101.304))/1.025 = 102.522$.
Put value $= 102.522 - 102.114 = 0.408$ versus 0.283 at zero volatility (V6 p.140).
Q1: At 20% volatility the putable bond is worth more than 102.522, because the put value that is added grows with volatility.
Q2: Putable at 95 instead of 100, the value is closest to 102.114.
No node value falls below 95, the put is worthless, and the putable bond equals the straight bond. ^ex-06-03-4

### Example 5: Bonds with Embedded Options and Volatility (V6 p.141, p.142, p.143, p.144)

WA's default-free three-year annual bonds: Bond X 5.2% callable at par Years 1 and 2; Bond Y unknown coupon, callable at par Years 1 and 2, price 101.325; Bond Z 4.8% putable at par Year 2.
Par rates 4.400%/4.700%/5.000%, volatility 15%, tree Year 0: 4.4000%, Year 1: 5.7678%/4.2729%, Year 2: 7.4832%/5.5437%/4.1069%.
Q1: Price of Bond X.
Year 2: $105.2/1.074832 = 97.876$; $105.2/1.055437 = 99.674$; $105.2/1.041069 = 101.050 \to 100$.
Year 1 up: $(5.2 + 0.5 \times (97.876 + 99.674))/1.057678 = 98.305$.
Year 1 down: $(5.2 + 0.5 \times (99.674 + 100))/1.042729 = 100.733 \to 100$.
Year 0: $(5.2 + 0.5 \times (98.305 + 100))/1.044 = 99.954$ (B); my unrounded run gives 99.955, same choice.
Q2: Coupon of Bond Y is closest to 6.000% (C).
Elimination is fastest: the three-year par rate is 5%, so a 5% straight bond is worth par and a 5% callable must be worth less than par, well below 101.325, killing B; a 4.2% coupon is worth even less, killing A.
Verification with a 6% coupon: Year 2: $106/1.074832 = 98.620$; $106/1.055437 = 100.432 \to 100$; $106/1.041069 = 101.818 \to 100$.
Year 1 up: $(6 + 0.5 \times (98.620 + 100))/1.057678 = 99.567$; Year 1 down: $(6 + 0.5 \times (100 + 100))/1.042729 = 101.656 \to 100$.
Year 0: $(6 + 0.5 \times (99.567 + 100))/1.044 = 101.325$, matching the quoted price exactly.
Q3: Price of Bond Z (putable Year 2 only).
Year 2: $104.8/1.074832 = 97.504 \to 100$; $104.8/1.055437 = 99.295 \to 100$; $104.8/1.041069 = 100.666$ stays.
Year 1 up: $(4.8 + 0.5 \times (100 + 100))/1.057678 = 99.085$ (no put right in Year 1).
Year 1 down: $(4.8 + 0.5 \times (100 + 100.666))/1.042729 = 100.825$.
Year 0: $(4.8 + 0.5 \times (99.085 + 100.825))/1.044 = 100.340$ (B).
Q4: At lower volatility Bond X's price is higher: smaller call value subtracted from an unchanged straight value.
Q5: At higher volatility Bond Z's price is higher: larger put value added. ^ex-06-03-5

### Example 6: Option-Adjusted Spread (V6 p.147, p.148)

Three-year 7% annual French corporate bond callable at par Years 1 and 2, valued off the government par curve 4.600%/4.900%/5.200% at 15% volatility, tree Year 0: 4.6000%, Year 1: 5.9988%/4.4440%, Year 2: 7.7515%/5.7425%/4.2541%; the bond should carry an OAS of 200 bps.
Q1: The OAS is added to the rates in the binomial tree (B).
It is never netted against the coupon and never subtracted; it shifts every one-period forward rate up by the same amount.
Q2: Value at 15% volatility with OAS 200 bps.
Shifted rates: Year 0: 6.6000%, Year 1: 7.9988%/6.4400%, Year 2: 9.7515%/7.7425%/6.2541%.
Year 2: $107/1.097515 = 97.493$; $107/1.077425 = 99.311$; $107/1.062541 = 100.702 \to 100$.
Year 1 up: $(7 + 0.5 \times (97.493 + 99.311))/1.079988 = 97.595$.
Year 1 down: $(7 + 0.5 \times (99.311 + 100))/1.064400 = 100.202 \to 100$.
The printed exhibit shows 101.199 at this node; my recomputation gives 100.202 with the reset Year 2 value (or 100.532 without the reset), so the printed intermediate looks like a typo, but the node exceeds 100 under every variant, is called either way, and the final answer is unaffected.
Year 0: $(7 + 0.5 \times (97.595 + 100))/1.066 = 99.247$ (B).
Q3: Holding the price fixed, the OAS at 20% volatility is lower (A): more volatility makes the call absorb more value, so a smaller spread reprices the bond.
^ex-06-03-6

### Example 7: Interest Rate Sensitivity (V6 p.158, p.159, p.160)

Bond X: three-year 3.75% annual, callable at par in Year 1, $PV_0 = 100.594$, $PV_- = 101.194$, $PV_+ = 99.860$ for 30 bps shifts.
Bond Y: three-year 3.75% annual, putable at par in Year 1, $PV_0 = 101.330$, $PV_- = 101.882$, $PV_+ = 100.924$.
Q1: EffDur of Bond X $= (101.194 - 99.860)/(2 \times 0.003 \times 100.594) = 1.334/0.60356 = 2.21$ (B).
A (0.67) is below the roughly one-year duration of even a certain one-year call; C (4.42, the answer without the factor 2) exceeds the bond's three-year maturity.
Q2: EffDur of Bond Y $= (101.882 - 100.924)/(2 \times 0.003 \times 101.330) = 0.958/0.60798 = 1.58$ (C).
Q3: When rates rise, Bond Y's effective duration shortens (B): the put goes into the money and the bond trades toward the put date.
The callable lengthens toward straight-bond duration (call moves out of the money), and a straight bond's effective duration falls, not rises, as rates rise.
Q4: With Bond Y's put in the money, one-sided durations show more sensitivity to a decrease in rates (A): the put price floors the downside while the upside is unlimited.
Q5: Bond X's price responds to all par rate shifts but most to the one-year and three-year rates (C): the call decision at Year 1 turns on the two-year forward rate one year from now, which those two par rates drive.
Q6: Bond X's effective convexity turns negative when the call is near the money (B): the call caps the upside, so the price gains less on the down-shift than it loses on the up-shift.
Q7: For a given rate decline, Bond X has less upside than Bond Y (B): the call is exercised into strength, while the putable bond's upside is uncapped; putable convexity is always positive, and straight bonds have low positive convexity. ^ex-06-03-7

### Example 8: Capped and Floored Floaters (V6 p.163, p.164, p.165)

Base tree as in Exhibit 11 (2.5000%; 3.8695%/3.1681%; 5.5258%/4.5242%/3.7041%), coupons set in arrears.
Q1: Three-year floater capped at 5.600% is worth 100.000 (A).
The highest node rate is 5.5258%, below the cap, so the cap never binds and the floater is a par instrument at every reset; recomputation confirms 100.000.
The curriculum's own capped example at 4.500% (Exhibit 26) is the template: cap binds at the 5.5258% and 4.5242% nodes, Year 2 values $104.5/1.055258 = 99.028$ and $104.5/1.045242 = 99.977$, bottom node uncapped at 100, Year 1 values 99.521 and 99.989, Year 0 value $(2.5 + 0.5 \times (99.521 + 99.989))/1.025 = 99.761$, so the cap is worth $100 - 99.761 = 0.239$ (V6 p.162).
Q2: Three-year floater floored at 3.000% is worth 100.488 (B).
The only node below 3.000% is Year 0 at 2.5000%, so only the Year 1 coupon is raised to 3.000: Year 2 and Year 1 values all equal 100, and Year 0 $= (3.0 + 0.5 \times (100 + 100))/1.025 = 100.488$.
C (103.000) ignores discounting entirely, and A misses that the floor binds today; the curriculum's 3.500% floor (Exhibit 27) binds at Year 0 and at the 3.1681% node and is worth $101.133 - 100 = 1.133$ (V6 p.163).
Q3: Eurozone floater at 12-month MRR + 320 bps capped at 5.50%, 8% volatility, tree of all-in rates Year 0: 3.7430%, Year 1: 5.2908%/4.9817%, Year 2: 5.8865%/5.4893%/5.1508%.
Year 2: top coupon capped, $105.5/1.058865 = 99.635$; middle $105.4893/1.054893 = 100$; bottom $105.1508/1.051508 = 100$.
Year 1 up: $(5.2908 + 0.5 \times (99.635 + 100))/1.052908 = 99.827$; Year 1 down: $(4.9817 + 100)/1.049817 = 100$.
Year 0: $(3.7430 + 0.5 \times (99.827 + 100))/1.037430 = 99.916$ (B).
The 5.50% cap gives away slightly more value than the extra 20 bps of spread adds, which is why the note prices just under par. ^ex-06-03-8

### Example 9: Valuation of Convertible Bonds (V6 p.174, p.175, p.176)

Heavy Element 3.75% annual convertible, issued 15 September 2020 at $1,000 par, maturing 2025, conversion ratio 23.26; on 16 September 2022 the bond trades at $1,230 and the stock at $52.
Q1: Conversion price $= 1{,}000 / 23.26 = \$42.99 \approx \$43$ (B).
Q2: Conversion value $= 52 \times 23.26 = \$1{,}209.52 \approx \$1{,}209$ (C).
Q3: Market conversion premium per share $= 1{,}230/23.26 - 52 = 52.88 - 52 = \$0.88$ (A).
Q4: With the share price ($52) above the conversion price ($43), the bond is equity-like (B); a busted convertible requires the share to sit well below the conversion price.
Q5: Narrowing credit spreads will not change the price significantly (B): an equity-like convertible is driven by the share price, not by rates or spreads.
Q6: At a market price of $1,050, below the $1,209 conversion value, the arbitrage is to buy the bond, convert, and sell the shares (B), pocketing $1{,}209.52 - 1{,}050 = \$159.52$ per bond; shorting the convertible in A and C shorts the cheap asset and loses.
Q7: After the share falls to $28, well below $43, the bond is a busted convertible with bond-like risk-return characteristics (A); hybrid behavior needs the share near the conversion price and equity behavior needs it above. ^ex-06-03-9

## Item-set patterns

> [!warning] Trap 1: the volatility dial
> The vignette changes the volatility assumption (10% to 15%) and asks for the direction of a bond's value or its OAS.
> Correct approach: option value always rises with volatility, so callable value falls, putable value rises, and for a fixed market price the callable's OAS falls.
> Distractors offer "unchanged" (tempting because the curve did not move) and the straight-bond logic (tempting because volatility does not affect option-free values, which is true but irrelevant).

> [!warning] Trap 2: forgetting the exercise rule at a node
> A tree valuation whose answer choices include the straight-bond value.
> Correct approach: at every exercise date compare the computed node value with the exercise price, reset it (call: take the minimum; put: take the maximum), and only then discount left.
> The straight value (no resets) and the value from resetting at only one of the two dates are the standard wrong answers; in Practice Q5 the straight value 103.688 sits one choice away from the putable answer 103.744.

> [!warning] Trap 3: OAS comparisons across credit quality
> A table of callable bonds with OAS figures and mixed ratings asks which is cheap.
> Correct approach: higher OAS than bonds of similar characteristics and credit quality means underpriced; the comparison is only valid within the same rating bucket.
> The distractor pairs a CCC bond's 105 bps against a B bond's 85 bps; the extra spread is default compensation, not cheapness (Practice Q18).

> [!warning] Trap 4: effective duration denominator surgery
> The vignette hands you $PV_-$, $PV_+$, $PV_0$ and a shift and asks for EffDur.
> Correct approach: $(PV_- - PV_+)/(2 \times \Delta\text{Curve} \times PV_0)$ with the shift in decimal.
> Distractors drop the factor 2 (doubling the answer, often exceeding maturity, which is your sanity check), use the shift in bps, or use a shifted price as $PV_0$.

> [!warning] Trap 5: sign of the option in a decomposition
> A convertible with several embedded options and the component values listed.
> Correct approach: add what the investor holds (stock call, investor put), subtract what the issuer holds (bond call): $978 + 147 - 43 + 26 = 1{,}108$ (Practice Q35).
> The distractors flip exactly one sign, most often adding the issuer call or subtracting the investor put.

> [!warning] Trap 6: currently callable at par means the price is pinned
> A bond callable at par today (or with no protection period) and a straight value above 100.
> Correct approach: no investor pays above the price at which the bond can be called away immediately, so the market price caps at 100 and the call is worth straight value minus 100 (Practice Q14, Q17).
> The straight value (100.879) is the trap answer for the price.

> [!warning] Trap 7: set in arrears, and the floor that binds today
> Capped or floored floater on a tree; the phrase "set in arrears" means the coupon fixed at a node is paid one period later.
> Correct approach: cap or floor the coupon at each node including Year 0; a floor above today's rate is already binding even though every future node clears it (Example 8 Q2, Practice Q24).
> Distractors apply the cap or floor only at maturity nodes or ignore the Year 0 reset.

> [!warning] Trap 8: initial conversion price versus market conversion price
> A convertible bought in the secondary market, with the issue-date conversion price, the current bond price and the current share price all quoted.
> Correct approach: market conversion price = current bond price divided by the conversion ratio; the premium per share subtracts the current share price.
> Using the initial conversion price (Practice Q34 choice A) or the issue-date share price (choice C) are both planted.

> [!warning] Trap 9: which duration moves, and which way
> "When interest rates rise, the effective duration of ..." with callable, putable and straight bonds on offer.
> Correct approach: rates up puts the put in the money (putable duration shortens) and pushes the call out of the money (callable duration lengthens toward the straight bond's); rates down mirrors this.
> The tempting error is to reason from price change direction instead of from which option moves into the money.

> [!warning] Trap 10: curve shape versus curve level
> The vignette forecasts flattening or inversion rather than a parallel move.
> Correct approach: flattening or inversion lowers the forward rates on the tree, which multiplies call-exercise opportunities (call value up) and starves put-exercise opportunities (put value down); an upward-sloping curve does the reverse.
> Distractors treat flattening as neutral or apply the level logic (rates fall, both bonds gain) to the shape question.

## Practice problems

> [!note] Kept private
> These are the curriculum's end-of-module problems, restated with solutions; the problems are CFA Institute copyright, so they live in the gitignored `17-CFA/Private/CFA-L-2/Practice-Problems/` and render here only where that folder exists.

![[LM03-Valuation-and-Analysis-of-Bonds-with-Embedded-Options-Practice-Problems]]

## Cross-links

- [[LM01-The-Term-Structure-and-Interest-Rate-Dynamics]]: supplies the spot, par and forward rate machinery and the equivalence between the three curve forms that Exhibit 1 rehearses; the bootstrap and forward indifference equations here come straight from that module.
- [[LM02-The-Arbitrage-Free-Valuation-Framework]]: builds and calibrates the binomial interest rate tree and proves backward induction reprices the par curve; this module adds only the exercise decision at each node, so tree mechanics rusty there will fail here.
- [[LM04-Credit-Analysis-Models]]: takes over where OAS stops, making default probabilities and recovery explicit instead of packing credit into a constant spread; the Z-spread and OAS defined here are the reduced-form benchmarks that module refines.
- [[LM02-Valuation-of-Contingent-Claims]]: the Derivatives treatment of option valuation on binomial trees; the conversion option priced there as an equity call is the component added to the straight bond in the convertible decomposition, and the volatility-raises-option-value logic is shared.

## Self-test

Vignette: Priya Nair values three-year annual-pay bonds of Kestrel Corp on a benchmark tree calibrated at 10% volatility (one-year par rate 3.000%): Year 0: 3.0000%, Year 1: 4.4150%/3.6150%, Year 2: 5.9280%/4.8540%/3.9740%.
Kestrel's bonds, all 4.6% coupon: Bond K1 straight (value on the tree 101.837); Bond K2 callable at par at Years 1 and 2; Bond K3 putable at par at Years 1 and 2.
Nair also examines a Kestrel floater paying the one-year reference rate set in arrears, in capped (4.25%) and floored (3.80%) variants, and a Kestrel convertible: par $1,000, conversion ratio 20, bond price $1,060, share price $44, straight value $965.
For a separate callable holding she records $PV_0 = 102.280$, $PV_- = 102.890$, $PV_+ = 101.650$ for 25 bps shifts.

1. The value of Bond K2 is closest to:
A. 100.879.
B. 101.292.
C. 101.837.

2. The value of Bond K3 is closest to:
A. 101.837.
B. 102.242.
C. 102.646.

3. The value of the call option embedded in Bond K2 is closest to:
A. 0.404.
B. 0.546.
C. 0.950.

4. If Nair reruns the valuation at 5% volatility, the value of Bond K2 will most likely:
A. fall.
B. be unchanged.
C. rise.

5. Bond K2's market price implies an OAS of 18 bps at 10% volatility. If Nair repeats the OAS calculation at 15% volatility holding the price fixed, the OAS will most likely:
A. fall.
B. be unchanged.
C. rise.

6. The effective duration of the separate callable holding is closest to:
A. 1.21.
B. 2.42.
C. 4.85.

7. The value of the capped floater is closest to:
A. 99.286.
B. 100.000.
C. 100.714.

8. The market conversion premium ratio of the convertible is closest to:
A. 9.8%.
B. 13.6%.
C. 20.5%.

9. If the convertible's price fell to $850 with the share still at $44, the nearest-term consequence is:
A. the bond is put back to Kestrel at par.
B. arbitrageurs buy the bond, convert, and sell shares for a $30 per bond profit.
C. arbitrageurs short the bond and buy the stock for a $30 per bond profit.

10. For the separate callable holding, which statement about its risk profile is most accurate?
A. Its one-sided down-duration exceeds its one-sided up-duration.
B. Its effective convexity is closest to $-31$, so its upside is smaller than its downside.
C. Its effective convexity is positive because callable bonds behave like straight bonds near the money.

> [!success]- Answer key
> 1. B.
> Year 2: $104.6/1.059280 = 98.746$; $104.6/1.048540 = 99.758$; $104.6/1.039740 = 100.602 \to 100$.
> Year 1 up: $(4.6 + 0.5 \times (98.746 + 99.758))/1.044150 = 99.461$; Year 1 down: $(4.6 + 0.5 \times (99.758 + 100))/1.036150 = 101.124 \to 100$.
> Year 0: $(4.6 + 0.5 \times (99.461 + 100))/1.03 = 101.292$.
> C is the straight value (no resets); A applies the call reset at every node including where the value is below par.
> 2. B.
> Year 2: $98.746 \to 100$; $99.758 \to 100$; 100.602 stays.
> Year 1 up: $(4.6 + 0.5 \times (100 + 100))/1.044150 = 100.177$; Year 1 down: $(4.6 + 0.5 \times (100 + 100.602))/1.036150 = 101.241$.
> Year 0: $(4.6 + 0.5 \times (100.177 + 101.241))/1.03 = 102.242$.
> A is the straight value; C double-counts by adding the put value to the putable value.
> 3. B.
> $V_{\text{call}} = V_{\text{straight}} - V_{\text{callable}} = 101.837 - 101.292 = 0.546$ (rounding of the node values can shift the third decimal).
> A is the put option's value ($102.242 - 101.837 = 0.404$); C is the sum of both options, which answers no question.
> 4. C.
> Lower volatility shrinks the call value subtracted from the unchanged straight value, so the callable bond rises.
> 5. A.
> At higher assumed volatility the call absorbs more value, so a smaller constant spread reprices the same market price; callable OAS falls as assumed volatility rises.
> 6. B.
> $(102.890 - 101.650)/(2 \times 0.0025 \times 102.280) = 1.240/0.5114 = 2.42$.
> C drops the factor 2; A doubles the denominator's shift.
> 7. A.
> The cap binds at the 5.9280%, 4.8540% and 4.4150% nodes: Year 2 values $104.25/1.059280 = 98.416$, $104.25/1.048540 = 99.424$, $103.974/1.039740 = 100$; Year 1: $(4.25 + 0.5 \times (98.416 + 99.424))/1.044150 = 98.808$ and $(3.6150 + 0.5 \times (99.424 + 100))/1.036150 = 99.722$; Year 0: $(3.0 + 0.5 \times (98.808 + 99.722))/1.03 = 99.286$.
> B ignores the cap; C adds the cap value to par instead of subtracting.
> The floored variant for contrast: the 3.80% floor binds at Year 0 and the 3.6150% node, worth $100.863 - 100 = 0.863$.
> 8. C.
> Market conversion price $= 1{,}060/20 = \$53$; premium per share $= 53 - 44 = \$9$; ratio $= 9/44 = 20.5\%$.
> A is the premium over straight value ($1{,}060/965 - 1 = 9.8\%$); B divides the premium by the market conversion price instead of the share price.
> 9. B.
> Conversion value $= 44 \times 20 = \$880 >$ the $850 price, so buy at 850, convert, sell shares for 880, earning $30; the minimum-value condition is violated.
> A invents a put; C shorts the cheap asset and loses the $30 instead.
> 10. B.
> EffCon $= (102.890 + 101.650 - 2 \times 102.280)/(0.0025^2 \times 102.280) = -0.020/0.000639 = -31.3$, negative because the near-the-money call caps the upside.
> A describes a putable bond's asymmetry; C states the opposite of the computed sign.

## Flashcards

#flashcards/cfa-l2/06-Fixed-Income/lm03

Value of a callable bond in terms of the straight bond::Value of straight bond minus value of the issuer call option (V6 p.125)

Value of a putable bond in terms of the straight bond::Value of straight bond plus value of the investor put option (V6 p.125)

Who holds each embedded option?
?
Issuer holds the call and the cap on a floater.
Investor holds the put, the floor, the conversion option and the extension option.
Rule for value: subtract issuer options, add investor options (V6 p.121, p.161, p.162).

A Bermudan-style call is exercisable::only on a predetermined schedule of specified dates after the call protection period (V6 p.121)

An American-style call is exercisable::continuously, at any time starting on the first call date (V6 p.121)

A three-year 3.30% bond putable in Year 2 has the same value as::a two-year 3.30% bond extendible by one year at the same coupon (V6 p.141)

The issuer exercises the call at a node when::the present value of the bond's remaining cash flows exceeds the call price (V6 p.127, p.137)

The investor exercises the put at a node when::the present value of the bond's remaining cash flows is below the put price (V6 p.128, p.139)

The three steps to value a bond with embedded options under volatility are {{generate a rate tree from the yield curve and volatility}}, {{apply the exercise decision at each node}}, and {{backward induction from maturity}} (V6 p.136).

Binomial tree rate link at one time slice::Ru equals Rd times e to the power 2 sigma root t, so adjacent rates at 10% volatility differ by factor 1.2214 (V6 p.137)

Higher interest rate volatility does what to callable and putable bond values?
?
Both embedded option values rise.
Callable bond value falls (call is subtracted).
Putable bond value rises (put is added) (V6 p.130, p.131).

As the yield curve flattens or inverts, the embedded call option value {{rises}} and the embedded put option value {{falls}}, because lower forward rates create more call-exercise and fewer put-exercise opportunities (V6 p.134, p.136).

Why does a callable bond rise less than its straight bond when the curve level falls?::The call moves into the money and its growing value offsets part of the straight bond's gain (V6 p.133)

Definition of OAS::the constant spread that, added to every one-period forward rate on the tree with the exercise rule applied, makes the model value equal the market price (V6 p.145)

Relation of Z-spread to OAS::the Z-spread of an option-free bond equals its OAS at zero interest rate volatility (V6 p.145)

A callable bond shows a higher OAS than comparable bonds of the same credit quality. Rich or cheap?::Cheap (underpriced); lower OAS would mean rich (V6 p.146)

Holding market price fixed, raising the volatility assumption moves a callable bond's OAS::down, because the more valuable call absorbs more of the price (V6 p.146, p.147)

Why is modified (yield) duration invalid for bonds with embedded options?::It assumes cash flows do not change when yields change, which fails when exercise is contingent on rates; use effective duration off shifted benchmark curves (V6 p.150)

Effective duration formula::PV minus, less PV plus, divided by 2 times delta-curve times PV zero (V6 p.150)

Effective convexity formula::PV minus, plus PV plus, minus twice PV zero, all divided by delta-curve squared times PV zero (V6 p.158)

30-second numeric: PV minus 101.599, PV plus 100.407, PV zero 101.000, shift 30 bps. EffDur?
?
Keystrokes: 101.599 minus 100.407 equals 1.192; 2 times .003 times 101 equals .606; 1.192 divided by .606 equals 1.97 (V6 p.151).

30-second numeric: PV minus 101.381, PV plus 100.146, PV zero 100.785, shift 30 bps. EffCon?
?
Numerator 101.381 plus 100.146 minus 201.570 equals negative 0.043.
Denominator .003 squared times 100.785 equals .000907.
EffCon approximately negative 47.4 (V6 p.158).

The four-step procedure for effective duration of a bond with options starts by::implying the OAS from the market price, then revaluing on down- and up-shifted trees at that same OAS (V6 p.151)

Effective duration of cash::zero (V6 p.154)

Effective duration of a zero-coupon bond::approximately its maturity (V6 p.154)

Effective duration of a floater at MRR flat::approximately the time to the next reset date (V6 p.154)

Can the effective duration of a callable or putable bond exceed that of the straight bond?::No; the option can only shorten it, and deep in the money the bond trades like a straight bond maturing at the first exercise date (V6 p.152, p.153)

When rates fall, the effective duration of a callable bond {{shortens}}; when rates rise, the effective duration of a putable bond {{shortens}} (V6 p.152, p.153).

For a callable bond near the money, which one-sided duration is larger?::One-sided up-duration exceeds one-sided down-duration, because the call price caps the upside (V6 p.155)

For a putable bond near the money, which one-sided duration is larger?::One-sided down-duration exceeds one-sided up-duration, because the put price floors the downside (V6 p.155)

For an option-free bond trading at par, which par rate shift changes its value?::Only the maturity-matched par rate; all other key rate durations are zero (V6 p.156)

Why can a 10-year zero-coupon bond have a negative five-year key rate duration?
?
Raising the five-year par rate leaves the 10-year par bond at par, so the 10-year zero rate must fall slightly to compensate for the higher five-year zero rate.
A lower 10-year zero rate raises the zero-coupon bond's value, so its value rises when the five-year par rate rises (V6 p.156).

As the coupon of a 30-year bond callable in 10 years rises, its dominant key rate duration migrates from the {{30-year}} rate to the {{10-year}} rate, because exercise becomes nearly certain (V6 p.157).

Effective convexity signs: straight bond {{low positive}}, putable bond {{always positive}}, callable bond {{negative when the call is near the money}} (V6 p.158).

Value of a capped floater::value of the straight floater minus the value of the embedded cap; the cap is an issuer option (V6 p.161)

Value of a floored floater::value of the straight floater plus the value of the embedded floor; the floor is an investor option (V6 p.162)

Why is an uncapped floater at the reference rate worth par at every reset?::The coupon set at each node equals that node's discount rate, so every node discounts to 100 (V6 p.162)

"Set in arrears" means::the coupon rate fixed at a node is paid at the end of that period, so a cap or floor at a node changes the next period's cash flow (V6 p.161)

30-second numeric: floater floored at 3.0%, Year 0 rate 2.5%, all other nodes above 3.0%, par curve gives straight value 100. Value?
?
Only the Year 1 coupon changes, to 3.0.
Keystrokes: 3.0 plus 100 equals 103; divide by 1.025 equals 100.488 (V6 p.164).

Conversion price::par value divided by the conversion ratio (V6 p.166, p.174)

Conversion value (parity value)::current share price times the conversion ratio (V6 p.168)

Minimum value of a convertible bond::the greater of the conversion value and the straight bond value; a moving floor because the straight value shifts with rates and spreads (V6 p.168)

Market conversion price::convertible bond price divided by the conversion ratio; the break-even share price effectively paid through the bond (V6 p.169)

Market conversion premium per share::market conversion price minus the current underlying share price (V6 p.169)

Market conversion premium ratio::market conversion premium per share divided by the underlying share price (V6 p.170)

Premium over straight value::convertible bond price divided by straight value, minus 1; flawed because the straight value floor moves (V6 p.170, p.171)

Value of a callable putable convertible bond
?
Straight bond value, plus the call option on the issuer's stock, minus the issuer call option on the bond, plus the investor put option on the bond (V6 p.172).

30-second numeric: straight 978, stock call 147, issuer call 43, investor put 26. Convertible value?
?
Keystrokes: 978 plus 147 minus 43 plus 26 equals 1,108 (V6 p.172).

A busted convertible trades on which factors?::Interest rates and credit spreads, like a straight bond, because the share price sits well below the conversion price (V6 p.172, p.173)

When the share price is above the conversion price, a convertible's price follows::the underlying stock, nearly one for one, and rate or spread moves matter little (V6 p.173)

Forced conversion happens when::the issuer calls a convertible while the share price is above the conversion price, making conversion the better choice for holders (V6 p.168)

A stock dividend above the threshold dividend adjusts the conversion price::downward, compensating convertible holders (V6 p.167)

After a 2-for-1 stock split, a conversion price of 57.14 and ratio of 17.5 become::28.57 and 35; price halves, ratio doubles (V6 p.167)

Hard put versus soft put::hard put must be redeemed in cash; soft put lets the issuer choose cash, stock, subordinated notes or a combination (V6 p.167)

Which convertible trap answer uses the initial conversion price?::The market conversion premium distractor; always divide the current bond price by the conversion ratio instead (V6 p.169)

A callable bond callable at par today with straight value above par trades at::the call price, 100; no investor pays more than the immediate call price (V6 p.154, p.128)

## Common mistakes

1. Forgetting to apply the exercise rule at every node and reporting the straight-bond value; in Practice Q5 the straight value 103.688 is planted next to the putable answer 103.744.
2. Applying the exercise reset after discounting to the earlier node instead of before; the reset value (not the computed value) is what enters the expected value one column left (V6 p.138).
3. Sign errors in the decomposition: adding the issuer call or subtracting the investor put, especially in the convertible combination formula (Practice Q35).
4. Reasoning that higher volatility helps both option holders' bonds; it raises both option values, but the callable bond loses value while the putable gains (V6 p.130, p.131).
5. Confusing level effects with shape effects: a falling level lifts both bonds (callable less), while flattening or inversion raises call value and lowers put value (V6 p.133, p.134, p.136).
6. Comparing OAS across different credit ratings; OAS relative value only works against bonds of similar characteristics and credit quality (Practice Q18).
7. Quoting OAS without its volatility assumption; the same price gives 138.2 bps at 0% volatility and 1.2 bps at 30% in Exhibit 16 (V6 p.147).
8. Dropping the factor 2 or misplacing the decimal shift in effective duration and convexity; an answer above the bond's maturity is the built-in sanity check (V6 p.150, Example 7).
9. Using modified (yield) duration for a bond with embedded options; only effective duration and effective convexity are valid because cash flows move with rates (V6 p.150).
10. Missing that a cap or floor can bind at the Year 0 node when the coupon is set in arrears (Example 8 Q2, Practice Q24).
11. Using the initial conversion price or the issue-date share price in market conversion premium calculations instead of the current bond price over the conversion ratio and the current share price (Practice Q34).
12. Treating the convertible's straight-value floor as fixed; it falls when rates rise or credit spreads widen, so premium over straight value understates downside risk (V6 p.168, p.171).

```dataview
LIST rule
FROM "17-CFA/CFA-L-2/23-Error-Log"
WHERE type = "cfa-error" AND lm = "06-03" AND resolved != true
```

## Teach-back

> [!note] Teach-back
> Write the module in your own words after Pass 1. Empty caps mastery at 60.
>
