from mailing.mail.send_email import send_email
from core.models import User


async def send_verify_email(user: User, token: str):
    await send_email(
        recipient=user.email,
        sub="Verification Token,Warning Dont Share",
        body=token,
    )


async def send_success_email(user: User):
    await send_email(
        recipient=user.email,
        sub="Congratulations",
        body="You are successfuly verified",
    )
