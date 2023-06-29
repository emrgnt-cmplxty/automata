LLMConversationDatabaseProvider
===============================

``LLMConversationDatabaseProvider`` is an abstract base class for
implementing different types of database providers to store and manage
conversation messages. The class defines the necessary methods such as
``get_messages()`` and ``save_message()``, which can be used by the
Automata Agent to interact with conversation databases.

Overview
--------

``LLMConversationDatabaseProvider`` provides a way to get and save
messages for an agent by implementing the required abstract methods in
its subclasses. It also allows observing conversation changes and
updating the database accordingly. The class is closely related to the
``AutomataAgentConversationDatabase`` implementation, which is a
specific implementation for Automata providers.

Related Symbols
---------------

-  ``automata.core.base.database.relational.SQLDatabase``
-  ``automata.core.llm.completion.LLMChatMessage``
-  ``automata.core.agent.conversation_database.AutomataAgentConversationDatabase``
-  ``automata.core.llm.completion.LLMConversation``

Example
-------

The following example demonstrates an example subclass of
``LLMConversationDatabaseProvider``:

.. code:: python

   from automata.core.llm.completion import LLMConversationDatabaseProvider, LLMChatMessage
   from automata.core.base.database.relational import SQLDatabase

   class CustomDatabaseProvider(LLMConversationDatabaseProvider, SQLDatabase):
       def __init__(self, session_id: str, db_path: str):
           super().__init__(session_id, db_path)

       def get_messages(self):
           # Implement the method to get all messages from the database
           pass

       def save_message(self, message: LLMChatMessage):
           # Implement the method to save a message to the database
           pass

Limitations
-----------

``LLMConversationDatabaseProvider`` is an abstract base class and cannot
be used directly. It must be subclassed with the implementation of its
abstract methods for a specific database type. Furthermore, it does not
provide reasoning or decision-making capabilities and should be used
solely as a means to store and manage conversation messages for the
providers.

Follow-up Questions:
--------------------

-  How can we better integrate database management within the existing
   framework of the Automata Agent?
-  Is there a need for other database types besides SQL?
