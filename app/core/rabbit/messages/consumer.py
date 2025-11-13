from typing import TYPE_CHECKING
import logging
import pika
from app.core.rabbit.config.config import get_connection, configurate_logger
from core.config import settings
from core.rabbit.common.email_updates import EmailRabbitUpdates

log = logging.getLogger(__name__)

if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties


def process_new_message(
    channel: "BlockingChannel",
    method: "Basic.Deliver",
    properties: "BasicProperties",
    body: bytes,
):
    log.info("chanel:%s", channel)
    log.info("Received method: %r", method)
    log.info("Received message: %r", body)
    log.info("Received properties: %r", properties)


def consume_message(channel: "BlockingChannel"):
    channel.basic_consume(
        queue=settings.rabbitmq.queue,
        on_message_callback=process_new_message,
        # auto_ack=True,
    )
    log.warning("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


def consumer_main():
    with EmailRabbitUpdates() as rabbit:
        consume_message(rabbit.channel)
