AgentEvalComposite
==================

``AgentEvalComposite`` is a utility class that facilitates multiple
evaluations in a composite manner. It is used when you need to perform a
set of evaluations and aggregate their results. This class is essential
when dealing with complex evaluation setups where the final evaluation
result depends on the results of several different evaluators.

Overview
--------

``AgentEvalComposite`` is a subclass of ``Eval``, intended to use
several ``AgentEval`` instances for a multi-faceted evaluation approach.
At initialization, the uniqueness of the evaluators is checked and a
list of agent evaluators is compiled. The class provides functionality
to generate evaluation results, extract actions and filter actions
(although the last function is not implemented). This composite class is
primarily designed to be a flexible manager object that operates with
multiple evaluators to provide a comprehensive evaluation.

Related Symbols
---------------

-  ``automata.eval.agent.agent_eval_composite.check_eval_uniqueness``
-  ``automata.cli.scripts.run_tool_eval.run_eval_harness``
-  ``automata.eval.agent.openai_function_eval.OpenAIFunctionEval.__repr__``
-  ``automata.tools.tool_executor.ToolExecution``
-  ``automata.cli.scripts.run_agent_eval.run_eval_harness``
-  ``automata.cli.scripts.run_agent_eval.main``
-  ``automata.llm.llm_base.LLMChatCompletionProvider``

Example
-------

Below is an example demonstrating how to use the ``AgentEvalComposite``
class. In this example, two dummy evaluators (``CustomAgentEval1`` and
``CustomAgentEval2``, which are hypothetical subclasses of
``AgentEval``) are combined using the ``AgentEvalComposite``. Please
replace the ``CustomAgentEval`` classes with actual ``AgentEval``
subclasses according to your application.

Note: This is a simplified example and does not cover all the possible
uses and features of ``AgentEvalComposite``.

.. code:: python

   from automata.eval.agent.agent_eval_composite import AgentEvalComposite
   from automata.eval.agent.agent_eval import AgentEval

   class CustomAgentEval1(AgentEval):
       pass

   class CustomAgentEval2(AgentEval):
       pass

   evaluator1 = CustomAgentEval1()
   evaluator2 = CustomAgentEval2()
   composite_evaluator = AgentEvalComposite([evaluator1, evaluator2])

   # Additional implementation of the evaluators and the composite evaluator is required to demonstrate the complete operation.

Limitations
-----------

Though providing the flexibility needed to combine multiple evaluators,
``AgentEvalComposite`` does not implement action filtering
(``_filter_actions``). This could limit its capacity in scenarios where
filtering actions based on certain conditions is needed after extracting
action from the given message. Implementing this in a subclass might be
necessary based on the use case.

Another limitation comes into play when the evaluators return a type
that is not an ``AgentEvalResult``. Since the composite evaluator
strictly checks the type to be ``AgentEvalResult``, it throws a
``ValueError`` in case the type returned is incorrect. Hence,
subclassing ``AgentEval`` demands discipline ensuring that the output
type is always as expected.

Follow-up Questions:
--------------------

-  Is there a way to make ’\_filter_actions’ method in
   ``AgentEvalComposite`` more flexible or adaptable to the specific
   cases where action filtering is needed?
-  How could type checking be made more robust, or handled in a more
   pythonic way, rather than checking after results are computed?
-  In which cases are composite evaluations particularly beneficial, and
   could example cases be provided in the documentation?
