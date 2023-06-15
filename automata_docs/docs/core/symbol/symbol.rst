Symbol
======

``Symbol`` is similar to a URI and identifies a class, method, or a
local variable. It has the ability to interact with rich metadata about
symbols such as the docstring. Symbol has a standardized string
representation, which is the following:
``<symbol> ::= <scheme> ' ' <package> ' ' (<descriptor>)+ | 'local ' <local-id>``.
The class is part of the ``automata_docs.core.symbol.symbol_types``
module and the import statement is as follows:

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol

Overview
--------

``Symbol`` allows parsing and transforming of Symbol string
representations and provides information about the symbol. It supports
comparison, hashing, and string conversion. Moreover, it provides
utility methods such as ``dotpath``, ``module_name``, ``parent``, and
others to facilitate symbol examination and manipulation.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata_docs.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata_docs.tests.unit.test_symbol_parser.test_is_local_symbol``
-  ``automata_docs.core.database.vector.JSONVectorDatabase``
-  ``automata_docs.tests.unit.test_symbol_graph.test_get_all_symbols``
-  ``automata_docs.tests.unit.test_database_vector.test_add_symbol``

Example
-------

The following examples demonstrate how to create ``Symbol`` instances
using a class and a method.

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol
   from automata_docs.core.symbol.parser import parse_symbol

   symbol_class = parse_symbol(
       "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#"
   )

   symbol_method = parse_symbol(
       "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.base.tool`/ToolNotFoundError#__init__()."
   )

Limitations
-----------

The primary limitation of ``Symbol`` is that it mostly relies on its
string representation for parsing and transformation. As a result, any
changes or updates to the string representation may have undesired
effects on the behavior of the ``Symbol`` instances.

Follow-up Questions:
--------------------

-  How can we handle non-standard string representations when working
   with Symbol?
-  How can we avoid potential issues caused by updates to the string
   representation of Symbol?
