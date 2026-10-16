---
type: concept
track: [quant-dev]
tier: core
status: solid
prereqs: [quant-developer-role-and-stack]
est_hours: 8
sources: [Stroustrup - A Tour of C++ 3rd ed (Addison-Wesley 2022), Meyers - Effective Modern C++ (O'Reilly 2014) items 23-30 and 41, Josuttis - C++ Move Semantics - The Complete Guide (2020), Joshi - C++ Design Patterns and Derivatives Pricing 2nd ed (Cambridge 2008), Stroustrup and Sutter - C++ Core Guidelines (isocpp.github.io), ISO/IEC 14882:2020 (C++20) [basic.life] [intro.races] [expr.pre], Fog - Optimizing software in C++ (agner.org), Cook - When a Microsecond Is an Eternity (CppCon 2017), Regehr - A Guide to Undefined Behavior in C and C++ (blog 2010), Lattner - What Every C Programmer Should Know About Undefined Behavior (LLVM blog 2011), GCC manual - -fdevirtualize-speculatively]
---

# C++ for Trading Systems

## TL;DR

- Split the code into a hot path (per message, per order) and a cold path (startup, configuration, tooling); the hot path allows no allocation, no exceptions thrown, no blocking I/O and no unpredictable indirect calls, while the cold path follows ordinary modern C++.
- Ownership is expressed in types: values and RAII by default, `unique_ptr` for owning pointers, raw pointers and references only to observe; mark move operations `noexcept` or `std::vector` will copy instead of move (measured below: 1023 copies for 1000 appends).
- Choose polymorphism by the shape of the set: CRTP or plain templates when the type is known at compile time, `std::variant` for a closed set, `virtual` for an open set off the hot path; measure, because the compiler may devirtualize for you.
- Prices are integers with an implied scale, never `double`; check `price * qty` for overflow, because signed overflow is undefined behaviour, not wrap-around.
- Undefined behaviour is the main C++ risk in production: know the catalogue (signed overflow, out-of-bounds, dangling references, strict aliasing, data races, uninitialised reads) and run ASan, UBSan and TSan in CI.

## Learning objectives

- Write modern C++ with clear ownership, RAII and no undefined behaviour.
- Use templates, constexpr and CRTP where they remove runtime cost.
- Answer C++ language questions asked at HFT firms (memory model, move semantics, virtual dispatch cost).
- Represent prices and quantities safely and lay out structs deliberately.
- Choose between exceptions and error codes per path, and explain the cost of each.
- Use allocators (`std::pmr`, pools) to make a steady state allocation-free.

## Core concepts

### Hot path and cold path

A trading process spends almost all its life waiting for the next message and must then react in microseconds.
The code that runs per message is the hot path; everything else is cold.
The rules differ, and good codebases mark the boundary explicitly.

| Concern | Cold path (C++ Core Guidelines as written) | Hot path override | Why |
| :--- | :--- | :--- | :--- |
| Memory | `std::vector`, `std::string`, smart pointers freely | Preallocate at startup; pools, arenas, fixed-capacity containers | `malloc` has data-dependent latency and can take locks |
| Errors | Exceptions | Error codes or `expected`-style results, `noexcept` entry points | A throw costs microseconds (measured below) and is unpredictable |
| Polymorphism | `virtual`, `std::function` | Templates, CRTP, `std::variant` over a closed set | Indirect calls block inlining and can mispredict |
| I/O and logging | Synchronous is fine | Push a POD record to a queue drained by another thread | Formatting and I/O cost microseconds |
| Containers | `std::map`, `std::unordered_map` | Flat or open-addressing maps sized at startup, arrays indexed by id | Node-based containers allocate and chase pointers |

### Value semantics, RAII and the rule of zero

C++ objects are values: copying an object copies its state, and its destructor runs deterministically at scope exit.
RAII ties every resource (memory, file descriptor, socket, lock, mapped region) to an object whose destructor releases it, so release happens on every path, including stack unwinding.
The rule of zero: a class that owns resources only through members (vectors, `unique_ptr`, handles) declares none of the five special members, and the compiler-generated ones are correct.
The rule of five: if you write any of destructor, copy constructor, copy assignment, move constructor or move assignment, write or delete all five.
A raw `T*` or `T&` never owns; ownership transfer is a `unique_ptr` by value.
`shared_ptr` is for genuinely shared lifetimes on the cold path: each copy is an atomic increment, and the last owner decides where the destructor runs.

The repo's `ResourceHandle` in [cpp_idioms.hpp](code/cpp/cpp_idioms.hpp) is a move-only RAII handle; its test throws while holding a handle and checks the resource was released before the `catch` block runs.

### Move semantics

An rvalue reference `T&&` binds to temporaries and to objects cast with `std::move`.
`std::move` does not move anything: it is a cast to an rvalue reference that permits a move constructor or move assignment to be chosen.
A moved-from object is in a valid but unspecified state; only assign to it or destroy it.

The detail interviews probe: `std::vector` relocates its elements when it grows, and it uses `std::move_if_noexcept`.
If the move constructor is not `noexcept` and a copy constructor exists, the vector copies, to keep the strong exception guarantee (if a move threw halfway, the old buffer would be half-moved and unrecoverable).
For 1000 `emplace_back` calls without `reserve`, capacity doubles from 1 in both libstdc++ and libc++, so growth relocates $1 + 2 + 4 + \dots + 512 = 1023$ elements.

| Element type | Copies | Moves |
| :--- | ---: | ---: |
| `noexcept` move constructor | 0 | 1023 |
| move constructor that may throw | 1023 | 0 |
| either, after `reserve(1000)` | 0 | 0 |

These counts are printed and asserted by [cpp_idioms_demo.cpp](code/cpp/cpp_idioms_demo.cpp) under both Clang (libc++) and GCC (libstdc++).
Pass sink parameters by value and move them in; return by value and rely on copy elision (guaranteed for prvalues since C++17).

### Templates, CRTP, variant and virtual dispatch

There are three ways to call "the strategy's `on_tick`":

- `virtual`: an open set of types; each call loads the vtable pointer, loads the function pointer and makes an indirect call that usually cannot be inlined.
- CRTP (curiously recurring template pattern): `class Momentum : public StrategyBase<Momentum>`; the base calls `static_cast<Derived*>(this)->on_tick_impl()`, resolved at compile time and inlined; the price is that you lose heterogeneous containers.
- `std::variant<A, B>` plus `std::visit`: a closed set stored inline (no heap), dispatched by an index the optimiser can see; good for message types.

Cost depends on prediction: an indirect call whose target never changes is predicted almost perfectly; one whose target changes randomly mispredicts often.
Measured by [dispatch_bench.cpp](code/cpp/dispatch_bench.cpp) (4096 strategy objects, median of 31 repetitions, one run on an Apple M3 Pro under macOS, Apple clang 21 at `-O2`; machine-dependent):

| Dispatch | ns per call |
| :--- | ---: |
| CRTP, one type (inlined) | 0.21 |
| `virtual`, every object the same type | 0.86 |
| `virtual`, two types in random order | 5.01 |
| `std::variant`, two types in random order | 4.48 |
| `std::variant`, same objects sorted by type | 0.87 |

The lesson is the prediction, not the keyword: sorting the same variants by type cut the cost from 4.48 to 0.87 ns.
The same source built with GCC 16 measured 1.17 ns for the random virtual case, because GCC enables `-fdevirtualize-speculatively` at `-O2` and, seeing two `final` implementations in the translation unit, turns the indirect call into compares and inlined bodies; rebuilt with `-fno-devirtualize-speculatively` it measured 4.60 ns.
Read the assembly (Compiler Explorer, `objdump -d`) before arguing about virtual dispatch.

### constexpr and compile-time work

`constexpr` functions run at compile time when given constant arguments; `consteval` functions must.
Use them to validate configuration and literals and to build lookup tables in read-only data.
`parse_price("101.25")` in [cpp_idioms.hpp](code/cpp/cpp_idioms.hpp) is `constexpr`, so `static_assert(parse_price("101.25")->raw == 1'012'500)` fails the build if parsing is wrong; [compile_time_greeks.cpp](code/cpp/compile_time_greeks.cpp) builds a normal CDF table entirely at compile time.
Templates with concepts (`requires`) state constraints in the signature, and give readable errors instead of instantiation backtraces.

### Prices are integers

Binary floating point cannot represent 0.01 exactly.
`0.1 + 0.2 == 0.3` is false (the difference is `5.551115e-17`), and adding 0.01 one thousand times to 100.0 gives `110.000000000005116`, an error of `5.116e-12`.
Exchanges publish integer prices with an implied scale: Nasdaq ITCH 5.0 "Price (4)" fields carry 4 implied decimal places, with a maximum of 200,000.0000.
Keep prices as `int64_t` ticks end to end, convert to decimal only for display, and compare with `==` safely.
Notional is `price * qty`: with the ITCH maximum price (raw 2,000,000,000), the largest quantity that does not overflow `int64_t` is 4,611,686,018, so any product above that is undefined behaviour unless checked (`__builtin_mul_overflow`, or a wider type).

### Layout, padding and the ABI

Members are laid out in declaration order, each aligned to its own alignment, and the struct is padded to a multiple of its largest alignment.
`{bool, double, bool, int64_t, bool}` occupies 40 bytes; reordered as `{double, int64_t, bool, bool, bool}` it occupies 24 (asserted with `static_assert` on LP64 targets).
On the hot path, put fields used together in the same cache line, split cold fields out, and keep data written by different threads on different lines (see [Low-Latency Engineering](03-Low-Latency-Engineering.md)).

The ABI (application binary interface) fixes layout, calling convention and name mangling between separately compiled code.
Small trivially copyable structs (up to 16 bytes) are passed in registers by the x86-64 System V and AArch64 calling conventions; a type with a non-trivial copy constructor or destructor is passed by hidden reference.
ABI breaks happen: libstdc++ changed `std::string` and `std::list` in GCC 5 and kept both versions behind `_GLIBCXX_USE_CXX11_ABI`, so mixing binaries built with different settings fails at link time.
Inlining needs the definition visible at the call site: put hot small functions in headers, or use link-time optimisation (`-flto`).

### Errors: exceptions versus error codes

Exceptions are zero-cost when not thrown on modern ABIs (table-based unwinding), but a throw allocates the exception object and walks unwind tables.
Measured by [dispatch_bench.cpp](code/cpp/dispatch_bench.cpp) on the same machine (machine- and OS-dependent): a failed validation returned as an error code cost 0.33 ns per call, a throw and catch cost about 14,700 ns.
On the hot path return an `expected`-style result (`std::expected` in C++23; the repo's minimal `Expected<T, E>` for C++20) marked `[[nodiscard]]`, and make entry points `noexcept`.
Exceptions remain the right tool on the cold path, where a constructor that cannot establish its invariant should throw.
Some firms compile hot translation units with `-fno-exceptions`; then every allocation failure and container error must be designed for explicitly.

### Allocators

`std::pmr` containers take a `memory_resource*` at run time, so one container type can draw from different arenas.
A `monotonic_buffer_resource` over a stack array serves allocations by bumping a pointer and frees everything at once.
In [cpp_idioms.hpp](code/cpp/cpp_idioms.hpp), a `pmr::vector<int64_t>` of 100 elements (800 bytes) in a 4 KiB stack buffer made 0 heap allocations, while 1000 elements (8000 bytes) made 1, counted by an upstream resource that intercepts every heap request.
Fixed-size object pools and arenas are covered in [Concurrency, Lock-Free Queues and Memory Pools](04-Concurrency-Lock-Free-and-Memory-Pools.md).

### Undefined behaviour catalogue

Undefined behaviour means the standard places no requirement on the program; optimisers assume it never happens and transform code accordingly.

| UB | Typical trading-code form | Safe alternative |
| :--- | :--- | :--- |
| Signed overflow | `price * qty` on large values | Checked multiply, wider type, proven bounds |
| Out-of-bounds access | Indexing a level array by an unvalidated price | Validate inputs at the boundary; `at()` in cold code |
| Dangling reference or view | `std::string_view` into a temporary; reference into a vector across `push_back` | Own the data; never hold references across invalidating operations |
| Use after free | Callback captures `this` of a destroyed object | Clear ownership; cancel callbacks in the destructor |
| Strict aliasing and misalignment | `*reinterpret_cast<const uint32_t*>(buf + 1)` on a packet | `std::memcpy` or `std::bit_cast` (compiles to one load) |
| Data race | Two threads touch a non-atomic counter | `std::atomic` with a stated order, or a mutex |
| Uninitialised read | A struct field left unset on one code path | Default member initialisers |
| Shift past width | `1 << 32` on a 32-bit int | Use `uint64_t{1} << n` with `n < 64` |

ASan finds memory errors, UBSan finds overflow, bad shifts and misaligned access, and TSan finds data races; every C++ example in this section runs clean under all three.

## Worked examples

### Why does `std::vector<Order>` copy when it grows?

"My `Order` has a user-declared move constructor, but profiling shows copies on `push_back`."
The move constructor is not `noexcept`, so `std::vector` uses `move_if_noexcept` and copies to keep the strong guarantee.
With 1000 appends and no `reserve`, that is 1023 copies instead of 1023 moves; with `reserve(1000)` it is 0 of either.
Fix: declare the move operations `noexcept` (or `= default` them so the compiler deduces it), and `reserve` at startup on the hot path.

### Pricing the cost of a virtual call

"Is a virtual call expensive?"
It depends on prediction and inlining, so measure the case you have.
With one dynamic type the indirect branch is always predicted: 0.86 ns per call on the M3 Pro, against 0.21 ns for the inlined CRTP version.
With two types in random order it measured 5.01 ns, because the predictor cannot guess the target.
The fix is often data layout, not language features: sorting the objects by type brought a variant dispatch from 4.48 to 0.87 ns.

### Floating-point drift in a price ladder

"Generate the 1000 price levels above 100.00 in steps of 0.01."
In `double`, the top level is `110.000000000005116`, not 110, so a hash lookup or `==` comparison against 110.00 fails.
In integer ticks with scale $10^4$, the top level is exactly `1100000`.

### Will this notional overflow?

"Price is ITCH Price(4) as `int64_t`, quantity is `int64_t`. When can `price * qty` overflow?"
The maximum price is 200,000.0000, raw $2 \times 10^9$, so overflow needs $q > \lfloor (2^{63} - 1) / (2 \times 10^9) \rfloor = 4{,}611{,}686{,}018$.
That is unreachable for one equity order, but sums of notionals over a day, or products of raw prices with raw prices, overflow far sooner; check or widen.

### Shrinking a struct by reordering

`{bool is_bid; double price; bool is_firm; int64_t size; bool is_last;}` is 40 bytes: each `bool` is followed by 7 bytes of padding before an 8-byte member, and the tail is padded to 8.
Ordering by decreasing alignment gives 8 + 8 + 3 = 19 bytes of data, padded to 24.

## Pitfalls

- Using `std::move` on a `const` object: the move constructor cannot bind, so it silently copies.
- Returning `std::move(local)`: it disables copy elision; return the local by name.
- Forgetting `noexcept` on move operations, and on destructors of types used in containers.
- Storing `std::string_view` or `std::span` members that outlive the buffer they view.
- Keeping an iterator or reference into a `std::vector` or `std::unordered_map` across an insertion that can reallocate or rehash.
- Comparing prices as `double`, or converting a decimal string to `double` and back.
- Believing `volatile` gives atomicity or ordering; it does neither in C++.
- Benchmarking at `-O0`, or letting the optimiser delete the code under test; keep results alive and check the assembly.
- Calling a virtual function from a constructor or destructor: it dispatches to the class being constructed, not the derived one.
- Throwing from a destructor, which calls `std::terminate` during unwinding.

## Interview questions

> [!question]- qd-cpp-std-move-does | What does `std::move` actually do?
> Nothing at run time: it is a `static_cast` to `T&&`, which lets overload resolution pick a move constructor or move assignment. The move, if any, happens in that function.

> [!question]- qd-cpp-noexcept-vector | Why should move constructors be `noexcept`, and what happens if they are not?
> `std::vector` relocates with `move_if_noexcept`: a throwing move with an available copy constructor makes it copy, to keep the strong exception guarantee. Measured here: 1000 appends cost 1023 copies instead of 1023 moves.

> [!question]- qd-cpp-relocations-count | A vector grows by doubling from capacity 1. How many element relocations do 1000 `push_back` calls cause?
> 1023. Reallocations happen when size reaches 1, 2, 4, ..., 512, moving that many elements each time: $2^{10} - 1 = 1023$. `reserve(1000)` makes it 0.

> [!question]- qd-cpp-rule-of-five | State the rule of zero and the rule of five.
> Zero: if members manage all resources, declare no special members and the defaults are correct. Five: if you declare any of destructor, copy constructor, copy assignment, move constructor or move assignment, declare or delete all five.

> [!question]- qd-cpp-raii | What is RAII and why does it matter for a trading process?
> Resource acquisition is initialisation: a resource is owned by an object whose destructor releases it, so release happens on every exit path including exceptions. Sockets, locks, mapped files and pool slots cannot leak or double-release.

> [!question]- qd-cpp-crtp | What is CRTP and what does it buy over virtual functions?
> `class D : public Base<D>`; the base calls `static_cast<D*>(this)->impl()`. Dispatch is resolved at compile time, so calls inline and nothing is predicted at run time. You lose run-time heterogeneity: no `vector<Base*>` of mixed types.

> [!question]- qd-cpp-virtual-cost | When is a virtual call expensive?
> When the target is unpredictable (mixed types in random order) and when it blocks inlining of a small function in a hot loop. A monomorphic virtual call is cheap. Measured on an M3 Pro: 0.86 ns monomorphic vs 5.01 ns with two random types vs 0.21 ns for CRTP.

> [!question]- qd-cpp-variant-vs-virtual | When would you use `std::variant` instead of a class hierarchy?
> For a closed set of alternatives known at compile time, such as message types: the value is stored inline without heap allocation, `std::visit` dispatch is visible to the optimiser, and adding a type forces every visitor to handle it.

> [!question]- qd-cpp-devirtualization | Your virtual-call benchmark is fast with GCC and slow with Clang. Why might that be?
> GCC enables speculative devirtualization at `-O2`: with few known implementations it compares the vtable pointer and inlines each body. Measured here: 1.17 ns with GCC, 4.60 ns with `-fno-devirtualize-speculatively`. Read the assembly before concluding anything.

> [!question]- qd-cpp-fixed-point | Why not store prices as `double`?
> Decimal ticks like 0.01 are not representable in binary, so arithmetic drifts (1000 additions of 0.01 to 100.0 give an error of `5.116e-12`) and equality and hashing break. Use integer ticks with an implied scale, like ITCH Price(4).

> [!question]- qd-cpp-overflow-threshold | Prices are int64 with 4 implied decimals, maximum 200,000.0000. Above what quantity does `price * qty` overflow?
> 4,611,686,018: $\lfloor (2^{63}-1) / (2 \times 10^9) \rfloor$. Signed overflow is undefined behaviour, so check with `__builtin_mul_overflow` or prove the bound.

> [!question]- qd-cpp-padding | What is `sizeof` of `struct {bool a; double b; bool c; int64_t d; bool e;}` on x86-64 Linux, and how do you shrink it?
> 40 bytes: each bool is padded to 8 before an 8-byte member and the tail pads to 8. Reordering largest-first gives 19 bytes of data padded to 24.

> [!question]- qd-cpp-exceptions-hot-path | Why avoid throwing exceptions on the hot path if they are "zero cost"?
> Zero cost applies only when nothing is thrown. A throw allocates and unwinds through tables: measured here at about 14,700 ns per throw and catch on macOS, versus 0.33 ns for an error code. Use `expected`-style results and `noexcept` entry points.

> [!question]- qd-cpp-strict-aliasing | How do you read a big-endian `uint32_t` at an unaligned offset of a packet buffer without UB?
> `std::memcpy` into a `uint32_t` and byte-swap (or assemble from bytes). `reinterpret_cast` to `uint32_t*` violates alignment and strict aliasing; `memcpy` compiles to a single load anyway.

> [!question]- qd-cpp-ub-list | Name five kinds of undefined behaviour you would look for in a code review of trading code.
> Signed overflow, out-of-bounds indexing, dangling references or views (including iterator invalidation), data races, strict-aliasing or misaligned access through `reinterpret_cast`. Also uninitialised reads and shifts past the width.

> [!question]- qd-cpp-pmr | What does `std::pmr::monotonic_buffer_resource` give you on a hot path?
> Allocation by pointer bump from a buffer you supply (for example on the stack), no per-object free, release all at once. A `pmr::vector` of 100 int64 values in a 4 KiB buffer made 0 heap allocations here.

> [!question]- qd-cpp-shared-ptr-cost | Why is `std::shared_ptr` discouraged on the hot path?
> Every copy and destruction is an atomic reference-count update (a cache line bounced between cores when shared), the control block is a heap allocation unless `make_shared` merges it, and the last owner runs the destructor at an unpredictable place.

> [!question]- qd-cpp-moved-from | What can you do with a moved-from `std::string`?
> Assign to it or destroy it; it is valid but in an unspecified state. Do not rely on it being empty.

> [!question]- qd-cpp-abi-break | What is an ABI break, with a real example?
> A change in layout, calling convention or mangling that makes separately compiled binaries incompatible. GCC 5 changed `std::string` and `std::list` for C++11 conformance and kept both behind `_GLIBCXX_USE_CXX11_ABI`; mixing the settings fails at link time.

> [!question]- qd-cpp-constexpr-use | Give two uses of `constexpr` in a trading codebase.
> Validating literals and configuration at compile time (`static_assert(parse_price("101.25")->raw == 1012500)`), and building lookup tables (tick tables, a normal CDF table) in read-only data so nothing is computed at startup or per message.

## In this repo and SDE-Interview-Prep

- Code: [cpp_idioms.hpp](code/cpp/cpp_idioms.hpp) (fixed-point prices, layout, move counting, RAII, CRTP and variant, `Expected`, `memcpy` and `bit_cast`, `pmr`), [cpp_idioms_demo.cpp](code/cpp/cpp_idioms_demo.cpp) (prints and checks every number above), [dispatch_bench.cpp](code/cpp/dispatch_bench.cpp) (dispatch and exception cost), tests in [tests/test_cpp_idioms.cpp](code/cpp/tests/test_cpp_idioms.cpp), and [compile_time_greeks.cpp](code/cpp/compile_time_greeks.cpp).
- Next: [Low-Latency Engineering](03-Low-Latency-Engineering.md), [Concurrency, Lock-Free Queues and Memory Pools](04-Concurrency-Lock-Free-and-Memory-Pools.md), [Pricing Library Design](10-Pricing-Library-Design.md).
- [Ultimate C++ advanced guide (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/Ultimate-CPP-Advanced-Guide.md)
- [STL complete reference (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/02-Programming-Languages/C%2B%2B/stl_complete_reference.md)
- [Static vs virtual dispatch in hot paths (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/04%20-%20Hardware%20Mechanical%20Sympathy/Static%20vs%20Virtual%20Dispatch%20in%20Hot%20Paths.md)
- [Allocation-free steady state patterns (SDE-Interview-Prep)](https://github.com/shreejitverma/SDE-Interview-Prep/blob/main/14-Low-Latency-Systems/08%20-%20Low-Latency%20Programming/Allocation-Free%20Steady%20State%20Patterns.md)

## Further reading

- Bjarne Stroustrup, *A Tour of C++*, 3rd edition (Addison-Wesley, 2022): the language in one sitting, C++20 included.
- Scott Meyers, *Effective Modern C++* (O'Reilly, 2014), chapter 5 (items 23 to 30, rvalue references, move semantics and perfect forwarding) and item 41.
- Nicolai Josuttis, *C++ Move Semantics: The Complete Guide* (2020).
- Mark Joshi, *C++ Design Patterns and Derivatives Pricing*, 2nd edition (Cambridge University Press, 2008).
- Bjarne Stroustrup and Herb Sutter (editors), *C++ Core Guidelines*, isocpp.github.io/CppCoreGuidelines.
- Agner Fog, *Optimizing software in C++*, agner.org/optimize.
- Carl Cook, "When a Microsecond Is an Eternity: High Performance Trading Systems in C++", CppCon 2017.
- John Regehr, "A Guide to Undefined Behavior in C and C++" (blog series, 2010), and Chris Lattner, "What Every C Programmer Should Know About Undefined Behavior" (LLVM blog, 2011).
