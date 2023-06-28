AgentConfigName
===============

``AgentConfigName`` is an enumeration of agent configuration names. It
corresponds to the name of the yaml file in ``automata/config/agent/``.
This enumeration makes it easy and safe to reference configuration files
for an Automata Agent.

Overview
--------

``AgentConfigName`` provides predefined names for use when loading an
``AutomataAgentConfig``. The enum values can be used to set
``config_name`` when building an agent configuration using the
``AutomataAgentConfigBuilder`` or directly loading a configuration using
the ``AutomataAgentConfig.load`` method.

Related Symbols
---------------

-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.core.base.agent.AgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.config.config_types.AutomataAgentConfig.Config``
-  ``automata.tests.unit.test_symbol_rank.test_pagerank_config_validation``
-  ``automata.config.config_types.AutomataAgentConfig``

Example
-------

The following example shows how to use ``AgentConfigName`` to create and
load an instance of ``AutomataAgentConfig``.

.. code:: python

   from config.config_enums import AgentConfigName
   from config.automata_agent_config import AutomataAgentConfig

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

Limitations
-----------

``AgentConfigName`` contains a limited set of predefined configuration
names. While this ensures a consistent way of referring to
configurations, it might potentially restrict flexibility if you need to
load a custom configuration file. If there is a need to use custom
configuration names, create your own enumeration or extend the existing
``AgentConfigName``.

Follow-up Questions:
--------------------

-  How can we include custom configuration names for loading into the
   ``AutomataAgentConfig`` class?
