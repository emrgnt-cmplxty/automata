import abc
from typing import Any

from automata.core.symbol.symbol_types import Symbol, SymbolEmbedding


class SymbolDatabaseProvider(abc.ABC):
    """
    Abstract base class for different types of database providers.
    """

    @abc.abstractmethod
    def save(self) -> Any:
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
    def add(self, embedding: SymbolEmbedding) -> Any:
        """
        Abstract method to add an embedding to the database.
        """
        pass

    @abc.abstractmethod
    def update(self, embedding: SymbolEmbedding) -> Any:
        """
        Abstract method to update an existing embedding.
        """
        pass

    @abc.abstractmethod
    def discard(self, symbol: Symbol) -> Any:
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
    def clear(self) -> Any:
        """
        Abstract method to clear all embeddings.
        """
        pass

    @abc.abstractmethod
    def contains(self, symbol: Symbol) -> bool:
        """
        Abstract method to check if a specific embedding is present.
        """
        pass
