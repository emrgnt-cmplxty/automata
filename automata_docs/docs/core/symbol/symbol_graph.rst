SymbolGraph
===========

``SymbolGraph`` is a class that represents a graph of symbols and their
relationships. It provides methods for querying and analyzing symbols,
including retrieving all available symbols, finding potential callers
and callees, and creating a subgraph of rankable symbols. The class also
works with related classes such as ``Symbol``, ``SubGraph``,
``GraphBuilder``, and ``SymbolSearch``.

Overview
--------

``SymbolGraph`` facilitates the analysis of symbols and their
relationships by constructing a graph from an index protobuf file. It
enables the retrieval of symbols, file nodes, potential callers and
callees, and references to a given symbol. Additionally, it provides
functionality for generating subgraphs that contain rankable symbols.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph.SubGraph``
-  ``automata_docs.core.symbol.graph.GraphBuilder``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

The following example demonstrates how to create an instance of
``SymbolGraph`` using a predefined protobuf index file.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph

   index_path = "/path/to/index.protobuf"
   symbol_graph = SymbolGraph(index_path)

Limitations
-----------

The primary limitation of ``SymbolGraph`` lies in its reliance on index
protobuf files. It is not able to process other file formats or process
custom index files natively.

Another limitation is that the methods for getting potential callers and
callees require downstream filtering to remove non-call statements.

Follow-up Questions:
--------------------

-  Can ``SymbolGraph`` be extended to handle other file formats or
   custom index files?
-  Is there a way to refine the methods for getting callers and callees
   to remove non-call statements?
