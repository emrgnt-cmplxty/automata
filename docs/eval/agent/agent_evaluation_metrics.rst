AgentEvaluationMetrics
======================

``AgentEvaluationMetrics`` is a class designed to compute and store
various metrics derived from a list of ``AgentEvalResult`` objects.
These results are the output of evaluating the performance of an agent.
The metrics calculated include the total number of actions, successful
actions, full matches, partial matches, extra actions, as well as the
frequency of extra, successful, and failed actions. Moreover, this class
provides a method for calculating success rates for action, full match,
and partial match.

Overview
--------

``AgentEvaluationMetrics`` provides a way to assess and quantify the
agent’s performance during its operation. The measures include plain
counts (e.g., total number of actions, successful actions) and more
complex metrics (e.g., success rates for different types of matches and
actions). Properties and methods of ``AgentEvaluationMetrics`` lazily
compute these values when accessed and then cache it for future access.

Related Symbols
---------------

-  ``automata.eval.agent.agent_eval_result.AgentEvalResult``
-  ``python.collections.Counter``

Example
-------

The following shows an example of how to use ``AgentEvaluationMetrics``
to compute metrics from a list of ``AgentEvalResult`` instances.

.. code:: python

   from automata.eval.agent.agent_eval_metrics import AgentEvaluationMetrics
   from automata.eval.agent.agent_eval_result import AgentEvalResult
   # Assume we have a list of AgentEvalResult instances as results
   metrics = AgentEvaluationMetrics(results)

   # We can now access various metrics
   print(f"Total actions: {metrics.total_actions}")
   print(f"Total successful actions: {metrics.total_successful_actions}")
   print(f"Total full matches: {metrics.total_full_matches}")
   print(f"Total partial matches: {metrics.total_partial_matches}")
   print(f"Action success rate: {metrics.action_success_rate}")
   # etc.

Limitations
-----------

``AgentEvaluationMetrics`` does not detect changes in the underlying
``AgentEvalResult`` list, i.e., once a metric is accessed and computed,
adding more ``AgentEvalResults`` to the list won’t change the computed
metrics. In addition, this class assumes that the results passed during
the instance creation are comprehensive and final. If the evaluation
results are updated or change dynamically, a new instance of
``AgentEvaluationMetrics`` needs to be created.

Follow-up Questions:
--------------------

-  Is there a way to make ``AgentEvaluationMetrics`` more dynamic, i.e.,
   enabling it to handle updates or changes in the ``AgentEvalResult``
   list?
-  How can we make the information retrieval (property access) less
   verbose, considering the many metrics it can provide?
