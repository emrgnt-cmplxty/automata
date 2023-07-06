SymbolCodeEmbeddingBuilder
==========================

``SymbolCodeEmbeddingBuilder`` is a builder class that constructs
``Symbol`` source code embeddings. An embedding is essentially a
mathematical representation of the symbol’s source code and is used to
measure the similarity between different symbols. The
``SymbolCodeEmbeddingBuilder`` specifically creates the
``SymbolCodeEmbedding`` from the source code and the ``Symbol``, both of
which are provided as input arguments.

``SymbolCodeEmbeddingBuilder`` plays a critical role in understanding
and processing python codes in a way that allows more sophisticated
operations, like similarity measurement and recommending pieces of codes
based on existing ones. This is achieved by transforming the code from
its primitive form to numerical representations (vectors) that can be
differentiated and compared.

Overview
--------

The ``SymbolCodeEmbeddingBuilder`` uses an ``EmbeddingVectorProvider``
to build an embedding vector from the source code. The embedding vector
captures the syntactical and perhaps some semantic essence of the code,
and in effect, creates a numerical representation for it. The
``SymbolCodeEmbeddingBuilder`` then leverages the source code, the
symbol, and the embedding vector to build a ``SymbolCodeEmbedding``.

Related Symbols
---------------

-  ``automata.embedding.base.EmbeddingBuilder``: An abstract class
   to build embeddings, from which ``SymbolCodeEmbeddingBuilder``
   inherits.
-  ``automata.embedding.base.EmbeddingVectorProvider``: An abstract
   class that provides a standard API for creating embedding vectors.
-  ``automata.symbol_embedding.base.SymbolCodeEmbedding``: A class
   for symbol code embeddings.
-  ``automata.symbol.base.Symbol``: A class which contains the
   associated logic for a Symbol.

Example
-------

This is an example demonstrating how to create an instance of
``SymbolCodeEmbedding`` using ``SymbolCodeEmbeddingBuilder``.

.. code:: python

   # Required imports
   from automata.symbol_embedding.builders import SymbolCodeEmbeddingBuilder
   from automata.symbol.base import Symbol
   from automata.embedding.base import EmbeddingVectorProvider

   # Instantiate embedding vector provider
   embedding_provider = EmbeddingVectorProvider()  # Replace with specific instance of embedding vector provider.

   # Instantiate SymbolCodeEmbeddingBuilder
   embedding_builder = SymbolCodeEmbeddingBuilder(embedding_provider)

   # Define the source code and symbol
   source_code = "def hello_world():\n    print('Hello, world!')"
   symbol = Symbol.from_string("scip-python python HelloWorld 1a2b3c HelloWorld#")

   # Build the SymbolCodeEmbedding
   code_embedding = embedding_builder.build(source_code, symbol)

Limitations
-----------

One limitation with the ``SymbolCodeEmbeddingBuilder`` is that the
quality of the ``SymbolCodeEmbedding`` that it builds is highly
dependent on the ``EmbeddingVectorProvider`` used. Different providers
may create different quality embeddings.

Another limitation is that word, line, symbol, variable or class usages
that span across different files or projects may not be embedded or
tracked correctly.

Follow-up Questions:
--------------------

-  What makes a good ``EmbeddingVectorProvider``?
-  What are the trade-offs of relying on ``SymbolCodeEmbedding`` vs
   simpler forms of text representations such as Bag of Words or TF-IDF?
-  How does the builder handle different scopes in python source code
   (i.e. local, global, nonlocal, class scopes)?

Note:
-----

This example assumes there’s an implementation of
EmbeddingVectorProvider available. In actuality, you might need to
implement a specific Embedding Provider or use a third-party library.
