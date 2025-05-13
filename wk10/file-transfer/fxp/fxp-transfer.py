from ftplib import FTP
import re

def parse_pasv(response):
    import re
    m = re.search(r'\((\d+,\d+,\d+,\d+,\d+,\d+)\)', response)
    if not m:
        raise ValueError(f"Invalid PASV response format: {response}")
    parts = list(map(int, m.group(1).split(',')))
    if len(parts) != 6:
        raise ValueError(f"Invalid number of parts in PASV: {parts}")
    ip = '.'.join(map(str, parts[:4]))
    port = (parts[4] << 8) + parts[5]
    return ip, port, parts

# Connect to both servers
ftp_src = FTP()
ftp_src.connect('127.0.0.1', 2121)
ftp_src.login('user', '12345')

ftp_dst = FTP()
ftp_dst.connect('127.0.0.1', 2122)
ftp_dst.login('user', '12345')

# Passive mode on destination (returns IP/port for source to connect to)
pasv_resp = ftp_dst.sendcmd('PASV')
print("PASV Response:", pasv_resp)
ip, port, nums = parse_pasv(pasv_resp)

# Tell source to connect to destination's passive listener via PORT
# ⚠️ Ensure it's sending its own IP (127.0.0.1) for compatibility
port_cmd = f'PORT {",".join(map(str, nums))}'
print("Sending to src:", port_cmd)
resp = ftp_src.sendcmd(port_cmd)
print("PORT response:", resp)

# Perform FXP transfer: destination does STOR, source does RETR
filename = 'test.txt'

# STOR first (opens the connection), then RETR to push data
print("Starting FXP transfer...")
ftp_dst.sendcmd(f'STOR {filename}')
ftp_src.sendcmd(f'RETR {filename}')

ftp_src.quit()
ftp_dst.quit()

print("FXP transfer complete.")
