OpenAIAutomataConversationDatabase
==================================

``OpenAIAutomataConversationDatabase`` is a class used to handle
interactions of an Automata agent with a conversation database. It
facilitates operations such as saving messages, retrieving messages, and
maintaining sessions and interactions within a conversation.

Overview
--------

``OpenAIAutomataConversationDatabase`` provides functionality to handle
conversation storage within a database for an Automata agent. It
inherits from ``LLMConversationDatabaseProvider``, and defines methods
to interact with the database. Primary functions provide the ability to:
check session validity, save messages per sessions, fetch messages based
on session id, and maintain interaction count. The table for
conversation data is created at the time of class object creation.

Related Symbols
---------------

-  ``automata.memory_store.conversation_database_providers.LLMConversationDatabaseProvider``
-  ``OpenAIChatMessage``
-  ``chat.open_ai_chat_message.FunctionCall``

Example
-------

The following is an example demonstrating how to create an instance of
``OpenAIAutomataConversationDatabase`` and using its functionalities.

.. code:: python

   from automata.memory_store.conversation_database_providers import OpenAIAutomataConversationDatabase
   from chat.open_ai_chat_message import OpenAIChatMessage, FunctionCall

   # create conversation database
   db = OpenAIAutomataConversationDatabase(db_path="path/to/db")

   # create a message 
   message = OpenAIChatMessage(role="user", content="Hello, bot", function_call=FunctionCall(function_name="Hello", kwargs={}))

   # save the message in session
   db.save_message(session_id= "session1", message= message)

   # get all the messages in the session
   messages_in_session = db.get_messages(session_id="session1")

Limitations
-----------

In its current form, the ``OpenAIAutomataConversationDatabase`` relies
heavily on proper usage of session IDs, and as such, any mistakes with
session IDs can lead to errors. There is also a ‘TODO’ in the method
save_message and get_messages.

Follow-up Questions:
--------------------

-  Can we provide different implementations of the ``save_message`` and
   ``get_messages`` methods in order to handle any form of session IDs?
-  Can potential scaling issues be avoided? For example, if a session
   has a very large number of messages, it could impact the retrieval
   speed or memory usage.
-  How do we handle different types of messages that aren’t just
   ``OpenAIChatMessage``? The ``save_message`` and ``get_messages``
   methods currently expect this type of message.
