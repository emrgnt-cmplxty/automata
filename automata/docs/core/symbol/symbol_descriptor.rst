SymbolDescriptor
================

``SymbolDescriptor`` is a wrapper class for the descriptor component of
the URI in the ``automata.core.symbol.symbol_types`` module. The purpose
of this class is to wrap a descriptor into a Python object to make it
more convenient to work with.

Overview
--------

``SymbolDescriptor`` contains three attributes: ``name``, ``suffix``,
and ``disambiguator``, representing the name of the symbol, the suffix
used for symbol kind identification, and an optional disambiguator
string to differentiate between symbols with the same name. It also
provides static methods for converting between SCIP and Python suffixes,
escaping names, and unparsing the descriptor back into a URI string.

Methods
-------

-  ``__init__(self, name: str, suffix: DescriptorProto, disambiguator: Optional[str] = None) -> None``
-  ``__repr__(self) -> str``
-  ``convert_scip_to_python_suffix(descriptor_suffix: DescriptorProto) -> PyKind``
-  ``get_escaped_name(name) -> str``
-  ``is_simple_identifier(name) -> bool``
-  ``unparse(self) -> str``

Related Symbols
---------------

-  ``automata.core.symbol.search.symbol_parser.parse_symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.parser._SymbolParser.parse_descriptor``

Example Usage
-------------

In this example, we create an instance of ``SymbolDescriptor`` and
demonstrate how to access its attributes and methods:

.. code:: python

   from automata.core.symbol.symbol_types import SymbolDescriptor
   from automata.core.symbol.scip_pb2 import Descriptor as DescriptorProto

   name = "example_symbol"
   suffix = DescriptorProto.LOCAL
   descriptor = SymbolDescriptor(name, suffix)

   #print descriptor attributes
   print(descriptor.name)         # Output: example_symbol
   print(descriptor.suffix)       # Output: LOCAL
   print(descriptor.disambiguator)  # Output: None

   #print the representation of the descriptor
   print(descriptor)               # Output: Descriptor(example_symbol, LOCAL)

   #convert SCIP suffix to Python suffix
   python_suffix = SymbolDescriptor.convert_scip_to_python_suffix(suffix)
   print(python_suffix)           # Output: PyKind.Local

   #get escaped name of the symbol
   escaped_name = SymbolDescriptor.get_escaped_name(name)
   print(escaped_name)            # Output: example_symbol

   #check if the name is a simple identifier
   is_simple = SymbolDescriptor.is_simple_identifier(name)
   print(is_simple)               # Output: True

   #unparse the descriptor back into URI string
   uri_string = descriptor.unparse()
   print(uri_string)              # Output: example_symbol

Limitations
-----------

The main limitation of the ``SymbolDescriptor`` class is the assumption
that the descriptor is always in the SCIP protocol format. If a non-SCIP
format is used, the class would need to be modified accordingly.

Follow-up Questions:
--------------------

-  Are there any known cases where the descriptor component of the URI
   is not in the SCIP format, and would this affect the
   ``SymbolDescriptor`` class?
