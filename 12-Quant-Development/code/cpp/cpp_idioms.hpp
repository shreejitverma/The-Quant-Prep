// Modern C++ idioms for trading systems, used by 02-Cpp-for-Trading-Systems.md.
//
// Each block is small, self-contained and tested in tests/test_cpp_idioms.cpp:
//   1. Fixed-point prices with compile-time parsing and overflow-checked notional.
//   2. Struct layout and padding.
//   3. Move semantics: why a noexcept move constructor matters to std::vector.
//   4. RAII ownership of a resource, including on the exception path.
//   5. Static (CRTP), dynamic (virtual) and closed-set (std::variant) polymorphism.
//   6. Error codes on the hot path: a minimal Expected<T, E> (std::expected is C++23).
//   7. UB-free byte handling: std::bit_cast and memcpy instead of reinterpret_cast.
//   8. Polymorphic memory resources: a stack buffer with zero heap allocations.

#pragma once

#include <array>
#include <bit>
#include <cstddef>
#include <cstdint>
#include <cstring>
#include <memory_resource>
#include <new>
#include <optional>
#include <stdexcept>
#include <string_view>
#include <type_traits>
#include <utility>
#include <variant>
#include <vector>

namespace qpidioms {

// ---------------------------------------------------------------------------------------------
// 1. Fixed-point prices. Binary floating point cannot represent 0.1 exactly, so equality and
// tick arithmetic on doubles drift. Exchanges publish integer prices with an implied scale
// (Nasdaq ITCH "Price (4)" has 4 implied decimals); keep them integer end to end.
// ---------------------------------------------------------------------------------------------
inline constexpr std::int64_t kPriceScale = 10'000;  // 4 implied decimals

struct Price {
    std::int64_t raw;  // price * kPriceScale
    friend constexpr auto operator<=>(Price, Price) = default;
    friend constexpr Price operator+(Price a, Price b) noexcept { return Price{a.raw + b.raw}; }
    friend constexpr Price operator-(Price a, Price b) noexcept { return Price{a.raw - b.raw}; }
};

// Parses "123.45" into Price{1'234'500}. Rejects signs, empty input, more than 4 decimals and
// values that would overflow int64. constexpr, so literals can be validated at compile time.
[[nodiscard]] constexpr std::optional<Price> parse_price(std::string_view s) noexcept {
    if (s.empty()) return std::nullopt;
    std::int64_t whole = 0;
    std::int64_t frac = 0;
    int frac_digits = 0;
    bool seen_dot = false;
    bool any_digit = false;
    for (char ch : s) {
        if (ch == '.') {
            if (seen_dot) return std::nullopt;
            seen_dot = true;
            continue;
        }
        if (ch < '0' || ch > '9') return std::nullopt;
        any_digit = true;
        const int d = ch - '0';
        if (seen_dot) {
            if (++frac_digits > 4) return std::nullopt;
            frac = frac * 10 + d;
        } else {
            if (whole > (INT64_MAX / kPriceScale - d) / 10) return std::nullopt;
            whole = whole * 10 + d;
        }
    }
    if (!any_digit) return std::nullopt;
    for (int i = frac_digits; i < 4; ++i) frac *= 10;
    if (whole == INT64_MAX / kPriceScale && frac > INT64_MAX % kPriceScale) return std::nullopt;
    return Price{whole * kPriceScale + frac};
}

static_assert(parse_price("101.25")->raw == 1'012'500);
static_assert(parse_price("0.0001")->raw == 1);
static_assert(!parse_price("1.23456").has_value());
static_assert(!parse_price("-1").has_value());

// Notional in raw units (price raw * quantity). Returns nullopt instead of overflowing:
// signed overflow is undefined behaviour, not wrap-around.
[[nodiscard]] constexpr std::optional<std::int64_t> checked_notional(Price p, std::int64_t qty) noexcept {
    std::int64_t out = 0;
    if (__builtin_mul_overflow(p.raw, qty, &out)) return std::nullopt;
    return out;
}

// ---------------------------------------------------------------------------------------------
// 2. Layout. Members are laid out in declaration order with padding to each member's alignment;
// ordering by decreasing alignment removes the holes. Values below hold on LP64 targets
// (Linux x86-64, Linux AArch64, macOS arm64).
// ---------------------------------------------------------------------------------------------
struct PaddedQuote {
    bool is_bid;
    double price;
    bool is_firm;
    std::int64_t size;
    bool is_last;
};
struct PackedQuote {
    double price;
    std::int64_t size;
    bool is_bid;
    bool is_firm;
    bool is_last;
};
static_assert(sizeof(PaddedQuote) == 40);
static_assert(sizeof(PackedQuote) == 24);

// ---------------------------------------------------------------------------------------------
// 3. Move semantics. std::vector relocates elements on growth with std::move_if_noexcept: if the
// move constructor may throw and a copy constructor exists, it copies to keep the strong
// exception guarantee. Forgetting noexcept silently turns every relocation into a deep copy.
// ---------------------------------------------------------------------------------------------
struct CopyMoveCounts {
    long copies = 0;
    long moves = 0;
};

template <bool NoexceptMove>
class Tracked {
    CopyMoveCounts* counts_;
    std::int64_t value_;

public:
    Tracked(CopyMoveCounts* counts, std::int64_t value) noexcept : counts_(counts), value_(value) {}
    Tracked(const Tracked& o) : counts_(o.counts_), value_(o.value_) { ++counts_->copies; }
    Tracked(Tracked&& o) noexcept(NoexceptMove) : counts_(o.counts_), value_(o.value_) { ++counts_->moves; }
    Tracked& operator=(const Tracked& o) {
        counts_ = o.counts_;
        value_ = o.value_;
        ++counts_->copies;
        return *this;
    }
    Tracked& operator=(Tracked&& o) noexcept(NoexceptMove) {
        counts_ = o.counts_;
        value_ = o.value_;
        ++counts_->moves;
        return *this;
    }
    ~Tracked() = default;
    [[nodiscard]] std::int64_t value() const noexcept { return value_; }
};

// Appends n elements without reserve() and reports how many copies and moves the growth caused.
template <bool NoexceptMove>
CopyMoveCounts count_growth_relocations(int n, bool reserve_first) {
    CopyMoveCounts counts;
    std::vector<Tracked<NoexceptMove>> v;
    if (reserve_first) v.reserve(static_cast<std::size_t>(n));
    for (int i = 0; i < n; ++i) v.emplace_back(&counts, i);  // constructs in place: no copy or move
    return counts;
}

// ---------------------------------------------------------------------------------------------
// 4. RAII. The handle owns one unit of a counted resource (think socket, mapped file, lock); the
// destructor releases it on every path, including stack unwinding. Move-only: copying an owner
// would double-release.
// ---------------------------------------------------------------------------------------------
struct ResourceLedger {
    int open = 0;
};

class ResourceHandle {
    ResourceLedger* ledger_ = nullptr;

public:
    explicit ResourceHandle(ResourceLedger& ledger) noexcept : ledger_(&ledger) { ++ledger_->open; }
    ~ResourceHandle() {
        if (ledger_ != nullptr) --ledger_->open;
    }
    ResourceHandle(const ResourceHandle&) = delete;
    ResourceHandle& operator=(const ResourceHandle&) = delete;
    ResourceHandle(ResourceHandle&& o) noexcept : ledger_(std::exchange(o.ledger_, nullptr)) {}
    ResourceHandle& operator=(ResourceHandle&& o) noexcept {
        if (this != &o) {
            if (ledger_ != nullptr) --ledger_->open;
            ledger_ = std::exchange(o.ledger_, nullptr);
        }
        return *this;
    }
    [[nodiscard]] bool owns() const noexcept { return ledger_ != nullptr; }
};

// ---------------------------------------------------------------------------------------------
// 5. Three ways to call "the strategy's on_tick".
// ---------------------------------------------------------------------------------------------
struct Tick {
    std::int64_t price;
    std::int64_t qty;
};

// Dynamic: open set of types, one indirect call per message, rarely inlined.
class IStrategy {
public:
    virtual ~IStrategy() = default;
    virtual std::int64_t on_tick(const Tick& t) noexcept = 0;

protected:
    IStrategy() = default;
    IStrategy(const IStrategy&) = default;
    IStrategy& operator=(const IStrategy&) = default;
};

class MomentumVirtual final : public IStrategy {
    std::int64_t last_ = 0;

public:
    std::int64_t on_tick(const Tick& t) noexcept override {
        const std::int64_t signal = t.price - last_;
        last_ = t.price;
        return signal;
    }
};

class MeanReversionVirtual final : public IStrategy {
    std::int64_t ema_ = 0;

public:
    std::int64_t on_tick(const Tick& t) noexcept override {
        ema_ += (t.price - ema_) / 8;
        return ema_ - t.price;
    }
};

// Static (CRTP): the base calls the derived implementation through a static_cast, resolved at
// compile time, so the call inlines. The price: one type per instantiation, no heterogeneous container.
template <typename Derived>
class StrategyBase {
public:
    std::int64_t on_tick(const Tick& t) noexcept { return static_cast<Derived*>(this)->on_tick_impl(t); }
};

class MomentumCrtp : public StrategyBase<MomentumCrtp> {
    std::int64_t last_ = 0;

public:
    std::int64_t on_tick_impl(const Tick& t) noexcept {
        const std::int64_t signal = t.price - last_;
        last_ = t.price;
        return signal;
    }
};

class MeanReversionCrtp : public StrategyBase<MeanReversionCrtp> {
    std::int64_t ema_ = 0;

public:
    std::int64_t on_tick_impl(const Tick& t) noexcept {
        ema_ += (t.price - ema_) / 8;
        return ema_ - t.price;
    }
};

// Closed set: std::variant stores any of the alternatives inline (no heap) and std::visit
// dispatches with a jump table or compare chain the optimiser can see through.
using AnyStrategy = std::variant<MomentumCrtp, MeanReversionCrtp>;

inline std::int64_t on_tick(AnyStrategy& s, const Tick& t) noexcept {
    return std::visit([&t](auto& strat) noexcept { return strat.on_tick(t); }, s);
}

// Message handling over a closed set of message types, with the "overloaded" visitor idiom.
struct AddOrderMsg {
    std::uint64_t id;
    std::int64_t price;
    std::int64_t qty;
};
struct CancelOrderMsg {
    std::uint64_t id;
};
struct TradeMsg {
    std::int64_t price;
    std::int64_t qty;
};
using Message = std::variant<AddOrderMsg, CancelOrderMsg, TradeMsg>;

template <typename... Fs>
struct Overloaded : Fs... {
    using Fs::operator()...;
};
template <typename... Fs>
Overloaded(Fs...) -> Overloaded<Fs...>;

struct FlowStats {
    std::int64_t adds = 0;
    std::int64_t cancels = 0;
    std::int64_t traded_qty = 0;
    std::int64_t traded_notional = 0;
};

inline void apply(FlowStats& s, const Message& m) noexcept {
    std::visit(Overloaded{
                   [&s](const AddOrderMsg&) noexcept { ++s.adds; },
                   [&s](const CancelOrderMsg&) noexcept { ++s.cancels; },
                   [&s](const TradeMsg& t) noexcept {
                       s.traded_qty += t.qty;
                       s.traded_notional += t.price * t.qty;
                   },
               },
               m);
}

// ---------------------------------------------------------------------------------------------
// 6. Errors without exceptions. A throw costs a heap allocation for the exception object plus
// table-driven unwinding (microseconds); an error code costs a compare and a branch.
// ---------------------------------------------------------------------------------------------
enum class OrderError : std::uint8_t { BadQuantity, BadPrice, NotionalLimit };

template <typename T, typename E>
class [[nodiscard]] Expected {
    std::variant<T, E> v_;

public:
    constexpr Expected(T value) noexcept(std::is_nothrow_move_constructible_v<T>) : v_(std::in_place_index<0>, std::move(value)) {}
    static constexpr Expected failure(E e) noexcept { return Expected(std::in_place_index<1>, e); }
    [[nodiscard]] constexpr bool has_value() const noexcept { return v_.index() == 0; }
    [[nodiscard]] constexpr const T& value() const { return std::get<0>(v_); }
    [[nodiscard]] constexpr E error() const { return std::get<1>(v_); }

private:
    constexpr Expected(std::in_place_index_t<1>, E e) noexcept : v_(std::in_place_index<1>, e) {}
};

// Returns the order notional in raw price units, or why the order is rejected.
constexpr Expected<std::int64_t, OrderError> validate_order(Price px, std::int64_t qty, std::int64_t max_notional) noexcept {
    if (qty <= 0) return Expected<std::int64_t, OrderError>::failure(OrderError::BadQuantity);
    if (px.raw <= 0) return Expected<std::int64_t, OrderError>::failure(OrderError::BadPrice);
    const auto notional = checked_notional(px, qty);
    if (!notional || *notional > max_notional) return Expected<std::int64_t, OrderError>::failure(OrderError::NotionalLimit);
    return *notional;
}

// The same check reporting failure by exception, for the cost comparison in dispatch_bench.cpp.
inline std::int64_t validate_order_or_throw(Price px, std::int64_t qty, std::int64_t max_notional) {
    const auto r = validate_order(px, qty, max_notional);
    if (!r.has_value()) throw std::invalid_argument("order rejected");
    return r.value();
}

// ---------------------------------------------------------------------------------------------
// 7. Bytes without undefined behaviour. Reading a uint32 through reinterpret_cast<const
// uint32_t*>(buf + 1) breaks alignment and strict aliasing; memcpy compiles to a single load.
// ---------------------------------------------------------------------------------------------
inline std::uint32_t load_be32(const unsigned char* p) noexcept {
    std::uint32_t v;
    std::memcpy(&v, p, sizeof v);
    if constexpr (std::endian::native == std::endian::little) v = __builtin_bswap32(v);
    return v;
}

constexpr std::uint64_t double_bits(double x) noexcept { return std::bit_cast<std::uint64_t>(x); }
static_assert(double_bits(1.0) == 0x3FF0000000000000ULL);

// ---------------------------------------------------------------------------------------------
// 8. Allocators. std::pmr containers take a memory_resource at run time; a monotonic buffer over
// a stack array serves allocations by bumping a pointer and frees everything at scope exit.
// The counting upstream proves whether the heap was touched.
// ---------------------------------------------------------------------------------------------
class CountingResource final : public std::pmr::memory_resource {
    std::pmr::memory_resource* upstream_;

public:
    long allocations = 0;
    explicit CountingResource(std::pmr::memory_resource* upstream = std::pmr::new_delete_resource()) noexcept : upstream_(upstream) {}

private:
    void* do_allocate(std::size_t bytes, std::size_t align) override {
        ++allocations;
        return upstream_->allocate(bytes, align);
    }
    void do_deallocate(void* p, std::size_t bytes, std::size_t align) override { upstream_->deallocate(p, bytes, align); }
    bool do_is_equal(const std::pmr::memory_resource& o) const noexcept override { return this == &o; }
};

// Fills a pmr::vector with n int64 values from a 4 KiB stack buffer; returns heap allocations made.
inline long pmr_heap_allocations(std::size_t n) {
    CountingResource heap;
    std::array<std::byte, 4096> buffer{};
    std::pmr::monotonic_buffer_resource arena(buffer.data(), buffer.size(), &heap);
    std::pmr::vector<std::int64_t> v(&arena);
    v.reserve(n);
    for (std::size_t i = 0; i < n; ++i) v.push_back(static_cast<std::int64_t>(i));
    return heap.allocations;
}

}  // namespace qpidioms
