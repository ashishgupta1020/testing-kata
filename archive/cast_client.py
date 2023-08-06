import socket
import time

host = "127.0.0.1"
cast_port = 8082

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

start = time.time()
s.connect((host, cast_port))

while True:
    data = s.recv(1024)
    if not data:
        raise RuntimeError("The oracle has no words.")
    else:
        print(f"{data.decode()}")

end = time.time()
print(f"\n Took {end - start} seconds to respond.")