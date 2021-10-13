import logging
from email.message import EmailMessage
from django.conf import settings
import aiosmtplib

logger = logging.getLogger()

class EmailSender:

    async def send_message(self, msg, to):

        message = EmailMessage()
        message["From"] = settings.DEFAULT_FROM_EMAIL
        message["To"] = to
        message["Subject"] = "CheckITout - site down"
        message.set_content(msg)


        try:
            await aiosmtplib.send(message,
                                  hostname=settings.EMAIL_HOST,
                                  port=settings.EMAIL_PORT,
                                  username=settings.EMAIL_HOST_USER,
                                  password=settings.EMAIL_HOST_PASSWORD,
                                  use_tls=True,
                                  validate_certs=False
                                  )

            logger.info(f"EMAIL: Message was sent to {to}")
        except Exception as e:
            logger.info(f"EMAIL:Sending message error {e} - to {to}")

    async def run(self):
        return None
