OpenAIConversation
==================

``OpenAIConversation`` is a class representing a conversation between
the user and the AI assistant. It is used in conjunction with the
``OpenAIChatCompletionProvider`` to manage interactions and message
history with OpenAI’s API. It provides methods to add, remove, reset
messages in the conversation, manage message observers, and generate a
structured payload of messages that can be used by the
``OpenAIChatCompletionProvider`` to obtain completions.

Overview
--------

``OpenAIConversation`` extends the abstract base class
``LLMConversation``, providing implementations for its abstract methods
as well as additional functionality specifically for OpenAI API
interaction. The conversation is initialized with an empty message list
and a set of observers that can be registered or unregistered to be
notified when the conversation changes.

Related Symbols
---------------

-  ``automata.core.llm.providers.openai.OpenAIChatCompletionProvider``
-  ``automata.core.llm.foundation.LLMConversation``
-  ``automata.core.base.patterns.observer.Observer``
-  ``automata.core.llm.providers.openai.OpenAIChatMessage``

Example
-------

.. code:: python

   from automata.core.llm.providers.openai import OpenAIConversation, OpenAIChatMessage

   conversation = OpenAIConversation()

   user_message = OpenAIChatMessage(role="user", content="What is the capital of France?")
   conversation.add_message(user_message)

   assistant_message = OpenAIChatMessage(role="assistant", content="The capital of France is Paris.")
   conversation.add_message(assistant_message)

   print(len(conversation))  # Output: 2

   conversation.reset_conversation()
   print(len(conversation))  # Output: 0

Limitations
-----------

``OpenAIConversation`` is designed specifically for use with OpenAI’s
API and may not be compatible with other language model providers
without modification. Additionally, it assumes a certain structure for
messages and conversation states, based on OpenAI’s API expectations.

Follow-up Questions:
--------------------

-  How can the conversation class structure be improved to be more
   flexible and maintain better compatibility with other language model
   providers?
