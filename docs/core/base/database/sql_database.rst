SQLDatabase
===========

Overview
--------

``SQLDatabase`` is a concrete implementation class derived from
``RelationalDatabase`` to manage operations with SQLite databases. It
abstracts basic operations like creating a table, inserting data into a
table, selecting data from a table, updating an entry in a table and
deleting data from a table. Two important utilities
i.e. ``NullConnection`` and ``NullCursor`` are used to represent null
database connection and cursor respectively.

Related Symbols
---------------

-  ``sqlite3.Connection, sqlite3.Cursor``
-  ``automata.core.base.database.relational_database.RelationalDatabase``
   - The base class of ``SQLDatabase``.

Example
-------

This example demonstrates creating an SQLite Database and performing
simple operations like creating a table, inserting and selecting data.

.. code:: python

   from automata.core.base.database.relational_database import SQLDatabase

   # Initialize SQLDatabase Object
   database = SQLDatabase()

   # Connect to Database
   database.connect(db_path="my_database.sqlite3")

   # Define Table Name and Fields
   table_name = "Employees"
   fields = {
       "ID": "INTEGER PRIMARY KEY",
       "NAME": "TEXT",
       "AGE": "INT",
       "ADDRESS": "CHAR(50)",
       "SALARY": "REAL"
   }

   # Create new table
   database.create_table(table_name, fields)

   # Insert data
   data = {
       "NAME": "Paul",
       "AGE": 32,
       "ADDRESS": "California",
       "SALARY": 20000.00
   }
   database.insert(table_name, data)

   # Select data
   fields = ["NAME", "AGE"]
   conditions = {"AGE": 32}
   employees = database.select(table_name, fields, conditions)

   # Update data
   data = {"SALARY": 25000.00}
   conditions = {"NAME": "Paul"}
   database.update_entry(table_name, data, conditions)

   # Close the database connection
   database.close()

Please ensure that the file path and data used are modified as per your
system and needs.

Limitations
-----------

-  The ``SQLDatabase`` class is designed specifically to work with
   SQLite databases and hence may not be compatible with other types of
   SQL databases like MySQL, PostgreSQL, etc.
-  The ``commit`` method of ``NullConnection`` and ``execute``,
   ``fetchall`` methods of ``NullCursor`` raise ``NotImplementedError``.
   These classes serve as placeholders for null connection and cursor
   and not expected to have these methods operational.

Follow-up Questions:
--------------------

-  Does the SQLDatabase support different type of SQL databases other
   than SQLite?
-  Can SQLDatabase handle composite primary keys while creating tables?
-  How does SQLDatabase handle SQL injection attacks in its current
   form?
