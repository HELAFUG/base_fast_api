__all__ = ("main",)
from core.gunicorn import get_app_options, Application
from core.config import settings
from core.config import settings
from core.rabbit import configurate_logger, get_connection
from core.rabbit.messages.consumer import consumer_main
from main import main_app


def main():
    app = Application(
        app=main_app,
        options=get_app_options(
            host=settings.srv.host,
            port=settings.srv.port,
            workers=settings.srv.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()
    conn = get_connection()
    consumer_main(conn)
    configurate_logger(level=settings.logging.log_level)
