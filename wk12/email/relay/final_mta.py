import asyncio
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import AsyncMessage

class FinalHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Final server received message from:', session.peer)
        print('Message addressed from:', envelope.mail_from)
        print('Message addressed to  :', envelope.rcpt_tos)
        print('Message length        :', len(envelope.content))
        return '250 OK'

if __name__ == '__main__':
    handler = FinalHandler()
    controller = Controller(handler, hostname='localhost', port=1026)
    controller.start()
    print("Final SMTP server running on localhost:1026")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
