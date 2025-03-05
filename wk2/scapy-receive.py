#!/usr/bin/env python3

from scapy.all import sniff, UDP, IP

def udp_packet_handler(packet):
    if UDP in packet:
        src_ip = packet[IP].src
        dst_ip = packet[IP].dst
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
        payload = bytes(packet[UDP].payload)
        print(f"[+] Received UDP packet from {src_ip}:{src_port} to {dst_ip}:{dst_port}")
        print(f"    Payload: {payload}")

if __name__ == "__main__":
    # Use a BPF (Berkeley Packet Filter) to capture only UDP on port 9999
    # and only on the loopback interface (lo).
    sniff(
        filter="udp and port 9999",
        iface="lo",
        prn=udp_packet_handler
    )
