import logging
import pika

from core.config import settings


def get_connection() -> pika.BlockingConnection:
    credentials = pika.PlainCredentials(
        settings.rabbitmq.user, settings.rabbitmq.password
    )
    return pika.BlockingConnection(
        pika.ConnectionParameters(
            host=settings.rabbitmq.host,
            port=settings.rabbitmq.port,
            credentials=credentials,
        )
    )


def configurate_logger(level: int = logging.INFO):
    logging.basicConfig(
        level=level,
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
