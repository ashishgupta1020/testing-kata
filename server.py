import threading

from server_utils import run_service, start_server


host = "127.0.0.1"
identity_port = 8081
# broadcast_port = 8082

id_counter = 0

id_socket = start_server(host, identity_port)
# cast_socket = start_server(host, broadcast_port)

t1 = threading.Thread(target=run_service, args=(id_socket,))
# t2 = threading.Thread(target=broadcast_service, args=(cast_socket,))

t1.start()
# t2.start()

t1.join()
# t2.join()

print("Done, exiting server!")