SymbolSimilarity
================

``SymbolSimilarity`` is a class that calculates the similarity between
symbols using their embeddings. The similarity calculations can be used
to find the most similar symbols to a given query text or to calculate
the similarity scores for all symbols in a database.

Overview
--------

``SymbolSimilarity`` is built using a ``SymbolEmbeddingHandler``
instance to manage symbol embeddings and an ``EmbeddingProvider`` to
generate embeddings for query texts. It is capable of computing
similarity scores using different norm types (specified by the optional
``norm_type`` parameter).

Two main methods are provided: ``get_nearest_entries_for_query`` and
``get_query_similarity_dict``. These methods can be used to find the
most similar symbols to a given query text, and to calculate the
similarity scores for all symbols in the database, respectively.

Related Symbols
---------------

-  ``automata.core.llm.core.SymbolEmbeddingHandler``
-  ``automata.core.llm.core.EmbeddingProvider``
-  ``automata.core.llm.core.EmbeddingNormType``
-  ``automata.core.base.symbol.Symbol``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSimilarity`` and use it to find the most similar symbols to a
given query text.

.. code:: python

   import numpy as np
   from automata.core.llm.core import (
       SymbolEmbeddingHandler,
       EmbeddingProvider,
       EmbeddingNormType,
       SymbolSimilarity,
   )
   from automata.core.base.symbol import Symbol

   # Create a mock SymbolEmbeddingHandler and EmbeddingProvider
   symbol_embedding_handler = SymbolEmbeddingHandler(...)
   embedding_provider = EmbeddingProvider(...)

   # Instantiate SymbolSimilarity
   symbol_similarity = SymbolSimilarity(
       symbol_embedding_manager=symbol_embedding_handler,
       norm_type=EmbeddingNormType.L2,
   )

   # Find the k most similar symbols to a query text
   query_text = "example query text"
   k = 5
   similar_symbols = symbol_similarity.get_nearest_entries_for_query(query_text, k=k)

Limitations
-----------

``SymbolSimilarity`` relies on the ``SymbolEmbeddingHandler`` and
``EmbeddingProvider`` being properly set up with the correct embeddings
and data. If the embeddings used by these classes are of low quality or
not appropriate for the compared symbols, the similarity calculation may
not provide useful results. Additionally, the class assumes that the
embeddings are dense vectors using ``numpy`` arrays, and might not work
with other types of embeddings.

Follow-up Questions:
--------------------

-  How can we improve the quality of the embeddings used by
   ``SymbolSimilarity`` to ensure better similarity calculations?
