AutomataAgent
=============

``AutomataAgent`` is an autonomous agent designed to execute
instructions and report the results back to the main system. It
communicates with the OpenAI API to generate responses based on given
instructions and manages interactions with various tools.

Overview
--------

``AutomataAgent`` uses the OpenAI API for generating responses,
processing those responses, and managing interactions with the
corresponding tools. It can retrieve completion messages, perform
specific actions using the available tools, and generate observed user
messages. The ``AutomataAgent`` class takes ``instructions`` and an
optional ``config`` (AutomataAgentConfig) as input during instantiation.
The agent can be run until it produces a result or until the maximum
iterations are exceeded.

Related Symbols
---------------

-  ``automata.core.agent.agent.Agent``
-  ``automata.core.agent.coordinator.AutomataCoordinator``
-  ``automata.core.agent.database.AutomataAgentDatabase``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.agent.action.ToolAction``

Example
-------

The following example demonstrates how to create an instance of
``AutomataAgent`` and run it to execute a set of instructions.

.. code:: python

   from automata.core.agent.agent import AutomataAgent
   from automata.config import AutomataAgentConfig
   from automata.config.config_types import AgentConfigName

   instructions = "your instructions here"
   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

   agent = AutomataAgent(instructions, config)
   agent.setup()

   result = agent.run()
   print(result)

Limitations
-----------

The primary limitations of ``AutomataAgent`` are:

-  It relies on OpenAI API for response generation, which can result in
   rate-limiting or other API-related issues.
-  It depends on the availability and proper functioning of the tools it
   interacts with. If a specific tool is unavailable or not working
   correctly, the agent may produce incomplete or incorrect results.

Follow-up Questions:
--------------------

-  What happens if, during execution, one of the tools becomes
   unavailable or encounters an error?
