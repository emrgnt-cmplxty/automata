EmbeddingNormType
=================

``EmbeddingNormType`` is an enumeration class that provides a set of
normalization types for symbol embeddings. The available types include
L1, L2, and softmax normalizations, which affect the way embeddings are
normalized during similarity calculations.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.tests.unit.test_symbol_embedding.test_add_new_embedding``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.tests.conftest.mock_embedding``
-  ``automata.core.base.symbol_embedding.SymbolEmbedding``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``
-  ``automata.core.base.symbol_embedding.SymbolCodeEmbedding``
-  ``automata.tests.unit.test_symbol_embedding.test_update_embedding``

Example
-------

The following example demonstrates how to use ``EmbeddingNormType`` with
``SymbolSimilarity``.

.. code:: python

   from automata.core.base.symbol import SymbolEmbedding
   from automata.core.symbol_embedding.similarity import SymbolSimilarity

   # Create an instance of SymbolSimilarity class with L2 normalization
   symbol_similarity = SymbolSimilarity(symbol_embedding_manager, norm_type=EmbeddingNormType.L2)

Limitations
-----------

The current implementation of ``EmbeddingNormType`` only supports L1,
L2, and softmax normalization methods. To use custom normalization
methods, the class and its usage in ``SymbolSimilarity`` would need to
be modified to support additional normalization types.

Follow-up Questions:
--------------------

-  Are there any plans to support custom normalization types within the
   ``EmbeddingNormType`` enumeration class?
