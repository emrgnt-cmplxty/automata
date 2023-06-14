SymbolGraph.SubGraph
--------------------

``SymbolGraph.SubGraph`` is a representation of a subgraph within the
``SymbolGraph`` class. It is used to store and access relevant parts of
a symbol graph, offering the ability to work with specific portions of
the larger graph while retaining its context.

Related Symbols

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.graph.GraphBuilder``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

The following example demonstrates how to create a ``SymbolGraph``
instance using ``SymbolGraph.Subgraph``.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph

   # assuming the path to a valid index protobuf file, you should replace it with your own file path
   file_dir = os.path.dirname(os.path.abspath(__file__))
   index_path = os.path.join(file_dir, "index.scip")
   graph = SymbolGraph(index_path)

   # Creating a SymbolSearch instance with a custom symbol_rank_config and code_subgraph
   from automata_docs.core.symbol.search.symbol_search import SymbolSearch
   from automata_docs.core.symbol.search.sources.symbol_similarity import SymbolSimilarity
   from automata_docs.core.symbol.rank.SymbolRank import SymbolRankConfig

   symbol_similarity = SymbolSimilarity()
   symbol_rank_config = SymbolRankConfig(lambda_=0.85, tol=1e-06)

   symbol_search = SymbolSearch(
       symbol_graph=graph,
       symbol_similarity=symbol_similarity,
       symbol_rank_config=symbol_rank_config,
       code_subgraph=graph.get_rankable_symbol_subgraph("bidirectional")
   )

Limitations
-----------

``SymbolGraph.SubGraph`` relies on the internal structure of the
``SymbolGraph`` class and is not designed for standalone use. It is
meant to be a convenient way to organize and work with specific parts of
a larger graph. Due to its close dependence on ``SymbolGraph``,
potential changes in the design of the ``SymbolGraph`` class might
affect the functionality of ``SymbolGraph.SubGraph``.

Follow-up Questions:
--------------------

-  Is there a need for additional functionality when using
   ``SymbolGraph.SubGraph``, or can it be left as a barebones class for
   subgraph organization?
-  Is it possible to sanitize the user input on ``SymbolGraph.SubGraph``
   to ensure that only valid subgraphs are created?
