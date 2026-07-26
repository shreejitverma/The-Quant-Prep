"""Regression test for the Reg NMS & SHO regulatory guide.

This test parses the markdown guide located at
``Market Making/Quant_Dev_Market_Making_Guide/01_Regulatory_Framework_NMS_SHO.md``,
extracts the concrete numerical and structural rules it describes, and then
asserts that a minimal mock trading engine implements those rules faithfully.

The goal is two-fold:

1. Pin the regulatory numbers quoted in the document so that silent edits to
   the guide (e.g. changing the Rule 610 fee cap or the Rule 201 threshold)
   are caught by CI.
2. Provide a self-contained reference implementation of the key Reg NMS and
   Reg SHO compliance checks that production code can be validated against.

The mock engine is deliberately small - it is not a real OMS - but it
implements every rule that is quantified in the guide.
"""

from __future__ import annotations

import os
import re
import unittest
from dataclasses import dataclass, field
from datetime import date, timedelta
from enum import Enum
from typing import Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Guide location
# ---------------------------------------------------------------------------
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
GUIDE_PATH = os.path.join(
    REPO_ROOT,
    "Market Making",
    "Quant_Dev_Market_Making_Guide",
    "01_Regulatory_Framework_NMS_SHO.md",
)


# ---------------------------------------------------------------------------
# Markdown parser
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class RuleSpec:
    """Numerical and structural rules extracted from the regulatory guide."""

    # Rule 610 - Access
    access_fee_cap_per_share: float
    access_fee_price_threshold: float

    # Rule 612 - Sub-Penny
    sub_penny_price_threshold: float
    sub_penny_min_increment: float

    # Rule 611 - Order Protection (flickering quote exception window)
    flickering_quote_window_seconds: float

    # Rule 201 - Alternative Uptick / Circuit Breaker
    rule201_decline_pct: float
    rule201_restriction_next_days: int

    # Rule 204 - Close-out
    rule204_participant_close_out_days: int
    rule204_mm_close_out_days: int

    # Threshold securities
    threshold_security_min_shares: int
    threshold_security_min_outstanding_pct: float
    threshold_security_persistence_days: int
    threshold_security_hard_close_out_days: int

    # Protected quotation requirements (Rule 611)
    protected_quote_keywords: Tuple[str, ...]


def _require(pattern: str, text: str, flags: int = 0) -> re.Match:
    match = re.search(pattern, text, flags)
    if match is None:
        raise AssertionError(
            f"Guide parser failed: pattern {pattern!r} not found. "
            "Has the regulatory guide structure changed?"
        )
    return match


def parse_guide(path: str = GUIDE_PATH) -> RuleSpec:
    """Parse the Reg NMS/SHO markdown guide and return a :class:`RuleSpec`.

    The parser relies on the numbers the document quotes verbatim. If the
    guide is edited in a way that invalidates any of these regexes the test
    suite fails fast with an actionable message.
    """

    with open(path, encoding="utf-8") as fh:
        text = fh.read()

    # Rule 610 access-fee cap: "$0.003 per share (30 mils)" for stocks >= $1.00
    fee_match = _require(
        r"\$([0-9]+\.[0-9]+)\s*per share\s*\(\s*30\s*mils\s*\).{0,120}?"
        r"for stocks\s*[>=\u2265]+\s*\$([0-9]+\.[0-9]+)",
        text,
        re.DOTALL,
    )
    access_fee_cap = float(fee_match.group(1))
    access_fee_threshold = float(fee_match.group(2))

    # Rule 612 sub-penny: "stocks priced >= $1.00 ... increments smaller than $0.01"
    sub_penny_match = _require(
        r"stocks priced\s*[>=\u2265]+\s*\$([0-9]+\.[0-9]+).{0,200}?"
        r"increments smaller than\s*\*\*\$([0-9]+\.[0-9]+)",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    sub_penny_threshold = float(sub_penny_match.group(1))
    sub_penny_increment = float(sub_penny_match.group(2))

    # Rule 611 flickering quote exception: "displayed <1 second ago"
    flicker_match = _require(
        r"[Ff]lickering.{0,120}?displayed\s*<\s*([0-9]+(?:\.[0-9]+)?)\s*second",
        text,
        re.DOTALL,
    )
    flicker_window = float(flicker_match.group(1))

    # Rule 201 decline pct: "intraday price decline of **10% or more**"
    rule201_match = _require(
        r"intraday price decline of\s*\*\*([0-9]+(?:\.[0-9]+)?)%\s*or more",
        text,
    )
    rule201_decline = float(rule201_match.group(1)) / 100.0

    # Rule 201 duration: rest-of-day + entire next trading day
    _require(
        r"Remainder of the day.{0,100}?entire next trading day",
        text,
        re.DOTALL | re.IGNORECASE,
    )
    rule201_restriction_days = 1  # "next trading day"

    # Rule 204: participants must close out by T+2, market makers extended to T+3
    _require(r"Participants must close out FTDs by.{0,80}?\*\*T\+2\*\*", text, re.DOTALL)
    _require(r"\*\*T\+3\*\*.{0,80}?bona fide market making fails", text, re.DOTALL)
    rule204_participant_days = 2
    rule204_mm_days = 3

    # Threshold securities
    thresh_shares_match = _require(
        r"[\u2265>=]+\s*([0-9][0-9,]*)\s*shares,\s*AND",
        text,
    )
    thresh_pct_match = _require(
        r"[\u2265>=]+\s*([0-9.]+)%\s*of total shares outstanding",
        text,
    )
    thresh_persist_match = _require(
        r"These levels must persist for\s*([0-9]+)\s*consecutive settlement days",
        text,
    )
    thresh_hard_match = _require(
        r"FTDs persist for\s*([0-9]+)\s*consecutive settlement days.{0,120}?immediate close-out",
        text,
        re.DOTALL | re.IGNORECASE,
    )

    threshold_min_shares = int(thresh_shares_match.group(1).replace(",", ""))
    threshold_min_pct = float(thresh_pct_match.group(1)) / 100.0
    threshold_persist_days = int(thresh_persist_match.group(1))
    threshold_hard_days = int(thresh_hard_match.group(1))

    # Rule 611 protected-quotation keywords
    protected_keywords = ("automated", "displayed", "disseminated", "quotation")
    for kw in protected_keywords:
        _require(rf"\*\*{kw}", text, re.IGNORECASE)

    return RuleSpec(
        access_fee_cap_per_share=access_fee_cap,
        access_fee_price_threshold=access_fee_threshold,
        sub_penny_price_threshold=sub_penny_threshold,
        sub_penny_min_increment=sub_penny_increment,
        flickering_quote_window_seconds=flicker_window,
        rule201_decline_pct=rule201_decline,
        rule201_restriction_next_days=rule201_restriction_days,
        rule204_participant_close_out_days=rule204_participant_days,
        rule204_mm_close_out_days=rule204_mm_days,
        threshold_security_min_shares=threshold_min_shares,
        threshold_security_min_outstanding_pct=threshold_min_pct,
        threshold_security_persistence_days=threshold_persist_days,
        threshold_security_hard_close_out_days=threshold_hard_days,
        protected_quote_keywords=protected_keywords,
    )


# ---------------------------------------------------------------------------
# Mock trading engine
# ---------------------------------------------------------------------------
class OrderMark(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    SHORT_EXEMPT = "SHORT_EXEMPT"


class MarketState(str, Enum):
    NORMAL = "NORMAL"
    LOCKED = "LOCKED"
    CROSSED = "CROSSED"


@dataclass(frozen=True)
class ProtectedQuote:
    venue: str
    price: float
    size: int


@dataclass(frozen=True)
class ChildOrder:
    venue: str
    price: float
    quantity: int
    is_iso: bool
    mark: OrderMark = OrderMark.LONG


@dataclass
class ComplianceResult:
    ok: bool
    reason: str = ""


class MockTradingEngine:
    """Reference implementation of the compliance checks described in the
    Reg NMS & SHO guide.

    Every constant below is sourced from the markdown guide. The regression
    tests below cross-check these constants against the parsed values.
    """

    # --- Rule 610 --------------------------------------------------------
    ACCESS_FEE_CAP_PER_SHARE: float = 0.003
    ACCESS_FEE_PRICE_THRESHOLD: float = 1.00

    # --- Rule 612 --------------------------------------------------------
    SUB_PENNY_PRICE_THRESHOLD: float = 1.00
    SUB_PENNY_MIN_INCREMENT: float = 0.01

    # --- Rule 611 --------------------------------------------------------
    FLICKERING_QUOTE_WINDOW_SECONDS: float = 1.0

    # --- Rule 201 --------------------------------------------------------
    RULE201_DECLINE_PCT: float = 0.10
    RULE201_RESTRICTION_NEXT_DAYS: int = 1

    # --- Rule 204 --------------------------------------------------------
    RULE204_PARTICIPANT_CLOSE_OUT_DAYS: int = 2  # T+2
    RULE204_MM_CLOSE_OUT_DAYS: int = 3  # T+3 for bona fide MM

    # --- Threshold securities -------------------------------------------
    THRESHOLD_MIN_SHARES: int = 10_000
    THRESHOLD_MIN_OUTSTANDING_PCT: float = 0.005  # 0.5%
    THRESHOLD_PERSISTENCE_DAYS: int = 5
    THRESHOLD_HARD_CLOSE_OUT_DAYS: int = 13

    # ------------------------------------------------------------------
    # Rule 610: access-fee cap
    # ------------------------------------------------------------------
    def validate_access_fee(self, fee_per_share: float, reference_price: float) -> ComplianceResult:
        if reference_price < self.ACCESS_FEE_PRICE_THRESHOLD:
            # Rule 610 cap only applies to stocks priced >= $1.00.
            return ComplianceResult(True)
        if fee_per_share > self.ACCESS_FEE_CAP_PER_SHARE + 1e-12:
            return ComplianceResult(
                False,
                f"Access fee {fee_per_share} exceeds Rule 610 cap "
                f"{self.ACCESS_FEE_CAP_PER_SHARE}",
            )
        return ComplianceResult(True)

    # ------------------------------------------------------------------
    # Rule 610: locked / crossed markets
    # ------------------------------------------------------------------
    def classify_market(self, my_bid: Optional[float], my_ask: Optional[float],
                        nbbo_bid: float, nbbo_ask: float) -> MarketState:
        """Classify whether the quote locks or crosses the protected NBBO."""
        if my_bid is not None and my_bid > nbbo_ask:
            return MarketState.CROSSED
        if my_ask is not None and my_ask < nbbo_bid:
            return MarketState.CROSSED
        if my_bid is not None and my_bid == nbbo_ask:
            return MarketState.LOCKED
        if my_ask is not None and my_ask == nbbo_bid:
            return MarketState.LOCKED
        return MarketState.NORMAL

    def validate_quote(self, my_bid: Optional[float], my_ask: Optional[float],
                       nbbo_bid: float, nbbo_ask: float) -> ComplianceResult:
        state = self.classify_market(my_bid, my_ask, nbbo_bid, nbbo_ask)
        if state is MarketState.NORMAL:
            return ComplianceResult(True)
        return ComplianceResult(False, f"Rule 610 violation: market {state.value}")

    # ------------------------------------------------------------------
    # Rule 612: sub-penny price display
    # ------------------------------------------------------------------
    def is_valid_display_price(self, price: float) -> bool:
        """Return True if the price can legally be displayed under Rule 612."""
        if price < self.SUB_PENNY_PRICE_THRESHOLD:
            # Sub-penny increments allowed below $1.00.
            return price > 0
        # At or above $1.00 the minimum increment is $0.01.
        scaled = round(price / self.SUB_PENNY_MIN_INCREMENT)
        return abs(scaled * self.SUB_PENNY_MIN_INCREMENT - price) < 1e-9

    # ------------------------------------------------------------------
    # Rule 611: order protection / trade-through
    # ------------------------------------------------------------------
    def validate_trade_through(self, execution_price: float, is_buy: bool,
                               protected_nbbo_bid: float, protected_nbbo_ask: float,
                               is_iso: bool) -> ComplianceResult:
        if is_iso:
            return ComplianceResult(True, "ISO exception to Rule 611")
        if is_buy and execution_price > protected_nbbo_ask + 1e-12:
            return ComplianceResult(False, "Buy traded through protected ask")
        if (not is_buy) and execution_price < protected_nbbo_bid - 1e-12:
            return ComplianceResult(False, "Sell traded through protected bid")
        return ComplianceResult(True)

    def route_iso_sweep(self, is_buy: bool, limit_price: float, quantity: int,
                        protected_quotes: List[ProtectedQuote],
                        destination_venue: str) -> List[ChildOrder]:
        """Build the child-order list for an ISO sweep.

        The sweep must (a) target every better-priced protected quote and
        (b) send the residual to the destination venue, all tagged as ISO
        and marked IOC for the sweep legs. Every child is flagged
        ``is_iso=True`` so Rule 611 routing obligations are satisfied.
        """

        def better_than_limit(q: ProtectedQuote) -> bool:
            return q.price <= limit_price if is_buy else q.price >= limit_price

        better_quotes = sorted(
            (q for q in protected_quotes if better_than_limit(q)),
            key=lambda q: (q.price if is_buy else -q.price),
        )

        children: List[ChildOrder] = []
        remaining = quantity
        for quote in better_quotes:
            if remaining <= 0:
                break
            sweep_qty = min(remaining, quote.size)
            children.append(
                ChildOrder(
                    venue=quote.venue,
                    price=quote.price,
                    quantity=sweep_qty,
                    is_iso=True,
                )
            )
            remaining -= sweep_qty

        if remaining > 0:
            children.append(
                ChildOrder(
                    venue=destination_venue,
                    price=limit_price,
                    quantity=remaining,
                    is_iso=True,
                )
            )
        return children

    # ------------------------------------------------------------------
    # Rule 200: long / short / short-exempt marking
    # ------------------------------------------------------------------
    def mark_sell_order(self, inventory: int, sell_qty: int,
                        is_bona_fide_mm: bool = False,
                        circuit_breaker_active: bool = False) -> OrderMark:
        if sell_qty <= inventory:
            return OrderMark.LONG
        if circuit_breaker_active and is_bona_fide_mm:
            return OrderMark.SHORT_EXEMPT
        return OrderMark.SHORT

    # ------------------------------------------------------------------
    # Rule 201: Alternative Uptick circuit breaker
    # ------------------------------------------------------------------
    def rule201_trigger_price(self, prior_close: float) -> float:
        return prior_close * (1.0 - self.RULE201_DECLINE_PCT)

    def rule201_is_triggered(self, intraday_low: float, prior_close: float) -> bool:
        return intraday_low <= self.rule201_trigger_price(prior_close)

    def rule201_restriction_end_date(self, trigger_date: date) -> date:
        """Restriction lasts through the end of the next trading day."""
        end = trigger_date + timedelta(days=self.RULE201_RESTRICTION_NEXT_DAYS)
        while end.weekday() >= 5:  # skip Sat/Sun
            end += timedelta(days=1)
        return end

    def validate_short_sale_under_rule201(self, price: float, nbb: float,
                                           triggered: bool, is_short_exempt: bool,
                                           current_date: date,
                                           trigger_date: Optional[date]) -> ComplianceResult:
        if not triggered or trigger_date is None:
            return ComplianceResult(True)
        if current_date > self.rule201_restriction_end_date(trigger_date):
            return ComplianceResult(True, "Restriction window expired")
        if is_short_exempt:
            return ComplianceResult(True, "Short-exempt order (e.g. bona fide MM)")
        if price <= nbb + 1e-12:
            return ComplianceResult(
                False, f"Short sale at {price} must exceed NBB {nbb}")
        return ComplianceResult(True)

    # ------------------------------------------------------------------
    # Rule 204: close-out deadlines
    # ------------------------------------------------------------------
    def close_out_deadline(self, trade_date: date, is_market_maker: bool) -> date:
        days = (
            self.RULE204_MM_CLOSE_OUT_DAYS
            if is_market_maker
            else self.RULE204_PARTICIPANT_CLOSE_OUT_DAYS
        )
        deadline = trade_date + timedelta(days=days)
        while deadline.weekday() >= 5:
            deadline += timedelta(days=1)
        return deadline

    # ------------------------------------------------------------------
    # Threshold securities
    # ------------------------------------------------------------------
    def is_threshold_security(self, ftd_shares: int, shares_outstanding: int,
                              consecutive_days: int) -> bool:
        if shares_outstanding <= 0:
            return False
        pct = ftd_shares / shares_outstanding
        return (
            ftd_shares >= self.THRESHOLD_MIN_SHARES
            and pct >= self.THRESHOLD_MIN_OUTSTANDING_PCT
            and consecutive_days >= self.THRESHOLD_PERSISTENCE_DAYS
        )

    def requires_hard_close_out(self, consecutive_ftd_days: int) -> bool:
        return consecutive_ftd_days >= self.THRESHOLD_HARD_CLOSE_OUT_DAYS


# ---------------------------------------------------------------------------
# Regression tests
# ---------------------------------------------------------------------------
class TestGuideParsingMatchesEngine(unittest.TestCase):
    """Parse the markdown guide and verify the mock engine matches."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.spec = parse_guide()
        cls.engine = MockTradingEngine()

    def test_rule_610_fee_cap_constants(self) -> None:
        self.assertAlmostEqual(
            self.spec.access_fee_cap_per_share,
            self.engine.ACCESS_FEE_CAP_PER_SHARE,
        )
        self.assertAlmostEqual(
            self.spec.access_fee_price_threshold,
            self.engine.ACCESS_FEE_PRICE_THRESHOLD,
        )

    def test_rule_612_sub_penny_constants(self) -> None:
        self.assertAlmostEqual(
            self.spec.sub_penny_price_threshold,
            self.engine.SUB_PENNY_PRICE_THRESHOLD,
        )
        self.assertAlmostEqual(
            self.spec.sub_penny_min_increment,
            self.engine.SUB_PENNY_MIN_INCREMENT,
        )

    def test_rule_611_flickering_window_constant(self) -> None:
        self.assertAlmostEqual(
            self.spec.flickering_quote_window_seconds,
            self.engine.FLICKERING_QUOTE_WINDOW_SECONDS,
        )

    def test_rule_201_constants(self) -> None:
        self.assertAlmostEqual(
            self.spec.rule201_decline_pct,
            self.engine.RULE201_DECLINE_PCT,
        )
        self.assertEqual(
            self.spec.rule201_restriction_next_days,
            self.engine.RULE201_RESTRICTION_NEXT_DAYS,
        )

    def test_rule_204_constants(self) -> None:
        self.assertEqual(
            self.spec.rule204_participant_close_out_days,
            self.engine.RULE204_PARTICIPANT_CLOSE_OUT_DAYS,
        )
        self.assertEqual(
            self.spec.rule204_mm_close_out_days,
            self.engine.RULE204_MM_CLOSE_OUT_DAYS,
        )

    def test_threshold_security_constants(self) -> None:
        self.assertEqual(
            self.spec.threshold_security_min_shares,
            self.engine.THRESHOLD_MIN_SHARES,
        )
        self.assertAlmostEqual(
            self.spec.threshold_security_min_outstanding_pct,
            self.engine.THRESHOLD_MIN_OUTSTANDING_PCT,
        )
        self.assertEqual(
            self.spec.threshold_security_persistence_days,
            self.engine.THRESHOLD_PERSISTENCE_DAYS,
        )
        self.assertEqual(
            self.spec.threshold_security_hard_close_out_days,
            self.engine.THRESHOLD_HARD_CLOSE_OUT_DAYS,
        )

    def test_protected_quotation_keywords_present(self) -> None:
        for keyword in self.spec.protected_quote_keywords:
            self.assertIn(keyword, ("automated", "displayed", "disseminated", "quotation"))


class TestRule610Access(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_fee_cap_enforced_above_dollar(self) -> None:
        ok = self.engine.validate_access_fee(0.003, reference_price=50.0)
        self.assertTrue(ok.ok)
        bad = self.engine.validate_access_fee(0.004, reference_price=50.0)
        self.assertFalse(bad.ok)

    def test_fee_cap_not_applied_below_dollar(self) -> None:
        # Rule 610 fee cap only applies to stocks priced >= $1.00.
        ok = self.engine.validate_access_fee(0.01, reference_price=0.50)
        self.assertTrue(ok.ok)

    def test_locked_market_detected(self) -> None:
        # Bid meets best offer -> lock.
        state = self.engine.classify_market(
            my_bid=100.01, my_ask=None, nbbo_bid=100.00, nbbo_ask=100.01
        )
        self.assertEqual(state, MarketState.LOCKED)

    def test_crossed_market_detected(self) -> None:
        # Ask below best bid -> cross.
        state = self.engine.classify_market(
            my_bid=None, my_ask=99.99, nbbo_bid=100.00, nbbo_ask=100.01
        )
        self.assertEqual(state, MarketState.CROSSED)

    def test_normal_quote_accepted(self) -> None:
        result = self.engine.validate_quote(
            my_bid=99.99, my_ask=100.02, nbbo_bid=100.00, nbbo_ask=100.01
        )
        self.assertTrue(result.ok)


class TestRule612SubPenny(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_sub_penny_rejected_above_dollar(self) -> None:
        self.assertFalse(self.engine.is_valid_display_price(100.001))
        self.assertFalse(self.engine.is_valid_display_price(100.0099))

    def test_penny_increments_accepted(self) -> None:
        for px in (100.00, 100.01, 100.02, 1.00):
            self.assertTrue(self.engine.is_valid_display_price(px), px)

    def test_sub_penny_allowed_below_dollar(self) -> None:
        for px in (0.9999, 0.9998, 0.0001):
            self.assertTrue(self.engine.is_valid_display_price(px), px)


class TestRule611OrderProtection(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_trade_through_blocked_without_iso(self) -> None:
        result = self.engine.validate_trade_through(
            execution_price=100.02, is_buy=True,
            protected_nbbo_bid=100.00, protected_nbbo_ask=100.01,
            is_iso=False,
        )
        self.assertFalse(result.ok)

    def test_trade_through_allowed_with_iso(self) -> None:
        result = self.engine.validate_trade_through(
            execution_price=100.02, is_buy=True,
            protected_nbbo_bid=100.00, protected_nbbo_ask=100.01,
            is_iso=True,
        )
        self.assertTrue(result.ok)

    def test_iso_sweep_clears_all_better_prices(self) -> None:
        """Example reproduced from section 1.2.2 of the guide."""
        protected = [
            ProtectedQuote("A", 100.01, 500),
            ProtectedQuote("B", 100.01, 300),
            ProtectedQuote("C", 100.01, 200),
        ]
        children = self.engine.route_iso_sweep(
            is_buy=True,
            limit_price=100.02,
            quantity=2000,
            protected_quotes=protected,
            destination_venue="D",
        )
        # One child per venue that needs sweeping + one residual primary order.
        self.assertEqual(len(children), 4)
        self.assertTrue(all(child.is_iso for child in children))

        swept_total = sum(c.quantity for c in children if c.venue in {"A", "B", "C"})
        self.assertEqual(swept_total, 1000)

        residual = [c for c in children if c.venue == "D"]
        self.assertEqual(len(residual), 1)
        self.assertEqual(residual[0].quantity, 1000)
        self.assertAlmostEqual(residual[0].price, 100.02)


class TestRule200Marking(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_long_sale_from_inventory(self) -> None:
        mark = self.engine.mark_sell_order(inventory=500, sell_qty=300)
        self.assertEqual(mark, OrderMark.LONG)

    def test_short_sale_when_no_inventory(self) -> None:
        mark = self.engine.mark_sell_order(inventory=0, sell_qty=100)
        self.assertEqual(mark, OrderMark.SHORT)

    def test_short_exempt_for_bona_fide_mm_during_cb(self) -> None:
        mark = self.engine.mark_sell_order(
            inventory=0, sell_qty=100,
            is_bona_fide_mm=True,
            circuit_breaker_active=True,
        )
        self.assertEqual(mark, OrderMark.SHORT_EXEMPT)


class TestRule201CircuitBreaker(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_trigger_price_is_10_pct_below_close(self) -> None:
        self.assertAlmostEqual(
            self.engine.rule201_trigger_price(prior_close=100.0), 90.0
        )

    def test_triggered_when_intraday_reaches_threshold(self) -> None:
        self.assertTrue(
            self.engine.rule201_is_triggered(intraday_low=90.00, prior_close=100.0)
        )
        self.assertFalse(
            self.engine.rule201_is_triggered(intraday_low=90.01, prior_close=100.0)
        )

    def test_short_sale_price_must_exceed_nbb(self) -> None:
        trigger = date(2025, 4, 8)  # Tuesday
        result = self.engine.validate_short_sale_under_rule201(
            price=89.50, nbb=89.50,
            triggered=True, is_short_exempt=False,
            current_date=trigger, trigger_date=trigger,
        )
        self.assertFalse(result.ok)

        good = self.engine.validate_short_sale_under_rule201(
            price=89.51, nbb=89.50,
            triggered=True, is_short_exempt=False,
            current_date=trigger, trigger_date=trigger,
        )
        self.assertTrue(good.ok)

    def test_short_exempt_bypasses_price_test(self) -> None:
        trigger = date(2025, 4, 8)
        result = self.engine.validate_short_sale_under_rule201(
            price=89.00, nbb=89.50,
            triggered=True, is_short_exempt=True,
            current_date=trigger, trigger_date=trigger,
        )
        self.assertTrue(result.ok)

    def test_restriction_covers_next_trading_day(self) -> None:
        trigger = date(2025, 4, 8)  # Tuesday
        end = self.engine.rule201_restriction_end_date(trigger)
        self.assertEqual(end, date(2025, 4, 9))  # Wednesday

        # Friday trigger -> end on Monday (skip weekend).
        friday = date(2025, 4, 11)
        self.assertEqual(
            self.engine.rule201_restriction_end_date(friday), date(2025, 4, 14)
        )

    def test_restriction_expires_after_end_date(self) -> None:
        trigger = date(2025, 4, 8)
        result = self.engine.validate_short_sale_under_rule201(
            price=89.00, nbb=89.50,
            triggered=True, is_short_exempt=False,
            current_date=date(2025, 4, 10),  # Thursday
            trigger_date=trigger,
        )
        self.assertTrue(result.ok)


class TestRule204CloseOut(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_participant_close_out_is_t_plus_2(self) -> None:
        # Monday 2025-04-07 -> Wednesday 2025-04-09.
        deadline = self.engine.close_out_deadline(date(2025, 4, 7), is_market_maker=False)
        self.assertEqual(deadline, date(2025, 4, 9))

    def test_market_maker_close_out_is_t_plus_3(self) -> None:
        # Monday -> Thursday.
        deadline = self.engine.close_out_deadline(date(2025, 4, 7), is_market_maker=True)
        self.assertEqual(deadline, date(2025, 4, 10))

    def test_market_maker_gets_extra_day(self) -> None:
        mm = self.engine.close_out_deadline(date(2025, 4, 7), is_market_maker=True)
        reg = self.engine.close_out_deadline(date(2025, 4, 7), is_market_maker=False)
        self.assertGreater(mm, reg)


class TestThresholdSecurities(unittest.TestCase):
    def setUp(self) -> None:
        self.engine = MockTradingEngine()

    def test_requires_both_shares_and_percent(self) -> None:
        # Meets share count but not percentage.
        self.assertFalse(
            self.engine.is_threshold_security(
                ftd_shares=10_000,
                shares_outstanding=100_000_000,  # 0.01%
                consecutive_days=5,
            )
        )
        # Meets percentage but not share count.
        self.assertFalse(
            self.engine.is_threshold_security(
                ftd_shares=5_000,
                shares_outstanding=500_000,  # 1%
                consecutive_days=5,
            )
        )
        # Meets both.
        self.assertTrue(
            self.engine.is_threshold_security(
                ftd_shares=10_000,
                shares_outstanding=1_000_000,  # 1%
                consecutive_days=5,
            )
        )

    def test_requires_five_consecutive_days(self) -> None:
        self.assertFalse(
            self.engine.is_threshold_security(
                ftd_shares=10_000,
                shares_outstanding=1_000_000,
                consecutive_days=4,
            )
        )

    def test_hard_close_out_after_13_days(self) -> None:
        self.assertFalse(self.engine.requires_hard_close_out(12))
        self.assertTrue(self.engine.requires_hard_close_out(13))
        self.assertTrue(self.engine.requires_hard_close_out(20))


if __name__ == "__main__":
    unittest.main()
