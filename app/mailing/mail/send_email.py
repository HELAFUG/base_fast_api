from email.message import EmailMessage

import aiosmtplib


async def send_email(recipient: str, sub: str, body: str) -> None:
    admin_email = "max@gmail.com"

    message = EmailMessage()
    message["From"] = admin_email
    message["To"] = recipient
    message["Subject"] = sub
    message.set_content(body)

    await aiosmtplib.send(
        message,
        recipients=[recipient],
        sender=admin_email,
        port=1025,
        hostname="localhost",
    )
