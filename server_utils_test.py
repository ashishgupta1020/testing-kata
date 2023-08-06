import socket
import threading
from time import sleep
from unittest.mock import patch
from server_utils import decode_request, get_villains, run_service, process_request, start_server
import unittest

class TestServer(unittest.TestCase):
    def test_start_server(self):
        test_host = "127.0.0.1"
        test_port = 8083
        s1 = start_server(test_host, test_port)
        server_thread = threading.Thread(target=s1.accept)
        server_thread.start()
        
        sleep(0.1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            s.connect((test_host, test_port))
        finally:
            s.close()
            s1.close()
            server_thread.join()

        assert True, "Server start up successful"

    @patch('server_utils.process_request')
    @patch('server_utils.decode_request')
    def test_run_service(self, decode_request, process_request):
        test_host = "127.0.0.1"
        test_port = 8083
        # Mocks
        decode_request.return_value = b'Q. Who is the villain?'
        process_request.return_value = "Lucius Malfoy".encode()

        s1 = start_server(test_host, test_port)
        server_thread = threading.Thread(target=run_service, args=(s1,))
        server_thread.start()

        sleep(0.1)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try: 
            s.connect((test_host, test_port))
            s.sendall(b'\x16Q. Who is the villain?')
            data = s.recv(1024)
            assert data.decode() == "Lucius Malfoy", "Service responds correctly"
        finally:
            s.close()
            s1.close()
            server_thread.join()

    def test_get_villains(self):
        assert len(get_villains()) == 3

    @patch('server_utils.get_villains')
    def test_process_request(self, get_villains):
        get_villains.return_value = ["Ron", "Harry", "Hermione"]
        assert process_request('Q. Who is the villain?') == b"Harry", "Process works correctly"
        assert process_request('') == b"unknown", "Process works correctly with empty input"

        get_villains.side_effect = RuntimeError("Mock error")
        assert process_request('Q. Who is the villain?') == b"A Nobody", "Process is resilient"
        try:
            process_request('Q. Is this unexpected?')
        except:
            assert True, "Unexpected query raised an exception"
        else:
            assert False, "Unexpected query silently failed"

    def test_decode_request(self):
        assert decode_request(b'Repeat after me') == "Repeat after me", "Decode works correctly"

if __name__ == '__main__':
    unittest.main()