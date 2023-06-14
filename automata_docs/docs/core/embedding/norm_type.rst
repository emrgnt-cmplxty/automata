NormType
========

``NormType`` is an enumeration class that provides different norm types
to be used for calculating similarity in embeddings. It includes three
options: L1, L2, and SOFTMAX.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingSimilarity``

Example
-------

The following example demonstrates how to use ``NormType`` to initialize
an instance of ``SymbolSimilarity``.

.. code:: python

   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   from automata_docs.core.embedding.dummy_handlers import DummyEmbeddingManager
   from automata_docs.core.embedding.embedding_types import NormType

   embedding_manager = DummyEmbeddingManager()
   norm_type = NormType.L2

   symbol_similarity = SymbolSimilarity(embedding_manager, norm_type)

Discussion
----------

``NormType`` provides a simple way to select different types of norms
used for calculating similarity in various embedding scenarios. It is
primarily used with the ``SymbolSimilarity`` class to specify which norm
type should be applied when looking for similarities between symbols. By
providing different norm types, it allows for increased flexibility
within the embedding handling process.

Limitations
-----------

``NormType`` currently supports only three options: L1, L2, and SOFTMAX.
The implementation of additional norm types would require modifications
to related classes such as ``SymbolSimilarity`` and
``EmbeddingSimilarity``. Moreover, ``NormType`` is limited by the
underlying functionality provided by its associated classes and may not
suit all use cases.

Follow-up Questions:
--------------------

-  Are there any additional norm types that should be supported in
   ``NormType``?
