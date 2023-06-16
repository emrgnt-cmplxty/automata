SymbolReference
===============

``SymbolReference`` is a class that represents a reference to a symbol
in a file. It is used for tracking and managing references to symbols
within a codebase. It provides utility methods for comparing and hashing
symbol references based on their URI, line number, and column number.
This class is used in conjunction with other classes related to symbols,
such as ``Symbol``, ``SymbolDescriptor``, and ``SymbolEmbedding``.

Overview
--------

A ``SymbolReference`` object represents a unique reference to a symbol
based on its URI, line number, and column number. It provides methods to
check for equality and uniqueness with other symbol references. It is
useful in tracking and managing references to symbols in files based on
their location and use in the codebase.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.symbol_types.SymbolDescriptor``
-  ``automata.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata.core.symbol.graph.SymbolGraph``

Example
-------

The following example demonstrates how to create an instance of
``SymbolReference`` and compare it with other symbol references.

.. code:: python

   from automata.core.symbol.symbol_types import SymbolReference
   from automata.core.symbol.parser import parse_symbol

   symbol_uri = "example_uri"
   line_number = 10
   column_number = 5
   symbol = parse_symbol(symbol_uri)

   symbol_ref1 = SymbolReference(symbol, line_number, column_number)
   symbol_ref2 = SymbolReference(symbol, line_number + 1, column_number)

   assert symbol_ref1 != symbol_ref2
   assert hash(symbol_ref1) != hash(symbol_ref2)

   symbol_ref3 = SymbolReference(symbol, line_number, column_number)
   assert symbol_ref1 == symbol_ref3

Limitations
-----------

The primary limitation of ``SymbolReference`` is that it could cause
collisions when the same symbol is referenced in different files at the
same location (line and column). This situation is relatively rare, but
it is worth noting as a potential limitation when working with a large
number of symbol references across multiple files.

Follow-up Questions:
--------------------

-  Is there any way to mitigate the collision issue while maintaining
   the utility methods provided by ``SymbolReference``?
