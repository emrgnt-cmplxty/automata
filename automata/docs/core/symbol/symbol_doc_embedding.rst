SymbolDocEmbedding
==================

``SymbolDocEmbedding`` is a class that represents the embedding for
symbol documents. It extends the ``SymbolEmbedding`` class and adds
additional metadata such as the source code, summary, and context of the
symbol.

Overview
--------

``SymbolDocEmbedding`` provides a way to store and access the embeddings
for symbol documents, which are important for tasks like search and
similarity comparison. The class is used in conjunction with
``SymbolDocEmbeddingHandler`` to create, update, and retrieve embeddings
for a given symbol.

Related Symbols
---------------

-  ``Symbol``: A class representing the primary symbol URI, which can be
   a class, method, or a local variable.
-  ``SymbolDocEmbeddingHandler``: A handler class to manage
   ``SymbolDocEmbedding`` objects, providing methods to create, update,
   and retrieve embeddings.
-  ``SymbolCodeEmbedding``: A class representing the embeddings for
   symbol code.
-  ``SymbolCodeEmbeddingHandler``: A handler class to manage
   ``SymbolCodeEmbedding`` objects, providing methods to create, update,
   and retrieve embeddings.

Example
-------

The following example demonstrates how to create an instance of
``SymbolDocEmbedding``.

.. code:: python

   import numpy as np
   from automata_docs.core.symbol.symbol_types import Symbol
   from automata_docs.core.symbol.symbol_types import SymbolDocEmbedding

   symbol_str = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   symbol = Symbol.from_string(symbol_str)

   document = "This is a sample document"
   vector = np.array([0.1, 0.2, 0.3])
   source_code = "class ActionIndicator(Enum): ..."
   summary = "This class represents an enum for action indicators."
   context = "The ActionIndicator enum is used to describe the current state..."

   embedding = SymbolDocEmbedding(symbol, document, vector, source_code=source_code, summary=summary, context=context)

Limitations
-----------

``SymbolDocEmbedding`` relies on external handler classes like
``SymbolDocEmbeddingHandler`` for proper creation, updating, and
retrieval of embeddings. Moreover, it assumes the embeddings are
provided as NumPy arrays, which may limit the usage of other types of
embeddings.

Follow-up Questions:
--------------------

-  Can the ``SymbolDocEmbedding`` class be extended to support different
   types of embeddings, other than NumPy arrays?
