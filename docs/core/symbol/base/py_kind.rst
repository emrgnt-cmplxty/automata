SymbolDescriptor
================

``SymbolDescriptor`` is a class to represent the description component
of a Symbol URI. A Symbol URI is a standardized string representation of
a Python class, method, or a local variable. ``SymbolDescriptor``
encapsulates the key aspect of a symbol - its unique descriptor. This
class recognizes that each Symbol URI has a unique descriptor, that
represents its unique identity within the package.

Overview
--------

``SymbolDescriptor`` takes ``name``, ``suffix`` and optionally
``disambiguator`` during its initialization and it provides several
methods to interact with and manipulate these attributes. The class
implements a ``__repr__`` method for generating a string representation
of the instance. The ``convert_scip_to_python_suffix`` is a crucial
method that maps a descriptor suffix from the SCIP protocol to the
Python-specific kind of that descriptor. In addition, it provides
methods to generate a URI-ready version of a name and to unparse a name
from a descriptor to its original format.

Related Symbols
---------------

-  ``automata.symbol.scip_pb2.Descriptor`` - the protobuf format of
   descriptor used to interact with descriptors
-  ``automata.symbol.base.Symbol`` - the base class for symbols for
   which ``SymbolDescriptor`` provides description functionality
-  ``automata.symbol.parser`` - where the ``parse_symbol`` method
   utilizes ``SymbolDescriptor``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolDescriptor``.

.. code:: python

   from automata.symbol.scip_pb2 import Descriptor as DescriptorProto
   from automata.symbol.base import SymbolDescriptor

   descriptor_suffix = DescriptorProto.NAME  # example value
   name = 'test_name'
   desc_obj = SymbolDescriptor(name, descriptor_suffix)

A descriptive example of using ``SymbolDescriptor`` is when we parse a
symbol -

.. code:: python

   from automata.experimental.search.symbol_parser import parse_symbol
   symbol_method = parse_symbol(
       "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.tools.base`/ToolNotFoundError#__init__()."
   )
   # SymbolDescriptor is used internally in this process

Limitations
-----------

The primary limitation of ``SymbolDescriptor`` is that it only supports
descriptors that follow the SCIP standard. Therefore, while it provides
a flexible way to create, manage, and interact with descriptors, it may
not be able to accurately work with descriptors that are not in SCIP
standard.

Follow-up Questions
-------------------

-  Are there plans to support parsing symbols with descriptors that do
   not follow the SCIP standard?
-  How are errors handled when a descriptor not following SCIP standard
   is passed to the ``SymbolDescriptor`` class?
