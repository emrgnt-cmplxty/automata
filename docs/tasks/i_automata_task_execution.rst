IAutomataTaskExecution
======================

Overview
--------

``IAutomataTaskExecution`` is a class designed for executing general
tasks by creating and running an ``AutomataAgent``. It implements the
``execute`` method from the ``ITaskExecution`` interface, and is used to
manage the execution process of a given task, handle failures and update
task’s status.

Related Symbols
---------------

1. ``AutomataTask``: A task object that is consumed by the
   ``IAutomataTaskExecution`` for execution. ``AutomataTask`` is a form
   of ``Task`` which is built to be executed by ``TaskExecutor``.

2. ``OpenAIAutomataAgent``: An autonomous agent designed to execute
   instructions and report the results back to the main system. It
   communicates with the OpenAI API to generate responses based on given
   instructions.

3. ``TaskStatus``: Enum representing the status of a task (RUNNING,
   COMPLETED, ERROR, etc.) It is used by ``IAutomataTaskExecution`` to
   mark the status of the task at different stages of its execution.

4. ``AutomataTaskExecutor``: A class for using
   ``IAutomataTaskExecution`` behavior to execute a task. It essentially
   executes the ``AutomataTask`` with the given
   ``IAutomataTaskExecution`` implementation.

5. ``AgentTaskGeneralError``: An exception raised when a general error
   occurs during task execution.

Usage Example
-------------

.. code:: python

   from automata.tasks.executor import IAutomataTaskExecution
   from automata.tasks.tasks import AutomataTask

   # Construct an Automata Task
   task = AutomataTask(name="custom_task", instructions="execute something")

   # Instantiate IAutomataTaskExecution and execute task
   task_execution = IAutomataTaskExecution()
   task_execution.execute(task)

Discussion
----------

``IAutomataTaskExecution`` manages the execution of a given
``AutomataTask``. It attempts to run an ``OpenAIAutomataAgent`` with the
``AutomataTask``, updating the task’s status throughout the execution.
If the execution of the task fails, the task’s retry count is
incremented. Once the maximum number of retries is reached, the task is
then marked as failed.

When a task is passed to the ``execute`` method, an ``AutomataAgent`` is
built, and set to run the task. If the task execution succeeds, the
task’s status is set to ‘SUCCESS’ and the task’s result attribute is
populated by the result of the ``AutomataAgent`` run. If an exception
occurs, the task’s status is set to ‘FAILED’, its error attribute is
populated with the error message, its retry count incremented, and the
exception is raised.

It is important to note that ``IAutomataTaskExecution`` requires a
``AutomataTask``, if a different type is passed it will throw an
``AgentTaskGeneralError``.

Limitations
-----------

``IAutomataTaskExecution`` depends on ``AutomataTask`` class for tasks,
thus cannot consume tasks created by other types of ``Task`` classes. It
also depends heavily on ``OpenAIAutomataAgent`` for executing tasks,
providing limited flexibility for running tasks using different types of
agents.

Follow-up Questions:
--------------------

-  What happens when the ``AutomataTask`` execution continues to fail
   even after maximum retry attempts? Is there a system in place to
   handle this scenario?
-  How is the maximum retry count decided and can it be customized?
-  Can ``IAutomataTaskExecution`` support other types of tasks apart
   from ``AutomataTask`` in the future?
