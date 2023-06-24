from typing import Any, Dict


class Singleton:
    """A singleton metaclass"""

    _instances: Dict[Any, Any] = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instances[cls]
