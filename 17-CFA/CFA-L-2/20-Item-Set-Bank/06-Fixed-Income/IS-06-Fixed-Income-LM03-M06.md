---
type: cfa-itemset
topic: "Fixed Income"
topic_code: "06"
topic_slug: "06-Fixed-Income"
lm: 3
title: "Tessaro Brands Treasury Funding Review"
los: [los-06-03-e, los-06-03-m, los-06-03-n, los-06-03-o]
difficulty: 3
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/fixed-income]
---

# Tessaro Brands Treasury Funding Review

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Ines Carvalho is the treasurer of Tessaro Brands, a BBB-rated consumer goods company.
She is preparing the annual funding review for Tessaro's board with Rohan Mehta, a debt capital markets banker at Albury & Finch.
Tessaro has three debt instruments outstanding.

- 2034 bonds: 4.90% annual coupon, callable by Tessaro at par on each coupon date from 2029.
- 2031 notes: 4.20% annual coupon, putable by investors at par in 2028.
- Convertible bonds: 1.75% annual coupon, par USD 1,000, maturing 2030, convertible into 25 Tessaro shares per bond, and callable by Tessaro at USD 1,020 at any time; the bonds carry no put.

**Exhibit 1: Tessaro convertible bond data on 11 September**

| Item | Value |
|---|---|
| Share price at issuance | USD 34.50 |
| Current share price | USD 46.00 |
| Current convertible bond price | USD 1,212 |
| Straight value (same terms, no conversion option) | USD 1,010 |
| Issuer call price | USD 1,020 |
| Threshold dividend per share | USD 0.60 |
| Current annual dividend per share | USD 0.52 |

The board has also asked Carvalho to evaluate a proposed three-year floating-rate note.
The note would pay the one-year market reference rate (MRR) plus 150 bps annually, set in arrears.
The all-in coupon would be floored at 4.30% and capped at 5.80%.
Mehta explains that 150 bps matches Tessaro's current credit spread, so a note without the cap and floor would price at par.
He supplies a binomial tree of all-in rates, equal to the one-year benchmark rates calibrated at 12% volatility plus 150 bps.

**Exhibit 2: All-in one-year rates (benchmark plus 150 bps)**

| Node | Year 0 | Year 1 | Year 2 |
|---|---|---|---|
| Upper | 4.1000% | 5.7818% | 7.0881% |
| Middle | | | 5.8958% |
| Lower | | 4.8681% | 4.9578% |

At the funding meeting on 12 September, Carvalho and Mehta each make a statement about the existing bonds.

Statement 1 (Carvalho): "If the whole yield curve falls by 100 bps, our 2034 callable bonds will gain as much in price as an option-free Tessaro bond with the same coupon and maturity, because the cash flows are identical until the call is exercised."

Statement 2 (Mehta): "If the curve flattens, with the one-year rate unchanged and longer rates falling, the put in our 2031 notes becomes less valuable to investors."

Carvalho then turns to the convertible.
The board wants to reduce leverage without spending cash, and she asks Mehta whether calling the convertible today would achieve that.
She also asks him how expensive the convertible looks relative to Tessaro's straight debt, because several holders have told her they regard the bond mainly as downside protection.
Mehta notes that Tessaro's dividend is below the threshold dividend in the indenture.

## Questions

1. Which of the statements made at the 12 September meeting is correct? (LOS: los-06-03-e)
   - A. Statement 1 only
   - B. Statement 2 only
   - C. Both Statement 1 and Statement 2
2. The value of the proposed floored and capped floating-rate note is closest to: (LOS: los-06-03-m)
   - A. 99.686
   - B. 99.878
   - C. 100.192
3. The premium over straight value of the Tessaro convertible is closest to: (LOS: los-06-03-o)
   - A. 5.39%
   - B. 13.86%
   - C. 20.00%
4. If Tessaro calls the convertible today, the most likely outcome is that holders: (LOS: los-06-03-n)
   - A. surrender their bonds for USD 1,020 each in cash, which Tessaro must fund.
   - B. convert into shares worth USD 1,150 per bond, retiring the debt without a cash outlay.
   - C. receive a downward adjustment of the conversion price to compensate for the lost coupons.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** Statement 2 is correct: flattening lowers the one-period forward rates on the tree, which reduces the number of nodes where the value of the notes falls below the put price, so the put loses value (V6 p.134, p.136).
> Statement 1 is wrong: when the curve level falls, the straight bond rises but the call moves toward or into the money, so the value of the issuer's call rises and offsets part of the gain, and the callable bond rises less than the option-free bond (V6 p.133).
> A is wrong because it treats the callable's cash flows as fixed, ignoring that exercise depends on rates.
> C is wrong because Statement 1 fails for the reason above.
> 2. **B.** Coupons are set in arrears at $\min(\max(r_{\text{node}}, 4.30\%), 5.80\%)$ and discounted at the all-in node rate (V6 p.161, p.162).
> Year 2 upper: $7.0881\% > 5.80\%$, so the coupon is capped: $105.80/1.070881 = 98.7972$.
> Year 2 middle: $5.8958\% > 5.80\%$, capped: $105.80/1.058958 = 99.9095$.
> Year 2 lower: 4.9578% lies inside the collar, so the node is worth 100.
> Year 1 upper: 5.7818% is just below the cap, so the coupon is 5.7818: $(5.7818 + 0.5 \times (98.7972 + 99.9095))/1.057818 = 99.3887$.
> Year 1 lower: $(4.8681 + 0.5 \times (99.9095 + 100))/1.048681 = 99.9569$.
> Year 0: 4.1000% is below the 4.30% floor, so the Year 1 coupon is 4.30: $(4.30 + 0.5 \times (99.3887 + 99.9569))/1.041 = 99.8778$.
> The cap (issuer option) is worth more than the floor (investor option), so the note prices below par.
> A is wrong because it applies the cap but ignores that the floor already binds at Year 0: $(4.10 + 0.5 \times (99.3887 + 99.9569))/1.041 = 99.6857$.
> C is wrong because it applies the floor but ignores the cap, so every later node is worth 100: $(4.30 + 100)/1.041 = 100.1921$.
> 3. **C.** Premium over straight value $= 1{,}212/1{,}010 - 1 = 20.00\%$ (V6 p.170).
> A is wrong because it is the market conversion premium ratio: market conversion price $= 1{,}212/25 = 48.48$, premium per share $= 48.48 - 46.00 = 2.48$, and $2.48/46.00 = 5.39\%$.
> B is wrong because it compares the conversion value, $46.00 \times 25 = 1{,}150$, with the straight value instead of the bond price: $1{,}150/1{,}010 - 1 = 13.86\%$.
> 4. **B.** Conversion value $= 46.00 \times 25 = \$1{,}150$, above the USD 1,020 call price, so holders facing the call convert rather than accept cash; this is forced conversion, and it retires the debt by issuing shares (V6 p.168).
> A is wrong because rational holders would give up USD 130 per bond by taking the call price.
> C is wrong because conversion terms are adjusted for corporate actions and for dividends above the threshold dividend, and Tessaro's USD 0.52 dividend is below the USD 0.60 threshold (V6 p.167).

## Distractor design

- Q1: A applies option-free logic to a callable bond under a level change (ignores the call); C accepts both statements without testing the level effect.
- Q2: A skips the floor at the Year 0 node (set-in-arrears timing error); C applies the floor but omits the cap (partial exercise).
- Q3: A substitutes the market conversion premium ratio (wrong formula variant); B puts the conversion value in the numerator (misread exhibit).
- Q4: A ignores that conversion value exceeds the call price (holder behavior misread); C confuses a call with a conversion-price adjustment trigger (wrong feature).
