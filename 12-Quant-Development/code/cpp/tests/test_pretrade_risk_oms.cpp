// Unit tests for the pre-trade risk gateway and order state machine
// (12-Quant-Development/code/cpp/pretrade_risk_oms.hpp), used by
// 12-Quant-Development/13-Risk-Checks-and-Order-Management.md.
//
// Covers: each check at its boundary, illegal transitions, duplicate execution reports,
// overfills and reconciliation failures tripping the kill switch, fills racing a cancel,
// replace exposure, cancel rejects, kill-switch behaviour, the FIX 4.4 Appendix D cancel
// scenarios B.1.b to B.1.d, and fail-closed handling of clock steps. Framework-free.

#include "pretrade_risk_oms.hpp"

#include <cstdint>
#include <iostream>
#include <string>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                              \
    do {                                                                                          \
        ++g_total;                                                                                \
        if (!(cond)) {                                                                            \
            ++g_failures;                                                                         \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << std::endl; \
        }                                                                                         \
    } while (0)

#define RUN_TEST(fn)                                                                    \
    do {                                                                                \
        std::cout << "[RUN ] " #fn << std::endl;                                        \
        const int before = g_failures;                                                  \
        fn();                                                                           \
        std::cout << (g_failures == before ? "[ OK ] " : "[FAIL] ") << #fn << std::endl; \
    } while (0)

using namespace oms;

constexpr std::uint64_t kMs = 1'000'000;

RiskLimits limits() {
    RiskLimits l;
    l.maxOrderQty = 1000;
    l.maxOrderNotionalCents = 10'000'000;  // $100,000
    l.priceCollarBps = 1000;               // 10%
    l.maxAbsPosition = 2000;
    l.creditLimitCents = 30'000'000;  // $300,000
    l.maxMessagesPerWindow = 100;
    l.throttleWindowNs = 1000 * kMs;
    l.repeatWindowNs = 10 * kMs;
    return l;
}

RiskGateway gateway() {
    RiskGateway gw(limits());
    gw.setReferencePrice("ABC", 5'000);  // $50.00
    return gw;
}

// Feeds a New ack so the order is live.
void ack(RiskGateway& gw, const std::string& id, const std::string& execId, std::int64_t qty) {
    EXPECT(gw.onExecutionReport({execId, id, "", ExecType::New, OrdStatus::New, 0, 0, qty, 0}) == ApplyResult::Applied);
}

void test_quantity_boundary() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"a", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::None);  // exactly at the limit
    EXPECT(gw.submit({"b", "ABC", Side::Buy, 1001, 5'000}, 1 * kMs) == RejectReason::MaxQuantity);
    EXPECT(gw.submit({"c", "ABC", Side::Buy, 0, 5'000}, 2 * kMs) == RejectReason::InvalidOrder);
    EXPECT(gw.submit({"d", "ABC", Side::Buy, -5, 5'000}, 3 * kMs) == RejectReason::InvalidOrder);
}

void test_collar_boundary_both_sides() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"b1", "ABC", Side::Buy, 10, 5'500}, 0) == RejectReason::None);  // +10.00% exactly
    EXPECT(gw.submit({"b2", "ABC", Side::Buy, 10, 5'501}, 20 * kMs) == RejectReason::PriceCollar);
    EXPECT(gw.submit({"s1", "ABC", Side::Sell, 10, 4'500}, 40 * kMs) == RejectReason::None);  // -10.00% exactly
    EXPECT(gw.submit({"s2", "ABC", Side::Sell, 10, 4'499}, 60 * kMs) == RejectReason::PriceCollar);
    // A sell far above the reference or a buy far below is not erroneous in the dangerous direction.
    EXPECT(gw.submit({"s3", "ABC", Side::Sell, 10, 9'000}, 80 * kMs) == RejectReason::None);
}

void test_notional_boundary_and_overflow_guard() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"n1", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::None);  // $50,000
    RiskLimits tight = limits();
    tight.maxOrderNotionalCents = 4'999'999;
    RiskGateway gw2(tight);
    gw2.setReferencePrice("ABC", 5'000);
    EXPECT(gw2.submit({"n2", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::MaxNotional);
    EXPECT(gw2.submit({"n3", "ABC", Side::Buy, 999, 5'000}, 0) == RejectReason::None);
    // An absurd price is rejected before any multiplication can overflow.
    EXPECT(gw2.submit({"n4", "ABC", Side::Buy, 1, INT64_MAX / 2}, 0) == RejectReason::InvalidOrder);
}

void test_reference_and_restricted_fail_closed() {
    RiskGateway gw = gateway();
    gw.restrict("BAD");
    gw.setReferencePrice("BAD", 1'000);
    EXPECT(gw.submit({"r1", "BAD", Side::Buy, 1, 1'000}, 0) == RejectReason::RestrictedSymbol);
    EXPECT(gw.submit({"r2", "NEW", Side::Buy, 1, 1'000}, 0) == RejectReason::NoReferencePrice);
    EXPECT(!gw.setReferencePrice("ZERO", 0));
    EXPECT(gw.submit({"r3", "ZERO", Side::Buy, 1, 1'000}, 0) == RejectReason::NoReferencePrice);
}

// A corrupt reference for a held symbol must not shrink the credit aggregate.
void test_bad_reference_for_held_symbol_fails_closed() {
    RiskLimits l = limits();
    l.creditLimitCents = 10'500'000;  // $105,000
    RiskGateway gw(l);
    EXPECT(gw.setReferencePrice("XYZ", 10'000));
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"x", "XYZ", Side::Buy, 1000, 10'000}, 0) == RejectReason::None);
    ack(gw, "x", "e1", 1000);
    EXPECT(gw.onExecutionReport({"e2", "x", "", ExecType::Trade, OrdStatus::Filled, 1000, 10'000, 0, 1000}) == ApplyResult::Applied);
    EXPECT(gw.grossExposureCents() == 10'000'000);  // 1000 x $100.00
    // $100,000 held + $10,000 new is over the $105,000 limit.
    EXPECT(gw.submit({"a1", "ABC", Side::Buy, 200, 5'000}, 20 * kMs) == RejectReason::CreditLimit);
    EXPECT(!gw.setReferencePrice("XYZ", 0));
    EXPECT(!gw.setReferencePrice("XYZ", -1));
    EXPECT(gw.submit({"a2", "ABC", Side::Buy, 200, 5'000}, 40 * kMs) == RejectReason::CreditLimit);
    EXPECT(gw.submit({"a3", "ABC", Side::Buy, 1, 5'000}, 60 * kMs) == RejectReason::CreditLimit);
    EXPECT(gw.submit({"x2", "XYZ", Side::Sell, 1, 10'000}, 80 * kMs) == RejectReason::NoReferencePrice);
    EXPECT(gw.setReferencePrice("XYZ", 10'000));
    EXPECT(gw.submit({"a4", "ABC", Side::Buy, 100, 5'000}, 100 * kMs) == RejectReason::None);  // $105,000 exactly
}

void test_duplicate_ids_are_burned_even_when_rejected() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"x", "ABC", Side::Buy, 5000, 5'000}, 0) == RejectReason::MaxQuantity);
    EXPECT(gw.submit({"x", "ABC", Side::Buy, 10, 5'000}, 1 * kMs) == RejectReason::DuplicateClOrdId);
}

void test_repeat_window_boundary() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"p1", "ABC", Side::Buy, 10, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.submit({"p2", "ABC", Side::Buy, 10, 5'000}, 9 * kMs) == RejectReason::RepeatedOrder);
    EXPECT(gw.submit({"p3", "ABC", Side::Buy, 11, 5'000}, 9 * kMs) == RejectReason::None);  // differs in qty
    EXPECT(gw.submit({"p4", "ABC", Side::Buy, 10, 5'000}, 10 * kMs) == RejectReason::None);  // window elapsed
}

void test_throttle_rolling_window() {
    RiskLimits l = limits();
    l.maxMessagesPerWindow = 2;
    RiskGateway gw(l);
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"t1", "ABC", Side::Buy, 1, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.submit({"t2", "ABC", Side::Buy, 2, 5'000}, 500 * kMs) == RejectReason::None);
    EXPECT(gw.submit({"t3", "ABC", Side::Buy, 3, 5'000}, 999 * kMs) == RejectReason::Throttle);
    EXPECT(gw.submit({"t4", "ABC", Side::Buy, 4, 5'000}, 1000 * kMs) == RejectReason::None);  // t1 left the window
    // Cancels are never throttled.
    EXPECT(gw.requestCancel("t1", "c1") == RejectReason::None);
}

void test_position_limit_counts_open_orders_both_sides() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"l1", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.submit({"l2", "ABC", Side::Buy, 1000, 4'990}, 20 * kMs) == RejectReason::None);  // worst case long 2000
    EXPECT(gw.submit({"l3", "ABC", Side::Buy, 1, 4'980}, 40 * kMs) == RejectReason::PositionLimit);
    // Sells are checked against the short side independently: open buys do not offset them.
    EXPECT(gw.submit({"s1", "ABC", Side::Sell, 1000, 5'010}, 60 * kMs) == RejectReason::None);
    EXPECT(gw.submit({"s2", "ABC", Side::Sell, 1000, 5'020}, 80 * kMs) == RejectReason::None);
    EXPECT(gw.submit({"s3", "ABC", Side::Sell, 1, 5'030}, 100 * kMs) == RejectReason::PositionLimit);
}

void test_credit_limit_is_gross() {
    RiskLimits l = limits();
    l.creditLimitCents = 9'000'000;  // $90,000
    RiskGateway gw(l);
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"g1", "ABC", Side::Buy, 900, 5'000}, 0) == RejectReason::None);  // $45,000
    EXPECT(gw.submit({"g2", "ABC", Side::Sell, 900, 5'000}, 20 * kMs) == RejectReason::None);  // $90,000 exactly
    EXPECT(gw.grossExposureCents() == 9'000'000);
    EXPECT(gw.submit({"g3", "ABC", Side::Sell, 1, 5'000}, 40 * kMs) == RejectReason::CreditLimit);
}

void test_lifecycle_and_duplicate_reports() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 300, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.order("o")->status == OrdStatus::PendingNew);
    ack(gw, "o", "e1", 300);
    EXPECT(gw.onExecutionReport({"e1", "o", "", ExecType::New, OrdStatus::New, 0, 0, 300, 0}) == ApplyResult::Duplicate);
    const ExecReport fill{"e2", "o", "", ExecType::Trade, OrdStatus::PartiallyFilled, 100, 5'000, 200, 100};
    EXPECT(gw.onExecutionReport(fill) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport(fill) == ApplyResult::Duplicate);  // replayed after a reconnect
    EXPECT(gw.position("ABC") == 100);
    EXPECT(gw.onExecutionReport({"e3", "o", "", ExecType::Trade, OrdStatus::Filled, 200, 5'010, 0, 300}) == ApplyResult::Applied);
    EXPECT(gw.order("o")->status == OrdStatus::Filled);
    EXPECT(gw.position("ABC") == 300);
    EXPECT(!gw.killed());
}

void test_illegal_transitions_trip_kill_switch() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    // Replaced without a pending replace is illegal.
    EXPECT(gw.onExecutionReport({"e1", "o", "", ExecType::Replaced, OrdStatus::New, 0, 0, 100, 0}) == ApplyResult::IllegalTransition);
    EXPECT(gw.killed());
    EXPECT(gw.submit({"o2", "ABC", Side::Buy, 1, 5'000}, 20 * kMs) == RejectReason::KillSwitch);
    gw.resetKillSwitch();  // a human re-arms
    EXPECT(gw.submit({"o3", "ABC", Side::Buy, 2, 5'000}, 40 * kMs) == RejectReason::None);
}

void test_bad_last_px_is_inconsistent() {
    for (const std::int64_t px : {std::int64_t{0}, std::int64_t{-5'000}, kMaxPriceCents + 1, INT64_MAX / 2}) {
        RiskGateway gw = gateway();
        EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
        ack(gw, "o", "e1", 100);
        EXPECT(gw.onExecutionReport({"e2", "o", "", ExecType::Trade, OrdStatus::PartiallyFilled, 3, px, 97, 3}) == ApplyResult::Inconsistent);
        EXPECT(gw.killed() && gw.position("ABC") == 0 && gw.order("o")->cumQty == 0);
    }
}

void test_overfill_and_mismatch_are_inconsistent() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Sell, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "o", "e1", 100);
    EXPECT(gw.onExecutionReport({"e2", "o", "", ExecType::Trade, OrdStatus::Filled, 150, 5'000, 0, 150}) == ApplyResult::Inconsistent);
    EXPECT(gw.killed());
    RiskGateway gw2 = gateway();
    EXPECT(gw2.submit({"p", "ABC", Side::Sell, 100, 5'000}, 0) == RejectReason::None);
    ack(gw2, "p", "f1", 100);
    // Venue says CumQty 60 after a 50-share fill: our books disagree, stop.
    EXPECT(gw2.onExecutionReport({"f2", "p", "", ExecType::Trade, OrdStatus::PartiallyFilled, 50, 5'000, 50, 60}) == ApplyResult::Inconsistent);
    EXPECT(gw2.killed());
    RiskGateway gw3 = gateway();
    EXPECT(gw3.onExecutionReport({"g1", "nobody", "", ExecType::New, OrdStatus::New, 0, 0, 1, 0}) == ApplyResult::UnknownOrder);
    EXPECT(gw3.killed());
}

void test_fill_racing_cancel_then_cancel_reject() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "o", "e1", 100);
    EXPECT(gw.requestCancel("o", "c1") == RejectReason::None);
    EXPECT(gw.requestCancel("o", "c2") == RejectReason::NotModifiable);  // one in flight at a time
    EXPECT(gw.onExecutionReport({"e2", "o", "", ExecType::Trade, OrdStatus::PendingCancel, 40, 5'000, 60, 40}) == ApplyResult::Applied);
    EXPECT(gw.onCancelReject("c1") == ApplyResult::Applied);  // venue refused the cancel
    EXPECT(gw.order("o")->status == OrdStatus::PartiallyFilled);
    // The remaining 60 fill: the order completes.
    EXPECT(gw.onExecutionReport({"e3", "o", "", ExecType::Trade, OrdStatus::Filled, 60, 5'000, 0, 100}) == ApplyResult::Applied);
    EXPECT(gw.requestCancel("o", "c3") == RejectReason::NotModifiable);
}

void test_replace_checks_worst_case_and_applies() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.submit({"q", "ABC", Side::Buy, 900, 4'990}, 20 * kMs) == RejectReason::None);  // worst case 1900
    ack(gw, "o", "e1", 1000);
    // 1101 is above the 1000-share order limit, so the per-order check fires first.
    EXPECT(gw.requestReplace("o", "r1", 1101, 5'000, 40 * kMs) == RejectReason::MaxQuantity);
    // With a looser order limit, growing o to 1101 would allow 2001 long in the worst case.
    RiskLimits l = limits();
    l.maxOrderQty = 5000;
    l.maxOrderNotionalCents = 100'000'000;
    RiskGateway gw2(l);
    gw2.setReferencePrice("ABC", 5'000);
    EXPECT(gw2.submit({"o", "ABC", Side::Buy, 1000, 5'000}, 0) == RejectReason::None);
    EXPECT(gw2.submit({"q", "ABC", Side::Buy, 900, 4'990}, 20 * kMs) == RejectReason::None);
    ack(gw2, "o", "e1", 1000);
    EXPECT(gw2.requestReplace("o", "r1", 1101, 5'000, 40 * kMs) == RejectReason::PositionLimit);
    EXPECT(gw2.requestReplace("o", "r2", 1100, 5'000, 60 * kMs) == RejectReason::None);  // exactly 2000
    EXPECT(gw2.openQty("ABC", Side::Buy) == 2000);
    EXPECT(gw2.onExecutionReport({"e2", "r2", "o", ExecType::Replaced, OrdStatus::New, 0, 0, 1100, 0}) == ApplyResult::Applied);
    EXPECT(gw2.order("o")->orderQty == 1100);
    EXPECT(gw2.order("r2")->currentClOrdId == "r2");
    // Cannot shrink below the filled quantity.
    EXPECT(gw2.onExecutionReport({"e3", "r2", "", ExecType::Trade, OrdStatus::PartiallyFilled, 500, 5'000, 600, 500}) == ApplyResult::Applied);
    EXPECT(gw2.requestReplace("o", "r3", 500, 5'000, 80 * kMs) == RejectReason::InvalidOrder);
}

void test_kill_switch_lists_live_orders_and_allows_cancels() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"a", "ABC", Side::Buy, 10, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.submit({"b", "ABC", Side::Buy, 20, 5'000}, 20 * kMs) == RejectReason::None);
    EXPECT(gw.submit({"c", "ABC", Side::Buy, 30, 5'000}, 40 * kMs) == RejectReason::None);
    ack(gw, "a", "e1", 10);
    EXPECT(gw.onExecutionReport({"e2", "a", "", ExecType::Trade, OrdStatus::Filled, 10, 5'000, 0, 10}) == ApplyResult::Applied);
    const auto cancels = gw.engageKillSwitch("manual");
    EXPECT(cancels.size() == 2 && cancels[0] == "b" && cancels[1] == "c");
    EXPECT(gw.requestReplace("b", "rb", 5, 5'000, 60 * kMs) == RejectReason::KillSwitch);
    EXPECT(gw.requestCancel("b", "cb") == RejectReason::None);
    EXPECT(gw.engageKillSwitch("again").size() == 1);  // b is pending cancel, only c remains
    EXPECT(gw.killReason() == "manual");               // the first reason is kept
}

// The kill switch must be able to cancel an order whose replace is still in flight.
void test_kill_switch_cancels_order_with_pending_replace() {
    // Venue applies the replace, then the cancel.
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "X", "e1", 100);
    EXPECT(gw.requestReplace("X", "R", 300, 4'900, 20 * kMs) == RejectReason::None);
    const auto cancels = gw.engageKillSwitch("manual");
    EXPECT(cancels.size() == 1 && cancels[0] == "X");
    EXPECT(gw.requestCancel("X", "C") == RejectReason::None);
    EXPECT(gw.order("X")->status == OrdStatus::PendingCancel);
    EXPECT(gw.engageKillSwitch("again").empty());
    EXPECT(gw.openQty("ABC", Side::Buy) == 300);  // either set of replace terms can still trade
    EXPECT(gw.grossExposureCents() == 1'500'000);  // 300 x $50.00, the worse price
    EXPECT(gw.onExecutionReport({"e2", "R", "X", ExecType::PendingReplace, OrdStatus::PendingReplace, 0, 0, 100, 0}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e3", "X", "", ExecType::Trade, OrdStatus::PendingCancel, 10, 5'000, 90, 10}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e4", "R", "X", ExecType::Replaced, OrdStatus::PendingCancel, 0, 0, 290, 10}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::PendingCancel && gw.order("X")->orderQty == 300);
    EXPECT(gw.onExecutionReport({"e5", "C", "R", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 10}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::Canceled && gw.openQty("ABC", Side::Buy) == 0);
    EXPECT(gw.position("ABC") == 10 && gw.killReason() == "manual");

    // Venue rejects the replace; the cancel still stands and then completes.
    RiskGateway gw2 = gateway();
    EXPECT(gw2.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw2, "X", "e1", 100);
    EXPECT(gw2.requestReplace("X", "R", 300, 4'900, 20 * kMs) == RejectReason::None);
    EXPECT(gw2.requestCancel("X", "C") == RejectReason::None);
    EXPECT(gw2.onCancelReject("R") == ApplyResult::Applied);
    EXPECT(gw2.order("X")->status == OrdStatus::PendingCancel && gw2.openQty("ABC", Side::Buy) == 100);
    EXPECT(gw2.onExecutionReport({"e2", "C", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(gw2.order("X")->status == OrdStatus::Canceled && !gw2.killed());

    // Venue rejects the cancel; the replace is still pending and then applies.
    RiskGateway gw3 = gateway();
    EXPECT(gw3.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw3, "X", "e1", 100);
    EXPECT(gw3.requestReplace("X", "R", 300, 4'900, 20 * kMs) == RejectReason::None);
    EXPECT(gw3.requestCancel("X", "C") == RejectReason::None);
    EXPECT(gw3.onCancelReject("C") == ApplyResult::Applied);
    EXPECT(gw3.order("X")->status == OrdStatus::PendingReplace);
    EXPECT(gw3.onExecutionReport({"e2", "R", "X", ExecType::Replaced, OrdStatus::New, 0, 0, 300, 0}) == ApplyResult::Applied);
    EXPECT(gw3.order("X")->status == OrdStatus::New && gw3.order("X")->priceCents == 4'900 && !gw3.killed());
}

// FIX 4.4 Volume 4, Appendix D, B.1.b: a fill that crosses our cancel on the wire carries the
// venue's pre-cancel OrdStatus (1), a later one carries Pending Cancel (6); both must be accepted.
void test_fix44_b1b_fill_crossing_cancel() {
    RiskLimits l = limits();
    l.maxOrderQty = 10'000;
    l.maxOrderNotionalCents = 100'000'000;
    l.maxAbsPosition = 20'000;
    l.creditLimitCents = 100'000'000;
    RiskGateway gw(l);
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"X", "ABC", Side::Buy, 10'000, 5'000}, 0) == RejectReason::None);
    ack(gw, "X", "e1", 10'000);
    EXPECT(gw.onExecutionReport({"e2", "X", "", ExecType::Trade, OrdStatus::PartiallyFilled, 2'000, 5'000, 8'000, 2'000}) == ApplyResult::Applied);
    EXPECT(gw.requestCancel("X", "Y") == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e3", "X", "", ExecType::Trade, OrdStatus::PartiallyFilled, 3'000, 5'000, 5'000, 5'000}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::PendingCancel);
    EXPECT(gw.onExecutionReport({"e4", "Y", "X", ExecType::PendingCancel, OrdStatus::PendingCancel, 0, 0, 5'000, 5'000}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e5", "X", "", ExecType::Trade, OrdStatus::PendingCancel, 1'000, 5'000, 4'000, 6'000}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e6", "Y", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 6'000}) == ApplyResult::Applied);
    EXPECT(gw.position("ABC") == 6'000);
    EXPECT(!gw.killed());
}

// B.1.c: the order fills completely while the cancel is pending. Pending Cancel takes precedence
// over Filled in that fill's OrdStatus, and the venue's cancel reject then reports Filled.
void test_fix44_b1c_filled_while_pending_cancel() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "X", "e1", 100);
    EXPECT(gw.requestCancel("X", "Y") == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e2", "Y", "X", ExecType::PendingCancel, OrdStatus::PendingCancel, 0, 0, 100, 0}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e3", "X", "", ExecType::Trade, OrdStatus::PendingCancel, 100, 5'000, 0, 100}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::PendingCancel && gw.order("X")->leavesQty == 0);
    EXPECT(gw.openQty("ABC", Side::Buy) == 0);  // nothing left that can execute
    EXPECT(gw.onCancelReject("Y") == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::Filled);
    EXPECT(gw.position("ABC") == 100);
    EXPECT(!gw.killed());
}

// B.1.d: a cancel sent before the ack; the venue acks the order (39=0), then cancels it.
void test_fix44_b1d_cancel_before_ack() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.requestCancel("X", "Y") == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e1", "Y", "X", ExecType::PendingCancel, OrdStatus::PendingCancel, 0, 0, 100, 0}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e2", "X", "", ExecType::New, OrdStatus::New, 0, 0, 100, 0}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::PendingCancel);
    EXPECT(gw.onExecutionReport({"e3", "Y", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(gw.order("X")->status == OrdStatus::Canceled);
    // Second half of B.1.d: canceled before it is ever accepted.
    EXPECT(gw.submit({"A", "ABC", Side::Buy, 50, 5'000}, 20 * kMs) == RejectReason::None);
    EXPECT(gw.requestCancel("A", "B") == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e4", "B", "A", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(!gw.killed());
}

// A replace whose new quantity is used up by fills while it is pending completes the order
// (FIX 4.4 Appendix D, C.3.b and C.3.c).
void test_replace_overtaken_by_fills() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "o", "e1", 100);
    EXPECT(gw.onExecutionReport({"e2", "o", "", ExecType::Trade, OrdStatus::PartiallyFilled, 40, 5'000, 60, 40}) == ApplyResult::Applied);
    EXPECT(gw.requestReplace("o", "r", 60, 5'000, 20 * kMs) == RejectReason::None);  // shrink to 60
    EXPECT(gw.onExecutionReport({"e3", "o", "", ExecType::Trade, OrdStatus::PartiallyFilled, 20, 5'000, 40, 60}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e4", "r", "o", ExecType::Replaced, OrdStatus::Filled, 0, 0, 0, 60}) == ApplyResult::Applied);
    EXPECT(gw.order("o")->status == OrdStatus::Filled && gw.order("o")->orderQty == 60);
    // Appendix D, C.3.c: replace 100 -> 70 crosses a fill of 80; the venue amends the order to 80, Filled.
    EXPECT(gw.submit({"p", "ABC", Side::Buy, 100, 5'010}, 40 * kMs) == RejectReason::None);
    ack(gw, "p", "f1", 100);
    EXPECT(gw.requestReplace("p", "rp", 70, 5'010, 60 * kMs) == RejectReason::None);
    EXPECT(gw.onExecutionReport({"f2", "p", "", ExecType::Trade, OrdStatus::PartiallyFilled, 80, 5'010, 20, 80}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"f3", "rp", "p", ExecType::Replaced, OrdStatus::Filled, 0, 0, 0, 80}) == ApplyResult::Applied);
    EXPECT(gw.order("p")->status == OrdStatus::Filled && gw.order("p")->orderQty == 80);
    EXPECT(!gw.killed());
}

// Fail closed on bad clocks and absurd references instead of wrapping or overflowing.
void test_clock_step_back_and_reference_bound() {
    RiskLimits l = limits();
    l.maxMessagesPerWindow = 1;
    RiskGateway gw(l);
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"t1", "ABC", Side::Buy, 1, 5'000}, 5'000 * kMs) == RejectReason::None);
    // The clock steps back 1 s: the unsigned age must not wrap and empty the window.
    EXPECT(gw.submit({"t2", "ABC", Side::Buy, 2, 5'000}, 4'000 * kMs) == RejectReason::Throttle);
    EXPECT(!gw.setReferencePrice("HUGE", kMaxPriceCents + 1));
    EXPECT(gw.submit({"h1", "HUGE", Side::Buy, 1, 1'000}, 6'000 * kMs) == RejectReason::NoReferencePrice);
}

}  // namespace

int main() {
    RUN_TEST(test_quantity_boundary);
    RUN_TEST(test_collar_boundary_both_sides);
    RUN_TEST(test_notional_boundary_and_overflow_guard);
    RUN_TEST(test_reference_and_restricted_fail_closed);
    RUN_TEST(test_bad_reference_for_held_symbol_fails_closed);
    RUN_TEST(test_duplicate_ids_are_burned_even_when_rejected);
    RUN_TEST(test_repeat_window_boundary);
    RUN_TEST(test_throttle_rolling_window);
    RUN_TEST(test_position_limit_counts_open_orders_both_sides);
    RUN_TEST(test_credit_limit_is_gross);
    RUN_TEST(test_lifecycle_and_duplicate_reports);
    RUN_TEST(test_illegal_transitions_trip_kill_switch);
    RUN_TEST(test_bad_last_px_is_inconsistent);
    RUN_TEST(test_overfill_and_mismatch_are_inconsistent);
    RUN_TEST(test_fill_racing_cancel_then_cancel_reject);
    RUN_TEST(test_replace_checks_worst_case_and_applies);
    RUN_TEST(test_kill_switch_lists_live_orders_and_allows_cancels);
    RUN_TEST(test_kill_switch_cancels_order_with_pending_replace);
    RUN_TEST(test_fix44_b1b_fill_crossing_cancel);
    RUN_TEST(test_fix44_b1c_filled_while_pending_cancel);
    RUN_TEST(test_fix44_b1d_cancel_before_ack);
    RUN_TEST(test_replace_overtaken_by_fills);
    RUN_TEST(test_clock_step_back_and_reference_bound);
    std::cout << "\n" << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
