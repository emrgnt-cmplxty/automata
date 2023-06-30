SymbolCodeEmbeddingHandler
==========================

``SymbolCodeEmbeddingHandler`` is a class responsible for handling
embeddings of symbols in the source code. It provides methods to build,
update, and retrieve embeddings of symbols. The class interacts with
other components such as ``VectorDatabaseProvider`` and
``EmbeddingProvider``. It is used in tasks like symbol similarity
calculations and code completion.

Overview
--------

``SymbolCodeEmbeddingHandler`` supports the generation and management of
symbol code embeddings. The class takes an instance of
``VectorDatabaseProvider`` and ``EmbeddingProvider`` as input, which
handle the storage and generation of embeddings, respectively. The key
methods available in this class include ``build_embedding``,
``get_embedding``, and ``update_embedding``. These methods enable
retrieving symbol embeddings, building new ones, and updating existing
embeddings when necessary.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.core.llm.core.EmbeddingProvider``
-  ``automata.core.base.symbol.Symbol``
-  ``automata.core.base.symbol_embedding.SymbolCodeEmbedding``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``

Example
-------

The following example demonstrates how to create an instance of
``SymbolCodeEmbeddingHandler`` and retrieve the embedding of a symbol:

.. code:: python

   from automata.core.base.database.vector import VectorDatabaseProvider
   from automata.core.llm.core import EmbeddingProvider, SymbolCodeEmbeddingHandler
   from automata.core.base.symbol import Symbol

   # Mocked objects for demonstration purposes
   mock_embedding_db = VectorDatabaseProvider()
   mock_embedding_provider = EmbeddingProvider()

   symbol_handler = SymbolCodeEmbeddingHandler(
       embedding_db=mock_embedding_db,
       embedding_provider=mock_embedding_provider
   )

   # Assuming a Symbol object is available
   symbol = Symbol()

   embedding = symbol_handler.get_embedding(symbol)

Limitations
-----------

``SymbolCodeEmbeddingHandler`` depends on the existence of a
``VectorDatabaseProvider`` instance for storing embeddings and an
``EmbeddingProvider`` instance for generating embeddings. The class
raises a ``ValueError`` if the symbol has no source code for updating
its embedding.

Follow-up Questions:
--------------------

-  How can we manage custom ``EmbeddingProvider`` and
   ``VectorDatabaseProvider`` instances with
   ``SymbolCodeEmbeddingHandler``?
