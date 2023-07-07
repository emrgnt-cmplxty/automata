import abc
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, Dict, List, Optional, TypeVar, Union

import numpy as np

from automata.core.base.database.vector import ChromaVectorDatabase, JSONVectorDatabase
from automata.symbol.parser import parse_symbol
from automata.symbol_embedding.base import SymbolEmbedding

if TYPE_CHECKING:
    # TODO - How does this impact dependencies?
    from chromadb.api.types import GetResult

V = TypeVar("V", bound=SymbolEmbedding)


class IEmbeddingLookupProvider(abc.ABC):
    """A concrete base class an interface for embedding lookup providers."""

    def embedding_to_key(self, entry: SymbolEmbedding) -> str:
        """Concrete implementation to generate a simple hashable key from a Symbol."""
        return entry.symbol.dotpath


class ChromaSymbolEmbeddingVectorDatabase(ChromaVectorDatabase[str, V], IEmbeddingLookupProvider):
    """A vector database that saves into a Chroma db."""

    def __init__(
        self,
        collection_name: str,
        factory: Callable[..., V],
        persist_directory: Optional[str] = None,
    ):
        super().__init__(collection_name, persist_directory)
        self._factory = factory

    # Parameterless methods

    def get_ordered_keys(self) -> List[str]:
        """Retrieves all keys in the collection in a sorted order."""
        results = self._collection.get(include=[])
        return sorted(results["ids"])

    def get_ordered_entries(self) -> List[V]:
        """Retrieves all entries in the collection in a sorted order."""
        results = self._collection.get(**{"include": ["documents", "metadatas", "embeddings"]})
        return self._sort_entries(results)

    # Value dependent methods (e.g. V dependent)

    def add(self, entry: V) -> None:
        """Adds a SymbolEmbedding to the collection, checking for existing entries."""
        self._check_duplicate_entry(self.entry_to_key(entry))
        self._collection.add(**self._prepare_entries_for_insertion([entry]))

    def batch_add(self, entries: List[V]) -> None:
        """Adds multiple entries to the collection."""
        self._collection.add(**self._prepare_entries_for_insertion(entries))

    def update_entry(self, entry: V) -> None:
        """Updates an entry in the database."""
        self._collection.update(**self._prepare_entries_for_insertion([entry]))

    def batch_update(self, entries: List[V]) -> None:
        """Updates multiple entries in the database."""
        self._collection.update(**self._prepare_entries_for_insertion(entries))

    def entry_to_key(self, entry: V) -> str:
        """Generates a hashable key from a Symbol."""
        return self.embedding_to_key(entry)

        # Keyed dependent methods (e.g. str dependent)

    def get(self, key: str, *args: Any, **kwargs: Any) -> V:
        """
        Retrieves an entry from the collection using the provided key.

        Keyword Args:
            ids: The ids of the embeddings to get. Optional.
            where: A Where type dict used to filter results by.
                E.g. `{"color" : "red", "price": 4.20}`. Optional.
            limit: The number of documents to return. Optional.
            offset: The offset to start returning results from.
                    Useful for paging results with limit. Optional.
            where_document: A WhereDocument type dict used to filter by the documents.
                            E.g. `{$contains: {"text": "hello"}}`. Optional.
            include: A list of what to include in the results.
                    Can contain `"embeddings"`, `"metadatas"`, `"documents"`.
                    Ids are always included.
                    Defaults to `["metadatas", "documents", "embeddings"]`. Optional.
        """
        kwargs["ids"] = [key]
        kwargs["include"] = kwargs.get("include", ["documents", "metadatas", "embeddings"])

        result = self._collection.get(**kwargs)
        self._check_result_entries(result["ids"], key)

        return self._construct_entry_from_result(result)

    def batch_get(self, keys: List[str], *args: Any, **kwargs: Any) -> List[V]:
        """
        Retrieves multiple entries from the collection using the provided keys.

        Check `get` for more information on accepted kwargs.
        """
        kwargs["ids"] = keys
        kwargs["include"] = kwargs.get("include", ["documents", "metadatas", "embeddings"])

        results = self._collection.get(**kwargs)
        self._check_result_entries(results["ids"], keys)

        return [self._construct_entry_from_result(result) for result in results]

    # Support methods

    def _check_duplicate_entry(self, key: str) -> None:
        """Raises an error if the key already exists in the collection."""
        if self.contains(key):
            raise KeyError(f"Add failed with {key} already in database")

    def _check_result_entries(self, ids: List[str], keys: Union[str, List[str]]) -> None:
        """Raises an error if no entries or multiple entries are found."""
        if not ids:
            raise KeyError(f"Get failed with {keys}, no entries found")
        if len(ids) > 1:
            raise KeyError(f"Get failed with {keys}, multiple entries found")

    def _prepare_entry_for_insertion(self, entry: V) -> Dict[str, Any]:
        """Prepares an entry for insertion into the database."""
        metadata = deepcopy(entry.metadata)
        metadata["symbol_uri"] = entry.symbol.uri
        return {
            "document": entry.document,
            "metadata": metadata,
            "id": self.entry_to_key(entry),
            "embedding": [int(ele) for ele in entry.vector],
        }

    def _prepare_entries_for_insertion(self, entries: List[V]) -> Dict[str, Any]:
        """Prepares multiple entries for insertion into the database."""
        entries_data = [self._prepare_entry_for_insertion(entry) for entry in entries]
        return {
            "documents": [entry_data["document"] for entry_data in entries_data],
            "metadatas": [entry_data["metadata"] for entry_data in entries_data],
            "ids": [entry_data["id"] for entry_data in entries_data],
            "embeddings": [entry_data["embedding"] for entry_data in entries_data],
        }

    def _construct_entry_from_result(self, result: "GetResult") -> V:
        """Constructs an object from the provided result."""
        # FIXME - Consider how to properly handle typing here.
        metadatas = result["metadatas"][0]
        metadatas["key"] = parse_symbol(metadatas.pop("symbol_uri"))
        metadatas["vector"] = np.array(result["embeddings"][0]).astype(int)
        metadatas["document"] = result["documents"][0]

        return self._factory(**metadatas)

    def _sort_entries(self, results: Dict[str, List[Any]]) -> List[V]:
        """Sorts the entries based on their dotpaths."""
        entries = [
            self._construct_entry_from_result(
                {"metadatas": [metadata], "documents": [document], "embeddings": [embedding]}
            )
            for metadata, document, embedding in zip(
                results["metadatas"], results["documents"], results["embeddings"]
            )
        ]
        return sorted(entries, key=lambda x: x.symbol.dotpath)


class JSONSymbolEmbeddingVectorDatabase(
    JSONVectorDatabase[str, SymbolEmbedding], IEmbeddingLookupProvider
):
    """Concrete class to provide a vector database that saves into a JSON file."""

    def __init__(self, file_path: str):
        super().__init__(file_path)

    def get_ordered_keys(self) -> List[str]:
        return [
            ele.symbol.dotpath for ele in sorted(self.data, key=lambda x: self.entry_to_key(x))
        ]

    def get_ordered_entries(self) -> List[SymbolEmbedding]:
        return [self.data[self.index[key]] for key in self.get_ordered_keys()]

    def entry_to_key(self, entry: V) -> str:
        """
        Generates a simple hashable key from a Symbol.
        """
        return self.embedding_to_key(entry)
