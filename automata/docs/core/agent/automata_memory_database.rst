AutomataMemoryDatabase
======================

``AutomataMemoryDatabase`` is a class that manages the storage of
conversational interactions in an SQLite database. This class provides a
simple interface for interacting with the conversation database,
allowing users to get and put messages for a specific session.

Related Symbols
---------------

-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``automata.core.database.vector.JSONEmbeddingVectorDatabase``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.code_handling.py_coding.writer.PyCodeWriter``
-  ``automata.core.code_handling.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.tools.tool.Tool``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.base.openai.OpenAIChatMessage``

Import Statements
-----------------

.. code:: python

   import sqlite3
   from typing import List
   from automata.core.base.openai import OpenAIChatMessage
   from config import CONVERSATION_DB_PATH

Example
-------

The following example demonstrates how to create an instance of
``AutomataMemoryDatabase``, put a message, and get the conversation
history:

.. code:: python

   from automata.core.agent.memories import AutomataMemoryDatabase

   # Initialize the memory database with a specific session ID
   session_id = "12345"
   memory_database = AutomataMemoryDatabase(session_id)

   # Put a message into the database
   role = "user"
   content = "Hello, how can I help you?"
   interaction_id = 1
   memory_database.put_message(role, content, interaction_id)

   # Get conversation history
   conversation_history = memory_database.get_conversations()
   print(conversation_history)

Limitations
-----------

The ``AutomataMemoryDatabase`` relies on ``CONVERSATION_DB_PATH`` for
the SQLite database location, which may not be ideal in some use cases.
Users cannot provide custom database file paths. The class also assumes
a specific schema for the interaction database, which may be inflexible
for specific requirements.

Follow-up Questions:
--------------------

-  How can we allow users to provide custom SQLite database file paths
   to ``AutomataMemoryDatabase``?
