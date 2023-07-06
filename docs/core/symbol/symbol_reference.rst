SymbolReference
===============

``SymbolReference`` is a class in the ``automata.symbol.base``
module that represents a reference to a symbol in a file. It is
particularly useful in complex code structures where the same symbol can
be used in different parts of the code, and these references need to be
identified or compared.

Overview
--------

The ``SymbolReference`` class has two magic methods ``__eq__`` and
``__hash__`` which are used to evaluate equality and generate an
immutable hash, respectively. The class is used to compare instances of
``SymbolReference`` and check the equality of the ``uri``,
``line_number`` and ``column_number`` of the symbol reference. They are
also important for the usage of ``SymbolReference`` instances in sets or
dictionaries, where hash values are required.

Methods
-------

The class ``SymbolReference`` contains the following methods:

-  ``__eq__(self, other) -> bool`` : It checks the equality of two
   instances of ``SymbolReference`` by comparing the ``uri``,
   ``line_number`` and ``column_number`` of the ``SymbolReference``
   instances.

-  ``__hash__(self) -> int`` : This method creates a hash value for the
   instance of ``SymbolReference`` using the ``uri``, ``line_number``
   and ``column_number``.

It should be noted that the ``__hash__`` method could cause collisions
if the same symbol is referenced in different files at the same
location.

Related Symbols
---------------

-  ``automata.symbol.base.Symbol``
-  ``automata.symbol.graph.SymbolGraph``
-  ``automata.symbol.parser.parse_symbol``
-  ``automata.tests.unit.test_symbol_search.test_symbol_references``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_references``

Examples
--------

The following is an example demonstrating how to create an instance of
``SymbolReference`` and how to use the ``__eq__`` method.

.. code:: python

   from automata.symbol.base import Symbol, SymbolReference
   from automata.symbol.parser import parse_symbol

   symbol_uri = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#"
   symbol = parse_symbol(symbol_uri)

   symbol_ref_1 = SymbolReference(symbol=symbol, line_number=10, column_number=20)
   symbol_ref_2 = SymbolReference(symbol=symbol, line_number=10, column_number=20)

   print(symbol_ref_1 == symbol_ref_2)  # Will output: True

Follow-Up Questions:
--------------------

-  How are instances of ``SymbolReference`` generated in the system?
-  What are the likely scenarios where symbol collisions can occur and
   how are these handled?
-  Potential limitations or drawbacks of the ``__hash__`` implementation
   weren’t specified, can these be determined and documented?
