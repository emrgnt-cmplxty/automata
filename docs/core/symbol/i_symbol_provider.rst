ISymbolProvider
===============

``ISymbolProvider`` is an abstract base class that provides an interface
for classes that work with a collection of symbols. It contains several
methods aimed at managing, updating, and retrieving symbols.

Overview
--------

``ISymbolProvider`` is an abstract base class in the Automata library.
Its main purpose is to enforce a standard interface for classes that
manage symbolic representations in the library. It includes methods to
filter, sort, and manipulate symbols, as well as methods to mark symbol
collection as synchronized. ``ISymbolProvider`` is instantiated
indirectly via a child class.

Methods
-------

The core methods in the ``ISymbolProvider`` class include:

-  ``__init__``: Initializes a new instance of an ``ISymbolProvider``
   subclass with the ``is_synchronized`` flag set to ``False``.

-  ``filter_symbols``: An abstract method that needs to be implemented
   by any subclass. It is designed to filter the set of symbols managed
   by the class.

-  ``get_sorted_supported_symbols``: This method retrieves a list of
   sorted symbols. If the ``is_synchronized`` flag is ``False``, a
   ``RuntimeError`` is raised. It checks that the symbols are properly
   sorted.

-  ``set_synchronized``: This method sets the ``is_synchronized`` flag
   to the provided value. This method is used to update the state of the
   ``ISymbolProvider`` instance.

Related Symbols
---------------

Some symbolic classes and methods that are related to
``ISymbolProvider`` include:

-  ``automata.tests.unit.test_symbol_graph.test_get_all_symbols``
-  ``automata.tests.unit.test_symbol_graph.test_build_real_graph``
-  ``automata.context_providers.symbol_synchronization.SymbolProviderRegistry``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``

Example
-------

As ``ISymbolProvider`` is an abstract class, it cannot be directly
instantiated. A subclass implementing the ``filter_symbols`` function
must be created:

.. code:: python

   class SymbolProviderExample(ISymbolProvider):
       def filter_symbols(self, sorted_supported_symbols: List[Symbol]) -> None:
           self.sorted_supported_symbols = sorted_supported_symbols

Limitations
-----------

One major limitation of ``ISymbolProvider`` is that it is an abstract
class. This means it cannot be directly instantiated. Instead,
developers must subclass ``ISymbolProvider`` and provide an
implementation for the ``filter_symbols`` method.

Another potential limitation is the synchronization requirement, where
the ``is_synchronized`` flag needs to be set prior to attempting to
retrieve symbols. This could potentially lead to runtime exceptions
depending on the order of operations.

Follow-up Questions:
--------------------

1. How are subclasses of ``ISymbolProvider`` intended to implement the
   ``filter_symbols`` method? What criteria should they use to filter
   symbols?
2. Are there any performance implications associated with the checks
   performed in the ``get_sorted_supported_symbols`` method?
3. What happens if the sorted_symbols list is not correctly sorted? How
   does this impact the performance and reliability of the symbol
   provider?
4. Can there be multiple instances of a child class of
   ``ISymbolProvider`` working with different sets of symbols? If so,
   how is the synchronization managed across different instances?
