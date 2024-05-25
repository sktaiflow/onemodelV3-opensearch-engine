from enum import Enum

class ErrorCode(Enum):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.code = self.name
        self.status_code = status_code