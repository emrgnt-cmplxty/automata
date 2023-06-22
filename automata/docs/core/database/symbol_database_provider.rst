SymbolDatabaseProvider
======================

``SymbolDatabaseProvider`` is an abstract base class for different types
of database providers that store and manage symbol embeddings and
related data. The class provides a set of abstract methods to be
implemented by concrete database providers, allowing flexible
implementations for various database systems. The class collaborates
closely with related symbols such as ``Symbol`` and ``SymbolEmbedding``.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_references``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.tests.utils.factories.symbol_search_live``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.tests.unit.test_symbol_search.test_process_queries``
-  ``automata.core.database.vector.VectorDatabaseProvider``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.core.symbol.symbol_types.SymbolEmbedding``

Example
-------

The following example demonstrates how to create a custom
SymbolDatabaseProvider by extending the abstract base class and
implementing the required methods:

.. code:: python

   import abc
   from typing import Any
   from automata.core.symbol.symbol_types import Symbol, SymbolEmbedding
   from automata.core.database.provider import SymbolDatabaseProvider

   class CustomSymbolDatabaseProvider(SymbolDatabaseProvider):
       def __init__(self):
           self.embeddings = {}

       def add(self, embedding: SymbolEmbedding) -> Any:
           self.embeddings[embedding.symbol] = embedding

       def clear(self) -> Any:
           self.embeddings.clear()

       def contains(self, symbol: Symbol) -> bool:
           return symbol in self.embeddings

       def discard(self, symbol: Symbol) -> Any:
           self.embeddings.pop(symbol, None)

       def get(self, symbol: Symbol) -> Any:
           return self.embeddings.get(symbol)

       def load(self) -> Any:
           pass

       def save(self) -> Any:
           pass

       def update(self, embedding: SymbolEmbedding) -> Any:
           self.embeddings[embedding.symbol] = embedding

Limitations
-----------

``SymbolDatabaseProvider`` is an abstract base class, and cannot be
instantiated directly. Implementations must provide concrete subclasses
implementing the required abstract methods. This allows for flexibility
in the implementation, but may require additional effort to create
suitable providers for different database systems.

Follow-up Questions:
--------------------

-  Are there any specific storage systems or frameworks that should be
   supported by default with ``SymbolDatabaseProvider``?
