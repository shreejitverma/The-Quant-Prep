#include <iostream>
#include <vector>
#include <cassert>

/**
 * Simple Memory Pool Allocator for low-latency applications.
 * 
 * In HFT, we avoid 'new' and 'delete' on the hot path because:
 * 1. They involve a system call (context switch).
 * 2. They can cause heap fragmentation.
 * 3. Allocation time is non-deterministic.
 * 
 * This pool pre-allocates a chunk of memory and manages it manually.
 */

template <typename T, size_t BlockSize = 4096>
class MemoryPool {
private:
    struct Block {
        T data[BlockSize];
    };

    std::vector<Block*> blocks;
    std::vector<T*> free_list;
    size_t current_block_index;
    size_t current_slot_index;

public:
    MemoryPool() {
        current_block_index = 0;
        current_slot_index = 0;
        allocate_block();
    }

    ~MemoryPool() {
        for (auto block : blocks) {
            delete block;
        }
    }

    // Disable copy
    MemoryPool(const MemoryPool&) = delete;
    MemoryPool& operator=(const MemoryPool&) = delete;

    T* allocate() {
        // 1. Prefer picking from the free list (reusing returned memory)
        if (!free_list.empty()) {
            T* ptr = free_list.back();
            free_list.pop_back();
            return ptr;
        }

        // 2. If block is full, allocate a new one
        if (current_slot_index >= BlockSize) {
            allocate_block();
            current_block_index++;
            current_slot_index = 0;
        }

        // 3. Return next slot in current block
        return &(blocks[current_block_index]->data[current_slot_index++]);
    }

    void deallocate(T* ptr) {
        // In a real pool, we might want to check if ptr belongs to us.
        // For speed, we just push to free list for reuse.
        free_list.push_back(ptr);
    }

    template<typename... Args>
    T* construct(Args&&... args) {
        T* ptr = allocate();
        new(ptr) T(std::forward<Args>(args)...); // Placement new
        return ptr;
    }

    void destroy(T* ptr) {
        ptr->~T();
        deallocate(ptr);
    }

private:
    void allocate_block() {
        blocks.push_back(new Block());
    }
};

struct Order {
    int id;
    double price;
    double qty;
};

int main() {
    MemoryPool<Order> pool;

    std::cout << "Allocating orders from pool..." << std::endl;
    
    // Fast allocation without malloc overhead
    Order* o1 = pool.construct(1, 100.5, 10);
    Order* o2 = pool.construct(2, 100.6, 20);

    std::cout << "Order 1: " << o1->id << " @ " << o1->price << std::endl;

    // Reuse memory
    pool.destroy(o1);
    Order* o3 = pool.construct(3, 101.0, 5); // Should reuse o1's slot

    std::cout << "Order 3 (Reused): " << o3->id << " @ " << o3->price << std::endl;
    
    // Address verification
    std::cout << "Addr o1 (freed): " << o1 << std::endl;
    std::cout << "Addr o3 (new):   " << o3 << std::endl;
    
    if (o1 == o3) {
        std::cout << "Success: Memory was recycled!" << std::endl;
    }

    return 0;
}
