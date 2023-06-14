SymbolEmbeddingHandler
======================

``SymbolEmbeddingHandler`` is a base class for handling symbol
embeddings in the Automata codebase. It provides methods to get and
update embeddings for a given symbol, while also supporting retrieval of
all supported symbols from the embedding provider. Derived classes are
expected to implement the abstract methods to get and update the
embeddings.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.symbol.symbol_types.SymbolDocEmbedding``
-  ``automata_docs.core.symbol.symbol_types.SymbolCodeEmbedding``

Example
-------

The following example demonstrates how to create a custom
``SymbolEmbeddingHandler`` implementation to handle symbol embeddings.

.. code:: python

   from automata_docs.core.embedding.symbol_embedding import SymbolEmbeddingHandler
   from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding
   from automata_docs.core.embedding.embedding_types import VectorDatabaseProvider, EmbeddingsProvider

   class CustomSymbolEmbeddingHandler(SymbolEmbeddingHandler):
       def __init__(self, embedding_db: VectorDatabaseProvider, embedding_provider: EmbeddingsProvider):
           super().__init__(embedding_db, embedding_provider)

       def get_embedding(self, symbol: Symbol) -> SymbolEmbedding:
           # Custom implementation to get the embedding for a symbol
           pass

       def update_embedding(self, symbol: Symbol):
           # Custom implementation to update the embedding for a symbol
           pass

   # Instantiate the custom handler
   custom_handler = CustomSymbolEmbeddingHandler(embedding_db, embedding_provider)

Limitations
-----------

As ``SymbolEmbeddingHandler`` is an abstract base class, it cannot be
instantiated directly, and it requires derived classes to implement its
abstract methods. The abstract nature ensures that the derived class
provides the appropriate methods but does not enforce common canonical
behavior for handling embeddings.

Follow-up Questions:
--------------------

-  Are there any canonical implementations of ``SymbolEmbeddingHandler``
   that could be used as a starting point when creating a custom
   handler?
