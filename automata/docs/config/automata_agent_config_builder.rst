AutomataAgentConfigBuilder
==========================

The ``AutomataAgentConfigBuilder`` class is a builder for constructing
instances of ``AutomataAgents``. It offers a flexible and easy-to-use
interface for setting various properties of the agent before
instantiation. The class can be used to build custom configurations for
an ``AutomataAgent`` and initialize an agent based on the specified
configuration.

Overview
--------

``AutomataAgentConfigBuilder`` is used to create and modify
``AutomataAgentConfig`` instances. It allows users to set different
properties of the agent, such as the instruction payload, the model, the
temperature, and other important values. The builder provides several
methods to easily set properties and build the final agent configuration
object.

Related Symbols
---------------

-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``config.config_types.AutomataAgentConfig``

Example
-------

The following example demonstrates how to create an
``AutomataAgentConfigBuilder`` instance and set various properties for
the agent.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigBuilder
   from automata.config.config_types import AgentConfigName, AutomataInstructionPayload

   config_name = AgentConfigName.TEST
   agent_config_builder = AutomataAgentConfigBuilder.from_name(config_name)

   instruction_payload = AutomataInstructionPayload(
       agents_message="Test message",
       overview="Repository overview",
       tools="Available tools"
   )

   new_agent_config = (
       agent_config_builder.with_instruction_payload(instruction_payload)
       .with_model("gpt-4")
       .with_stream(False)
       .with_verbose(True)
       .with_max_iters(100)
       .with_temperature(0.8)
       .with_session_id("sample-session-id")
       .with_eval_mode(False) # Change this depending on actual use-case
       .build()
   )

Once you have the ``new_agent_config`` instance, you can use it to
create an ``AutomataAgent``.

.. code:: python

   from automata.core.agent.agent import AutomataAgent

   instructions = "Execute the given instructions."
   agent = AutomataAgent(instructions, config=new_agent_config)

Limitations
-----------

``AutomataAgentConfigBuilder`` assumes that the agent has a specific set
of properties and configuration settings. If there are additional
settings that an agent might need, they should be added as properties
and methods to the builder class.

Follow-up Questions:
--------------------

-  How can users add their custom configuration settings to the
   ``AutomataAgentConfigBuilder`` class?
