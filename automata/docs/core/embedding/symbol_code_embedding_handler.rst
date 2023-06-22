SymbolCodeEmbeddingHandler
==========================

``SymbolCodeEmbeddingHandler`` is a class that handles embeddings of
symbols derived from their source code. It is responsible for building,
storing, retrieving, and updating the embeddings of symbols in a given
database using a specified embedding provider. The class inherits from
``SymbolEmbeddingHandler`` and implements its abstract methods.

Overview
--------

When instantiating a ``SymbolCodeEmbeddingHandler``, it requires a
``VectorDatabaseProvider`` (i.e. ``embedding_db``) to store the
embeddings. Additionally, it needs an ``EmbeddingProvider``
(i.e. ``embedding_provider``) to compute the embeddings. The main
objective of this class is to facilitate the access and manipulation of
symbol embeddings. It supports the following operations:

-  Building an embedding for a symbol using its source code
-  Retrieving a symbol’s existing embedding from the database
-  Updating the embedding of a symbol, if needed, by comparing its
   source code or rebuilding the embedding

Related Symbols
---------------

-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.database.vector.VectorDatabaseProvider``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolCodeEmbedding``
-  ``automata.core.embedding.embedding_types.EmbeddingProvider``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``

Example
-------

The following example demonstrates how a ``SymbolCodeEmbeddingHandler``
instance is created with a mocked EmbeddingProvider and a mocked
JSONVectorDatabase for testing.

.. code:: python

   from unittest.mock import Mock, MagicMock
   from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
   from automata.core.symbol.symbol_types import Symbol
   from automata.core.embedding.embedding_types import EmbeddingProvider
   from automata.core.database.vector import JSONVectorDatabase

   # Mock EmbeddingProvider methods
   mock_embedding_provider = Mock(EmbeddingProvider)

   # Mock JSONVectorDatabase methods
   mock_embedding_db = MagicMock(JSONVectorDatabase)

   # Create a SymbolCodeEmbeddingHandler instance
   embedding_handler = SymbolCodeEmbeddingHandler(embedding_db=mock_embedding_db, embedding_provider=mock_embedding_provider)

   # Example of symbol to perform operations
   mock_symbol = Symbol.from_string(symbol_str="example_symbol")

   # Updating an embedding for a symbol
   embedding_handler.update_embedding(mock_symbol)

   # Getting an embedding for a symbol
   symbol_embedding = embedding_handler.get_embedding(mock_symbol)

Limitations
-----------

A limitation of ``SymbolCodeEmbeddingHandler`` lies in its dependency on
the provided ``embedding_db`` and ``embedding_provider``. If the
``VectorDatabaseProvider`` implementation does not satisfy the required
interface or if the ``EmbeddingProvider`` does not deliver accurate
embeddings, it may limit the capabilities of the handler. Moreover,
since the source code is required to build or update embeddings, there
might be errors if the source code is not provided correctly.

Follow-up Questions:
--------------------

-  What specific databases and embedding providers are typically
   compatible with ``SymbolCodeEmbeddingHandler``?
-  How are the embeddings computed for the symbols using the embedding
   providers?
