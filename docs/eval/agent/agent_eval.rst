AgentEval
=========

Overview
--------

``AgentEval`` is an abstract class designed for evaluating the
performance of Language Learning Models (LLMs) in the Automata library.
It operates by generating evaluation results for a specified set of
instructions and expected actions. “Evaluation” here includes processing
the results of a session, and comparing these results against an
expected sequence of actions to evaluate how closely the model’s actions
followed the expected sequence. Inheritances of this class should
implement the ``generate_eval_result`` and ``process_result`` methods.

Interface Methods
-----------------

generate_eval_result(self, exec_input: AutomataTask, expected_output: List[Action], executor: AutomataTaskExecutor, \*args, \**kwargs) -> EvalResult
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method is used to generate an evaluation result for a given set of
instructions (``exec_input``) and expected actions
(``expected_output``). The ``executor`` parameter is an instance of
``AutomataTaskExecutor`` that is used to execute the task.

process_result(self, expected_actions: List[Action], process_input: Sequence[LLMChatMessage], \*args, \**kwargs) -> EvalResult
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This method processes the result of an evaluation. It takes in an
expected list of actions and a sequence of ``LLMChatMessage`` instances
to process the evaluation.

Related Symbols
---------------

-  ``automata.eval.agent.agent_eval.AgentEvalResult``: A specialized
   ``EvalResult`` created and returned by the execution of
   ``AgentEval``. It provides granular results of an evaluation
   including match results, extra actions, session id, and other
   attributes.

-  ``automata.eval.agent.agent_eval_composite.AgentEvalComposite``:
   Combines multiple ``AgentEval`` evaluators into a composite evaluator
   to allow evaluation with multiple criteria.

-  ``automata.eval.eval_base.EvalResult``: An abstract class that
   represents the result of an evaluation. ``AgentEvalResult`` is a
   concrete implementation of this class.

-  ``automata.eval.agent.agent_eval_harness.AgentEvaluationHarness.evaluate``:
   Returns the evaluation metrics for a list of tasks given their
   expected actions.

-  ``automata.core.run_handlers.run_with_eval``: A function to perform a
   task run with the provided parameters and evaluates the results.

Usage Example
-------------

.. code:: python

   from automata.eval.agent.agent_eval import AgentEval
   from automata.eval.agent.agent_eval_result import AgentEvalResult
   from automata.tasks.task_executor import AutomataTaskExecutor
   from typing import List
   from automata.common.types import Action, AutomataTask

   class MyAgentEval(AgentEval):

       def generate_eval_result(self, exec_input: AutomataTask, expected_output: List[Action], executor: AutomataTaskExecutor) -> AgentEvalResult:
           # you need to implement this method based on how you want to evaluate.
           pass

       def process_result(self, expected_actions: List[Action], process_input: Sequence[LLMChatMessage]) -> EvalResult:
           # you need to implement this method based on how you want to process the evaluation.
           pass

   # Create an instance of MyAgentEval
   my_agent_eval = MyAgentEval()

Limitations
-----------

The primary limitations associated with ``AgentEval`` are the need for
each inheritor to implement its own versions of ``generate_eval_result``
and ``process_result`` methods. This requires a clear understanding of
the specific evaluation process required for each unique learning model.
This evaluation process must also be implementable in a manner
compatible with ``AgentEval``\ ’s methods.

Follow-up Questions:
--------------------

-  How can we generalize ``AgentEval`` evaluation methods to be
   applicable to a wider range of learning models?
-  Can we simplify ``AgentEval`` interfaces while maintaining their
   function for evaluations?
