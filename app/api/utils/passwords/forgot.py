from api.utils.mail.send_email import send_email
from core.models import User


async def send_verif_code(user: User, token: str):
    await send_email(
        recipient=user.email,
        sub="Verification Token,Warning Dont Share",
        body=token,
    )
