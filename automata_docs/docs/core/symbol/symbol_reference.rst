SymbolReference
===============

``SymbolReference`` is a class that represents a reference to a symbol
in a file. It provides methods for equality and hashing based on its
attributes, which include the symbol, line number, and column number in
the file. This class is related to other symbols used in the Automata
Docs project, such as ``Symbol``, ``SymbolEmbedding``, and others.

Overview
--------

``SymbolReference`` stores information about the symbol it references
and its location (line and column number) within the file. Comparisons
between ``SymbolReference`` instances are made by comparing their
symbol’s URI, line number, and column number. These attributes are
hashed to produce a unique identifier for each ``SymbolReference``
instance.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.symbol.graph.SymbolGraph``

Example
-------

Suppose we have two instances of ``SymbolReference`` with the same
symbol URI, line number, and column number:

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol
   from automata_docs.core.symbol.parser import parse_symbol

   symbol_uri = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   symbol = parse_symbol(symbol_uri)

   ref1 = SymbolReference(symbol=symbol, line_number=10, column_number=5)
   ref2 = SymbolReference(symbol=symbol, line_number=10, column_number=5)

Comparing them for equality and hashing:

.. code:: python

   print(ref1 == ref2)  # True
   print(hash(ref1) == hash(ref2))  # True

Limitations
-----------

The current implementation of ``SymbolReference`` might cause collisions
if the same symbol is referenced in different files at the same
location. However, this is unlikely due to the uniqueness of the Symbol
URI - especially the commit hash associated with each symbol.

Follow-up Questions:
--------------------

-  Can you provide an example of how to use ``SymbolFile`` in the
   context of ``SymbolReference``?
-  How can we improve the hash function to avoid collisions even
   further?
