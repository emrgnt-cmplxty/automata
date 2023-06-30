AgentConfigName
===============

``AgentConfigName`` is an enumeration of agent configuration names. It
corresponds to the name of the YAML file in the
``automata/config/agent/`` directory.

Overview
--------

``AgentConfigName`` is primarily used in configuration and testing for
the Automata project. It defines the possible enumeration values for
agent configuration names. These values are typically used when loading
the agent configurations using the ``AutomataAgentConfig`` class.

Related Symbols
---------------

-  ``config.config_enums.AgentConfigName``
-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``

Example
-------

Here’s an example of how to use ``AgentConfigName`` to load an
``AutomataAgentConfig``.

.. code:: python

   from config.config_enums import AgentConfigName
   from config.automata_agent_config import AutomataAgentConfig

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

Limitations
-----------

The primary limitation of ``AgentConfigName`` is that it only references
predefined enumeration values. Adding custom configuration names would
require modifying the ``AgentConfigName`` enumeration and adding the
corresponding YAML configuration files to the project’s
``config/agent/`` directory.

Follow-up Questions:
--------------------

-  Can the ``AgentConfigName`` enumeration be extended programmatically
   to support custom configuration names?
