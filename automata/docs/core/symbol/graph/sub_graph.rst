SymbolGraph.SubGraph
====================

``SymbolGraph.SubGraph`` is a data class responsible for maintaining the
subgraph of a ``SymbolGraph``. It contains a ``parent`` attribute to
track the parent ``SymbolGraph`` instance, and a ``graph`` attribute
representing the actual subgraph with nodes and edges.

Overview
--------

The ``SymbolGraph.SubGraph`` class provides an interface to work with
subgraphs of a ``SymbolGraph``. It can be used, for example, to analyze
a subgraph consisting of only rankable symbols. The class offers a
convenient way to encapsulate subgraphs for further analysis, connecting
it closely to the ``SymbolGraph`` class and related methods.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.graph.SymbolGraph.get_rankable_symbol_subgraph``
-  ``networkx.DiGraph``

Example
-------

The following is an example demonstrating how to obtain and use a
``SymbolGraph.SubGraph`` instance.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph

   # assuming the path to a valid index protobuf file
   index_path = "path/to/index.scip"
   symbol_graph = SymbolGraph(index_path=index_path)

   # Get a SubGraph consisting of only rankable symbols
   subgraph = symbol_graph.get_rankable_symbol_subgraph()

   # Use the SubGraph for further analysis and processing

Limitations
-----------

The main limitation of ``SymbolGraph.SubGraph`` is that it must be
created from a ``SymbolGraph`` instance. This means that in order to use
a ``SymbolGraph.SubGraph``, you must first have a ``SymbolGraph`` from
which you can extract the desired subgraph.

Follow-up Questions:
--------------------

-  How can we create ``SymbolGraph.SubGraph`` instances independent of
   the parent ``SymbolGraph``?
-  Are there any specific use cases where such independent
   ``SymbolGraph.SubGraph`` instances may be useful?
