Task
====

``Task`` is a generic task object used by the task executor in Automata.
It is responsible for storing the task id, priority, and maximum number
of retries. Additionally, Task provides methods to notify observers when
the task status changes and to generate deterministic task ids based on
the hashable kwargs.

Overview
--------

The ``Task`` class is an abstract base class that provides essential
methods and attributes to keep track of a task’s execution status,
retries, and priority. This class acts as a blueprint for creating
custom task objects suitable for the Automata framework.

``Task`` objects are responsible for: - Storing task id, priority, and
max retries - Generating deterministic task id based on the hash of the
hashable kwargs - Notifying observers when the task status changes

Related Symbols
---------------

-  ``automata.core.tasks.tasks.AutomataTask``
-  ``automata.core.tasks.base.ITaskExecution.execute``
-  ``automata.core.tasks.base.ITaskExecution``
-  ``automata.tests.unit.test_task_database.task``

Example
-------

The following is an example demonstrating how to create a custom
``Task`` object.

.. code:: python

   import uuid
   from automata.core.tasks.base import Task, TaskStatus

   class MyCustomTask(Task):
       def __init__(self, *args, **kwargs):
           super().__init__(*args, **kwargs)
           self.args = args
           self.kwargs = kwargs
           
   my_task = MyCustomTask(name="Example Task", priority=1, max_retries=2)
   print(my_task)  # Output: Task <UUID> (TaskStatus.CREATED)

Limitations
-----------

The ``Task`` class is an abstract base class, which means it cannot be
instantiated directly. Instead, you need to create a subclass of
``Task`` and customize it to suit your needs. Examples of such
subclasses include ``AutomataTask``.

Additionally, the default maximum number of retries might not be
suitable for all tasks. In scenarios where you might want more or fewer
retries for a task, it is necessary to customize the ``max_retries``
argument when instantiating the task object.

Follow-up Questions:
--------------------

-  How can we create and use custom task classes other than
   ``AutomataTask`` within the Automata framework?
