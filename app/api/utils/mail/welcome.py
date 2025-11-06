from .send_email import send_email
from core.models import User


async def welcome_email(user: User):
    await send_email(
        recepient=user.email,
        sub="Welcome",
        body=f"Welcome {user.email} to the app",
    )
