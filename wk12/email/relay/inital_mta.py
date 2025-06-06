import asyncio
import smtplib
from aiosmtpd.controller import Controller

class RelayHandler:
    async def handle_DATA(self, server, session, envelope):
        print('Receiving message from:', session.peer)
        print('Message addressed from:', envelope.mail_from)
        print('Message addressed to  :', envelope.rcpt_tos)
        print('Message length        :', len(envelope.content))

        try:
            with smtplib.SMTP('localhost', 1026) as relay:
                relay.sendmail(envelope.mail_from, envelope.rcpt_tos, envelope.content)
                print("Email successfully relayed to localhost:1026")
        except smtplib.SMTPException as e:
            print("Failed to relay email:", e)
            return '550 Failed to relay email'

        return '250 Message relayed successfully'

if __name__ == '__main__':
    handler = RelayHandler()
    controller = Controller(handler, hostname='localhost', port=1025)
    controller.start()
    print("SMTP relay server running on localhost:1025")
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        pass
    finally:
        controller.stop()
