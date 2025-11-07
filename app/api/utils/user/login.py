from datetime import datetime
from api.utils.mail.send_email import send_email
from core.models import User


async def after_login_email(user: User):
    await send_email(
        recepient=user.email,
        sub="Login Process",
        body=f"We have logged into your account time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )
