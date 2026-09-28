#include <iostream>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <cstring>
#include <vector>

/**
 * Mock UDP Multicast Receiver for Market Data.
 * 
 * In HFT, Market Data (e.g., NASDAQ TotalView-ITCH) is typically 
 * delivered via UDP Multicast.
 * 
 * Key Concepts:
 * 1. Non-blocking sockets (using fcntl).
 * 2. UDP Multicast Group joining.
 * 3. Raw byte parsing into structs.
 */

#pragma pack(push, 1)
struct MarketUpdate {
    char msg_type;     // 'A' for Add, 'E' for Execute
    uint32_t symbol_id;
    uint32_t price;
    uint32_t quantity;
};
#pragma pack(pop)

class MarketDataReceiver {
private:
    int sockfd;
    struct sockaddr_in addr;

public:
    MarketDataReceiver(const char* ip, int port) {
        // 1. Create UDP Socket
        sockfd = socket(AF_INET, SOCK_DGRAM, 0);
        if (sockfd < 0) {
            perror("socket");
            exit(1);
        }

        // 2. Allow multiple sockets to use the same PORT
        int reuse = 1;
        setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, (char *)&reuse, sizeof(reuse));

        // 3. Setup Address
        memset(&addr, 0, sizeof(addr));
        addr.sin_family = AF_INET;
        addr.sin_addr.s_addr = htonl(INADDR_ANY); 
        addr.sin_port = htons(port);

        // 4. Bind
        if (bind(sockfd, (struct sockaddr*)&addr, sizeof(addr)) < 0) {
            perror("bind");
            exit(1);
        }

        // 5. Join Multicast Group (Simplified Mock)
        struct ip_mreq mreq;
        mreq.imr_multiaddr.s_addr = inet_addr(ip);
        mreq.imr_interface.s_addr = htonl(INADDR_ANY);
        // setsockopt(sockfd, IPPROTO_IP, IP_ADD_MEMBERSHIP, (char *)&mreq, sizeof(mreq));
        
        std::cout << "Listening for Market Data on " << ip << ":" << port << "..." << std::endl;
    }

    void receive_loop() {
        char buffer[1024];
        struct sockaddr_in from;
        socklen_t fromlen = sizeof(from);

        while (true) {
            ssize_t n = recvfrom(sockfd, buffer, sizeof(buffer), 0, (struct sockaddr*)&from, &fromlen);
            if (n < 0) break;

            if (n >= sizeof(MarketUpdate)) {
                MarketUpdate* update = reinterpret_cast<MarketUpdate*>(buffer);
                process_update(*update);
            }
        }
    }

    void process_update(const MarketUpdate& update) {
        std::cout << "Msg: " << update.msg_type 
                  << " | SymID: " << update.symbol_id 
                  << " | Price: " << update.price / 10000.0 
                  << " | Qty: " << update.quantity << std::endl;
    }

    ~MarketDataReceiver() {
        close(sockfd);
    }
};

int main() {
    // Note: This won't run without a live UDP stream, 
    // but demonstrates the boilerplate required in HFT interviews.
    std::cout << "--- UDP Market Data Feed Handler Mock ---" << std::endl;
    // MarketDataReceiver receiver("233.0.0.1", 12345);
    // receiver.receive_loop();
    return 0;
}
