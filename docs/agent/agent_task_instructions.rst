AgentTaskInstructions
=====================

``AgentTaskInstructions`` is an exception class that is raised when
there is an error with the instructions for a given task. This class is
primarily used in the context of ``AutomataTask`` and its methods to
ensure proper task setup and execution.

Overview
--------

``AgentTaskInstructions`` is an integral part of validation of task
execution. Instances of ``AutomataTask`` are created with detailed
instructions, which serve as requirements for any given task to be
executed by the TaskExecutor. If instructions are either not provided or
are empty, the ``AgentTaskInstructions`` exception is raised to halt
execution and signal the error.

Related Symbols
---------------

-  ``automata.tests.unit.test_task_database.task``
-  ``automata.tests.conftest.task``
-  ``automata.tasks.tasks.AutomataTask``
-  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
-  ``automata.tasks.tasks.AutomataTask.__init__``
-  ``automata.tests.unit.test_task_executor.TestExecuteBehavior``
-  ``automata.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.unit.test_task_executor.TestExecuteBehavior.execute``
-  ``automata.agent.agent.AgentInstance.run``
-  ``automata.tests.unit.sample_modules.sample2.PythonAgentToolkit.python_agent_python_task``

Example
-------

The following is an example demonstrating how an
``AgentTaskInstructions`` exception is raised when instructions are
missing or empty for an ``AutomataTask`` instance.

.. code:: python

   from automata.tasks.tasks import AutomataTask

   try:
       task = AutomataTask("")  # Empty instructions
   except AgentTaskInstructions:
       print("AgentTaskInstructions exception raised. Task instructions cannot be empty.")

Limitations
-----------

One important limitation of ``AgentTaskInstructions`` is its dependence
on developer vigilance. That is, if the developer correctly provides
task instructions every time an ``AutomataTask`` instance is created,
this exception would never need to be raised. Conversely, in the absence
of this, the system can come to a halt if instructions are missing.

Follow-up Questions:
--------------------

-  Does ``AgentTaskInstructions`` support multi-language error messages?
-  Can a different mechanism be used to check instructions validity to
   avoid system halt?
