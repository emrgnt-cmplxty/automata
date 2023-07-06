SymbolRankConfig
================

``SymbolRankConfig`` is a configuration class for the SymbolRank object.
It is derived from the BaseModel class and is used to set up
configurations such as alpha, max_iterations, tolerance, and weight_key
for SymbolRank.

Overview
--------

``SymbolRankConfig`` allows for the setup of various parameters:

-  alpha: It affects the damping factor used in the calculation of the
   SymbolRank. Default value is 0.25.
-  max_iterations: Sets the maximum number of iterations for the
   SymbolRank calculation. Default value is 100.
-  tolerance: Specifies the tolerance for error in the SymbolRank
   calculations. The default is 1.0e-6.
-  weight_key: Specifies the key for accessing edge weights. The default
   is “weight”.

An instance of ``SymbolRankConfig`` then validates these values to
ensure that they are within certain bounds. If they fall outside these
bounds, it raises a ValueError.

Related Symbols
---------------

-  ``automata.core.experimental.search.rank.SymbolRank``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata.core.experimental.search.symbol_search.SymbolSearch.symbol_rank``
-  ``automata.tests.unit.test_symbol_rank.test_prepare_initial_ranks``
-  ``automata.core.singletons.dependency_factory.DependencyFactory.create_symbol_rank``
-  ``automata.tests.unit.test_symbol_search_tool.test_symbol_rank_search``
-  ``automata.tests.unit.test_symbol_rank.test_pagerank_config_validation``
-  ``automata.core.singletons.dependency_factory.DependencyFactory.create_symbol_search``
-  ``automata.tests.regression.test_symbol_searcher_regression.test_symbol_rank_search_on_symbol``

Example
-------

Below is a simple example on instantiation and validation of
SymbolRankConfig.

.. code:: python

   from automata.core.experimental.search.rank import SymbolRankConfig
   config = SymbolRankConfig(alpha=0.5, max_iterations=100, tolerance=1.0e-6)
   config.validate_config(config)

Limitations
-----------

``SymbolRankConfig`` is currently constrained to validate only alpha and
tolerance parameters. However, validation for other parameters such as
max_iterations and weight_key can also be crucial depending upon the
nature of graph and its edges.

Follow-up Questions:
--------------------

-  Are there plans to add any further parameters or configurations in
   the ``SymbolRankConfig`` class?
-  Is there any specific reason to keep the default value of weight_key
   as “weight”?
-  What kind of use cases are typically supported by the
   ``SymbolRankConfig`` class?
