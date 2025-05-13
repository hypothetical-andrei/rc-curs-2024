import sys
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

if len(sys.argv) != 2:
    print("Usage: python fxp_server.py <port>")
    sys.exit(1)

port = int(sys.argv[1])

# Setup user and permissions
authorizer = DummyAuthorizer()
authorizer.add_user("user", "12345", ".", perm="elradfmwMT")

# Handler with FXP support
handler = FTPHandler
handler.authorizer = authorizer
handler.permit_foreign_addresses = True

# Start the server
server = FTPServer(("127.0.0.1", port), handler)
print(f"Starting FTP server on port {port}")
server.serve_forever()
