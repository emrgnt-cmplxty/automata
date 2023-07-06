AutomataTask
============

``AutomataTask`` class is designed to be executed by the TaskExecutor.
The tasks initiated by this class are set up with instructions and a
path to a root python folder.

Overview
--------

``AutomataTask`` manages tasks to be executed by initializing its
properties and validating its instructions. It also manages the logging
for the task by creating a log file in the task directory and fetches
log content. The class utilizes parent class ``Task`` from
``automata.tasks.base`` to handle the underlying procedures.

Related Symbols
---------------

-  ``automata.tasks.environment.AutomataTaskEnvironment``
-  ``automata.tasks.agent_database.AutomataTaskRegistry.get_all_tasks``
-  ``automata.tasks.agent_database.AutomataAgentTaskDatabase.insert_task``
-  ``automata.tasks.executor.IAutomataTaskExecution``

Example
-------

Examples on how to create instances of ``AutomataTask``:

.. code:: python

   from automata.tasks.tasks import AutomataTask

   task = AutomataTask("task1", instructions="instruction1")

.. code:: python

   from automata.tasks.tasks import AutomataTask
   from tests.mocks import MockRepositoryClient
   from config.config_enums import AgentConfigName

   repo_manager = MockRepositoryClient()

   task = AutomataTask(
       repo_manager,
       config_to_load=AgentConfigName.TEST.value,
       generate_deterministic_id=False,
       instructions="This is a test.",
   )

Limitations
-----------

``task_id`` generated here can take either a deterministic form based on
the hash of hashable keyword arguments or a random ``uuid`` depending on
the ``generate_deterministic_id`` flag. There’s no way to provide a
custom method of generating task_id.

``AutomataTask`` assumes the python folder is in the root folder, which
can limit the extraction of python files if the directory structure
changes.

Follow-up Questions
-------------------

-  Can a custom task_id generation method be facilitated?
-  Can the assumption of the python folder being in the root folder be
   eliminated, making it more robust?
