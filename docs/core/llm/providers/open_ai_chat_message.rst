OpenAIChatMessage
=================

Overview
--------

``OpenAIChatMessage`` is a class that represents a processed chat
message TO or FROM the OpenAI LLM Chat API. It provides convenient
methods to parse and generate messages compatible with the OpenAI Chat
API.

This class is a part of the ``automata.core.llm.providers.openai``
module and extends the ``LLMChatMessage`` base class, adding unique
fields and methods suitable for communication with the OpenAI API.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.core.llm.providers.openai.OpenAIChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMChatMessage``

Example
-------

Below is an example of creating a message, converting it to a
dictionary, and retrieving it from a completion result:

.. code:: python

   from automata.core.llm.providers.openai import FunctionCall, OpenAIChatCompletionResult, OpenAIChatMessage

   # The function call 
   function_call = FunctionCall.from_response_dict({
       "name": "call_termination",
       "arguments": '{"result": "Success"}',
   })

   # Create an OpenAI Chat Message instance
   message = OpenAIChatMessage(role="assistant", function_call=function_call)

   # Convert message to dictionary
   message_dict = message.to_dict()

   # Create a mock OpenAI Chat Completion Result
   completion_result = OpenAIChatCompletionResult.from_args(
       role="assistant",
       content=None,
       function_call=function_call
   )

   # Retrieve the OpenAI Chat Message from the completion result
   retrieved_message = OpenAIChatMessage.from_completion_result(completion_result)

Limitations
-----------

This class assumes that the ``OpenAIChatCompletionResult`` already has
the required fields parsed in the expected format. Consequently, if the
OpenAI API changes its response format, the ``from_completion_result``
method may not function as expected.

Machines created from ``OpenAIChatMessage`` may not contain a
``function_call`` field if the processed message does not instruct a
function call.

Follow-up Questions:
--------------------

-  How does ``OpenAIChatMessage`` handle unexpected
   ``OpenAIChatCompletionResult`` structures?
-  Are there safety measures in place to ensure ``OpenAIChatMessage``
   instances are created correctly when a ``function_call`` field is
   missing from a message?
