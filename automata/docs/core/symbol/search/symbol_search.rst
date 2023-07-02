SymbolSearch
============

``SymbolSearch`` is a class that searches for symbols in a
``SymbolGraph``. It provides various search methods such as
``exact_search``, ``symbol_rank_search``, and ``symbol_references``. The
search results include paths to files containing the pattern and
corresponding line numbers.

Overview
--------

``SymbolSearch`` is initialized with a ``SymbolGraph``,
``SymbolSimilarity`` object with a code embedding handler, and optional
``SymbolRankConfig`` object. The class provides methods for searching
for symbols with different types of queries such as exact search or
ranked search based on the query and returns a list of matching symbols.

Related Symbols
---------------

-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol_embedding.similarity.SymbolSimilarity``
-  ``automata.core.experimental.search.rank.SymbolRank``
-  ``automata.core.experimental.search.rank.SymbolRankConfig``
-  ``automata.core.symbol.base.Symbol``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSearch`` and perform an exact search:

.. code:: python

   from automata.core.symbol.graph import SymbolGraph
   from automata.core.symbol_embedding.similarity import SymbolSimilarity
   from automata.core.experimental.search.symbol_search import SymbolSearch, ExactSearchResult
   from automata.core.experimental.search.rank import SymbolRankConfig

   # Create instances of SymbolGraph and SymbolSimilarity
   symbol_graph = SymbolGraph(...)
   symbol_similarity = SymbolSimilarity(...)

   # Initialize SymbolSearch with the required parameters
   symbol_search = SymbolSearch(symbol_graph, symbol_similarity, SymbolRankConfig())

   # Perform an exact search with a pattern
   result = symbol_search.exact_search("pattern")
   assert isinstance(result, ExactSearchResult)

Limitations
-----------

``SymbolSearch`` has some limitations:

1. It assumes that the code graph has been filtered to only contain
   nodes that are in the available symbols set before creating a
   ``SymbolSearch`` object.
2. The ``symbol_graph`` and ``code_subgraph`` objects must be set up
   correctly and have the correct relationship with each other for the
   search to work effectively.
3. The class relies on a fixed set of search types for query processing.
   Custom search types can not be easily added without modifying the
   code.

Follow-up Questions:
--------------------

-  How can we easily implement custom search types in the
   ``SymbolSearch`` class?
-  How can we remove the reliance on ``SymbolRank`` by accepting a
   completed instance?
