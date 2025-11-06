import aiosmtplib
from os import getenv
from email.message import EmailMessage
from core.config import settings

ADMIN_EMAIL = getenv("ADMIN_EMAIL", "admin@example.com")


async def send_email(recepient: str, receier: str, sub: str):

    message = EmailMessage()
    message["Subject"] = sub
    message["From"] = ADMIN_EMAIL
    message["To"] = recepient
    message.set_content()

    await aiosmtplib.send(
        message,
        hostname="localhost",
        recipients=[recepient],
        port=1025,
        sender=ADMIN_EMAIL,
    )
