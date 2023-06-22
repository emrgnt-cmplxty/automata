SymbolRankConfig
================

``SymbolRankConfig`` is a configuration class for the ``SymbolRank``
algorithm. It contains various attributes such as ``alpha``,
``max_iterations``, ``tolerance``, and ``weight_key`` that help
configure the algorithm. It also provides a static method
``validate_config`` to ensure the supplied configuration parameters are
valid.

Overview
--------

``SymbolRankConfig`` is used to configure an instance of the
``SymbolRank`` class, which computes the PageRank algorithm scores for
symbols in a given graph. The configuration options allow easy
customization of the algorithm’s behavior and ensure that the user can
adjust the tolerance and stopping criteria to achieve the desired
results.

Related Symbols
---------------

-  ``automata.tests.unit.test_symbol_rank.test_get_ranks``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata.core.symbol.search.rank.SymbolRank``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_symbol_rank.test_prepare_initial_ranks``
-  ``automata.core.base.tool.ToolkitType``
-  ``automata.tests.unit.test_symbol_rank.test_pagerank_config_validation``
-  ``automata.core.agent.coordinator.AutomataInstance.Config``
-  ``automata.tests.regression.test_symbol_searcher_regression.test_symbol_rank_search_on_symbol``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolRankConfig`` and use it to configure a ``SymbolRank`` instance.

.. code:: python

   import networkx as nx
   from automata.core.symbol.search.rank import SymbolRankConfig, SymbolRank

   # Configuration parameters
   alpha = 0.25
   max_iterations = 100
   tolerance = 1.0e-6
   weight_key = "weight"

   # Create an instance of SymbolRankConfig
   config = SymbolRankConfig(alpha=alpha, max_iterations=max_iterations, tolerance=tolerance, weight_key=weight_key)

   # Create a basic graph
   G = nx.DiGraph()
   G.add_edge(1, 2)
   G.add_edge(2, 3)
   G.add_edge(3, 1)

   # Create an instance of SymbolRank with the configuration
   symbol_rank = SymbolRank(G, config)

   # Get the ranks of the nodes in the graph
   ranks = symbol_rank.get_ranks()

Limitations
-----------

The current implementation of ``SymbolRankConfig`` assumes that the user
provides a valid configuration. However, if an invalid configuration is
detected during the ``validate_config`` call, a ``ValueError`` is
raised. Additionally, the configuration validation is only done when
``validate_config()`` method is called explicitly.

Follow-up Questions:
--------------------

-  Can the validation process be made more foolproof and automatically
   performed during the initialization of ``SymbolRankConfig``?
-  How can the error messages be improved to provide more information on
   the specific validation failure?
