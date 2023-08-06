import socket
import sys
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
    # 6. account for malformed input
    # try:
    input = data.decode()
    # except UnicodeDecodeError:
        # return ""
    # 1. introduce bug for integration testing - process_request isn't updated
    # return input[3:]
    return input

def get_villains():
    # 2. introduce regression (also fix test)
    # villains = ["You-Know-Who", "Lucius Malfoy", "Gilderoy Lockhart", "Voldemort"]

    # 7. add degradation under stress
    # sleep(1)
    with open('villains.txt', 'r') as file:
        villains = file.read().splitlines()
    return villains
    # 9. introduce chaos - remove file

def process_request(input: str):
    try:
        villains = get_villains()
    except:
        villains = ["A Nobody"]

    # round-robin the names
    global id_counter
    # 5. introduce mutation
    # id_counter = 1
    id_counter += 1
    index = id_counter % len(villains)

    # 1. fix bug for integration testing
    # if input == 'Who is the villain?':
    if input == 'Q. Who is the villain?':
        return villains[index].encode()
    # 4. fix missing functionality
    # elif input == 'Q. Are you the villain?':
    #     return "not me. I am Tom Riddle.".encode()
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
            # 8. fix after need to test with prod data is recognised
            # while True:
            size = conn.recv(1)
            data = conn.recv(int.from_bytes(size,byteorder='little'))
                # if not data:
                    # break
            input = decode_request(data)
            output = process_request(input)
            conn.sendall(output)
            conn.close()
        except (ConnectionAbortedError, OSError) as error:
            print("Server needed to be closed..", error)
            break   

def broadcast_service(s: socket):
    while True:
        conn, addr = s.accept()
        print(f"Client connected for broadcast: {addr}")
        while True:
            if len(get_villains()) == 0:
                conn.sendall(b"Voldy's gone mouldy, so now let's have fun!")
                sleep(5)
            else:
                conn.sendall(b"The war is on..")
                sleep(5)