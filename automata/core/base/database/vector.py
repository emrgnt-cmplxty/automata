import abc
import contextlib
import logging
import logging.config
from typing import Dict, Generic, List, Optional, TypeVar, cast

import jsonpickle

logger = logging.getLogger(__name__)

K = TypeVar("K")
V = TypeVar("V")


class VectorDatabaseProvider(abc.ABC, Generic[K, V]):
    """An abstract base class for different types of vector database providers."""

    @abc.abstractmethod
    def __len__(self) -> int:
        pass

    # Parameterless methods

    @abc.abstractmethod
    def save(self) -> None:
        """Abstract method to save data."""
        pass

    @abc.abstractmethod
    def load(self) -> None:
        """Abstract method to load data."""
        pass

    @abc.abstractmethod
    def clear(self) -> None:
        """Abstract method to clear all entries."""
        pass

    @abc.abstractmethod
    def get_ordered_keys(self) -> List[K]:
        """Abstract method to get all keys stored in the database."""
        pass

    @abc.abstractmethod
    def get_ordered_entries(self) -> List[V]:
        """
        Abstract method to get an ordered list entries in the database.
        These vectors should be ordered in the same way as the keys returned by get_ordered_keys.
        """
        pass

    # Value dependent methods (e.g. V dependent)

    @abc.abstractmethod
    def add(self, entry: V) -> None:
        """Abstract method to add an entry to the database."""
        pass

    @abc.abstractmethod
    def batch_add(self, entries: V) -> None:
        """Abstract method to add a batch of specific entries to the database."""
        pass

    @abc.abstractmethod
    def update_entry(self, entry: V) -> None:
        """Abstract method to update a specific entry."""
        pass

    @abc.abstractmethod
    def batch_update(self, entries: List[V]) -> None:
        """Abstract method to update a list of specific entries."""
        pass

    @abc.abstractmethod
    def entry_to_key(self, entry: V) -> K:
        """Abstract method to generate a unique hashable key from an entry of type V."""
        pass

    # Keyed dependent methods (e.g. K dependent)

    @abc.abstractmethod
    def contains(self, key: K) -> bool:
        """Abstract method to check if a specific entry is present in the database."""
        pass

    @abc.abstractmethod
    def get(self, key: K) -> V:
        """Abstract method to get a specific entry."""
        pass

    @abc.abstractmethod
    def batch_get(self, keys: List[K]) -> List[V]:
        """Abstract method to get a batch of specific entries."""
        pass

    @abc.abstractmethod
    def discard(self, key: K) -> None:
        """Abstract method to discard a specific entry."""
        pass

    @abc.abstractmethod
    def batch_discard(self, keys: List[K]) -> None:
        """Abstract method to discard a batch of specific entries."""
        pass


class JSONVectorDatabase(VectorDatabaseProvider, Generic[K, V]):
    """
    An abstraction to provide a vector database that saves into a JSON file.

    Note - This implementation was not designed with efficiency in mind.
    """

    def __init__(self, file_path: str):
        self.file_path = file_path
        self.data: List[V] = []
        self.index: Dict[K, int] = {}
        self.load()

    def __len__(self) -> int:
        return len(self.data)

    # Parameterless methods

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

    def clear(self) -> None:
        self.data = []
        self.index = {}
        with contextlib.suppress(FileNotFoundError):
            with open(self.file_path, "r") as file:
                file.write("")

    @abc.abstractmethod
    def get_ordered_keys(self) -> List[K]:
        """We need specificity for the ordering of keys in the JSON database."""
        pass

    def get_ordered_entries(self) -> List[V]:
        return [self.data[self.index[key]] for key in self.get_ordered_keys()]

    # Value dependent methods (e.g. V dependent)

    def add(self, entry: V) -> None:
        self.data.append(entry)
        self.index[self.entry_to_key(entry)] = len(self.data) - 1

    def batch_add(self, entries: List[V]) -> None:
        for entry in entries:
            self.add(entry)

    def update_entry(self, entry: V) -> None:
        key = self.entry_to_key(entry)
        if key not in self.index:
            raise KeyError(f"Update database failed with key {key} not in database")
        self.data[self.index[key]] = entry

    def batch_update(self, entries: List[V]) -> None:
        for entry in entries:
            self.update_entry(entry)

    @abc.abstractmethod
    def entry_to_key(self, entry: V) -> K:
        """We need specificity for the converstion of values to keys."""
        pass

    # Key dependent methods (e.g. V dependent)

    def contains(self, key: K) -> bool:
        return key in self.index

    def get(self, key: K) -> V:
        if key not in self.index:
            raise KeyError(f"Get failed with {key} not in database")
        return self.data[self.index[key]]

    def batch_get(self, keys: List[K]) -> List[V]:
        return [self.get(key) for key in keys]

    def discard(self, key: K) -> None:
        if key not in self.index:
            raise KeyError
        index = self.index[key]
        del self.data[index]
        del self.index[key]
        # Recalculate indices after deletion
        self.index = {self.entry_to_key(entry): i for i, entry in enumerate(self.data)}

    def batch_discard(self, keys: List[K]) -> None:
        # TODO - This implementation is super inefficient, we should think
        # on a better way to handle the index recalculation for batches.
        for key in keys:
            self.discard(key)


class ChromaVectorDatabase(VectorDatabaseProvider, Generic[K, V]):
    """Concrete class to provide a vector database that uses Chroma."""

    def __init__(self, collection_name: str, persist_directory: Optional[str] = None):
        self._setup_chroma_client(persist_directory)
        self._collection = self.client.get_or_create_collection(collection_name)

    def _setup_chroma_client(self, persist_directory: Optional[str] = None):
        """Setup the Chroma client, here we attempt to contain the Chroma dependency."""
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
                    persist_directory=persist_directory,
                )
            )
        else:
            # A single instance client which terminates at session end
            self.client = chromadb.Client()

    def __len__(self):
        return self._collection.count()

    # Parameterless methods

    def load(self) -> None:
        """As Chroma is a live database, no specific load action is required."""
        pass

    def save(self) -> None:
        """As Chroma is a live database, no specific save action is required."""
        self.client.persist()

    def clear(self) -> None:
        """Clears all entries in the collection, Use with care!"""
        self._collection.delete(where={})

    @abc.abstractmethod
    def get_ordered_keys(self) -> List[K]:
        """Specificity required to determine the correct ordering of keys."""
        pass

    @abc.abstractmethod
    def get_ordered_entries(self) -> List[V]:
        """Specificity required to get the ordered entries efficiently."""
        pass

    # Value dependent methods (e.g. V dependent)

    @abc.abstractmethod
    def add(self, entry: V) -> None:
        """Specificity required to carry out the add operation correctly."""
        pass

    @abc.abstractmethod
    def batch_add(self, entries: List[V]) -> None:
        """Specificity required to carry out the batch add efficiently."""
        pass

    @abc.abstractmethod
    def update_entry(self, entry: V) -> None:
        """Specificity required to carry out the update operation correctly."""
        pass

    @abc.abstractmethod
    def batch_update(self, entries: List[V]) -> None:
        """Specificity required to carry out the batch update efficiently."""
        pass

    @abc.abstractmethod
    def entry_to_key(self, entry: V) -> K:
        """Specificity required to convert the entry to the corresponding key."""
        pass

    # Keyed dependent methods (e.g. K dependent)
    # TODO - PyLance is complaining about the type of the ids parameter below
    # Can we constrain the TypeVar to be a Chroma compatible type (e.g. ID)?

    def contains(self, key: K) -> bool:
        result = self._collection.get(ids=[key])
        return len(result["ids"]) != 0

    def discard(self, key: K) -> None:
        try:
            self._collection.delete(ids=[key])
        except RuntimeError as e:
            # FIXME - It seems an error in Chroma is causing this to be raised falsely
            if str(e) != "The requested to delete element is already deleted":
                raise

    def batch_discard(self, keys: List[K]) -> None:
        self._collection.delete(ids=keys)
