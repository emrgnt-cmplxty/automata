AgentResultError
================

``AgentResultError`` is an exception raised when an
``AutomataOpenAIAgent`` fails to produce a result. This error is raised
by the ``run()`` method of the ``AutomataOpenAIAgent`` when the agent
doesn’t produce a result within the specified maximum number of
iterations.

Related Symbols
---------------

-  ``automata.core.agent.agents.AutomataOpenAIAgent``
-  ``automata.core.agent.error.AgentTaskInstructions``
-  ``automata.core.agent.error.AgentMaxIterError``

Example
-------

The following example illustrates how the ``AutomataOpenAIAgent`` can
raise an ``AgentResultError`` when a specific result is not received in
the conversation within the maximum number of iterations.

.. code:: python

   from automata.core.agent.agents import AutomataOpenAIAgent
   from automata.core.agent.config import AutomataAgentConfig
   from automata.core.agent.error import AgentResultError

   instructions = "Please find the result for this task."
   config = AutomataAgentConfig.load("your_config_name")

   agent = AutomataOpenAIAgent(instructions, config)
   agent.config.max_iterations = 3

   try:
       result = agent.run()
   except AgentResultError:
       print("Agent failed to produce a result within the maximum number of iterations.")

Limitations
-----------

The primary limitation of ``AgentResultError`` is that it assumes that
the agent must produce an explicit result within the maximum number of
iterations. When this error is raised, it might not necessarily indicate
an insufficiency in the agent itself but rather that the task is too
complex, or the conversation has not converged to a specific result.

Follow-up Questions:
--------------------

-  Are there any other possible reasons the ``AgentResultError`` might
   be raised besides exceeding the maximum number of iterations?
-  Is there any possibility that, although the maximum number of
   iterations is exceeded, the conversation content might still contain
   the desired result?
