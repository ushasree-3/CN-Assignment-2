import socket
import time

# Configuration
SERVER_ADDRESS = "0.0.0.0"  # Updated IP address
SERVER_PORT = 45678  # Updated port number
ENABLE_NAGLE = False  # Set to False to disable Nagle’s Algorithm
SEND_RATE = 40  # Bytes per second
FILE_SIZE = 4096  # 4 KB file
DATA_CHUNK = 40  # Sending 40 bytes at a time

# Create and configure client socket
cli_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not ENABLE_NAGLE:
    cli_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)  # Disable Nagle

cli_socket.connect((SERVER_ADDRESS, SERVER_PORT))

print("Connected to server, starting data transfer...")

start_time = time.time()
bytes_sent = 0
packet_counter = 0

while bytes_sent < FILE_SIZE:
    chunk = b"x" * DATA_CHUNK  # Sending dummy 40-byte data
    cli_socket.sendall(chunk)
    bytes_sent += DATA_CHUNK
    packet_counter += 1

    response = cli_socket.recv(1024)  # Wait for ACK
    print(f"Sent {bytes_sent} bytes, Received: {response.decode()}")

    time.sleep(1)  # Maintain transfer rate of 40 bytes/sec

end_time = time.time()
elapsed_time = end_time - start_time

print("\nFile transfer complete")
print(f"Total time taken: {elapsed_time:.2f} seconds")
print(f"Total packets sent: {packet_counter}")

cli_socket.close()
