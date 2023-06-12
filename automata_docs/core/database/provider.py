import abc
from typing import Any

from automata_docs.core.symbol.symbol_types import Embedding, Symbol


class DatabaseProvider(abc.ABC):
    """
    Abstract base class for different types of database providers.
    """

    @abc.abstractmethod
    def save(self, data: Any):
        """
        Abstract method to save data.
        """
        pass

    @abc.abstractmethod
    def load(self) -> Any:
        """
        Abstract method to load data.
        """
        pass

    @abc.abstractmethod
    def add(self, embedding: Embedding):
        """
        Abstract method to add an embedding to the database.
        """
        pass

    @abc.abstractmethod
    def discard(self, symbol: Symbol):
        """
        Abstract method to discard a specific embedding.
        """
        pass

    @abc.abstractmethod
    def get(self, symbol: Symbol) -> Any:
        """
        Abstract method to get a specific embedding.
        """
        pass

    @abc.abstractmethod
    def clear(self):
        """
        Abstract method to clear all embeddings.
        """
        pass
