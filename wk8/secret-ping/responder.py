import socket
import struct
import os
import time

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

def create_reply_packet(packet):
    icmp_header = packet[20:28]
    type, code, chksum, pkt_id, sequence = struct.unpack("bbHHh", icmp_header)
    if type != ICMP_ECHO_REQUEST:
        return None

    payload = packet[28:]
    reply_type = ICMP_ECHO_REPLY
    code = 0
    chksum = 0
    header = struct.pack("bbHHh", reply_type, code, chksum, pkt_id, sequence)
    chksum = checksum(header + payload)
    header = struct.pack("bbHHh", reply_type, code, socket.htons(chksum), pkt_id, sequence)
    return header + payload

def run_icmp_responder():
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    print("Ping responder started. Waiting for ICMP Echo Requests...")
    while True:
        packet, addr = sock.recvfrom(1024)
        reply = create_reply_packet(packet)
        if reply:
            sock.sendto(reply, addr)
            print(f"Replied to ping from {addr[0]}")

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Must run as root!")
    else:
        run_icmp_responder()
