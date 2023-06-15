SymbolGraph.SubGraph
====================

``SymbolGraph.SubGraph`` is a dataclass representing a subgraph of a
larger ``SymbolGraph``. It helps in constructing and analyzing
sub-graphs and extracting useful information from the relationships
between the symbols in the graph. The subgraph can be used to perform
various tasks such as retrieving the relationships between symbols,
finding potential callees and callers, exploring the source code
references, and ranking symbols based on their significance in the
graph.

Overview
--------

The ``SymbolGraph.SubGraph`` contains a NetworkX MultiDiGraph and a
reference to its parent ``SymbolGraph``, from which it was derived. The
subgraph can be created by methods such as
``symbol_graph.get_rankable_symbol_subgraph()``. The subgraph provides
information about its nodes and edges, which represent symbols and their
relationships, respectively.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_utils.get_rankable_symbols``
-  ``automata_docs.core.symbol.graph.GraphBuilder``

Example
-------

The following example demonstrates how to create and work with a
``SymbolGraph.SubGraph``:

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph

   # Initialize a SymbolGraph with a path to an index protobuf file.
   symbol_graph = SymbolGraph(index_path="your_index_path.scip")

   # Get a rankable symbol subgraph for analysis.
   subgraph = symbol_graph.get_rankable_symbol_subgraph()

   # Access nodes and edges in the subgraph.
   nodes = subgraph.graph.nodes()
   edges = subgraph.graph.edges()

   # In case you need the parent graph
   parent_graph = subgraph.parent

Limitations
-----------

The primary limitation of ``SymbolGraph.SubGraph`` is that it relies on
the ``SymbolGraph`` to provide it with data, thus requiring the index
protobuf file. Creating custom subgraphs based on specific filtering
criteria or requirements might need additional logic built around the
``SymbolGraph`` to manipulate and generate the desired ``SubGraph``.

Follow-up Questions:
--------------------

-  Are there any methods to merge related subgraphs into a single
   subgraph?
-  Can ``SymbolGraph.SubGraph`` support custom filtering or other
   manipulations based on user requirements?
