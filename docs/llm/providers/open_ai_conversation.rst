OpenAIConversation
==================

``OpenAIConversation`` is a class that represents a conversation with
the OpenAI API. It manages the series of messages that are part of the
conversation flow. The class includes methods to add messages, get the
latest message, get all messages for the next completion, and reset the
conversation. The OpenAIConversation class is heavily used in
interactions within the agent classes.

Overview
--------

``OpenAIConversation`` provides a way to manage and manipulate the
conversation of an agent with the OpenAI API. Each message in the
conversation is an instance of OpenAIChatMessage. The primary purpose of
``OpenAIConversation`` is to keep track of the series of messages in the
conversation. Each new message is appended to the list of messages and
can be retrieved when required. An important aspect is that the
``OpenAIConversation`` only accepts messages of type
``OpenAIChatMessage``.

Related Symbols
---------------

-  ``automata.llm.providers.openai.OpenAIChatMessage``
-  ``automata.llm.providers.openai.OpenAIChatCompletionProvider``
-  ``automata.agent.providers.OpenAIAutomataAgent``
-  ``automata.llm.foundation.LLMChatMessage``

Example
-------

Here is an example demonstrating how to create and manage messages in an
``OpenAIConversation``:

.. code:: python

   from automata.llm.providers.openai import OpenAIConversation, OpenAIChatMessage

   # create conversation
   conversation = OpenAIConversation()

   # create a message and add it into the conversation
   message = OpenAIChatMessage(role="assistant", content="Hello, I am an assistant.")
   conversation.add_message(message)

   # retrieve the latest message
   latest_message = conversation.get_latest_message()
   print(latest_message)  # OpenAIChatMessage object

   # retrieve all messages for next completion
   messages_for_completion = conversation.get_messages_for_next_completion()
   print(messages_for_completion)  # list of messages

   # reset the conversation
   conversation.reset_conversation()
   # checking the length of conversation after reset
   print(len(conversation))  # Output: 0

Limitations
-----------

One limitation of ``OpenAIConversation`` is that it only accepts
messages of the type ``OpenAIChatMessage``. This could make it less
flexible if a different message class needs to be used in certain
situations.

Follow-up Questions:
--------------------

-  Is there a way to extend the OpenAIConversation to handle more types
   of chat messages?
-  How does the class interact with other parts, like agent classes or
   completion providers, to contribute to the overall functionality of
   the Automata library?
