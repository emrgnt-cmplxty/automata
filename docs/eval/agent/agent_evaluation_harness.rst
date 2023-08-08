AgentEvaluationHarness
======================

Overview
--------

``AgentEvaluationHarness`` is a class that provides functionalities for
performing evaluation of a list of instructions against a set of
expected actions. It does so by comparing the commenced actions of an
agent to an expected result set. The core function ``evaluate`` takes
tasks, their expected actions, and an executor and provides an
aggregation of AgentEvaluationMetrics as output.

The class is initialized with a list of ``AgentEval`` objects and a
``AgentEvalResultDatabase`` object, which is used for writing the
results into a data store. The evaluation is done for each task and its
corresponding set of instructions by processing the task through an
evaluator. The results are then aggregated (if specified) and written to
the database.

Related Symbols
---------------

-  ``automata.eval.agent.agent_eval.AgentEval``
-  ``automata.eval.agent.agent_eval_result_database.AgentEvalResultDatabase``
-  ``automata.eval.agent.agent_evaluation_metrics.AgentEvaluationMetrics``
-  ``automata.tasks.task_executor.IAutomataTaskExecution.execute``

Usage Example
-------------

.. code:: python

   from automata.eval.agent.agent_eval_harness import AgentEvaluationHarness
   from automata.eval.agent.agent_eval import SomeCustomAgentEval
   from automata.eval.agent.agent_eval_result_database import SomeCustomAgentEvalResultDatabase
   from automata.tasks.task_executor import SomeCustomAutomataTaskExecutor
   from dataclasses import dataclass
   from typing import List

   @dataclass
   class AutomataTask:
       # Custom task definition
       task_detail: str  # Simplified for example 

   @dataclass
   class Action:
       # Custom action definition
       action_detail: str  # Simplified for example 

   evals: List[SomeCustomAgentEval] = [eval1, eval2]
   database = SomeCustomAgentEvalResultDatabase()
   harness = AgentEvaluationHarness(evals, database)

   tasks: List[AutomataTask] = [task1, task2]
   tasks_expected_actions: List[List[Action]] = [[action1, action2], [action3, action4]]
   executor = SomeCustomAutomataTaskExecutor()

   metrics = harness.evaluate(tasks, tasks_expected_actions, executor, aggregate=True)

In this simplified example, custom agent evaluation, agent result
database, automata task executor, task, and action classes are assumed.
These should be replaced with actual implementations according to the
use case.

Limitations
-----------

The ``AgentEvaluationHarness`` assumes that the evaluator defined in the
``AgentEval`` objects returns an ``AgentEvalResult`` type of result. In
case it doesn’t, it will raise a ValueError exception, limiting its
usability with erroneous evaluators.

Due to its dependency on the ``AgentEval`` and
``AgentEvalResultDatabase`` classes, implementing custom evaluation or
database storage methods would require defining new classes that adhere
to these two interfaces. The code encapsulation provided by this class
makes extensive customizations slightly more tedious due to the need to
maintain consistent interfaces.

The execution is stopped if there is an exception occurring during the
evaluation of a task. While it ensures the integrity of the test run, it
also entails that no further tests will be conducted beyond an erring
one.

Follow-up Questions:
--------------------

-  For larger sets of tests, would it be beneficial to implement a
   recovery or skip mechanism for faulty tasks to enable the completion
   of the entire test suite?
-  Could there be opportunities to allow more flexible evaluators that
   do not strictly have to return ``AgentEvalResult`` objects? Could
   this be accommodated with wrapper or adaptor patterns?
-  What amendments would be needed to handle asynchronous task
   executions to potentially increase throughput?
