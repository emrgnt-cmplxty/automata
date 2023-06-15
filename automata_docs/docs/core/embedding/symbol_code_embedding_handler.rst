SymbolCodeEmbeddingHandler
==========================

``SymbolCodeEmbeddingHandler`` is a class that handles the embedding of
code symbols. It extends ``EmbeddingHandler`` abstract base class and
has methods to get, update, and calculate similarity of symbol
embeddings.

Overview
--------

``SymbolCodeEmbeddingHandler`` provides a way to interact with a
symbol’s code embedding. It uses an ``embedding_db``
(VectorDatabaseProvider) to store the embeddings, and an optional
``embedding_provider`` (EmbeddingsProvider) to get the embeddings from.
The class offers methods to get an existing embedding, update the
embedding with new symbols, and calculate similarity between symbols
based on their embeddings.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolCodeEmbedding``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolCodeEmbeddingHandler`` using a ``VectorDatabaseProvider`` and
update the embedding for a given symbol.

.. code:: python

   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider
   from automata_docs.core.database.vector import JSONVectorDatabase

   # Initialize a JSONVectorDatabase to store the embeddings
   embedding_db = JSONVectorDatabase(<JSON_FILE_PATH>)

   # Initialize the SymbolCodeEmbeddingHandler
   embedding_handler = SymbolCodeEmbeddingHandler(embedding_db)

   # Update the embedding for a given symbol
   symbol = SymbolGraph().get_main_class_symbol('automata_docs.core.agent.automata_agent.snippets_classes')
   embedding_handler.update_embedding(symbol)

Limitations
-----------

``SymbolCodeEmbeddingHandler`` relies on ``VectorDatabaseProvider`` to
store the embeddings and retrieve them when required. The performance of
the handler is tightly coupled with the performance of the
``VectorDatabaseProvider``. Moreover, the handler uses pre-trained
models to generate embeddings, and the quality of retrieved embeddings
depends on the underlying machine learning models.

Follow-up Questions:
--------------------

-  Can custom embeddings be provided for symbols instead of relying on
   pre-trained models in the ``SymbolCodeEmbeddingHandler`` class?

Please consult the source code or unit tests for explanations on the
other methods of the class, such as ``get_embedding``.
