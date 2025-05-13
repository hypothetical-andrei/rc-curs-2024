import paramiko
import socket
import threading

# Update the host key to a generated key on your machine
host_key = paramiko.RSAKey.from_private_key_file('id_rsa', '1234')

class Server (paramiko.ServerInterface):
  def __init__(self):
    self.event = threading.Event()

  def check_channel_request(self, kind, chanid):
    if kind == 'session':
      return paramiko.OPEN_SUCCEEDED
    return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

  def check_auth_password(self, username, password):
    # Here you can use more complex logic or check against a user database
    if (username == 'testuser') and (password == 'testpassword'):
      return paramiko.AUTH_SUCCESSFUL
    return paramiko.AUTH_FAILED

  def check_channel_pty_request(self, channel, term, width, height, pixelwidth, pixelheight, modes):
    # Acknowledge and allow PTY allocation requests
    return True

  def check_channel_shell_request(self, channel):
    self.event.set()
    return True

def listen():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('', 2200))  # You can specify any available port here
    sock.listen(100)
    print("Listening for connection ...")
    client, addr = sock.accept()

    print('Got a connection!')

    try:
        transport = paramiko.Transport(client)
        transport.add_server_key(host_key)
        server = Server()

        try:
          transport.start_server(server=server)
        except paramiko.SSHException:
          print('SSH session failed.')

        chan = transport.accept(20)
        if chan is None:
          print('No channel.')
          return
        
        print('Authenticated!')
        chan.send('Welcome to the SSH \n')
        command = ''
        while True:
          part = chan.recv(1024)
          if not part:
            break
          if part == 'exit':
            chan.send('exit')
            break
          print(f'received {part}')
          command += part.decode('utf-8')
          if part.decode('utf-8') == '\r':
            print(f'received command {command}')
            chan.send(f'I should execute: {command} \n')
            command = ''
        chan.close()
    except Exception as e:
      print(f"Caught exception: {e}")
    finally:
      transport.close()

if __name__ == "__main__":
    listen()
