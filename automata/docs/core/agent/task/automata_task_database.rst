AutomataTaskDatabase
====================

``AutomataTaskDatabase`` is a database that provides a local store for
all tasks. It contains methods for inserting, updating, and querying
tasks within the database, interacting with the ``AutomataTask`` class
objects to perform various operations related to tasks. The connection
to the database is established using the ``SQLDatabase`` class which
provides a SQL interface for these operations.

Overview
--------

``AutomataTaskDatabase`` prioritizes tasks handling by offering methods
that allow users to check the existence of a task in the database, get
tasks by specified queries, insert new tasks, and update existing tasks.
The class utilizes ``jsonpickle`` for encoding and decoding tasks in
JSON format.

Related Symbols
---------------

-  ``automata.core.agent.task.task.AutomataTask``
-  ``automata.core.base.database.relational.SQLDatabase``
-  ``automata.tests.unit.test_task_database.db``
-  ``automata.core.agent.task.registry.AutomataTaskRegistry``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataTaskDatabase``, insert a task, and check if it exists in the
database.

.. code:: python

   from automata.config import TASK_DB_PATH
   from automata.core.agent.task.registry import AutomataTaskDatabase
   from automata.core.agent.task.task import AutomataTask

   # Create an instance of AutomataTaskDatabase
   task_db = AutomataTaskDatabase(db_path=TASK_DB_PATH)

   # Create a task
   task = AutomataTask("task1", instructions="instruction1")

   # Insert the task into the database
   task_db.insert_task(task)

   # Check if the task exists in the database
   task_exists = task_db.contains(task)
   print(task_exists)  # Output: True

Limitations
-----------

``AutomataTaskDatabase`` assumes a specific table structure in the
database and relies on JSON encoding/decoding for task storage. Custom
configurations or alternative storage methods for tasks are not
supported.

Follow-up Questions:
--------------------

-  Is there a way to support custom database table structures or
   alternative storage methods for tasks?
