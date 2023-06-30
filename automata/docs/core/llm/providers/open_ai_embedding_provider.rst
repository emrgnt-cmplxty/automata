OpenAIEmbeddingProvider
=======================

``OpenAIEmbeddingProvider`` is a class that provides embeddings for
symbols using OpenAI’s API. It extends the ``EmbeddingProvider``
abstract base class and implements the method ``build_embedding`` to get
the embedding for a given symbol.

Overview
--------

``OpenAIEmbeddingProvider`` gets embeddings for symbols using the OpenAI
API. It requires the OpenAI API key to be set before usage. The class
has a single ``build_embedding`` method that accepts a source code
string representing the symbol and returns a NumPy array containing the
embedding.

Related Symbols
---------------

-  ``automata.core.llm.core.EmbeddingProvider``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding``
-  ``automata.tests.unit.test_symbol_embedding.test_get_embedding_exception``
-  ``automata.tests.unit.test_symbol_embedding.test_add_new_embedding``
-  ``automata.tests.unit.test_symbol_embedding.test_update_embedding``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.core.llm.core.SymbolEmbeddingHandler.__init__``

Example
-------

The following example demonstrates how to use the
``OpenAIEmbeddingProvider`` to fetch an embedding for a sample source
code symbol.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
   import numpy as np

   symbol_source = "def add(a, b): return a + b"
   embedding_provider = OpenAIEmbeddingProvider()
   embedding = embedding_provider.build_embedding(symbol_source)

   assert isinstance(embedding, np.ndarray)

Limitations
-----------

``OpenAIEmbeddingProvider`` has a few limitations. First, it relies on
the OpenAI API to retrieve embeddings, which requires internet
connectivity and an API key. Second, the implementation assumes the
usage of a specific transformer model from the OpenAI API, and
customizing this model may require modifying the provider
implementation. Lastly, it may be slower than other local embedding
providers as it requires fetching embeddings from the OpenAI API.

Follow-up Questions:
--------------------

-  Is there any way to cache the embeddings fetched from the OpenAI API
   to improve efficiency and reduce the number of API calls?
-  How can we customize the transformer model used by
   OpenAIEmbeddingProvider to support different pre-trained models?
