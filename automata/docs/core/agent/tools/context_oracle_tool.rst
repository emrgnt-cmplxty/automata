ContextOracleTool
=================

``ContextOracleTool`` is a powerful tool responsible for managing
context within Automata agents. It combines the functionalities of
``SymbolSearch`` and ``SymbolSimilarity`` to create comprehensive
contexts for a given query. This allows the agent to generate more
accurate responses based on the input query.

Overview
--------

The ``ContextOracleTool`` class initializes with a ``SymbolSearch``
object and a ``SymbolSimilarity`` object. It provides a ``build`` method
that returns a list of built tools. These built tools use the input
context to generate comprehensive contexts that include the most
relevant documentation and symbols found with ``SymbolSearch`` and
``SymbolSimilarity``.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

Below is an example of how to use the ``ContextOracleTool`` to create a
context based on a given query.

.. code:: python

   from automata.core.agent.tools.context_oracle import ContextOracleTool
   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.symbol.search.symbol_search import SymbolSearch

   symbol_search_instance = SymbolSearch(...)
   symbol_sim_instance = SymbolSimilarity(...)

   context_oracle_tool = ContextOracleTool(
       symbol_search=symbol_search_instance,
       symbol_doc_similarity=symbol_sim_instance
   )

   built_tools = context_oracle_tool.build()
   context_tool = built_tools[0]

   query = "Tell me about SymbolRank"
   context = context_tool.func(query)
   print(context)

Limitations
-----------

-  The quality of the generated context depends on the accuracy and
   completeness of the ``SymbolSearch`` and ``SymbolSimilarity``
   objects.
-  ``ContextOracleTool`` assumes that the input query is well-formed and
   relevant for the available symbols and documentation.

Follow-up Questions:
--------------------

-  How can we improve the quality of the generated context?
-  What pre-processing steps should be carried out on the input query to
   ensure better context generation?
