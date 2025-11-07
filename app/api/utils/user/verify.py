from api.utils.mail.send_email import send_email
from core.models import User


async def verify_email(user: User, token: str):
    await send_email(
        recepient=user.email,
        sub="Verification Token Inside, Please Be Cautious",
        body=token,
    )
