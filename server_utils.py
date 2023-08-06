import socket
from time import sleep

global id_counter
id_counter = 0

def start_server(host, port): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(0)
    return s

def decode_request(data: bytes):
    input = data.decode()
    return input

def get_villains():
    with open('villains.txt', 'r') as file:
        villains = file.readlines()
    return villains

def process_request(input: str):
    try:
        villains = get_villains()
    except:
        villains = ["A Nobody"]

    # round-robin the names
    global id_counter
    id_counter += 1
    index = id_counter % len(villains)

    if input == 'Q. Who is the villain?':
        return villains[index].encode()
    # malformed input
    elif input == '':
        return "unknown".encode()
    else:
        raise RuntimeError("I am not capable..")

def run_service(s: socket):
    while True:
        try:
            conn, addr = s.accept()
        
            print(f"Client connected: {addr}")
            size = conn.recv(1)
            data = conn.recv(int.from_bytes(size,byteorder='little'))
            input = decode_request(data)
            output = process_request(input)
            conn.sendall(output)
            conn.close()
        except (ConnectionAbortedError, OSError) as error:
            print("Server needed to be closed..", error)
            break   

# def broadcast_service(s: socket):
#     while True:
#         conn, addr = s.accept()
#         print(f"Client connected for broadcast: {addr}")
#         while True:
#             if len(get_villains()) == 0:
#                 conn.sendall(b"Voldy's gone mouldy, so now let's have fun!")
#                 sleep(5)