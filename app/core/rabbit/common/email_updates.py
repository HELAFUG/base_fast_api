from typing import TYPE_CHECKING
from pika.exchange_type import ExchangeType
from core import config


if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel


class EmailUpdatesRabbitMixin:
    channel: "BlockingChannel"

    def declare_email_updates_exchange(self):
        self.channel.exchange_declare(
            exchange=config.MQ_EMAIL_UPDATES_EXCHANGE_NAME,
            exchange_type=ExchangeType.fanout,
        )
