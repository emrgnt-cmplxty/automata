SymbolRankConfig
================

``SymbolRankConfig`` is a configuration class for ``SymbolRank``. It
provides a way to configure the alpha, maximum iterations, tolerance,
and weight_key parameters in ``SymbolRank``. The class also includes a
validation method to check whether the provided configuration parameters
are valid or not.

Overview
--------

``SymbolRankConfig`` can be used to set up alpha, maximum iterations,
tolerance, and weight_key for ``SymbolRank``. The class validates the
configuration parameters with the validate method, which raises a
ValueError if the alpha is not in (0, 1), or tolerance is not in (1e-4,
1e-8).

Related Symbols
---------------

-  ``automata_docs.core.symbol.search.rank.SymbolRank``
-  ``automata_docs.tests.unit.test_symbol_rank.test_get_ranks``
-  ``automata_docs.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata_docs.tests.unit.test_symbol_rank.test_prepare_initial_ranks``
-  ``automata_docs.tests.unit.test_symbol_rank.test_pagerank_config_validation``

Example
-------

The following example demonstrates how to create a ``SymbolRankConfig``
instance and use it for checking the validity of SymbolRank
configuration parameters.

.. code:: python

   from automata_docs.core.symbol.search.rank import SymbolRankConfig

   config = SymbolRankConfig(alpha=0.25, max_iterations=100, tolerance=1.0e-6, weight_key="weight")
   config.validate(config)

Limitations
-----------

The primary limitation of ``SymbolRankConfig`` is that it only provides
validation for the given configuration parameters and does not support
more complex relationships or additional parameters. It assumes a
specific set of parameters for ``SymbolRank`` and does not allow for
easy modification or customization.

Follow-up Questions:
--------------------

-  How can we extend the ``SymbolRankConfig`` class to support more
   complex relationships between the parameters or additional
   parameters?
