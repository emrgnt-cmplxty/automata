SymbolRank
==========

SymbolRank class applies the PageRank algorithm on a graph to rank
symbols such as methods and classes based on their semantic context and
structural relationships within a software.

Symbols are the classes, methods or other elements in a code corpus. A
SymbolGraph is constructed where each symbol forms a node and
dependencies between symbols form edges. This SymbolGraph maps
structural information from the codebase and helps explore symbol
dependencies, relationships and hierarchy.

Finally, a prepared similarity dictionary between symbols is used in
combination with the SymbolGraph to compute their SymbolRanks. This is
performed using an iterative computation analogous to Google’s PageRank
algorithm, considering symbols’ similarity scores and their connectivity
within the graph.

For this a SymbolRankConfig is required which provides the necessary
parameters for the computations.

Methods
-------

``__init__(self, graph: nx.DiGraph, config: SymbolRankConfig) -> None:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Initializes a SymbolRank instance with a given graph and a
SymbolRankConfig. If config is not provided, a default SymbolRankConfig
is initialized.

``get_ranks(self,query_to_symbol_similarity: Optional[Dict[Symbol, float]] = None,initial_weights: Optional[Dict[Symbol, float]] = None,dangling: Optional[Dict[Symbol, float]] = None,) -> List[Tuple[Symbol, float]]:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Calculate the SymbolRanks of each node in the graph.

``get_top_symbols(self, n: int) -> List[Tuple[str, float]]:``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Get the top ‘n’ symbols as per their ranks. Returns a list of tuples,
where each tuple contains the dotpath of a symbol and its rank.

Examples
--------

.. code:: python

   from automata.symbol.base import Symbol
   from automata.experimental.search.rank import SymbolRank, SymbolRankConfig
   import networkx as nx

   # create a graph
   G = nx.DiGraph()
   G.add_edge(1, 2)
   G.add_edge(2, 3)
   G.add_edge(3, 1)

   # initialize SymbolRankConfig and SymbolRank
   config = SymbolRankConfig()
   sr = SymbolRank(G, config)

   # retrieve SymbolRanks
   ranks = sr.get_ranks()

Related Modules
---------------

-  automata.symbol.base.Symbol
-  automata.experimental.search.symbol_search.SymbolSearch
-  automata.tools.builders.symbol_search.SymbolSearchToolkitBuilder

Limitations
-----------

-  The SymbolRank class assumes that every node in the graph is a symbol
   from an application’s corpus. Therefore, the graph should be prepared
   accordingly.
-  SymbolRank uses an algorithm similar to the PageRank algorithm which
   is iterative in nature. Hence, it may take significant time for large
   graphs.
-  As the ranks depend on both the graph structure and symbol
   similarity, inaccurate results can be returned when the graph is not
   properly constructed or appropriate symbol similarity is not used.

Follow-up Questions:
--------------------

-  What is default value of ``SymbolRankConfig`` if not provided while
   initializing ``SymbolRank``?
-  Are there any specific assumptions or requirements for the format or
   structure of ``Query_symbol_similarity`` , ``initial_weights`` ,
   ``dangling``?
-  What is the depth up to which symbol dependencies are considered
   while constructing the SymbolGraph?
-  How are the weights of the edges in the SymbolGraph determined?
-  How is the similarity between symbols computed?
-  What happens if the ``get_ranks`` method does not converge in
   ``max_iterations``? What approaches can be used to mitigate this?
