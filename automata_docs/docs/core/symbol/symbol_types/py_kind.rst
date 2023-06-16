SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of
the URI into a Python object. It serves as a building block for creating
and parsing symbols within the ``automata_docs.core.symbol`` framework.
Additionally, it provides methods for working with descriptor
components, such as converting descriptor suffixes and unparsing
descriptor objects.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.parser.SymbolParser``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolReference``
-  ``automata_docs.core.symbol.graph.SymbolGraph``

Example
-------

The following example demonstrates how to create a ``SymbolDescriptor``
instance:

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolDescriptor
   from automata_docs.core.symbol.scip_pb2 import Descriptor as DescriptorProto

   descriptor = SymbolDescriptor(
       name="ActionIndicator",
       suffix=DescriptorProto.TYPE,
   )

Methods
-------

-  ``__init__(self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None)``:
   Initializes a ``SymbolDescriptor`` instance with the given ``name``,
   ``suffix``, and an optional ``disambiguator``.
-  ``__repr__(self) -> None``: Represents the ``SymbolDescriptor`` as a
   string.
-  ``convert_scip_to_python_suffix(descriptor_suffix: DescriptorProto) -> PyKind``:
   Converts a descriptor suffix from the ``DescriptorProto`` format to
   the ``PyKind`` format.
-  ``get_escaped_name(name) -> None``: Escapes a string name with
   backticks.
-  ``is_simple_identifier(name) -> None``: Determines if the given name
   is a simple identifier or not.
-  ``unparse(self) -> None``: Unparses the ``SymbolDescriptor`` instance
   into a string.

Limitations
-----------

``SymbolDescriptor`` is closely tied to the
``automata_docs.core.symbol`` framework and assumes a specific syntax
and representation for descriptor components. If the underlying
descriptor format or parser implementation changes, updates to
``SymbolDescriptor`` may be necessary.

Follow-up Questions:
--------------------

-  How does the ``SymbolDescriptor`` interact with other parts of the
   ``automata_docs.core.symbol`` framework?
