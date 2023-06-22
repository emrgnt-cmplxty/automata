EmbeddingSimilarity
===================

``EmbeddingSimilarity`` is an abstract base class that provides an
interface for estimating the similarity between an embedding and a
collection of symbols. This class contains two abstract methods,
``get_nearest_entries_for_query`` and ``get_query_similarity_dict``,
which return the k nearest symbols and the similarity between a given
query and all symbols, respectively.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``
-  ``automata.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.core.database.vector.VectorDatabaseProvider.calculate_similarity``
-  ``automata.tests.unit.test_symbol_embedding.test_update_embeddings``
-  ``automata.core.database.vector.JSONVectorDatabase.calculate_similarity``
-  ``automata.tests.unit.test_symbol_embedding.test_add_new_embedding``
-  ``automata.core.symbol.symbol_types.SymbolEmbedding``

Example
-------

The following is an example demonstrating how to subclass
``EmbeddingSimilarity`` and implement its abstract methods.

.. code:: python

   from automata.core.embedding.embedding_types import EmbeddingSimilarity

   class MyEmbeddingSimilarity(EmbeddingSimilarity):

       def get_nearest_entries_for_query(self, query_text: str, k_nearest: int) -> Dict[Any, float]:
           # Implement logic for finding the k nearest entries for the given query text
           pass

       def get_query_similarity_dict(self, query_text: str) -> Dict[Any, float]:
           # Implement logic for finding the similarity between the query text and all supported symbols
           pass

Limitations
-----------

As an abstract base class, ``EmbeddingSimilarity`` cannot be
instantiated directly. It serves as a template for creating custom
classes to estimate embedding similarity by having the custom class
inherit from ``EmbeddingSimilarity`` and implementing its abstract
methods. Additionally, the example provided above uses dummy ``pass``
statements for the custom implementation of the abstract methods. In a
real implementation, these methods need to be replaced with appropriate
logic for obtaining the desired similarity measures.

Follow-up Questions:
--------------------

-  How can the supplied context be expanded to provide more
   comprehensive and executable examples for ``EmbeddingSimilarity``
   subclasses?
