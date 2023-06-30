EmbeddingProvider
=================

``EmbeddingProvider`` is an abstract base class that provides embeddings
for symbols. It is used in different embedding types such as
``OpenAIEmbedding`` and as an input in classes like
``SymbolCodeEmbeddingHandler`` and ``SymbolDocEmbeddingHandler`` for
managing symbol embeddings.

Overview
--------

The primary purpose of the ``EmbeddingProvider`` is to provide a
consistent interface for generating embeddings for symbols. Any class
that implements the ``EmbeddingProvider`` interface must provide a
``build_embedding`` method that takes a ``symbol_source`` as input and
returns a numpy ndarray.

Related Symbols
---------------

-  ``automata.core.memory_store.embedding_types.OpenAIEmbedding``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``

Example
-------

The following is an example demonstrating how to create an instance of a
class that inherits from ``EmbeddingProvider`` and implement the
``build_embedding`` method.

.. code:: python

   import numpy as np
   from automata.core.memory_store.embedding_types import EmbeddingProvider

   class MyEmbeddingProvider(EmbeddingProvider):

       def build_embedding(self, symbol_source: str) -> np.ndarray:
           # Implement your own logic to generate the embedding for a given symbol source
           embedding = np.random.randn(1024)
           return embedding

   embedding_provider = MyEmbeddingProvider()
   symbol_source = "some_symbol_source"
   embedding = embedding_provider.build_embedding(symbol_source)

Limitations
-----------

Since ``EmbeddingProvider`` is an abstract base class, it cannot be used
directly to generate embeddings. Instead, it should be inherited and
implemented by a subclass providing a specific kind of embedding, such
as an implementation using OpenAI’s API.

Follow-up Questions:
--------------------

-  Are there any specific requirements for the input ``symbol_source``
   when using the ``build_embedding`` method?
-  What are some example use cases for creating custom
   ``EmbeddingProvider`` implementations?
