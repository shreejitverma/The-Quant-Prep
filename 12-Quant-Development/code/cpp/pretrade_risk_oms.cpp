// Demo for 12-Quant-Development/13-Risk-Checks-and-Order-Management.md: a session through the
// pre-trade risk gateway and the order state machine. Every number the note quotes is printed
// and asserted here.
//
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror -pthread -o pretrade_risk_oms pretrade_risk_oms.cpp
// Run:   ./pretrade_risk_oms

#include "pretrade_risk_oms.hpp"

#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <string>

namespace {

int g_failures = 0;

void check(bool ok, const char* what) {
    if (!ok) {
        ++g_failures;
        std::fprintf(stderr, "ASSERTION FAILED: %s\n", what);
    }
}

constexpr std::uint64_t kMs = 1'000'000;  // nanoseconds per millisecond

oms::RejectReason send(oms::RiskGateway& gw, const char* id, const char* sym, oms::Side side, std::int64_t qty, std::int64_t px,
                       std::uint64_t tMs) {
    const oms::RejectReason r = gw.submit({id, sym, side, qty, px}, tMs * kMs);
    std::printf("    t=%6.1f ms  %-4s %-5s %-4s %5lld @ %7.2f  -> %s\n", static_cast<double>(tMs), id, sym,
                side == oms::Side::Buy ? "buy" : "sell", static_cast<long long>(qty), static_cast<double>(px) / 100.0, oms::toString(r));
    return r;
}

oms::ApplyResult report(oms::RiskGateway& gw, const oms::ExecReport& er) {
    const oms::ApplyResult r = gw.onExecutionReport(er);
    const oms::Order* o = gw.order(er.clOrdId);
    std::printf("    ExecID %-3s 150=%c on %-3s last %3lld @ %6.2f -> %-18s status %-15s cum %4lld leaves %4lld\n", er.execId.c_str(),
                static_cast<char>(er.execType), er.clOrdId.c_str(), static_cast<long long>(er.lastQty),
                static_cast<double>(er.lastPxCents) / 100.0, oms::toString(r), o ? oms::toString(o->status) : "-",
                o ? static_cast<long long>(o->cumQty) : 0LL, o ? static_cast<long long>(o->leavesQty) : 0LL);
    return r;
}

}  // namespace

int main() {
    using oms::ExecType;
    using oms::OrdStatus;
    using oms::RejectReason;
    using oms::Side;

    oms::RiskLimits limits;
    limits.maxOrderQty = 1000;
    limits.maxOrderNotionalCents = 8'000'000;  // $80,000
    limits.priceCollarBps = 500;               // 5% around the reference price
    limits.maxAbsPosition = 1500;
    limits.creditLimitCents = 20'000'000;  // $200,000 gross
    limits.maxMessagesPerWindow = 3;
    limits.throttleWindowNs = 1000 * kMs;  // 3 orders per rolling second
    limits.repeatWindowNs = 50 * kMs;

    oms::RiskGateway gw(limits);
    gw.setReferencePrice("XYZ", 10'000);  // $100.00
    gw.restrict("RST");

    std::printf("[1] pre-trade checks (XYZ reference $100.00, collar 5%%)\n");
    const std::int64_t buyCap = 10'000 * (10'000 + limits.priceCollarBps) / 10'000;
    const std::int64_t sellFloor = 10'000 * (10'000 - limits.priceCollarBps) / 10'000;
    std::printf("    collar band: buys up to %.2f, sells down to %.2f\n", static_cast<double>(buyCap) / 100.0,
                static_cast<double>(sellFloor) / 100.0);
    check(buyCap == 10'500 && sellFloor == 9'500, "collar band 105.00 / 95.00");
    check(send(gw, "O1", "XYZ", Side::Buy, 500, 10'000, 0) == RejectReason::None, "O1 accepted");
    check(send(gw, "O1", "XYZ", Side::Buy, 10, 10'000, 0) == RejectReason::DuplicateClOrdId, "duplicate ClOrdID");
    check(send(gw, "O2", "XYZ", Side::Buy, 1200, 10'000, 0) == RejectReason::MaxQuantity, "max qty");
    check(send(gw, "O3", "XYZ", Side::Buy, 100, 10'501, 0) == RejectReason::PriceCollar, "buy collar at 105.01");
    check(send(gw, "O3b", "XYZ", Side::Buy, 100, 10'500, 1) == RejectReason::None, "buy at collar edge 105.00 accepted");
    check(send(gw, "O4", "XYZ", Side::Sell, 100, 9'499, 2) == RejectReason::PriceCollar, "sell collar at 94.99");
    check(send(gw, "O5", "RST", Side::Buy, 10, 5'000, 2) == RejectReason::RestrictedSymbol, "restricted");
    check(send(gw, "O5b", "NOREF", Side::Buy, 10, 5'000, 2) == RejectReason::NoReferencePrice, "no reference fails closed");
    check(send(gw, "O5c", "XYZ", Side::Buy, 900, 10'000, 3) == RejectReason::MaxNotional, "900 x $100 = $90,000 > $80,000");
    check(send(gw, "O6", "XYZ", Side::Buy, 500, 10'000, 10) == RejectReason::RepeatedOrder, "repeat of O1 inside 50 ms");
    check(send(gw, "O7", "XYZ", Side::Buy, 800, 10'000, 100) == RejectReason::None, "O7 accepted, worst-case long 1400");
    const std::int64_t openBuys = gw.openQty("XYZ", Side::Buy);
    std::printf("    open buys after O7: %lld; O8 would make the worst-case long %lld\n", static_cast<long long>(openBuys),
                static_cast<long long>(openBuys + 300));
    check(openBuys == 1400 && openBuys + 300 == 1700, "open buys 500 + 100 + 800, then 1700 with O8");
    check(send(gw, "O8", "XYZ", Side::Buy, 300, 9'900, 150) == RejectReason::PositionLimit, "1400 + 300 > 1500");
    const std::int64_t grossBefore = gw.grossExposureCents();
    std::printf("    gross exposure of open orders: $%.2f\n", static_cast<double>(grossBefore) / 100.0);
    check(grossBefore == 14'050'000, "gross $140,500");
    const std::int64_t o9Notional = 700 * 10'100;
    std::printf("    O9 notional $%.2f, gross with O9 $%.2f\n", static_cast<double>(o9Notional) / 100.0,
                static_cast<double>(grossBefore + o9Notional) / 100.0);
    check(o9Notional == 7'070'000 && grossBefore + o9Notional == 21'120'000, "70,700 and 211,200");
    check(send(gw, "O9", "XYZ", Side::Sell, 700, 10'100, 150) == RejectReason::CreditLimit, "140,500 + 70,700 > 200,000");
    check(send(gw, "O10", "XYZ", Side::Sell, 100, 10'050, 200) == RejectReason::Throttle, "4th order inside 1 s");
    check(send(gw, "O10b", "XYZ", Side::Sell, 100, 10'050, 1000) == RejectReason::None, "O1 slot expired at t = 1000 ms");

    std::printf("[2] execution reports, idempotency and the state machine\n");
    check(report(gw, {"E1", "O1", "", ExecType::New, OrdStatus::New, 0, 0, 500, 0}) == oms::ApplyResult::Applied, "O1 ack");
    check(report(gw, {"E2", "O1", "", ExecType::Trade, OrdStatus::PartiallyFilled, 200, 10'000, 300, 200}) == oms::ApplyResult::Applied,
          "O1 partial");
    check(report(gw, {"E2", "O1", "", ExecType::Trade, OrdStatus::PartiallyFilled, 200, 10'000, 300, 200}) == oms::ApplyResult::Duplicate,
          "replayed E2 ignored");
    check(gw.order("O1")->cumQty == 200, "cum unchanged by duplicate");
    check(report(gw, {"E3", "O1", "", ExecType::Trade, OrdStatus::Filled, 300, 9'998, 0, 500}) == oms::ApplyResult::Applied, "O1 filled");
    const double avgPx = gw.order("O1")->avgPx();
    std::printf("    O1 AvgPx (tag 6) = %.3f, XYZ position %lld\n", avgPx, static_cast<long long>(gw.position("XYZ")));
    check(std::fabs(avgPx - 99.988) < 1e-9, "avg px 99.988");
    check(gw.position("XYZ") == 500, "position 500");

    // Cancel O7, but 100 shares fill while the cancel is pending: the fill must be booked.
    check(report(gw, {"E4", "O7", "", ExecType::New, OrdStatus::New, 0, 0, 800, 0}) == oms::ApplyResult::Applied, "O7 ack");
    check(gw.requestCancel("O7", "C7") == RejectReason::None, "cancel sent");
    check(gw.order("O7")->status == OrdStatus::PendingCancel, "pending cancel");
    check(report(gw, {"E5", "O7", "", ExecType::Trade, OrdStatus::PendingCancel, 100, 10'000, 700, 100}) == oms::ApplyResult::Applied,
          "fill during pending cancel");
    check(report(gw, {"E6", "C7", "O7", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 100}) == oms::ApplyResult::Applied, "O7 canceled");
    check(gw.position("XYZ") == 600, "position 600 after the racing fill");

    // Replace O3b: 100 @ 105.00 -> 300 @ 104.00, risk-checked on the worst case of old and new.
    check(report(gw, {"E7", "O3b", "", ExecType::New, OrdStatus::New, 0, 0, 100, 0}) == oms::ApplyResult::Applied, "O3b ack");
    check(gw.requestReplace("O3b", "R3", 300, 10'400, 1500 * kMs) == RejectReason::None, "replace accepted");
    // While the replace is in flight, either 100 @ 105.00 or 300 @ 104.00 could trade: count the worst of each.
    const std::int64_t worstLong = gw.position("XYZ") + gw.openQty("XYZ", Side::Buy);
    const std::int64_t grossDuring = gw.grossExposureCents();
    std::printf("    during replace: worst-case long %lld, gross exposure $%.2f\n", static_cast<long long>(worstLong),
                static_cast<double>(grossDuring) / 100.0);
    check(worstLong == 900, "600 + max(100, 300)");
    check(grossDuring == 10'155'000, "600 x 100 + 100 x 100.50 + 300 x 105.00 = $101,550");
    check(report(gw, {"E8", "R3", "O3b", ExecType::Replaced, OrdStatus::New, 0, 0, 300, 0}) == oms::ApplyResult::Applied, "replaced");
    const oms::Order* o3 = gw.order("R3");
    std::printf("    O3b after replace: ClOrdID %s qty %lld price %.2f status %s\n", o3->currentClOrdId.c_str(),
                static_cast<long long>(o3->orderQty), static_cast<double>(o3->priceCents) / 100.0, oms::toString(o3->status));
    check(o3->orderQty == 300 && o3->priceCents == 10'400 && o3->status == OrdStatus::New, "replace applied");

    std::printf("[3] an impossible report trips the kill switch\n");
    check(report(gw, {"E9", "O1", "", ExecType::Canceled, OrdStatus::Canceled, 0, 0, 0, 500}) == oms::ApplyResult::IllegalTransition,
          "cancel of a filled order is illegal");
    const auto cancels = gw.engageKillSwitch("operator confirm");
    std::printf("    kill switch %s (%s); cancels to send: %zu", gw.killed() ? "ON" : "off", gw.killReason().c_str(), cancels.size());
    for (const auto& k : cancels) std::printf(" %s", k.c_str());
    std::printf("\n");
    check(gw.killed(), "kill switch engaged automatically");
    check(cancels.size() == 2 && cancels[0] == "O10b" && cancels[1] == "O3b", "two live orders to cancel");
    check(send(gw, "O11", "XYZ", Side::Sell, 10, 10'000, 2000) == RejectReason::KillSwitch, "new orders blocked");
    check(gw.requestCancel("O3b", "C3") == RejectReason::None, "cancels still allowed under the kill switch");

    std::printf("[4] why limit checks use integer cents\n");
    // A 15% collar on 100.00 should accept a buy at exactly 115.00.
    const volatile double collarFactor = 1.0 + 0.15;  // volatile: keep the computation at run time
    const double floatLimit = 100.0 * collarFactor;
    const bool floatAccepts = 115.00 <= floatLimit;
    const bool intAccepts = std::int64_t{11'500} * 10'000 <= std::int64_t{10'000} * (10'000 + 1'500);
    std::printf("    double: 100.0 * (1 + 0.15) = %.17g -> buy at 115.00 %s\n", floatLimit, floatAccepts ? "accepted" : "rejected");
    std::printf("    integer cents: 11500 * 10000 <= 10000 * 11500 -> buy at 115.00 %s\n", intAccepts ? "accepted" : "rejected");
    check(floatLimit < 115.0 && !floatAccepts, "floating-point collar wrongly rejects the edge");
    check(intAccepts, "integer collar accepts the edge");

    if (g_failures != 0) {
        std::fprintf(stderr, "%d assertion(s) failed\n", g_failures);
        return EXIT_FAILURE;
    }
    std::printf("all assertions passed\n");
    return EXIT_SUCCESS;
}
