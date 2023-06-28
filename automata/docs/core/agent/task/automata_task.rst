AutomataTask
============

``AutomataTask`` is a task object that is designed to be executed by the
``TaskExecutor``. It extends the ``Task`` class and includes a mandatory
``instructions`` attribute that stores the instructions for the task.
Additionally, it handles logging configurations and offers methods to
retrieve the logs associated with the task execution.

Overview
--------

``AutomataTask`` is responsible for initializing a task with
instructions, setting up logging configurations, and providing access to
the logs. Its primary use is to store the instructions and other
necessary information associated with a task. It relies on the ``Task``
base class for managing task-related properties like ``task_id``,
``priority``, ``max_retries``, and others. AutomataTask also initializes
the logging configurations and ensures the logs for the task can be
accessed after the task execution.

Related Symbols
---------------

-  ``automata.core.base.task.Task``
-  ``automata.core.agent.error.AgentTaskInstructions``
-  ``automata.core.utils.get_logging_config``
-  ``automata.core.utils.get_root_fpath``
-  ``automata.core.utils.get_root_py_fpath``

Example
-------

The following example demonstrates how to create an instance of
``AutomataTask`` with instructions and a default path to the root python
folder.

.. code:: python

   from automata.core.agent.task.task import AutomataTask

   instructions = "Perform text analysis and store the results."
   task = AutomataTask(instructions=instructions)

Limitations
-----------

``AutomataTask`` assumes that the Python folder is in the root folder.
It relies on this assumption to set the path to the root Python folder
if it is not provided.\ ``AutomataTask`` also depends on various helper
functions to properly initialize it, such as ``get_logging_config``,
``get_root_fpath``, and ``get_root_py_fpath``.

Follow-up Questions:
--------------------

-  Can ``AutomataTask`` be extended to allow custom paths for the Python
   folder?
