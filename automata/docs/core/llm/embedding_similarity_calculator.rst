EmbeddingSimilarityCalculator
=============================

``EmbeddingSimilarityCalculator`` is an abstract base class that
provides a method for calculating the similarity between a query string
and a set of symbols.

Overview
--------

``EmbeddingSimilarityCalculator`` uses the abstractmethod
``calculate_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]``
that each derived class needs to implement. The method is expected to
calculate and return a dictionary mapping each symbol to a float that
represents its similarity to the ``query_text``. The similarity
calculation is generally done by comparing the embeddings of the query
and the symbols.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarityCalculator``
-  ``automata.core.agent.tool.tool_utils.DependencyFactory.create_symbol_code_similarity``

Example
-------

The following is an example demonstrating the creation of a custom
EmbeddingSimilarityCalculator -

.. code:: python

   from automata.core.llm.embedding import EmbeddingSimilarityCalculator
   from typing import Dict
   from automata.core.symbol.base import Symbol

   class MyEmbeddingSimilarityCalculator(EmbeddingSimilarityCalculator):
       def calculate_query_similarity_dict(self, query_text: str) -> Dict[Symbol, float]:
           # Implement the method depending on your specific way to calculate similarity
           pass

Limitations
-----------

As ``EmbeddingSimilarityCalculator`` is an abstract class, you cannot
create an instance of ``EmbeddingSimilarityCalculator`` directly. You
must inherit the class and implement the
``calculate_query_similarity_dict`` method. This method assumes that the
similarity between the query and a symbol can be reduced to a single
float number which might not always be the case.

Follow-up Questions:
--------------------

-  What kind of embeddings are usually used by this method and how are
   they obtained?
-  What is the best practice way of implementing the
   ``calculate_query_similarity_dict`` method?
-  What kind of similarity measures are generally used?
-  How can the similarity measure be customized in a class inheriting
   ``EmbeddingSimilarityCalculator``?
