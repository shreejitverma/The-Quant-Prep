import io
import struct


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

    MESSAGE_FORMAT = ">BQQIIc"  # Big-Endian: uchar, ulong, ulong, uint, uint, char
    MESSAGE_SIZE = struct.calcsize(MESSAGE_FORMAT)  # 1 + 8 + 8 + 4 + 4 + 1 = 26 bytes

    def __init__(self):
        pass

    def create_mock_packet(self, msg_type, timestamp, order_id, price, qty, side):
        """Creates a binary buffer representing a market message."""
        # round, not int(): int() truncates, and 0.57 * 10000 is 5699.999999999999 in binary floating point.
        price_int = round(price * 10000)
        return struct.pack(self.MESSAGE_FORMAT, msg_type, timestamp, order_id, price_int, qty, side.encode("ascii"))

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
                "side": unpacked[5].decode("ascii"),
            }
            yield msg


if __name__ == "__main__":
    parser = ItchParserMock()

    # 1. Simulate Incoming Network Stream
    buffer = io.BytesIO()

    # Add an order
    buffer.write(parser.create_mock_packet(1, 1600000000, 101, 150.25, 100, "B"))
    # Add another order
    buffer.write(parser.create_mock_packet(1, 1600000005, 102, 150.30, 50, "S"))

    # Rewind buffer to read
    buffer.seek(0)

    print(f"Packet Size: {parser.MESSAGE_SIZE} bytes")
    print("--- Parsing Stream ---")

    parsed = list(parser.parse_stream(buffer))
    for msg in parsed:
        print(f"Time: {msg['timestamp']} | ID: {msg['order_id']} | {msg['side']} {msg['quantity']} @ {msg['price']:.4f}")
    assert parser.MESSAGE_SIZE == 1 + 8 + 8 + 4 + 4 + 1 == 26
    assert [(m["timestamp"], m["order_id"], m["side"], m["quantity"], m["price"]) for m in parsed] == [
        (1600000000, 101, "B", 100, 150.25),
        (1600000005, 102, "S", 50, 150.30),
    ]

    # Every cent price from 0.01 to 999.99 must survive the trip to integer ticks.
    truncated = sum(1 for c in range(1, 100_000) if int(c / 100 * 10000) != c * 100)
    rounded = sum(1 for c in range(1, 100_000) if round(c / 100 * 10000) != c * 100)
    print(f"cent prices mis-scaled by int(): {truncated}, by round(): {rounded}")
    assert truncated == 5228 and rounded == 0
    print(f"0.57 * 10000 = {0.57 * 10000!r}, int() gives {int(0.57 * 10000)}")
    assert repr(0.57 * 10000) == "5699.999999999999" and int(0.57 * 10000) == 5699
