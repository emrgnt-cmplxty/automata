AutomataTaskExecutor
====================

``AutomataTaskExecutor`` is a class for executing tasks using different
execution behaviors. It provides methods to execute an ``AutomataTask``
object with a specified execution behavior. The class requires an
instance of ``ITaskExecution`` to be passed during its instantiation,
which defines the execution behavior. ``AutomataTaskExecutor`` is mainly
responsible for handling task retries and switching their status during
execution.

Overview
--------

``AutomataTaskExecutor`` provides an easy way to execute tasks with
different behaviors and handling retries based on the ``max_retries``
attribute of the task. The class has two methods, ``__init__`` and
``execute``. The ``__init__`` method takes an instance of
``ITaskExecution`` as an argument, while the ``execute`` method is
responsible for executing the task using the provided execution
behavior. The class will automatically retry the task execution in case
of failure, up to the maximum number of retries specified in the task.

Related Symbols
---------------

-  ``automata.core.agent.task.task.AutomataTask``
-  ``automata.core.base.task.ITaskExecution``
-  ``automata.core.agent.task.executor.IAutomataTaskExecution``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataTaskExecutor`` and execute an ``AutomataTask`` using it.

.. code:: python

   from automata.core.agent.task.executor import AutomataTaskExecutor, ITaskExecution
   from automata.core.agent.task.task import AutomataTask

   # Define custom execution behavior by implementing ITaskExecution
   class CustomExecuteBehavior(ITaskExecution):
       def execute(self, task: AutomataTask) -> None:
           print("Custom execution logic for the task.")

   # Create AutomataTask instance
   task = AutomataTask(instructions="Do something.")

   # Create AutomataTaskExecutor instance with the custom execution behavior
   task_executor = AutomataTaskExecutor(execution=CustomExecuteBehavior())

   # Execute the task using the task_executor
   task_executor.execute(task)

Limitations
-----------

``AutomataTaskExecutor`` depends on the implementation of the
``ITaskExecution`` interface, which defines the execute method for
executing tasks. This requires the user to define custom execution
behaviors for their specific use cases. Additionally, the class assumes
that the task object passed to the ``execute`` method is an instance of
``AutomataTask`` and that it has the correct status of
``TaskStatus.PENDING``.

Follow-up Questions:
--------------------

-  How can we improve the flexibility of the ``AutomataTaskExecutor`` to
   handle other types of tasks besides ``AutomataTask``?
-  Is there a way to make ``AutomataTaskExecutor`` execute tasks in
   parallel or distributed across multiple systems?
