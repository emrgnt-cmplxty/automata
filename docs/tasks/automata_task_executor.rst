AutomataTaskExecutor
====================

``AutomataTaskExecutor`` is the module in charge of managing the
execution of tasks in a given automata. The class takes a task with
behavior specified through an ``ITaskExecution`` interface and performs
the task, handling retries on failure, status tracking, and error
logging.

It uses the exponential backoff algorithm to space out retries, doubling
the wait time with each failed attempt. This algorithm has proven vital
in networking related tasks, as it gives a system time to recover,
reducing the chances of a system being overwhelmed.

Overview
--------

``AutomataTaskExecutor`` manages task execution within an automata,
ensuring that tasks that fail are retried until a maximum number of
attempts are reached. The class provides an ``execute`` method that
handles the main task execution, thoroughly logging each step of the
process. The method checks the task’s status, executes it, logs status
updates, and retries if necessary based on the task’s own max retries
setting.

The ``AutomataTaskExecutor`` class communicates task status updates
throughout the execution process, changing the task status from
``PENDING`` to ``RUNNING``, then to ``SUCCESS`` or ``RETRYING`` as
appropriate. If the task fails and retries are exhausted, an exception
is propagated upwards.

Related Symbols
---------------

-  ``automata.tasks.task.ITaskExecution``
-  ``automata.tasks.task.AutomataTask``
-  ``automata.tasks.task_status.TaskStatus``
-  ``automata.tasks.task_state_error.TaskStateError``

Usage Example
-------------

.. code:: python

   from automata.tasks.task_executor import AutomataTaskExecutor
   from automata.tasks.ITaskExecution import ITaskExecution
   from automata.tasks.task import AutomataTask
   from automata.tasks.task_status import TaskStatus

   # Define your ITaskExecution behavior
   class CustomTaskExecution(ITaskExecution):
       def execute(self, task: AutomataTask) -> any:
           # Place your execution logic here.
           return "Custom Task Execution Result"

   # Create your AutomataTask
   task = AutomataTask(id='TASK-1', session_id='SESS-1', status=TaskStatus.PENDING)

   # Pass the task object and execution behavior to AutomataTaskExecutor
   task_executor = AutomataTaskExecutor(execution=CustomTaskExecution())
   result = task_executor.execute(task)

   print(result)  # Outputs: Custom Task Execution Result

Limitations
-----------

The ``AutomataTaskExecutor`` will only run tasks with the ``PENDING``
status. When a task status is not ``PENDING``, the execution raises a
``TaskStateError``. It also does not handle side effects of failure
related to external systems used in the task execution code provided
through the ``ITaskExecution`` interface.

Follow-up Questions:
--------------------

-  Can the ``AutomataTaskExecutor`` be improved to handle the status of
   tasks in other stages and states?
-  How might we handle side effects of task failures within the
   ``AutomataTaskExecutor`` system?
-  How can we customize the behavior of the exponential backoff
   algorithm based on specific task characteristics or conditions?
