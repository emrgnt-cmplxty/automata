SymbolEmbedding
===============

``SymbolEmbedding`` is an abstract base class for different types of
embeddings associated with symbols in the Automata codebase. It handles
the initialization of a symbol embedding with a given symbol and its
corresponding vector representation. This class serves as the foundation
for creating more specialized types of symbol embeddings, like
``SymbolCodeEmbedding`` and ``SymbolDocEmbedding``.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbedding``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingsProvider``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolEmbeddingHandler``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbeddingHandler``

Example
-------

The following example demonstrates how to create a custom symbol
embedding class that inherits from ``SymbolEmbedding``. We’ll create a
hypothetical ``CustomSymbolEmbedding`` class for this purpose.

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol, SymbolEmbedding
   import numpy as np

   class CustomSymbolEmbedding(SymbolEmbedding):
       def __init__(self, symbol: Symbol, vector: np.array):
           super().__init__(symbol, vector)

Now, we can create an instance of our custom symbol embedding.

.. code:: python

   from automata_docs.core.symbol.search.symbol_parser import parse_symbol

   symbol_ex = parse_symbol("scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#")
   vector_ex = np.array([0.1, 0.2, 0.3])

   custom_embedding = CustomSymbolEmbedding(symbol_ex, vector_ex)

Limitations
-----------

Since ``SymbolEmbedding`` is an abstract base class, it should not be
used directly to create instances. Instead, it must be subclassed and
extended with any additional properties and methods required for the
specific embedding type.

Follow-up Questions:
--------------------

-  Are there more specific examples of ``SymbolEmbedding`` subclasses
   that can be showcased?
-  What are the use cases for the different types of symbol embeddings?
