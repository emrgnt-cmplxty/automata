VectorDatabaseProvider
======================

Overview
--------

``VectorDatabaseProvider`` is an abstract base class that provides an
interface for different types of vector database providers. It defines a
standard set of operations for interacting with a vector database. The
operations covered include database CRUD operations, such as saving,
loading, clearing, and getting entries.

The ``VectorDatabaseProvider`` relies on the concrete implementation of
these operations which could be tailored according to the specific
vector database in use, such as ``SQLiteVectorDatabaseProvider``,
``MemoryVectorDatabaseProvider``, ``RedisVectorDatabaseProvider``, etc.

Related Symbols
---------------

-  ``automata.embedding.embedding_base.EmbeddingHandler``
-  ``automata.embedding.embedding_base.EmbeddingBuilder.__init__``
-  ``automata.embedding.embedding_base.EmbeddingSimilarityCalculator``
-  ``automata.symbol_embedding.symbol_embedding_builders.SymbolCodeEmbeddingBuilder``
-  ``automata.memory_store.symbol_code_embedding_handler.SymbolCodeEmbeddingHandler.process_embedding``

Example
-------

Although ``VectorDatabaseProvider`` is an abstract base class and cannot
be instantiated directly, the following example demonstrates how it
might be extended and used in practice:

.. code:: python

   from automata.core.base.database.vector_database import VectorDatabaseProvider
   from typing import Any, List

   class MyDatabaseProvider(VectorDatabaseProvider[Any, Any]):
       """Custom vector database provider."""

       def __len__(self) -> int:
           ...
           
       def save(self) -> None:
           ...
           
       def load(self) -> None:
           ...
           
       def clear(self) -> None:
           ...
           
       def get_ordered_keys(self) -> List[Any]:
           ...
           
       def get_all_ordered_embeddings(self) -> List[Any]:
           ...
           
       def add(self, entry: Any) -> None:
           ...
           
       def batch_add(self, entries: Any) -> None:
           ...
           
       def update_entry(self, entry: Any) -> None:
           ...
           
       def batch_update(self, entries: List[Any]) -> None:
           ...
           
       def entry_to_key(self, entry: Any) -> Any:
           ...
           
       def contains(self, key: Any) -> bool:
           ...
           
       def get(self, key: Any) -> Any:
           ...
           
       def batch_get(self, keys: List[Any]) -> List[Any]:
           ...
           
       def discard(self, key: List[Any]) -> None:
           ...
           
       def batch_discard(self, keys: List[Any]) -> None:
           ...

Note: The ``Any`` type is used as placeholders for an actual key type
``K`` and vector type ``V``. Replace it with the appropriate types based
on your specific context and vector database connection requirements.

Limitations
-----------

The ``VectorDatabaseProvider`` in itself doesn’t perform any operations,
it simply declares the methods that all vector database providers should
implement. The efficiency and effectiveness of these operations are
completely dependent on the implementation in the concrete classes that
extend ``VectorDatabaseProvider``.

Follow-up Questions:
--------------------

-  How should the handling of exceptions in the concrete subclasses be
   standardized?
-  Is there a provision to define a custom hashing algorithm in the
   ``entry_to_key`` method for unique keys generation?
-  How can we introduce asynchronous capabilities to increase
   performance where necessary?
