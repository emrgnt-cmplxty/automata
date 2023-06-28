OpenAIChatCompletionResult
==========================

``OpenAIChatCompletionResult`` is a class to represent a completion
result from the OpenAI API. The class provides utility methods to
interact with and process completion results, as well as a way to create
a new ``OpenAIChatCompletionResult`` from arguments. The class extends
the base class ``LLMCompletionResult``.

Overview
--------

``OpenAIChatCompletionResult`` offers methods to get the content and
role of the completion message and retrieve the function call if
present. The class can also serve as a foundation to build more
specialized completion result classes if needed.

Related Symbols
---------------

-  ``automata.core.llm.completion.LLMCompletionResult``
-  ``automata.core.llm.providers.openai.FunctionCall``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.llm.providers.openai.OpenAIChatCompletionProvider``
-  ``automata.tests.unit.test_automata_agent.mock_openai_response_with_completion_message``
-  ``automata.tests.unit.test_automata_agent.test_run_with_completion_message``

Example
-------

The following is an example demonstrating how to create an instance of
``OpenAIChatCompletionResult`` using a raw response dictionary.

.. code:: python

   api_response_data = {
       "choices": [
           {
               "message": {
                   "role": "assistant",
                   "content": "Welcome to the chat!",
               }
           }
       ]
   }

   completion_result = OpenAIChatCompletionResult(raw_data=api_response_data)

To create a new ``OpenAIChatCompletionResult`` from arguments:

.. code:: python

   from automata.core.llm.providers.openai import FunctionCall, OpenAIChatCompletionResult

   role = "assistant"
   content = "Hello user!"
   function_call = FunctionCall.from_response_dict({"name": "greet_user", "arguments": {}})

   completion_result = OpenAIChatCompletionResult.from_args(role, content, function_call)

Limitations
-----------

The primary limitation of ``OpenAIChatCompletionResult`` is that it is
designed specifically for processing completion results received from
the OpenAI API. It cannot work with completion results from other APIs
or different response structures.

Follow-up Questions:
--------------------

-  How can we extend ``OpenAIChatCompletionResult`` to support more
   specialized completion results or other APIs?
-  Are there any alternative ways to represent completion results that
   would provide more flexibility or modularity?
