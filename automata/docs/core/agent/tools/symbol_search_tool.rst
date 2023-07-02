SymbolSearchTool
================

``SymbolSearchTool`` is a class that provides various search tools used
to search for symbols in a program’s codebase. The tools are built on
top of the ``SymbolSearch`` class and utilize the different search
functions available. ``SymbolSearchTool`` includes search tools such as
Symbol Rank Search, Symbol References, Retrieve Source Code by Symbol,
and Exact Search.

Overview
--------

``SymbolSearchTool`` offers a convenient way to build, initialize, and
process various searches related to symbols in the codebase. It takes a
``SymbolSearch`` object and an optional list of search tools as input
during initialization. The available search tools can be built on
demand, and a specific search tool can be utilized by processing a query
using the desired tool.

Related Symbols
---------------

-  ``automata.core.experimental.search.symbol_search.SymbolSearch``
-  ``automata.core.toolss.symbol_search.SearchTool``
-  ``automata.core.tools.tool.Tool``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSearchTool``, build search tools, and process a query using one
of the available search tools.

.. code:: python

   from automata.core.experimental.search.symbol_search import SymbolSearch
   from automata.core.toolss.symbol_search import SymbolSearchTool, SearchTool

   symbol_search = SymbolSearch()  # Note: Replace with actual SymbolSearch instance
   symbol_search_tool = SymbolSearchTool(symbol_search)

   tools = symbol_search_tool.build()
   tool_type = SearchTool.SYMBOL_RANK_SEARCH
   query = "example_query"

   result = symbol_search_tool.process_query(tool_type, query)

Limitations
-----------

The primary limitation of ``SymbolSearchTool`` is that it relies on the
search functions available in the ``SymbolSearch`` class. Any new search
functionality needs to be implemented in ``SymbolSearch`` and then added
as a search tool in ``SymbolSearchTool``. Moreover, it currently takes
only a list of search tools and builds all of them at once, which may
not be efficient in certain scenarios.

Follow-up Questions:
--------------------

-  How does the ``SymbolSearch`` class work, and how does it interact
   with ``SymbolSearchTool``?
-  Can we make the ``SymbolSearchTool`` more flexible in terms of adding
   new search tools or building only specific tools on demand?
