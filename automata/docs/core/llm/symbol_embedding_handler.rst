SymbolEmbeddingHandler
======================

``SymbolEmbeddingHandler`` is an abstract class used to handle the
embedding of symbols. It provides methods to get, update, and store
embeddings for symbols, thereby allowing easy access and management of
symbol embeddings.

Overview
--------

``SymbolEmbeddingHandler`` contains abstract methods for handling symbol
embeddings, including ``__init__``, ``get_embedding``, and
``update_embedding``. These methods are implemented in child classes
such as ``SymbolCodeEmbeddingHandler`` and
``SymbolDocEmbeddingHandler``, which handle the embedding of code
symbols and symbol documents, respectively. ``SymbolEmbeddingHandler``
also provides the ``get_all_supported_symbols`` method to retrieve all
available symbols in the embedding database.

Related Symbols
---------------

-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.embedding.doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.base.database.vector.VectorDatabaseProvider``

Example
-------

The following example demonstrates how to use a
``SymbolCodeEmbeddingHandler`` instance to retrieve the embedding for a
specific symbol.

.. code:: python

   from automata.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
   from automata.core.symbol.symbol_types import Symbol
   from automata.core.base.database.vector import JSONVectorDatabase
   from automata.core.embedding.embedding_provider import EmbeddingProvider

   # Create instances for the database and embedding provider
   embedding_db = JSONVectorDatabase(database_filename)
   embedding_provider = EmbeddingProvider()

   # Create a SymbolCodeEmbeddingHandler instance
   code_embedding_handler = SymbolCodeEmbeddingHandler(
       embedding_db=embedding_db, embedding_provider=embedding_provider
   )

   # Sample symbol
   symbol = Symbol.from_string("scip-python python automata .../`automata.core.base.tool`/ToolNotFoundError#__init__().")

   # Get the embedding for the symbol
   symbol_embedding = code_embedding_handler.get_embedding(symbol)

Limitations
-----------

The primary limitation of ``SymbolEmbeddingHandler`` is that it is an
abstract class, and thus cannot be instantiated directly. Instead, it
must be extended and implemented by other classes such as
``SymbolCodeEmbeddingHandler`` and ``SymbolDocEmbeddingHandler``.

Follow-up Questions:
--------------------

-  Are there any additional customization options for the
   ``SymbolEmbeddingHandler`` that should be included in this
   documentation?
