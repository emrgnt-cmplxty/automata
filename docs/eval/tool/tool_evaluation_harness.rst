ToolEvaluationHarness
=====================

Overview
--------

``ToolEvaluationHarness`` is a utility class designed to facilitate the
evaluation of a list of function calls against a set of expected
actions. It leverages various related tools and interfaces to perform
the evaluation, compute metrics, and report the results. The class
generates a unique run ID for each evaluation session and provides an
interface to conduct the evaluation with custom configurations.

Related Symbols
---------------

-  ``automata.tasks.task_executor.AutomataTaskExecutor.__init__``
-  ``automata.tools.tool_executor.ToolExecution.__init__``
-  ``automata.tasks.task_base.TaskEnvironment.setup``
-  ``automata.tasks.task_base.Task.__init__``
-  ``automata.tasks.task_environment.AutomataTaskEnvironment.teardown``
-  ``automata.agent.agent.AgentToolkitBuilder.build``
-  ``automata.experimental.symbol_embedding.symbol_doc_embedding_builder.SymbolDocEmbeddingBuilder._build_prompt``
-  ``automata.symbol.graph.symbol_caller_callees.CallerCalleeProcessor.process``
-  ``automata.cli.env_operations.show_key_value``

Usage Example
-------------

Below is an example showcasing how ``ToolEvaluationHarness`` can be
integrated. This depiction presumes existing lists of
``input_functions`` and ``expected_actions``, in addition to the
``executor`` as an instance of ``ToolExecution``.

.. code:: python

   from automata.eval.tool.tool_eval_harness import ToolEvaluationHarness
   from automata.tools.tool_executor import ToolExecution
   from mock import MagicMock  # using mock objects for illustration

   # Assuming these lists are predefined and filled with functions and actions respectively
   input_functions = [MagicMock(name='function') for _ in range(10)]
   expected_actions = [MagicMock(name='action') for _ in range(10)]
   # Assuming executor is an instance of ToolExecution
   executor = ToolExecution([MagicMock(name='tool')])

   # Initialize a ToolEvaluationHarness instance
   tool_eval_harness = ToolEvaluationHarness([])  # Empty evals list for this example

   # Conduct an evaluation
   metrics = tool_eval_harness.evaluate(input_functions, expected_actions, executor)

   # `metrics` now contains the evaluation results

Limitations
-----------

``ToolEvaluationHarness`` requires thorough understanding for its
effective utilization due to its close association with other symbolic
representations and automation tasks. The exact working and usefulness
of this class becomes clearer when combined with related symbols like
``AutomataTaskExecutor``, ``ToolExecution``, and
``CallerCalleeProcessor``.

While the class shuffles function-action pairs randomly to prevent
ordering bias, this could potentially dilute important order nuances in
certain evaluation scenarios.

Finally, please note that exception thrown during evaluation will halt
the process and needs to be managed appropriately.

Follow-up Questions:
--------------------

1. What’s the level of granularity for ``ToolEvaluationMetrics``? Any
   chance to get evaluation breakdown per function call or action in the
   results?
2. Any alternatives to handle exceptions during function call executions
   to maintain the continuity of the evaluation process?
3. Is there a way to override the default random seed for shuffling
   function-action pairs in evaluation for specific use-cases?
4. What happens if input function list and expected action list don’t
   have the same lengths?
