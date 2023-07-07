import abc
from copy import deepcopy
from typing import TYPE_CHECKING, Any, Callable, List, Optional, TypeVar

import numpy as np

from automata.core.base.database.vector import ChromaVectorDatabase, JSONVectorDatabase
from automata.symbol.parser import parse_symbol
from automata.symbol_embedding.base import SymbolEmbedding

if TYPE_CHECKING:
    from chromadb.api.types import GetResult

V = TypeVar("V", bound=SymbolEmbedding)


class IEmbeddingLookupProvider(abc.ABC):
    """A concrete base class an interface for embedding lookup providers."""

    def embedding_to_key(self, entry: SymbolEmbedding) -> str:
        """Concrete implementation to generate a simple hashable key from a Symbol."""
        return entry.symbol.dotpath


class ChromaSymbolEmbeddingVectorDatabase(ChromaVectorDatabase[str, V], IEmbeddingLookupProvider):
    """Concrete class to provide a vector database that saves into a Chroma db."""

    def __init__(
        self,
        collection_name: str,
        factory: Callable[..., V],
        persist_directory: Optional[str] = None,
    ):
        super().__init__(collection_name, persist_directory)
        self._factory = factory

    def add(self, entry: V) -> None:
        """
        Adds a SymbolEmbedding to the collection.

        Adds the specified SymbolEmbedding to the collection.
        FIXME - Adding raw symbol to the metadata is a hack
        to get around the fact that we are using 'dotpaths' as keys
        rather than the raw symbols.
        We should think of a smarter way to approach this problem.
        We have chosen to use dotpaths since they are easier to maintain
        as a commit hash change will not cause them to become stale.
        """
        if self.contains(self.entry_to_key(entry)):
            raise KeyError(f"Add failed with {entry} already in database")

        metadata = deepcopy(entry.metadata)
        metadata["symbol_uri"] = entry.symbol.uri
        self._collection.add(
            documents=[entry.document],
            metadatas=[metadata],
            ids=[self.entry_to_key(entry)],
            embeddings=[[int(ele) for ele in entry.vector]],
        )

    def batch_add(self, entries):
        """
        Batch add entries to the database.

        Arguments:
        entries -- list of entries to add
        """
        documents = []
        metadatas = []
        ids = []
        embeddings = []

        for entry in entries:
            documents.append(entry.document)
            metadatas.append(entry.metadata)
            ids.append(self.entry_to_key(entry))
            embeddings.append([int(ele) for ele in entry.vector])

        self._collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )

    def get(
        self,
        key: str,
        *args: Any,
        **kwargs: Any,
    ) -> V:
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
        kwargs = {
            "ids": key,
            "where": kwargs.get("where"),
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset"),
            "where_document": kwargs.get("where_document"),
            "include": kwargs.get("include", ["documents", "metadatas", "embeddings"]),
        }

        result = self._collection.get(**kwargs)
        if len(result["ids"]) == 0:
            raise KeyError(f"Get failed with {key} not in database")
        elif len(result["ids"]) > 1:
            raise KeyError(f"Get failed with {key}, multiple entries found")

        return self._construct_object_from_result(result)

    def get_ordered_entries(self) -> List[V]:
        """Retrieves all embeddings in the collection in a sorted order."""
        results = self._collection.get(include=["documents", "metadatas", "embeddings"])
        embeddings = [
            self._construct_object_from_result(
                {"metadatas": [metadata], "documents": [document], "embeddings": [embedding]}
            )
            for metadata, document, embedding in zip(
                results["metadatas"], results["documents"], results["embeddings"]
            )
        ]
        return sorted(embeddings, key=lambda x: x.symbol.dotpath)

    def update_entry(self, entry: V):
        """Updates an entry in the database."""
        # Update the entry in the database.
        metadata = deepcopy(entry.metadata)
        metadata["symbol_uri"] = entry.symbol.uri
        self._collection.update(
            documents=[entry.document],
            metadatas=[metadata],
            ids=[self.entry_to_key(entry)],
            embeddings=[[int(ele) for ele in entry.vector]],
        )

        return entry.symbol.dotpath

    def _construct_object_from_result(self, result: "GetResult") -> V:
        """Constructs an object from the provided result."""
        metadatas = result["metadatas"][0]
        metadatas["key"] = parse_symbol(metadatas.pop("symbol_uri"))
        metadatas["vector"] = np.array(result["embeddings"][0]).astype(int)
        metadatas["document"] = result["documents"][0]

        return self._factory(**metadatas)

    def entry_to_key(self, entry: V) -> str:
        """
        Generates a simple hashable key from a Symbol.
        """
        return self.embedding_to_key(entry)

    def get_ordered_keys(self) -> List[str]:
        """Retrieves all keys in the collection in a sorted order."""
        results = self._collection.get(include=[])
        return sorted(list(results["ids"]))

    def batch_update(self, entries: List[V]) -> None:
        """
        Batch update entries in the database.

        Arguments:
        entries -- list of entries to update
        """
        documents = []
        metadatas = []
        ids = []
        embeddings = []

        for entry in entries:
            documents.append(entry.document)
            metadatas.append(entry.metadata)
            ids.append(self.entry_to_key(entry))
            embeddings.append([int(ele) for ele in entry.vector])

        self._collection.update(
            documents=documents,
            metadatas=metadatas,
            ids=ids,
            embeddings=embeddings,
        )

    def batch_get(self, keys: List[str], *args: Any, **kwargs: Any) -> List[V]:
        """
        Retrieves multiple entries from the collection using the provided keys.

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
        kwargs = {
            "ids": keys,
            "where": kwargs.get("where"),
            "limit": kwargs.get("limit"),
            "offset": kwargs.get("offset"),
            "where_document": kwargs.get("where_document"),
            "include": kwargs.get("include", ["documents", "metadatas", "embeddings"]),
        }

        result = self._collection.get(**kwargs)
        if len(result["ids"]) == 0:
            raise KeyError(f"Get failed with {keys}, no entries found")

        return [
            self._construct_object_from_result(
                {"metadatas": [metadata], "documents": [document], "embeddings": [embedding]}
            )
            for metadata, document, embedding in zip(
                result["metadatas"], result["documents"], result["embeddings"]
            )
        ]


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
