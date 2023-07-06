AutomataAgentTaskDatabase
=========================

``AutomataAgentTaskDatabase`` is a class that provides the ability to
manage tasks in a local storage database.

Overview
--------

The ``AutomataAgentTaskDatabase`` class, inherited from ``SQLDatabase``,
serves as a local storage for all ``AutomataTask`` objects. It features
functionality to check if a particular task exists in the database,
retrieve tasks based on a given query, insert new tasks, and update
existing tasks.

Related Symbols
---------------

-  ``automata.tests.unit.test_task_database.db``
-  ``automata.tests.conftest.task``
-  ``automata.core.tasks.agent_database.AutomataTaskRegistry.__init__``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.core.tasks.agent_database.AutomataTaskRegistry``
-  ``automata.tests.unit.test_task.test_deterministic_task_id``
-  ``automata.core.memory_store.agent_conversation_database.AgentConversationDatabase``
-  ``automata.tests.unit.test_task_database.task``
-  ``automata.core.tasks.tasks.AutomataTask``
-  ``automata.tests.unit.test_conversation_database.db``

Method Details
--------------

\__init\_\_(db_path: str = TASK_DB_PATH)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Connects to the SQL database at the provided database path.
-  Creates a new table, if not existing, with a defined schema in the
   connected database.

contains(task: AutomataTask) -> bool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Checks if the task exists in the database.
-  Returns ``True`` if the task exists, otherwise ``False``.

get_tasks_by_query(query: str, params: Tuple = ()) -> List[AutomataTask]
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Retrieves list of tasks by applying the specified SQL query.
-  Returns a list of ``AutomataTask`` objects.

insert_task(task: AutomataTask) -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Inserts a new task into the database.

update_task(task: AutomataTask) -> None
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Updates an existing task in the database.

Example
-------

This Python library does not provide direct examples of
``AutomataAgentTaskDatabase`` usage. However, the usage of this class is
indirectly shown through its use in test fixtures and various other
parts of the code. Here is a constructed example demonstrating a basic
usage:

.. code:: python

   from automata.core.tasks.agent_database import AutomataAgentTaskDatabase
   from automata.core.tasks.tasks import AutomataTask

   # Instantiate AutomataTask
   task = AutomataTask(
       repo_manager=None,
       config_to_load="TEST",
       generate_deterministic_id=False,
       instructions="This is a test."
   )

   # Initialize Task Database
   db = AutomataAgentTaskDatabase()

   # Insert task
   db.insert_task(task)

   # Verify insertion
   assert db.contains(task) == True

Limitations
-----------

The primary limitation of ``AutomataAgentTaskDatabase`` is that it is
reliant on the ``AutomataTask`` object structure. Any changes in the
``AutomataTask`` definition may require changes in this class.

Also, operations like getting tasks by query may fail in complex
scenarios due to data serialization. A more robust error checking
mechanism might be required.

Follow-up Questions:
--------------------

-  It would be beneficial to provide a mechanism to delete tasks from
   the database, is there a plan for this feature?
-  Handling the exception in ``get_tasks_by_query`` function currently
   only logs the error. Would it make sense to propagate the error to
   the caller?
