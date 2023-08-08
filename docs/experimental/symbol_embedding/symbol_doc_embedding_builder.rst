SymbolDocEmbeddingBuilder
=========================

``SymbolDocEmbeddingBuilder`` is a dedicated class for generating
embeddings from the documentation of symbols.

Overview
--------

The ``SymbolDocEmbeddingBuilder`` class is designed to interact with and
generate embeddings from the documentation of symbols. The class
interacts with the documentation on two main scopes - those specifying a
class, and those specifying a non-class type symbol.

The class uses a number of helper methods, such as the
``_build_class_document`` and ``_build_class_document_summary`` methods,
to facilitate the generation of embeddings. It also interacts with an
``EmbeddingVectorProvider`` to obtain the actual embeddings for symbols,
and leverages a context handler for producing relevant context for
symbols. The class itself is an implementation of the
``EmbeddingBuilder`` abstract class.

One key aspect of this class is its ability to also build non-class type
symbols’ documentation and generate embeddings for them. The
``build_non_class`` method is specifically tailored to handle non-class
type symbols.

Apart from building individual embeddings, ``SymbolDocEmbeddingBuilder``
can also build a batch of embeddings using its ``batch_build`` method,
but this feature has not been implemented yet.

It’s also worth mentioning that the ``class_cut_size`` attribute
determines the threshold of the source code’s length, below which the
code is considered insufficient for processing and embedding generation.

The ``SymbolDocEmbeddingBuilder`` class considers the context of a
symbol, meaning it includes related symbols, dependencies, and test
scripts in the construction of the symbol context. It may also generate
a search list by splicing the search results on the symbol with the
search results biased on automata.tests.

Related Symbols
---------------

-  ``EmbeddingBuilder``
-  ``EmbeddingVectorProvider``
-  ``LLMChatCompletionProvider``
-  ``SymbolSearch``
-  ``PyContextHandler``
-  ``SymbolDocEmbedding``

Example
-------

Below is an example of how to create an instance of the
``SymbolDocEmbeddingBuilder`` and subsequently use it to build a
documentation embedding for a symbol:

.. code:: python

   from automata.experimental.symbol_embedding.symbol_doc_embedding_builder import SymbolDocEmbeddingBuilder
   from automata.llm.providers.openai_llm import OpenAIEmbeddingProvider
   from automata.llm.llm_base import LLMChatCompletionProvider
   from automata.tools.context_generation.symbol_search import SymbolSearch
   from automata.experimental.code_parsers.py.context_processing.context_handler import PyContextHandler
   from automata.tools.payl_py_code_objs import Symbol

   # Initializing the necessary providers
   embedding_provider = OpenAIEmbeddingProvider()
   completion_provider = LLMChatCompletionProvider()
   symbol_search = SymbolSearch()
   handler = PyContextHandler()

   # Create builder instance
   doc_embedding_builder = SymbolDocEmbeddingBuilder(embedding_provider, completion_provider, symbol_search, handler)

   # Assume symbol is a generated symbol
   # symbol = ...
   doc_embedding = doc_embedding_builder.build(symbol.source_code, symbol)

Limitations
-----------

One limitation of the ``SymbolDocEmbeddingBuilder`` is the
``batch_build`` method, which is not yet implemented for building
document embeddings.

Moreover, the class requires an instance of
``EmbeddingVectorProvider``,\ ``LLMChatCompletionProvider``,
``SymbolSearch``, and ``PyContextHandler``. It implies that it can only
function where these four classes are implemented and can provide the
necessary functionalities.

As with other classes that use machine learning models for generating
embeddings, the quality of the output depends heavily on the underlying
model and the input data. Badly written or incomplete documentation for
a symbol may lead to poor embeddings, and consequently, unreliable
outcomes when these embeddings are utilized.

Follow-up Questions
-------------------

-  How does the ``class_cut_size`` attribute influence the processing
   and embeddings generation of a given symbol?
-  How could we handle symbols whose source code length fails to reach
   the ``class_cut_size`` mark, beyond skipping them or considering them
   non-class type symbols?
