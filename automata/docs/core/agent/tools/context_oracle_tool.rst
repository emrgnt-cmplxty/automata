ContextOracleTool
=================

``ContextOracleTool`` is a class responsible for managing context oracle
tools. It combines ``SymbolSearch`` and ``SymbolSimilarity`` to create
contexts. Given a query, the tool calculates the similarity between each
symbol’s documentation and the query, and returns the most similar
document. Then, it leverages ``SymbolSearch`` to combine semantic search
with PageRank to find the most relevant symbols to the query, providing
a comprehensive context for the query.

Overview
--------

``ContextOracleTool`` receives a ``SymbolSearch`` object and a
``SymbolSimilarity`` object upon initialization, and then builds the
associated tools for the context oracle. The main functionality is
provided by the ``_context_generator`` private method, which is the core
of the “context-oracle” tool.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

.. code:: python

   from automata.core.agent.tools.context_oracle import ContextOracleTool
   from automata.core.symbol_embedding.similarity import SymbolSimilarity
   from automata.core.symbol.search.symbol_search import SymbolSearch

   symbol_search = SymbolSearch()
   symbol_doc_similarity = SymbolSimilarity()

   context_oracle = ContextOracleTool(
       symbol_search=symbol_search,
       symbol_doc_similarity=symbol_doc_similarity
   )

   tools = context_oracle.build()

Limitations
-----------

``ContextOracleTool`` relies on the capabilities and limitations of both
``SymbolSearch`` and ``SymbolSimilarity``. Thus, its results are limited
by the quality of similarity measurements and search results provided by
these two components.

Follow-up Questions:
--------------------

-  Are there any specific query formatting guidelines or restrictions
   for the input query?
-  How can we improve the relevancy and accuracy of the generated
   context?
