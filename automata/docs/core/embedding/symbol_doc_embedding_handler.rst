SymbolDocEmbeddingHandler
=========================

``SymbolDocEmbeddingHandler`` is a class designed to manage and store
embeddings for the documentation of any given symbol in the code. It
extends the ``EmbeddingProvider`` and ``SymbolEmbeddingHandler``
classes, allowing for easy integration with other parts of the Automata
system. The class provides functionality for building, updating, and
retrieving embeddings for symbol documentation, as well as fetching
completed documentations through a completion provider.

Overview
--------

The primary responsibilities of the ``SymbolDocEmbeddingHandler`` class
include:

-  Building documentation embeddings based on the symbol’s source code
   and other related contextual information
-  Updating existing documentation embeddings or rolling them forward
   when necessary
-  Retrieving the documentation embeddings of a symbol
-  Fetching completed documentation via the
   ``LLMChatCompletionProvider``

Additionally, the ``SymbolDocEmbeddingHandler`` class utilizes various
other Automata components to perform its functions.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.core.llm.embedding.EmbeddingProvider``
-  ``automata.core.llm.embedding.SymbolEmbeddingHandler``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.base.SymbolDocEmbedding``

Example
-------

The following example demonstrates the usage of
``SymbolDocEmbeddingHandler`` to build and update documentation
embeddings.

.. code:: python

   from automata.core.embedding.doc_embedding import SymbolDocEmbeddingHandler
   from automata.core.llm.completion import LLMChatCompletionProvider
   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.context.py.retriever import PyContextRetriever

   symbol = ...
   embedding_db = ...
   embedding_provider = ...
   completion_provider = LLMChatCompletionProvider()
   symbol_search = SymbolSearch()
   retriever = PyContextRetriever()

   # Initialize the SymbolDocEmbeddingHandler
   handler = SymbolDocEmbeddingHandler(
       embedding_db=embedding_db,
       embedding_provider=embedding_provider,
       completion_provider=completion_provider,
       symbol_search=symbol_search,
       retriever=retriever
   )

   # update or build the documentation embedding for a given symbol
   handler.update_embedding(symbol)

   # Retrieve the documentation embedding
   doc_embedding = handler.get_embedding(symbol)

Limitations
-----------

A notable limitation of the ``SymbolDocEmbeddingHandler`` is its
dependency on the Automata components and how they interact. Specific
logic may be required to update the embedding and associated
documentation, which might be non-trivial depending on the dependencies.

Follow-up Questions:
--------------------

-  What could be the sample examples for the symbol documentation that
   ``SymbolDocEmbeddingHandler`` can handle?
