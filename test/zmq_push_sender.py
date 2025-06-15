import zmq
import struct
import time
import random

context = zmq.Context()
socket = context.socket(zmq.PUSH)
socket.connect("tcp://127.0.0.1:5555")

print("[Sender] Sending binary messages...")

for _ in range(5):
    data = [random.random() for _ in range(4)]  # 4 random floats
    packed = struct.pack("ffff", *data)
    socket.send(packed)
    print(f"[Sender] Sent: {data}")
    time.sleep(1)
