ToolEvaluationMetrics
=====================

``ToolEvaluationMetrics`` is a class developed to evaluate, quantify,
and provide detailed metrics accumulated from a sequence of Tool
Evaluation Results. It offers a comprehensive overview of evaluation
results from tool testing, gathered in one handy reference data object.

Overview
--------

``ToolEvaluationMetrics`` class is initialized using a list of tool
evaluation results. It then provides various metrics such as the total
count of evaluations, total full matches, total partial matches and
their respective rates. The interpretive metrics available aid in
understanding, to a fine degree, the performance and effectiveness of
the tools being evaluated.

Related Symbols
---------------

-  ``automata.cli.scripts.run_agent.process_issues``
-  ``automata.cli.scripts.run_agent_config_validation.test_yaml_validation``
-  ``automata.singletons.dependency_factory.DependencyFactory.build_dependencies_for_tools``
-  ``automata.cli.install_indexing.generate_local_indices``

Example
-------

Following is a simple example demonstrating the usage of
``ToolEvaluationMetrics``.

.. code:: python

   from automata.eval.tool.tool_eval_metrics import ToolEvaluationMetrics
   from yourmodule import YourToolEvalResults  # Replace with actual module and class

   evaluation_results = [YourToolEvalResults()]  # List of evaluation results

   metrics = ToolEvaluationMetrics(evaluation_results)

   print(f'Total Evaluations Conducted: {metrics.total_evaluations}')
   print(f'Total Full Matches Observed: {metrics.total_full_matches}')
   print(f'Total Partial Matches Observed: {metrics.total_partial_matches}')
   print(f'Full Match Rate: {metrics.full_match_rate}')
   print(f'Partial Match Rate: {metrics.partial_match_rate}')

*Note: Replace ``YourToolEvalResults`` with the actual class that
contains results of tool evaluations.*

Limitations
-----------

``ToolEvaluationMetrics`` is dependent on the result objects that have
to contain ``is_full_match`` and ``is_partial_match`` properties to
compute the full and partial matches. If a tool’s evaluation results do
not include these properties, the ToolEvaluationMetrics cannot compute
these metrics.

The above example assumes that you’ve replaced ``YourToolEvalResults``
with the proper class of your tool evaluation results.

Follow-up Questions:
--------------------

-  Is there a way to handle the computation of metrics even when the
   ``is_full_match`` and ``is_partial_match`` are not present within the
   tool’s evaluation results?
-  How are ``is_full_match`` and ``is_partial_match`` being decided
   within the tool’s evaluation results?
