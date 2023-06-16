SymbolPackage
=============

``SymbolPackage`` is a class that wraps the package component of the
URI. It helps manage and handle packages in the context of symbols,
which are like URIs identifying a class, method, or a local variable.

Overview
--------

The ``SymbolPackage`` class consists of utility methods to work with
packages in the context of a ``Symbol``. It provides methods to unparse
a package into a URI string and get the string representation of the
package.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.parser.parse_symbol``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolPackage`` and unparse it into a URI string.

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolPackage

   example_package = SymbolPackage(manager="python", name="automata_docs", version="75482692a6fe30c72db516201a6f47d9fb4af065")
   print(repr(example_package))  # Output: Package(python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065)

.. code:: python

   unparsed_package = example_package.unparse()
   print(unparsed_package)  # Output: python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065

Limitations
-----------

``SymbolPackage`` is limited in its functionality and mainly serves as
an abstraction of the package component of a symbol URI. It does not
provide any advanced features for package management or manipulation
beyond its primary functionalities of unparsing a package into a URI
string and obtaining its string representation.

Follow-up Questions:
--------------------

-  Are there any additional methods or features that would be useful to
   include in the ``SymbolPackage`` class?
