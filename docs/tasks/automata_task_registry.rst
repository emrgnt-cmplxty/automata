AutomataTaskRegistry
====================

Overview
--------

``AutomataTaskRegistry`` is a manager class that manages storing and
fetching tasks. It interacts with an instance of
``AutomataAgentTaskDatabase`` to fetch task by id, perform operations
like registering a task, getting all tasks, and updating a task in
registry. It also ensures that tasks are in the correct state to be
executed.

Related Symbols
---------------

-  ``AutomataAgentTaskDatabase``
-  ``AgentTaskGeneralError``
-  ``AgentTaskStateError``
-  ``TaskStatus``
-  ``AutomataTask``

Example
-------

.. code:: python

   from automata.tasks.agent_database import AutomataTaskRegistry
   from automata.tests.unit.test_task_database import task

   # Creating a task
   task = task()

   # Fetching a task using registry
   registry = AutomataTaskRegistry(db_path)
   fetched_task = registry.fetch_task_by_id(task.task_id)

   # Getting all tasks using registry
   all_tasks = registry.get_all_tasks()

   # Registering a task using registry
   registry.register(task)

   # Updating task using registry
   registry.update_task(task)

Note: We assume that ``db_path`` is a string indicating the correct path
to the task database.

Limitations
-----------

While ``AutomataTaskRegistry`` is capable of managing tasks, the user
must ensure that the tasks are in the correct state to be executed
(e.g., registered and not in a errored state). If a task is flagged as
errored, it would be necessary to manually change the task’s state.

Follow-up Questions:
--------------------

-  How should error-handling be incorporated during the task execution
   process to avoid corrupted or faulty tasks?
-  How should tasks be retrieved if a faulty task has been inserted into
   the database?
