__all__ = ("welcome_email_notification",)

import sys
import logging
from core.config import settings
from .welcome_email_notification import welcome_email_notification


if sys.argv[0] == "worker":
    logging.basicConfig(
        level=settings.logging.log_level,
        datefmt=settings.logging.datefmt,
    )
