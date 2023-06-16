SymbolSearch
============

``SymbolSearch`` is a class that searches for symbols in a
``SymbolGraph``. It provides methods to process NLP-formatted queries
and searches for exact matches, symbol references, symbol rankings, and
source code retrieval.

Overview
--------

``SymbolSearch`` is initialized with a ``SymbolGraph``, a
``SymbolSimilarity`` object, an optional ``SymbolRankConfig`` object,
and an optional ``SymbolGraph.SubGraph``. The class contains methods
such as ``exact_search``, ``filter_graph``, ``find_pattern_in_modules``,
``process_query``, ``retrieve_source_code_by_symbol``,
``shifted_z_score_sq``, ``symbol_rank_search``, and
``symbol_references`` to perform various search operations.

The class uses a symbol similarity algorithm to rank symbols based on
their relevance to the input query and a SymbolRank algorithm to compute
a global ranking of symbols in the codebase. It provides search results
in different formats depending on the search type specified in the
query.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.parser.parse_symbol``
-  ``automata_docs.core.symbol.symbol_utils.convert_to_fst_object``
-  ``automata_docs.core.embedding.symbol_similarity.SymbolSimilarity``
-  ``automata_docs.core.symbol.search.rank.SymbolRank``

Example
-------

The following example demonstrates how to use ``SymbolSearch`` to
process a query and retrieve the search results.

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.embedding.symbol_similarity import SymbolSimilarity
   from automata_docs.core.symbol.search.symbol_search import SymbolSearch

   # Initialize necessary objects
   symbol_graph = SymbolGraph()
   symbol_similarity = SymbolSimilarity()

   # Create the SymbolSearch object
   symbol_searcher = SymbolSearch(symbol_graph, symbol_similarity)

   # Process a query and get the search results
   query = "type:symbol_references <symbol_uri>"
   result = symbol_searcher.process_query(query)

Limitations
-----------

``SymbolSearch`` relies on the availability of symbols in the
``SymbolGraph`` and the ``SymbolSimilarity`` object. If either of these
objects doesn’t have the necessary data, the search results might be
incomplete or incorrect. Moreover, the class assumes a specific format
for NLP-formatted queries and raises errors if the input query does not
follow the expected format.

Follow-up Questions:
--------------------

-  How can we improve the search performance of the ``SymbolSearch``
   class?
