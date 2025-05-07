import socket
import struct
import time
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

ICMP_ECHO_REQUEST = 8

def checksum(source):
    sum = 0
    count = 0
    max_count = len(source) - (len(source) % 2)

    while count < max_count:
        val = source[count + 1] * 256 + source[count]
        sum = sum + val
        sum = sum & 0xffffffff
        count += 2

    if len(source) % 2:
        sum += source[-1]

    sum = (sum >> 16) + (sum & 0xffff)
    sum += (sum >> 16)
    return (~sum) & 0xffff

def encrypt_message(message: bytes, pub_key_path: str) -> bytes:
    with open(pub_key_path, "rb") as f:
        public_key = serialization.load_pem_public_key(f.read())
    encrypted = public_key.encrypt(
        message,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    return encrypted

def create_packet(packet_id, sequence, encrypted_payload):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, packet_id, sequence)
    chksum = checksum(header + encrypted_payload)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(chksum), packet_id, sequence)
    return header + encrypted_payload

def secure_ping(host="127.0.0.1", message=b"HelloPing", key_path="public.pem"):
    dest = socket.gethostbyname(host)
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(1)

    packet_id = os.getpid() & 0xFFFF
    sequence = 1

    encrypted_payload = encrypt_message(message, key_path)
    packet = create_packet(packet_id, sequence, encrypted_payload)
    send_time = time.time()
    sock.sendto(packet, (dest, 0))

    try:
        reply, _ = sock.recvfrom(1024)
        recv_time = time.time()
        rtt = (recv_time - send_time) * 1000
        print(f"Reply received from {dest} in {rtt:.2f} ms")
    except socket.timeout:
        print("Request timed out")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Run as root")
    else:
        secure_ping(message=b'I am a secret')
