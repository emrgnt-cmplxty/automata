AgentConversationDatabase
=========================

Overview
--------

``AgentConversationDatabase`` is a class that manages the interactions
of a given conversation with the Automata agent. Its main
functionalities are connecting to the conversation database, creating
and managing the interaction’s table in the database, and saving,
retrieving and ordering the messages of a given conversation session.
This class inherits from the abstract base class
``LLMConversationDatabaseProvider`` and thus provides an implementation
for the methods ``get_messages`` and ``save_message``.

Related Symbols
---------------

-  ``automata.llm.providers.openai.OpenAIChatCompletionProvider.reset``
-  ``automata.config.CONVERSATION_DB_PATH``
-  ``automata.core.base.database.relational.SQLDatabase.connect``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.tests.unit.test_conversation_database.test_get_messages_returns_all_messages_for_session``
-  ``automata.tests.unit.test_conversation_database.test_put_message_increments_interaction_id``
-  ``automata.llm.foundation.LLMConversationDatabaseProvider.get_messages``
-  ``automata.llm.foundation.LLMConversationDatabaseProvider.save_message``
-  ``automata.agent.providers.OpenAIAutomataAgent.set_database_provider``

Example
-------

The following is an example demonstrating how to create an instance of
``AgentConversationDatabase``, save a message and then retrieve it.

.. code:: python

   from automata.memory_store.agent_conversation_database import AgentConversationDatabase
   from automata.llm.foundation import LLMChatMessage

   # Initialize a database path and session id
   db_path = 'path/to/db'
   session_id = 'a_unique_session_id'

   # Create an instance of AgentConversationDatabase
   db = AgentConversationDatabase(session_id, db_path)

   # Create a message
   message = LLMChatMessage(role='system', content='Hello, world!')

   # Save the message to the database
   db.save_message(message)

   # Retrieve all messages from the database
   messages = db.get_messages()

In this example, the ‘messages’ object should now contain the previously
saved LLMChatMessage.

Limitations
-----------

One of the limitations of ``AgentConversationDatabase`` is it’s heavily
reliant on the underlying SQL database implementation, thus requiring
careful handling of database connections and queries to prevent
potential data corruption. The current implementation also lacks support
for efficiently handling function call conversations, as stated in the
TODO comment found in the ``save_message`` method.

Certain aspects are pending improvements, including additional testing
around the ``get_messages`` method and better handling of function calls
in ``save_message``. This is evidenced by the presence of “TODO”
comments in the codebase for this class.

Follow-up Questions:
--------------------

-  How can we expand the functionality to handle additional forms of
   conversation such as function calls more efficiently?
-  What kind of additional testing and validation is required around the
   ``get_messages`` method?
