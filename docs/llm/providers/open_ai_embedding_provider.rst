OpenAIEmbeddingProvider
=======================

``OpenAIEmbeddingProvider`` is a class that extracts embeddings from the
OpenAI API. It is subclassed from ``EmbeddingVectorProvider``.

Overview
--------

The ``OpenAPIEmbeddingProvider`` class provides methods to create
embeddings from source text or batch of texts using OpenAI API. Its main
functionality is embedded primarily in two methods:
``build_embedding_vector()`` and ``batch_build_embedding_vector()``. The
first method generates an embedding for a single string of text, while
the latter performs the same operation for multiple strings contained
within a list.

The class needs the OpenAI API key to be set for it to work properly. By
default, it utilizes the ‘text-embedding-ada-002’ engine. However, it
can also operate with the engine designated in the constructor at object
creation.

Related Symbols
---------------

The related symbols for the ``OpenAIEmbeddingProvider`` class are
methods imported from the ``openai.embeddings_utils`` module. They are:
- ``get_embedding()`` - ``get_embeddings()``

Example
-------

Here is an example demonstrating the usage of the
``OpenAIEmbeddingProvider`` class. This includes the full process of
creating an instance, building an embedding vector, and a batch of
vectors.

.. code:: python

   from automata.llm.providers.openai_llm import OpenAIEmbeddingProvider
   import numpy as np

   # Instantiating the provider using the default engine
   provider = OpenAIEmbeddingProvider()

   # Building an embedding vector for a single source
   source_text = "OpenAI is an artificial intelligence research lab."
   embedding_vector = provider.build_embedding_vector(source_text)
   print(embedding_vector)  # Outputs the resulting numpy array

   # Building embedding vectors for a batch of sources
   sources_batch = ["OpenAI was founded in December 2015.", 
                            "The lab is associated with Elon Musk."]
   batch_embedding_vector = provider.batch_build_embedding_vector(sources_batch)
   for vector in batch_embedding_vector:
       print(vector)  # Outputs numpy arrays

Limitations
-----------

The ``OpenAIEmbeddingProvider`` class is reliant on the OpenAI API. As a
result, if the OpenAI API is down or inaccessible, it will also be
unable to function properly. Furthermore, the class requires an OpenAI
API key to operate, which might be a hurdle if you’re not an OpenAI
user. Also, the quality of embeddings depends upon the chosen engine. By
default it uses ‘text-embedding-ada-002’ engine but OpenAI provides
other engines too which might give different results as per their
training.

Follow-up Questions:
--------------------

-  What are the different engines supported by OpenAI for text
   embedding?
-  How to handle the situation if OpenAI API is down momentarily?
-  Is there a way to use a different API key for different instances of
   ``OpenAIEmbeddingProvider``?
