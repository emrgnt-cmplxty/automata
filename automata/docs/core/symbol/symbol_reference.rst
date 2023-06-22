SymbolReference
===============

``SymbolReference`` is a class that represents a reference to a symbol
in a file. It stores information about the symbol, its location in the
file (line and column number), and provides methods to compare and hash
instances of the class. ``SymbolReference`` is commonly used in symbol
search and retrieval, and is closely related to the ``Symbol`` class.

Overview
--------

A ``SymbolReference`` is created using a ``Symbol`` object and the
location (line and column number) of the reference in a file. It is used
in various parts of the system to identify where a particular symbol is
being used or referenced. It provides a robust way to track symbol
references and can be used in combination with other tools and methods
to perform code analysis, search, and navigation.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_symbol_search.test_symbol_references``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_references``
-  ``automata.core.symbol.graph._SymbolGraphNavigator._get_symbol_references_in_scope``

Example
-------

Given an instance of a ``Symbol``, you can create a ``SymbolReference``
by providing the line number and column number of the symbol reference
in the file.

.. code:: python

   from automata.core.symbol.symbol_types import Symbol, SymbolReference
   from automata.core.symbol.parser import parse_symbol

   # Parse a symbol from its string representation
   symbol_str = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#"
   symbol = parse_symbol(symbol_str)

   # Create a SymbolReference with the symbol and its location in the file
   line_number = 42
   column_number = 12
   symbol_reference = SymbolReference(symbol, line_number, column_number)

Limitations
-----------

``SymbolReference`` could cause hash collisions if the same symbol is
referenced in different files at the same location. However, such cases
are expected to be rare, and the impact of these occasional collisions
should not be significant.

Follow-up Questions:
--------------------

-  Are there better ways to handle potential hash collisions?
