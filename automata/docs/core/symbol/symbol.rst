Symbol
======

``Symbol`` is a class that identifies a class, method, or a local
variable, similar to a URI. ``Symbol`` contains rich metadata about
symbols, such as docstrings. It has a standardized string representation
that can be used interchangeably, with a specific syntax to represent
each type of symbol.

``Symbol`` provides various methods, utility functions, and attributes
to work with symbols, compare them, and extract information such as the
symbol’s module name, parent symbol, dotpath, and symbol kind.

Overview
--------

``Symbol`` is initialized with four parameters - ``uri``, ``scheme``,
``package``, and ``descriptors``. It provides methods to compare two
symbols, get a symbol’s dotpath, hash a symbol, and create a string
representation of the symbol. Additionally, it includes utility
functions to determine whether a symbol is local, meta, parameter, or
protobuf.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.core.base.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.core.memory_store.symbol_code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.tests.unit.test_database_vector.test_add_symbol``

Example
-------

.. code:: python

   from automata.core.symbol.parser import parse_symbol

   symbol_class = parse_symbol("scic-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#")

   symbol_method = parse_symbol("scic-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__().")

Limitations
-----------

The primary limitation of the ``Symbol`` class is that it assumes a
specific structure and syntax for symbols. Incorrectly formatted symbols
may result in errors or unexpected behavior during parsing or usage.

Follow-up Questions:
--------------------

-  Are there any plans to support custom symbol formats?
-  Can symbol representations be easily extended to support additional
   symbol types if needed in the future?
