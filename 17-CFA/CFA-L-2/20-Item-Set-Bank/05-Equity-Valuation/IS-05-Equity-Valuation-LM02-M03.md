---
type: cfa-itemset
topic: "Equity Valuation"
topic_code: "05"
topic_slug: "05-Equity-Valuation"
lm: 2
title: "Tidewell Energy Storage: Pricing a Dividend That Has Not Started"
los: [los-05-02-a, los-05-02-j, los-05-02-n, los-05-02-p]
difficulty: 4
minutes: 12
source: mock-03
attempts: 0
tags: [cfa/l2, cfa/itemset, cfa/equity-valuation]
---

# Tidewell Energy Storage: Pricing a Dividend That Has Not Started

> [!info] Timer
> 12 minutes for 4 questions. Record confidence 1-5 before opening the answer key.

## Vignette

Farah Qureshi, CFA, is a senior analyst at the Ashgrove College Endowment, a US university endowment that holds non-controlling positions in listed mid-cap companies.
On 8 September 2026 she is valuing Tidewell Energy Storage Inc., a manufacturer of grid-scale battery systems whose shares trade at USD 10.20.
Tidewell has never paid a dividend.
Its board has announced that no dividend will be paid in years 1 and 2 while a second plant is completed, and that an initial annual dividend of USD 0.60 per share will be paid at the end of year 3.

Qureshi forecasts that the dividend will grow at 20% a year in years 4 and 5 and at 10% a year in years 6 and 7.
From year 8 onward she expects dividends to grow indefinitely at Tidewell's mature sustainable growth rate.
Her method sets that rate equal to the mature retention ratio multiplied by a mature ROE built from industry benchmark DuPont components, because Tidewell's current ratios reflect a young, highly levered balance sheet.
Tidewell's board has stated a long-run target payout ratio of 60% of earnings.

Exhibit 1: DuPont components

| Component | Tidewell, fiscal 2025 | Mature industry benchmark |
|---|---|---|
| Net profit margin | 7.2% | 6.0% |
| Total asset turnover | 1.30 | 1.10 |
| Equity multiplier | 2.10 | 1.50 |

Exhibit 2: Required return inputs

| Input | Value |
|---|---|
| 10-year US Treasury yield (risk-free rate) | 4.2% |
| Tidewell beta | 1.05 |
| Equity risk premium | 6.0% |
| Yield to maturity on Tidewell senior unsecured bonds | 7.3% |
| Risk premium over own-bond yield (committee guidance) | 4.5% |

Exhibit 3: Tidewell per-share forecasts (USD)

| | Year 1 | Year 2 | Year 3 | Year 4 |
|---|---|---|---|---|
| Earnings per share | 0.85 | 1.05 | 1.30 | 1.52 |
| Free cash flow to equity | -1.35 | -0.70 | 0.95 | 1.10 |

Qureshi's base case estimates the required return with the CAPM.
The endowment's investment committee treats a share as fairly valued when its price is within plus or minus 15% of the analyst's intrinsic value estimate.
The committee has also asked every analyst to show how the conclusion changes when the required return is instead estimated as the company's own bond yield plus the committee's risk premium.

Martin Oduya, a junior analyst on Qureshi's team, reviews her draft on 9 September 2026 and adds three statements about Tidewell to the file.

Statement 1: "Because Tidewell pays no dividend today, a dividend discount model cannot be used to value its shares."

Statement 2: "Residual income is a suitable alternative to the DDM for Tidewell, because it pays no dividend today and its free cash flow to equity is forecast to be negative in years 1 and 2."

Statement 3: "A free cash flow to equity model is the preferred alternative to the DDM for Tidewell precisely because its FCFE is forecast to be negative in the early years."

## Questions

1. The mature sustainable dividend growth rate that Qureshi should use from year 8 onward is closest to: (LOS: los-05-02-p)
   - A. 3.96%.
   - B. 5.94%.
   - C. 7.86%.
2. Using Qureshi's base case, the intrinsic value of a Tidewell share today is closest to: (LOS: los-05-02-n)
   - A. USD 9.97.
   - B. USD 10.76.
   - C. USD 13.13.
3. Under the committee's alternative required return, Tidewell's intrinsic value and the committee's conclusion are closest to: (LOS: los-05-02-j)
   - A. USD 15.50; undervalued.
   - B. USD 8.70; fairly valued.
   - C. USD 8.70; overvalued.
4. Which of Oduya's statements is most accurate? (LOS: los-05-02-a)
   - A. Statement 1.
   - B. Statement 2.
   - C. Statement 3.

## Answer key

> [!success]- Answers and reasoning
> 1. **A.** Mature ROE from the benchmark components $= 0.060 \times 1.10 \times 1.50 = 0.0990$, or 9.90%.
> Mature retention $= 1 - 0.60 = 0.40$, so $g = b \times ROE = 0.40 \times 9.90\% = 3.96\%$.
> The rate is below the required return in Question 2 (10.5%), so a Gordon terminal value is admissible.
> B is wrong because it multiplies ROE by the payout ratio instead of the retention ratio, $0.60 \times 9.90\% = 5.94\%$.
> C is wrong because it keeps Tidewell's current leverage-inflated ROE, $0.072 \times 1.30 \times 2.10 = 19.66\%$, and $0.40 \times 19.66\% = 7.86\%$, contrary to Qureshi's stated method.
> 2. **B.** CAPM: $r = 4.2\% + 1.05 \times 6.0\% = 10.5\%$.
> Dividends: $D_3 = 0.6000$, $D_4 = 0.7200$, $D_5 = 0.8640$, $D_6 = 0.9504$, $D_7 = 1.0454$, with PVs at 10.5% of $0.4447 + 0.4829 + 0.5244 + 0.5221 + 0.5197 = 2.4939$; the zero dividends in years 1 and 2 contribute nothing but still occupy two periods.
> Terminal value at $t = 7$: $D_8 = 1.0454 \times 1.0396 = 1.0868$; $V_7 = 1.0868/(0.105 - 0.0396) = 1.0868/0.0654 = 16.6183$.
> PV of $V_7 = 16.6183/1.105^7 = 16.6183/2.0116 = 8.2614$; $V_0 = 2.4939 + 8.2614 = 10.7552$, or USD 10.76.
> The terminal value is $8.2614/10.7552 = 76.8\%$ of value.
> Calculator: CF0 = 0, C01 = 0, C02 = 0, C03 = 0.60, C04 = 0.72, C05 = 0.864, C06 = 0.9504, C07 = 1.04544 + 16.6183 = 17.6637, I = 10.5, NPV = 10.76.
> Against the committee band of $0.85 \times 10.7552 = 9.1419$ to $1.15 \times 10.7552 = 12.3685$, the USD 10.20 price is inside, so the base case says fairly valued.
> A is wrong because it discounts $V_7$ eight periods, $16.6183/1.105^8 = 16.6183/2.2228 = 7.4763$, total 9.97.
> C is wrong because it places the first dividend at $t = 1$ and ignores the two dividend-free years, so every flow is discounted two periods too few: PV of dividends 3.0451 plus $16.6183/1.105^5 = 10.0873$, total 13.13.
> 3. **C.** Bond yield plus risk premium: $r = 7.3\% + 4.5\% = 11.8\%$.
> PVs of $D_3$ to $D_7$ at 11.8%: $0.4294 + 0.4609 + 0.4947 + 0.4867 + 0.4789 = 2.3504$.
> $V_7 = 1.0868/(0.118 - 0.0396) = 1.0868/0.0784 = 13.8627$; PV $= 13.8627/1.118^7 = 13.8627/2.1832 = 6.3498$; $V_0 = 2.3504 + 6.3498 = 8.7002$, or USD 8.70.
> Band around value: $0.85 \times 8.7002 = 7.3952$ to $1.15 \times 8.7002 = 10.0052$; the USD 10.20 price is above the upper bound, so the shares are overvalued.
> A 1.3-percentage-point change in $r$ flips the conclusion because the terminal value (73.0% of value here) is capitalized at $r - g_L$.
> A is wrong because it adds the premium to the risk-free rate instead of Tidewell's own bond yield, $r = 4.2\% + 4.5\% = 8.7\%$, giving $V_7 = 22.9291$ and $V_0 = 2.7114 + 12.7873 = 15.50$, a band of 13.17 to 17.82 and an undervalued call.
> B is wrong because it builds the band around the price, $10.20 \pm 1.53$ or 8.67 to 11.73, which contains 8.70; the band must be built around intrinsic value.
> 4. **B.** Residual income is a suitable alternative for a non-dividend payer and is preferred when free cash flow is expected to be negative within the forecast horizon, because it recognizes value through book value rather than through distant positive cash flows.
> Tidewell meets both conditions: it pays no dividend today and its FCFE is forecast to be negative in years 1 and 2.
> A is wrong because a multistage DDM with zero dividends in the early years is valid when the timing and size of the initial dividend can be forecast, which the board's announcement makes possible here.
> C is wrong because negative near-term free cash flow is the case in which a free cash flow model is least convenient, since the present value of the negative flows is negative and value depends on distant positive flows; it is the argument for residual income, not for FCFE.

## Distractor design

1. B: payout used instead of retention in $g = b \times ROE$; C: current leverage-inflated ROE not normalized to benchmark components (misread exhibit and method).
2. A: terminal value discounted $n + 1$ periods; C: dividend-free years dropped from the timeline, so the first dividend is discounted as if paid at $t = 1$ (period error).
3. A: risk premium added to the risk-free rate instead of the company's own bond yield (wrong formula variant); B: fair value band built around price instead of intrinsic value.
4. A: absence of a current dividend treated as ruling out a DDM; C: negative free cash flow read as a reason for a free cash flow model rather than for residual income.
