CompletionResult
================

``CompletionResult`` is an abstract base class that provides a method
``get_completions()`` which should be implemented by any classes
extending it. The purpose of ``CompletionResult`` is to provide a
standard way of retrieving completions resulting from the AI interaction
using OpenAI’s API.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.database.vector.JSONVectorDatabase``

Method
------

-  ``get_completions() -> list[str]:`` An abstract method that should be
   implemented by the extending class. It should return a list of string
   completions.

Example
-------

The following example demonstrates how to create a custom class
extending ``CompletionResult`` and implementing the
``get_completions()`` method.

.. code:: python

   from automata.core.base.openai import CompletionResult

   class CustomCompletionResult(CompletionResult):
       def __init__(self, completions):
           self._completions = completions

       def get_completions(self) -> list[str]:
           return self._completions

   completions = ["completion_1", "completion_2", "completion_3"]
   custom_completion_result = CustomCompletionResult(completions)
   result_completions = custom_completion_result.get_completions()

   print(result_completions)  # Output: ['completion_1', 'completion_2', 'completion_3']

Limitations
-----------

The ``CompletionResult`` class is limited by the fact that it does not
provide any native functionality for interacting with the OpenAI API.
The responsibility of generating completions and interacting with the
API is left to the classes extending ``CompletionResult``. It simply
provides a standardized method for extracting completions provided by
the implementing classes.

Follow-up Questions:
--------------------

-  What is the primary use case for the ``CompletionResult`` class in
   the context of the other related classes?
-  Are there any other important methods or properties that should be
   included in the ``CompletionResult`` class?
