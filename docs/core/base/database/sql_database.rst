SQLDatabase
===========

``SQLDatabase`` is a concrete class that enables interaction with an
SQLite database. It encapsulates various common operations that one
needs to perform on a SQL database such as creation and deletion of
tables, data insertion, selection, and deletion as well as closing the
database connection.

Overview
--------

``SQLDatabase`` opens a connection to a SQLite database file and
provides a set of methods to execute SQL queries for Data Definition
Language (DDL) like ``create_table`` and Data Manipulation Language
(DML) like ``delete``, ``insert``, ``select``, and ``update_database``.

Import Statements
-----------------

.. code:: python

   import sqlite3
   from abc import ABC, abstractmethod
   from typing import Dict, List
   from automata.config import CONVERSATION_DB_PATH

Related Symbols
---------------

-  ``automata.tests.unit.test_task_database.db``
-  ``automata.tests.unit.test_conversation_database.db``
-  ``automata.core.tasks.agent_database.AutomataAgentTaskDatabase``
-  ``automata.core.base.database.relational.RelationalDatabase``
-  ``automata.core.memory_store.agent_conversation_database.AgentConversationDatabase``

Example
-------

This example demonstrates the way to use the ``SQLDatabase`` for
performing the basic SQL operations.

.. code:: python

   # Create instance of SQLDatabase
   database = SQLDatabase()

   # Connect to the SQLite database
   database.connect('example.db')

   # Create a table
   database.create_table('students', {'name': 'TEXT', 'age': 'INTEGER'})

   # Insert data into the table
   database.insert('students', {'name': 'John', 'age': 20})

   # Select data from the table
   data = database.select('students', ['name', 'age'])

   print(data)

   # Delete data from the table
   database.delete('students', {'name': 'John'})

   # Close the database connection
   database.close()

Limitations
-----------

The ``SQLDatabase`` class specifically designed for SQLite databases. It
is not explicitly designed to work with other types of SQL databases,
for example MySQL or PostgreSQL.

Follow-up Questions:
--------------------

-  Is ``SQLDatabase`` compatible with all versions of SQLite or only
   with particular ones?
-  How is exception handling managed in the ``SQLDatabase`` class?
-  Are there any plans to extend ``SQLDatabase`` class for compatibility
   with other types of SQL databases?

Notes
-----

-  Mock objects referenced in test files have been replaced with actual
   objects for this documentation.
-  Information provided for
   ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
   class has been excluded from this documentation, as it appears to be
   unrelated to the primary symbol. If this class is important to
   understanding ``SQLDatabase``, more context would be helpful.
