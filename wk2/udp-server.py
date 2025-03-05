import socket
import sys

PORT = 3333

PORT = int(PORT)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
  server_socket.bind(('', PORT))
  while True:
    message, address = server_socket.recvfrom(1024)
    server_socket.sendto(message.upper(), address)