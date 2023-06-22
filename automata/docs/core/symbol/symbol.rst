Symbol
======

``Symbol`` is a class that identifies a class, method, or a local
variable similar to a URI. It has a standardized string representation
that can be used interchangeably with ``Symbol``. This class is useful
in creating unique identifiers for various symbols and provides utility
functions to perform comparisons, retrieve metadata, and interact with
related classes such as ``SymbolDescriptor``.

Overview
--------

``Symbol`` has a scheme, package, descriptors, and a string
representation called URI. It provides methods to compare symbols,
retrieve dotpath, module name, and symbol kinds. There are also
functions to check if the symbol is local, meta, parameter or protobuf.
Moreover, it allows creating a ``Symbol`` instance from a string
representation and getting its parent symbol.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.tests.unit.test_symbol_parser.test_is_local_symbol``
-  ``automata.tests.unit.test_database_vector.test_add_symbol``
-  ``automata.tests.unit.test_database_vector.test_add_symbols``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_references``
-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.symbol.parser.parse_symbol``

Example
-------

The following example demonstrates how to parse a ``Symbol`` using
provided URI strings:

.. code:: python

   from automata.core.symbol.parser import parse_symbol

   symbol_class = parse_symbol(
     "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#"
   )

   symbol_method = parse_symbol(
     "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__()."
   )

Limitations
-----------

``Symbol`` has some limitations regarding its string representation. It
assumes a specific format for the symbol string, and it may not work
correctly with non-conforming representations.

Follow-up Questions:
--------------------

-  Are there any alternative representations other than the standardized
   string representation for ``Symbol``?
-  How can we extend the functionality of ``Symbol`` to incorporate
   additional types of symbols?
