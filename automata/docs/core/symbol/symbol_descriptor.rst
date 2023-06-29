SymbolDescriptor
================

``SymbolDescriptor`` is a class that wraps the descriptor component of
the URI into a Python object. It provides utility methods to convert
SCIP (Symbol Common Intermediate Protocol) to Python suffixes, determine
if a given name is a simple identifier, and unparse the descriptor back
into a URI string.

Overview
--------

``SymbolDescriptor`` is mainly used in conjunction with ``Symbol`` to
identify symbols like classes, methods, or local variables. The class
stores the name, suffix, and an optional disambiguator for the
descriptor.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``

Example
-------

The following example demonstrates how to create an instance of
``SymbolDescriptor``.

.. code:: python

   from automata.core.symbol.base import SymbolDescriptor
   from automata.core.symbol.scip_pb2 import Descriptor as DescriptorProto

   name = "automata.core.agent.agent_enums.ActionIndicator"
   suffix = DescriptorProto.Type
   disambiguator = None

   descriptor = SymbolDescriptor(name, suffix, disambiguator)

Usage
-----

Here’s an example to unparse a ``SymbolDescriptor`` instance back into a
URI string:

.. code:: python

   unparsed_descriptor = descriptor.unparse()
   # Returns: "`automata.core.agent.agent_enums.ActionIndicator`#"

Limitations
-----------

-  The primary limitation of ``SymbolDescriptor`` is its reliance on
   SCIP protocols for conversion. It assumes that the notation for
   descriptor components will not change in the future, which may not
   always be the case.

-  SymbolDescriptor has a fixed set of descriptor suffix options. If new
   descriptor types are introduced, this class might need to be updated
   to accommodate those changes.

Follow-up Questions:
--------------------

-  Is there a better way to handle possible updates to the SCIP protocol
   or descriptor types, rather than simply updating the class with each
   change?
