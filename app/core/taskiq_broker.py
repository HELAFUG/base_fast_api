__all__ = ("broker",)

import logging
from taskiq import TaskiqEvents, TaskiqState
from taskiq_aio_pika import AioPikaBroker
from core.config import settings

log = logging.getLogger(__name__)

broker = AioPikaBroker(url=settings.taskiq.url)


@broker.on_event(TaskiqEvents.WORKER_STARTUP)
async def on_worker_start_up(state: TaskiqState) -> None:
    logging.basicConfig(
        level=settings.logging.log_level,
        datefmt=settings.logging.datefmt,
    )
    log.info("Worker started up: %r", state)


@broker.on_event(TaskiqEvents.WORKER_SHUTDOWN)
async def on_worker_shut_down(state: TaskiqState) -> None:
    log.info("Worker shut down: %r", state)
