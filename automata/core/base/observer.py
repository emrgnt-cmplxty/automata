from abc import ABC, abstractmethod
from typing import Any


class Observer(ABC):
    """An abstract class for implementing an observer."""

    @abstractmethod
    def update(self, subject: Any):
        """
        When the subject changes, this method is called to notify the observer.
        """
        pass
