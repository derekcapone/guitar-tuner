import zmq
import struct

context = zmq.Context()
socket = context.socket(zmq.PULL)
socket.bind("tcp://127.0.0.1:5555")

print("[Receiver] Waiting for messages...")

while True:
    raw = socket.recv()  # blocking
    floats = struct.unpack("ffff", raw)
    print(f"[Receiver] Got floats: {floats}")
