import socket
import struct
import os
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization, hashes

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY = 0

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

def decrypt_payload(encrypted: bytes, priv_key_path: str) -> bytes:
    with open(priv_key_path, "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)
    return private_key.decrypt(
        encrypted,
        padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )

def create_reply(packet, decrypted_payload):
    icmp_header = packet[20:28]
    type, code, chksum, pkt_id, sequence = struct.unpack("bbHHh", icmp_header)

    if type != ICMP_ECHO_REQUEST:
        return None, None

    reply_type = ICMP_ECHO_REPLY
    code = 0
    chksum = 0
    header = struct.pack("bbHHh", reply_type, code, chksum, pkt_id, sequence)
    chksum = checksum(header + decrypted_payload)
    header = struct.pack("bbHHh", reply_type, code, socket.htons(chksum), pkt_id, sequence)

    return header + decrypted_payload, (pkt_id, sequence)

def run_responder(priv_key_path="private.pem"):
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print("Secure ping responder is running...")

    while True:
        packet, addr = sock.recvfrom(1024)
        encrypted_payload = packet[28:]

        try:
            decrypted = decrypt_payload(encrypted_payload, priv_key_path)
            print(f"Received message from {addr[0]}: {decrypted.decode('utf-8')}")
        except Exception as e:
            print(f"Failed to decrypt: {e}")
            continue

        reply, _ = create_reply(packet, encrypted_payload)
        if reply:
            sock.sendto(reply, addr)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Run as root")
    else:
        run_responder()
