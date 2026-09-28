import struct
import io

class ItchParserMock:
    """
    Mock parser for a binary market data feed (Simulating NASDAQ ITCH).
    
    Protocol Definition (Mock):
    [Message Type: 1 byte]
    [Timestamp: 8 bytes (unsigned long long)]
    [Order ID: 8 bytes (unsigned long long)]
    [Price: 4 bytes (unsigned int, price * 10000)]
    [Quantity: 4 bytes (unsigned int)]
    [Side: 1 byte ('B' or 'S')]
    """
    
    MESSAGE_FORMAT = ">BQQIIc" # Big-Endian: uchar, ulong, ulong, uint, uint, char
    MESSAGE_SIZE = struct.calcsize(MESSAGE_FORMAT) # 1 + 8 + 8 + 4 + 4 + 1 = 26 bytes

    def __init__(self):
        pass

    def create_mock_packet(self, msg_type, timestamp, order_id, price, qty, side):
        """Creates a binary buffer representing a market message."""
        price_int = int(price * 10000)
        return struct.pack(self.MESSAGE_FORMAT, 
                           msg_type, 
                           timestamp, 
                           order_id, 
                           price_int, 
                           qty, 
                           side.encode('ascii'))

    def parse_stream(self, stream):
        """Reads from a binary stream and yields parsed messages."""
        while True:
            # Read exact number of bytes for one message
            data = stream.read(self.MESSAGE_SIZE)
            if not data or len(data) < self.MESSAGE_SIZE:
                break
            
            # Unpack
            unpacked = struct.unpack(self.MESSAGE_FORMAT, data)
            
            msg = {
                "type": unpacked[0],
                "timestamp": unpacked[1],
                "order_id": unpacked[2],
                "price": unpacked[3] / 10000.0,
                "quantity": unpacked[4],
                "side": unpacked[5].decode('ascii')
            }
            yield msg

if __name__ == "__main__":
    parser = ItchParserMock()
    
    # 1. Simulate Incoming Network Stream
    buffer = io.BytesIO()
    
    # Add an order
    buffer.write(parser.create_mock_packet(1, 1600000000, 101, 150.25, 100, 'B'))
    # Add another order
    buffer.write(parser.create_mock_packet(1, 1600000005, 102, 150.30, 50, 'S'))
    
    # Rewind buffer to read
    buffer.seek(0)
    
    print(f"Packet Size: {parser.MESSAGE_SIZE} bytes")
    print("--- Parsing Stream ---")
    
    for msg in parser.parse_stream(buffer):
        print(f"Time: {msg['timestamp']} | ID: {msg['order_id']} | {msg['side']} {msg['quantity']} @ {msg['price']:.4f}")
