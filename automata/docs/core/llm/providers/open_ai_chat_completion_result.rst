``OpenAIChatCompletionResult``
==============================

Overview
--------

``OpenAIChatCompletionResult`` is a class that represents a chat
response from the OpenAI API. This class takes in raw messages from the
chat API and structures them for further use. Apart from regular chat
message contents, it can also include function calls which the API may
return during an ongoing chat.

Related Symbols
---------------

-  ``LLMChatCompletionProvider``
-  ``LLMChatMessage``
-  ``FunctionCall``
-  ``OpenAIChatMessage``
-  ``OpenAIChatCompletionProvider``

Initialization
--------------

``OpenAIChatCompletionResult`` class can be initialized by providing the
raw data from OpenAI chat API. The ``__init__`` function processes the
raw data and assigns it to class variables.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIChatCompletionResult

   # Example raw data from OpenAI chat API
   raw_data = {
       "choices": [
           {
               "message": {
                   "role": "assistant",
                   "content": "Hello, how can I assist you today?",
                   "function_call": None
               }
           }
       ]
   }

   completion_result = OpenAIChatCompletionResult(raw_data)

Methods
-------

``OpenAIChatCompletionResult`` class has a few methods for handling and
representing the data it encapsulates:

-  ``__str__``: Produces a string representation of the completion
   result.
-  ``from_args``: A class method for creating an instance of
   ``OpenAIChatCompletionResult``.
-  ``get_function_call``: Returns the ``FunctionCall`` object if
   present. If no function call is present, it returns None.

Usage Example
-------------

Following is an example of a using ``from_args`` method to create an
instance and printing it out using the ``__str__`` method:

.. code:: python

   # Import necessary classes
   from automata.core.llm.providers.openai import OpenAIChatCompletionResult

   # Create an instance using the `from_args` class method
   completion_result = OpenAIChatCompletionResult.from_args("assistant", "Hello, how can I assist you today?", None)

   # Use the `__str__` method to print the instance
   print(completion_result)

Limitations
-----------

One possible limitation of the ``OpenAIChatCompletionResult`` is its
strict reliance on the OpenAI API’s ``choices`` output structure. Any
changes in the API’s response structure can potentially break the
functionality of this class.

Follow-Up Questions:
--------------------

-  What happens if the OpenAI API changes the response structure? Do we
   have a mechanism to handle these changes?
-  Is there a validation step to check the integrity and format of the
   raw data received from the OpenAI API before it’s processed?
-  Is there a way to handle other roles besides “assistant”? Are other
   roles anticipated in the future?
