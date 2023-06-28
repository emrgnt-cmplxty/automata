ContextOracleTool
=================

``ContextOracleTool`` is a class responsible for managing context oracle
tools. It combines ``SymbolSearch`` with ``SymbolSimilarity`` to create
comprehensive contexts for queries. The generated contexts are useful
for natural language processing tasks like answering questions or
providing contextual details for certain symbols.

Overview
--------

The ``ContextOracleTool`` class is initialized with a ``SymbolSearch``
object and a ``SymbolSimilarity`` object. The ``build()`` method
provides a list of tools associated with the context oracle.

Key related symbols include: -
``automata.core.symbol.search.symbol_search.SymbolSearch`` -
``automata.core.embedding.symbol_similarity.SymbolSimilarity`` -
``automata.core.base.tool.Tool`` -
``automata.core.agent.tool.builder.context_oracle.ContextOracleOpenAIToolBuilder``
- ``automata.core.base.agent.AgentToolBuilder`` -
``automata.core.base.agent.AgentToolProviders`` -
``automata.core.agent.tool_tool_utils.AgentToolFactory``

Example
-------

The following example demonstrates how to create an instance of
``ContextOracleTool`` and build the associated tools.

.. code:: python

   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.agent.tool.builder.context_oracle import ContextOracleTool

   symbol_search = SymbolSearch(...)  # Set up the SymbolSearch object
   symbol_doc_similarity = SymbolSimilarity(...)  # Set up the SymbolSimilarity object

   context_oracle_tool = ContextOracleTool(symbol_search=symbol_search, symbol_doc_similarity=symbol_doc_similarity)
   tools = context_oracle_tool.build()

Limitations
-----------

The primary limitation of ``ContextOracleTool`` is that it relies on the
provided ``SymbolSearch`` and ``SymbolSimilarity`` objects, which must
be set up and configured correctly. It assumes that these objects have
been initialized with appropriate embeddings and configuration settings.

Follow-up Questions:
--------------------

-  How can we improve the example to show more realistic usage with
   specific configuration settings for SymbolSearch and
   SymbolSimilarity?
-  Can you provide more details about the underlying Mock objects for
   the example tests in the context, like MagicMock for
   SymbolDocEmbedding, etc.?
