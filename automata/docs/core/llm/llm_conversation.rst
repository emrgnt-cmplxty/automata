LLMConversation
===============

``LLMConversation`` is an abstract base class for different types of
language learning model (LLM) conversations. It provides an interface
for managing conversation instances and their messages.

Overview
--------

``LLMConversation`` defines a set of abstract methods for creating,
managing, and resetting conversations. It is designed to be extended by
subclasses which implement the conversation logic and handle the LLM
chat messages. Some of the main methods include ``add_message``,
``get_latest_message``, ``get_messages_for_next_completion``, and
``reset_conversation``. Together, these methods allow for a flexible and
customizable way of working with LLM conversations.

Related Symbols
---------------

-  ``automata.core.llm.foundation.LLMChatMessage``
-  ``automata.core.llm.providers.openai.OpenAIConversation``
-  ``automata.core.llm.foundation.LLMChatCompletionProvider``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``
-  ``automata.core.base.observer.Observer``
-  ``automata.core.base.database.relational.SQLDatabase``

Example
-------

The following is an example demonstrating how to create a custom LLM
conversation class (e.g., ``CustomLLMConversation``) which extends
``LLMConversation``:

.. code:: python

   from automata.core.llm.foundation import LLMConversation, LLMChatMessage

   class CustomLLMConversation(LLMConversation):
       def __init__(self):
           self.messages = []

       def add_message(self, message: LLMChatMessage):
           self.messages.append(message)

       def get_latest_message(self) -> LLMChatMessage:
           if not self.messages:
               raise LLMConversation.LLMEmptyConversationError
           return self.messages[-1]

       def get_messages_for_next_completion(self):
           return self.messages

       def register_observer(self, observer) -> None:
           pass
           
       def unregister_observer(self, observer) -> None:
           pass

       def reset_conversation(self) -> None:
           self.messages = []

       def notify_observers(self):
           pass

   # Example Usage
   conversation = CustomLLMConversation()
   conversation.add_message(LLMChatMessage(role="user", content="Hello, LLM!"))
   print(conversation.get_latest_message())

Limitations
-----------

As an abstract base class, ``LLMConversation`` cannot be instantiated
directly. Instead, it must be subclassed and its abstract methods need
to be implemented by the derived class. Additionally, the class does not
provide an implementation for observer functionality (i.e., registering,
unregistering, and notifying observers) as this should be implemented in
each subclass based on the specific needs.

Follow-up Questions:
--------------------

-  How does the ``notify_observers`` method work in concrete subclasses
   such as ``OpenAIConversation``?
