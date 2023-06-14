EmbeddingHandler
================

``EmbeddingHandler`` is an abstract class for handling the embedding of
symbols. It provides a way to obtain embeddings for symbols as well as
to update these embeddings. The class offers closely related symbols,
such as ``SymbolCodeEmbeddingHandler`` and
``SymbolDocEmbeddingHandler``.

Overview
--------

``EmbeddingHandler`` is used to handle the embeddings for symbols.
Developers can subclass this class to implement specific embedding
types. The abstract methods defined in this class are
``get_all_supported_symbols``, ``get_embedding``, and
``update_embedding``. The implementation of these methods is left to the
subclasses.

Related Symbols
---------------

-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbeddingHandler``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolEmbedding``
-  ``automata_docs.core.symbol.symbol_types.Symbol``

Example
-------

Here’s an example of how to use the ``SymbolCodeEmbeddingHandler``
class, which is a subclass of ``EmbeddingHandler``.

.. code:: python

   from automata_docs.core.embedding.embedding_types import VectorDatabaseProvider
   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler, EmbeddingsProvider
   from automata_docs.core.symbol.symbol_types import Symbol

   # Create an instance of SymbolCodeEmbeddingHandler
   embedding_db = VectorDatabaseProvider() # Replace with your own implementation of VectorDatabaseProvider
   embedding_provider = EmbeddingsProvider()

   code_embedding_handler = SymbolCodeEmbeddingHandler(embedding_db, embedding_provider)

   # Use the handler to get embeddings for specific symbols
   symbol = Symbol("example_symbol")
   embedding = code_embedding_handler.get_embedding(symbol)

Limitations
-----------

The primary limitation of ``EmbeddingHandler`` is that it only supports
specific symbol types. Developers looking to use non-supported symbol
types would need to implement their own subclasses of
``EmbeddingHandler``. Additionally, the ``EmbeddingHandler`` class
itself is an abstract class, so developers will need to use subclasses
or create new subclasses that implement the abstract methods.

Follow-up Questions:
--------------------

-  Are there any other limitations or caveats to using the
   ``EmbeddingHandler`` class?
