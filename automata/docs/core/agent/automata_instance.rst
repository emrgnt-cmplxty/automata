AutomataInstance
================

``AutomataInstance`` is a class representing an agent instance with a
specific configuration. It allows a user to create and run agents based
on the given configuration name. Each ``AutomataInstance`` has a
``config_name`` and a ``description``.

Overview
--------

``AutomataInstance`` provides a way to create agent instances with
specified configurations and run instructions on that agent. It
facilitates the creation and management of agents for various tasks in
the application. The class offers a convenient way to create and run an
agent with the desired configurations, interacting with the
``AutomataAgentConfigFactory``, and ``AutomataAgent``.

Related Symbols
---------------

-  ``config.config_types.AgentConfigName``
-  ``config.agent_config_builder.AutomataAgentConfigFactory``
-  ``core.agent.coordinator.AutomataCoordinator``
-  ``core.agent.agent.AutomataAgent``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataInstance``, create the agent using
``AutomataInstance.create()``, and run specific instructions with the
``run()`` method.

.. code:: python

   from core.agent.coordinator import AutomataInstance
   from config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   automata_instance = AutomataInstance.create(config_name)

   instructions = "Execute a specific action with the agent."
   result = automata_instance.run(instructions)

Limitations
-----------

The primary limitation of ``AutomataInstance`` is that it requires the
``AutomataAgentConfigFactory`` to create the agent configurations. The
configurations are assumed to be stored in a specific directory
structure, and the names should correspond to the ``AgentConfigName``
enum. When using custom agent configurations, a user must ensure their
configuration names conform to this assumption.

Follow-up Questions:
--------------------

-  How can we include custom agent configuration files for creating
   ``AutomataInstance`` objects?
