SymbolPackage
=============

Overview
--------

``SymbolPackage`` is a class representing the package component of a
Symbol URI in Python. A Symbol URI is a standardized string
representation for a python class, method, or local variable. With
``SymbolPackage``, you can easily manage the packages associated with
your Symbols.

Import Statement
----------------

.. code:: python

   from automata.core.symbol.base import SymbolPackage

Related Symbols
---------------

-  ``automata.core.symbol.scip_pb2.Descriptor as DescriptorProto``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.utils.is_sorted``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.tests.unit.test_symbol_search.test_retrieve_source_code_by_symbol``
-  ``automata.core.symbol_embedding.base.SymbolCodeEmbedding``
-  ``automata.tests.unit.test_symbol_search.test_exact_search``
-  ``automata.core.symbol.base.Symbol.__repr__``
-  ``automata.tests.unit.sample_modules.sample.OuterClass``
-  ``automata.core.context_providers.symbol_synchronization.SymbolProviderSynchronizationContext``

Example
-------

The following is an example demonstrating how to generate
``SymbolPackage``.

.. code:: python

   from automata.core.symbol.parser import parse_symbol

   symbol_class = parse_symbol(
   "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 `automata.core.agent.agent_enums`/ActionIndicator#"
   )

   print(f"Package: {symbol_class.package}")

Limitations
-----------

Although ``SymbolPackage`` representation is string-friendly to work
with, it fails to capture the package structure or the hierarchical
relationship between packages and sub-packages, which could be crucial
in complex systems.

Methods Documentation
---------------------

``unparse(self) -> str:``
~~~~~~~~~~~~~~~~~~~~~~~~~

This method converts the SymbolPackage object back to its original URI
string form.

``__repr__(self) -> str:``
~~~~~~~~~~~~~~~~~~~~~~~~~~

This method generates a string representation of class blueprint.

Follow-up Questions:
--------------------

-  Can the ``SymbolPackage`` class representation be updated to capture
   hierarchical relationships in packaging structures?
-  How does ``SymbolPackage`` handle versioning in its string
   representation? Especially in situations where multiple versions of
   the same package exist in the system.
