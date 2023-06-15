SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of a
Symbol’s URI into a Python object. It is used in conjunction with the
``Symbol`` class for working with standardized string representations of
classes, methods, or local variables in a Python project. The
``SymbolDescriptor`` class offers utility methods for working with the
descriptor component, including converting ``DescriptorProto`` to the
more Python-friendly ``PyKind``.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.scip_pb2.Descriptor``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolDescriptor.PyKind``

Example
-------

The following is an example demonstrating how to use a
``SymbolDescriptor`` object:

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolDescriptor
   from automata_docs.core.symbol.scip_pb2 import Descriptor as DescriptorProto

   descriptor_name = "ToolNotFoundError"
   descriptor_suffix = DescriptorProto.TYPE
   descriptor = SymbolDescriptor(descriptor_name, descriptor_suffix)

   # Accessing properties
   print(descriptor.name)  # Output: ToolNotFoundError
   print(descriptor.suffix)  # Output: 1 (corresponding to DescriptorProto.TYPE)

Limitations
-----------

The primary limitation of ``SymbolDescriptor`` lies in its dependency on
specific syntax and formatting for symbol URI. It requires the proper
usage of ``DescriptorProto`` and assumes the specific structure of the
symbol URI string.

Follow-up Questions:
--------------------

-  What are the possible improvements for ``SymbolDescriptor`` to make
   it more flexible for different URI formats?

Method Summary
--------------

**init**\ (self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Constructor for the ``SymbolDescriptor`` class, which initializes a new
instance with the given name, suffix, and optional disambiguator.

**repr**\ (self) -> None
~~~~~~~~~~~~~~~~~~~~~~~~

Return the string representation of the ``SymbolDescriptor`` instance.

convert_scip_to_python_suffix(descriptor_suffix: DescriptorProto) -> PyKind
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Converts a ``DescriptorProto`` suffix to its corresponding ``PyKind``
value.

get_escaped_name(name) -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Checks if the provided string ``name`` is a valid escaped identifier.

is_simple_identifier(name) -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Checks if the provided string ``name`` is a simple identifier.

unparse(self) -> None
~~~~~~~~~~~~~~~~~~~~~

Returns the unparsed string representation of the ``SymbolDescriptor``
instance, including the name, suffix, and optional disambiguator.
