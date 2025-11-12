from mail import send_email
from core.models import User


async def send_reset_password_email(user: User):
    await send_email(
        recipient=user.email,
        sub="Reset is successful",
        body="you are successfuly reset your password",
    )
