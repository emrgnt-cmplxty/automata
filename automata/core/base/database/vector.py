import abc
import logging
import logging.config
from typing import Any, Dict, Generic, List, Optional, TypeVar, cast

import jsonpickle

logger = logging.getLogger(__name__)

K = TypeVar("K")
V = TypeVar("V")


class VectorDatabaseProvider(abc.ABC, Generic[K, V]):
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
    def add(self, obj: V) -> Any:
        """Abstract method to add a vector to the database."""
        pass

    @abc.abstractmethod
    def update_database(self, obj: V) -> Any:
        """Abstract method to update an existing vector."""
        pass

    @abc.abstractmethod
    def clear(self) -> Any:
        """Abstract method to clear all vectors."""
        pass

    @abc.abstractmethod
    def get_ordered_embeddings(self) -> List[V]:
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
    def get(self, key: K, *args: Any, **kwargs: Any) -> Any:
        """Abstract method to get a specific vector."""
        pass

    @abc.abstractmethod
    def entry_to_key(self, entry: V) -> K:
        """Method to generate a hashable key from an entry of type V."""
        pass


class JSONVectorDatabase(VectorDatabaseProvider[K, V], Generic[K, V]):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[V] = []
        self.index: Dict[K, int] = {}
        self.load()

    def save(self) -> None:
        """Saves the vector database to the JSON file."""
        with open(self.file_path, "w") as file:
            encoded_data = cast(str, jsonpickle.encode(self.data))
            file.write(encoded_data)

    def load(self) -> None:
        """Loads the vector database from the JSON file."""
        try:
            with open(self.file_path, "r") as file:
                self.data = cast(List[V], jsonpickle.decode(file.read()))
                self.index = {
                    self.entry_to_key(embedding): i for i, embedding in enumerate(self.data)
                }

        except FileNotFoundError:
            logger.info(f"Creating new vector database at {self.file_path}")

    def add(self, entry: V) -> None:
        self.data.append(entry)
        self.index[self.entry_to_key(entry)] = len(self.data) - 1

    def update_database(self, entry: V):
        key = self.entry_to_key(entry)
        if key not in self.index:
            raise KeyError(f"Update database failed with key {key} not in database")
        self.data[self.index[key]] = entry

    def discard(self, key: K) -> None:
        if key not in self.index:
            raise KeyError
        index = self.index[key]
        del self.data[index]
        del self.index[key]
        # Recalculate indices after deletion
        self.index = {self.entry_to_key(entry): i for i, entry in enumerate(self.data)}

    def contains(self, key: K) -> bool:
        return key in self.index

    def get(self, key: K, *args: Any, **kwargs: Any) -> V:
        if key not in self.index:
            raise KeyError(f"Get failed with {key} not in database")
        return self.data[self.index[key]]

    def clear(self):
        self.data = []
        self.index = {}


class ChromaVectorDatabase(VectorDatabaseProvider[K, V]):
    """Concrete class to provide a vector database that uses Chroma."""

    def __init__(self, collection_name: str, persist_directory: Optional[str] = None):
        try:
            import chromadb
            from chromadb.config import Settings
        except ImportError as e:
            raise ImportError(
                "Please install Chroma Python client first: " "`pip install chromadb`"
            ) from e
        if persist_directory:
            self.client = chromadb.Client(
                Settings(
                    chroma_db_impl="duckdb+parquet",
                    persist_directory=persist_directory,  # Optional, defaults to .chromadb/ in the current directory
                )
            )
        else:
            self.client = chromadb.Client()
        self._collection = self.client.get_or_create_collection(collection_name)
