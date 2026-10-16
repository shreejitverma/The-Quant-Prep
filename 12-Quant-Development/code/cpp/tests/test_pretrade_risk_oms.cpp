// Unit tests for the pre-trade risk gateway and order state machine
// (12-Quant-Development/code/cpp/pretrade_risk_oms.hpp), used by
// 12-Quant-Development/13-Risk-Checks-and-Order-Management.md.
//
// Covers: each check at its boundary, illegal transitions, duplicate execution reports,
// overfills and reconciliation failures tripping the kill switch, fills racing a cancel,
// replace exposure, cancel rejects, and kill-switch behaviour. Framework-free.

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
    gw.setReferencePrice("ZERO", 0);
    EXPECT(gw.submit({"r3", "ZERO", Side::Buy, 1, 1'000}, 0) == RejectReason::NoReferencePrice);
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
    // Growing o to 1101 would allow 2001 long in the worst case.
    EXPECT(gw.requestReplace("o", "r1", 1101, 5'000, 40 * kMs) == RejectReason::MaxQuantity);
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

}  // namespace

int main() {
    RUN_TEST(test_quantity_boundary);
    RUN_TEST(test_collar_boundary_both_sides);
    RUN_TEST(test_notional_boundary_and_overflow_guard);
    RUN_TEST(test_reference_and_restricted_fail_closed);
    RUN_TEST(test_duplicate_ids_are_burned_even_when_rejected);
    RUN_TEST(test_repeat_window_boundary);
    RUN_TEST(test_throttle_rolling_window);
    RUN_TEST(test_position_limit_counts_open_orders_both_sides);
    RUN_TEST(test_credit_limit_is_gross);
    RUN_TEST(test_lifecycle_and_duplicate_reports);
    RUN_TEST(test_illegal_transitions_trip_kill_switch);
    RUN_TEST(test_overfill_and_mismatch_are_inconsistent);
    RUN_TEST(test_fill_racing_cancel_then_cancel_reject);
    RUN_TEST(test_replace_checks_worst_case_and_applies);
    RUN_TEST(test_kill_switch_lists_live_orders_and_allows_cancels);
    std::cout << "\n" << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
