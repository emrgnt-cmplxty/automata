TaskStatus
==========

``TaskStatus`` is a crucial component of the ``Task`` object which
represents its current status or stage in the task management process.
This enum value is updated by the task executor as the task progresses
and changes state. Multiple states ``TaskStatus`` can represent include
``CREATED``, ``REGISTERED``, ``RETRYING``, ``SUCCESS`` and others.

Overview
--------

A ``Task`` object’s status is set initially to ``TaskStatus.CREATED``
and as the task is processed by the task executor or the automata
environment, its status gets updated to indicates its progress. Status
like ``RETRYING`` is used when a task failure occurs and a retry attempt
is being made, ``SUCCESS`` when the task completes successfully,
``REGISTERED`` when the task is registered into the system.

Related Symbols
---------------

-  ``automata.tests.unit.test_task.test_status_setter``
-  ``automata.tests.unit.test_task.test_task_inital_state``
-  ``automata.core.tasks.base.Task.status``
-  ``automata.tests.unit.test_task_database.test_update_task``
-  ``automata.core.tasks.base.Task``
-  ``automata.tests.unit.test_task_database.test_database_lifecycle``
-  ``automata.core.tasks.tasks.AutomataTask``
-  ``automata.tests.unit.test_task.test_register_task``

Example
-------

The following is an example demonstrating how to set and change the
status of a ``Task``.

.. code:: python

   from automata.core.tasks.base import Task
   from automata.core.tasks.base import TaskStatus

   task = Task("Task1", "", priority=1)
   print(task.status)  # Should print: TaskStatus.CREATED

   task.status = TaskStatus.REGISTERED
   print(task.status)  # Should print: TaskStatus.REGISTERED

   task.status = TaskStatus.SUCCESS
   print(task.status)  # Should print: TaskStatus.SUCCESS

Limitations
-----------

There are no known limitations for ``TaskStatus``. It represents the
state of a task as it is processed, and has enough values to represent
important stages in a task’s lifecycle.

Follow-up Questions:
--------------------

-  What are the exact definitions and implications of each
   ``TaskStatus``?
-  Are there any considerations if new status values need to be added to
   ``TaskStatus`` in the future?
-  How are status transitions managed, ensuring a task status can’t
   directly jump between non-sequential states (like from ``CREATED`` to
   ``SUCCESS``)? (Note: Unit tests are often setup using ``mock``
   objects for complex operations like database interactions, network
   calls etc. In some examples, these mocks are swapped with actual
   objects as far as possible.)
