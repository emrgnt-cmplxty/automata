ContextOracleToolkitBuilder
===========================

Overview
--------

The ``ContextOracleToolkitBuilder`` class is part of the Automata SDK
and provides tools which translate natural language processing (NLP)
queries into relevant context. It is a specialized toolkit builder
responsible for providing context to a given query by computing the
semantic similarity between the query, documentation, and code of all
available symbols.

Related Symbols
---------------

-  ``automata.agent.agent.AgentToolkitBuilder``
-  ``automata.tests.unit.test_context_oracle_tool.context_oracle_tool_builder``
-  ``automata.tests.unit.test_context_oracle_tool.test_build``
-  ``automata.tests.unit.test_context_oracle_tool.test_init``
-  ``automata.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``

Dependencies
------------

-  ``automata.embedding.base.EmbeddingSimilarityCalculator``
-  ``automata.memory_store.symbol_doc_embedding.SymbolDocEmbeddingHandler``
-  ``automata.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.tools.base.Tool``

Example
-------

.. code:: python

   from automata.tools.builders.context_oracle import ContextOracleToolkitBuilder
   from automata.embedding.base import EmbeddingSimilarityCalculator
   from automata.memory_store.symbol_doc_embedding import SymbolDocEmbeddingHandler
   from automata.memory_store.symbol_code_embedding import SymbolCodeEmbeddingHandler

   symbol_doc_embedding_handler = SymbolDocEmbeddingHandler()
   symbol_code_embedding_handler = SymbolCodeEmbeddingHandler()
   embedding_similarity_calculator = EmbeddingSimilarityCalculator()
      
   context_oracle_tool_builder = ContextOracleToolkitBuilder(
     symbol_doc_embedding_handler=symbol_doc_embedding_handler,
     symbol_code_embedding_handler=symbol_code_embedding_handler,
     embedding_similarity_calculator=embedding_similarity_calculator,
   )

   tools = context_oracle_tool_builder.build()
   for tool in tools:
     print(tool.name)

Limitations
-----------

The ``ContextOracleToolkitBuilder`` is reliant on various interfaces and
classes including ``EmbeddingSimilarityCalculator``,
``SymbolDocEmbeddingHandler``, and ``SymbolCodeEmbeddingHandler``.
Limitations of these classes will inherently limit the functionality or
performance of ``ContextOracleToolkitBuilder``.

Follow-up Questions
-------------------

1. Is there a way to specify custom similarity calculators or embedding
   handlers?
2. How does the ``ContextOracleToolkitBuilder`` handle situations when a
   similarity score is not available?
3. How is the context for a query optimized? Can we specify the number
   of most similar symbols for which we want to include the context?
