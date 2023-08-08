ToolEval
========

``ToolEval`` is an abstract class designed for evaluating the
performance of tools by generating and comparing expected and observed
results. It has several methods you can override to customize the
evaluation process. It requires the expected output, the tool executor,
and the function call to generate the eval result.

Overview
--------

``ToolEval`` is a core part of the evaluation system in Automata. It
provides a structure and means to evaluate how well a tool performs in
its task. This class requires implementation of the ``extract_action``
and ``to_tool_result`` methods, meaning you can give it specific
evaluation behaviours such as how to translate operations and determine
the equivalence between expected and observed actions.

Related Symbols
---------------

-  ``automata.tasks.task_environment.AutomataTaskEnvironment.validate``
-  ``automata.core.base.patterns.singleton.Singleton``
-  ``automata.cli.env_operations.update_key_value``
-  ``automata.tasks.task_environment.EnvironmentMode``
-  ``automata.tasks.task_base.ITaskExecution``
-  ``automata.tasks.task_base.ITaskExecution.execute``
-  ``automata.eval.eval_base.Action.__init__``
-  ``automata.cli.env_operations.load_env_vars``
-  ``automata.tasks.task_base.TaskEnvironment.teardown``
-  ``automata.tools.tool_executor.ToolExecutor.__init__``

Example
-------

Please note that ``ToolEval`` is an abstract base class and cannot be
instantiated directly. The following is an example demonstrating how to
create an implementation of ``ToolEval``.

.. code:: python

   from automata.eval.tool.tool_eval import ToolEval
   from automata.eval.eval_base import EvalResult, Action
   from typing import Tuple, Optional, List

   class CustomToolEval(ToolEval):

       def extract_action(self, input_action_tuple: Tuple) -> Action:
           # Custom implementation of action extraction
           pass

       def to_tool_result(self, expected_action: Action, observed_action: Optional[Action]) -> EvalResult:
           # Custom method of evaluating tool results
           pass

       def _filter_actions(self, actions: List[Action]) -> List[Action]:
           # Custom implementation to filter actions if necessary
           pass

Limitations
-----------

The limitations of the ``ToolEval`` class are up to the implemented
class, as ``ToolEval`` is an abstract base class. However, it’s worth
noting that it does not inherently include any failure recovery or retry
mechanisms. If these are necessary for your use case, you should include
them in your implementation.

Follow-up Questions:
--------------------

-  What are some common strategies for implementing ``extract_action``
   and ``to_tool_result``?
-  How can we handle cases where the tool execution fails?
-  How can this be used in conjunction with other parts of the Automata
   project? Is there a method to easily integrate this with existing
   task environments or tool executors?
