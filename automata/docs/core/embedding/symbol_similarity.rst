SymbolSimilarity
================

``SymbolSimilarity`` is a class providing functionality to compute
similarity scores between given query texts and symbols using
embeddings. You can retrieve the most similar symbols for a specific
query and create a dictionary mapping the similarity scores to each
symbol. Additionally, you have the flexibility to set the available
symbols for similarity calculation.

Overview
--------

The ``SymbolSimilarity`` class takes a ``SymbolCodeEmbeddingHandler``,
and an optional ``NormType`` to calculate similarity between query texts
and symbols. It offers methods to get available symbols, get the nearest
symbols for a query, and get the similarity dictionary for a query. The
class uses embeddings and a variety of similarity metrics for
determining the similarity between query texts and symbols.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingSimilarity``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata_docs.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.NormType``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSimilarity`` using a predefined ``SymbolCodeEmbeddingHandler``.

.. code:: python

   import numpy as np
   from automata_docs.core.embedding.code_embedding import SymbolCodeEmbeddingHandler
   from automata_docs.core.embedding.embedding_types import EmbeddingProvider, NormType
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity

   # Instance of a SymbolCodeEmbeddingHandler
   embedding_handler = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_provider=embedding_provider)

   # Create an instance of SymbolSimilarity
   symbol_similarity = SymbolSimilarity(symbol_embedding_manager=embedding_handler, norm_type=NormType.L2)

   # Set available symbols
   symbol_similarity.set_available_symbols(available_symbols)

   # Get the nearest entries for a query
   nearest_entries = symbol_similarity.get_nearest_entries_for_query("example query", k=5)

   # Get the query similarity dictionary
   query_similarity_dict = symbol_similarity.get_query_similarity_dict("example query")

Limitations
-----------

-  The primary limitation of ``SymbolSimilarity`` is its reliance on
   pre-trained embeddings, which means the quality of the similarity
   scores depends on the quality of the embeddings and the selected norm
   type. If embeddings do not accurately represent the symbols or the
   norm type is not suitable for the given problem, the similarity
   scores might not be as accurate.
-  As ``SymbolSimilarity`` uses ``SymbolCodeEmbeddingHandler`` to handle
   embeddings, if ``SymbolCodeEmbeddingHandler`` is not properly
   constructed or initialized, the class may not provide the desired
   results.

Follow-up Questions:
--------------------

-  How can we extend ``SymbolSimilarity`` for other types of embeddings
   or similarity measurements?
