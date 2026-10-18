// Demo of the fixed-size object pool and the monotonic arena in memory_pool.hpp.
// Build: g++ -std=c++20 -O2 memory_pool.cpp

#include "memory_pool.hpp"

#include <cstdint>
#include <iostream>

struct Order {
    int id;
    double price;
    double qty;
};

struct Quote {  // trivially destructible: may live in an arena
    std::int64_t bid;
    std::int64_t ask;
};

int main() {
    qpmem::ObjectPool<Order> pool;
    Order* o1 = pool.create(1, 100.5, 10.0);
    Order* o2 = pool.create(2, 100.6, 20.0);
    std::cout << "order " << o1->id << " @ " << o1->price << ", order " << o2->id << " @ " << o2->price << '\n';

    const void* freed_slot = o1;  // remember the address, not the dangling pointer
    pool.destroy(o1);
    Order* o3 = pool.create(3, 101.0, 5.0);
    const bool reused = static_cast<const void*>(o3) == freed_slot;
    std::cout << "order " << o3->id << " reused the freed slot: " << std::boolalpha << reused << "\nlive " << pool.live()
              << " of capacity " << pool.capacity() << '\n';
    pool.destroy(o2);
    pool.destroy(o3);

    qpmem::Arena arena(1024);
    int placed = 0;
    while (arena.make<Quote>(Quote{100, 101}) != nullptr) ++placed;
    std::cout << "arena of 1024 bytes holds " << placed << " Quotes of " << sizeof(Quote) << " bytes\n";
    arena.reset();
    const bool reset_ok = arena.used() == 0 && arena.make<Quote>(Quote{1, 2}) != nullptr;

    return (pool.live() == 0 && reused && placed == 64 && reset_ok) ? 0 : 1;
}
