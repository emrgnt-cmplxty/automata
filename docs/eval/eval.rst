Eval
====

Overview
--------

``Eval`` is an abstract class that provides a blueprint for evaluating
the performance of Language Learning Models (LLMs). The class is
designed to be very flexible and accommodates different kinds of
evaluators through method overriding. It requires implementing three
primary methods: ``generate_eval_result``, ``extract_action``, and
``_filter_actions``. The ``generate_eval_result`` is used to produce an
evaluation result given a set of instructions, expected actions, and an
execution mechanism. The ``extract_action`` method is for pulling out a
list of actions from a given message, and ``_filter_actions`` is for
refining the action list according to the needs of the evaluation.

Related Symbols
---------------

-  ``automata.singletons.py_module_loader.PyModuleLoader.__init__``
-  ``automata.eval.tool.tool_eval_metrics.ToolEvaluationMetrics.__init__``
-  ``automata.llm.llm_base.LLMConversation.__init__``
-  ``automata.embedding.embedding_base.Embedding.__str__``
-  ``automata.tasks.task_base.TaskEnvironment.validate``
-  ``automata.tasks.task_base.Task.status``
-  ``automata.core.ast_handlers.DocstringRemover.visit``
-  ``automata.tasks.automata_task.AutomataTask.__init__``
-  ``automata.llm.llm_base.LLMCompletionResult``
-  ``automata.core.base.patterns.observer.Observer``

Example
-------

Since ``Eval`` is an abstract class, you cannot create an instance of it
directly. Instead, you need to create a subclass that implements the
required methods: ``generate_eval_result``, ``extract_action``, and
``_filter_actions``. Below is an example of how to create a subclass of
Eval:

.. code:: python

   from automata.eval.eval_base import Eval

   class MyCustomEval(Eval):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)

       def generate_eval_result(self, exec_input, expected_output, executor, *args, **kwargs):
           # Implement the method to generate eval result
           pass

       def extract_action(self, input):
           # Implement the method to extract actions from the input
           pass

       def _filter_actions(self, inputs):
           # Implement the method to filter the extracted actions
           pass

Limitations
-----------

The main limitation of the ``Eval`` class is that it is an abstract base
class (ABC) and it cannot be used on its own without providing concrete
implementations of the ``generate_eval_result``, ``extract_action``, and
``_filter_actions`` methods. This means that the usefulness of the
``Eval`` class is dependant on how these methods are implemented in the
subclass.

Follow-up Questions:
--------------------

-  What are some strategies for implementing the
   ``generate_eval_result``, ``extract_action``, and ``_filter_actions``
   methods?
-  Is it possible to provide a default implementation of these methods
   in the ``Eval`` class to make it usable out of the box, while still
   allowing for customization via subclassing?
