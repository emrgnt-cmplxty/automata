SymbolReference
===============

``SymbolReference`` is a class representing a reference to a symbol in a
file. It provides equality and hashing functions that allow easy
comparison and storage of symbol references. This class is used in
various contexts, such as symbol searching, symbol embedding, and
retrieving source code by symbol.

Overview
--------

``SymbolReference`` is mainly used to reference a symbol in a file and
is utilized in various applications, such as searching for symbol
references or storing them in databases. By providing equality and
hashing methods, ``SymbolReference`` allows for simple handling and
comparison of symbol reference objects, even across different files.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.graph._SymbolGraphNavigator._get_symbol_references_in_scope``
-  ``automata.tests.unit.test_symbol_search.tool.test_symbol_references``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``
-  ``automata.core.symbol_embedding.base.SymbolDocEmbedding``

Example
-------

.. code:: python

   from automata.core.symbol.base import Symbol, SymbolReference

   # Create two Symbol objects
   symbol_1 = Symbol.from_string("scip-python python automata 0.1.0 AutomataNamespace/ClassName#")
   symbol_2 = Symbol.from_string("scip-python python automata 0.2.0 AutomataNamespace/ClassName#")

   # Create two SymbolReference objects with the created Symbol objects
   symbol_reference_1 = SymbolReference(symbol=symbol_1, line_number=10, column_number=5)
   symbol_reference_2 = SymbolReference(symbol=symbol_2, line_number=10, column_number=5)

   # Evaluate the equality of the SymbolReference objects
   assert symbol_reference_1 != symbol_reference_2

Limitations
-----------

Although ``SymbolReference`` provides an efficient way to compare symbol
references, its hashing method can potentially generate collisions if
the same symbol is referenced in different files at the same location.
This might affect performance when storing symbol references in large
collections, such as dictionaries or sets. However, this does not
significantly impact the overall functionality or usability of the
class.

Follow-up Questions:
--------------------

-  Are there any other known use cases for ``SymbolReference`` apart
   from those in the related symbols?
