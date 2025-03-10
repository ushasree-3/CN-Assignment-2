import socket
import time

SERVER_IP = "172.24.133.110"
SERVER_PORT = 12345

print("Client started...")

start_time = time.time()
while time.time() - start_time < 140:  # Run for 140 seconds
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((SERVER_IP, SERVER_PORT))
        msg = client_socket.recv(1024)
        print(msg.decode('utf-8'))
        client_socket.close()
    except Exception as e:
        print(f"Connection failed: {e}")
    time.sleep(1)  # Simulate normal traffic
