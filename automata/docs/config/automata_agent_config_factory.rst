AutomataAgentConfigFactory
==========================

``AutomataAgentConfigFactory`` is a factory class that provides a simple
and convenient way to create ``AutomataAgentConfig`` instances based on
the provided arguments. It allows users to create agent configurations
with custom settings and handles any conflicting or missing arguments.

Overview
--------

``AutomataAgentConfigFactory`` utilizes the ``create_config`` method to
create an instance of the ``AutomataAgentConfig``. This method takes in
various arguments that are used to create an ``AutomataAgentConfig`` and
offers the flexibility to override or change the default settings as
needed. The class also checks for any conflicts or missing mandatory
arguments during the creation process.

Related Symbols
---------------

-  ``config.automata_agent_config.AutomataAgentConfig``
-  ``config.automata_agent_config_utils.AutomataAgentConfigBuilder``
-  ``core.agent.agent.AutomataAgent``
-  ``config.config_enums.AgentConfigName``

Example
-------

The following example demonstrates how to create an
``AutomataAgentConfig`` using the ``AutomataAgentConfigFactory``.

.. code:: python

   from automata.core.agent.agent import AutomataAgentConfig
   from automata.config.agent_config_builder import AutomataAgentConfigFactory, AgentConfigName

   instructions = "Execute the following query: SELECT * FROM users;"
   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfigFactory.create_config(main_config_name=config_name)

Limitations
-----------

``AutomataAgentConfigFactory`` relies on predefined configurations from
the ``AutomataAgentConfig`` and ``AutomataAgentConfigBuilder`` classes.
The user should have knowledge of these configurations and their default
values before using the factory method. Additionally, the factory method
may raise exceptions for any conflicting or missing mandatory arguments,
which the user must handle.

Follow-up Questions:
--------------------

-  Can the factory method implementation be improved to provide better
   error handling and be more user-friendly?
