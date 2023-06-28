SymbolPackage
=============

``SymbolPackage`` is a class that wraps the package component of a URI.
It provides methods to parse and unparse the package information to and
from URI string format.

Related Symbols
---------------

-  ``automata.core.symbol.scip_pb2.Descriptor``
-  ``automata.core.symbol.parser.parse_symbol``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_symbol_parser.test_parse_symbol``

Methods
-------

``__repr__(self) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~~

Returns a string representation of the ``SymbolPackage`` object.

``unparse(self) -> str``
~~~~~~~~~~~~~~~~~~~~~~~~

Converts the ``SymbolPackage`` object back into URI string format.

Example
-------

The ``SymbolPackage`` class is typically used in conjunction with the
``parse_symbol`` function from the ``automata.core.symbol.parser``
module.

.. code:: python

   from automata.core.symbol.parser import parse_symbol

   symbol_str = "scip-python python automata 75482692a6fe30c72db516201a6f47d9fb4af065 automata.core.agent.agent_enums/ActionIndicator#"
   symbol = parse_symbol(symbol_str)

   assert symbol.package.manager == "python"
   assert symbol.package.name == "automata"
   assert symbol.package.version == "75482692a6fe30c72db516201a6f47d9fb4af065"

Follow-up Questions:
--------------------

-  Are there any limitations or edge cases when using the
   ``SymbolPackage`` methods ``__repr__`` and ``unparse``? Consider:
   does the representation handle spaces, punctuation, or special
   characters?
