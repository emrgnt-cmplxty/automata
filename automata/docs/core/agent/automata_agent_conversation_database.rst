AutomataAgentConversationDatabase
=================================

``AutomataAgentConversationDatabase`` is a class that provides a
database for managing the conversations of Automata agents. It allows
for storing, retrieving, and managing messages in a conversation, with
the ability to access all messages for a specific session. The class
also supports metadata interactions and database access to various
related symbols.

Overview
--------

``AutomataAgentConversationDatabase`` is an essential component for
utilizing Automata agents, as it allows storing and managing
conversation histories for each session. Using this class, agents can
effectively reference conversation histories to provide responses in a
multi-turn interaction context. The class offers methods for saving and
retrieving messages from a session, along with metadata interactions to
handle session management.

Related Symbols
---------------

-  ``automata.core.agent.agents.AutomataOpenAIAgent``
-  ``automata.core.llm.completion.LLMChatMessage``
-  ``automata.core.llm.completion.LLMConversationDatabaseProvider``
-  ``automata.core.base.database.relational.SQLDatabase``

Example
-------

The following example demonstrates how to create an
``AutomataAgentConversationDatabase`` instance and use it to manage
messages.

.. code:: python

   from automata.core.agent.conversation_database import AutomataAgentConversationDatabase
   from automata.core.llm.completion import LLMChatMessage

   # Create a new AutomataAgentConversationDatabase instance
   db = AutomataAgentConversationDatabase(session_id="my_session")

   # Save a message in the database
   message = LLMChatMessage(role="user", content="Hello, what is your name?")
   db.save_message(message)

   # Retrieve messages from the database
   messages = db.get_messages()
   print(messages)

Limitations
-----------

The primary limitation of ``AutomataAgentConversationDatabase`` is that
the database implementation is currently limited to a local SQL
database. As a result, it might not be suitable for distributed systems
or high-scale applications without additional adjustments. Additionally,
its dependency on ``automata.config.CONVERSATION_DB_PATH`` may cause
issues if the directory structure or path is changed.

Follow-up Questions:
--------------------

-  Can we adapt ``AutomataAgentConversationDatabase`` to support other
   types of databases, such as NoSQL or distributed systems?
-  Are there any performance optimizations we can perform for
   large-scale applications or heavy load scenarios?
