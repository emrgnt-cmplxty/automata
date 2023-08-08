Task
====

``Task`` is a generic object used by ``TaskExecutor``. It is responsible
for storing relevant task details such as the task id, priority level,
and maximum retries. The ``Task`` class also provides parameters to
receive arguments and keyword arguments which are then passed to the
task function when the task is executed. Additionally, it includes a
method to generate a deterministic task id based on a hash of the
hashable keyword arguments.

Overview
--------

The ``Task`` class is initiated with optional keyword arguments for task
priority and maximum retries, defaulting to 0 and 3 respectively.
Optional ``generate_deterministic_id`` keyword argument can also be
provided to generate deterministic task id based on the hash of hashable
kwargs.

Task status is handled through properties, allowing for the task’s
status to be updated as it moves through different stages of execution.

The ``Task`` object also includes support for logging, with
notifications system when task status is changed.

Related Symbols
---------------

-  ``TaskExecutor``
-  ``TaskStatus``

Usage Example
-------------

**Initialization**

.. code:: python

   from tasks.task_base import Task

   task = Task(priority=2, max_retries=5, generate_deterministic_id=True)

**Setting Status**

.. code:: python

   from tasks.task_base import Task, TaskStatus

   # Initialize a task
   task = Task(priority=2, max_retries=5)

   # Set status of the task
   task.status = TaskStatus.STARTED

Limitations
-----------

Task’s status cannot be set to ``RETRYING`` if the maximum number of
retries has been reached. In such cases, default status is ‘FAILED’.

Another limitation is the potential for collision if deterministic
session_ids are generated from identical sets of keyword arguments. This
could potentially overwrite previous task with the same derived task id.

Follow-up Questions:
--------------------

-  Is the ``retry_count`` field incremented when a task’s status is set
   to ``RETRYING``? What happens to this count when a task is successful
   or fails?
-  How are tasks with identical deterministic task ids handled? In the
   presence of such a scenario, will it lead to data loss by overwriting
   the existing task details with the new task details?
