SymbolSearchToolkitBuilder
==========================

Overview
--------

The ``SymbolSearchToolkitBuilder`` is a class responsible for the
interaction with the SymbolSearch API. Its main focus is to search an
indexed Python codebase.

The class leverages SymbolSearch in different capacities, such as
agent-facilitated search, symbol similarity search, symbol rank search,
retrieving source code by symbol, locating symbol references, and
executing exact searches.

Each type of search operation is encapsulated in its own method and
these are used during the building phase of the toolkit. Upon
construction, the toolkit is populated with a set of pre-defined tools.
The builder also provides a method (``process_query``) to process a
given query by routing it to the appropriate tool.

Related Symbols
---------------

-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._symbol_references_processor``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._symbol_rank_search_processor``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._symbol_code_similarity_search_processor``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._symbol_agent_search_processor``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._exact_search_processor``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder.__init__``
-  ``automata.experimental.tools.builders.symbol_search_builder.SymbolSearchToolkitBuilder._retrieve_source_code_by_symbol_processor``
-  ``automata.experimental.search.symbol_search.SymbolSearch.exact_search``
-  ``automata.experimental.search.symbol_search.SymbolSearch.retrieve_source_code_by_symbol``

Example
-------

.. code:: python

   from automata.experimental.tools.builders.symbol_search_builder import SymbolSearchToolkitBuilder
   from automata.experimental.search.symbol_search import SymbolSearch

   symbol_search = SymbolSearch()
   builder = SymbolSearchToolkitBuilder(symbol_search)

   builder.build()  # builds a suite of tools for searching the associated codebase
   builder.process_query(SearchTool.SYMBOL_SIMILARITY_SEARCH, 'search_query')  # processes a query by routing it to the symbol similarity search tool

Limitations
-----------

``SymbolSearchToolkitBuilder`` relies on the ``SymbolSearch`` object
supplied during initialization. Therefore, any limitations inherent to
SymbolSearch will carry over. For instance, if the ``SymbolSearch``
object is not correctly initialized or its source data is not properly
indexed, the search functionality provided by the
``SymbolSearchToolkitBuilder`` may fail or under-perform.

Particularly, for methods involving text processing such as
``_symbol_agent_search_processor``, the end results highly rely on the
model used for AI-based suggestions (currently using GPT-4). The quality
and relevance of the results will depend on the capabilities and tuning
parameters of this model.

Follow-up Questions:
--------------------

-  What should happen if an unknown ``tool_type`` is supplied to the
   ``process_query`` function?
-  Is there a need for an update or refresh method to occur if the
   underlying source data of the ``SymbolSearch`` object changes after
   the ``SymbolSearchToolkitBuilder`` has been initialized?
