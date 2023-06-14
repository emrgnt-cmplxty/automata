SymbolReference
===============

``SymbolReference`` represents a reference to a symbol in a file. This
class is part of the automata_docs.core.symbol.symbol_types and provides
functionality to determine the equality and hash value of a symbol
reference based on its URI, line number, and column number.

Overview
--------

A ``SymbolReference`` is mainly used for code analysis and navigation
tasks. It stores the location and context of a symbol within a specific
file. The main use of the ``SymbolReference`` is to be able to identify
and compare different symbol references based on their unique properties
like URI, line number, and column number.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.SymbolEmbedding``
-  ``automata_docs.core.embedding.symbol_embedding.SymbolCodeEmbeddingHandler``
-  ``automata_docs.core.symbol.symbol_types.SymbolDescriptor``
-  ``automata_docs.core.context.py_context.retriever.PyContextRetriever``

Example
-------

.. code:: python

   from automata_docs.core.symbol.symbol_types import Symbol, SymbolReference

   symbol = Symbol("scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.agent.automata_agent_enums`/ActionIndicator#")
   symbol_ref = SymbolReference(symbol, 10, 5)

   other_symbol = Symbol("scip-python python automata_docs 75482692a6fe30c72db516201a6f47d9fb4af065 `automata_docs.core.base.tool`/ToolNotFoundError#__init__().")
   other_symbol_ref = SymbolReference(other_symbol, 10, 5)

   # Check equality of symbol references
   print(symbol_ref == other_symbol_ref)

Limitations
-----------

The primary limitation of ``SymbolReference`` is that it may produce
collisions if the same symbol is referenced in different files at the
same location. This limitation should be carefully considered when
working with large codebases with multiple similar symbol references.

Follow-up Questions:
--------------------

-  How can the risk of collisions be minimized when working with
   ``SymbolReference`` instances?
