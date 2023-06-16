OpenAIEmbedding
===============

``OpenAIEmbedding`` is a class that provides embeddings for symbols
using OpenAI API. It allows you to build and return embeddings for a
given source code by making API calls to OpenAI service. Inherits from
the ``EmbeddingProvider`` abstract class.

Overview
--------

``OpenAIEmbedding`` takes an optional engine parameter to define the
text embedding model to be used from OpenAI API. By default, it uses the
“text-embedding-ada-002” engine. The main method of this class is
``build_embedding``, which receives a symbol source code as input and
returns the corresponding numpy array representing the embedding.

Import Statements
-----------------

.. code:: python

   import numpy as np
   import openai
   from automata_docs.core.embedding.embedding_types import EmbeddingProvider
   from config import OPENAI_API_KEY
   from openai.embeddings_utils import get_embedding

Related Symbols
---------------

-  ``automata_docs.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.embedding.embedding_types.EmbeddingProvider``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``config.OPENAI_API_KEY``

Example
-------

Here’s an example of how to initialize and use ``OpenAIEmbedding`` to
build embeddings for a symbol source.

.. code:: python

   from automata_docs.core.embedding.embedding_types import OpenAIEmbedding

   # Initialize OpenAIEmbedding instance
   embedding_provider = OpenAIEmbedding()

   # Create an example source code
   symbol_source = "def greet(name):\n    return f\"Hello {name}!\""

   # Get the embedding for the symbol
   embedding_array = embedding_provider.build_embedding(symbol_source)

   print(embedding_array.shape)

Limitations
-----------

The primary limitation of ``OpenAIEmbedding`` is that it relies on
external API calls to the OpenAI service, requiring an internet
connection and a valid API key to work. As a result, the speed and
availability of building embeddings depend on the OpenAI service’s
performance and any restrictions imposed by OpenAI, such as rate limits.

Follow-up Questions:
--------------------

-  How can the user choose different OpenAI text embedding models?
-  Are there any specific feature differences across various OpenAI text
   embedding models?
