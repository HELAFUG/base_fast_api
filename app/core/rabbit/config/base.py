from typing import TYPE_CHECKING
import pika
from .exc import RabbitException


class RabbitBase:
    def __init__(self, conn_params: pika.ConnectionParameters) -> None:
        self.connection_params = conn_params
        self._connection: pika.BlockingConnection = pika.BlockingConnection()
        self._channel: pika.BlockingChannel | None = None

    def get_connection(self) -> pika.BlockingConnection:
        return self._connection

    @property
    def channel(self) -> pika.BlockingChannel:
        if self._channel is None:
            raise RabbitException("No channel yet")
        return self._channel

    def __enter__(self):
        self._connection = self.get_connection()
        self._channel = self._connection.channel()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self._channel.is_open:
            self._channel.close()
        if self._connection.is_open:
            self._connection.close()
