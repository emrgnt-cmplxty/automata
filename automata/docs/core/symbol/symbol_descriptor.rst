SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of
the URI into a Python object. It represents different symbols of a URI
such as local, namespace, type, method, term, macro, parameter, and
type-parameter. The ``SymbolDescriptor`` class provides methods to
convert the descriptor suffix from the URI representation to a Python
representation, extract the escaped name from a given string, and
represent the object as a URI string.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.parser.SymbolParser.parse_descriptor``
-  ``automata.core.symbol.parser.SymbolParser.parse_descriptors``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.symbol_types.Symbol.dotpath``
-  ``automata.core.symbol.symbol_types.Symbol.is_local``
-  ``automata.core.symbol.symbol_types.Symbol.is_meta``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolDescriptor`` using a name, suffix, and an optional
disambiguator.

.. code:: python

   from automata.core.symbol.symbol_types import SymbolDescriptor
   from automata.core.symbol.scip_pb2 import Descriptor as DescriptorProto

   name = "example_descriptor"
   suffix = DescriptorProto.Type
   disambiguator = "example_disambiguator"

   descriptor = SymbolDescriptor(name, suffix, disambiguator)

Limitations
-----------

``SymbolDescriptor`` relies on the specific structure of the URI
representation and assumes a specific format for the descriptor suffix.
As a result, it may not support handling custom URI representations or
descriptors that do not follow the predefined format and structure.

Follow-up Questions:
--------------------

-  Is there a way to update ``SymbolDescriptor`` to handle custom URI
   representations or descriptors that do not follow the predefined
   format?
-  Are there any precautions that need to be taken when using
   ``SymbolDescriptor``, e.g., ensuring a correct format for the
   descriptor suffix and disambiguator?
