import socket
import time

host = "127.0.0.1"
id_port = 8081
cast_port = 8082

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

start = time.time()
s.connect((host, id_port))

# 22 = 00010110 = \x16
# 19 = 00010011 = \x13
s.sendall(b'\x16Q. Who is the villain?')

data = s.recv(1024)
if not data:
    raise RuntimeError("The oracle has no answers.")
if data.decode == "Voldemort":
    raise RuntimeError("*Shudders* Never take You-Know-Who's name!")
else:
    print(f"The villain is {data.decode()}")

end = time.time()
print(f"\n Took {end - start} seconds to respond.")