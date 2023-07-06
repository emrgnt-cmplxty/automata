AutomataTaskExecutor
====================

``AutomataTaskExecutor`` is a class that adopts ``ITaskExecution``
behavior for executing an ``AutomataTask``. It executes the task
following the behavior specified in the execution instance provided
during the initialization of ``AutomataTaskExecutor``. The task
execution can go through multiple stages with different ``TaskStatus``
such as ``PENDING``, ``RUNNING``, ``SUCCESS``, etc. If a task fails and
does not exceed the maximum retries, it will be retried after a period
of ‘exponential backoff’ time.

Overview
--------

AutomataTaskExecutor is intended to execute an ``AutomataTask``
following the ``ITaskExecution`` interface standards. The execution of
the task is carried out by the ``execute`` method of the task execution
instance, which raises exceptions if the task is not in the ``PENDING``
status or if the task fails exceeding the maximum retries.

Related Symbols
---------------

-  ``ITaskExecution``
-  ``TaskStatus``
-  ``AutomataTask``
-  ``AutomataTaskEnvironment``
-  ``AutomataTaskRegistry``

Example
-------

The following is an example demonstrating how to use
``AutomataTaskExecutor`` to execute an ``AutomataTask``.

.. code:: python

   from automata.core.tasks.executor import AutomataTaskExecutor
   from automata.core.tasks.tasks import AutomataTask
   from automata.tests.unit.test_task_executor import TestExecuteBehavior

   # Create an AutomataTask instance
   my_task = AutomataTask(
       title="Task 1",
       instructions="Perform task 1",
       max_retries=5
   )

   # Create a TestExecuteBehavior instance
   test_execution_behavior = TestExecuteBehavior()

   # Create an AutomataTaskExecutor instance
   task_executor = AutomataTaskExecutor(test_execution_behavior)

   # Execute the task
   task_executor.execute(my_task)

This will execute the ``AutomataTask`` with the behavior specified in
``TestExecuteBehavior``.

Limitations
-----------

``AutomataTaskExecutor`` relies heavily on the provided
``ITaskExecution`` behavior passed during its instantiation. If the
execution behavior doesn’t correctly implement the ``execute`` method,
the task execution might not work as intended.

``AutomataTaskExecutor`` also requires the task to be in a ``PENDING``
status to be successfully executed. Therefore, tasks that aren’t in the
``PENDING`` status would require explicit modification before the
execution.

Follow-up Questions:
--------------------

-  How do we handle exceptions raised by other parts of the
   ``ITaskExecution`` process?
-  Are there specific rules for exponential backoff time?
-  Can tasks in other states (like ``SUCCESS``, ``FAILED``, etc.) be
   re-executed?
