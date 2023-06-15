SymbolSimilarity
================

Overview
--------

``SymbolSimilarity`` is a class used to calculate and retrieve the
similarity scores between a given query text and all the supported
symbols. This class can be used to find the most similar symbols for a
given query text as well as filter the available symbols based on
certain conditions. The class provides methods like
``get_available_symbols``, ``get_nearest_entries_for_query``, and
``get_query_similarity_dict``.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingSimilarity``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolSimilarity`` and find the most similar symbols to a given query
text.

.. code:: python

   import numpy as np
   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider, NormType
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity

   # Create instances of necessary classes
   embedding_db = JSONVectorDatabase("path/to/database")
   embedding_provider = EmbeddingsProvider()
   cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_provider=embedding_provider)
   symbol_similarity = SymbolSimilarity(cem)

   # Set sample query_text and find the most similar symbols
   query_text = "This is a sample query text"
   similar_symbols = symbol_similarity.get_nearest_entries_for_query(query_text, k=5)

Limitations
-----------

The ``SymbolSimilarity`` class assumes a specific format for the
embeddings and the symbols. It also depends on the
``EmbeddingsProvider`` class to create the embeddings for the query
texts. Changing the way embeddings are created or modifying the symbols
would require substantial changes to the class.

Follow-up Questions:
--------------------

-  How can the implementation of ``SymbolSimilarity`` be modified to
   support custom embeddings and symbol formats?
