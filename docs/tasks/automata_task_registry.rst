AutomataTaskRegistry
====================

``AutomataTaskRegistry`` is a class that manages the storage and
retrieval of tasks. Each task is stored with a ``session_id`` that
uniquely identifies it and their status are updated in the registry.

Overview
--------

``AutomataTaskRegistry`` interacts with the
``AutomataAgentTaskDatabase`` to interact with stored tasks. It offers
methods to register tasks, update tasks, fetch tasks by their session id
and get all tasks in the registry. Each task must be in the ``CREATED``
status to be registered, and an exception is raised if a task is
attempted to be registered again or if it doesn’t exist in the registry.

Related Symbols
---------------

-  ``automata.tasks.task_registry.AutomataTask``
-  ``automata.tasks.task_registry.AutomataAgentTaskDatabase``
-  ``automata.tasks.task_registry.TaskStatus``

Example
-------

The following is an example demonstrating how to register a new task to
the ``AutomataTaskRegistry``:

.. code:: python

   from automata.tasks.task_registry import AutomataTaskRegistry, AutomataTask, AutomataAgentTaskDatabase, TaskStatus

   db = AutomataAgentTaskDatabase()
   registry = AutomataTaskRegistry(db)

   task = AutomataTask("session_id_1", "task_name", TaskStatus.CREATED)
   registry.register(task)

Limitations
-----------

The ``AutomataTaskRegistry`` class assumes each ``AutomataTask`` has a
unique ``session_id``. Fetching a task by ``session_id`` will raise an
exception if multiple tasks with the same ``session_id`` are found.
Also, it can only handle ``AutomataTask`` and not any other type of
tasks.

Follow-up Questions:
--------------------

-  Robust error handling and clear error messages if a task doesn’t
   exist in the database, or if multiple tasks with the same
   ``session_id`` are found.
-  Could ``AutomataTaskRegistry`` be extended to support other types of
   tasks, not just ``AutomataTask``?
-  How are tasks removed or dequeued from the registry once they’ve been
   completed?
