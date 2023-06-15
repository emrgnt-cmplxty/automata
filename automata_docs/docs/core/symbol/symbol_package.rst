SymbolPackage
=============

``SymbolPackage`` is a class that wraps the package component of a
symbol’s URI, providing methods to represent and manipulate this
information. A package consists of three components: ``manager``,
``name``, and ``version``. Instances of this class are mainly used in
conjunction with the ``Symbol`` class, which represents a symbol (e.g.,
a class, method, or local variable) in a standardized format.

Overview
--------

The ``SymbolPackage`` class provides the following methods:

-  ``__repr__(self)``: Returns a string representation of the package.
-  ``unparse(self)``: Converts the ``SymbolPackage`` back into a URI
   string.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``: The main class
   used to represent and manipulate a symbol.

Example
-------

The following example shows how to create a ``SymbolPackage`` and
convert it back into a URI string.

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolPackage

   manager = "python"
   name = "automata_docs"
   version = "75482692a6fe30c72db516201a6f47d9fb4af065"

   package = SymbolPackage(manager=manager, name=name, version=version)
   uri_string = package.unparse()

   print(uri_string)  # Output: "python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065"

Limitations
-----------

``SymbolPackage`` serves as a simple container for a symbol’s package
component, and does not provide any functionality for querying or
modifying the package itself. Additionally, this class is tied to the
specific representation and format of a symbol as defined by the
``Symbol`` class.

Follow-up Questions:
--------------------

-  Are there plans to extend the functionality of ``SymbolPackage`` to
   better support varying symbol representations or formats?
