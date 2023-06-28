SymbolSearchToolBuilder
=======================

``SymbolSearchToolBuilder`` is a class that helps building tools for
searching and processing symbols in a codebase using ``SymbolSearch``.
It provides functionalities such as building tools, processing queries
using built tools, and handling various types of search results. This
class is an essential part of Automata’s core agent, responsible for
processing search queries regarding symbols in a codebase.

Overview
--------

``SymbolSearchToolBuilder`` offers a simple and convenient way to build
and process various tools related to symbol search using the provided
``SymbolSearch`` object. The main features of this class revolve around
(1) creating built tools using a list of search tools from
``SearchTool``, (2) processing queries using the built tools, and (3)
handling the results of these queries.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_search_tool.test_build``
-  ``automata.core.agent.tool.builder.symbol_search.SymbolSearchOpenAIToolBuilder``
-  ``automata.core.base.agent.AgentToolBuilder``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

The following example demonstrates how to use
``SymbolSearchToolBuilder`` to search for symbols in a codebase using
various search tools.

.. code:: python

   from automata.core.agent.tool.builder.symbol_search import (
       SymbolSearchToolBuilder,
       SearchTool,
   )
   from automata.core.symbol.search.symbol_search import SymbolSearch

   # Assuming an instance of SymbolSearch
   symbol_search = SymbolSearch( ... )

   # Create an instance of SymbolSearchToolBuilder with the SymbolSearch object
   tool_builder = SymbolSearchToolBuilder(symbol_search=symbol_search)

   # Build the tools for symbol searching
   tools = tool_builder.build()

   # Process a query using a specific built tool
   query = "search_query"
   tool_type = SearchTool.SYMBOL_RANK_SEARCH
   result = tool_builder.process_query(tool_type, query)

Limitations
-----------

The primary limitation of ``SymbolSearchToolBuilder`` is that it relies
on the supported search tools defined by ``SearchTool``. Any additional
search tools will need to be added to the ``SearchTool`` enumeration.
Furthermore, the currently used processors for processing results are
minimal in the present implementation and might not cover all related
function cases.

Follow-up Questions:
--------------------

-  Can we improve the handling of processors to make sure the
   implementation works well with different types of queries and tools?
-  Is it possible to dynamically add more search tools to the
   ``SearchTool`` enumeration without modifying its code?
