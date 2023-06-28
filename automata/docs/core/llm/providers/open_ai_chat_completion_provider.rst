OpenAIChatCompletionProvider
============================

``OpenAIChatCompletionProvider`` is a class that provides chat messages
from the OpenAI API. Using this class allows the user to add new
messages, get completions from the assistant, and reset the conversation
state.

Overview
--------

``OpenAIChatCompletionProvider`` initializes with a defined model,
temperature, and conversation state. It can process chat messages, make
requests to the OpenAI API, and extract completions from the API
response. This class leverages the API calls for chat completion and
performs additional functionality like managing conversation state,
registering custom functions, and interacting with other related classes
and components.

Related Symbols
---------------

-  ``automata.core.llm.completion.LLMChatCompletionProvider``
-  ``automata.core.llm.completion.LLMChatMessage``
-  ``automata.core.llm.completion.LLMCompletionResult``
-  ``automata.core.llm.completion.LLMConversation``
-  ``automata.core.llm.providers.openai.OpenAIChatCompletionResult``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.core.llm.providers.openai.OpenAIFunction``

Example
-------

The following is an example demonstrating how to create an instance of
``OpenAIChatCompletionProvider`` and add a new message to the
conversation.

.. code:: python

   from automata.core.llm.providers.openai import OpenAIChatCompletionProvider, OpenAIChatMessage

   # Initialize OpenAIChatCompletionProvider
   completion_provider = OpenAIChatCompletionProvider(model="gpt-4", temperature=0.7, stream=False)

   # Add a new message to the conversation
   message = OpenAIChatMessage(role="user", content="What's the capital of France?")
   completion_provider.add_message(message)

   # Get the completion from the assistant
   response = completion_provider.get_next_assistant_completion()
   print(response.content)

Limitations
-----------

``OpenAIChatCompletionProvider`` is limited by the capabilities of the
underlying OpenAI API and the defined model. It is subject to the
quality of completions provided by the API and might not always produce
desired results. In addition, the API must be set up with proper
authentication keys to be used.

Follow-up Questions:
--------------------

-  How does the ``stream`` parameter influence the behavior of the
   class?
-  Are there any specific limitations with using custom functions?
