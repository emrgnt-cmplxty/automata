LLMChatMessage
==============

``LLMChatMessage`` is a base class representing different types of Lower
Level Model (LLM) chat messages. This class structures the chat messages
that are processed to and from an LLM. It is used widely throughout the
linked conversational module talks, and plays a critical role in
structuring and storing various chat interactions for retrieval later.

Overview
--------

The ``LLMChatMessage`` class provides a way to structure conversations
in a conversational user interface with an LLM. Each instance of the
class represents one message in the chat. The ``LLMChatMessage`` class
encapsulates the role and content of a chat message and provides a
uniform interface in the form of the ``to_dict()`` method for converting
the message to a dictionary object.

The ``LLMChatMessage`` class is included in the interaction with the
chat API, the chat message completion providers, the chat conversations,
and in test scenarios.

Related Symbols
---------------

-  ``automata.llm.providers.openai.OpenAIChatMessage``
-  ``automata.llm.providers.openai.OpenAIConversation.get_latest_message``
-  ``automata.llm.foundation.LLMConversation.get_latest_message``

Examples
--------

The following is an example demonstrating how to create an instance of
``LLMChatMessage`` and use it in conversation.

.. code:: python

   from automata.llm.foundation import LLMChatMessage

   # Create a LLMChatMessage instance
   message = LLMChatMessage(role="user", content="Hello, how are you?")

   # Convert the message to a dict
   message_dict = message.to_dict()
   print(message_dict) # Prints: {'role': 'user', 'content': 'Hello, how are you?'}

The following is an example demonstrating how to save a conversation
interaction to a database.

.. code:: python

   from automata.llm.foundation import LLMChatMessage
   from automata.core.base.database.relational import SQLDatabase

   # Given a SQL database instance and a conversation interaction
   db = SQLDatabase()
   interaction = {"role": "user", "content": "Good morning!"}

   # Save the message to the database
   db.save_message(LLMChatMessage(**interaction))

Limitations
-----------

``LLMChatMessage`` is essentially a structure providing interface for a
chat message object. It does not check the validity of the chat message
or analyze its text. Additional limitations depend on the
implementations in the related symbols.

##Follow-up Questions:

-  What are the valid values for the ``role`` attribute in
   ``LLMChatMessage``?
-  Is there a limit on the ``content`` length for a chat message? If so,
   how is a message beyond this limit handled?
