// Unit tests for the pre-trade risk gateway and order state machine
// (12-Quant-Development/code/cpp/pretrade_risk_oms.hpp), used by
// 12-Quant-Development/13-Risk-Checks-and-Order-Management.md.
//
// Covers: each check at its boundary, illegal transitions, duplicate execution reports,
// overfills and reconciliation failures tripping the kill switch, fills racing a cancel,
// replace exposure, cancel rejects, kill-switch behaviour, the FIX 4.4 Appendix D cancel
// scenarios B.1.b to B.1.d, late acks after fills, responses matched to the request ledger,
// fail-closed handling of clock steps, bad references and exposure overflow, and a randomized
// model check against an independently written venue. Framework-free.

#include "pretrade_risk_oms.hpp"

#include <cstdint>
#include <cstdlib>
#include <deque>
#include <iostream>
#include <limits>
#include <map>
#include <optional>
#include <string>
#include <vector>

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

// A bad tick is rejected and counted, and the last valid reference keeps valuing the position.
void test_invalid_reference_keeps_last_valid() {
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
    EXPECT(!gw.setReferencePrice("XYZ", kMaxPriceCents + 1));
    EXPECT(gw.invalidReferencePrices() == 3);
    EXPECT(gw.grossExposureCents() == 10'000'000);  // still valued at $100.00
    EXPECT(gw.submit({"a2", "ABC", Side::Buy, 200, 5'000}, 40 * kMs) == RejectReason::CreditLimit);
    // The 10% collar is still measured against $100.00: 89.99 is below 90.00, 90.00 is not.
    EXPECT(gw.submit({"x2", "XYZ", Side::Sell, 1, 8'999}, 60 * kMs) == RejectReason::PriceCollar);
    EXPECT(gw.submit({"x3", "XYZ", Side::Sell, 1, 9'000}, 80 * kMs) == RejectReason::None);
    // $100,000 + $90 + 98 x $50.00 = $104,990, within $105,000.
    EXPECT(gw.submit({"a3", "ABC", Side::Buy, 98, 5'000}, 100 * kMs) == RejectReason::None);
    EXPECT(gw.grossExposureCents() == 10'499'000);
}

// A position held in a symbol that never had a valid reference cannot be valued: fail closed.
void test_held_symbol_without_any_reference_fails_closed() {
    RiskGateway gw = gateway();
    gw.setStartOfDayPosition("XYZ", -100);
    EXPECT(gw.grossExposureCents() == RiskGateway::kUnvaluedExposure);
    EXPECT(gw.submit({"a1", "ABC", Side::Buy, 1, 5'000}, 0) == RejectReason::CreditLimit);
    EXPECT(!gw.setReferencePrice("XYZ", 0));
    EXPECT(gw.submit({"a2", "ABC", Side::Buy, 2, 5'000}, 20 * kMs) == RejectReason::CreditLimit);
    EXPECT(gw.setReferencePrice("XYZ", 10'000));
    EXPECT(gw.grossExposureCents() == 1'000'000);  // |-100| x $100.00
    EXPECT(gw.submit({"a3", "ABC", Side::Buy, 3, 5'000}, 40 * kMs) == RejectReason::None);
    // A flat carried-in position needs no reference.
    RiskGateway flat = gateway();
    flat.setStartOfDayPosition("XYZ", 0);
    EXPECT(flat.submit({"b1", "ABC", Side::Buy, 1, 5'000}, 0) == RejectReason::None);
}

// Exposures past int64 must fail the credit check closed, not wrap negative and pass it.
void test_exposure_overflow_fails_closed() {
    RiskLimits l;
    l.maxOrderQty = 10'000'000;
    l.maxOrderNotionalCents = std::numeric_limits<std::int64_t>::max();
    l.priceCollarBps = 1000;
    l.maxAbsPosition = 10'000'000;
    l.creditLimitCents = std::numeric_limits<std::int64_t>::max() - 1;
    l.maxMessagesPerWindow = 100;
    l.throttleWindowNs = 1000 * kMs;
    l.repeatWindowNs = 10 * kMs;
    RiskGateway gw(l);
    gw.setReferencePrice("XYZ", 1'000);
    gw.setReferencePrice("ABC", 5'000);
    EXPECT(gw.submit({"x", "XYZ", Side::Buy, 9'000'000, 1'000}, 0) == RejectReason::None);
    ack(gw, "x", "e1", 9'000'000);
    EXPECT(gw.onExecutionReport({"e2", "x", "", ExecType::Trade, OrdStatus::Filled, 9'000'000, 1'000, 0, 9'000'000}) == ApplyResult::Applied);
    // 9e6 x 2^40 cents is about 9.9e18, above INT64_MAX (about 9.2e18).
    EXPECT(gw.setReferencePrice("XYZ", kMaxPriceCents));
    EXPECT(gw.grossExposureCents() == RiskGateway::kUnvaluedExposure);
    EXPECT(gw.submit({"a", "ABC", Side::Buy, 1, 5'000}, 20 * kMs) == RejectReason::CreditLimit);

    // A replace whose worst case pairs the old quantity with the new price overflows the same way.
    RiskLimits big = l;
    big.maxOrderQty = std::int64_t{1} << 30;
    big.maxAbsPosition = std::int64_t{1} << 30;
    big.priceCollarBps = 0;
    RiskGateway gw2(big);
    gw2.setReferencePrice("XYZ", kMaxPriceCents);
    EXPECT(gw2.submit({"o", "XYZ", Side::Buy, std::int64_t{1} << 30, 1}, 0) == RejectReason::None);
    EXPECT(gw2.requestReplace("o", "r", 1, kMaxPriceCents, 20 * kMs) == RejectReason::CreditLimit);  // 2^30 x 2^40

    // A fill whose notional cannot be represented does not reconcile.
    RiskGateway gw3(l);
    gw3.setReferencePrice("XYZ", 1'000);
    EXPECT(gw3.submit({"y", "XYZ", Side::Buy, 9'000'000, 1'000}, 0) == RejectReason::None);
    ack(gw3, "y", "f1", 9'000'000);
    EXPECT(gw3.onExecutionReport({"f2", "y", "", ExecType::Trade, OrdStatus::Filled, 9'000'000, kMaxPriceCents, 0, 9'000'000}) ==
           ApplyResult::Inconsistent);
    EXPECT(gw3.killed() && gw3.position("XYZ") == 0 && gw3.order("y")->cumQty == 0);
}

// A fill before the New ack is an implicit acknowledgement; the late ack is a no-op, not a kill.
void test_late_ack_after_fill_is_reconciled() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e1", "o", "", ExecType::Trade, OrdStatus::PartiallyFilled, 10, 5'000, 90, 10}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"e2", "o", "", ExecType::PendingNew, OrdStatus::PendingNew, 0, 0, 100, 0}) == ApplyResult::Ignored);
    EXPECT(gw.onExecutionReport({"e3", "o", "", ExecType::New, OrdStatus::New, 0, 0, 100, 0}) == ApplyResult::Ignored);
    EXPECT(gw.ignoredResponses() == 2);
    EXPECT(gw.order("o")->status == OrdStatus::PartiallyFilled && gw.order("o")->cumQty == 10 && gw.order("o")->leavesQty == 90);
    EXPECT(!gw.killed());
    // A cancel sent before the ack, then a fill, then the ack (B.1.d with a fill in between).
    EXPECT(gw.submit({"p", "ABC", Side::Buy, 50, 5'000}, 20 * kMs) == RejectReason::None);
    EXPECT(gw.requestCancel("p", "cp") == RejectReason::None);
    EXPECT(gw.onExecutionReport({"f1", "p", "", ExecType::Trade, OrdStatus::PartiallyFilled, 20, 5'000, 30, 20}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"f2", "p", "", ExecType::New, OrdStatus::New, 0, 0, 50, 0}) == ApplyResult::Ignored);
    EXPECT(gw.order("p")->status == OrdStatus::PendingCancel && !gw.killed());
    EXPECT(gw.onExecutionReport({"f3", "cp", "p", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 20}) == ApplyResult::Applied);
    EXPECT(gw.position("ABC") == 30 && !gw.killed());
    // A late ack that does not add up to the order is still a reconciliation failure.
    EXPECT(gw.submit({"q", "ABC", Side::Buy, 70, 5'000}, 40 * kMs) == RejectReason::None);
    EXPECT(gw.onExecutionReport({"g1", "q", "", ExecType::Trade, OrdStatus::PartiallyFilled, 5, 5'000, 65, 5}) == ApplyResult::Applied);
    EXPECT(gw.onExecutionReport({"g2", "q", "", ExecType::New, OrdStatus::New, 0, 0, 50, 0}) == ApplyResult::Inconsistent);
    EXPECT(gw.killed());
    // Without a fill, a second ack is still illegal.
    RiskGateway gw2 = gateway();
    EXPECT(gw2.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw2, "o", "e1", 100);
    EXPECT(gw2.onExecutionReport({"e2", "o", "", ExecType::New, OrdStatus::New, 0, 0, 100, 0}) == ApplyResult::IllegalTransition);
    EXPECT(gw2.killed());
}

// Responses to a cancel or replace are matched against the request ledger.
void test_responses_must_match_request_in_flight() {
    // A resent reject for an earlier, already rejected cancel is counted and ignored: it must not
    // undo the cancel now in flight.
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"o", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "o", "e1", 100);
    EXPECT(gw.requestCancel("o", "c1") == RejectReason::None);
    EXPECT(gw.onCancelReject("c1") == ApplyResult::Applied);
    EXPECT(gw.requestCancel("o", "c2") == RejectReason::None);
    EXPECT(gw.onCancelReject("c1") == ApplyResult::Ignored);
    EXPECT(!gw.killed() && gw.order("o")->status == OrdStatus::PendingCancel && gw.ignoredResponses() == 1);
    EXPECT(gw.onCancelReject("c2") == ApplyResult::Applied);
    EXPECT(gw.order("o")->status == OrdStatus::New);
    // An unknown id trips the kill switch.
    RiskGateway gw2 = gateway();
    EXPECT(gw2.onCancelReject("nobody") == ApplyResult::UnknownOrder);
    EXPECT(gw2.killed());
    // With a cancel over a pending replace, the original id is neither request in flight.
    RiskGateway gw3 = gateway();
    EXPECT(gw3.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw3, "X", "e1", 100);
    EXPECT(gw3.requestReplace("X", "R", 300, 4'900, 20 * kMs) == RejectReason::None);
    EXPECT(gw3.requestCancel("X", "C") == RejectReason::None);
    EXPECT(gw3.onCancelReject("X") == ApplyResult::IllegalTransition);
    EXPECT(gw3.killed() && gw3.order("X")->status == OrdStatus::PendingCancel && gw3.order("X")->replacePending());
    // Replaced must carry the pending replace's ClOrdID, Canceled the pending cancel's or the current one.
    RiskGateway gw4 = gateway();
    EXPECT(gw4.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw4, "X", "e1", 100);
    EXPECT(gw4.requestReplace("X", "R1", 200, 5'000, 20 * kMs) == RejectReason::None);
    EXPECT(gw4.onCancelReject("R1") == ApplyResult::Applied);
    EXPECT(gw4.requestReplace("X", "R2", 300, 5'000, 40 * kMs) == RejectReason::None);
    EXPECT(gw4.onExecutionReport({"e2", "R1", "X", ExecType::Replaced, OrdStatus::New, 0, 0, 200, 0}) == ApplyResult::IllegalTransition);
    EXPECT(gw4.killed() && gw4.order("X")->orderQty == 100);
    RiskGateway gw5 = gateway();
    EXPECT(gw5.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw5, "X", "e1", 100);
    EXPECT(gw5.requestCancel("X", "C1") == RejectReason::None);
    EXPECT(gw5.onCancelReject("C1") == ApplyResult::Applied);
    EXPECT(gw5.requestCancel("X", "C2") == RejectReason::None);
    EXPECT(gw5.onExecutionReport({"e2", "C1", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::IllegalTransition);
    EXPECT(gw5.killed() && gw5.order("X")->status == OrdStatus::PendingCancel);
    // An unsolicited cancel on the current ClOrdID is accepted.
    RiskGateway gw6 = gateway();
    EXPECT(gw6.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw6, "X", "e1", 100);
    EXPECT(gw6.onExecutionReport({"e2", "X", "", ExecType::Expired, OrdStatus::Expired, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(!gw6.killed());
    // A cancel reject after the venue rejected the order itself changes nothing.
    RiskGateway gw7 = gateway();
    EXPECT(gw7.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    EXPECT(gw7.requestCancel("X", "C") == RejectReason::None);
    EXPECT(gw7.onExecutionReport({"e1", "X", "", ExecType::Rejected, OrdStatus::Rejected, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(gw7.onCancelReject("C") == ApplyResult::Ignored);
    EXPECT(gw7.order("X")->status == OrdStatus::Rejected && !gw7.killed());
    // The venue ends the order on its own (end of day) while our cancel, or our replace, is on the
    // wire; the venue then answers that request with a too-late cancel reject, a routine race.
    RiskGateway gw8 = gateway();
    EXPECT(gw8.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw8, "X", "e1", 100);
    EXPECT(gw8.requestCancel("X", "C1") == RejectReason::None);
    EXPECT(gw8.onExecutionReport({"e2", "X", "", ExecType::Expired, OrdStatus::Expired, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(gw8.onCancelReject("C1") == ApplyResult::Ignored);
    EXPECT(gw8.order("X")->status == OrdStatus::Expired && !gw8.killed());
    RiskGateway gw9 = gateway();
    EXPECT(gw9.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw9, "X", "e1", 100);
    EXPECT(gw9.requestReplace("X", "R1", 200, 5'000, 20 * kMs) == RejectReason::None);
    EXPECT(gw9.onExecutionReport({"e2", "X", "", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(gw9.onCancelReject("R1") == ApplyResult::Ignored);
    EXPECT(gw9.order("X")->status == OrdStatus::Canceled && !gw9.killed());
    // A reject naming the ended order itself, not a request sent for it, is still a reconciliation failure.
    EXPECT(gw9.onCancelReject("X") == ApplyResult::IllegalTransition && gw9.killed());
}

// The venue cannot both accept and reject one request: a reject for an accepted cancel or replace
// is a reconciliation break, while a resent reject for one already rejected is only late.
void test_contradictory_answers_are_breaks() {
    // (a) the cancel succeeded, then a reject for the same cancel arrives.
    RiskGateway a = gateway();
    EXPECT(a.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(a, "X", "e1", 100);
    EXPECT(a.requestCancel("X", "C1") == RejectReason::None);
    EXPECT(a.onExecutionReport({"e2", "C1", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(a.onCancelReject("C1") == ApplyResult::IllegalTransition && a.killed());
    // (b) the cancel was rejected, the order later expired, then the reject is resent.
    RiskGateway b = gateway();
    EXPECT(b.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(b, "X", "e1", 100);
    EXPECT(b.requestCancel("X", "C1") == RejectReason::None);
    EXPECT(b.onCancelReject("C1") == ApplyResult::Applied);
    EXPECT(b.onExecutionReport({"e2", "X", "", ExecType::Expired, OrdStatus::Expired, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(b.onCancelReject("C1") == ApplyResult::Ignored && !b.killed());
    // (c) replace R1 was accepted and superseded by R2; a reject for R1 after the order ended.
    RiskGateway c = gateway();
    EXPECT(c.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(c, "X", "e1", 100);
    EXPECT(c.requestReplace("X", "R1", 200, 5'000, 20 * kMs) == RejectReason::None);
    EXPECT(c.onExecutionReport({"e2", "R1", "X", ExecType::Replaced, OrdStatus::New, 0, 0, 200, 0}) == ApplyResult::Applied);
    EXPECT(c.requestReplace("R1", "R2", 300, 5'000, 40 * kMs) == RejectReason::None);
    EXPECT(c.onExecutionReport({"e3", "R2", "R1", ExecType::Replaced, OrdStatus::New, 0, 0, 300, 0}) == ApplyResult::Applied);
    EXPECT(c.onExecutionReport({"e4", "R2", "", ExecType::Expired, OrdStatus::Expired, 0, 0, 0, 0}) == ApplyResult::Applied);
    EXPECT(!c.killed());
    EXPECT(c.onCancelReject("R1") == ApplyResult::IllegalTransition && c.killed());
    // A report naming a ClOrdID that was never sent for the order, routed by its OrigClOrdID.
    RiskGateway d = gateway();
    EXPECT(d.submit({"X", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(d, "X", "e1", 100);
    EXPECT(d.onExecutionReport({"e2", "Z", "X", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 0}) == ApplyResult::IllegalTransition);
    EXPECT(d.killed() && d.order("X")->status == OrdStatus::New);
}

// ------------------------------------------------------------------ model check
// A venue written independently of the gateway. It works our requests in arrival order, sometimes
// in two phases (a Pending Cancel or Pending Replace ack first, the outcome later), fills, expires
// or cancels orders on its own, sometimes holds an ack back until after a fill, rejects some
// orders and replaces, and replays reports. Each direction of the session is a FIFO queue, and the
// driver interleaves our sends, deliveries in both directions and venue events at random, so
// requests and reports cross on the wire. Oracle: the venue's own book. Legal venue behaviour
// must never trip the kill switch; whenever both queues are empty the gateway must agree with the
// venue on every order, position and exposure; and an injected illegal message must trip it.

struct Mix {  // SplitMix64
    std::uint64_t s;
    std::uint64_t next() {
        std::uint64_t z = (s += 0x9E3779B97F4A7C15ull);
        z = (z ^ (z >> 30)) * 0xBF58476D1CE4E5B9ull;
        z = (z ^ (z >> 27)) * 0x94D049BB133111EBull;
        return z ^ (z >> 31);
    }
    std::int64_t below(std::int64_t n) { return static_cast<std::int64_t>(next() % static_cast<std::uint64_t>(n)); }
    bool chance(int oneIn) { return below(oneIn) == 0; }
};

struct ToVenue {
    char kind;  // 'N' new, 'C' cancel, 'R' replace
    std::string key;
    std::string id;
    std::int64_t qty;
    std::int64_t px;
};

struct ToGateway {
    bool cancelReject;
    ExecReport er;
    std::string rejectId;
};

struct VenueOrder {
    std::string key;
    std::string current;
    std::string symbol;
    Side side;
    std::int64_t qty;
    std::int64_t origQty;
    std::int64_t px;
    std::int64_t cum = 0;
    bool ackOwed = false;
    bool ackSent = false;
    std::optional<OrdStatus> ended;
    std::optional<ToVenue> working;  // a request between its Pending ack and its outcome
    std::deque<ToVenue> backlog;     // requests that arrived while one was being worked
    std::int64_t leaves() const { return ended ? 0 : qty - cum; }
    OrdStatus status() const {
        if (ended) return *ended;
        if (working) return working->kind == 'C' ? OrdStatus::PendingCancel : OrdStatus::PendingReplace;
        return qty == cum ? OrdStatus::Filled : cum > 0 ? OrdStatus::PartiallyFilled : OrdStatus::New;
    }
};

struct ModelStats {
    long steps = 0, reports = 0, implicitAcks = 0, tooLate = 0, twoPhase = 0, unsolicited = 0, replaced = 0, amendedToCum = 0, replays = 0,
         orderRejects = 0, quiesces = 0, faultsCaught = 0;
};

class VenueModel {
public:
    explicit VenueModel(std::uint64_t seed) : rng_{seed} {}
    std::map<std::string, VenueOrder> orders;
    std::deque<ToGateway> out;
    std::vector<ToGateway> sent;  // for replays
    std::map<std::string, std::int64_t> position;
    ModelStats* stats = nullptr;

    void receive(const ToVenue& m) {
        if (m.kind == 'N') {
            VenueOrder& v = orders[m.key];
            v.key = v.current = m.key;
            v.symbol = m.id;
            v.side = m.qty > 0 ? Side::Buy : Side::Sell;
            v.qty = v.origQty = m.qty > 0 ? m.qty : -m.qty;
            v.px = m.px;
            if (rng_.chance(10)) {
                v.ended = OrdStatus::Rejected;
                ++stats->orderRejects;
                report(v, ExecType::Rejected, v.key, "", 0, 0);
            } else if (rng_.chance(4)) {
                v.ackOwed = true;
            } else {
                if (rng_.chance(4)) report(v, ExecType::PendingNew, v.key, "", 0, 0, OrdStatus::PendingNew);
                v.ackSent = true;
                report(v, ExecType::New, v.key, "", 0, 0);
            }
            return;
        }
        VenueOrder& v = orders.at(m.key);
        if (v.working) {
            v.backlog.push_back(m);
            return;
        }
        work(v, m);
    }

    // One spontaneous venue event on a random order.
    void act() {
        if (orders.empty()) return;
        auto it = orders.begin();
        std::advance(it, rng_.below(static_cast<std::int64_t>(orders.size())));
        VenueOrder& v = it->second;
        const std::int64_t r = rng_.below(10);
        if (r < 5) {
            fill(v);
        } else if (r < 7) {
            if (v.working) finishWorking(v);
        } else if (r < 8) {
            flushAck(v);
        } else if (r < 9) {
            if (v.ackSent && !v.ackOwed && !v.ended && v.leaves() > 0 && rng_.chance(3)) {
                v.ended = rng_.chance(2) ? OrdStatus::Expired : OrdStatus::Canceled;
                ++stats->unsolicited;
                report(v, *v.ended == OrdStatus::Expired ? ExecType::Expired : ExecType::Canceled, v.current, "", 0, 0);
            }
        } else if (!sent.empty()) {
            out.push_back(sent[static_cast<std::size_t>(rng_.below(static_cast<std::int64_t>(sent.size())))]);
            ++stats->replays;
        }
    }

    // Works every request to its end, so the venue has nothing pending.
    void settle() {
        for (auto& [key, v] : orders) {
            flushAck(v);
            while (v.working) finishWorking(v);
        }
    }

private:
    Mix rng_;

    void report(VenueOrder& v, ExecType t, const std::string& id, const std::string& orig, std::int64_t lastQty, std::int64_t lastPx,
                std::optional<OrdStatus> status = std::nullopt) {
        ToGateway m{false, {"x" + std::to_string(++execIds_), id, orig, t, status ? *status : v.status(), lastQty, lastPx, v.leaves(), v.cum}, {}};
        out.push_back(m);
        sent.push_back(m);
    }
    void reject(const std::string& id) {
        ToGateway m{true, {}, id};
        out.push_back(m);
        sent.push_back(m);
    }

    void flushAck(VenueOrder& v) {
        if (!v.ackOwed) return;
        v.ackOwed = false;
        v.ackSent = true;
        ToGateway m{false, {"x" + std::to_string(++execIds_), v.key, "", ExecType::New, OrdStatus::New, 0, 0, v.origQty, 0}, {}};
        if (v.cum > 0) ++stats->implicitAcks;
        out.push_back(m);
        sent.push_back(m);
    }

    void fill(VenueOrder& v) {
        if (v.ended || v.leaves() == 0 || !(v.ackSent || v.ackOwed)) return;
        const std::int64_t q = rng_.chance(3) ? v.leaves() : 1 + rng_.below(v.leaves());
        v.cum += q;
        position[v.symbol] += v.side == Side::Buy ? q : -q;
        report(v, ExecType::Trade, v.current, "", q, v.px);
    }

    void work(VenueOrder& v, const ToVenue& m) {
        flushAck(v);
        if (v.ended || v.leaves() == 0 || (m.kind == 'R' && rng_.chance(8))) {
            if (v.ended || v.leaves() == 0) ++stats->tooLate;
            reject(m.id);
            return;
        }
        if (rng_.chance(3)) {
            v.working = m;
            ++stats->twoPhase;
            report(v, m.kind == 'C' ? ExecType::PendingCancel : ExecType::PendingReplace, m.id, v.current, 0, 0);
            return;
        }
        complete(v, m);
    }

    void complete(VenueOrder& v, const ToVenue& m) {
        if (m.kind == 'C') {
            v.ended = OrdStatus::Canceled;
            report(v, ExecType::Canceled, m.id, v.current, 0, 0);
            return;
        }
        const std::string orig = v.current;
        v.qty = std::max(m.qty, v.cum);
        if (v.qty == v.cum) ++stats->amendedToCum;
        v.px = m.px;
        v.current = m.id;
        ++stats->replaced;
        report(v, ExecType::Replaced, m.id, orig, 0, 0);
    }

    void finishWorking(VenueOrder& v) {
        const ToVenue m = *v.working;
        v.working.reset();
        if (v.ended || v.leaves() == 0) {
            ++stats->tooLate;
            reject(m.id);
        } else {
            complete(v, m);
        }
        while (!v.working && !v.backlog.empty()) {
            const ToVenue next = v.backlog.front();
            v.backlog.pop_front();
            work(v, next);
        }
    }

    std::uint64_t execIds_ = 0;
};

RiskLimits wideLimits() {
    RiskLimits l;
    l.maxOrderQty = 1'000'000;
    l.maxOrderNotionalCents = std::int64_t{1} << 50;
    l.priceCollarBps = 1000;
    l.maxAbsPosition = std::int64_t{1} << 40;
    l.creditLimitCents = std::numeric_limits<std::int64_t>::max() - 1;
    l.maxMessagesPerWindow = std::size_t{1} << 30;
    l.throttleWindowNs = 1;
    l.repeatWindowNs = 0;
    return l;
}

// The book invariants that must hold after every message, legal or not.
bool invariantsHold(const RiskGateway& gw, const std::vector<std::string>& keys) {
    for (const std::string& k : keys) {
        const Order* o = gw.order(k);
        if (o == nullptr) continue;
        if (o->cumQty < 0 || o->cumQty > o->orderQty) return false;
        if (isTerminal(o->base) ? o->leavesQty != 0 : o->leavesQty != o->orderQty - o->cumQty) return false;
        if (isTerminal(o->base) && o->worstCaseLeaves() != 0) return false;
    }
    return true;
}

// Runs one session. With fault set, one illegal message is injected at a random step; returns
// false on any disagreement with the model.
bool runSession(std::uint64_t seed, int steps, bool fault, ModelStats& st) {
    Mix rng{seed * 7919 + 1};
    VenueModel venue(seed);
    venue.stats = &st;
    RiskGateway gw(wideLimits());
    const char* symbols[] = {"S", "T"};
    for (const char* sym : symbols) gw.setReferencePrice(sym, 5'000);
    std::deque<ToVenue> toVenue;
    std::vector<std::string> keys;
    std::uint64_t now = 0;
    int ids = 0;
    const int faultAt = fault ? 50 + static_cast<int>(rng.below(steps - 50)) : -1;

    auto deliverToGateway = [&]() -> bool {
        const ToGateway m = venue.out.front();
        venue.out.pop_front();
        ++st.reports;
        const ApplyResult r = m.cancelReject ? gw.onCancelReject(m.rejectId) : gw.onExecutionReport(m.er);
        if (r == ApplyResult::IllegalTransition || r == ApplyResult::Inconsistent || r == ApplyResult::UnknownOrder || gw.killed()) {
            std::cerr << "  model: legal message rejected (" << toString(r) << ") id " << (m.cancelReject ? m.rejectId : m.er.clOrdId)
                      << " type " << static_cast<char>(m.er.execType) << " seed " << seed << std::endl;
            return false;
        }
        return invariantsHold(gw, keys);
    };

    auto quiesce = [&]() -> bool {
        ++st.quiesces;
        do {
            while (!toVenue.empty()) {
                venue.receive(toVenue.front());
                toVenue.pop_front();
            }
            venue.settle();
            while (!venue.out.empty())
                if (!deliverToGateway()) return false;
        } while (!toVenue.empty());
        std::map<std::string, std::int64_t> exposure;
        for (const auto& [key, v] : venue.orders) {
            const Order* o = gw.order(key);
            if (o == nullptr || o->cumQty != v.cum || o->leavesQty != v.leaves() || o->status != v.status() || o->currentClOrdId != v.current)
                return false;
        }
        std::int64_t expectedGross = 0;
        for (const char* sym : symbols) {
            const std::int64_t pos = venue.position[sym];
            if (gw.position(sym) != pos) return false;
            expectedGross += (pos < 0 ? -pos : pos) * 5'000;
            std::int64_t buys = 0, sells = 0;
            for (const auto& [key, v] : venue.orders) {
                if (v.symbol != sym) continue;
                (v.side == Side::Buy ? buys : sells) += v.leaves();
                expectedGross += v.leaves() * v.px;
            }
            if (gw.openQty(sym, Side::Buy) != buys || gw.openQty(sym, Side::Sell) != sells) return false;
        }
        return gw.grossExposureCents() == expectedGross;
    };

    for (int step = 0; step < steps; ++step) {
        ++st.steps;
        now += 1'000;
        if (step == faultAt) {
            // Pick an order and send something no legal venue can send; the kill switch must trip.
            std::vector<const Order*> live, ended, accepted;
            for (const std::string& k : keys) {
                const Order* o = gw.order(k);
                if (!isTerminal(o->base) && o->leavesQty > 0) live.push_back(o);
                if (isTerminal(o->base) && o->base != OrdStatus::Filled) ended.push_back(o);
                if (o->currentClOrdId != o->key) accepted.push_back(o);
            }
            const std::int64_t kind = rng.below(6);
            if (kind == 0 && !live.empty()) {
                const Order* o = live[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(live.size())))];
                (void)gw.onExecutionReport({"bad", o->currentClOrdId, "", ExecType::Trade, OrdStatus::Filled, o->leavesQty + 1, o->priceCents, 0,
                                            o->cumQty + o->leavesQty + 1});
            } else if (kind == 1 && !live.empty()) {
                const Order* o = live[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(live.size())))];
                (void)gw.onExecutionReport({"bad", o->currentClOrdId, "", ExecType::Trade, OrdStatus::PartiallyFilled, 1, o->priceCents,
                                            o->leavesQty - 1, o->cumQty + 2});
            } else if (kind == 2 && !ended.empty()) {
                const Order* o = ended[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(ended.size())))];
                (void)gw.onExecutionReport({"bad", o->currentClOrdId, "", ExecType::Trade, OrdStatus::Filled, 1, o->priceCents, 0, o->cumQty + 1});
            } else if (kind == 3 && !accepted.empty()) {
                (void)gw.onCancelReject(accepted[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(accepted.size())))]->currentClOrdId);
            } else if (kind == 4 && !keys.empty()) {
                (void)gw.onCancelReject(keys[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(keys.size())))]);
            } else {
                (void)gw.onExecutionReport({"bad", "nobody", "", ExecType::New, OrdStatus::New, 0, 0, 1, 0});
            }
            if (!gw.killed()) {
                std::cerr << "  model: injected fault " << kind << " not caught, seed " << seed << std::endl;
                return false;
            }
            ++st.faultsCaught;
            return true;
        }
        const std::int64_t a = rng.below(100);
        if (a < 8) {
            const std::string key = "o" + std::to_string(++ids);
            const char* sym = symbols[rng.below(2)];
            const Side side = rng.chance(2) ? Side::Buy : Side::Sell;
            const std::int64_t qty = 1 + rng.below(200);
            const std::int64_t px = 4'600 + rng.below(800);
            if (gw.submit({key, sym, side, qty, px}, now) != RejectReason::None) return false;
            keys.push_back(key);
            toVenue.push_back({'N', key, sym, side == Side::Buy ? qty : -qty, px});
        } else if (a < 16 && !keys.empty()) {
            const std::string& key = keys[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(keys.size())))];
            const std::string id = "c" + std::to_string(++ids);
            if (gw.requestCancel(key, id) == RejectReason::None) toVenue.push_back({'C', key, id, 0, 0});
        } else if (a < 24 && !keys.empty()) {
            const std::string& key = keys[static_cast<std::size_t>(rng.below(static_cast<std::int64_t>(keys.size())))];
            const std::string id = "r" + std::to_string(++ids);
            const std::int64_t qty = gw.order(key)->cumQty + 1 + rng.below(200);
            const std::int64_t px = 4'600 + rng.below(800);
            if (gw.requestReplace(key, id, qty, px, now) == RejectReason::None) toVenue.push_back({'R', key, id, qty, px});
        } else if (a < 44 && !toVenue.empty()) {
            venue.receive(toVenue.front());
            toVenue.pop_front();
        } else if (a < 70 && !venue.out.empty()) {
            if (!deliverToGateway()) return false;
        } else if (a < 98) {
            venue.act();
        } else if (!fault && !quiesce()) {
            std::cerr << "  model: gateway and venue disagree at rest, seed " << seed << std::endl;
            return false;
        }
    }
    if (fault) return true;
    if (!quiesce()) {
        std::cerr << "  model: gateway and venue disagree at the end, seed " << seed << std::endl;
        return false;
    }
    return !gw.killed() && gw.ignoredResponses() > 0;
}

void test_model_check_against_venue() {
    ModelStats st;
    int failed = 0;
    for (std::uint64_t seed = 1; seed <= 150; ++seed)
        if (!runSession(seed, 2'000, false, st)) ++failed;
    for (std::uint64_t seed = 1001; seed <= 1200; ++seed)
        if (!runSession(seed, 400, true, st)) ++failed;
    std::cout << "  model check: " << st.steps << " steps, " << st.reports << " venue messages, " << st.quiesces << " rest checks, "
              << st.implicitAcks << " implicit acks, " << st.twoPhase << " two-phase requests, " << st.tooLate << " too-late rejects, "
              << st.unsolicited << " unsolicited ends, " << st.replaced << " replaces (" << st.amendedToCum << " amended to CumQty), "
              << st.replays << " replays, " << st.orderRejects << " order rejects, " << st.faultsCaught << "/200 faults caught" << std::endl;
    EXPECT(failed == 0);
    EXPECT(st.faultsCaught == 200);
    EXPECT(st.steps > 300'000);
    // Every race the session is meant to produce actually happened.
    EXPECT(st.implicitAcks > 0 && st.twoPhase > 0 && st.tooLate > 0 && st.unsolicited > 0 && st.replaced > 0 && st.amendedToCum > 0);
    EXPECT(st.replays > 0 && st.orderRejects > 0 && st.quiesces > 150);
}

// After a replace the venue knows the order by its new ClOrdID, so the kill switch cancels that one.
void test_kill_switch_uses_current_clordid() {
    RiskGateway gw = gateway();
    EXPECT(gw.submit({"O", "ABC", Side::Buy, 100, 5'000}, 0) == RejectReason::None);
    ack(gw, "O", "e1", 100);
    EXPECT(gw.requestReplace("O", "R", 200, 5'000, 20 * kMs) == RejectReason::None);
    EXPECT(gw.onExecutionReport({"e2", "R", "O", ExecType::Replaced, OrdStatus::New, 0, 0, 200, 0}) == ApplyResult::Applied);
    const auto cancels = gw.engageKillSwitch("manual");
    EXPECT(cancels.size() == 1 && cancels[0] == "R");
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
    RUN_TEST(test_invalid_reference_keeps_last_valid);
    RUN_TEST(test_held_symbol_without_any_reference_fails_closed);
    RUN_TEST(test_exposure_overflow_fails_closed);
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
    RUN_TEST(test_late_ack_after_fill_is_reconciled);
    RUN_TEST(test_responses_must_match_request_in_flight);
    RUN_TEST(test_kill_switch_uses_current_clordid);
    RUN_TEST(test_contradictory_answers_are_breaks);
    RUN_TEST(test_model_check_against_venue);
    std::cout << "\n" << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
