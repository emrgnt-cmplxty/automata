RelationalDatabase
==================

``RelationalDatabase`` is an abstract base class for different types of
relational databases. It provides an interface for creating tables,
connecting to databases, inserting, updating, selecting, and deleting
data with the help of abstract methods.

Overview
--------

The ``RelationalDatabase`` class acts as an interface for various types
of relational databases and offers a uniform way of interacting with
different database technologies like SQLite, MySQL, and PostgreSQL.
Implementing the ``RelationalDatabase`` class requires overriding the
abstract methods to provide a concrete implementation for interacting
with the database of choice.

Related Symbols
---------------

-  ``automata.core.base.database.relational.SQLDatabase``
-  ``automata.tests.unit.test_task_database.db``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.core.tasks.agent_database.AutomataAgentTaskDatabase``
-  ``automata.core.llm.foundation.LLMConversationDatabaseProvider``

Example
-------

Suppose we want to implement a SQLite-based storage for tasks, we can
derive our class from ``RelationalDatabase``. Here’s a simple example:

.. code:: python

   import sqlite3
   from automata.core.base.database.relational import RelationalDatabase
   from typing import Dict, List

   class SQLiteTaskDatabase(RelationalDatabase):
       def connect(self, db_path: str):
           self.conn = sqlite3.connect(db_path)
           self.cursor = self.conn.cursor()

       def close(self):
           self.conn.close()

       def create_table(self, table_name: str, fields: Dict):
           field_list = ", ".join(
               [f"{field} {field_type}" for field, field_type in fields.items()]
           )
           self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {table_name} ({field_list})")
           self.conn.commit()

       # Implement other methods (insert, select, delete, update)

Limitations
-----------

The ``RelationalDatabase`` is an abstract class and does not provide any
concrete implementation. It needs to be subclassed, and the respective
methods must be implemented for the desired database technology. It
serves as an interface for different relational databases but cannot be
used directly.

Follow-up Questions:
--------------------

-  What are some recommended best practices for implementing the
   abstract methods in specialized classes for different database
   technologies?
-  Are there any specific performance concerns or recommendations when
   implementing these database classes?
