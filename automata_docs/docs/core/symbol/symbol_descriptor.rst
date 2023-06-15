SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of
the URI into a Python object. It provides methods for converting between
the descriptor’s SCIP suffix and Python representation as well as
unescaping and unescaping symbol names. The ``SymbolDescriptor`` class
can be used in conjunction with other components such as the ``Symbol``,
``SymbolParser`` and the ``SymbolGraph`` classes for processing and
analyzing symbols in Python projects.

Overview
--------

The ``SymbolDescriptor`` class offers the following methods:

-  ``__init__(self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None)``:
   Initializes the ``SymbolDescriptor`` instance with the provided
   ``name``, ``suffix``, and optional ``disambiguator``.
-  ``__repr__(self)``: Provides a string representation of the
   ``SymbolDescriptor`` instance.
-  ``convert_scip_to_python_suffix(descriptor_suffix: DescriptorProto) -> PyKind``:
   Converts the given SCIP descriptor suffix to the corresponding Python
   representation.
-  ``get_escaped_name(name)``: Returns the escaped version of the input
   ``name``.
-  ``unparse(self)``: Converts the ``SymbolDescriptor`` instance back
   into a URI string.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``: Represents a
   symbol with metadata, similar to a URI.
-  ``automata_docs.core.symbol.parser.SymbolParser``: Contains methods
   for parsing symbols into structured objects.
-  ``automata_docs.core.symbol.graph.SymbolGraph``: A graph
   representation of the symbols and their relationships.

Example
-------

The following example demonstrates how to use ``SymbolDescriptor`` in
conjunction with the ``parse_symbol`` function:

.. code:: python

   from automata_docs.core.symbol.parser import parse_symbol
   from automata_docs.core.symbol.symbol_types import SymbolDescriptor

   symbol_uri = "scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.base.tool`/ToolNotFoundError#__init__()."
   symbol = parse_symbol(symbol_uri)
   descriptor = symbol.descriptors[-1]

   # Access the descriptor properties
   print(descriptor.name) # Output: __init__
   print(descriptor.suffix) # Output: 4 (integer representation of SCIP Suffix.Method)

   # Unparse the descriptor into its URI string representation
   unparsed_descriptor = descriptor.unparse()
   print(unparsed_descriptor) # Output: __init__(Met).

Limitations
-----------

``SymbolDescriptor`` itself does not have any significant limitations.
However, when working with related classes like ``SymbolParser`` and
``Symbol``, it is important to ensure that their implementations are
synchronized with the source library to keep the parsing and processing
consistent.

Follow-up Questions:
--------------------

-  Are there any additional utility methods you’d like to see
   implemented in ``SymbolDescriptor``?
