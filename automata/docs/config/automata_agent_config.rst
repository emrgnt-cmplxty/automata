AutomataAgentConfig
===================

``AutomataAgentConfig`` is a configuration class that helps configure
and set up an ``AutomataAgent``. It contains various attributes such as
``config_name``, ``instruction_payload``, ``llm_toolkits``, and others
to provide the necessary setup and settings to be used by the agent.

Overview
--------

``AutomataAgentConfig`` provides a way to load the agent configurations
specified by the ``AgentConfigName``. The configuration options can be
set during the instantiation of the class or can be loaded using the
``load`` class method. It provides utility methods to load and set up
agent configurations while also validating the provided settings. The
class offers a convenient way to create an agent with custom
configurations and includes closely related symbols such as
``AgentConfigName``.

Related Symbols
---------------

-  ``config.config_types.AgentConfigName``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.core.agent.coordinator.AutomataCoordinator``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataAgentConfig`` using a predefined configuration name.

.. code:: python

   from automata.config.config_types import AutomataAgentConfig, AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

Limitations
-----------

The primary limitation of ``AutomataAgentConfig`` is that it relies on
the predefined configuration files based on ``AgentConfigName``. It can
only load configurations from those files and cannot load custom
configuration files. In addition, it assumes a specific directory
structure for the configuration files.

Follow-up Questions:
--------------------

-  How can we include custom configuration files for loading into the
   ``AutomataAgentConfig`` class?
