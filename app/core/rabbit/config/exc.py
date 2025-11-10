class RabbitException(Exception):
    def __init__(self, message) -> None:
        super().__init__(f"Rabbit Error Now: {message}")
