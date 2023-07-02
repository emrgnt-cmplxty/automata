SymbolDatabaseProvider
======================

``SymbolDatabaseProvider`` is an abstract base class for different types
of database providers. The class defines abstract methods for adding,
clearing, checking, discarding, getting, loading, saving, and updating
embeddings in the database.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol_embedding.base.SymbolEmbedding``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.base.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.tests.utils.factories.symbol_search_live``

Example
-------

The following is an example of a custom implementation of
``SymbolDatabaseProvider``.

.. code:: python

   from automata.core.base.database.provider import SymbolDatabaseProvider
   from automata.core.symbol.base import Symbol, SymbolEmbedding

   class CustomDatabase(SymbolDatabaseProvider):
       def __init__(self):
           self.data = {}

       def add(self, embedding: SymbolEmbedding):
           self.data[embedding.symbol] = embedding

       def clear(self):
           self.data = {}

       def contains(self, symbol: Symbol) -> bool:
           return symbol in self.data

       def discard(self, symbol: Symbol):
           if symbol in self.data:
               del self.data[symbol]

       def get(self, symbol: Symbol):
           return self.data.get(symbol)

       def load(self):
           pass

       def save(self):
           pass

       def update(self, embedding: SymbolEmbedding):
           
           if embedding.symbol in self.data:
               self.data[embedding.symbol] = embedding

Limitations
-----------

As an abstract base class, ``SymbolDatabaseProvider`` only provides the
blueprint for different types of database providers. It cannot be
instantiated directly and must be subclassed to create a custom
implementation.

Follow-up Questions:
--------------------

-  What is the most efficient way to store embeddings in a custom
   implementation of ``SymbolDatabaseProvider``?
