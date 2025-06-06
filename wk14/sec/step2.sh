# run a service scan
nmap -sV 192.168.56.101
# aggressive fingerprinting
nmap -A 192.168.56.101
# when scanning aggressively
# -O (OS detection)
# -sC (default NSE scripts)
# -sV (version detection)
nmap -sC 192.168.56.101
