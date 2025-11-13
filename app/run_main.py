__all__ = ("main",)
from core.gunicorn import get_app_options, Application
from core.config import settings
from core.config import settings
from core.rabbit.config.config import configurate_logger
from core.rabbit.messages.consumer import consumer_main
from main import main_app


def main():
    configurate_logger(level=settings.logging.log_level)
    app = Application(
        app=main_app,
        options=get_app_options(
            host=settings.srv.host,
            port=settings.srv.port,
            workers=settings.srv.workers,
            log_level=settings.logging.log_level,
        ),
    ).run()
    consumer_main()
