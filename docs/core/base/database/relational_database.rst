RelationalDatabase
==================

``RelationalDatabase`` serves as an abstract base class to represent
various types of relational databases. It organizes data into one or
more tables with designated fields.

Overview
--------

``RelationalDatabase`` primarily provides methods for basic database
operations such as connecting, closing the connection, creating tables,
inserting data, selecting data, updating entries, and deleting data.
Given its status as an abstract base class, it only defines the
interface for these operations. The implementation details must be
provided by concrete subclasses, such as an SQL database class that
implements these operations specific to SQL databases.

Related Symbols
---------------

-  ``automata.core.base.database.relational_database.SQLDatabase``: This
   is a concrete class that provides an SQL database. It inherits from
   ``RelationalDatabase`` and thus has the same methods, but with
   specific implementations for an SQL database.
-  ``automata.core.base.database.vector_database.VectorDatabaseProvider``:
   This is an abstract base class for different types of vector database
   providers.
-  ``automata.eval.agent.agent_eval_database.AgentEvalResultDatabase``:
   This class writes evaluation results to an SQLite database.

Example
-------

As ``RelationalDatabase`` is an abstract base class, below is an example
of a hypothetical subclass ``MySQLDatabase`` implementing the methods in
``RelationalDatabase``:

.. code:: python

   from automata.core.base.database.relational_database import RelationalDatabase

   class MySQLDatabase(RelationalDatabase):
     def connect(self, db_path):
       # implementation for MySQL connect
     
     def close(self):
       # implementation for MySQL close
     
     def create_table(self, table_name, fields):
       # implementation for MySQL create table
     
     def insert(self, table_name, data):
       # implementation for MySQL insert
     
     def select(self, table_name, fields, conditions):
       # implementation for MySQL select
     
     def update_entry(self, table_name, data, conditions):
       # implementation for MySQL update_entry
     
     def delete(self, table_name, conditions):
       # implementation for MySQL delete

You would use the subclass similarly to how you would use any class:

.. code:: python

   db = MySQLDatabase()
   db.connect("/path/to/db")
   db.create_table("MyTable", {"name": "VARCHAR(100)", "age": "INT"})
   db.insert("MyTable", {"name": "John Doe", "age": 30})
   results = db.select("MyTable", ["name"], {"age": 30})
   db.close()

Limitations
-----------

The ``RelationalDatabase`` class itself does not provide any actual
implementation details. Thus, instances of ``RelationalDatabase`` cannot
be directly used for operations. Also, any class that inherits from
``RelationalDatabase`` must provide concrete implementations for the
abstract methods defined in the ``RelationalDatabase`` class.

Follow-Up Questions:
--------------------

-  Are there default implementations for any of the methods defined in
   ``RelationalDatabase`` in common scenarios?
-  How does error handling work at this level? For example, what happens
   if one tries to select data from a table that does not exist?
-  What type of databases other than SQL might make use of the abstract
   ``RelationalDatabase`` class in a typical application’s use case?
