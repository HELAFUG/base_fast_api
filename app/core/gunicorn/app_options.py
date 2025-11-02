from .logger import GunicornLogger


def get_app_options(
    host: str,
    port: int,
    workers: int,
    log_level: str,
) -> dict:
    return {
        "accesslog": "-",
        "errorlog": "-",
        "loglevel": log_level,
        "loggerclass": GunicornLogger,
        "bind": f"{host}:{port}",
        "worker_class": "uvicorn.workers.UvicornWorker",
        "workers": workers,
    }
