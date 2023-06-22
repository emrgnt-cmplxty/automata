AgentConfigName
===============

``AgentConfigName`` is an enum that represents the possible agent config
names. Corresponding to the name of the YAML file in
``automata/configs/agent_configs``. This can be used to load the
required configuration while creating an instance of
``AutomataAgentConfig``.

Overview
--------

``AgentConfigName`` comprises two types of configs: Helper Configs and
Production Configs. Helper Configs include ``DEFAULT``, ``TEST``, and
``AUTOMATA_INITIALIZER``. Production Configs include
``AUTOMATA_RETRIEVER``, ``AUTOMATA_MAIN``, and ``AUTOMATA_WRITER``.

Related Symbols
---------------

-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.core.agent.coordinator.AutomataInstance.Config``

Example
-------

The following is an example demonstrating how to use the
``AgentConfigName`` enum.

.. code:: python

   from config.config_enums import AgentConfigName
   from config.automata_agent_config import AutomataAgentConfig

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

Limitations
-----------

``AgentConfigName`` enums are limited to the available YAML
configuration files in the ``automata/configs/agent_configs`` directory.
If you want to use a custom configuration name, you will need to add the
corresponding YAML file in that directory and update the
``AgentConfigName`` enum accordingly.

Follow-up Questions:
--------------------

-  What are the specific configurations and setup options for each of
   the available ``AgentConfigName`` enums?
