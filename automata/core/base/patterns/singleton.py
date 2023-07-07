import abc
from typing import Any, Dict, List


class Singleton(abc.ABCMeta, type):
    """
    Singleton metaclass for ensuring only one instance of a class.
    """

    _instances: Dict[str, Any] = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the singleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Doubleton(abc.ABCMeta, type):
    """
    Doubleton metaclass for ensuring at most two instances of a class.
    """

    _instances: Dict[str, List[Any]] = {}

    def __call__(cls, *args, **kwargs):
        """Call method for the doubleton metaclass."""
        if cls not in cls._instances:
            cls._instances[cls] = []
        if len(cls._instances[cls]) < 2:
            instance = super(Doubleton, cls).__call__(*args, **kwargs)
            cls._instances[cls].append(instance)
        return cls._instances[cls][-1]  # Always return the last created instance
