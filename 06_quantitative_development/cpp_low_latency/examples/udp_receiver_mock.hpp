#ifndef QUANT_PREP_UDP_RECEIVER_MOCK_HPP
#define QUANT_PREP_UDP_RECEIVER_MOCK_HPP

#include <cstdint>
#include <cstddef>
#include <cstring>

/**
 * Shared types and pure-logic helpers for the mock UDP market data
 * receiver. Splitting these out of udp_receiver_mock.cpp lets us unit
 * test packet parsing and error handling without opening real sockets.
 */

#pragma pack(push, 1)
struct MarketUpdate {
    char msg_type;       // 'A' for Add, 'E' for Execute
    uint32_t symbol_id;
    uint32_t price;      // Fixed point (price / 10000.0 -> display)
    uint32_t quantity;
};
#pragma pack(pop)

static_assert(sizeof(MarketUpdate) == 13,
              "MarketUpdate must remain wire-packed (1 + 4 + 4 + 4 bytes)");

/**
 * Result of attempting to parse a raw UDP datagram into a MarketUpdate.
 */
enum class ParseStatus {
    Ok = 0,
    NullBuffer,       // buffer pointer was nullptr
    BufferTooSmall,   // n < sizeof(MarketUpdate)
    InvalidMsgType,   // msg_type is not one of the supported codes
};

/**
 * Validate a raw datagram and, on success, populate `out` with the
 * parsed MarketUpdate. Uses memcpy instead of reinterpret_cast to
 * avoid strict aliasing / alignment undefined behavior when the
 * caller hands us an unaligned byte buffer.
 *
 * Only 'A' (Add) and 'E' (Execute) message types are accepted, matching
 * the comment in udp_receiver_mock.cpp.
 */
inline ParseStatus parse_market_update(const char* buffer,
                                       std::size_t n,
                                       MarketUpdate& out) {
    if (buffer == nullptr) {
        return ParseStatus::NullBuffer;
    }
    if (n < sizeof(MarketUpdate)) {
        return ParseStatus::BufferTooSmall;
    }
    std::memcpy(&out, buffer, sizeof(MarketUpdate));
    if (out.msg_type != 'A' && out.msg_type != 'E') {
        return ParseStatus::InvalidMsgType;
    }
    return ParseStatus::Ok;
}

#endif  // QUANT_PREP_UDP_RECEIVER_MOCK_HPP
