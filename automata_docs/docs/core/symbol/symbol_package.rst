SymbolPackage
=============

``SymbolPackage`` is a class that wraps the package component of a URI
(Uniform Resource Identifier) and provides methods to work with it
conveniently. It is a part of the ``Symbol`` class, which is similar to
a URI and identifies a class, method, or local variable in the context
of Automata documentation.

Overview
--------

``SymbolPackage`` is a utility class for handling the package component
of a URI. It provides methods to convert the package component back into
a URI string and to represent it as a string itself. It is closely
related to other symbols like the ``Symbol`` class itself and the rest
of the classes in the ``automata_docs.core.symbol.symbol_types`` module.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolPackage`` and obtain the URI string from it.

.. code:: python

   from automata_docs.core.symbol.symbol_types import SymbolPackage

   manager = "python"
   name = "automata_docs"
   version = "75482692a6fe30c72db516201a6f47d9fb4af065"

   package = SymbolPackage(manager, name, version)
   uri_string = package.unparse()

   print(uri_string)

Methods
-------

-  ``__repr__(self)``: Returns a string representation of the
   ``SymbolPackage`` object.
-  ``unparse(self)``: Converts the ``SymbolPackage`` object back into a
   URI string.

Limitations
-----------

The ``SymbolPackage`` class is specifically designed for handling the
package component of a URI in the context of Automata documentation. It
may not be suitable for more general URI handling in other projects or
libraries.

Follow-up Questions:
--------------------

-  Are there any other specific use cases for the ``SymbolPackage``
   class outside the Automata documentation context?
