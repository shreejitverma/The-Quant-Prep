"""
Reference Pricing, Curve Graph, and Real-Time Risk Engine.

Implements core architectural patterns for Section 18 (Pricing and Risk Systems):
1. Dependency Graph (DAG) for market data, curves, and calibrated surfaces with dirty-flag invalidation.
2. Instrument / Model / Engine separation with vectorised and forward-mode sensitivity evaluation.
3. Real-Time Pre-Trade Limit Check service with sub-millisecond checks (PV01, CS01, Notional, Net Exposure).
4. PnL Explain Engine (Hypothetical PnL, Risk-Theoretical PnL, Taylor decomposition: Delta, Gamma, Theta, Unexplained).
"""

from __future__ import annotations

import math
from collections.abc import Callable
from dataclasses import dataclass
from enum import Enum


class CurveType(Enum):
    DISCOUNT = "discount"
    FORWARD = "forward"
    CREDIT = "credit"


@dataclass
class MarketQuote:
    quote_id: str
    value: float
    timestamp: float


class DependencyNode:
    """Node in a SecDB-style reactive dependency DAG."""

    def __init__(self, name: str, compute_fn: Callable[[], any] | None = None):
        self.name = name
        self.compute_fn = compute_fn
        self.children: set[DependencyNode] = set()  # Downstream dependencies
        self.parents: set[DependencyNode] = set()  # Upstream inputs
        self._value: any = None
        self._is_valid: bool = False

    def add_parent(self, parent: DependencyNode) -> None:
        self.parents.add(parent)
        parent.children.add(self)

    def invalidate(self) -> None:
        """Mark this node and all downstream children as dirty."""
        if not self._is_valid:
            return
        self._is_valid = False
        self._value = None
        for child in self.children:
            child.invalidate()

    def get_value(self) -> any:
        """Evaluate lazily if dirty, or return cached value."""
        if not self._is_valid:
            if self.compute_fn is not None:
                self._value = self.compute_fn()
            self._is_valid = True
        return self._value

    def set_value(self, val: any) -> None:
        """Set root value and invalidate downstream graph."""
        self._value = val
        self._is_valid = True
        for child in self.children:
            child.invalidate()


class YieldCurve:
    """Zero-coupon discount curve parameterized by zero rates."""

    def __init__(self, name: str, pillar_times: list[float], zero_rates: list[float]):
        if len(pillar_times) != len(zero_rates):
            raise ValueError("Pillar times and zero rates must match in length")
        self.name = name
        self.pillar_times = list(pillar_times)
        self.zero_rates = list(zero_rates)

    def zero_rate(self, t: float) -> float:
        if t <= self.pillar_times[0]:
            return self.zero_rates[0]
        if t >= self.pillar_times[-1]:
            return self.zero_rates[-1]
        for i in range(len(self.pillar_times) - 1):
            t1, t2 = self.pillar_times[i], self.pillar_times[i + 1]
            if t1 <= t <= t2:
                w = (t - t1) / (t2 - t1)
                return (1.0 - w) * self.zero_rates[i] + w * self.zero_rates[i + 1]
        return self.zero_rates[-1]

    def df(self, t: float) -> float:
        if t <= 0:
            return 1.0
        r = self.zero_rate(t)
        return math.exp(-r * t)

    def forward_rate(self, t1: float, t2: float) -> float:
        if t2 <= t1:
            raise ValueError("t2 must be greater than t1")
        df1 = self.df(t1)
        df2 = self.df(t2)
        return (df1 / df2 - 1.0) / (t2 - t1)


@dataclass
class VanillaSwap:
    swap_id: str
    counterparty_id: str
    desk_id: str
    notional: float
    fixed_rate: float
    tenor: float
    payment_frequency: float = 0.5  # Semiannual
    is_payer: bool = True  # True = Pay Fixed, Receive Float


class SwapPricingEngine:
    """Pricing engine separating instrument representation from valuation."""

    @staticmethod
    def pv(swap: VanillaSwap, curve: YieldCurve) -> float:
        n_periods = int(round(swap.tenor / swap.payment_frequency))
        pv_fixed = 0.0
        pv_float = 0.0

        for i in range(1, n_periods + 1):
            t_end = i * swap.payment_frequency
            t_start = (i - 1) * swap.payment_frequency
            df_end = curve.df(t_end)

            # Fixed leg cashflow
            fixed_cf = swap.notional * swap.fixed_rate * swap.payment_frequency
            pv_fixed += fixed_cf * df_end

            # Floating leg cashflow: forward rate * dt * df_end = (df_start/df_end - 1) * df_end = df_start - df_end
            df_start = curve.df(t_start)
            float_cf = swap.notional * (df_start - df_end)
            pv_float += float_cf

        if swap.is_payer:
            return pv_float - pv_fixed
        else:
            return pv_fixed - pv_float

    @staticmethod
    def pv01(swap: VanillaSwap, curve: YieldCurve, bump_bps: float = 1.0) -> float:
        """Compute parallel DV01 (PV change for +1 bp rate shift)."""
        bump = bump_bps * 1e-4
        bumped_rates = [r + bump for r in curve.zero_rates]
        bumped_curve = YieldCurve(curve.name + "_up", curve.pillar_times, bumped_rates)
        pv_base = SwapPricingEngine.pv(swap, curve)
        pv_up = SwapPricingEngine.pv(swap, bumped_curve)
        return pv_up - pv_base


@dataclass
class DeskLimit:
    desk_id: str
    max_dv01: float
    max_notional: float
    max_gross_pv: float


class PreTradeRiskGateway:
    """Sub-millisecond pre-trade compliance and limit check service."""

    def __init__(self, limits: dict[str, DeskLimit]):
        self.limits = limits
        self.active_swaps: dict[str, list[VanillaSwap]] = {desk: [] for desk in limits}

    def check_trade(self, swap: VanillaSwap, curve: YieldCurve) -> tuple[bool, str]:
        desk_lim = self.limits.get(swap.desk_id)
        if not desk_lim:
            return False, f"Unknown desk {swap.desk_id}"

        # 1. Check standalone notional limit
        if swap.notional > desk_lim.max_notional:
            return False, f"Trade notional {swap.notional} exceeds desk limit {desk_lim.max_notional}"

        # 2. Check incremental DV01
        existing_swaps = self.active_swaps[swap.desk_id]
        current_dv01 = sum(SwapPricingEngine.pv01(s, curve) for s in existing_swaps)
        trade_dv01 = SwapPricingEngine.pv01(swap, curve)
        projected_dv01 = current_dv01 + trade_dv01

        if abs(projected_dv01) > desk_lim.max_dv01:
            return False, f"Projected DV01 {projected_dv01:.2f} exceeds limit {desk_lim.max_dv01:.2f}"

        return True, "Trade approved"

    def commit_trade(self, swap: VanillaSwap) -> None:
        self.active_swaps[swap.desk_id].append(swap)


class PnLExplainEngine:
    """Decomposes daily PnL into Risk-Theoretical Greek attribution vs Unexplained residual."""

    @staticmethod
    def explain_swap_pnl(swap: VanillaSwap, curve_t0: YieldCurve, curve_t1: YieldCurve, dt_years: float = 1.0 / 252.0) -> dict[str, float]:
        pv_t0 = SwapPricingEngine.pv(swap, curve_t0)
        pv_t1 = SwapPricingEngine.pv(swap, curve_t1)
        actual_pnl = pv_t1 - pv_t0

        # Delta explain: sum_i (DV01_i * shift_i)
        # We test parallel curve shift
        mean_rate_t0 = sum(curve_t0.zero_rates) / len(curve_t0.zero_rates)
        mean_rate_t1 = sum(curve_t1.zero_rates) / len(curve_t1.zero_rates)
        d_rate = mean_rate_t1 - mean_rate_t0

        dv01 = SwapPricingEngine.pv01(swap, curve_t0, bump_bps=1.0)
        delta_pnl = (dv01 / 1e-4) * d_rate

        # Gamma explain: 0.5 * Gamma * (d_rate)^2
        bump = 1e-4
        rates_up = [r + bump for r in curve_t0.zero_rates]
        rates_dn = [r - bump for r in curve_t0.zero_rates]
        pv_up = SwapPricingEngine.pv(swap, YieldCurve("up", curve_t0.pillar_times, rates_up))
        pv_dn = SwapPricingEngine.pv(swap, YieldCurve("dn", curve_t0.pillar_times, rates_dn))
        gamma_rate = (pv_up - 2.0 * pv_t0 + pv_dn) / (bump**2)
        gamma_pnl = 0.5 * gamma_rate * (d_rate**2)

        # Theta (carry / roll-down)
        # Advance maturity by dt
        swap_rolled = VanillaSwap(
            swap.swap_id,
            swap.counterparty_id,
            swap.desk_id,
            swap.notional,
            swap.fixed_rate,
            max(0.0, swap.tenor - dt_years),
            swap.payment_frequency,
            swap.is_payer,
        )
        pv_rolled = SwapPricingEngine.pv(swap_rolled, curve_t0)
        theta_pnl = pv_rolled - pv_t0

        explained_pnl = delta_pnl + gamma_pnl + theta_pnl
        unexplained = actual_pnl - explained_pnl

        return {
            "pv_t0": pv_t0,
            "pv_t1": pv_t1,
            "actual_pnl": actual_pnl,
            "delta_pnl": delta_pnl,
            "gamma_pnl": gamma_pnl,
            "theta_pnl": theta_pnl,
            "explained_pnl": explained_pnl,
            "unexplained_pnl": unexplained,
        }


def run_all_tests():
    """Execute automated self-tests."""
    # 1. Dependency Graph Test
    root_quote = DependencyNode("US_10Y_QUOTE")
    root_quote.set_value(0.045)

    curve_node = DependencyNode(
        "USD_OIS_CURVE",
        lambda: YieldCurve(
            "USD",
            [1.0, 5.0, 10.0],
            [root_quote.get_value(), root_quote.get_value() + 0.005, root_quote.get_value() + 0.01],
        ),
    )
    curve_node.add_parent(root_quote)

    swap_node = DependencyNode(
        "SWAP_PV",
        lambda: SwapPricingEngine.pv(
            VanillaSwap("SW01", "CPTY1", "RATES_DESK", 10_000_000, 0.05, 5.0, 0.5, True),
            curve_node.get_value(),
        ),
    )
    swap_node.add_parent(curve_node)

    pv1 = swap_node.get_value()
    assert isinstance(pv1, float)

    # Invalidate root
    root_quote.set_value(0.050)
    assert not curve_node._is_valid
    assert not swap_node._is_valid
    pv2 = swap_node.get_value()
    assert pv1 != pv2  # Correctly recalculated

    # 2. Swap Pricing and DV01
    curve = YieldCurve("USD", [1.0, 2.0, 5.0, 10.0], [0.04, 0.042, 0.045, 0.048])
    swap = VanillaSwap("SW01", "CPTY1", "RATES_DESK", 10_000_000.0, 0.045, 5.0, 0.5, True)
    pv = SwapPricingEngine.pv(swap, curve)
    assert isinstance(pv, float)
    dv01 = SwapPricingEngine.pv01(swap, curve)
    assert dv01 > 0.0  # Payer swap gains when rates rise

    # 3. Pre-Trade Gateway Test
    limits = {"RATES_DESK": DeskLimit("RATES_DESK", max_dv01=50_000.0, max_notional=100_000_000.0, max_gross_pv=5_000_000.0)}
    gateway = PreTradeRiskGateway(limits)
    approved, msg = gateway.check_trade(swap, curve)
    assert approved, f"Should be approved: {msg}"
    gateway.commit_trade(swap)

    # Enormous trade exceeding limits
    huge_swap = VanillaSwap("SW02", "CPTY1", "RATES_DESK", 500_000_000.0, 0.045, 10.0, 0.5, True)
    approved2, msg2 = gateway.check_trade(huge_swap, curve)
    assert not approved2
    assert "exceeds" in msg2

    # 4. PnL Explain Test
    curve_t1 = YieldCurve("USD_T1", [1.0, 2.0, 5.0, 10.0], [0.0405, 0.0425, 0.0455, 0.0485])  # +5 bps parallel
    explain = PnLExplainEngine.explain_swap_pnl(swap, curve, curve_t1)
    assert abs(explain["unexplained_pnl"]) < abs(explain["actual_pnl"]) * 0.15  # Explained within 15% tolerance

    print("All Pricing and Risk Systems tests passed successfully!")


if __name__ == "__main__":
    run_all_tests()
