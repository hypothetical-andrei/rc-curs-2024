from scapy.all import *

for i in range(1, 10):
  resp = sr(IP(dst="8.8.8.8")/ICMP())
  print(resp)
