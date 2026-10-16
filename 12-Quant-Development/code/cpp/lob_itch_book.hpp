// Order-by-order book building from Nasdaq TotalView-ITCH 5.0 messages, for
// 07-Order-Book-and-Matching-Engine.md. Field offsets and lengths follow the ITCH 5.0
// specification in ../../protocol-specs/ (section 4.3 Add Order, 4.4 Modify Order messages):
//
//   'A' Add Order (no MPID)        36 bytes: ref@11 u64, side@19, shares@20 u32, stock@24 8B, price@32 u32
//   'F' Add Order (MPID)           40 bytes: as 'A' plus attribution@36 4B
//   'E' Order Executed             31 bytes: ref@11, executed shares@19 u32, match number@23 u64
//   'C' Order Executed With Price  36 bytes: as 'E' plus printable@31, execution price@32 u32
//   'X' Order Cancel               23 bytes: ref@11, cancelled shares@19 u32
//   'D' Order Delete               19 bytes: ref@11
//   'U' Order Replace              35 bytes: original ref@11, new ref@19, shares@27 u32, price@31 u32
//
// Every message starts with type@0, stock locate@1 u16, tracking number@3 u16, timestamp@5 u48
// (nanoseconds since midnight). Integers are big-endian; prices are Price(4), 4 implied decimals.
// Modify messages carry only the order reference, so the builder must remember each order's side
// and price from its Add; executed, cancelled and deleted shares are subtracted from that order.
// Messages arrive framed as [u16 big-endian length][message] blocks (the MoldUDP64 message block
// layout); unknown message types are skipped using the length, which is what makes the format
// forward compatible.

#pragma once

#include <cstddef>
#include <cstdint>
#include <functional>
#include <map>
#include <unordered_map>
#include <vector>

namespace lob::itch {

inline std::uint64_t be(const std::uint8_t* p, int bytes) noexcept {
    std::uint64_t v = 0;
    for (int i = 0; i < bytes; ++i) v = (v << 8) | p[i];
    return v;
}

inline void put_be(std::vector<std::uint8_t>& out, std::uint64_t v, int bytes) {
    for (int i = bytes - 1; i >= 0; --i) out.push_back(static_cast<std::uint8_t>(v >> (8 * i)));
}

enum class Status : std::uint8_t { Ok, Skipped, Truncated, UnknownOrder, DuplicateOrder, Overfill, BadSide };

[[nodiscard]] constexpr std::size_t message_length(char type) noexcept {
    switch (type) {
        case 'A': return 36;
        case 'F': return 40;
        case 'E': return 31;
        case 'C': return 36;
        case 'X': return 23;
        case 'D': return 19;
        case 'U': return 35;
        default: return 0;  // not a book message: skipped
    }
}

class BookBuilder {
    struct Resting {
        bool buy;
        std::uint32_t price;
        std::uint32_t shares;
    };
    std::uint16_t locate_;
    std::unordered_map<std::uint64_t, Resting> orders_;
    std::map<std::uint32_t, std::uint64_t, std::greater<>> bids_;  // price -> displayed shares, best first
    std::map<std::uint32_t, std::uint64_t> asks_;

    template <typename LevelMap>
    static void bump(LevelMap& side, std::uint32_t price, std::int64_t delta) {
        auto it = side.try_emplace(price, 0).first;
        it->second = static_cast<std::uint64_t>(static_cast<std::int64_t>(it->second) + delta);
        if (it->second == 0) side.erase(it);
    }
    void level_add(bool buy, std::uint32_t price, std::int64_t delta) {
        if (buy)
            bump(bids_, price, delta);
        else
            bump(asks_, price, delta);
    }

    Status add(std::uint64_t ref, char side, std::uint32_t shares, std::uint32_t price) {
        if (side != 'B' && side != 'S') return Status::BadSide;
        if (!orders_.try_emplace(ref, Resting{side == 'B', price, shares}).second) return Status::DuplicateOrder;
        level_add(side == 'B', price, shares);
        return Status::Ok;
    }

    // Executions, partial cancels and deletes all shrink an existing order.
    Status reduce(std::uint64_t ref, std::uint32_t shares, bool delete_all) {
        const auto it = orders_.find(ref);
        if (it == orders_.end()) return Status::UnknownOrder;
        Resting& r = it->second;
        const std::uint32_t take = delete_all ? r.shares : shares;
        if (take > r.shares) return Status::Overfill;
        level_add(r.buy, r.price, -static_cast<std::int64_t>(take));
        r.shares -= take;
        if (r.shares == 0) orders_.erase(it);
        return Status::Ok;
    }

public:
    std::uint64_t applied = 0;
    std::uint64_t skipped = 0;
    std::uint64_t errors = 0;

    explicit BookBuilder(std::uint16_t stock_locate) : locate_(stock_locate) {}

    // Applies one unframed message of n bytes.
    Status apply(const std::uint8_t* p, std::size_t n) {
        if (n < 1) return Status::Truncated;
        const char type = static_cast<char>(p[0]);
        const std::size_t need = message_length(type);
        if (need == 0) {
            ++skipped;
            return Status::Skipped;
        }
        if (n < need) return Status::Truncated;
        if (be(p + 1, 2) != locate_) {
            ++skipped;
            return Status::Skipped;
        }
        Status s = Status::Ok;
        switch (type) {
            case 'A':
            case 'F':
                s = add(be(p + 11, 8), static_cast<char>(p[19]), static_cast<std::uint32_t>(be(p + 20, 4)),
                        static_cast<std::uint32_t>(be(p + 32, 4)));
                break;
            case 'E':
            case 'C':
                s = reduce(be(p + 11, 8), static_cast<std::uint32_t>(be(p + 19, 4)), false);
                break;
            case 'X':
                s = reduce(be(p + 11, 8), static_cast<std::uint32_t>(be(p + 19, 4)), false);
                break;
            case 'D':
                s = reduce(be(p + 11, 8), 0, true);
                break;
            case 'U': {
                // Replace: the old order disappears entirely; the new reference inherits its side.
                const auto it = orders_.find(be(p + 11, 8));
                if (it == orders_.end()) {
                    s = Status::UnknownOrder;
                    break;
                }
                const char side = it->second.buy ? 'B' : 'S';
                s = reduce(be(p + 11, 8), 0, true);
                if (s == Status::Ok)
                    s = add(be(p + 19, 8), side, static_cast<std::uint32_t>(be(p + 27, 4)), static_cast<std::uint32_t>(be(p + 31, 4)));
                break;
            }
            default:
                break;
        }
        if (s == Status::Ok)
            ++applied;
        else
            ++errors;
        return s;
    }

    // Applies a buffer of [u16 length][message] blocks; stops at the first truncated block.
    Status apply_stream(const std::uint8_t* p, std::size_t n) {
        std::size_t off = 0;
        while (off < n) {
            if (n - off < 2) return Status::Truncated;
            const auto len = static_cast<std::size_t>(be(p + off, 2));
            if (n - off - 2 < len) return Status::Truncated;
            const Status s = apply(p + off + 2, len);
            if (s == Status::Truncated) return s;
            off += 2 + len;
        }
        return Status::Ok;
    }

    [[nodiscard]] std::uint64_t bid_shares(std::uint32_t price) const {
        const auto it = bids_.find(price);
        return it == bids_.end() ? 0 : it->second;
    }
    [[nodiscard]] std::uint64_t ask_shares(std::uint32_t price) const {
        const auto it = asks_.find(price);
        return it == asks_.end() ? 0 : it->second;
    }
    [[nodiscard]] std::uint32_t best_bid() const { return bids_.empty() ? 0 : bids_.begin()->first; }
    [[nodiscard]] std::uint32_t best_ask() const { return asks_.empty() ? 0 : asks_.begin()->first; }
    [[nodiscard]] std::size_t live_orders() const { return orders_.size(); }
};

// ------------------------------------------------------------------ encoders (tests, demos, replay tools)
inline void header(std::vector<std::uint8_t>& m, char type, std::uint16_t locate, std::uint64_t ts_ns) {
    m.push_back(static_cast<std::uint8_t>(type));
    put_be(m, locate, 2);
    put_be(m, 0, 2);  // tracking number
    put_be(m, ts_ns, 6);
}

inline std::vector<std::uint8_t> encode_add(std::uint16_t locate, std::uint64_t ts, std::uint64_t ref, char side, std::uint32_t shares,
                                            const char (&stock)[9], std::uint32_t price) {
    std::vector<std::uint8_t> m;
    header(m, 'A', locate, ts);
    put_be(m, ref, 8);
    m.push_back(static_cast<std::uint8_t>(side));
    put_be(m, shares, 4);
    for (int i = 0; i < 8; ++i) m.push_back(static_cast<std::uint8_t>(stock[i]));
    put_be(m, price, 4);
    return m;
}

inline std::vector<std::uint8_t> encode_executed(std::uint16_t locate, std::uint64_t ts, std::uint64_t ref, std::uint32_t shares,
                                                 std::uint64_t match) {
    std::vector<std::uint8_t> m;
    header(m, 'E', locate, ts);
    put_be(m, ref, 8);
    put_be(m, shares, 4);
    put_be(m, match, 8);
    return m;
}

inline std::vector<std::uint8_t> encode_cancel(std::uint16_t locate, std::uint64_t ts, std::uint64_t ref, std::uint32_t shares) {
    std::vector<std::uint8_t> m;
    header(m, 'X', locate, ts);
    put_be(m, ref, 8);
    put_be(m, shares, 4);
    return m;
}

inline std::vector<std::uint8_t> encode_delete(std::uint16_t locate, std::uint64_t ts, std::uint64_t ref) {
    std::vector<std::uint8_t> m;
    header(m, 'D', locate, ts);
    put_be(m, ref, 8);
    return m;
}

inline std::vector<std::uint8_t> encode_replace(std::uint16_t locate, std::uint64_t ts, std::uint64_t old_ref, std::uint64_t new_ref,
                                                std::uint32_t shares, std::uint32_t price) {
    std::vector<std::uint8_t> m;
    header(m, 'U', locate, ts);
    put_be(m, old_ref, 8);
    put_be(m, new_ref, 8);
    put_be(m, shares, 4);
    put_be(m, price, 4);
    return m;
}

// Appends one message as a [u16 length][message] block.
inline void frame(std::vector<std::uint8_t>& stream, const std::vector<std::uint8_t>& msg) {
    put_be(stream, msg.size(), 2);
    stream.insert(stream.end(), msg.begin(), msg.end());
}

}  // namespace lob::itch
