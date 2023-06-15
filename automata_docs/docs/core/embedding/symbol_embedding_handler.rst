SymbolEmbeddingHandler
======================

``SymbolEmbeddingHandler`` is an abstract class that manages and handles
the embeddings of symbols in the ``automata_docs`` project. It provides
functionalities to retrieve, update, and work with embeddings of
different symbols while interacting with external ``embedding_db``
databases and ``embedding_provider`` providers for acquiring the
embeddings. This class is part of the larger embeddings management
system that covers ``SymbolCodeEmbeddingHandler``,
``SymbolDocEmbeddingHandler``, and all the related ``SymbolEmbedding``
objects.

Overview
--------

The primary purpose of ``SymbolEmbeddingHandler`` is to facilitate the
management of symbol embeddings within ``automata_docs``. It offers an
extensible and customizable interface for other embedding handlers to
inherit from and implement. The class features abstract methods like
``get_embedding`` and ``update_embedding`` that should be implemented by
derived classes. The ``SymbolEmbeddingHandler`` also maintains a list of
all the supported symbols managed by the embedding provider.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.database.vector.VectorDatabaseProvider``

Example
-------

The following is an example demonstrating how to use a derived class
``SymbolCodeEmbeddingHandler`` from ``SymbolEmbeddingHandler``.

.. code:: python

   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider
   from automata_docs.core.symbol.symbol_types import Symbol

   embedding_db = JSONVectorDatabase("path/to/database.json")
   embedding_provider = EmbeddingsProvider()

   handler = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_provider=embedding_provider)

   symbol = Symbol.from_string("your-symbol-string-representation")

   embedded_symbol = handler.get_embedding(symbol)

Limitations
-----------

The main limitation of ``SymbolEmbeddingHandler`` is that it is an
abstract class that relies on derived classes for specific
implementations. In its current form, it cannot be used directly and
requires an understanding of the embedding handling mechanism.

Follow-up Questions:
--------------------

-  What are the actual implementations for retrieving and updating
   embeddings in ``SymbolEmbeddingHandler``-derived classes?
