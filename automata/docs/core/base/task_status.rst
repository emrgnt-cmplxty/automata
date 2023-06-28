TaskStatus
==========

``TaskStatus`` is an enumeration used by the ``Task`` class to represent
the various stages a task can be in during its execution. Task statuses
include ``CREATED``, ``REGISTERED``, ``RUNNING``, ``RETRYING``,
``SUCCESS``, and ``FAILED``. The task executor updates the status of the
task as it progresses through different stages of execution.

Related Symbols
---------------

-  ``automata.core.base.task.Task``
-  ``automata.core.agent.task.task.AutomataTask``
-  ``automata.tests.unit.test_task``

Example
-------

The following example demonstrates how to use ``TaskStatus`` with an
``AutomataTask`` and check or update its status.

.. code:: python

   from automata.core.agent.task.task import AutomataTask
   from automata.core.base.task import TaskStatus

   task = AutomataTask(instructions="example_instructions")
   print("Task initial status:", task.status)

   task.status = TaskStatus.REGISTERED
   print("Task status after registration:", task.status)

Limitations
-----------

The ``TaskStatus`` enumeration is primarily used within the task
executor and not intended for direct manipulation by users. Changing the
task status manually may lead to unintended consequences or inconsistent
task states during execution.

Follow-up Questions:
--------------------

-  Are there any other TaskStatus values that could be added to better
   represent the different stages of task execution and aid in task
   management?
