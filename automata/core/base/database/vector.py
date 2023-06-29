import abc
import logging
import logging.config
from typing import Any, Dict, List

import jsonpickle

from automata.core.symbol.base import Symbol, SymbolEmbedding

logger = logging.getLogger(__name__)


class VectorDatabaseProvider:
    """An abstract base class for different types of vector database providers."""

    @abc.abstractmethod
    def save(self) -> Any:
        """Abstract method to save data."""
        pass

    @abc.abstractmethod
    def load(self) -> Any:
        """Abstract method to load data."""
        pass

    @abc.abstractmethod
    def add(self, embedding: SymbolEmbedding) -> Any:
        """Abstract method to add an embedding to the database."""
        pass

    @abc.abstractmethod
    def update_database(self, embedding: SymbolEmbedding) -> Any:
        """Abstract method to update an existing embedding."""
        pass

    @abc.abstractmethod
    def discard(self, symbol: Symbol) -> Any:
        """Abstract method to discard a specific embedding."""
        pass

    @abc.abstractmethod
    def get(self, symbol: Symbol) -> Any:
        """Abstract method to get a specific embedding."""
        pass

    @abc.abstractmethod
    def clear(self) -> Any:
        """Abstract method to clear all embeddings."""
        pass

    @abc.abstractmethod
    def contains(self, symbol: Symbol) -> bool:
        """Abstract method to check if a specific embedding is present."""
        pass

    @abc.abstractmethod
    def get_all_entries(self) -> List[Symbol]:
        """Abstract method to calculate the similarity between the given vector and vectors in the database."""
        pass


class JSONVectorDatabase(VectorDatabaseProvider):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[SymbolEmbedding] = []
        self.index: Dict[str, int] = {}
        self.load()

    def save(self):
        """Saves the vector database to the JSON file."""
        with open(self.file_path, "w") as file:
            encoded_data = jsonpickle.encode(self.data)
            file.write(encoded_data)

    def load(self):
        """Loads the vector database from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                self.data = jsonpickle.decode(file.read())
                # We index on the dotpath of the symbol, which is unique and indepenent of commit hash
                self.index = {embedding.symbol.dotpath: i for i, embedding in enumerate(self.data)}
        except FileNotFoundError:
            logger.info(f"Creating new vector embedding db at {self.file_path}")

    def add(self, embedding: SymbolEmbedding):
        self.data.append(embedding)
        self.index[embedding.symbol.dotpath] = len(self.data) - 1

    def update_database(self, embedding: SymbolEmbedding):
        if embedding.symbol not in self.index:
            raise KeyError(f"Symbol {embedding.symbol} not in database")
        self.data[self.index[embedding.symbol.dotpath]] = embedding

    def discard(self, symbol: Symbol):
        if symbol.dotpath not in self.index:
            raise KeyError(f"Symbol {symbol} not in database")
        index = self.index[symbol.dotpath]
        del self.data[index]
        del self.index[symbol.dotpath]
        # Recalculate indices after deletion
        self.index = {embedding.symbol.dotpath: i for i, embedding in enumerate(self.data)}

    def contains(self, symbol: Symbol) -> bool:
        return symbol.dotpath in self.index

    def get(self, symbol: Symbol) -> SymbolEmbedding:
        if symbol.dotpath not in self.index:
            raise KeyError(f"Symbol {symbol} not in database")
        return self.data[self.index[symbol.dotpath]]

    def clear(self):
        self.data = []
        self.index = {}

    def get_all_entries(self) -> List[Symbol]:
        symbol_list = [embedding.symbol for embedding in self.data]
        return sorted(symbol_list, key=lambda x: str(x.dotpath))
