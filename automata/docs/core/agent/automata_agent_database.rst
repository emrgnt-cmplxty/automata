AutomataAgentDatabase
=====================

``AutomataAgentDatabase`` is a class that helps manage the interactions
between an ``AutomataAgent`` and the SQLite database used to store
conversation history. This class provides methods to initialize the
database, get a list of previous conversations, and insert messages into
the database for a specific session.

Overview
--------

The main methods offered by the ``AutomataAgentDatabase`` class include:
- ``__del__``: Closes the connection to the agent database. -
``__init__``: Initializes a connection to the agent database using the
provided session ID. - ``get_conversations``: Loads previous
interactions from the database and populates the messages list. -
``put_message``: Inserts a message into the appropriate session and
interaction ID.

The ``AutomataAgentDatabase`` class is used in conjunction with the
``AutomataAgent`` class to store and retrieve conversation history for a
given session ID.

Related Symbols
---------------

-  ``automata.core.agent.database.AutomataAgentDatabase``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.tests.unit.test_automata_agent.test_save_and_load_interaction``
-  ``automata.core.base.openai.OpenAIChatMessage``

Example
-------

The following example demonstrates how to use ``AutomataAgentDatabase``
to save and retrieve messages in a conversation:

.. code:: python

   import sqlite3
   from uuid import uuid4
   from automata.core.agent.database import AutomataAgentDatabase

   # Create a new session ID
   session_id = str(uuid4())

   # Initialize the AutomataAgentDatabase with the session ID
   automata_agent_db = AutomataAgentDatabase(session_id=session_id)

   # Save a message to the database
   automata_agent_db.put_message("assistant", "Test message.", 1)

   # Load the conversation history
   messages = automata_agent_db.get_conversations()

   # Print the messages
   for message in messages:
       print(f"{message.role}: {message.content}")

Limitations
-----------

The ``AutomataAgentDatabase`` class uses SQLite as the database backend
to manage the interactions between the agent and database, which may not
be suitable for large-scale applications or highly concurrent
environments.

Follow-up Questions:
--------------------

-  Can the ``AutomataAgentDatabase`` class be easily adapted to use
   another database solution, like PostgreSQL or MySQL?
