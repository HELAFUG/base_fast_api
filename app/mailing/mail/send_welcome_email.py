from core.models import User
from .send_email import send_email


async def send_welcome_email(user: User) -> None:
    await send_email(
        recipient=user.email,
        sub="Welcome to FastAPI",
        body="Thanks for signing up",
    )
