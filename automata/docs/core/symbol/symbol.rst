Symbol
======

``Symbol`` is a class that identifies a class, method, or local variable
in a package. It works similarly to a URI and includes rich metadata
such as the docstring. It has a standardized string representation that
can be used interchangeably with Symbol. The syntax and examples of
Symbol can be found below.

Overview
--------

``Symbol`` identifies a class, method, or local variable and includes
rich metadata. It has a standardized string representation that can be
used interchangeably with Symbol. ``Symbol`` instances can be created
from string representations and can be compared with one another. Each
``Symbol`` instance comes with utility methods for parsing, creating,
and querying symbolic data. Related symbols include those within
embedding, graph, and parser modules.

Related Symbols
---------------

-  ``automata.core.embedding.code_embedding.SymbolCodeEmbeddingHandler``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.tests.unit.test_symbol_parser.test_is_local_symbol``
-  ``automata.tests.unit.test_symbol_graph.test_get_all_symbols``
-  ``automata.core.embedding.doc_embedding.SymbolDocEmbeddingHandler``

Example
-------

The following examples demonstrate how to create an instance of
``Symbol`` using the ``parse_symbol`` function.

.. code:: python

   from automata.core.symbol.search.symbol_parser import parse_symbol

   symbol_class = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.automata_agent_enums`/ActionIndicator#"
   )

   symbol_method = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.base.tool`/ToolNotFoundError#__init__()."
   )

Limitations
-----------

``Symbol`` assumes specific syntax when parsing string representations,
and it can only handle specific symbol types. It does not support custom
symbol types or variations in syntax.

Follow-up Questions:
--------------------

-  How can we extend Symbol to support custom symbol types and
   variations in syntax?
