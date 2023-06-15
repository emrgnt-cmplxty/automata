SymbolSearch
============

``SymbolSearch`` is a class that provides functionality to search for
symbols in a ``SymbolGraph``. It supports different types of search
queries, such as searching for exact matches, finding references to a
symbol, retrieving the source code of a symbol, and ranking symbols
based on their similarity to a query.

Overview
--------

``SymbolSearch`` interacts with a ``SymbolGraph`` to search for symbols
and access their metadata. It uses a ``SymbolSimilarity`` object to
measure the similarity between the query and symbols in the graph. The
class also provides a method to filter the graph to only include nodes
that are part of the given available symbols.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.search.rank.SymbolRank``

Example
-------

This example demonstrates how to create an instance of ``SymbolSearch``
and perform several types of search queries.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   from automata_docs.core.symbol.search.symbol_search import SymbolSearch
   from automata_docs.core.symbol.search.rank import SymbolRankConfig

   symbol_graph = SymbolGraph()
   symbol_similarity = SymbolSimilarity()

   symbol_searcher = SymbolSearch(
       symbol_graph=symbol_graph,
       symbol_similarity=symbol_similarity,
       symbol_rank_config=SymbolRankConfig(),
   )

   # Exact search
   exact_search_result = symbol_searcher.exact_search("pattern")

   # Symbol references search
   symbol_references_result = symbol_searcher.symbol_references("example_symbol_uri")

   # Symbol rank search
   symbol_rank_result = symbol_searcher.symbol_rank_search("query")

   # Retrieve source code by symbol
   source_code_result = symbol_searcher.retrieve_source_code_by_symbol("symbol_uri")

Limitations
-----------

``SymbolSearch`` assumes that the input ``SymbolGraph`` and
``SymbolSimilarity`` objects are correctly initialized and it does not
perform any validation on them. It also depends on the availability of
symbols in the graph and the embedding used (e.g. in
``SymbolSimilarity``). The performance of the search may be affected by
the level of detail provided in the ``SymbolGraph`` and the quality of
the embeddings used for similarity measurements.

Follow-up Questions:
--------------------

-  How can we improve the performance of the search by optimizing the
   processing of available symbols and their embeddings?
-  Is there any way to include additional search algorithms or ranking
   methods in the ``SymbolSearch`` class?
