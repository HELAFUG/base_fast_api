import logging
from typing import TYPE_CHECKING, Callable
from pika.exchange_type import ExchangeType
from core import config


if TYPE_CHECKING:
    from pika.adapters.blocking_connection import BlockingChannel
    from pika.spec import Basic, BasicProperties

log = logging.getLogger(__name__)


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

    def consume_message(
        self,
        on_message_callback: Callable[
            [
                "BlockingChannel",
                "Basic.Deliver",
                "BasicProperties",
                bytes,
            ],
            None,
        ] = None,
        pre_count: int = 1,
        queue_name: str = "",
    ):
        self.channel.basic_qos(prefetch_count=pre_count)
        self.channel.basic_consume(
            queue=queue_name,
            on_message_callback=on_message_callback,
            auto_ack=True,
        )
        log.warning("Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()


class EmailRabbitUpdates(EmailUpdatesRabbitMixin):
    pass
