AutomataInstructionPayload
==========================

``AutomataInstructionPayload`` is a dataclass used to store the payload
for formatting the introduction instruction. Fields on this class are
used to format the introduction instruction. The class provides a method
called ``validate_fields`` to ensure that all the required fields are
initialized while setting up the payload.

Related Symbols
---------------

-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.agent.coordinator.AutomataInstance``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``

Example
-------

The following example demonstrates how to create and use an instance of
``AutomataInstructionPayload``.

.. code:: python

   from automata.config.config_types import AutomataInstructionPayload

   payload = AutomataInstructionPayload(agents_message="Hello, I'm an AI Assistant.", tools="List of available tools")
   payload.validate_fields(["agents_message", "tools"])

Limitations
-----------

The primary limitation of ``AutomataInstructionPayload`` is that it
requires the user to manually validate the fields using the
``validate_fields`` method. It is essential to use this method to ensure
the reliability of the instructions.

Follow-up Questions:
--------------------

-  Can the validation of fields be automated without the need to
   manually call ``validate_fields``?
