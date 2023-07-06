SearchTool
==========

``SearchTool`` is a class contained within the
``automata.tools.builders.symbol_search`` module. It is one of the
available tools for search operations, as its name implies. It is mainly
used for building ``SymbolSearchToolkitBuilder`` objects. This class
enables interaction with ``SymbolSearch`` API, which is capable of
searching through an indexed Python codebase.

Import Statements
-----------------

To make use of the ``SearchTool`` class, include the following import
statements:

.. code:: python

   from enum import Enum
   from automata.tools.builders.symbol_search import SearchTool

Overview
--------

``SearchTool`` does not contain any methods. It is an enumeration used
to represent various available search tools during the instantiation of
a ``SymbolSearchToolkitBuilder`` object. Following are the enumerated
values -

Related Symbols
---------------

-  ``automata.tools.builders.symbol_search.SymbolSearchToolkitBuilder``
-  ``automata.tools.base.Tool``
-  ``automata.tests.unit.test_symbol_search_tool.symbol_search_tool_builder``
-  ``automata.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_tool.TestTool``

Example
-------

Below is an example to demonstrate how ``SearchTool`` enum is used while
creating the ``SymbolSearchToolkitBuilder`` object –

.. code:: python

   from automata.tools.builders.symbol_search import SearchTool, SymbolSearchToolkitBuilder
   from automata.experimental.search.symbol_search import SymbolSearch

   symbol_search = SymbolSearch(index="my_python_index")
   builder = SymbolSearchToolkitBuilder(symbol_search=symbol_search, search_tools=[SearchTool.EXACT, SearchTool.RANK])

In the above example, ``EXACT`` and ``RANK`` are two available search
tools part of the ``SearchTool`` enumeration.

Limitations
-----------

``SearchTool`` is an enum class providing the available search tools.
Thus, it does not possess any functionality itself, but rather specifies
options for other classes’ methods or constructors that require a search
tool.

Follow-up Questions
-------------------

-  Are there any plans to extend the existing enum with additional
   search tools?
-  How are these search tools interconnected with the rest of the
   codebase? For instance, how do they impact the search results?

Note: The context included references to ‘Mock’ objects in test files.
These aren’t actual underlying objects but are simplified objects used
for testing purposes.
