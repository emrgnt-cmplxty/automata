SymbolDescriptor
================

``SymbolDescriptor`` is a class that represents the description
component of a Symbol URI. It includes functionalities to parse and
unparse symbol identifiers in Python and convert between different
symbol descriptors.

Overview
--------

``SymbolDescriptor`` is used for naming and addressing symbols. It
includes a list of Python kinds of symbols in the nested ``PyKind``
Enum. Each instance of ``SymbolDescriptor`` stores a symbol name, a
descriptor suffix, and an optional disambiguator.

The class provides methods to unparse the descriptor back into an URI
string, get the escaped name of a symbol, and convert a Scip suffix to a
python kind.

Related Symbols
---------------

-  ``DescriptorProto``
-  ``Enum``

Example
-------

The following is an example demonstrating how to create and manipulate
an instance of ``SymbolDescriptor``.

.. code:: python

   from automata.symbol.symbol_base import SymbolDescriptor
   from DescriptorProto import DescriptorProto

   descriptor = SymbolDescriptor('sample', DescriptorProto.Type, 'disambiguator')

   # Print the descriptor
   print(repr(descriptor))

   # Unparse the descriptor to an URI string
   print(descriptor.unparse())

Limitations
-----------

The ``SymbolDescriptor`` class uses strict rules to parse and unparse
symbols. It may not cater to all Python codes if unconventional naming
schemes are used.

A caveat to note is that the ``unparse`` method raises a ValueError
exception if an invalid Descriptor suffix is provided. Care must be
taken to ensure the symbol’s Descriptor suffix is one of the defined
DescriptorProto values.

Follow-up Questions:
--------------------

-  Are there situations where escaping the name of a symbol can cause
   issues?
-  Can ``SymbolDescriptor`` handle all Python names, or are there some
   limitations to consider?
-  Is it possible to extend the ``PyKind`` Enum to cater to additional
   symbol types?
-  How does the class handle ambiguous symbols, ones that can fit into
   multiple ``PyKind`` categories?
