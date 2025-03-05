import socket
import sys

HOST='127.0.0.1'
PORT=3333

PORT = int(PORT)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:
  while True:
    data = input("Please enter the message:\n")
    client_socket.sendto(data.encode('utf-8'), (HOST, PORT))
    message, address = client_socket.recvfrom(1024)
    print(message)