import logging
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from taskiq import TaskiqDepends
from core import broker
from core.models import User, db_helper
from crud.user import get_user_by_id
from mailing.user.login import send_login_email
from mailing.user.verify import send_verify_email, send_success_email

log = logging.getLogger(__name__)


@broker.task
async def send_after_login(
    user_id: int,
    session: Annotated[AsyncSession, TaskiqDepends(db_helper.session_getter)],
):
    user: User = await get_user_by_id(session=session, user_id=user_id)
    log.info("Sending login email to user %r", user_id)
    await send_login_email(user=user)


@broker.task
async def send_after_verify_req(
    user_id: int,
    token: str,
    session: Annotated[AsyncSession, TaskiqDepends(db_helper.session_getter)],
):
    user: User = await get_user_by_id(session=session, user_id=user_id)
    log.info("Sending verify email to user %r", user_id)
    await send_verify_email(user=user, token=token)


@broker.task
async def on_after_success(
    user_id: int,
    session: Annotated[AsyncSession, TaskiqDepends(db_helper.session_getter)],
):
    user: User = await get_user_by_id(session=session, user_id=user_id)
    log.info("Sending verify email to user %r", user_id)
    await send_success_email(user=user)
