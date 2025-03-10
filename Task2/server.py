import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 12345      # Port to listen on

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen(5)

print(f"Server listening on {HOST}:{PORT}...")

while True:
    client_socket, addr = server_socket.accept()
    print(f"Connection from {addr}")
    client_socket.sendall(b"Welcome to the server!\n")
    client_socket.close()
