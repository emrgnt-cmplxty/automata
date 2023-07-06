LLMConversation
===============

``LLMConversation`` is an abstract base class designed to represent
different types of LLM (Language Learning Module) conversations. It is a
part of the library, ``automata.llm.foundation``.

Overview
--------

``LLMConversation`` is an outline or blueprint for implementing
different conversation types. As an abstract base class, it lays out a
set of methods that should be implemented in the child classes. Some of
the methods specified by this class involve getting the latest message,
registering observers, and managing messages within a conversation.

One of the exceptions managed by this module is the
``LLMEmptyConversationError``, raised when an operation is invoked for
an empty conversation.

Related Symbols
---------------

-  ``automata.llm.foundation.LLMConversation.get_latest_message``
-  ``automata.llm.providers.openai.OpenAIConversation.get_latest_message``
-  ``automata.llm.foundation.LLMChatMessage``
-  ``automata.llm.foundation.LLMConversationDatabaseProvider``
-  ``automata.llm.providers.openai.OpenAIConversation``

Example
-------

Below is a sample implementation of ``LLMConversation`` and usage of
``LLMEmptyConversationError``. As ``LLMConversation`` is an abstract
base class, we need to first implement all abstract methods in a
subclass:

.. code:: python

   from automata.llm.foundation.LLMConversation import LLMEmptyConversationError, LLMChatMessage
   from automata.core.base.patterns.observer import Observer

   class CustomConversation(LLMConversation):
       def __init__(self):
           self._observers: Set[Observer] = set()
           self.messages: List[LLMChatMessage] = []

       def get_latest_message(self) -> LLMChatMessage:
           try:
               return self.messages[-1]
           except IndexError:
               raise LLMEmptyConversationError()

       # Note: Similarly implement the rest of the abstract methods here...

   # Usage
   conversation = CustomConversation()

   try:
       latest_message = conversation.get_latest_message()
   except LLMEmptyConversationError:
       print("Conversation is currently empty.")

Limitations
-----------

This class is an abstract base class, so it cannot be instantiated
directly. Additionally, it does not provide default implementations for
its abstract methods requiring subclasses to provide their own specific
implementations. Also, error handling for empty conversations is a
responsibility of the class’s consumers.

Follow-up Questions:
--------------------

-  Are there any specifications on how the other abstract methods (like
   ``__len__``, ``get_messages_for_next_completion``, and
   ``notify_observers``) should be implemented?
-  How are observers expected to interact with this class?
