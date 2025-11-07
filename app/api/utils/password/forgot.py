from api.utils.mail.send_email import send_email
from core.models import User


async def forgot_password_email(user: User, token: str):
    await send_email(
        recepient=user.email,
        sub="Reset Password Token Inside, Please Be Cautious",
        body=token,
    )
