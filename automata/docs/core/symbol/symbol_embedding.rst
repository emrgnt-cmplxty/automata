SymbolEmbedding
===============

``SymbolEmbedding`` is an abstract base class for different types of
embeddings representing symbols, such as ``SymbolCodeEmbedding`` and
``SymbolDocEmbedding``. It provides a basic structure for initializing
and managing symbol embeddings, considering the source of the embedding
and the vector representing the embedding in the feature space.
``SymbolEmbedding`` is used in various embedding handlers, such as
``SymbolCodeEmbeddingHandler`` and ``SymbolDocEmbeddingHandler``.

Related Symbols
---------------

-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolDocEmbedding``
-  ``automata.core.symbol.symbol_types.SymbolCodeEmbedding``
-  ``automata.core.embedding.doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.core.embedding.embedding_types.EmbeddingProvider``
-  ``automata.core.embedding.embedding_types.SymbolEmbeddingHandler``
-  ``automata.core.database.vector.JSONVectorDatabase``

Example
-------

The following example demonstrates how to create an instance of a
derived class ``SymbolCodeEmbedding``:

.. code:: python

   from automata.core.symbol.symbol_types import SymbolCodeEmbedding
   from automata.core.symbol.parser import parse_symbol
   import numpy as np

   symbol_str = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__()."
   symbol = parse_symbol(symbol_str)
   source_code = "def __init__(self, message): pass"
   vector = np.array([0.1, 0.2, 0.3])

   symbol_code_embedding = SymbolCodeEmbedding(symbol, source_code, vector)

Limitations
-----------

``SymbolEmbedding`` serves as a base class to be extended by classes
with specific embedding types, like ``SymbolCodeEmbedding`` or
``SymbolDocEmbedding``. So, the functionality provided by
``SymbolEmbedding`` is limited to its role as a base class.

Follow-up Questions:
--------------------

-  Are there more concrete classes derived from ``SymbolEmbedding``
   other than ``SymbolCodeEmbedding`` and ``SymbolDocEmbedding``?
-  How are the embedding vectors for ``SymbolEmbedding`` instances
   usually generated?
