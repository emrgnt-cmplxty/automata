AutomataAgentTaskDatabase
=========================

Overview
--------

``AutomataAgentTaskDatabase`` is an SQLDatabase subclass that offers a
persistent local store specifically designed for ``AutomataTask``
objects. It is designed to maintain all task-related information such as
the ``json`` representation of the task, the task’s ``instructions``,
and its ``status``. This database class helps in storing, updating, and
querying Automata tasks and ascertaining their existence in the
database.

Related Symbols
---------------

-  ``automata.tasks.task.AutomataTask``
-  ``config.database.SQLDatabase``

Usage Example
-------------

The following is an example demonstrating how to insert, update and
retrieve an AutomataTask from AutomataAgentTaskDatabase:

.. code:: python

   from automata.tasks.task import AutomataTask
   from automata.tasks.task_database import AutomataAgentTaskDatabase
   from automata.tasks.task_status import TaskStatus

   # Creating a task instance
   task = AutomataTask(session_id="1", instructions="Test Instructions", status=TaskStatus.INCOMPLETE)

   # Creating a database instance and inserting the task
   db_path = "tasks.db"
   task_db = AutomataAgentTaskDatabase(db_path)
   task_db.insert_task(task)

   # Make some modifications and update the task
   task.status = TaskStatus.DONE
   task_db.update_task(task)

   # Get tasks by a specific query
   task_list = task_db.get_tasks_by_query("WHERE status = ?", (TaskStatus.DONE.value,))

   # Check if task exists in database
   existence = task_db.contains(task)

   print(existence)  # Returns: True

This code segment consists of creating an instance of ``AutomataTask``,
creating an instance of ``AutomataAgentTaskDatabase``, and then
inserting the task into the database through ``insert_task()``. The task
status is then updated and reflected in the database using
``update_task()``. Tasks with a specific status are fetched using
``get_tasks_by_query()``. Finally, the presence of a task in the
database is confirmed using ``contains()``.

Limitations
-----------

The primary limitation of the ``AutomataAgentTaskDatabase`` is its
dependency on specific structured data. The ``AutomataTask`` objects
need to have a specific predefined structure, and data outside this
format cannot be correctly processed. Additionally, encoding and
decoding of tasks to and from ``json`` format relies on ``jsonpickle``,
which might produce ambiguity or data loss for overly complex or
unconventional data structures.

Follow-up Questions:
--------------------

-  How can the AutomataAgentTaskDatabase be made more generic to
   accommodate various data structures apart from ``AutomataTask``?
-  How can the error handling mechanism be improved for instances when
   decoding of tasks fail?
