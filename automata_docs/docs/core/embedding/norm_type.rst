NormType
========

``NormType`` is an enumeration in the
``automata_docs.core.embedding.embedding_types`` module. It represents
different norm types that can be used for normalizing embeddings and
calculating similarity between embeddings. ``NormType`` values are used
as parameters for methods in related classes like ``SymbolSimilarity``
to specify which norm to use.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.database.vector.VectorDatabaseProvider``

Overview
--------

``NormType`` enumeration includes the following members:

-  ``NormType.L1``: Use L1 norm (also known as Manhattan distance) for
   normalization.
-  ``NormType.L2``: Use L2 norm (also known as Euclidean distance) for
   normalization.
-  ``NormType.SOFTMAX``: Use softmax normalization.

These norm types determine how to normalize embeddings and calculate the
similarity between them for subsequent processing and comparisons.

Example
-------

The following example demonstrates how to use ``NormType`` to initialize
a ``SymbolSimilarity`` instance.

.. code:: python

   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   from automata_docs.core.embedding.embedding_types import NormType
   from automata_docs.core.embedding.symbol_code_embedding_handler import SymbolCodeEmbeddingHandler

   symbol_embedding_manager = SymbolCodeEmbeddingHandler()
   norm_type = NormType.L2
   symbol_similarity = SymbolSimilarity(symbol_embedding_manager, norm_type=norm_type)

Limitations
-----------

``NormType`` is specific to the ``automata_docs`` package and may not be
applicable or recognized in other contexts. Additionally, it only
supports three norm types (L1, L2, and softmax). Any other norm types or
custom normalization techniques would need to be implemented separately.

Follow-up Questions:
--------------------

-  Are there plans to expand ``NormType`` with additional normalization
   options?
