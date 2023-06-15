SymbolGraph
===========

``SymbolGraph`` is a class that represents a directed graph of symbols
and their relationships. It is designed to provide an efficient way to
access and navigate the relationships between symbols in a given
codebase. The class provides methods to get information about symbols
such as their dependencies, callers, and related symbols.
``SymbolGraph`` comes with a navigator, which handles graph navigation
and symbol lookup.

Overview
--------

``SymbolGraph`` is initialized with the path of an index protobuf file
and optionally whether to build caller-callee relationships. Once
initialized, the graph can be queried for symbols, files, and
relationships between symbols. Furthermore, a rankable subgraph can be
generated based on the symbol graph, which can be useful for ranking
symbols by importance and relevance.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.tests.unit.test_symbol_graph.test_get_all_symbols``
-  ``automata_docs.core.symbol.search.tests.conftest.symbol_graph_mock``
-  ``automata_docs.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata_docs.core.symbol.graph.GraphBuilder``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``
-  ``config.config_enums.ConfigCategory``

Example
-------

The following is an example of how to instantiate a ``SymbolGraph`` and
use its methods to access information about symbols.

.. code:: python

   import os
   from automata_docs.core.symbol.graph import SymbolGraph

   file_dir = os.path.dirname(os.path.abspath(__file__))
   index_path = os.path.join(file_dir, "index.scip")
   symbol_graph = SymbolGraph(index_path)

   # Get all available symbols in the graph
   symbols = symbol_graph.get_all_available_symbols()

   # Get all file nodes in the graph
   files = symbol_graph.get_all_files()

   # Get callers and callees of a specific symbol
   symbol = symbols[0]
   callers = symbol_graph.get_potential_symbol_callers(symbol)
   callees = symbol_graph.get_potential_symbol_callees(symbol)

Limitations
-----------

``SymbolGraph`` assumes that the input index protobuf file is properly
formatted and contains the necessary information to build the graph. If
the protobuf file is improperly formatted or missing data, the resulting
graph may not accurately represent the codebase and its relationships.

Additionally, some methods like ``get_potential_symbol_callers()`` and
``get_potential_symbol_callees()`` require downstream filtering to
remove non-call statements, which can be a performance concern for large
graphs. There might be more efficient ways to achieve this filtering
that have not been implemented yet.

Follow-up Questions:
--------------------

-  Is there any performance optimization planned for methods that
   require downstream filtering such as
   ``get_potential_symbol_callers()`` and
   ``get_potential_symbol_callees()``?
-  Are there any plans to support custom index protobuf file formats, or
   is it assumed that users are only working with the default format?
