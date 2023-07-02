AgentTaskStateError
===================

``AgentTaskStateError`` is an exception class raised when the task is
not in the correct state for the operation. This is a specific error
handling mechanism for tasks to ensure that they are being executed
under valid and expected conditions.

Related Symbols
---------------

-  ``automata.core.tasks.base.TaskStatus``
-  ``automata.tests.unit.test_task.test_task_inital_state``
-  ``automata.tests.unit.test_task.test_status_setter``
-  ``automata.core.agent.error.AgentTaskGitError``
-  ``automata.core.agent.error.AgentTaskGeneralError``
-  ``automata.core.agent.error.AgentTaskInstructions``

Example
-------

The following is an example demonstrating how to raise the
``AgentTaskStateError`` when a task is not in the correct state.

.. code:: python

   from automata.core.tasks.base import AutomataTask, TaskStatus
   from automata.core.agent.error import AgentTaskStateError

   # Define your task
   task = AutomataTask(...)

   # Assuming your task must be in TaskStatus.SUCCESS to retrieve the result
   if task.status != TaskStatus.SUCCESS:
       raise AgentTaskStateError("Cannot retrieve the result if the task is not in a SUCCESS state")

   # Retrieve the result if the task is in SUCCESS state
   result = task.result

Limitations
-----------

The primary limitation of ``AgentTaskStateError`` is that it assumes
that a task’s state is based on the ``TaskStatus`` enumeration. It may
not be compatible with other task states defined outside
``automata.core.tasks.base.TaskStatus``.

Follow-up Questions:
--------------------

-  Can ``AgentTaskStateError`` handle custom tasks that do not use the
   default ``TaskStatus`` enumeration?
