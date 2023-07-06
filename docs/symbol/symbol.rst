Symbol
======

The ``Symbol`` class in Automata is used to represent a reference to a
Python object in a standardized format. This could be a class, method,
or a local variable. The ``Symbol`` is specified by a Uniform Resource
Identifier (URI) with a defined syntax.

Overview
--------

The ``Symbol`` class primarily works with the concept of a URI. A URI
for a Symbol is composed of a ``scheme``, ``package``, and
``descriptor``. The ``scheme`` consists of any UTF-8 characters, and
spaces within this portion of the URI need to be escaped using a double
space. The ``package`` specifies the ``manager``, ``package-name``, and
``version``. The ``descriptors`` define the ``namespace``, ``type``,
``term``, ``method``, ``type-parameter``, ``parameter``, ``meta``, or
``macro``.

Useful methods offered by the ``Symbol`` class include:

-  ``__eq__()``: Compares the current symbol to another to determine
   equivalence.
-  ``__hash__()``: Calculates the hash value of a symbol.
-  ``__repr__()``: Returns the string representation of the Symbol
   instance.
-  ``dotpath()``: Returns the dotpath of the symbol.
-  ``from_string()``: Creates a ``Symbol`` instance from a string
   representation.
-  ``is_local()``, ``is_meta()``, ``is_parameter()``, ``is_protobuf()``:
   These methods help determine the type of symbol based on the
   descriptor attributes.
-  ``module_name()``: Returns the module name of the symbol.
-  ``parent()``: Returns the parent symbol of the current symbol.
-  ``symbol_kind_by_suffix()``, ``symbol_raw_kind_by_suffix()``: The two
   methods convert the suffix of the URI into PyKind and DescriptorProto
   respectively, which help determine the type of symbol.

Examples
--------

Here is an example of how you can use the ``Symbol`` class:

.. code:: python

   from automata.experimental.search.symbol_parser import parse_symbol

   symbol_class = parse_symbol(
   "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.agent.agent_enums`/ActionIndicator#"
   )

   symbol_method = parse_symbol(
   "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.base`/ToolNotFoundError#__init__()."
   )

Related Symbols
---------------

The following are the related symbols:

-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata.symbol_embedding.base.SymbolEmbedding.symbol``
-  ``automata.tests.unit.test_database_vector.test_delete_symbol``
-  ``automata.symbol_embedding.base.SymbolCodeEmbedding``
-  ``automata.tests.unit.test_symbol_parser.test_is_local_symbol``

Limitations
-----------

Given that the ``Symbol`` class relies on formatting a URI with a
specific syntax, it is important to follow the symbol syntax strictly,
especially when dealing with special characters.

Dependencies
------------

-  ``automata.symbol.parser.parse_symbol``: This parses a ``Symbol``
   given a URI.

Follow-up Questions:
--------------------

-  What happens if the supplied URI for the ``Symbol`` doesn’t match the
   specified format?
-  What if the ``scheme`` or ``package`` supplied in the URI doesn’t
   exist?
-  Is there any way to validate if the ``Symbol`` created maps to a
   valid Python object?
