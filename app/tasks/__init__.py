__all__ = (
    "welcome_email_notification",
    "send_after_forgot",
    "send_after_reset",
)

import sys
import logging
from core.config import settings
from .welcome_email_notification import welcome_email_notification
from .passwords import send_after_forgot, send_after_reset


# if sys.argv[0] == "worker":
#     logging.basicConfig(
#         level=settings.logging.log_level,
#         datefmt=settings.logging.datefmt,
#     )
