import socket
import time

host = "127.0.0.1"
id_port = 8081
cast_port = 8082

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, cast_port))

start = time.time()
s.connect((host, id_port))

# 3. introduce backwards incompatibility
# s.sendall(b'Who is the villain?')

# 22 = 00010110 = \x16
# s.sendall(b'\x16Q. Who is the villain?')
# 6. introduce need for fuzz testing
# s.sendall(b'\xfe\xff')

# 8. testing with prod data, streaming client
s.sendall(b'\x16Q. Who is the villain?' + b'\x16Q. Who is the villain?')

# 4. introduce missing functionality - client sends an unexpected request
# s.sendall(b'Q. Are you the villain?')

#for _ in range(5):
data = s.recv(1024)
if not data:
    raise RuntimeError("The oracle has no answers.")
if data.decode == "Voldemort":
    raise RuntimeError("*Shudders* Never take You-Know-Who's name!")
else:
    print(f"The villain is {data.decode()}")

end = time.time()
print(f"\n Took {end - start} seconds to respond.")