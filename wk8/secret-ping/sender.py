import socket
import struct
import time
import os

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

def create_packet(packet_id, sequence):
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, 0, packet_id, sequence)
    payload = b'PingTest' + struct.pack("d", time.time())
    chksum = checksum(header + payload)
    header = struct.pack("bbHHh", ICMP_ECHO_REQUEST, 0, socket.htons(chksum), packet_id, sequence)
    return header + payload

def ping(host, count=4, timeout=1):
    dest = socket.gethostbyname(host)
    print(f"Pinging {host} [{dest}] with ICMP:")

    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    sock.settimeout(timeout)
    packet_id = os.getpid() & 0xFFFF

    for seq in range(count):
        packet = create_packet(packet_id, seq)
        send_time = time.time()
        sock.sendto(packet, (dest, 0))

        try:
            reply, _ = sock.recvfrom(1024)
            recv_time = time.time()
            rtt = (recv_time - send_time) * 1000
            print(f"Reply from {dest}: seq={seq} time={rtt:.2f} ms")
        except socket.timeout:
            print(f"Request timed out for seq={seq}")

        time.sleep(1)

if __name__ == "__main__":
    if os.geteuid() != 0:
        print("Must run as root!")
    else:
        ping("127.0.0.1")
