AutomataInstance
================

``AutomataInstance`` is a class that represents an instance of an
autonomous agent that can be configured using the given configuration
settings. The class provides methods to create and run an agent,
providing a convenient interface for using the agent’s functionality.

Overview
--------

``AutomataInstance`` provides two methods: ``create`` and ``run``. The
``create`` method is used to create a new instance of the class, and
takes the configuration settings as its input. The ``run`` method is
used to execute the agent with the given instructions, producing output
based on the given instruction set.

Related Symbols
---------------

-  ``config.agent_config_builder.AutomataAgentConfigFactory``
-  ``core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``core.agent.action.AutomataAction``

Example
-------

The following is an example demonstrating how to create an
``AutomataInstance`` using a predefined agent configuration name and
runs the agent with a set of instructions.

.. code:: python

   from automata.core.agent.coordinator import AutomataInstance
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   instance = AutomataInstance.create(config_name=config_name, description="Example automata agent")

   instructions = "Create a simple function that adds two numbers together"
   output = instance.run(instructions)

   print(output)

Limitations
-----------

The primary limitation of ``AutomataInstance`` is that it assumes a
specific directory structure for agent configurations, which are defined
by ``AgentConfigName``. In addition, ``AutomataInstance`` does not
provide explicit ways to access the underlying agent nor the ability to
update the agent’s state or configurations on the fly.

Follow-up Questions:
--------------------

-  How can we include custom agent configurations for loading into the
   ``AutomataInstance`` class?
-  How could we access or modify the underlying agent in more detail
   without directly interacting with the underlying ``AutomataAgent``
   class?
