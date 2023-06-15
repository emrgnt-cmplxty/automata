EmbeddingsProvider
==================

``EmbeddingsProvider`` is a class to provide embeddings for symbols in
an Automata Docs project. It offers a method to build a numpy array
representing the embedding for a given source code of the symbol.

Overview
--------

The ``EmbeddingsProvider`` class utilizes the OpenAI embeddings_utils to
obtain embeddings for the given source code of symbols. It is designed
to work alongside related classes like ``SymbolCodeEmbeddingHandler``
and ``SymbolEmbedding``, allowing easy integration with the larger
system to manage and process these embeddings.

Related Symbols
---------------

-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.Symbol``

Example
-------

The following example demonstrates how to use the ``EmbeddingsProvider``
class to obtain the embedding for a given source code.

.. code:: python

   import numpy as np
   from automata_docs.core.embedding.embedding_types import EmbeddingsProvider

   source_code = "def example_function():\n    pass"
   embeddings_provider = EmbeddingsProvider()
   embedding = embeddings_provider.build_embedding(source_code)

   assert isinstance(embedding, np.ndarray)

Limitations
-----------

``EmbeddingsProvider`` relies on OpenAI’s ``embeddings_utils`` to obtain
embeddings, which requires an internet connection and API key. As a
result, performance may be affected by network latency, and users need
to have a valid OpenAI API key.

Follow-up Questions:
--------------------

-  Can the ``EmbeddingsProvider`` class use other methods for obtaining
   embeddings besides OpenAI’s ``embeddings_utils``?
