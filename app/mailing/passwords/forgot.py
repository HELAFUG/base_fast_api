from mailing.mail.send_email import send_email
from core.models import User


async def send_password_forgot_email(user: User, token: str):
    await send_email(
        recipient=user.email,
        sub="Verification Token Inside,Warning Dont Share",
        body=f"your personal reset token is {token}",
    )
