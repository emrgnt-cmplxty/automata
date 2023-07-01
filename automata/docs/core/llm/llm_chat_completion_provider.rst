LLMChatCompletionProvider
=========================

``LLMChatCompletionProvider`` is an abstract base class that defines the
methods and behaviors for chat completion providers that work with the
LLM (Language Learning Machine) models. It provides an interface for
derived classes to implement core methods such as adding messages to the
chat, getting the next message from the assistant, and resetting the
chat provider.

Derived chat providers, such as ``OpenAIChatCompletionProvider``, can be
used to communicate with different language models for generating
completions and managing chat state.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.foundation.LLMConversation``

Example
-------

You can create a custom chat completion provider that extends
``LLMChatCompletionProvider``. For this example, let’s create a custom
completion provider called ``MyChatCompletionProvider``:

.. code:: python

   from automata.core.llm.foundation import LLMChatCompletionProvider, LLMChatMessage

   class MyChatCompletionProvider(LLMChatCompletionProvider):

       def __init__(self):
           super().__init__()

       def add_message(self, message: LLMChatMessage) -> None:
           # Implement your custom logic for adding messages.
           pass

       def get_next_assistant_completion(self) -> LLMChatMessage:
           # Implement your custom logic for generating completions from the LLM.
           pass

       def reset(self) -> None:
           # Implement your custom logic for resetting the chat provider.
           pass

Once you have implemented your custom chat completion provider, you can
use it to generate completions from the LLM:

.. code:: python

   my_chat_provider = MyChatCompletionProvider()
   user_message = LLMChatMessage(role="user", content="Hello, how are you?")
   my_chat_provider.add_message(user_message)
   assistant_response = my_chat_provider.get_next_assistant_completion()
   print(assistant_response.content)

Limitations
-----------

Since ``LLMChatCompletionProvider`` is an abstract base class, you
cannot instantiate it directly. You must create a derived class and
implement the required abstract methods.

Also, it only specifies the methods for adding messages, getting the
next completion, and resetting the provider. Additional features or
functionalities, such as streaming or advanced control over generated
completions, should be implemented in the derived classes.

Follow-up Questions:
--------------------

-  Can you provide examples of using different derived classes of
   LLMChatCompletionProvider with different LLM models?
