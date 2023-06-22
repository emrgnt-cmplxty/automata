NormType
========

``NormType`` is an enumeration that defines various types of
normalization techniques used in the ``SymbolSimilarity`` class when
calculating the similarity between embeddings. The available
normalization techniques are L1, L2, and softmax.

Overview
--------

``NormType`` provides three normalization options for use in the
``SymbolSimilarity`` class. By specifying a ``NormType``, you can
control how the embeddings are normalized before calculating similarity
scores. Knowing the appropriate normalization method for the use case
can lead to more accurate similarity results.

Related Symbols
---------------

-  ``automata.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata.core.embedding.symbol_similarity.SymbolSimilarity.__init__``

Example
-------

Here’s an example demonstrating how to create an instance of
``SymbolSimilarity`` using a custom ``NormType``.

.. code:: python

   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.embedding.embedding_types import NormType
   from automata.core.symbol.symbol_types import SymbolEmbeddingHandler

   symbol_embedding_manager = SymbolEmbeddingHandler()
   norm_type = NormType.L1

   symbol_similarity = SymbolSimilarity(symbol_embedding_manager, norm_type)

Limitations
-----------

The main limitation of ``NormType`` is that it only offers three
normalization options (L1, L2, and softmax). Additional normalization
techniques may be necessary for specific use cases, but they would have
to be implemented separately.

Follow-up Questions:
--------------------

-  Are there other normalization techniques that should be included in
   the ``NormType`` enumeration?
