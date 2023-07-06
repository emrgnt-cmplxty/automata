SymbolDocEmbeddingBuilder
=========================

``SymbolDocEmbeddingBuilder`` is a class that creates documentation
embeddings for a given ``Symbol``. This class exists in the
``automata.symbol_embedding.builders`` package. It is crucial in
understanding and building the context surrounding primary symbols in
the code.

Overview
--------

``SymbolDocEmbeddingBuilder`` is used to build an embedding for a
symbol’s documentation. It generates a search list for related context,
accumulates documentation from retrieval sources, and then creates an
embedding from the final document. This class works in combination with
other classes such as ``EmbeddingVectorProvider``,
``LLMChatCompletionProvider``, ``SymbolSearch``, and
``PyContextRetriever``.

Related Symbols
---------------

-  ``automata.embedding.base.EmbeddingBuilder``
-  ``automata.embedding.base.EmbeddingVectorProvider``
-  ``automata.retrievers.py.context.PyContextRetriever``
-  ``automata.llm.foundation.LLMChatCompletionProvider``
-  ``automata.experimental.search.symbol_search.SymbolSearch``
-  ``automata.symbol_embedding.base.SymbolDocEmbedding``

Examples
--------

The following is a basic example demonstrating how the
``SymbolDocEmbeddingBuilder`` would be used to create documentation
embeddings for a symbol.

.. code:: python

   from automata.symbol_embedding.builders import SymbolDocEmbeddingBuilder
   from automata.embedding.base.EmbeddingVectorProvider import MyEmbeddingVectorProvider
   from automata.llm.foundation import MyLLMChatCompletionProvider
   from automata.experimental.search.symbol_search import MySymbolSearch
   from automata.retrievers.py.context import PyContextRetriever

   embedding_provider = MyEmbeddingVectorProvider(...)
   completion_provider = MyLLMChatCompletionProvider(...)
   symbol_search = MySymbolSearch(...)
   retriever = PyContextRetriever(...)

   builder = SymbolDocEmbeddingBuilder(
       embedding_provider=embedding_provider,
       completion_provider=completion_provider,
       symbol_search=symbol_search,
       retriever=retriever
   )

   source_code = """
   def my_func():
       \"\"\"This is a sample function.\"\"\"
       return 5
   """

   symbol = Symbol.from_string(...)
   result = builder.build(source_code, symbol)

Where all the ``My...`` objects are various classes of those types.

Please note that the actual class names and instantiation will depend on
the specific embedding provider, completion provider, symbol_search, and
retriever that you use.

Limitations
-----------

While extremely useful for creating documentation embeddings,
``SymbolDocEmbeddingBuilder`` should be used with due consideration of
its potential limitations. The quality and accuracy of the embeddings
depend heavily on the underlying ``EmbeddingVectorProvider`` and
``LLMChatCompletionProvider`` used.

Follow-up Questions:
--------------------

-  What is the expected format and content of the ``Symbol`` object?
-  How does the ``SymbolSearch`` class affect the output of
   ``SymbolDocEmbeddingBuilder``?
-  How can we optimize the source code to XML transformation in
   ``PyContextRetriever`` for better results?
