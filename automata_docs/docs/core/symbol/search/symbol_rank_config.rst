SymbolRankConfig
================

``SymbolRankConfig`` is a configuration class for ``SymbolRank``. It
contains several parameters that can be used to configure the algorithm,
including ``alpha``, ``max_iterations``, ``tolerance``, and
``weight_key``. This class also provides a ``validate`` method that
checks if the given configuration is valid.

Related Symbols
---------------

-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.tests.unit.test_symbol_rank.test_get_ranks``
-  ``automata_docs.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata_docs.core.symbol.search.rank.SymbolRank``
-  ``automata_docs.tests.unit.test_symbol_rank.test_prepare_initial_ranks``
-  ``automata_docs.tests.unit.test_symbol_rank.test_pagerank_config_validation``
-  ``automata_docs.tests.unit.conftest.symbol_searcher``
-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.embedding.embedding_types.NormType``
-  ``automata_docs.core.symbol.search.symbol_search.SymbolSearch``

Example
-------

The following example demonstrates how to create an instance of
``SymbolRankConfig`` and validate the configuration:

.. code:: python

   from automata_docs.core.symbol.search.rank import SymbolRankConfig

   # Create a SymbolRankConfig instance with custom parameters
   config = SymbolRankConfig(alpha=0.5, max_iterations=100, tolerance=1.0e-6, weight_key="weight")

   # Validate the configuration
   config.validate(config)

Limitations
-----------

The primary limitation of ``SymbolRankConfig`` is that it only supports
specific value ranges for ``alpha`` and ``tolerance``. For instance,
``alpha`` must be in the range (0, 1), and ``tolerance`` must be in the
range (1e-4, 1e-8). If a value outside of these ranges is provided, a
``ValueError`` will be raised.

Follow-up Questions:
--------------------

-  Are there any other configuration parameters that could be useful to
   include in the ``SymbolRankConfig`` class?
-  Are there plans to support additional validation checks for other
   configuration parameters, such as ``max_iterations`` and
   ``weight_key``?
