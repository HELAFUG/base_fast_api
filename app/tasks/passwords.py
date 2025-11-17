import logging
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from core import broker
from core.models import User, db_helper
from crud.user import get_user_by_id
from mailing.passwords.forgot import send_password_forgot_email as send

log = logging.getLogger(__name__)


@broker.task
async def send_after_forgot(
    user_id: int,
    session: Annotated[AsyncSession, TaskiqDepends(db_helper.session_getter)],
):
    user: User = await get_user_by_id(session=session, user_id=user_id)
    log.info("Sending password forgot email to user %r", user_id)
    await send(user=user)


@broker.task
async def send_after_reset(
    user_id: int,
    session: Annotated[AsyncSession, TaskiqDepends(db_helper.session_getter)],
):
    user: User = await get_user_by_id(session=session, user_id=user_id)
    log.info("Sending password reset email to user %r", user_id)
    await send(user=user)
