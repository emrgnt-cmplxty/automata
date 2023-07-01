SearchTool
==========

``SearchTool`` is an Enum that represents the available search tools
that can be used by ``SymbolSearchToolkit``. It is used as an input
while creating an instance of ``SymbolSearchToolkit`` to specify the
list of search tools that the builder should build.

Overview
--------

``SearchTool`` provides a convenient way to specify the search tools to
be created by the ``SymbolSearchToolkit``. It contains predefined
search tools like ``EXACT_SEARCH``, ``PARAMETER_SEARCH``, and others.
This Enum can be passed during the instantiation of
``SymbolSearchToolkit`` to include specific search tools in the list
of built tools.

Related Symbols
---------------

-  ``automata.core.agent.tool.builder.symbol_search.SearchToolkit``
-  ``automata.core.agent.tool.builder.symbol_search.SymbolSearchToolkit``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata.core.base.tool.Tool``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolSearchToolkit`` using the ``SearchTool`` Enum as input.

.. code:: python

   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.agent.tool.builder.symbol_search import SearchTool, SymbolSearchToolkit

   symbol_search = SymbolSearch()
   search_tools = [SearchTool.EXACT_SEARCH]
   symbol_search_tool_builder = SymbolSearchToolkit(symbol_search=symbol_search, search_tools=search_tools)

Limitations
-----------

The primary limitation of ``SearchTool`` is that it only supports a
predefined set of search tools. This limits the flexibility to include
custom search tools in the list of built tools. As ``SearchTool`` is an
Enum, adding new tools would require modifying the Enum itself, which
may not be ideal in some cases.

Follow-up Questions:
--------------------

-  How can custom search tools be added and used with
   ``SymbolSearchToolkit``?
-  Are there any specific dependencies within the search tools that
   should be considered when using them in combination?
