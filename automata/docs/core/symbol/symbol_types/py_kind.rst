SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of a
URI (Uniform Resource Identifier) into a Python object. It can be used
to represent descriptors for various types of elements, such as
namespaces, types, terms, methods, type parameters, parameters,
metadata, and macros. The class provides methods to parse and unparse
these descriptors, as well as handle escaped identifiers and suffix
conversion.

Overview
--------

``SymbolDescriptor`` is primarily used in the context of
``automata.core.base.symbol.Symbol``, a class that represents a
standardized string representation for various programming elements such
as packages, classes, methods, and more. By utilizing
``SymbolDescriptor``, it is possible to parse and store specific
descriptor information, which can be further used for symbol searching,
retrieval, or reference.

Related Symbols
---------------

-  ``automata.core.base.symbol.Symbol``
-  ``automata.core.symbol.parser._SymbolParser``
-  ``automata.core.base.symbol.SymbolDescriptor.PyKind``
-  ``automata.core.base.scip_pb2.Descriptor``

Examples
--------

Below are some examples using the ``SymbolDescriptor`` class:

.. code:: python

   from automata.core.base.symbol import SymbolDescriptor
   from automata.core.base.scip_pb2 import Descriptor as DescriptorProto

   # Create a SymbolDescriptor object for a Python method
   descriptor = SymbolDescriptor(
       name="__init__",
       suffix=DescriptorProto.METHOD,
       disambiguator=None
   )

   # Convert DescriptorProto suffix to PyKind
   python_suffix = SymbolDescriptor.convert_scip_to_python_suffix(DescriptorProto.METHOD)

   # Unescaping a name with special characters
   name = "`My`Escaped``Name`"
   unescaped_name = SymbolDescriptor.get_escaped_name(name)

Limitations
-----------

``SymbolDescriptor`` is focused on handling descriptors in the context
of the Symbol representation. It does not provide specific handling or
information for the symbols or programming elements it represents.
Additionally, the class assumes the usage of the provided descriptor
format, which may not cover all possible situations or programming
languages.

Follow-up Questions:
--------------------

-  Could ``SymbolDescriptor`` be extended to handle additional
   programming languages or descriptor formats more easily?
-  Are there any other limitations specific to ``SymbolDescriptor`` that
   should be considered?
