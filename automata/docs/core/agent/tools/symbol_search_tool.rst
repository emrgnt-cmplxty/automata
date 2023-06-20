SymbolSearchTool
================

``SymbolSearchTool`` is a class that encapsulates the search
functionalities for symbols in a codebase. It provides methods to build
and execute queries using various search tools provided by the
``SearchTool`` enumeration, and it relies on the ``SymbolSearch`` class
for performing the searches.

Overview
--------

``SymbolSearchTool`` allows users to search for symbols, their
references, source code, and perform exact pattern matching in the
codebase. The class takes a ``SymbolSearch`` object as input, along with
an optional list of ``SearchTool`` instances to build. It exposes
methods to build tools, process queries, and get results for different
types of searches.

Related Symbols
---------------

-  ``automata.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.symbol.symbol_types.Symbol``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSearchTool`` and perform a symbol rank search with a given query
string.

.. code:: python

   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.symbol.graph import SymbolGraph
   from automata.core.symbol.similarity import SymbolSimilarity
   from automata.core.symbol.descriptors import SymbolDescriptor
   from automata.core.agent.tools.symbol_search import SymbolSearchTool, SearchTool

   symbol_graph = SymbolGraph()
   similarity = SymbolSimilarity()
   search_tools = [SearchTool.SYMBOL_RANK_SEARCH]

   symbol_search = SymbolSearch(
       symbol_graph=symbol_graph,
       symbol_similarity=similarity,
       symbol_rank_config=None,
       code_subgraph=None,
   )

   search_tool = SymbolSearchTool(
       symbol_search=symbol_search,
       search_tools=search_tools
   )

   query = "Find the user-defined symbols in the codebase"
   result = search_tool.process_query(tool_type=SearchTool.SYMBOL_RANK_SEARCH, query=query)

Limitations
-----------

``SymbolSearchTool`` relies on the functionalities provided by
``SymbolSearch`` and the search tools available in ``SearchTool``.
Therefore, it inherits the limitations of those underlying classes. For
example, it assumes that the ``SymbolGraph`` and ``SymbolSimilarity``
instances are properly initialized and accurate.

Follow-up Questions:
--------------------

-  Are there any specific limitations or caveats while using
   ``SymbolSearchTool``?
