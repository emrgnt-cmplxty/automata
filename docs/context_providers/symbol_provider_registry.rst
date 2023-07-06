SymbolProviderRegistry
======================

Overview
--------

``SymbolProviderRegistry`` is a central registry management class which
keeps track of the multiple symbol providers in the system. The primary
role of the ``SymbolProviderRegistry`` is to synchronize the symbols
supported by several symbol providers and maintain them in a sorted
order. It ensures that only the common symbols across the system are
taken into account by the application.

This class operates primarily on singleton methods to maintain and
provide a single central registry.

Related Symbols
---------------

-  ``automata.symbol.base.Symbol``
-  ``automata.symbol.base.ISymbolProvider``
-  ``automata.tests.unit.test_symbol_graph.test_get_all_symbols``
-  ``automata.tests.unit.test_symbol_graph.test_build_real_graph``
-  ``automata.context_providers.symbol_synchronization.SymbolProviderSynchronizationContext.register_provider``
-  ``automata.context_providers.symbol_synchronization.SymbolProviderSynchronizationContext.synchronize``

Usage Example
-------------

.. code:: python

   from automata.symbol.base import ISymbolProvider, Symbol
   from automata.context_providers.symbol_synchronization import SymbolProviderRegistry

   # Define a custom symbol provider
   class CustomSymbolProvider(ISymbolProvider):
       ...

   custom_provider = CustomSymbolProvider()

   # Register your custom provider
   SymbolProviderRegistry.register_provider(custom_provider)

   # Synchronize the symbols across all providers
   SymbolProviderRegistry.synchronize()

   # Get the sorted list of supported symbols
   symbols = SymbolProviderRegistry.get_sorted_supported_symbols()

   # Your code with the symbol
   ...

Limitations
-----------

``SymbolProviderRegistry`` relies on the symbol providers in the system
implementing the ``ISymbolProvider`` interface correctly. If a symbol
provider provides incorrect or incomplete information about supported
symbols, it may introduce errors in the sorted symbols list.
Additionally, the registry assumes that all symbol providers will be
registered before any get or synchronize operation is performed. If a
new symbol provider is added after synchronization, it will not be
considered until the next synchronization.

Follow-up Questions
-------------------

-  How does adding a new symbol provider after synchronization affect
   the result? Is there a watch mechanism or notification setup in
   symbol providers when new symbols get added?
-  What precautions or considerations should be taken while implementing
   a custom symbol provider to ensure compatibility with
   ``SymbolProviderRegistry``?
