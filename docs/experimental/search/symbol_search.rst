SymbolSearch
============

Overview
--------

``SymbolSearch`` is a class that provides various search methods for
symbols. It initiates a search through embeddings and ranks the results
based on the similarity to the query. It can perform such operations as
getting symbol rank results, retrieving source codes based on symbols,
exactly searching across the indexed codebase, etc.

``SymbolSearch`` benefits from object-oriented programming to allow
different configurations to customize the behaviour of the search
process. This class takes care of various search functionalities that
include calculating similarity between embeddings, ranking, and
reference finding among others. It interacts with classes like
``SymbolGraph``, ``SymbolRankConfig``, and ``EmbeddingHandler`` for
exhaustive and effective search operations.

Related Symbols
---------------

-  ``automata.symbol.symbol_base.Symbol.__eq__``
-  ``automata.symbol.symbol_parser._SymbolParser.accept_escaped_identifier``
-  ``automata.symbol.symbol_parser._SymbolParser.peek_next``
-  ``automata.symbol.graph.symbol_navigator.SymbolGraphNavigator.get_symbol_dependencies``
-  ``automata.symbol.graph.symbol_graph.SymbolGraph.get_potential_symbol_callees``
-  ``automata.symbol.symbol_parser._SymbolParser.accept_space_escaped_identifier``
-  ``automata.symbol.symbol_parser._SymbolParser.current``
-  ``automata.symbol.symbol_base.SymbolDescriptor.get_escaped_name``
-  ``automata.symbol.symbol_parser._SymbolParser.accept_character``
-  ``automata.experimental.scripts.run_update_tool_eval.process_missing_symbols``

Example
-------

Here is an example showcasing how to use SymbolSearch class.

.. code:: python

   from automata.experimental.search.symbol_search import SymbolSearch
   from automata.symbol.graph.symbol_graph import SymbolGraph
   from automata.symbol.graph.embedding_handler import EmbeddingHandler
   from automata.symbol.graph.embedding_similarity_calculator import EmbeddingSimilarityCalculator
   from automata.symbol.graph.symbol_rank_config import SymbolRankConfig

   symbol_graph = SymbolGraph()            # Assume SymbolGraph is initialized
   embedding_handler = EmbeddingHandler()  # Assume EmbeddingHandler is initialized
   embedding_similarity_calculator = EmbeddingSimilarityCalculator() # Assume EmbeddingSimilarityCalculator is initialized
   symbol_rank_config = SymbolRankConfig() # Assume SymbolRankConfig is initialized

   symbol_search = SymbolSearch(
                       symbol_graph, 
                       symbol_rank_config, 
                       embedding_handler, 
                       embedding_similarity_calculator)

   query = "Insert your query here"
   # Get the ranked results based on the symbol
   symbol_rank_results = symbol_search.get_symbol_rank_results(query)

   # Get similar symbols based on the query
   symbol_similarity_results = symbol_search.get_symbol_code_similarity_results(query)

   # Get references to a certain symbol
   symbol_references = symbol_search.symbol_references("symbol_uri")

   # Retrieves the raw text of a module, class, method, or standalone function
   source_code = symbol_search.retrieve_source_code_by_symbol("symbol_uri")

   # Performs an exact search across the indexed codebase
   exact_search_result = symbol_search.exact_search("pattern")

Please replace ``"Insert your query here"``, ``"symbol_uri"``, and
``"pattern"`` with your desired values.

Limitations
-----------

The main limitation of ``SymbolSearch`` lies in its dependency on the
correct initialization and functioning of ``SymbolGraph``,
``EmbeddingHandler``, ``EmbeddingSimilarityCalculator``, and
``SymbolRankConfig`` classes. If these classes are not correctly
initialized or have errors, ``SymbolSearch`` may not be able to function
as expected.

In addition, the processing of NLP queries presumes a specific query
format with a ‘type:…’ and ‘query…’. Incorrectly formatted queries lead
to ``ValueError``.

The behaviour of methods like ``symbol_references``,
``retrieve_source_code_by_symbol``, and ``_find_pattern_in_modules``
relies on the quality of ``symbol_uri``, ``node``, and ``pattern`` given
to them. These methods may not behave as expected if the input values
are not as expected.

Follow-up Questions:
--------------------

-  How could we improve the error handling of ``SymbolSearch`` when
   dependencies have errors or are not properly initialized?
-  How can we optimize the ``SymbolSearch`` class when dealing with
   large amounts of data or highly complex symbol relationships?
