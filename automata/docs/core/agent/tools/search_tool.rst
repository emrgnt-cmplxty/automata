SearchTool
==========

``SearchTool`` is a class that provides an interface for a set of search
tools, each with a different functionality. The primary search tools
include exact-search, symbol-rank-search, source-code-search, and
symbol-references-search. The ``SearchTool`` class is part of the
``automata.core.agent.tools.symbol_search`` module and can be used to
build specific tools by specifying the desired search tool type.

Overview
--------

``SearchTool`` is an enumeration class that defines the available search
tools. It can be used in conjunction with the ``SymbolSearchTool``,
which provides methods to build and execute search tools. For example, a
tool for exact-search can be built by specifying the
``SearchTool.EXACT_SEARCH`` as its type.

Related Symbols
---------------

-  ``automata.core.agent.tools.symbol_search.SymbolSearchTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.symbol.search.symbol_search.*``

Example
-------

The following example demonstrates how to use ``SearchTool`` to create
and execute an exact-search tool:

.. code:: python

   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.agent.tools.symbol_search import (
       SymbolSearchTool,
       SearchTool,
   )

   # Create a SymbolSearch object
   symbol_search = SymbolSearch()
    
   # Create a SymbolSearchTool object
   symbol_search_tool = SymbolSearchTool(symbol_search)

   # Build all available search tools
   tools = symbol_search_tool.build()

   # Execute a specific search tool (exact-search in this example)
   tool_type = SearchTool.EXACT_SEARCH
   query = "module.path, pattern"

   for tool in tools:
       if tool.name == tool_type.value:
           result = tool.func(query)
           print(result)

Limitations
-----------

One limitation of the ``SearchTool`` is that it only provides a
predefined set of search tools, which may not cover all possible search
needs. The ``SearchTool`` enumeration cannot be extended inline, as
opposed to using other methods for building or combining search tools.

Follow-up Questions:
--------------------

-  Are additional search tools needed to address specific search needs?
-  How can we customize the search process to make it more robust and
   flexible for different use cases?
