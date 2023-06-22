SymbolSimilarity
================

``SymbolSimilarity`` is a class used to compute symbolic similarity
between source code elements in a given codebase, such as classes,
methods, or local variables. This is achieved using an embedding
provider that creates vector representations for source code elements,
allowing the calculation of similarities using a specified norm type
(e.g., L2 norm).

The class utilizes a ``SymbolEmbeddingHandler`` object, which is
responsible for managing the embeddings associated with symbols. It
provides methods for calculating similarities, finding the nearest
symbols to a given query, and setting the available symbols for
similarity calculation.

Related Symbols
---------------

-  ``automata.core.embedding.embedding_types.SymbolEmbeddingHandler``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.embedding.embedding_types.EmbeddingProvider``
-  ``automata.core.embedding.embedding_types.NormType``
-  ``automata.core.embedding.embedding_types.EmbeddingSimilarity``

Example
-------

The following example demonstrates how to create a ``SymbolSimilarity``
object using a mocked ``SymbolEmbeddingHandler`` and ``NormType`` L2.

.. code:: python

   import numpy as np
   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.embedding.embedding_types import SymbolEmbeddingHandler, NormType
   from unittest.mock import MagicMock

   # Mock a SymbolEmbeddingHandler instance
   mock_handler = MagicMock(SymbolEmbeddingHandler)

   # Create an instance of SymbolSimilarity
   symbol_similarity = SymbolSimilarity(symbol_embedding_manager=mock_handler, norm_type=NormType.L2)

   # Calculate the similarity between a given query text and the available code symbols
   query = "this is a sample query text"
   result = symbol_similarity.get_query_similarity_dict(query_text=query)

   # Should return a dictionary mapping each symbol's uri to its similarity score with the query

Limitations
-----------

``SymbolSimilarity`` assumes that the embeddings created by the provided
``EmbeddingProvider`` are of good quality and accurately represent the
code elements. The quality of the similarity results will depend on the
quality of the embeddings themselves.

Additionally, when calculating the similarity, ``SymbolSimilarity`` only
considers supported symbols in the given ``SymbolEmbeddingHandler``.
This means that if a symbol is not supported by the handler, it will not
be included in the calculation.

Follow-up Questions:
--------------------

-  Is there any method for adjusting the similarity algorithm to improve
   the quality of results?
-  What are the limitations of the norm types (e.g., L2 norm) used for
   similarity calculation, and is there any other preferred norm type?
