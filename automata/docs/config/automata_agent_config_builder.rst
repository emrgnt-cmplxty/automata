AutomataAgentConfigBuilder
==========================

``AutomataAgentConfigBuilder`` is a builder class that simplifies the
creation of ``AutomataAgentConfig`` instances. It provides an
easy-to-use interface to set various properties of the agent
configuration before instantiation. These properties include instruction
payload, toolkits, model, stream flag, verbose flag, and others.

Overview
--------

``AutomataAgentConfigBuilder`` takes in an ``AutomataAgentConfig``
instance or an optional configuration object and exposes various
``with_`` methods to set various properties. It simplifies the process
of setting agent configurations and validating the provided settings.
The class returns a new ``AutomataAgentConfig`` instance after building
the configuration with the updated attributes.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``config.config_types.AutomataAgentConfig``
-  ``config.config_types.InstructionConfigVersion``
-  ``core.base.tool.Tool``
-  ``core.agent.coordinator.AutomataInstance``
-  ``core.agent.coordinator.AutomataCoordinator``
-  ``core.symbol.graph.SymbolGraph``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataAgentConfigBuilder``.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigBuilder
   from config.config_types import AutomataAgentConfig, AgentConfigName

   builder = AutomataAgentConfigBuilder.from_name(AgentConfigName.DEFAULT)
   config = builder.with_temperature(0.8).with_stream(True).build()

Limitations
-----------

The ``AutomataAgentConfigBuilder`` does not have any significant
limitations. However, it is essential to be aware that the validity of
the provided settings is checked while setting individual attributes,
and any invalid attribute will raise a ``ValueError``.

Follow-up Questions:
--------------------

-  Can you provide an example of replacing ‘Mock’ objects with actual
   underlying objects?
