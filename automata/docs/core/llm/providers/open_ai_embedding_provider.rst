OpenAIEmbeddingProvider
=======================

``OpenAIEmbeddingProvider`` is a class in the Automata codebase that is
used to generate embeddings from the OpenAI API. The class works by
passing a given source text to the OpenAI API, which then returns an
embedding in the form of a numpy array.

Overview
--------

``OpenAIEmbeddingProvider`` implements ``EmbeddingVectorProvider``, and
uses the OpenAI API to generate embeddings for given input text. This
class relies heavily on OpenAI’s API and therefore, a key feature of
this embedding provider is its flexibility as the capability of the
provider will extend with any future enhancements made to the core API.

In this class, the engine used for generating embeddings is specified at
the time of object initialization, and the default engine used is
“text-embedding-ada-002”.

Related Symbols
---------------

-  ``automata.core.embedding.base.EmbeddingVectorProvider``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.foundation.LLMCompletionResult``
-  ``automata.core.llm.foundation.LLMConversation``
-  ``automata.core.singletons.dependency_factory.DependencyFactory``
-  ``automata.config.base.LLMProvider``
-  ``automata.core.tools.base.Tool``

Example
-------

Below is an example demonstrating how to use the
``OpenAIEmbeddingProvider``:

.. code:: python

   from automata.core.llm.providers.openai import OpenAIEmbeddingProvider
   import numpy as np

   # Create an instance of OpenAIEmbeddingProvider
   embedding_provider = OpenAIEmbeddingProvider(engine="text-embedding-ada-002")

   # Generate the embedding for a text
   source_text = "This is an example text."
   embedding = embedding_provider.build_embedding_vector(source_text)

   # Make sure the embedding is a numpy array
   assert isinstance(embedding, np.ndarray)

Limitations
-----------

One of the main limitations of the ``OpenAIEmbeddingProvider`` is that
its performance and capabilities are directly linked to the OpenAI API.
This means that any limitations in the API, such as maximum input text
size or rate limits, will also apply to the ``OpenAIEmbeddingProvider``.

For testing purposes, ``OpenAIEmbeddingProvider`` makes use of mocking
to simulate the behavior of actual objects. The mock objects are
instances of the ``Mock`` or ``MagicMock`` class in the
``unittest.mock`` module, which is a built-in module for constructing
mock objects in Python.

Follow-up Questions:
--------------------

-  How does ``OpenAIEmbeddingProvider`` handle potential rate limit
   restrictions from the OpenAI API?
-  What are the specific error handling strategies in place for API
   failures?
-  How can customization be introduced to enhance the use of different
   ‘engine’ types for different requirements?
