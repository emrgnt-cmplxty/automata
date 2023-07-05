SearchTool
==========

``SearchTool`` is an Enum that represents the available search tools
that can be used by ``SymbolSearchToolkitBuilder``. It is used as an input
while creating an instance of ``SymbolSearchToolkitBuilder`` to specify the
list of search tools that the builder should build.

Overview
--------

``SearchTool`` provides a convenient way to specify the search tools to
be created by the ``SymbolSearchToolkitBuilder``. It contains predefined
search tools like ``EXACT_SEARCH``, ``PARAMETER_SEARCH``, and others.
This Enum can be passed during the instantiation of
``SymbolSearchToolkitBuilder`` to include specific search tools in the list
of built tools.

Related Symbols
---------------

-  ``automata.core.tools.builders.symbol_search.SearchToolkit``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchToolkitBuilder``
-  ``automata.core.experimental.search.symbol_search.SymbolSearch``
-  ``automata.core.tools.tool.Tool``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolSearchToolkitBuilder`` using the ``SearchTool`` Enum as input.

.. code:: python

   from automata.core.experimental.search.symbol_search import SymbolSearch
   from automata.core.tools.builders.symbol_search import SearchTool, SymbolSearchToolkitBuilder

   symbol_search = SymbolSearch()
   search_tools = [SearchTool.EXACT_SEARCH]
   symbol_search_tool_builder = SymbolSearchToolkitBuilder(symbol_search=symbol_search, search_tools=search_tools)

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
   ``SymbolSearchToolkitBuilder``?
-  Are there any specific dependencies within the search tools that
   should be considered when using them in combination?
