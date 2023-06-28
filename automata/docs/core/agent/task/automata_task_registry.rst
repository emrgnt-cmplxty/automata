AutomataTaskRegistry
====================

``AutomataTaskRegistry`` is a class responsible for managing tasks in
Automata by storing and retrieving tasks in a given task database
(``AutomataTaskDatabase``). It provides methods that allow clients to
fetch tasks by ID, get all tasks, register new tasks, and update
existing tasks. AutomataTaskRegistry uses the AutomataTaskDatabase to
perform CRUD operations on tasks, ensuring proper interactions with the
underlying task storage.

Overview
--------

``AutomataTaskRegistry`` offers the following main methods:

-  ``__init__(self, db: AutomataTaskDatabase) -> None``: Initializes the
   registry and allows specifying a task database for managing tasks.
-  ``fetch_task_by_id(self, task_id: str) -> Optional[AutomataTask]``:
   Fetches a task from the database by its ID.
-  ``get_all_tasks(self) -> List[AutomataTask]``: Retrieves all tasks in
   the registry.
-  ``register(self, task: AutomataTask) -> None``: Adds a new task to
   the registry.
-  ``update_task(self, task: AutomataTask) -> None``: Updates a task in
   the registry.

Related Symbols
---------------

-  ``automata.core.agent.task.task.AutomataTask``
-  ``automata.config.TASK_DB_PATH``
-  ``automata.core.agent.error.AgentTaskGeneralError``
-  ``automata.core.agent.error.AgentTaskStateError``
-  ``automata.core.base.database.relational.SQLDatabase``
-  ``automata.core.base.task.TaskStatus``

Example
-------

Below is an example of how to use ``AutomataTaskRegistry`` for
registering a new task and retrieving tasks.

.. code:: python

   from automata.core.agent.task.registry import AutomataTaskRegistry
   from automata.core.agent.task.task import AutomataTask
   from automata.core.base.task import TaskStatus
   from automata.core.base.database.relational import SQLDatabase
   from automata.config import TASK_DB_PATH

   # Creating a new AutomataTask
   task = AutomataTask("test_task", instructions="sample_instructions")

   # Initializing the task database and registry
   task_db = SQLDatabase(db_path=TASK_DB_PATH)
   task_registry = AutomataTaskRegistry(db=task_db)

   # Registering the new task
   task_registry.register(task)
   assert task.status == TaskStatus.REGISTERED

   # Fetching the task by its ID
   task_fetched = task_registry.fetch_task_by_id(task.task_id)
   assert task_fetched == task

Limitations
-----------

There are a few limitations with the current ``AutomataTaskRegistry``
implementation:

-  It assumes that the tasks in the registry are always serialized and
   deserialized using ``jsonpickle``. This limits the choice of
   serialization libraries.
-  Error handling is minimal, and clients may need to implement
   additional error handling for specific use cases.

Follow-up Questions:
--------------------

-  Is there a way to support different serialization libraries in
   ``AutomataTaskRegistry``?
-  What improvements can be made in the error handling of
   ``AutomataTaskRegistry``?
