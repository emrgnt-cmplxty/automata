AgentMaxIterError
=================

``AgentMaxIterError`` is an exception raised when the agent exceeds the
maximum number of iterations while performing a task.

Overview
--------

This error is raised to indicate that the ``OpenAIAutomataAgent`` has
reached its maximum number of iterations before producing an expected
result. It is typically encountered during the ``run()`` method
execution of the agent. The error is a subclass of
``AgentIterationError``.

Related Symbols
---------------

-  ``automata.core.agent.error.AgentIterationError``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder.with_max_iterations``

Example
-------

The following example demonstrates how to handle ``AgentMaxIterError``
during the execution of an ``OpenAIAutomataAgent`` instance.

.. code:: python

   from automata.core.agent.providers import OpenAIAutomataAgent
   from automata.core.agent.error import AgentMaxIterError

   instructions = "Find the answer to the equation: x + 2 = 5"
   config = AutomataAgentConfig.load(AgentConfigName.AUTOMATA_MAIN)
   config.max_iterations = 5

   agent = OpenAIAutomataAgent(instructions, config)

   try:
       result = agent.run()
       print("The result is:", result)
   except AgentMaxIterError:
       print("The agent exceeded the maximum number of iterations.")

Limitations
-----------

The ``AgentMaxIterError`` exception is only raised when the agent
reaches the ``max_iterations`` during its ``run()`` method execution.
Adjusting the ``max_iterations`` attribute in the
``AutomataAgentConfig`` can help mitigate this issue, but excessive
iteration counts might cause unnecessary load on the system.

Follow-up Questions:
--------------------

-  Is there a way to gracefully recover from ``AgentMaxIterError`` and
   provide partial results?
