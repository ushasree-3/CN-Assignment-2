import socket
import time

# Configuration
LISTEN_IP = "127.0.0.1"  # Updated IP address
LISTEN_PORT = 45678  # Updated port number
ENABLE_DELAYED_ACK = False # Set to False to disable delayed ACK
RECEIVE_BUFFER = 1024  # Buffer size for receiving data
DATA_CHUNK = 40  # Expected chunk size

# Create and configure server socket
srv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
srv_socket.bind((LISTEN_IP, LISTEN_PORT))
srv_socket.listen(1)

print(f"Server listening on {LISTEN_IP}:{LISTEN_PORT}")
conn, client_addr = srv_socket.accept()
print(f"Connection established with {client_addr}")

start_time = time.time()
total_data_received = 0
packet_counter = 0
max_packet_size = 0

while True:
    data = conn.recv(RECEIVE_BUFFER)
    if not data:
        break

    packet_size = len(data)
    total_data_received += packet_size
    packet_counter += 1
    max_packet_size = max(max_packet_size, packet_size)

    if ENABLE_DELAYED_ACK:
        time.sleep(0.2)  # Simulate delayed ACK (200ms)

    conn.sendall(b"ACK")  # Send ACK back

    elapsed_time = time.time() - start_time
    if elapsed_time >= 120:  # Run for ~2 minutes
        break

end_time = time.time()
elapsed_time = end_time - start_time

# Performance metrics
throughput = total_data_received / elapsed_time
goodput = total_data_received / elapsed_time  # Since all data is useful
packet_loss_rate = (packet_counter - (total_data_received / DATA_CHUNK)) / packet_counter if packet_counter > 0 else 0

print("\nTransfer complete.")
print(f"Total data received: {total_data_received} bytes")
print(f"Total packets received: {packet_counter}")
print(f"Throughput: {throughput:.2f} bytes/sec")
print(f"Goodput: {goodput:.2f} bytes/sec")
print(f"Packet Loss Rate: {packet_loss_rate * 100:.2f}%")
print(f"Maximum packet size achieved: {max_packet_size} bytes")

conn.close()
srv_socket.close()
