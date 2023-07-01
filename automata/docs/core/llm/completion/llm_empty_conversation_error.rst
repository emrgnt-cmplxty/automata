LLMConversation
===============

``LLMConversation`` is an abstract base class for different types of LLM
conversations. It provides a standard interface for managing chat
messages and observers in a conversation. LLMConversation has methods to
add messages, get the latest message, and get messages for the next
completion.

Related Symbols
---------------

-  ``automata.core.llm.foundation.LLMEmptyConversationError``
-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.tests.unit.test_conversation_database``

Overview
--------

``LLMConversation`` is raised when the conversation is empty. It
provides methods to interact with and manage chat conversations, as well
as methods for managing observers. Derived classes provide more specific
implementations, such as the ``OpenAIConversation``.

Example
-------

The following example demonstrates creating a custom conversation class
that extends ``LLMConversation``:

.. code:: python

   from automata.core.llm.foundation import LLMConversation, LLMChatMessage

   class MyCustomConversation(LLMConversation):
       def __init__(self):
           super().__init__()
           self.messages = []
       
       def add_message(self, message: LLMChatMessage):
           self.messages.append(message)
       
       def get_latest_message(self) -> LLMChatMessage:
           if not self.messages:
               raise LLMConversation.LLMEmptyConversationError()
           return self.messages[-1]
           
       def get_messages_for_next_completion(self) -> Any:
           return [{"text": message.content} for message in self.messages]

   # Usage example
   conversation = MyCustomConversation()
   message = LLMChatMessage(role="user", content="Hello, LLM!")
   conversation.add_message(message)
   latest_message = conversation.get_latest_message()
   print(latest_message.content)  # Output: Hello, LLM!

Limitations
-----------

``LLMConversation`` is an abstract base class, so you can’t create an
instance of it directly. Instead, you need to create a derived
conversation class that implements the required methods, as demonstrated
in the example above.

Follow-up Questions:
--------------------

-  How can we modify the base class to allow custom configurations?
