NormType
========

``NormType`` is an enumeration class representing the different
normalization techniques available for use while calculating similarity
in a ``SymbolSimilarity`` object. It offers three options, L1, L2, and
softmax for normalization, which can be utilized by the
``SymbolSimilarity`` class while computing similarities between symbols
in a related codebase.

Related Symbols
---------------

-  ``automata.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata.core.symbol.symbol_types.Symbol``

Example
-------

The following example demonstrates how to create a ``SymbolSimilarity``
instance using a custom ``NormType``.

.. code:: python

   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.embedding.embedding_types import NormType
   from automata.core.embedding.manager.code_embedding_manager import SymbolCodeEmbeddingHandler

   symbol_embedding_manager = SymbolCodeEmbeddingHandler()
   custom_norm_type = NormType.L1

   symbol_similarity = SymbolSimilarity(symbol_embedding_manager, custom_norm_type)

Limitations
-----------

One potential limitation of using different normalization techniques
within ``SymbolSimilarity`` is the possibility of differences in the
interpretation of similarity results. While some techniques like L2
(Euclidean) are more commonly used and understood, others like L1 or
softmax might be less familiar. Additionally, the choice of
normalization technique can impact the efficiency of the similarity
calculation algorithm.

Follow-up Questions:
--------------------

-  Are there other normalization techniques that could be added to the
   ``NormType`` class?
-  How do different normalization techniques impact the performance and
   interpretation of similarity calculations?
