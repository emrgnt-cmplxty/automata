OpenAIBaseCompletionResult
==========================

``OpenAIBaseCompletionResult`` is an abstract base class for handling
the completion results from OpenAI API responses. It provides an
interface for extracting relevant completions from the returned raw
data.

Overview
--------

``OpenAIBaseCompletionResult`` aims to simplify the processing of OpenAI
API responses by defining an interface for extracting completion
results. Classes inheriting from this base class are expected to
implement the ``get_completions`` method, which should return a list of
extracted completions.

Related Symbols
---------------

-  ``automata.core.base.openai.OpenAIChatCompletionResult``
-  ``automata.core.base.openai.CompletionResult``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

Suppose we have a custom class called ``MyOpenAICompletionResult`` that
inherits from ``OpenAIBaseCompletionResult``.

.. code:: python

   from automata.core.base.openai import OpenAIBaseCompletionResult

   class MyOpenAICompletionResult(OpenAIBaseCompletionResult):
       def get_completions(self) -> list[str]:
           # Custom logic to extract completions from raw_data
           return ["completion 1", "completion 2"]

We can then use this class to process an OpenAI API response:

.. code:: python

   response_data = {
       "choices": [
           {"message": {"content": "completion 1"}},
           {"message": {"content": "completion 2"}},
       ]
   }

   my_result = MyOpenAICompletionResult(response_data)
   completions = my_result.get_completions()
   print(completions)  # Output: ["completion 1", "completion 2"]

Limitations
-----------

``OpenAIBaseCompletionResult`` is an interface and cannot be used
directly without providing an implementation for the ``get_completions``
method. It means that you must create a custom class inheriting from
``OpenAIBaseCompletionResult`` and provide the appropriate logic for
extracting the desired completion results.

Follow-up Questions:
--------------------

-  Can you provide an example of a comprehensive custom implementation
   of ``OpenAIBaseCompletionResult`` to handle different types of OpenAI
   API responses?
-  Are there other necessary methods or attributes that should be added
   to ``OpenAIBaseCompletionResult`` to cover more use cases?
