OpenAIChatCompletionResult
==========================

``OpenAIChatCompletionResult`` is a utility class that processes the
results obtained from the OpenAI Chat API. It contains a method to
extract the primary completion result from the chat API response.

Overview
--------

``OpenAIChatCompletionResult`` provides a way to extract the primary
completion message from the raw data received from the OpenAI Chat API.
The class provides a single method, ``get_completion``, which is
responsible for extracting the necessary information.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Example
-------

The following is an example demonstrating how to use
``OpenAIChatCompletionResult`` to extract the completion message from a
raw chat API response.

.. code:: python

   import json
   from automata.core.base.openai import OpenAIChatCompletionResult

   raw_data = json.loads("""
   {
     "id": "chatcmpl-6p9XYPYSTTRi0xEviKjjilqrWU2Ve",
     "object": "chat.completion",
     "created": 1677649420,
     "model": "gpt-3.5-turbo",
     "usage": {
       "prompt_tokens": 56,
       "completion_tokens": 31,
       "total_tokens": 87
     },
     "choices": [
       {
         "message": {
           "role": "assistant",
           "content": "The capital of France is Paris."
         },
         "finish_reason": "stop",
         "index": 0
       }
     ]
   }
   """)

   completion_result = OpenAIChatCompletionResult(raw_data)
   completion = completion_result.get_completion()
   print(completion)  # Output: "The capital of France is Paris."

Limitations
-----------

``OpenAIChatCompletionResult`` is specifically designed to work with the
OpenAI Chat API and may not be suitable for processing other
conversation-related API responses. Additionally, the class only
provides a method for extracting the primary completion message, and any
other information available in the chat API response is not accessible
through this class.
