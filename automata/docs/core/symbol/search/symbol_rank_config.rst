SymbolRankConfig
================

``SymbolRankConfig`` is a configuration class for SymbolRank and is used
to set up the parameters used in the SymbolRank algorithm. The class
contains attributes like ``alpha``, ``max_iterations``, ``tolerance``,
and ``weight_key``, which are the parameters for the ranking process.
The configuration options can be set during the instantiation of the
class, and it provides static method ``validate_config`` used to
validate the given parameters of the ``SymbolRankConfig`` instance.

Overview
--------

``SymbolRankConfig`` provides an easy way to customize the SymbolRank
algorithm’s parameters. The class allows users to set the desired values
for critical aspects of the algorithm, such as the damping factor
(alpha), the maximum number of iterations, and the tolerance for
convergence. The class also provides a method to validate the given
configuration to ensure the provided parameters are within the
acceptable range.

Related Symbols
---------------

-  ``automata.core.experimental.search.rank.SymbolRank``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks``
-  ``automata.tests.unit.test_symbol_rank.test_get_ranks_small_graph``
-  ``automata.core.singletons.dependency_factory.create_symbol_search``

Example
-------

The following is an example demonstrating how to create an instance of
``SymbolRankConfig`` and validate the configuration:

.. code:: python

   from automata.core.experimental.search.rank import SymbolRankConfig

   config = SymbolRankConfig(alpha=0.25, max_iterations=100, tolerance=1.0e-6)
   SymbolRankConfig.validate_config(config)

Limitations
-----------

The primary limitation of ``SymbolRankConfig`` is that it only validates
the limited range for alpha and tolerance. It does not provide advanced
options to customize other aspects of the SymbolRank algorithm, and
users may require additional mechanisms to customize the configuration
further.

Follow-up Questions:
--------------------

-  Are there plans to add more options for configuring the SymbolRank
   algorithm within the ``SymbolRankConfig`` class?
