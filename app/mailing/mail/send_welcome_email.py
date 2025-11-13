from core.models import db_helper
from core.models import User
from crud.user import get_user_by_id
from .send_email import send_email


async def send_welcome_email(user_id: int) -> None:
    async with db_helper.session_factory() as session:
        user = await get_user_by_id(session=session, user_id=user_id)
    await send_email(
        recipient=user.email,
        sub="Welcome to FastAPI",
        body="Thanks for signing up",
    )
