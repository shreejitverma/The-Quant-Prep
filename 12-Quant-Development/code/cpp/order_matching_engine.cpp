#include <iostream>
#include <map>
#include <unordered_map>
#include <list>
#include <memory>
#include <string>
#include <vector>

// Order Side
enum class Side { BUY, SELL };

// Order Structure
struct Order {
    int id;
    int price;
    int quantity;
    Side side;
    long timestamp; // For time priority

    Order(int id, int price, int quantity, Side side, long timestamp)
        : id(id), price(price), quantity(quantity), side(side), timestamp(timestamp) {}
};

// Limit Order Book Class
class OrderBook {
private:
    // Bids: Max-Heap behavior (Ordered descending key) -> standard map is ascending, so use greater<int>
    std::map<int, std::list<std::shared_ptr<Order>>, std::greater<int>> bids;
    // Asks: Min-Heap behavior (Ordered ascending key)
    std::map<int, std::list<std::shared_ptr<Order>>> asks;
    
    // Quick lookup for cancellations O(1)
    std::unordered_map<int, std::shared_ptr<Order>> order_map;

public:
    void add_order(int id, int price, int quantity, Side side, long timestamp) {
        auto order = std::make_shared<Order>(id, price, quantity, side, timestamp);
        
        // Try to match immediately (Crossing the spread)
        if (side == Side::BUY) {
            match_buy(order);
        } else {
            match_sell(order);
        }

        // If order still has quantity, add to book
        if (order->quantity > 0) {
            if (side == Side::BUY) {
                bids[price].push_back(order);
            } else {
                asks[price].push_back(order);
            }
            order_map[id] = order;
        }
    }

    void cancel_order(int id) {
        if (order_map.find(id) == order_map.end()) {
            std::cout << "Order " << id << " not found." << std::endl;
            return;
        }

        auto order = order_map[id];
        // In a real system, we would lazily delete or use a doubly-linked list node to remove O(1)
        // Here we just mark quantity as 0 for lazy deletion logic usually
        order->quantity = 0; 
        order_map.erase(id);
        std::cout << "Order " << id << " cancelled." << std::endl;
    }

private:
    void match_buy(std::shared_ptr<Order> buy_order) {
        // Look at lowest sells (asks)
        while (buy_order->quantity > 0 && !asks.empty()) {
            auto best_ask_itr = asks.begin();
            int best_price = best_ask_itr->first;

            if (best_price > buy_order->price) break; // No match possible

            auto& orders_at_level = best_ask_itr->second;
            
            while (buy_order->quantity > 0 && !orders_at_level.empty()) {
                auto sell_order = orders_at_level.front();
                
                int trade_qty = std::min(buy_order->quantity, sell_order->quantity);
                
                std::cout << "TRADE: " << trade_qty << " @ " << best_price << std::endl;
                
                buy_order->quantity -= trade_qty;
                sell_order->quantity -= trade_qty;

                if (sell_order->quantity == 0) {
                    orders_at_level.pop_front();
                    order_map.erase(sell_order->id);
                }
            }

            if (orders_at_level.empty()) {
                asks.erase(best_ask_itr);
            }
        }
    }

    void match_sell(std::shared_ptr<Order> sell_order) {
        // Look at highest buys (bids)
        while (sell_order->quantity > 0 && !bids.empty()) {
            auto best_bid_itr = bids.begin();
            int best_price = best_bid_itr->first;

            if (best_price < sell_order->price) break;

            auto& orders_at_level = best_bid_itr->second;

            while (sell_order->quantity > 0 && !orders_at_level.empty()) {
                auto buy_order = orders_at_level.front();

                int trade_qty = std::min(sell_order->quantity, buy_order->quantity);

                std::cout << "TRADE: " << trade_qty << " @ " << best_price << std::endl;

                sell_order->quantity -= trade_qty;
                buy_order->quantity -= trade_qty;

                if (buy_order->quantity == 0) {
                    orders_at_level.pop_front();
                    order_map.erase(buy_order->id);
                }
            }

            if (orders_at_level.empty()) {
                bids.erase(best_bid_itr);
            }
        }
    }
};

int main() {
    OrderBook book;
    
    std::cout << "--- Adding Liquidity ---" << std::endl;
    book.add_order(1, 100, 10, Side::SELL, 1000);
    book.add_order(2, 101, 20, Side::SELL, 1001);
    
    std::cout << "--- Crossing Spread (Aggressive Buy) ---" << std::endl;
    // Should match 10 @ 100, then rest 5 @ 101
    book.add_order(3, 102, 15, Side::BUY, 1002);

    return 0;
}
