EmbeddingNormType
=================

``EmbeddingNormType`` is an enumeration class that provides different
methods to normalize the embeddings vectors in the Automata’s core
functionalities. It is used in the process of comparing and ranking
symbol embeddings based on their similarity to a query.

Overview
--------

``EmbeddingNormType`` supports ``L1`` and ``L2`` methods. When used in
an embedding similarity calculator instance, this setting determines how
the distance between the query embedding vector and symbol embeddings
are calculated.

-  ``L1``: Calculates the L1 norm (Manhattan distance) between two
   vectors.
-  ``L2``: Calculates the L2 norm (Euclidean Distance) between two
   vectors.

``EmbeddingNormType`` is supplied as an argument to the
``EmbeddingSimilarityCalculator`` class during initialization,
determining the norm method used for all similarity calculations within
that instance.

Related Symbols
---------------

-  ``automata.symbol_embedding.base.SymbolCodeEmbedding``
-  ``automata.embedding.base.EmbeddingSimilarityCalculator``
-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``

Example
-------

.. code:: python

   from automata.embedding.base import EmbeddingNormType, EmbeddingSimilarityCalculator
   from automata.symbol_embedding.base import SymbolCodeEmbedding
   from automata.core.base.database.vector import JSONSymbolEmbeddingVectorDatabase

   # Assuming you have a set of symbol embeddings stored in a JSON database.
   database_path = "path_to_your_database.json"
   embedding_db = JSONSymbolEmbeddingVectorDatabase(database_path)

   # Assume we have a mock embedding provider 
   mock_provider = MockEmbeddingProvider()

   # Instantiate an EmbeddingSimilarityCalculator with L1 norm.
   similarity_calculator = EmbeddingSimilarityCalculator(
       embedding_provider=mock_provider,
       norm_type=EmbeddingNormType.L1,
   )

   # Get ordered embeddings from database and compute similarity of a query_text
   ordered_embeddings = embedding_db.get_all_ordered_embeddings()
   query_text = 'def initialize(x, y):'
   similarity_dict = similarity_calculator.calculate_query_similarity_dict(ordered_embeddings, query_text)

   # The keys of the returned dictionary are the symbols and the values are the similarity scores.
   most_similar_symbol = max(similarity_dict, key=similarity_dict.get)

   print(f"Symbol most similar to the query is {most_similar_symbol}")

Limitations
-----------

The ``EmbeddingNormType`` only supports L1 and L2 norm methods. While
these methods cover typical use cases in calculating document
similarity, there are other distance measurement norms which could be
useful in different contexts, such as cosine similarity or Hamming
distance.

Other limitations would be that the user must ensure to match the norm
type to the nature of the embeddings used - as certain norm types may
not be suitable or produce the desired results given the type or
characteristics of the embedding vectors.

Follow-up Questions:
--------------------

-  How could other norm types be added to the ``EmbeddingNormType``?
-  Could the norm type be dynamically set or changed for running
   instances of ``EmbeddingSimilarityCalculator``?
