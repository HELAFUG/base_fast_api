from datetime import datetime
from api.utils.mail.send_email import send_email
from core.models import User


async def after_update_account(user: User):
    await send_email(
        recepient=user.email,
        sub="Update Account Process",
        body=f"We have some changes in your account time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )


async def after_delete_account(user: User):
    await send_email(
        recepient=user.email,
        sub="Delete Account Process",
        body=f"You have deleted your account time:{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
    )
