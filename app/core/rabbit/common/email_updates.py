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

    def declare_queue_for_email_request(
        self,
        queue_name: str = "",
        exclusive: bool = True,
    ) -> str:
        self.declare_email_updates_exchange()
        queue = self.channel.queue_declare(
            queue=queue_name,
            exclusive=exclusive,
        )

        q_name = queue_name.method.queue

        self.channel.queue_bind(
            exchange=config.MQ_EMAIL_UPDATES_EXCHANGE_NAME,
            queue=q_name,
        )

        return q_name
