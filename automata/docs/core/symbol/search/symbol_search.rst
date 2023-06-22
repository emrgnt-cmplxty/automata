SymbolSearch
============

``SymbolSearch`` is a class that searches for symbols in a SymbolGraph.
It provides methods for exact search, symbol rank search, source code
retrieval by symbol, and processing NLP-formatted queries. The class
contains several static methods for filtering graphs, finding pattern
matches in modules, shifted z-score calculations, and transforming
dictionary values.

``SymbolSearch`` uses other classes such as ``SymbolGraph``,
``SymbolSimilarity``, ``SymbolRankConfig``, and ``SymbolRank`` for the
purpose of searching and ranking symbols based on the provided search
query.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_search_tool.test_exact_search``
-  ``automata.tests.unit.test_symbol_search.test_exact_search``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.core.agent.tools.symbol_search.SearchTool``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.core.agent.tools.symbol_search.SymbolSearchTool``
-  ``automata.core.agent.tools.tool_utils.DependencyFactory.create_symbol_search``
-  ``automata.tests.unit.test_symbol_search_tool.symbol_search_tool_builder``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSearch`` and then perform an exact search:

.. code:: python

   from automata.core.symbol.graph import SymbolGraph
   from automata.core.symbol.search.symbol_search import SymbolSearch
   from automata.core.embedding.symbol_similarity import SymbolSimilarity
   from automata.core.symbol.search.rank import SymbolRankConfig
   from automata.core.symbol.graph import SymbolGraph

   symbol_graph = SymbolGraph()
   symbol_code_similarity = SymbolSimilarity()
   symbol_rank_config = SymbolRankConfig()
   code_subgraph = SymbolGraph.SubGraph()

   symbol_search = SymbolSearch(symbol_graph=symbol_graph,
                               symbol_code_similarity=symbol_code_similarity,
                               symbol_rank_config=symbol_rank_config,
                               code_subgraph=code_subgraph)

   result = symbol_search.exact_search("some_pattern")

Limitations
-----------

The primary limitation of ``SymbolSearch`` lies in the fact that it
relies on other classes like ``SymbolGraph`` and ``SymbolSimilarity`` to
function properly. If these classes change, it’s likely that the
behavior of ``SymbolSearch`` would also be affected.

The current implementation also assumes a specific directory structure
for storing symbol graphs and corresponding data. Any changes to this
structure would require updates to the ``SymbolSearch`` class as well.

When creating a subgraph using ``SymbolGraph.SubGraph()``, one must
ensure that this subgraph is part of the parent ``SymbolGraph`` object.
Failure to do so would result in a ValueError.

Follow-up Questions:
--------------------

-  Are there any alternatives to the current implementation of symbol
   search based on the ``SymbolGraph`` and ``SymbolSimilarity`` classes?
-  How can custom directory structures be accommodated in the
   ``SymbolSearch`` class?
