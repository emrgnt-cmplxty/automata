SymbolSearchToolkitBuilder
==========================

The ``SymbolSearchToolkitBuilder`` is an overarching connector to the
SymbolSearch API. It offers functionality to comb through an indexed
Python codebase and execute searches therein. Thoroughly integrated, it
permits to search symbols, fetch their references, return the source
code corresponding to a certain symbol, and perform exact matches.

Overview
--------

``SymbolSearchToolkitBuilder``, fundamentally, is an intermediary agent
that binds together various tools designed to search the indexed
codebase. It enables the creation of tools for the purpose of ranking
symbols, fetching their references, and retrieving source code. It also
allows for exact pattern searches across the codebase.

The class initiates with a symbol search and a list of optional search
tools. It can build single tools or a complete suite of tools for
searching the codebase. With the ``process_query()`` method, it enables
the processing of a query by routing it directly to its sub-tool.

Related Symbols
---------------

-  ``SymbolSearchOpenAIToolkitBuilder``
-  ``ContextOracleOpenAIToolkitBuilder``
-  ``ContextOracleToolkitBuilder``
-  ``SearchTool``

Example
-------

To construct the ``SymbolSearchToolkitBuilder``, here is an example
snippet:

.. code:: python

   # assuming symbolGraph and other dependencies are based on existing contextual data
   from automata.experimental.search.symbol_search import SymbolSearch, SymbolSearchConfig
   from automata.tools.builders.symbol_search import SymbolSearchToolkitBuilder, SearchTool

   # Construct the Symbol Search 
   symbol_search = SymbolSearch(symbolGraph, SymbolSearchConfig.default())

   # Define the toolkit and the search tools required
   toolkit = SymbolSearchToolkitBuilder(symbol_search, [SearchTool.EXACT_SEARCH])

   # Build the tools required
   tools = toolkit.build()

In this example, the toolkit uses the SymbolSearch class to perform an
exact search for the given pattern in the Python codebase.

Limitations
-----------

One significant caveat with ``SymbolSearchToolkitBuilder`` is that the
processors currently available are basic implementations. While
functioning, they can be refined further to concretise their
performance.

The class’s design relies heavily on the enum SearchTool; if an invalid
or unrecognized tool is provided, it raises an ``UnknownToolError``.

Follow-Up Questions
-------------------

-  What mechanisms exist to extend the capabilities of StatusCodeBuilder
   beyond ‘simple implementations’?
-  How could the functionality be extended to include other programming
   languages beyond Python?
-  What would be the process of adding new search tools or extending the
   capabilities of existing ones in practice?
