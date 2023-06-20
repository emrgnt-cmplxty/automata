AutomataAgentDatabase
=====================

``AutomataAgentDatabase`` is a class that manages the interactions
between an ``AutomataAgent`` and the SQLite database. It stores and
retrieves conversation data for a particular session, allowing
persistent storage of the agent’s interactions. The class’s primary
functionality includes initializing the database connection, retrieving
conversations, and inserting messages into the database.

Overview
--------

``AutomataAgentDatabase`` enables an ``AutomataAgent`` to use an SQLite
database to store and load interactions for a given session. The class
stores conversations as a list of ``OpenAIChatMessage`` objects, which
are then serialized and deserialized for database storage. It manages
the database connection and provides methods to interact with the
database, including inserting messages and retrieving agents’
conversations.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.openai.OpenAIChatMessage``
-  ``config.CONVERSATION_DB_PATH``

Example
-------

The following code snippet demonstrates how to create an instance of
``AutomataAgentDatabase`` and use it to store and load agent
interactions.

.. code:: python

   from automata.core.agent.database import AutomataAgentDatabase
   from automata.core.base.openai import OpenAIChatMessage

   session_id = "example_session_id"
   automata_agent_db = AutomataAgentDatabase(session_id=session_id)

   # Save a message to the database
   saved_message = automata_agent_db.put_message("assistant", "Test message.", 0)

   # Load messages from the database
   loaded_messages = automata_agent_db.get_conversations()

   assert len(loaded_messages) == 1
   assert isinstance(loaded_messages[0], OpenAIChatMessage)
   assert loaded_messages[0].role == "assistant"
   assert loaded_messages[0].content == "Test message."

Limitations
-----------

``AutomataAgentDatabase`` relies on SQLite for storage, which may not be
ideal for high-concurrency scenarios or where more advanced database
features are necessary.

Follow-up Questions:
--------------------

-  Are there plans to support other database systems besides SQLite?
