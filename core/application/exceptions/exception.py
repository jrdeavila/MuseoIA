class MessageException(Exception):
    def __init__(self, message: str, headers: dict) -> None:
        self.message = message
        self.headers = headers


class NotFound(MessageException):
    def __init__(self, message: str) -> None:
        super().__init__(
            message,
            {
                "X-Error": "Not Found",
            },
        )
