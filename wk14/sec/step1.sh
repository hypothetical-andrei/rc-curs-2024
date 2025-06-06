# ping the target machine
# on metasploitable
# sudo ifconfig eth0 10.0.2.16 netmask 255.255.255.0 up
ping -c 3 192.168.56.101
# generic scan
nmap 192.168.56.101
