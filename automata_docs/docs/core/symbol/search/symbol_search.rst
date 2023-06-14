SymbolSearch
============

``SymbolSearch`` is a class that searches for symbols in a
``SymbolGraph``. It provides several search methods, including exact
search, symbol rank search, and symbol references search. By leveraging
different search methods, it allows users to search for specific
patterns, retrieve source code by symbol, or even process queries in an
NLP-based fashion.

Overview
--------

``SymbolSearch`` takes a ``SymbolGraph``, a ``SymbolSimilarity``, and a
``SymbolRankConfig`` object as input, and optionally a
``SymbolGraph.SubGraph`` object. It first filters the input graph to
only contain nodes that are available_symbols and are supported by the
``SymbolSimilarity`` object’s embedding handler. After that, it provides
different search methods to process queries and search for symbols in
various ways.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.search.symbol_search.ExactSearchResult``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolRankResult``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolReferencesResult``
-  ``automata_docs.core.symbol.search.symbol_search.SourceCodeResult``

Example
-------

The following example demonstrates how to create an instance of
``SymbolSearch`` and process a query to perform a symbol rank search.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.symbol.symbol_similarity import SymbolSimilarity
   from automata_docs.core.symbol.search.symbol_search import SymbolSearch
   from config.symbol_rank_config import SymbolRankConfig

   symbol_graph = SymbolGraph(index_path="your_index_path")
   symbol_similarity = SymbolSimilarity(embedding_handler="your_embedding_handler")
   symbol_rank_config = SymbolRankConfig()

   symbol_searcher = SymbolSearch(symbol_graph, symbol_similarity, symbol_rank_config)

   query = "type:symbol_rank example_symbol_uri"
   result = symbol_searcher.process_query(query)

Limitations
-----------

``SymbolSearch`` has some limitations. Specifically, it currently only
supports searches based on the input graph and available symbols. It may
not cover every possible search scenario desired by the users.
Additionally, the search methods rely on pre-trained models, which may
not provide perfect results for very specific or niche search scenarios.

Follow-up Questions:
--------------------

-  Is there a possibility to extend the search capabilities of
   ``SymbolSearch`` to cover more scenarios or support custom search
   methods?
