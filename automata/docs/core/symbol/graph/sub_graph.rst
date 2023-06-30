``SymbolGraph.SubGraph``
========================

``SymbolGraph.SubGraph`` is a class representing a subgraph of the
symbol graph generated from the symbols available in the index protobuf
file. It enables easier navigation and analysis of the symbol graph by
providing methods to access the subgraph’s elements, their properties,
and the relationships between them.

Overview
--------

``SymbolGraph.SubGraph`` provides methods to analyze and navigate the
symbol graph, such as retrieving the symbols, relationships between the
symbols, and their properties. Additionally, it offers methods to
compute the symbol ranks and filter the subgraph based on rank and path.

Related Symbols
---------------

-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.base.symbol.Symbol``
-  ``automata.core.base.scip_pb2.Index``
-  ``automata.core.symbol.symbol_utils.get_rankable_symbols``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks_small_graph``

Example
-------

The following example demonstrates how to create a ``SymbolGraph``
instance and retrieve a rankable symbol subgraph.

.. code:: python

   from automata.core.symbol.graph import SymbolGraph

   index_path = "/path/to/index.protobuf"  # Replace with the path to your own index.protobuf file
   symbol_graph = SymbolGraph(index_path)
   rankable_subgraph = symbol_graph.get_rankable_symbol_subgraph()

Limitations
-----------

The performance and accuracy of the ``SymbolGraph.SubGraph`` depend on
the quality of the index protobuf file provided as input. If the index
file is outdated or inaccurate, the resulting subgraph and subsequent
analysis may be affected.

Follow-up Questions:
--------------------

-  How efficient is the current algorithm for computing the symbol ranks
   in a subgraph, and can it be improved?
-  Are there any other use-cases where the subgraph analysis can be
   applied, other than finding the relationships between symbols?
