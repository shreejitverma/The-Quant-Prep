// Prints and checks every number quoted in 02-Cpp-for-Trading-Systems.md (worked examples).
// Build: clang++ -std=c++20 -O2 -Wall -Wextra -Wpedantic -Werror cpp_idioms_demo.cpp

#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <limits>
#include <optional>

#include "cpp_idioms.hpp"

namespace {

int g_failures = 0;

void check(bool ok, const char* what) {
    if (!ok) {
        ++g_failures;
        std::printf("CHECK FAILED: %s\n", what);
    }
}

// True when `v` printed with `fmt` is exactly the literal the note quotes.
bool prints_as(double v, const char* fmt, const char* literal) {
    char buf[64];
    std::snprintf(buf, sizeof buf, fmt, v);
    return std::strcmp(buf, literal) == 0;
}

}  // namespace

int main() {
    using namespace qpidioms;

    // Floating-point prices drift; integer ticks do not.
    const double sum = 0.1 + 0.2;
    std::printf("0.1 + 0.2 == 0.3 ? %s, difference %.6e\n", sum == 0.3 ? "true" : "false", sum - 0.3);
    check(sum - 0.3 == 0x1p-54 && prints_as(sum - 0.3, "%.6e", "5.551115e-17"), "0.1 + 0.2 - 0.3 = 2^-54 = 5.551115e-17");
    double px = 100.0;
    for (int i = 0; i < 1000; ++i) px += 0.01;  // walk up 1000 ticks of 0.01
    std::printf("100.0 + 1000 x 0.01 in double = %.15f (exact 110), error %.3e\n", px, px - 110.0);
    check(prints_as(px, "%.15f", "110.000000000005116") && prints_as(px - 110.0, "%.3e", "5.116e-12"),
          "accumulated double drift: 110.000000000005116, error 5.116e-12");
    Price ip = *parse_price("100");
    const Price tick = *parse_price("0.01");
    for (int i = 0; i < 1000; ++i) ip = ip + tick;
    std::printf("100.0000 + 1000 x 0.0100 in fixed point = raw %lld (exact 1100000)\n", static_cast<long long>(ip.raw));
    check(ip.raw == 1'100'000, "fixed point is exact");

    // Overflow-checked notional: the ITCH Price(4) maximum is 200,000.0000 = raw 2,000,000,000.
    const Price max_px = *parse_price("200000");
    const std::int64_t max_qty = std::numeric_limits<std::int64_t>::max() / max_px.raw;
    std::printf("max price raw %lld, largest qty without int64 overflow %lld\n", static_cast<long long>(max_px.raw),
                static_cast<long long>(max_qty));
    check(max_px.raw == 2'000'000'000, "ITCH maximum price 200,000.0000 is raw 2,000,000,000");
    check(max_qty == 4'611'686'018LL, "overflow threshold");
    check(checked_notional(max_px, max_qty).has_value(), "at threshold fits");
    check(!checked_notional(max_px, max_qty + 1).has_value(), "one more overflows");
    // ITCH share counts are 4-byte unsigned, so a single feed-bounded product always fits in int64.
    const std::int64_t itch_max_shares = std::numeric_limits<std::uint32_t>::max();
    const auto itch_max_notional = checked_notional(max_px, itch_max_shares);
    std::printf("max ITCH shares %lld, max single notional raw %lld\n", static_cast<long long>(itch_max_shares),
                static_cast<long long>(itch_max_notional.value_or(-1)));
    check(itch_max_shares < max_qty, "ITCH quantity is below the overflow threshold");
    check(itch_max_notional == std::optional<std::int64_t>{8'589'934'590'000'000'000LL}, "max ITCH notional");

    // Layout.
    std::printf("sizeof(PaddedQuote) = %zu, sizeof(PackedQuote) = %zu\n", sizeof(PaddedQuote), sizeof(PackedQuote));
    check(sizeof(PaddedQuote) == 40 && sizeof(PackedQuote) == 24, "layout sizes");
    const std::size_t data_bytes = sizeof(double) + sizeof(std::int64_t) + 3 * sizeof(bool);
    std::printf("data bytes in either layout = %zu (the rest is padding)\n", data_bytes);
    check(data_bytes == 19, "19 bytes of data");

    // Vector growth relocations for 1000 emplace_backs.
    const auto nx = count_growth_relocations<true>(1000, false);
    const auto mx = count_growth_relocations<false>(1000, false);
    const auto rx = count_growth_relocations<true>(1000, true);
    std::printf("noexcept move: copies %ld moves %ld | throwing move: copies %ld moves %ld | reserved: copies %ld moves %ld\n",
                nx.copies, nx.moves, mx.copies, mx.moves, rx.copies, rx.moves);
    // libstdc++ and libc++ both double capacity from 1, so relocations are 1 + 2 + ... + 512 = 1023.
    check(nx.copies == 0 && nx.moves == 1023, "noexcept move relocations");
    check(mx.copies == 1023 && mx.moves == 0, "throwing move falls back to copies");
    check(rx.copies == 0 && rx.moves == 0, "reserve avoids relocation");

    // pmr: 100 int64 (800 bytes) fit in the 4 KiB stack buffer; 1000 (8000 bytes) do not.
    const long small = pmr_heap_allocations(100);
    const long large = pmr_heap_allocations(1000);
    std::printf("pmr heap allocations: 100 elements -> %ld, 1000 elements -> %ld\n", small, large);
    check(small == 0, "small vector served from the stack buffer");
    check(large == 1, "large vector spills to the upstream resource once");

    // Error codes.
    const auto ok = validate_order(*parse_price("101.25"), 300, 1'000'000'000);
    const auto bad = validate_order(*parse_price("101.25"), 0, 1'000'000'000);
    std::printf("validate 300 @ 101.25: notional raw %lld; qty 0 -> error %d\n", static_cast<long long>(ok.value()),
                static_cast<int>(bad.error()));
    check(ok.has_value() && ok.value() == 303'750'000, "notional 300 x 101.25 = 30375.0000");
    check(!bad.has_value() && bad.error() == OrderError::BadQuantity, "zero quantity rejected");

    // Message dispatch over a variant.
    FlowStats stats;
    const Message msgs[] = {AddOrderMsg{1, 1'012'500, 100}, AddOrderMsg{2, 1'012'600, 200}, CancelOrderMsg{1}, TradeMsg{1'012'600, 50}};
    for (const auto& m : msgs) apply(stats, m);
    std::printf("flow: adds %lld cancels %lld traded qty %lld notional raw %lld\n", static_cast<long long>(stats.adds),
                static_cast<long long>(stats.cancels), static_cast<long long>(stats.traded_qty), static_cast<long long>(stats.traded_notional));
    check(stats.adds == 2 && stats.cancels == 1 && stats.traded_qty == 50 && stats.traded_notional == 50'630'000, "flow stats");

    std::printf("%s\n", g_failures == 0 ? "all checks passed" : "CHECKS FAILED");
    return g_failures == 0 ? EXIT_SUCCESS : EXIT_FAILURE;
}
