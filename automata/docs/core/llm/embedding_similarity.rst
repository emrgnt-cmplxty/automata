EmbeddingSimilarity
===================

``EmbeddingSimilarity`` is an abstract class that provides a way to get
the similarity between a given query string and a set of symbols. It
defines two main methods: ``get_nearest_entries_for_query`` and
``get_query_similarity_dict``. This class can be subclassed to implement
specific similarity measures based on different embedding
representations.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.core.base.symbol.Symbol``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``

Methods
-------

-  ``get_nearest_entries_for_query(self, query_text: str, k_nearest: int) -> Dict[Symbol, float]``:
   An abstract method to get the k-nearest symbols to a query.
-  ``get_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]``:
   An abstract method to get the similarity between a query and all
   symbols.

Example
-------

In order to use an ``EmbeddingSimilarity`` class, create a subclass that
implements the ``get_nearest_entries_for_query`` and
``get_query_similarity_dict`` methods. The following example
demonstrates a simple subclass that always returns an empty dictionary
for both methods:

.. code:: python

   from automata.core.llm.core import EmbeddingSimilarity

   class DummySimilarity(EmbeddingSimilarity):
       def get_nearest_entries_for_query(self, query_text: str, k_nearest: int) -> Dict[Symbol, float]:
           return {}

       def get_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
           return {}

Limitations
-----------

-  ``EmbeddingSimilarity`` is an abstract class that only provides a
   framework for implementing specific similarity measures. To create a
   usable similarity measure, one needs to subclass this class and
   implement the methods according to the desired similarity algorithm.
-  The similarity measures are based on embeddings, which can vary in
   quality and performance. Different embedding approaches may lead to
   different results based on their inherent strengths and weaknesses.

Follow-up Questions:
--------------------

-  Are there examples of other subclasses of ``EmbeddingSimilarity``?
