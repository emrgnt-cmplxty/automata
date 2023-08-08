AutomataTask
============

``AutomataTask`` is a class extended from ``Task`` that is executed by
``TaskExecutor``. This class represents a single auto-executable task
with a specific set of instructions. A task in this context is an
operation or series of operations packaged together for the
``TaskExecutor`` to execute and monitor. It also includes functionality
to initialize logging for the task and accumulate logs for the task’s
execution.

Overview
--------

An ``AutomataTask`` gets initialized with a set of arguments and keyword
arguments. Two critical keyword arguments that are necessary for task
initialization include ``instructions`` - the instructions for the task,
and ``path_to_root_py`` - the path to the root python folder. Provided
instructions cannot be empty; otherwise, it raises a
``TaskInstructionsError``. The Initialize logs and get logs methods are
used to configure logging for the task execution.

Related Symbols
---------------

-  ``automata.tasks.Task``
-  ``automata.tasks.TaskExecutor``
-  ``automata.errors.TaskInstructionsError``

Example
-------

The following example demonstrates how to create an instance of
``AutomataTask``.

.. code:: python

   from automata.tasks.automata_task import AutomataTask

   instructions = "These are the task instructions"
   path_to_root_py = "/path/to/root/python/directory"

   task = AutomataTask(instructions=instructions, path_to_root_py=path_to_root_py)

Limitations
-----------

The primary limitation of ``AutomataTask`` is that it heavily relies on
the arguments and keyword arguments provided during its instantiation.
If the keyword argument ``instructions`` is not provided or is empty, a
``TaskInstructionsError`` will be raised. Additionally, ``AutomataTask``
assumes the existence of a specific directory structure for logging.

Follow-up Questions:
--------------------

-  Can we include a validation method for arguments and keyword
   arguments necessary for the AutomataTask?
-  What happens when the path provided in ``path_to_root_py`` does not
   exist or is not accessible?
-  Is there a way to customise the logging path or log file from outside
   the class? Is it possible to decide not to log the task at all?
