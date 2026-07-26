// Unit tests for the pure parsing logic used by the mock UDP market data
// receiver (06_quantitative_development/cpp_low_latency/examples/udp_receiver_mock.cpp).
//
// These tests focus on:
//   * Packet parsing: exact-size buffers, larger buffers, field extraction,
//     struct packing guarantees.
//   * Error handling: null buffer, undersized buffer, zero-length buffer,
//     invalid message type.
//
// The tests are intentionally framework-free so they can be compiled and run
// in CI with nothing more than a C++17 toolchain. See the CI workflow for the
// exact g++ invocation used.

#include "udp_receiver_mock.hpp"

#include <cstdint>
#include <cstring>
#include <iostream>
#include <string>

namespace {

int g_failures = 0;
int g_total = 0;

#define EXPECT(cond)                                                            \
    do {                                                                        \
        ++g_total;                                                              \
        if (!(cond)) {                                                          \
            ++g_failures;                                                       \
            std::cerr << "  FAIL: " << __FILE__ << ":" << __LINE__              \
                      << " -> " #cond << std::endl;                             \
        }                                                                       \
    } while (0)

#define RUN_TEST(fn)                                                            \
    do {                                                                        \
        std::cout << "[RUN ] " #fn << std::endl;                                \
        int before = g_failures;                                                \
        fn();                                                                   \
        if (g_failures == before) {                                             \
            std::cout << "[ OK ] " #fn << std::endl;                            \
        } else {                                                                \
            std::cout << "[FAIL] " #fn << std::endl;                            \
        }                                                                       \
    } while (0)

// Helper: serialize a MarketUpdate into a byte buffer the same way the
// sender side would write it on the wire.
void encode(const MarketUpdate& in, char* out) {
    std::memcpy(out, &in, sizeof(MarketUpdate));
}

// ---------------------------------------------------------------------------
// Packet parsing
// ---------------------------------------------------------------------------

void test_struct_is_wire_packed() {
    // If padding ever sneaks back in, every downstream parser breaks.
    EXPECT(sizeof(MarketUpdate) == 13);
}

void test_parses_add_message() {
    MarketUpdate src{};
    src.msg_type = 'A';
    src.symbol_id = 4242u;
    src.price = 1'234'500u;   // 123.45
    src.quantity = 100u;

    char buf[sizeof(MarketUpdate)] = {};
    encode(src, buf);

    MarketUpdate out{};
    ParseStatus status = parse_market_update(buf, sizeof(buf), out);

    EXPECT(status == ParseStatus::Ok);
    EXPECT(out.msg_type == 'A');
    EXPECT(out.symbol_id == 4242u);
    EXPECT(out.price == 1'234'500u);
    EXPECT(out.quantity == 100u);
}

void test_parses_execute_message() {
    MarketUpdate src{};
    src.msg_type = 'E';
    src.symbol_id = 0u;             // boundary: min value
    src.price = 0xFFFFFFFFu;        // boundary: max uint32
    src.quantity = 1u;

    char buf[sizeof(MarketUpdate)] = {};
    encode(src, buf);

    MarketUpdate out{};
    ParseStatus status = parse_market_update(buf, sizeof(buf), out);

    EXPECT(status == ParseStatus::Ok);
    EXPECT(out.msg_type == 'E');
    EXPECT(out.symbol_id == 0u);
    EXPECT(out.price == 0xFFFFFFFFu);
    EXPECT(out.quantity == 1u);
}

void test_exact_size_boundary_is_ok() {
    // n == sizeof(MarketUpdate) is the smallest legal buffer.
    MarketUpdate src{};
    src.msg_type = 'A';
    src.symbol_id = 1u;
    src.price = 2u;
    src.quantity = 3u;

    char buf[sizeof(MarketUpdate)] = {};
    encode(src, buf);

    MarketUpdate out{};
    EXPECT(parse_market_update(buf, sizeof(MarketUpdate), out) == ParseStatus::Ok);
    EXPECT(out.symbol_id == 1u);
    EXPECT(out.price == 2u);
    EXPECT(out.quantity == 3u);
}

void test_accepts_larger_buffer_and_ignores_trailing_bytes() {
    // UDP datagrams may legitimately be larger than a single MarketUpdate
    // (e.g., a batch framing prefix or trailing padding). The parser must
    // pull off the first record and ignore the rest.
    MarketUpdate src{};
    src.msg_type = 'A';
    src.symbol_id = 99u;
    src.price = 50000u;
    src.quantity = 7u;

    constexpr std::size_t kExtra = 32;
    char buf[sizeof(MarketUpdate) + kExtra] = {};
    encode(src, buf);
    // Fill trailing bytes with garbage that must NOT be read.
    for (std::size_t i = sizeof(MarketUpdate); i < sizeof(buf); ++i) {
        buf[i] = static_cast<char>(0xAB);
    }

    MarketUpdate out{};
    ParseStatus status = parse_market_update(buf, sizeof(buf), out);

    EXPECT(status == ParseStatus::Ok);
    EXPECT(out.msg_type == 'A');
    EXPECT(out.symbol_id == 99u);
    EXPECT(out.price == 50000u);
    EXPECT(out.quantity == 7u);
}

void test_handles_unaligned_buffer() {
    // Incoming socket buffers are byte-aligned. Using memcpy internally
    // means parsing must succeed even when the source pointer is not
    // aligned to alignof(uint32_t).
    MarketUpdate src{};
    src.msg_type = 'E';
    src.symbol_id = 0xDEADBEEFu;
    src.price = 0x01020304u;
    src.quantity = 0x0A0B0C0Du;

    // Allocate sizeof(MarketUpdate) + 1 and start one byte in to force
    // misalignment relative to uint32_t.
    char raw[sizeof(MarketUpdate) + 1] = {};
    char* unaligned = raw + 1;
    encode(src, unaligned);

    MarketUpdate out{};
    ParseStatus status =
        parse_market_update(unaligned, sizeof(MarketUpdate), out);

    EXPECT(status == ParseStatus::Ok);
    EXPECT(out.msg_type == 'E');
    EXPECT(out.symbol_id == 0xDEADBEEFu);
    EXPECT(out.price == 0x01020304u);
    EXPECT(out.quantity == 0x0A0B0C0Du);
}

// ---------------------------------------------------------------------------
// Error handling
// ---------------------------------------------------------------------------

void test_rejects_null_buffer() {
    MarketUpdate out{};
    EXPECT(parse_market_update(nullptr, 64, out) == ParseStatus::NullBuffer);
    // Null buffer must be detected before any size check.
    EXPECT(parse_market_update(nullptr, 0, out) == ParseStatus::NullBuffer);
}

void test_rejects_zero_length_buffer() {
    char buf[sizeof(MarketUpdate)] = {};
    MarketUpdate out{};
    EXPECT(parse_market_update(buf, 0, out) == ParseStatus::BufferTooSmall);
}

void test_rejects_buffer_just_below_size() {
    // Off-by-one guard: sizeof(MarketUpdate) - 1 must be rejected.
    MarketUpdate src{};
    src.msg_type = 'A';
    src.symbol_id = 1u;
    src.price = 2u;
    src.quantity = 3u;

    char buf[sizeof(MarketUpdate)] = {};
    encode(src, buf);

    MarketUpdate out{};
    ParseStatus status =
        parse_market_update(buf, sizeof(MarketUpdate) - 1, out);
    EXPECT(status == ParseStatus::BufferTooSmall);
}

void test_rejects_invalid_msg_type() {
    // Only 'A' and 'E' are documented as supported in udp_receiver_mock.cpp.
    const char kBadTypes[] = {'\0', 'X', 'a', 'e', '1', static_cast<char>(0xFF)};
    for (char bad : kBadTypes) {
        MarketUpdate src{};
        src.msg_type = bad;
        src.symbol_id = 1u;
        src.price = 2u;
        src.quantity = 3u;

        char buf[sizeof(MarketUpdate)] = {};
        encode(src, buf);

        MarketUpdate out{};
        ParseStatus status = parse_market_update(buf, sizeof(buf), out);
        EXPECT(status == ParseStatus::InvalidMsgType);
    }
}

void test_invalid_msg_type_check_runs_after_size_check() {
    // A buffer that is simultaneously too small AND whose first byte is an
    // invalid msg_type must surface the more fundamental size error.
    char buf[1] = {'X'};
    MarketUpdate out{};
    EXPECT(parse_market_update(buf, sizeof(buf), out) ==
           ParseStatus::BufferTooSmall);
}

void test_parse_does_not_mutate_out_on_size_error() {
    // Callers should be able to rely on `out` being untouched when the
    // parser rejects a datagram for being too small.
    char buf[sizeof(MarketUpdate)] = {};
    MarketUpdate out{};
    out.msg_type = 'Z';
    out.symbol_id = 0xAAAAAAAAu;
    out.price = 0xBBBBBBBBu;
    out.quantity = 0xCCCCCCCCu;

    ParseStatus status = parse_market_update(buf, 1, out);
    EXPECT(status == ParseStatus::BufferTooSmall);
    EXPECT(out.msg_type == 'Z');
    EXPECT(out.symbol_id == 0xAAAAAAAAu);
    EXPECT(out.price == 0xBBBBBBBBu);
    EXPECT(out.quantity == 0xCCCCCCCCu);
}

}  // namespace

int main() {
    RUN_TEST(test_struct_is_wire_packed);
    RUN_TEST(test_parses_add_message);
    RUN_TEST(test_parses_execute_message);
    RUN_TEST(test_exact_size_boundary_is_ok);
    RUN_TEST(test_accepts_larger_buffer_and_ignores_trailing_bytes);
    RUN_TEST(test_handles_unaligned_buffer);
    RUN_TEST(test_rejects_null_buffer);
    RUN_TEST(test_rejects_zero_length_buffer);
    RUN_TEST(test_rejects_buffer_just_below_size);
    RUN_TEST(test_rejects_invalid_msg_type);
    RUN_TEST(test_invalid_msg_type_check_runs_after_size_check);
    RUN_TEST(test_parse_does_not_mutate_out_on_size_error);

    std::cout << "\n" << (g_total - g_failures) << "/" << g_total
              << " assertions passed" << std::endl;
    return g_failures == 0 ? 0 : 1;
}
