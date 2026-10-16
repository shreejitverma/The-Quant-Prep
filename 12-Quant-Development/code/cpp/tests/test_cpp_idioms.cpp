// Unit tests for cpp_idioms.hpp (02-Cpp-for-Trading-Systems.md). Framework-free; exits non-zero on failure.

#include "cpp_idioms.hpp"

#include <cstdint>
#include <iostream>
#include <limits>
#include <stdexcept>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                                            \
    do {                                                                                        \
        ++g_total;                                                                              \
        if (!(cond)) {                                                                          \
            ++g_failures;                                                                       \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__ << " -> " #cond << std::endl; \
        }                                                                                       \
    } while (0)

using namespace qpidioms;

void test_parse_price() {
    EXPECT(parse_price("101.25")->raw == 1'012'500);
    EXPECT(parse_price("101")->raw == 1'010'000);
    EXPECT(parse_price("0.5")->raw == 5'000);
    EXPECT(parse_price(".5")->raw == 5'000);
    EXPECT(parse_price("7.")->raw == 70'000);
    EXPECT(!parse_price("").has_value());
    EXPECT(!parse_price(".").has_value());
    EXPECT(!parse_price("1.2.3").has_value());
    EXPECT(!parse_price("12a").has_value());
    EXPECT(!parse_price("1.00001").has_value());
    // Largest representable: INT64_MAX raw = 922337203685477.5807
    EXPECT(parse_price("922337203685477.5807")->raw == std::numeric_limits<std::int64_t>::max());
    EXPECT(!parse_price("922337203685477.5808").has_value());
    EXPECT(!parse_price("9223372036854775807").has_value());
}

void test_checked_notional() {
    EXPECT(checked_notional(Price{1'012'500}, 300).value() == 303'750'000);
    EXPECT(checked_notional(Price{-5}, 3).value() == -15);
    EXPECT(!checked_notional(Price{2'000'000'000}, 4'611'686'019LL).has_value());
    EXPECT(checked_notional(Price{2'000'000'000}, 4'611'686'018LL).has_value());
}

void test_relocations() {
    const auto nx = count_growth_relocations<true>(1000, false);
    EXPECT(nx.copies == 0);
    EXPECT(nx.moves == 1023);
    const auto mx = count_growth_relocations<false>(1000, false);
    EXPECT(mx.copies == 1023);
    EXPECT(mx.moves == 0);
    const auto rx = count_growth_relocations<false>(1000, true);
    EXPECT(rx.copies == 0 && rx.moves == 0);
}

void test_raii_releases_on_every_path() {
    ResourceLedger ledger;
    {
        ResourceHandle a(ledger);
        ResourceHandle b(ledger);
        EXPECT(ledger.open == 2);
        ResourceHandle c(std::move(a));  // ownership moves, count unchanged
        EXPECT(ledger.open == 2);
        EXPECT(!a.owns() && c.owns());  // NOLINT(bugprone-use-after-move): moved-from state is specified here
        b = std::move(c);               // b releases its own unit, takes c's
        EXPECT(ledger.open == 1);
    }
    EXPECT(ledger.open == 0);
    try {
        ResourceHandle h(ledger);
        EXPECT(ledger.open == 1);
        throw std::runtime_error("venue disconnected");
    } catch (const std::runtime_error&) {
        EXPECT(ledger.open == 0);  // released during unwinding, before the handler runs
    }
}

void test_dispatch_styles_agree() {
    const Tick ticks[] = {{100, 1}, {104, 1}, {96, 1}, {120, 1}};
    MomentumVirtual mv;
    MomentumCrtp mc;
    AnyStrategy av = MomentumCrtp{};
    MeanReversionVirtual rv;
    MeanReversionCrtp rc;
    AnyStrategy ar = MeanReversionCrtp{};
    for (const auto& t : ticks) {
        const auto a = mv.on_tick(t);
        EXPECT(a == mc.on_tick(t));
        EXPECT(a == on_tick(av, t));
        const auto b = rv.on_tick(t);
        EXPECT(b == rc.on_tick(t));
        EXPECT(b == on_tick(ar, t));
    }
}

void test_flow_stats() {
    FlowStats s;
    apply(s, AddOrderMsg{1, 10, 5});
    apply(s, TradeMsg{10, 3});
    apply(s, TradeMsg{11, 2});
    apply(s, CancelOrderMsg{1});
    EXPECT(s.adds == 1 && s.cancels == 1 && s.traded_qty == 5 && s.traded_notional == 52);
}

void test_validate_order() {
    EXPECT(validate_order(Price{1'000'000}, 10, 1'000'000'000).value() == 10'000'000);
    EXPECT(validate_order(Price{1'000'000}, 0, 1'000'000'000).error() == OrderError::BadQuantity);
    EXPECT(validate_order(Price{0}, 1, 1'000'000'000).error() == OrderError::BadPrice);
    EXPECT(validate_order(Price{1'000'000}, 2'000, 1'000'000'000).error() == OrderError::NotionalLimit);
    EXPECT(validate_order(Price{2'000'000'000}, 5'000'000'000LL, std::numeric_limits<std::int64_t>::max()).error() ==
           OrderError::NotionalLimit);  // overflow is a rejection, not a wrap-around
    bool threw = false;
    try {
        (void)validate_order_or_throw(Price{1}, -1, 10);
    } catch (const std::invalid_argument&) {
        threw = true;
    }
    EXPECT(threw);
}

void test_bytes() {
    const unsigned char buf[] = {0xFF, 0x01, 0x02, 0x03, 0x04};
    EXPECT(load_be32(buf + 1) == 0x01020304u);  // unaligned source is fine with memcpy
    EXPECT(double_bits(-0.0) == 0x8000000000000000ULL);
}

void test_pmr() {
    EXPECT(pmr_heap_allocations(100) == 0);
    EXPECT(pmr_heap_allocations(1000) == 1);  // one upstream block for the reserved 8000 bytes
}

}  // namespace

int main() {
    test_parse_price();
    test_checked_notional();
    test_relocations();
    test_raii_releases_on_every_path();
    test_dispatch_styles_agree();
    test_flow_stats();
    test_validate_order();
    test_bytes();
    test_pmr();
    std::cout << (g_total - g_failures) << "/" << g_total << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
