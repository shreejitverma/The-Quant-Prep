"""Backtest Overfitting Trap and Deflated Sharpe Analyzer.

Standard-library only implementation of:
1. Bailey and Lopez de Prado (2014) Deflated Sharpe Ratio (DSR) & Probabilistic Sharpe Ratio (PSR).
2. Harvey, Liu, and Zhu (2016) multiple-testing haircuts (Bonferroni, Holm, BHY FDR) and t > 3.0 threshold.
3. Bailey, Borwein, Lopez de Prado, and Zhu (2017) Combinatorially Symmetric Cross-Validation (CSCV)
   and Probability of Backtest Overfitting (PBO).
4. Parameter grid mining demonstration showing how pure noise generates spurious in-sample Sharpe > 2.0.
5. Minimum Backtest Length (MinBTL) calculation.
"""

from __future__ import annotations

import itertools
import math
import random
from typing import Any

from .base import LabResult, Param, TradingLabEngine
from .registry import register

_LOG_SQRT_2PI = 0.5 * math.log(2.0 * math.pi)


def norm_cdf(x: float) -> float:
    """Standard normal cumulative distribution function."""
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def norm_logsf(x: float) -> float:
    """Natural log of the standard normal upper tail P(Z > x), finite for every finite x.

    Uses erfc (no cancellation in the tail) and, past x = 30 where erfc nears underflow,
    the Mills-ratio asymptotic series, whose truncation error there is below 2e-12.
    """
    if x < 30.0:
        return math.log(0.5 * math.erfc(x / math.sqrt(2.0)))
    inv = 1.0 / (x * x)
    series = 1.0 - inv + 3.0 * inv**2 - 15.0 * inv**3 + 105.0 * inv**4
    return -0.5 * x * x - math.log(x) - _LOG_SQRT_2PI + math.log(series)


def norm_isf_log(log_p: float) -> float:
    """Upper-tail quantile x >= 0 with log P(Z > x) = log_p, for log_p <= log(0.5).

    Newton iteration on the concave norm_logsf, so tail probabilities far below the
    smallest double (t-stats past 38) still invert without underflow.
    """
    if log_p >= -math.log(2.0):
        return 0.0
    x = -norm_inv_cdf(math.exp(log_p)) if log_p > -700.0 else math.sqrt(-2.0 * log_p)
    for _ in range(100):
        log_sf = norm_logsf(x)
        hazard = math.exp(-0.5 * x * x - _LOG_SQRT_2PI - log_sf)
        step = (log_sf - log_p) / hazard
        x += step
        if abs(step) <= 1e-14 * (1.0 + abs(x)):
            break
    return x


def norm_inv_cdf(p: float) -> float:
    """High-precision inverse normal CDF using Acklam's rational approximation.

    Accurate to within 1.15e-9 across 0 < p < 1.
    """
    if p <= 0.0:
        return -1e10
    if p >= 1.0:
        return 1e10
    if math.isclose(p, 0.5):
        return 0.0

    a1 = -3.969683028665376e01
    a2 = 2.209460984245205e02
    a3 = -2.759285104469687e02
    a4 = 1.383577518672690e02
    a5 = -3.066479806614716e01
    a6 = 2.506628277459239e00

    b1 = -5.447609879822406e01
    b2 = 1.615858368580409e02
    b3 = -1.556989798598866e02
    b4 = 6.680131188771972e01
    b5 = -1.328068155288572e01

    c1 = -7.784894002430293e-03
    c2 = -3.223964580411365e-01
    c3 = -2.400758277161838e00
    c4 = -2.549732539343734e00
    c5 = 4.374664141464968e00
    c6 = 2.938163982698783e00

    d1 = 7.784695709041462e-03
    d2 = 3.224671290700398e-01
    d3 = 2.445134137142996e00
    d4 = 3.754408661907416e00

    p_low = 0.02425
    p_high = 1.0 - p_low

    if p < p_low:
        q = math.sqrt(-2.0 * math.log(p))
        return (((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / ((((d1 * q + d2) * q + d3) * q + d4) * q + 1.0)
    elif p <= p_high:
        q = p - 0.5
        r = q * q
        return (((((a1 * r + a2) * r + a3) * r + a4) * r + a5) * r + a6) * q / (((((b1 * r + b2) * r + b3) * r + b4) * r + b5) * r + 1.0)
    else:
        q = math.sqrt(-2.0 * math.log(1.0 - p))
        return -((((((c1 * q + c2) * q + c3) * q + c4) * q + c5) * q + c6) / ((((d1 * q + d2) * q + d3) * q + d4) * q + 1.0))


def euler_mascheroni() -> float:
    return 0.57721566490153286


def expected_max_null_sharpe(num_trials: int, variance: float) -> float:
    """Expected maximum Sharpe ratio from N independent trials under the null hypothesis (Bailey & Lopez de Prado 2014)."""
    if num_trials <= 1:
        return 0.0
    gamma = euler_mascheroni()
    p1 = 1.0 - (1.0 / num_trials)
    p2 = 1.0 - (1.0 / (num_trials * math.e))
    z1 = norm_inv_cdf(p1)
    z2 = norm_inv_cdf(p2)
    bracket = (1.0 - gamma) * z1 + gamma * z2
    return math.sqrt(variance) * bracket


def probabilistic_sharpe_ratio(
    observed_sharpe: float,
    benchmark_sharpe: float,
    sample_length: int,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> float:
    """Calculate Probabilistic Sharpe Ratio (PSR) of Bailey and Lopez de Prado (2012).

    Parameters are in consistent periodic units (e.g. Daily).
    """
    if sample_length <= 1:
        return 0.0
    denom_var = 1.0 - skewness * observed_sharpe + ((kurtosis - 1.0) / 4.0) * (observed_sharpe**2)
    if denom_var <= 0:
        denom_var = 1e-6
    se = math.sqrt(denom_var / (sample_length - 1))
    z = (observed_sharpe - benchmark_sharpe) / se
    return norm_cdf(z)


def deflated_sharpe_ratio(
    observed_sharpe_ann: float,
    num_trials: int,
    sample_length_days: int,
    variance_ann: float,
    skewness: float = 0.0,
    kurtosis: float = 3.0,
) -> tuple[float, float, float]:
    """Calculate Deflated Sharpe Ratio (DSR) in Bailey & Lopez de Prado (2014).

    Returns (dsr_prob, expected_max_sr_ann, psr_zero).
    """
    sqrt_252 = math.sqrt(252.0)
    sr_daily = observed_sharpe_ann / sqrt_252
    var_daily = variance_ann / 252.0 if variance_ann > 0 else (1.0 / (sample_length_days - 1))

    # Expected max daily Sharpe under null
    sr_0_daily = expected_max_null_sharpe(num_trials, var_daily)
    sr_0_ann = sr_0_daily * sqrt_252

    dsr = probabilistic_sharpe_ratio(
        observed_sharpe=sr_daily,
        benchmark_sharpe=sr_0_daily,
        sample_length=sample_length_days,
        skewness=skewness,
        kurtosis=kurtosis,
    )
    psr_zero = probabilistic_sharpe_ratio(
        observed_sharpe=sr_daily,
        benchmark_sharpe=0.0,
        sample_length=sample_length_days,
        skewness=skewness,
        kurtosis=kurtosis,
    )
    return dsr, sr_0_ann, psr_zero


HLZ_T_HURDLE = 3.0


def harvey_liu_haircuts(sharpe_ann: float, sample_length_days: int, num_trials: int) -> dict[str, float]:
    """Harvey, Liu, and Zhu (2016) multiple-testing adjustments (Bonferroni, Sidak, BHY).

    Each adjustment maps the two-sided raw p-value to an adjusted p-value and back to an
    adjusted t-stat and Sharpe; the work is done on log p-values so huge t-stats neither
    underflow nor invent a haircut. The HLZ t > 3.0 hurdle already prices in multiple
    testing, so it is applied to the raw t-stat, never to an adjusted one.
    """
    years = max(0.1, sample_length_days / 252.0)
    t_stat = sharpe_ann * math.sqrt(years)
    log_p = min(0.0, math.log(2.0) + norm_logsf(abs(t_stat)))
    p_val = math.exp(log_p)
    log_n = math.log(num_trials)

    def adjusted(log_p_adj: float) -> tuple[float, float, float]:
        t_adj = norm_isf_log(min(0.0, log_p_adj) - math.log(2.0))
        sr_adj = max(0.0, t_adj / math.sqrt(years))
        haircut = max(0.0, (1.0 - sr_adj / sharpe_ann) * 100.0) if sharpe_ann > 0 else 100.0
        return t_adj, sr_adj, haircut

    t_bonf, sr_bonf, haircut_bonf = adjusted(log_p + log_n)

    if p_val * num_trials > 1e-12:
        p_sidak = -math.expm1(num_trials * math.log1p(-p_val)) if p_val < 1.0 else 1.0
        log_p_sidak = math.log(p_sidak)
    else:
        log_p_sidak = log_p + log_n
    t_sidak, sr_sidak, haircut_sidak = adjusted(log_p_sidak)

    # BHY under arbitrary dependence: harmonic factor c(M) = sum_{j=1}^M 1/j
    c_m = sum(1.0 / j for j in range(1, num_trials + 1))
    t_bhy, sr_bhy, haircut_bhy = adjusted(log_p + log_n + math.log(c_m))

    return {
        "t_stat": round(t_stat, 3),
        "raw_p_value": p_val,
        "t_bonferroni": round(t_bonf, 3),
        "sharpe_bonferroni": round(sr_bonf, 3),
        "haircut_bonferroni_pct": round(haircut_bonf, 2),
        "t_sidak": round(t_sidak, 3),
        "sharpe_sidak": round(sr_sidak, 3),
        "haircut_sidak_pct": round(haircut_sidak, 2),
        "t_bhy": round(t_bhy, 3),
        "sharpe_bhy": round(sr_bhy, 3),
        "haircut_bhy_pct": round(haircut_bhy, 2),
        "passes_hlz_threshold": 1.0 if t_stat >= HLZ_T_HURDLE else 0.0,
    }


def min_backtest_length_years(num_trials: int, target_sharpe_ann: float) -> float:
    """Bailey et al. (2014) minimum backtest length in years to clear selection bias.

    Infinite for a non-positive Sharpe, which no backtest length can establish as skill;
    zero for a single trial, which carries no selection bias.
    """
    if target_sharpe_ann <= 0.0:
        return math.inf
    if num_trials <= 1:
        return 0.0
    gamma = euler_mascheroni()
    p1 = 1.0 - (1.0 / num_trials)
    p2 = 1.0 - (1.0 / (num_trials * math.e))
    bracket = (1.0 - gamma) * norm_inv_cdf(p1) + gamma * norm_inv_cdf(p2)
    return (bracket / target_sharpe_ann) ** 2


def run_cscv_and_mining_simulation(
    num_trials: int,
    sample_length_days: int,
    num_blocks: int = 6,
    seed: int = 42,
) -> dict[str, Any]:
    """Execute CSCV on simulated multi-trial noise matrix to compute empirical PBO and OOS decay."""
    rng = random.Random(seed)
    sqrt_252 = math.sqrt(252.0)

    # 1. Generate matrix of returns for N random noise strategies over T days
    # True expected return is strictly 0.0
    daily_vol = 0.15 / sqrt_252
    returns_matrix: list[list[float]] = []
    for _ in range(num_trials):
        series = [rng.gauss(0.0, daily_vol) for _ in range(sample_length_days)]
        returns_matrix.append(series)

    # 2. Divide timeline into S contiguous blocks
    block_size = sample_length_days // num_blocks
    blocks = [range(i * block_size, (i + 1) * block_size) for i in range(num_blocks)]

    # 3. Combinations of S choose S/2 for training splits
    half_s = num_blocks // 2
    combinations = list(itertools.combinations(range(num_blocks), half_s))

    oos_ranks: list[float] = []
    under_median_count = 0
    in_sample_sharpes: list[float] = []
    out_of_sample_sharpes: list[float] = []

    def calc_sharpe(indices: list[int], series: list[float]) -> float:
        sub = [series[idx] for idx in indices]
        n = len(sub)
        if n < 2:
            return 0.0
        m = sum(sub) / n
        var = sum((x - m) ** 2 for x in sub) / (n - 1)
        std = math.sqrt(var) if var > 0 else 1e-8
        return (m / std) * sqrt_252

    for combo in combinations:
        train_blocks = set(combo)
        train_indices = [idx for b in range(num_blocks) if b in train_blocks for idx in blocks[b]]
        test_indices = [idx for b in range(num_blocks) if b not in train_blocks for idx in blocks[b]]

        # In-sample Sharpes for all N strategies
        is_sharpes = [calc_sharpe(train_indices, returns_matrix[n]) for n in range(num_trials)]
        best_n = max(range(num_trials), key=lambda n: is_sharpes[n])
        best_is_sr = is_sharpes[best_n]
        in_sample_sharpes.append(best_is_sr)

        # Out-of-sample Sharpes for all N strategies
        oos_sharpes = [calc_sharpe(test_indices, returns_matrix[n]) for n in range(num_trials)]
        best_oos_sr = oos_sharpes[best_n]
        out_of_sample_sharpes.append(best_oos_sr)

        # Out-of-sample relative rank of the in-sample winner
        sorted_oos = sorted(oos_sharpes)
        rank = sum(1 for x in sorted_oos if x <= best_oos_sr)
        relative_rank = rank / (num_trials + 1)
        oos_ranks.append(relative_rank)

        if relative_rank <= 0.50:
            under_median_count += 1

    pbo = under_median_count / len(combinations) if combinations else 0.50
    avg_is_sr = sum(in_sample_sharpes) / len(in_sample_sharpes) if in_sample_sharpes else 0.0
    avg_oos_sr = sum(out_of_sample_sharpes) / len(out_of_sample_sharpes) if out_of_sample_sharpes else 0.0
    decay_pct = (1.0 - (avg_oos_sr / avg_is_sr)) * 100.0 if avg_is_sr > 0 else 100.0

    # Whole-sample empirical Sharpe distribution across all N noise trials
    full_sharpes = [calc_sharpe(list(range(sample_length_days)), returns_matrix[n]) for n in range(num_trials)]
    full_sharpes.sort()
    max_full_sr = full_sharpes[-1]
    median_full_sr = full_sharpes[len(full_sharpes) // 2]
    mean_full_sr = sum(full_sharpes) / len(full_sharpes)
    var_full_sr = sum((s - mean_full_sr) ** 2 for s in full_sharpes) / (len(full_sharpes) - 1)

    return {
        "pbo": round(pbo, 4),
        "num_combinations": len(combinations),
        "avg_in_sample_sharpe": round(avg_is_sr, 3),
        "avg_out_of_sample_sharpe": round(avg_oos_sr, 3),
        "oos_decay_pct": round(decay_pct, 2),
        "noise_max_sharpe": round(max_full_sr, 3),
        "noise_median_sharpe": round(median_full_sr, 3),
        "noise_sharpe_variance": round(var_full_sr, 4),
    }


class OverfitTrapEngine(TradingLabEngine):
    @property
    def engine_id(self) -> str:
        return "overfit_trap"

    @property
    def name(self) -> str:
        return "Backtest Overfitting Trap & Deflated Sharpe Analyzer"

    @property
    def description(self) -> str:
        return (
            "Evaluates selection bias, Deflated Sharpe Ratio (Bailey-Lopez de Prado), "
            "Harvey-Liu multiple testing haircuts, and CSCV Probability of Backtest Overfitting (PBO)."
        )

    @property
    def asset_class(self) -> str:
        return "Systematic Trading / Quantitative Research"

    @property
    def params(self) -> dict[str, Param]:
        return {
            "observed_sharpe": Param(
                name="observed_sharpe",
                param_type="float",
                default=1.5,
                description="Annualized Sharpe ratio of the selected backtest strategy",
                min_val=0.0,
                max_val=10.0,
            ),
            "sample_length_days": Param(
                name="sample_length_days",
                param_type="int",
                default=1260,
                description="Sample length in trading days (1260 = ~5 years)",
                min_val=100,
                max_val=10000,
            ),
            "num_trials": Param(
                name="num_trials",
                param_type="int",
                default=100,
                description="Total number of backtest parameter variants or signals tested (N)",
                min_val=1,
                max_val=100000,
            ),
            "skewness": Param(
                name="skewness",
                param_type="float",
                default=0.0,
                description="Return skewness (negative values penalize Sharpe for crash risk)",
                min_val=-5.0,
                max_val=5.0,
            ),
            "kurtosis": Param(
                name="kurtosis",
                param_type="float",
                default=3.0,
                description="Return kurtosis (normal = 3.0; fat tails penalize Sharpe)",
                min_val=1.0,
                max_val=30.0,
            ),
            "sharpe_variance": Param(
                name="sharpe_variance",
                param_type="float",
                default=0.0,
                description="Annualized variance of Sharpe estimates across trials (if 0.0, derived analytically)",
                min_val=0.0,
                max_val=5.0,
            ),
            "run_mining_demo": Param(
                name="run_mining_demo",
                param_type="bool",
                default=True,
                description="Run simulated parameter grid mining and CSCV on pure noise",
            ),
            "mining_trials": Param(
                name="mining_trials",
                param_type="int",
                default=100,
                description="Trial count for noise mining simulation",
                min_val=10,
                max_val=500,
            ),
            "cscv_blocks": Param(
                name="cscv_blocks",
                param_type="int",
                default=6,
                description="Number of contiguous temporal blocks for CSCV splits (must be even)",
                choices=[4, 6, 8, 10],
            ),
            "seed": Param(
                name="seed",
                param_type="int",
                default=42,
                description="Random seed for deterministic Monte Carlo simulation",
            ),
        }

    def run(self, **kwargs: Any) -> LabResult:
        p = self.validate_params(kwargs)
        obs_sr: float = p["observed_sharpe"]
        days: int = p["sample_length_days"]
        trials: int = p["num_trials"]
        skew: float = p["skewness"]
        kurt: float = p["kurtosis"]
        var_ann: float = p["sharpe_variance"]
        run_demo: bool = p["run_mining_demo"]
        demo_trials: int = p["mining_trials"]
        blocks: int = p["cscv_blocks"]
        seed: int = p["seed"]

        years = days / 252.0
        if var_ann <= 0.0:
            # Under null hypothesis with iid returns, Var(SR_ann) ~ 1 / years
            var_ann = 1.0 / years if years > 0 else 1.0

        # 1. Deflated Sharpe Ratio (DSR) & Probabilistic Sharpe Ratio (PSR)
        dsr, exp_max_ann, psr_zero = deflated_sharpe_ratio(
            observed_sharpe_ann=obs_sr,
            num_trials=trials,
            sample_length_days=days,
            variance_ann=var_ann,
            skewness=skew,
            kurtosis=kurt,
        )

        # 2. Harvey-Liu Haircuts
        hlz = harvey_liu_haircuts(sharpe_ann=obs_sr, sample_length_days=days, num_trials=trials)

        # 3. Minimum Backtest Length (MinBTL)
        min_btl = min_backtest_length_years(num_trials=trials, target_sharpe_ann=obs_sr)
        min_btl_defined = math.isfinite(min_btl)

        # 4. CSCV and Noise Mining Simulation
        cscv_result: dict[str, Any] = {}
        if run_demo:
            cscv_result = run_cscv_and_mining_simulation(
                num_trials=demo_trials,
                sample_length_days=days,
                num_blocks=blocks,
                seed=seed,
            )

        metrics: dict[str, float | int | str] = {
            "observed_sharpe_ann": round(obs_sr, 3),
            "expected_max_null_sharpe": round(exp_max_ann, 3),
            "deflated_sharpe_ratio": round(dsr, 4),
            "probabilistic_sharpe_ratio": round(psr_zero, 4),
            "passes_dsr_95_confidence": "PASS" if dsr >= 0.95 else "FAIL",
            "harvey_liu_t_stat": hlz["t_stat"],
            "harvey_liu_t_bonferroni": hlz["t_bonferroni"],
            "harvey_liu_sharpe_bonferroni": hlz["sharpe_bonferroni"],
            "harvey_liu_haircut_pct": hlz["haircut_bonferroni_pct"],
            "passes_hlz_t3_threshold": "PASS" if hlz["passes_hlz_threshold"] == 1.0 else "FAIL",
            "min_backtest_length_years": round(min_btl, 2) if min_btl_defined else "UNDEFINED",
            "sample_length_years": round(years, 2),
            "sufficient_sample_length": "PASS" if min_btl_defined and years >= min_btl else "FAIL",
        }

        if cscv_result:
            metrics["pbo_cscv"] = cscv_result["pbo"]
            metrics["noise_mining_best_sharpe"] = cscv_result["noise_max_sharpe"]
            metrics["noise_oos_decay_pct"] = cscv_result["oos_decay_pct"]
            metrics["pbo_overfitting_verdict"] = "SEVERE_OVERFITTING" if cscv_result["pbo"] >= 0.50 else "ACCEPTABLE_GENERALIZATION"

        summary = (
            f"Overfit Trap Analysis for {trials} trials over {years:.1f} years (SR={obs_sr:.2f}): "
            f"Expected max null Sharpe is {exp_max_ann:.2f}. "
            f"Deflated Sharpe Ratio (DSR) is {dsr:.1%} ({metrics['passes_dsr_95_confidence']}). "
            f"Harvey-Liu Bonferroni haircut is {hlz['haircut_bonferroni_pct']:.1f}% "
            f"(Adjusted SR: {hlz['sharpe_bonferroni']:.2f}, adjusted t={hlz['t_bonferroni']:.2f}). "
            f"Raw t={hlz['t_stat']:.2f} vs HLZ hurdle t>{HLZ_T_HURDLE:.1f}: {metrics['passes_hlz_t3_threshold']}. "
            + (
                f"Min Backtest Length needed: {min_btl:.1f} years."
                if min_btl_defined
                else "Min Backtest Length is undefined: a non-positive Sharpe cannot clear selection bias at any length."
            )
        )

        data = {
            "deflated_sharpe_details": {
                "observed_sharpe_ann": obs_sr,
                "expected_max_null_sharpe_ann": exp_max_ann,
                "deflated_sharpe_ratio": dsr,
                "probabilistic_sharpe_ratio": psr_zero,
                "skewness": skew,
                "kurtosis": kurt,
                "sharpe_variance_ann": var_ann,
            },
            "harvey_liu_details": hlz,
            "min_backtest_length": {
                "min_years_required": min_btl if min_btl_defined else None,
                "actual_years": years,
                "gap_years": round(min_btl - years, 2) if min_btl_defined else None,
            },
            "cscv_simulation": cscv_result,
        }

        return LabResult(
            engine_id=self.engine_id,
            metrics=metrics,
            data=data,
            summary=summary,
        )


# Register engine into Trading Lab catalog
register(OverfitTrapEngine())
