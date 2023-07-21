RelationalDatabase
==================

``RelationalDatabase`` is an abstract base class for different types of
relational databases. The class definition includes several abstract
methods intended to be overridden by the subclasses. These methods
primarily facilitate core database operations.

Overview
--------

``RelationalDatabase`` provides a pattern for designing various types of
relational databases. It contains abstract methods that outline the
fundamental operations of a relational database. These operations
contain connecting, closing, creating tables on the database, and the
CRUD (Create, Read, Update, Delete) operation methods which are
``insert``, ``select``, ``update_database`` and ``delete``.

Related Symbols
---------------

-  ``automata.tests.unit.test_task_database.db``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.core.base.database.relational.SQLDatabase``
-  ``automata.tests.unit.test_task_database.test_database_lifecycle``
-  ``automata.llm.foundation.LLMConversationDatabaseProvider``
-  ``automata.tests.unit.test_conversation_database.test_get_get_last_interaction_id_when_no_interactions``
-  ``automata.tasks.agent_database.AutomataAgentTaskDatabase``
-  ``automata.tests.unit.test_task_database.test_get_tasks_by_query``
-  ``automata.memory_store.agent_conversation_database.AgentConversationDatabase``
-  ``automata.tests.unit.test_task_database.test_contains``

Example
-------

Due to its abstract nature, ``RelationalDatabase`` cannot be
instantiated. However, subsequent code shows an example of a concrete
subclass ``SQLDatabase`` which inherits from this class:

.. code:: python

   from automata.core.base.database.relational import SQLDatabase

   db_instance = SQLDatabase()
   db_instance.connect('path/to/database.db')
   db_instance.create_table('test_table', {'id': int, 'name': str, 'email': str})
   db_instance.insert('test_table', {'id': 1, 'name': 'Test', 'email': 'test@email.com'})
   data = db_instance.select('test_table', ['id', 'name', 'email'], {'id': 1})
   print(data)
   db_instance.close()

Limitations
-----------

The ``RelationalDatabase`` class is abstract and cannot be used directly
to create a database. It is intended to serve as a base class to be
subclassed by classes that implement specific databases.

Follow-up Questions:
--------------------

-  What specific databases are implemented from this abstract bases
   class?
-  How does the implementation vary from different subclasses of this
   abstract class?
