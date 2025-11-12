import logging

from core import broker
from mailing.mail.send_welcome_email import send_welcome_email as send

log = logging.getLogger(__name__)


@broker.task
async def welcome_email_notification(user_id: int):
    log.info("Sending welcome email to user %r", user_id)
    await send(user_id=user_id)
