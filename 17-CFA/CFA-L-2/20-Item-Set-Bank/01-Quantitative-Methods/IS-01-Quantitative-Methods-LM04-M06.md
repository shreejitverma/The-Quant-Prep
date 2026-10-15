---
type: cfa-itemset
topic: "Quantitative Methods"
topic_code: "01"
topic_slug: "01-Quantitative-Methods"
lm: 4
title: "Calder Ridge Advisors: IPO Allocation Models"
los: [los-01-04-a, los-01-04-b, los-01-04-c]
difficulty: 4
minutes: 12
source: mock-06
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/quantitative-methods]
---

# Calder Ridge Advisors: IPO Allocation Models

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Calder Ridge Advisors runs an equity fund that requests allocations in initial public offerings (IPOs).
Ingrid Solberg, CFA, the fund's quantitative analyst, maintains two models that the allocation desk uses before each book-building.

The first model is estimated by ordinary least squares on 60 IPOs.
The dependent variable, RET1, is the first-day return in percent.
LNSIZE is the natural log of offer proceeds in USD millions, and VC equals 1 if the issuer is venture-capital backed and 0 otherwise.
Every IPO lists on one of three venues: the Main Board, the Growth Market, or the Technology Segment.
GRW equals 1 for a Growth Market listing and TCH equals 1 for a Technology Segment listing.
VC_LNSIZE is the product of VC and LNSIZE.

**Exhibit 1: First-day return regression (n = 60)**

| | Coefficient | p-value |
|---|---|---|
| Intercept | 24.0 | 0.000 |
| LNSIZE | -3.2 | 0.001 |
| VC | 9.6 | 0.004 |
| GRW | 4.1 | 0.090 |
| TCH | 7.8 | 0.003 |
| VC_LNSIZE | -1.5 | 0.021 |

$R^2$ = 0.412; mean RET1 = 11.3%.

A junior colleague, Mateo Ferraz, reviewed the diagnostics on 2 October and wrote: "The model has four independent variables: size, VC backing, venue, and the interaction."
Solberg extracted the diagnostics for six IPOs (Exhibit 2).

**Exhibit 2: Influence diagnostics, selected IPOs**

| IPO | Leverage $h_{ii}$ | Studentized deleted residual $t_i^*$ |
|---|---|---|
| IPO-08 | 0.33 | 0.62 |
| IPO-15 | 0.28 | -2.41 |
| IPO-23 | 0.12 | 3.18 |
| IPO-31 | 0.36 | -2.12 |
| IPO-44 | 0.07 | -1.94 |
| IPO-52 | 0.26 | 1.21 |

Two-tailed 5% critical t-values: 2.007 (52 df), 2.006 (53 df), 2.005 (54 df).

Two deals are on the calendar.
Nordvik Robotics, VC-backed, is raising USD 150 million on the Technology Segment.
Aurelle Foods, not VC-backed, is raising USD 90 million on the Growth Market.

The second model is a logit estimated by maximum likelihood on 410 IPOs.
BREAK equals 1 if the stock closes its first day below the offer price.
TOP equals 1 if the lead underwriter is top-tier, HOT equals 1 if the IPO is priced in a month with above-median IPO volume, and DUAL equals 1 for a dual-class share structure.

**Exhibit 3: Break-issue logit (n = 410)**

| | Coefficient | p-value |
|---|---|---|
| Intercept | -3.10 | 0.000 |
| LNSIZE | 0.42 | 0.002 |
| VC | 1.35 | 0.010 |
| VC_LNSIZE | -0.38 | 0.015 |
| TOP | -0.60 | 0.008 |
| HOT | -0.85 | 0.001 |
| DUAL | 0.22 | 0.384 |

Log-likelihood = -212.4; LL-Null = -236.9.

The desk's policy caps the acceptable break probability at 25%.
Solberg must state the largest offer size, in USD millions, at which a single-class, non-VC-backed IPO led by a top-tier underwriter and priced outside a hot month stays within the cap.
She is also asked how VC backing changes the break probability for a USD 200 million single-class IPO led by a top-tier underwriter and priced outside a hot month.

## Questions

1. Based on Exhibits 1 and 2, the IPO(s) that breach both the leverage rule of thumb and the 5% studentized deleted residual test are: (LOS: los-01-04-a)
   - A. IPO-15 and IPO-31.
   - B. IPO-31 only.
   - C. none of the six IPOs.
2. Using Exhibit 1, the fitted first-day return of Nordvik Robotics minus that of Aurelle Foods is closest to: (LOS: los-01-04-b)
   - A. 4.15 percentage points.
   - B. 8.25 percentage points.
   - C. 11.67 percentage points.
3. The largest offer size at which the IPO described in the desk's policy stays within the 25% cap is closest to: (LOS: los-01-04-c)
   - A. USD 117 million.
   - B. USD 247 million.
   - C. USD 490 million.
4. For the USD 200 million IPO, the change in the break probability from being VC-backed rather than not VC-backed is closest to: (LOS: los-01-04-c)
   - A. -8.1 percentage points.
   - B. -10.1 percentage points.
   - C. +28.3 percentage points.

## Answer key

> [!success]- Answers and reasoning
> 1. **B.** The model has $k = 5$ independent variables: LNSIZE, VC, GRW, TCH, and VC_LNSIZE; three venues need $3 - 1 = 2$ dummies and the interaction is a regressor in its own right.
> Leverage cutoff $= 3(k+1)/n = 3 \times 6/60 = 0.3000$, which flags IPO-08 (0.33) and IPO-31 (0.36).
> Degrees of freedom $= n - k - 2 = 60 - 5 - 2 = 53$, so the critical value is 2.006, which flags IPO-15 ($|-2.41|$), IPO-23 (3.18), and IPO-31 ($|-2.12|$).
> Only IPO-31 appears in both sets.
> A is wrong because it uses a cutoff of 0.2500, obtained either from Ferraz's count of $k = 4$ ($3 \times 5/60$) or from $3k/n = 15/60$; that cutoff also flags IPO-15 (0.28) and IPO-52 (0.26), and IPO-15 then appears in both sets.
> C is wrong because it applies the $|t_i^*| > 3$ outlier rule (or counts only positive residuals), which flags only IPO-23, and IPO-23 has low leverage.
> 2. **A.** $\ln 150 = 5.0106$ and $\ln 90 = 4.4998$.
> Nordvik: $24.0 - 3.2(5.0106) + 9.6 + 7.8 - 1.5(5.0106) = 24.0 - 16.0340 + 9.6 + 7.8 - 7.5160 = 17.8500$.
> Aurelle: $24.0 - 3.2(4.4998) + 4.1 = 24.0 - 14.3994 + 4.1 = 13.7006$.
> Difference $= 17.8500 - 13.7006 = 4.1494$, about 4.15 percentage points.
> The VC effect for Nordvik is $9.6 - 1.5(5.0106) = 2.0840$, not 9.6, because the intercept and slope dummies together make the VC gap depend on size.
> B is wrong because it treats Aurelle as a Main Board (base) listing and omits the GRW shift: Aurelle $= 24.0 - 14.3994 = 9.6006$, so the gap becomes $4.1494 + 4.1 = 8.2494$.
> C is wrong because it ignores the slope dummy VC_LNSIZE and adds the full 9.6 intercept shift: the gap becomes $4.1494 + 1.5(5.0106) = 11.6654$.
> 3. **C.** The log odds matching a 25% probability are $\ln[0.25/(1 - 0.25)] = \ln(1/3) = -1.0986$.
> For VC = 0, TOP = 1, HOT = 0, DUAL = 0: $-3.10 + 0.42\,LNSIZE - 0.60 = -1.0986$, so $LNSIZE = 2.6014/0.42 = 6.1938$.
> Offer size $= e^{6.1938} = 489.69$, about USD 490 million.
> DUAL is set to zero by the single-class description, so its insignificant coefficient does not enter.
> A is wrong because it omits the TOP dummy: $LNSIZE = (-1.0986 + 3.10)/0.42 = 4.7652$ and $e^{4.7652} = 117.36$.
> B is wrong because it sets the log odds equal to $\ln 0.25 = -1.3863$, treating the probability as the odds: $LNSIZE = 2.3137/0.42 = 5.5088$ and $e^{5.5088} = 246.86$.
> 4. **A.** $\ln 200 = 5.2983$.
> Not VC-backed: $z_0 = -3.10 + 0.42(5.2983) - 0.60 = -1.4747$, so $P_0 = 1/(1 + e^{1.4747}) = 0.1862$.
> VC-backed: $z_1 = z_0 + 1.35 - 0.38(5.2983) = -1.4747 - 0.6634 = -2.1381$, so $P_1 = 1/(1 + e^{2.1381}) = 0.1055$.
> Change $= P_1 - P_0 = -0.0808$ from unrounded probabilities, about -8.1 percentage points; at this size the negative interaction outweighs the positive VC intercept shift.
> B is wrong because it approximates the discrete switch with the slope of the curve, $P_0(1 - P_0)(-0.6634) = 0.1862 \times 0.8138 \times (-0.6634) = -0.1005$, which overstates a large change because the logistic curve flattens as $P$ falls.
> C is wrong because it ignores the interaction and adds only the VC coefficient: $z = -1.4747 + 1.35 = -0.1247$, $P = 0.4689$, change $= +0.2826$.

## Distractor design

- Q1: A = leverage cutoff from $k = 4$ (interaction or venue miscounted) or $3k/n$; C = $|t^*| > 3$ outlier rule or sign ignored in place of the 5% test.
- Q2: B = wrong base category (Growth Market listing treated as the Main Board base); C = slope dummy VC_LNSIZE ignored.
- Q3: A = dummy TOP omitted from the index; B = probability converted to log odds without forming the odds first.
- Q4: B = linear slope approximation used for a discrete dummy switch; C = interaction term in the logit ignored.
