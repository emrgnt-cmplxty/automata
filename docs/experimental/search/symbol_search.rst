SymbolSearch
============

``SymbolSearch`` is a class which exposes various search methods for
symbols. It is designed to provide seamless and robust functionality for
searching symbols within an indexed codebase. This class uses
``SymbolGraph``, ``SymbolRankConfig``, ``SymbolEmbeddingHandler``, and
``EmbeddingSimilarityCalculator`` to perform its operations.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_search.test_exact_search``
-  ``automata.tools.builders.symbol_search.SymbolSearchToolkitBuilder``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.tools.builders.symbol_search.SearchTool``
-  ``automata.tests.unit.test_symbol_search_tool.test_retrieve_source_code_by_symbol``
-  ``automata.symbol.base.Symbol``
-  ``automata.tests.unit.test_symbol_search_tool.test_init``
-  ``automata.tools.builders.symbol_search.SymbolSearchToolkitBuilder._exact_search_processor``
-  ``automata.tests.unit.test_symbol_search.test_retrieve_source_code_by_symbol``

Methods
-------

exact_search
~~~~~~~~~~~~

Searches for exact matches across the indexed codebase.

.. code:: python

   def exact_search(self, pattern: str) -> ExactSearchResult:
       """Performs a exact search across the indexed codebase."""
       return self._find_pattern_in_modules(pattern)

For example, to search for an exact pattern ‘pattern1’:

.. code:: python

   result = symbol_search.exact_search("pattern1")

A test for the ``exact_search`` functionality can be seen in
``automata.tests.unit.test_symbol_search.test_exact_search``.

process_query
~~~~~~~~~~~~~

Processes an NLP-formatted query and returns the results of the
appropriate downstream search.

.. code:: python

   def process_query(
           self, query: str
       ) -> Union[SymbolReferencesResult, SymbolRankResult, SourceCodeResult, ExactSearchResult,]:

       """
       Processes an NLP-formatted query and returns the results of the appropriate downstream search.
       Raises:
           ValueError: If the query is not formatted correctly
       """
       ...

retrieve_source_code_by_symbol
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Finds the raw text of a module, class, method, or standalone function.

.. code:: python

   def retrieve_source_code_by_symbol(self, symbol_uri: str) -> SourceCodeResult:
       """Finds the raw text of a module, class, method, or standalone function."""
       ...

shifted_z_score_powered
~~~~~~~~~~~~~~~~~~~~~~~

Calculates the z-score, shifts them to be positive, and then raises the
values to the specified power.

.. code:: python

   @staticmethod
   def shifted_z_score_powered(
       values: Union[List[float], np.ndarray], power: int = 4
   ) -> np.ndarray:
       """
       Calculates the z-score, shifts them to be positive,
       and then raises the values to the specified power.
       """
       ...

symbol_rank_search
~~~~~~~~~~~~~~~~~~

Fetches the list of the SymbolRank similar symbols ordered by rank.

.. code:: python

   def symbol_rank_search(self, query: str) -> SymbolRankResult:
       """Fetches the list of the SymbolRank similar symbols ordered by rank."""
       ...

symbol_references
~~~~~~~~~~~~~~~~~

Finds all references to a module, class, method, or standalone function.

.. code:: python

   def symbol_references(self, symbol_uri: str) -> SymbolReferencesResult:
       """
       Finds all references to a module, class, method, or standalone function.
       """
       ...

Example
-------

The functionality of the SymbolSearch class can be approached as
follows:

.. code:: python

   from automata.experimental.search.symbol_search import SymbolSearch
   from automata.symbol.graph import SymbolGraph
   from automata.experimental.search.rank import SymbolRankConfig
   from automata.symbol_embedding.base import SymbolEmbeddingHandler
   from automata.embedding.base import EmbeddingSimilarityCalculator

   symbol_graph = SymbolGraph()
   symbol_rank_config = SymbolRankConfig()
   search_embedding_handler = SymbolEmbeddingHandler()
   embedding_similarity_calculator = EmbeddingSimilarityCalculator()

   symbol_search = SymbolSearch(
       symbol_graph, 
       symbol_rank_config, 
       search_embedding_handler, 
       embedding_similarity_calculator
   )

   # perform exact search
   result = symbol_search.exact_search("pattern1")

   # process a query 
   result = symbol_search.process_query("query1")

Follow-up Questions:
--------------------

-  How does ``_find_pattern_in_modules()`` work and what does it return?
-  What is the appropriate format for the query in the ``process_query``
   method?
-  What are the possible query formats other than ‘symbol_references’,
   ‘symbol_rank’, ‘exact’, and ‘source’ in the ``process_query`` method?
-  How is symbol rank determined in ``symbol_rank_search`` method?
-  Are references parsed in ``symbol_references`` method or do they need
   to be parsed prior to use?
-  The ``_find_pattern_in_modules()`` is mentioned in the exact search
   implementation but there is no information about this method. Could
   you provide more documentation or context for this function?
-  What does the ``retrieve_source_code_by_symbol`` return when the
   symbol does not exist?
-  How can we use the ``shifted_z_score_powered`` and
   ``transform_dict_values`` function? What can be the possible
   use-cases for these functions?
-  The functionality of the property ``symbol_rank`` is not clear, and
   it appears to instantiate SymbolRank. Could you provide more clarity
   on what it does and how it ties in with the rest of the functions in
   the class?
