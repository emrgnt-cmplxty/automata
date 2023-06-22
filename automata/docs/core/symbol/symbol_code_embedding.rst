SymbolCodeEmbedding
===================

``SymbolCodeEmbedding`` is a class that represents the embeddings for
symbol code. It is used to store and manage the embedding vectors for
symbols, which can be used for symbol similarity search, code retrieval,
and other tasks. The class extends the abstract base class
``SymbolEmbedding`` and provides an additional ``source_code`` attribute
to store the associated source code.

Overview
--------

``SymbolCodeEmbedding`` is mainly used for creating, storing, and
managing the code embeddings for symbols. The class provides methods to
initialize an instance with a symbol, its source code, and a NumPy array
representing its vector. It is widely used in various modules such as
symbol similarity search, embedding handler, and vector database
management.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.tests.unit.test_symbol_similarity.test_get_nearest_symbols_for_query``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolCodeEmbedding`` using a ``Symbol``, its source code, and a NumPy
array for embedding:

.. code:: python

   import numpy as np
   from automata.core.symbol.symbol_types import SymbolCodeEmbedding
   from automata.core.symbol.parser import parse_symbol

   symbol = parse_symbol("scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__().")
   source_code = "def __init__(self, message): super().__init__(message)"
   vector = np.array([0.1, 0.2, 0.3])

   embedding = SymbolCodeEmbedding(symbol, source_code, vector)

Limitations
-----------

As ``SymbolCodeEmbedding`` mainly focuses on code embeddings, it does
not include information about other types of embeddings such as
documentation or contextual information. For handling other types of
embeddings, consider using the related class ``SymbolDocEmbedding``.
