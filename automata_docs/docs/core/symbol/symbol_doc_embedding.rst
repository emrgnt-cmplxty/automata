SymbolDocEmbedding
==================

``SymbolDocEmbedding`` is a class that represents the embedding of
symbol documentation. It is a subclass of ``SymbolEmbedding``. The class
provides fields to store the symbol, the vector representing the
embedding, the source code of the symbol, the documentation string, an
optional summary, and optional context. The class can be used when
working with embeddings for symbol documents in projects like
``automata_docs``.

Overview
--------

The ``SymbolDocEmbedding`` class is mainly used to store the data
associated with symbol document embeddings. It inherits from the
abstract base class ``SymbolEmbedding``. The main fields include
``symbol``, ``vector``, ``source_code``, ``document``, ``summary``, and
``context``. It can be used to store and manipulate the embeddings of
symbol documentation in various modules and components of a project like
``automata_docs``.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.symbol.symbol_types.SymbolCodeEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolDocEmbeddingHandler.build_symbol_doc_embedding``

Example
-------

The following example demonstrates how the ``SymbolDocEmbedding`` class
can be used to store the symbol documentation embedding.

.. code:: python

   import numpy as np
   from automata_docs.core.symbol.symbol_types import Symbol
   from automata_docs.core.symbol.parser import parse_symbol
   from automata_docs.core.embedding.embedding_types import SymbolDocEmbedding

   symbol_str = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.base.tool`/ToolNotFoundError#__init__()."
   symbol = parse_symbol(symbol_str)

   vector = np.random.rand(512)
   source_code = "def __init__(self): ..."
   document = "Documentation string"
   summary = "Summary of documentation"

   symbol_doc_embedding = SymbolDocEmbedding(
       symbol=symbol,
       vector=vector,
       source_code=source_code,
       document=document,
       summary=summary,
   )

Limitations
-----------

The ``SymbolDocEmbedding`` class does not provide methods to manipulate
or update the stored embeddings. It only serves as a container for
storing the data but does not provide functionality to update or
manipulate the embeddings based on specific needs or requirements. The
embeddings need to be precomputed or retrieved from another source
before storing them as a ``SymbolDocEmbedding`` instance.

Follow-up Questions:
--------------------

-  How can we handle updating or manipulating the embeddings within the
   ``SymbolDocEmbedding`` class if required?
-  Are there any other fields that can be useful to store as part of the
   ``SymbolDocEmbedding`` class?
