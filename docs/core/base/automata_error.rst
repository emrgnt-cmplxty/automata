AutomataError
=============

Overview
--------

``AutomataError`` is an essential base class for all exceptions defined
in the Automata framework. It inherits directly from Python’s built-in
``Exception`` class, and adds a few additional properties that provide
greater context when an error is thrown.

A unique element of ``AutomataError`` is that in addition to the
standard exception message, it allows for the inclusion of extra details
in the form of another field, ``details``. This added context can
greatly simplify error handling and debugging in complex project
environments.

The ``user_message`` property is designed to return the ``Exception``
message, providing a useful, human-readable error message. If no message
is provided, it defaults to ``"<empty message>"``.

Related Symbols
---------------

``AutomataError`` is used as a base class for multiple exception classes
across the Automata project. Some of these classes include: -
``automata.tasks.task_error.TaskStateError`` -
``automata.tasks.task_error.TaskGeneralError`` -
``automata.eval.agent.code_writing_eval.CodeExecutionError`` -
``automata.eval.agent.code_writing_eval.VariableNotFoundError``

Usage Example
-------------

During the development of tasks, if a task is not in the correct state
for the operation, ``TaskStateError`` would be raised:

.. code:: python

   from automata.tasks.task_error import TaskStateError

   try:
       # Code that fails because of the task being in the wrong state
       task = AutomataTask()
       task.execute()  
   except TaskStateError as e:
       print(f"Encountered an error: {e.user_message}. Details: {e.details}")

Note: ``AutomataTask`` and its ``execute`` method is used as a
placeholder for this example.

Limitations
-----------

``AutomataError`` does not necessarily have limitations; however, one
might consider that both the ``message`` and ``details`` are not
enforced to adhere to any particular format, which could lead to
inconsistent error messages in a larger codebase. It might also be
perceived as a limitation that this error does not include built-in
support for richer error logging or serialization.

Follow-up Questions:
--------------------

-  Is there a need for a consistent format or schema for additional
   ``details`` in the ``AutomataError`` exceptions?
-  Would it be beneficial to integrate ``AutomataError`` with a logging
   or a monitoring system?
-  Could ``AutomataError`` benefit from being equipped with a feature
   allowing it to be serialized to JSON or another format?
