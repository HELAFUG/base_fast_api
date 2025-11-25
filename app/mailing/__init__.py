import sys
import logging
from core.config import settings

if sys.argv[0] == "worker":
    logging.basicConfig(level=settings.logging.log_level)
