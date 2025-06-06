import aiosmtpd.controller

class CustomSMTPHandler:
  async def handle_DATA(self, server, session, envelope):
    print('Message from:', envelope.mail_from)
    print('Message to:', envelope.rcpt_tos)
    print('Message content:')
    print(envelope.content.decode('utf8', errors='replace'))
    print('----------------')
    return '250 OK'

handler = CustomSMTPHandler()
server = aiosmtpd.controller.Controller(handler, hostname='localhost', port=8025)
server.start()
input("Server started. Press Return to quit.")
server.stop()