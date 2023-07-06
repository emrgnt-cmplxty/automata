LLMConversation
===============

``LLMConversation`` is an abstract base class for different types of
Language-Learning Model (LLM) conversations in the Automata framework.
It provides a blueprint for managing multiple conversations with
different observers in a multithreaded application scenario.

Overview
--------

``LLMConversation`` uses the Observer design pattern to manage updates
to the state of the conversation. It contains abstract methods that
provide the structure for handling different types of LLM chat messages
and can be expanded and customized for specific implementations. As an
abstract base class, ``LLMConversation`` cannot be instantiated directly
and must be subclassed to be utilized.

Related Symbols
---------------

-  ``automata.llm.providers.openai.OpenAIConversation.get_latest_message``
-  ``automata.llm.foundation.LLMChatMessage``
-  ``automata.tests.unit.test_conversation_database.test_put_message_increments_interaction_id``
-  ``automata.tests.unit.test_conversation_database.test_get_messages_returns_all_messages_for_session``
-  ``automata.llm.providers.openai.OpenAIConversation``
-  ``automata.memory_store.agent_conversation_database.AgentConversationDatabase``
-  ``automata.core.base.patterns.observer.Observer``

Example
-------

Below is an example of how a subclass of ``LLMConversation`` might be
designed:

.. code:: python

   from automata.llm.foundation import LLMConversation, LLMChatMessage
   from automata.core.base.patterns.observer import Observer

   class CustomConversation(LLMConversation):
       def __init__(self):
           super().__init__()
           self.messages = []

       def __len__(self):
           return len(self.messages)

       def get_latest_message(self) -> LLMChatMessage:
           return self.messages[-1]

       def get_messages_for_next_completion(self):
           return self.messages

       def reset_conversation(self) -> None:
           self.messages = []

   # Subscribing an observer to the custom conversation
   class CustomObserver(Observer):
       def update(self, subject: LLMConversation) -> None:
           print(f"Observer notified. Latest message: {subject.get_latest_message().to_dict()}")

   conversation = CustomConversation()
   observer = CustomObserver()
   conversation.register_observer(observer)

   # Create and add a message to the conversation
   message = LLMChatMessage(role="user", content="Hello!")
   conversation.messages.append(message)
   # Notify observers of the change
   conversation.notify_observers()

In this script: 1. A custom conversation class is built by subclassing
``LLMConversation`` and defining the required methods. 2. An observer
class is built by subclassing ``Observer`` and implementing the
``update`` method. 3. An instance of the custom conversation is created
and an observer is registered. 4. A new message is created and added to
the conversation, and the ``notify_observers`` method is called to
update all registered observers.

Limitations
-----------

``LLMConversation`` is an abstract class and cannot be used until all
its abstract methods are implemented in the subclass. The
responsibilities attached to the abstract methods should be
well-understood before implementing a subclass.

Follow-up Questions:
--------------------

-  Are there any performance considerations to keep in mind while
   implementing the abstract methods, especially when conversations get
   too long?
-  What is the underlying infrastructure to support notifications to a
   possibly large number of observers? Is there a limit on the number of
   observers that can be registered to an instance of
   ``LLMConversation``?
-  What additional functionality might be useful to include in the base
   ``LLMConversation`` class that would be universal across all types of
   chatbot conversations? Can this be extended to include multimedia
   messages along with text?
