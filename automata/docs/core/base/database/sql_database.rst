SQLDatabase
===========

``SQLDatabase`` is a concrete class that provides a simple interface to
interact with SQL databases. It provides methods to connect, create
tables, insert, update, delete, and select data from the database. The
class is derived from the ``RelationalDatabase`` abstract base class.

Overview
--------

``SQLDatabase`` allows for establishing a connection to an SQLite
database, and offers a set of CRUD (Create, Read, Update, and Delete)
operations for working with the data. It simplifies the process of
interacting with SQL databases and can be used with predefined
configurations provided by the ``CONVERSATION_DB_PATH`` variable.

Related Symbols
---------------

-  ``automata.core.base.database.relational.RelationalDatabase``
-  ``automata.tests.unit.test_task_database.db``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.core.tasks.agent_database.AutomataAgentTaskDatabase``

Usage Example
-------------

The following example demonstrates how to work with an SQLDatabase.

.. code:: python

   from automata.core.base.database.relational import SQLDatabase
   from automata.config import CONVERSATION_DB_PATH

   db = SQLDatabase()
   db.connect(CONVERSATION_DB_PATH)

   table_name = "test_table"
   fields = {"id": "integer primary key", "name": "text", "age": "integer"}
   db.create_table(table_name, fields)

   data = {"id": 1, "name": "John Doe", "age": 30}
   db.insert(table_name, data)

   # Update
   updated_data = {"age": 31}
   conditions = {"id": 1, "name": "John Doe"}
   db.update(table_name, updated_data, conditions)

   # Select
   selected_data = db.select(table_name, ["name", "age"], conditions)
   print(selected_data)

   # Delete
   db.delete(table_name, conditions)

   db.close()

Limitations
-----------

The primary limitation of ``SQLDatabase`` is that it is focused on
SQLite and may not provide complete compatibility with other SQL
databases. In addition, it assumes a specific format for queries and
conditions, which may not cover all possible SQL query variations.

Follow-up Questions:
--------------------

-  Are there plans to extend the functionality of ``SQLDatabase`` to
   support other SQL databases?
-  What is the suggested approach for using complex conditions when
   working with this class?
