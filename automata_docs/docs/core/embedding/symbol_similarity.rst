SymbolSimilarity
================

``SymbolSimilarity`` is a class that calculates the similarity between a
given query text and a set of supported symbols. It uses embeddings to
represent each symbol and the query text and computes the similarity
scores between the embeddings. The similarity scores can be used, for
example, to find the closest symbols to the query text in a search
context.

Overview
--------

The ``SymbolSimilarity`` class holds an instance of
``SymbolCodeEmbeddingHandler`` and maintains dictionaries for mapping
symbols to indices and vice versa. It also provides methods for
retrieving available symbols, computing the similarity between the query
text and symbols, and getting the nearest entries for a given query. The
class has the ability to filter the list of available symbols, which can
be helpful in cases where only a specific set of symbols is of interest.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingSimilarity``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.database.vector.VectorDatabaseProvider``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.core.symbol.symbol_types.SymbolReference``

Example
-------

The following example demonstrates how to create and use an instance of
``SymbolSimilarity`` to find the most similar symbol to a given query
text.

.. code:: python

   from automata_docs.core.embedding.symbol_embedding import SymbolCodeEmbeddingHandler
   from automata_docs.core.database.vector import JSONVectorDatabase
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider, SymbolCodeEmbedding
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   import numpy as np

   # Initialize an instance of JSONVectorDatabase
   temp_output_filename = "dummy_embedding_database.json"
   embedding_db = JSONVectorDatabase(temp_output_filename)

   # Create an instance of SymbolCodeEmbeddingHandler
   mock_provider = EmbeddingsProvider()
   cem = SymbolCodeEmbeddingHandler(embedding_db=embedding_db, embedding_provider=mock_provider)

   # Create an instance of SymbolSimilarity
   symbol_similarity = SymbolSimilarity(cem)

   # Add embeddings to the SymbolCodeEmbeddingHandler
   symbol = "dummy_symbol"
   vector = np.array([1, 0, 0, 0])
   embedding = SymbolCodeEmbedding(symbol=symbol, vector=vector, source_code="symbol")
   cem.add_embedding(embedding)

   # Find the most similar symbol for a given query text
   query_text = "dummy_query"
   cem.embedding_provider.build_embedding.return_value = np.array([1, 0, 0, 0])
   result = symbol_similarity.get_nearest_entries_for_query(query_text, k=1)
   assert list(result.keys()) == [symbol]

Limitations
-----------

The ``SymbolSimilarity`` class relies on the usage of embeddings to
represent symbols and query texts. As a result, its performance depends
on the quality of the embeddings. Moreover, the similarity metric
assumes that embeddings are continuous, high-dimensional vectors that
may not be appropriate for all use cases. In addition, the system does
not consider the context of symbols, which may result in false positives
or negatives in identifying relevant symbols.

Follow-up Questions:
--------------------

-  How can we improve the quality of the embeddings to better represent
   the symbols and their relationships?
-  Are there alternative similarity metrics that could be more suitable
   for calculating symbol similarity in certain cases?
-  How can we incorporate contextual information into the similarity
   calculation to improve the relevance of the results?
