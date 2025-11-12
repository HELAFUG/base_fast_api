from datetime import datetime
from mailing.mail.send_email import send_email
from core.models import User


async def send_login_email(user: User):

    await send_email(
        recipient=user.email,
        sub="Someone is login into your account",
        body=f"Login Time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )
