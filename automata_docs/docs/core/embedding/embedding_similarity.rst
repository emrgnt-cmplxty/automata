EmbeddingSimilarity
===================

``EmbeddingSimilarity`` is an abstract base class for calculating the
similarity between a given query and embeddings of symbols. It is meant
to be subclassed to implement the methods for calculating similarity and
retrieving nearest symbols to a query based on their embeddings.

Overview
--------

``EmbeddingSimilarity`` requires three main abstract methods to be
implemented in a subclass:

1. ``__init__``: Initialize the ``EmbeddingSimilarity`` subclass with
   the required parameters, such as an ``EmbeddingHandler``, and
   optionally a ``NormType``.
2. ``get_nearest_entries_for_query``: Given a query and an integer
   ``k_nearest``, return the ``k_nearest`` symbols that are most similar
   to the query, based on their embeddings.
3. ``get_query_similarity_dict``: Given a query, return a dictionary
   containing the similarity scores between the query and all available
   symbols.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.database.vector.VectorDatabaseProvider.calculate_similarity``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``

Example
-------

The following is an example demonstrating how to create and use a custom
``EmbeddingSimilarity`` subclass to calculate similarities between a
given query and available symbols.

.. code:: python

   from automata_docs.core.embedding.embedding_types import EmbeddingSimilarity
   from automata_docs.core.symbol.symbol_types import Symbol
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity

   class CustomEmbeddingSimilarity(EmbeddingSimilarity):
       def __init__(self, symbol_embedding_manager, norm_type):
           super().__init__(symbol_embedding_manager, norm_type)

       def get_nearest_entries_for_query(self, query_text, k_nearest):
           # Implement method to retrieve k_nearest symbols based on their embeddings
           pass

       def get_query_similarity_dict(self, query_text):
           # Implement method to return a dictionary with similarity scores between the query and all available symbols
           pass

   # Instantiate and use the custom subclass
   symbol_similarity_instance = CustomEmbeddingSimilarity(symbol_embedding_manager, norm_type)
   nearest_entries = symbol_similarity_instance.get_nearest_entries_for_query("example query", k_nearest=5)
   query_similarity = symbol_similarity_instance.get_query_similarity_dict("example query")

Limitations
-----------

``EmbeddingSimilarity`` is an abstract base class and cannot be used
directly. It must be subclassed, and the abstract methods must be
implemented in the subclass to suit the requirements of the specific use
case.

Follow-up Questions:
--------------------

-  How can we handle different types of embeddings when calculating
   similarity in the subclass implementations?
-  Can we provide different similarity measures apart from cosine
   similarity when calculating the similarity between a query and
   embeddings of symbols?
