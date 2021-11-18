from typing import Any

class DatabaseError(Exception):
    def __init__(self, message="Unable to complete database operation!", object_to_debug: Any=None) -> None:
        self.message: str = message
        super().__init__(self.message)