SymbolGraph
===========

``SymbolGraph`` is a class that represents the symbol graph of code,
providing utility methods and functionalities for analyzing and
interacting with the graph. The graph stores symbols such as classes,
methods, or local variables as nodes, and relationships between symbols
as edges. The ``SymbolGraph`` is useful for various code analysis tasks
like understanding callers of a function, dependencies between symbols,
and more.

Overview
--------

``SymbolGraph`` is built from an index protobuf file, and it supports
various operations related to symbol analysis, such as getting all
available symbols, retrieving potential callees or callers, getting a
subgraph of rankable symbols, and more. It also contains nested classes
like ``SubGraph``, which represents a subgraph of ``SymbolGraph``.

Related Symbols
---------------

-  ``automata.core.symbol.graph.GraphBuilder``
-  ``automata.core.symbol.graph.SymbolGraph.SubGraph``
-  ``automata.core.symbol.search.symbol_search.SymbolSearch``
-  ``automata.tests.utils.factories.symbol_graph_static_test``
-  ``automata.tests.conftest.symbol_graph_mock``

Example
-------

This example demonstrates how to create a ``SymbolGraph`` instance,
retrieve all symbols and files, and get a subgraph of rankable symbols.

*Note:* Make sure to replace ``index_path`` with the path to a valid
index protobuf file on your system.

.. code:: python

   from automata.core.symbol.graph import SymbolGraph

   index_path = "path/to/your/index.scip"
   symbol_graph = SymbolGraph(index_path)

   # Get all available symbols and files
   all_symbols = symbol_graph.get_all_available_symbols()
   all_files = symbol_graph.get_all_files()

   # Get a subgraph of rankable symbols
   subgraph = symbol_graph.get_rankable_symbol_subgraph()

Limitations
-----------

The ``SymbolGraph`` relies on an index protobuf file to populate the
graph. Creation and updates of this file are not part of the
``SymbolGraph`` class, which means any changes in the code require
rebuilding the index file before being reflected in the graph. Moreover,
loading a large graph might consume a significant amount of memory and
processing time.

Follow-up Questions:
--------------------

-  What is the process of updating the index protobuf file for a
   project?
-  Can the ``SymbolGraph`` be easily extended to support additional
   types of symbols or relationships?
-  Are there any strategies to handle large graphs more efficiently?
