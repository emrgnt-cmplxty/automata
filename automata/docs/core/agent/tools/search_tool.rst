SearchTool
==========

``SearchTool`` is a class that represents a search tool for retrieving
information about symbols from the source code. It is an enumeration of
available search tools and is used in conjunction with classes from the
``automata.core.symbol.search`` package.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.symbol.search.symbol_search.ExactSearchResult``
-  ``automata.core.symbol.search.symbol_search.SourceCodeResult``
-  ``automata.core.symbol.search.symbol_search.SymbolRankResult``
-  ``automata.core.symbol.search.symbol_search.SymbolReferencesResult``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata.core.symbol.symbol_types.Symbol``

Example
-------

Below is an example of how to use the ``SearchTool`` enumeration when
working with the ``SymbolSearch`` class:

.. code:: python

   from automata.core.agent.tools.symbol_search import SearchTool
   from automata.core.symbol.search.symbol_search import SymbolSearch

   search_tool = SearchTool.SYMBOL_RANK
   symbol_search = SymbolSearch(search_tool)

Limitations
-----------

``SearchTool`` is an enumeration and does not provide any functionality
within the class itself. It is only used to indicate the type of search
tool to be used when working with classes from the
``automata.core.symbol.search`` package.

Follow-up Questions:
--------------------

-  What are the different types of search tools available in the
   ``SearchTool`` enumeration?
-  How does the chosen search tool affect the behavior of classes from
   the ``automata.core.symbol.search`` package?
