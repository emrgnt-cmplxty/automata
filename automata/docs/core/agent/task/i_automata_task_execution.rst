IAutomataTaskExecution
======================

``IAutomataTaskExecution`` is a class for executing general tasks using
the ``AutomataAgent``. It provides a method ``execute`` for executing a
given task and handling the retry count if the task fails during
execution.

Overview
--------

``IAutomataTaskExecution`` is designed to handle general tasks execution
with customizable retry counts if the task fails. It uses
``AutomataAgent`` for executing the task and managing the task’s status
such as running, success, or failure. This enables the system to keep
track of how the task is progressing during its execution and manage the
task accordingly.

Related Symbols
---------------

-  ``automata.core.tasks.base.Task``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.core.tasks.tasks.AutomataTask``
-  ``automata.core.agent.error.AgentTaskGeneralError``
-  ``automata.core.tasks.executor.AutomataTaskExecutor``
-  ``automata.core.tasks.base.TaskStatus``

Example
-------

The following example demonstrates how to use ``IAutomataTaskExecution``
to execute a task and handle retries.

.. code:: python

   import time
   from automata.core.tasks.executor import IAutomataTaskExecution
   from automata.core.tasks.tasks import AutomataTask
   from automata.core.tasks.base import TaskStatus

   task = AutomataTask("test_task", instructions="Run test instructions")
   execution = IAutomataTaskExecution()

   while task.status != TaskStatus.SUCCESS:
       try:
           execution.execute(task)
           print(f"Task {task.task_id} succeeded")
       except Exception as e:
           if task.retry_count < task.max_retries:
               print(f"Task {task.task_id} failed. Retrying...")
               time.sleep(1)  # Add delay if needed
           else:
               print(f"Task {task.task_id} failed after {task.retry_count} retries")
               break

Limitations
-----------

The primary limitation of ``IAutomataTaskExecution`` is that it assumes
the task to be executed is an instance of ``AutomataTask``. If a
different task type is required, the implementation of the ``execute``
method should be modified accordingly.

Follow-up Questions:
--------------------

-  How can we make ``IAutomataTaskExecution`` more generic to handle
   different task types?
-  Are there any edge cases or potential issues with the provided
   example?
