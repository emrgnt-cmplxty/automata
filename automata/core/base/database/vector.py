import abc
import logging
import logging.config
from typing import Any, Dict, Generic, List, TypeVar, cast

import jsonpickle

from automata.core.symbol.base import SymbolEmbedding

logger = logging.getLogger(__name__)

T = TypeVar("T")
K = TypeVar("K")


class VectorDatabaseProvider(Generic[T, K]):
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
    def add(self, obj: T) -> Any:
        """Abstract method to add a vector to the database."""
        pass

    @abc.abstractmethod
    def update_database(self, obj: T) -> Any:
        """Abstract method to update an existing vector."""
        pass

    @abc.abstractmethod
    def clear(self) -> Any:
        """Abstract method to clear all vectors."""
        pass

    @abc.abstractmethod
    def get_all_entries(self) -> List[T]:
        """Abstract method to calculate the similarity between the given vector and vectors in the database."""
        pass

    # Keyed objects
    @abc.abstractmethod
    def contains(self, key: K) -> bool:
        """Abstract method to check if a specific vector is present."""
        pass

    @abc.abstractmethod
    def discard(self, key: K) -> Any:
        """Abstract method to discard a specific vector."""
        pass

    @abc.abstractmethod
    def get(self, key: K) -> Any:
        """Abstract method to get a specific vector."""
        pass

    @abc.abstractmethod
    def entry_to_key(self, entry: T) -> K:
        """Method to generate a hashable key from an entry of type T."""
        pass


class JSONVectorDatabase(VectorDatabaseProvider[T, K], Generic[T, K]):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[T] = []
        self.index: Dict[K, int] = {}
        self.load()

    def save(self):
        """Saves the vector database to the JSON file."""
        with open(self.file_path, "w") as file:
            encoded_data = cast(str, jsonpickle.encode(self.data))
            file.write(encoded_data)

    def load(self):
        """Loads the vector database from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                self.data = cast(List[T], jsonpickle.decode(file.read()))
                self.index = {
                    self.entry_to_key(embedding): i for i, embedding in enumerate(self.data)
                }

        except FileNotFoundError:
            logger.info(f"Creating new vector database at {self.file_path}")

    def add(self, entry: T):
        self.data.append(entry)
        self.index[self.entry_to_key(entry)] = len(self.data) - 1

    def update_database(self, entry: T):
        key = self.entry_to_key(entry)
        if key not in self.index:
            raise KeyError(f"Update database failed with key {key} not in database")
        self.data[self.index[key]] = entry

    def discard(self, key: K):
        if key not in self.index:
            raise KeyError
        index = self.index[key]
        del self.data[index]
        del self.index[key]
        # Recalculate indices after deletion
        self.index = {self.entry_to_key(entry): i for i, entry in enumerate(self.data)}

    def contains(self, key: K) -> bool:
        return key in self.index

    def get(self, key: K) -> T:
        if key not in self.index:
            raise KeyError(f"Get failed with {key} not in database")
        return self.data[self.index[key]]

    def clear(self):
        self.data = []
        self.index = {}


class JSONEmbeddingVectorDatabase(JSONVectorDatabase):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def entry_to_key(self, entry: SymbolEmbedding) -> str:
        """Method to generate a hashable key from an entry of type T."""
        return entry.symbol.dotpath

    def get_all_entries(self) -> List[SymbolEmbedding]:
        return sorted(self.data, key=lambda x: self.entry_to_key(x))


# class JSONEmbeddingVectorDatabase(VectorDatabaseProvider):
#     """Concrete class to provide a vector database that saves into a JSON file."""

#     def __init__(self, file_path: str):
#         self.file_path = file_path
#         self.data: List[SymbolEmbedding] = []
#         self.index: Dict[str, int] = {}
#         self.load()

#     def save(self):
#         """Saves the vector database to the JSON file."""
#         with open(self.file_path, "w") as file:
#             encoded_data = jsonpickle.encode(self.data)
#             file.write(encoded_data)

#     def load(self):
#         """Loads the vector database from the JSON file."""
#         try:
#             with open(self.file_path, "r") as file:
#                 self.data = jsonpickle.decode(file.read())
#                 # We index on the dotpath of the symbol, which is unique and indepenent of commit hash
#                 self.index = {embedding.symbol.dotpath: i for i, embedding in enumerate(self.data)}
#         except FileNotFoundError:
#             logger.info(f"Creating new vector embedding db at {self.file_path}")

#     def add(self, embedding: SymbolEmbedding):
#         self.data.append(embedding)
#         self.index[embedding.symbol.dotpath] = len(self.data) - 1

#     def update_database(self, embedding: SymbolEmbedding):
#         if embedding.symbol not in self.index:
#             raise KeyError(f"Symbol {embedding.symbol} not in database")
#         self.data[self.index[embedding.symbol.dotpath]] = embedding

#     def discard(self, symbol: Symbol):
#         if symbol.dotpath not in self.index:
#             raise KeyError(f"Symbol {symbol} not in database")
#         index = self.index[symbol.dotpath]
#         del self.data[index]
#         del self.index[symbol.dotpath]
#         # Recalculate indices after deletion
#         self.index = {embedding.symbol.dotpath: i for i, embedding in enumerate(self.data)}

#     def contains(self, symbol: Symbol) -> bool:
#         return symbol.dotpath in self.index

#     def get(self, symbol: Symbol) -> SymbolEmbedding:
#         if symbol.dotpath not in self.index:
#             raise KeyError(f"Symbol {symbol} not in database")
#         return self.data[self.index[symbol.dotpath]]

#     def clear(self):
#         self.data = []
#         self.index = {}

#     def get_all_entries(self) -> List[Symbol]:
#         symbol_list = [embedding.symbol for embedding in self.data]
#         return sorted(symbol_list, key=lambda x: str(x.dotpath))
