AgentConfigName
===============

``AgentConfigName`` is an enumeration representing different agent
config names. It corresponds to the name of the YAML configuration file
located in the ``automata/configs/agent_configs`` directory. This
enumeration can be used when setting up an ``AutomataAgent`` with custom
configurations using the ``AutomataAgentConfig`` class.

Overview
--------

``AgentConfigName`` provides a way to specify the configuration name
when loading agent configurations using the ``AutomataAgentConfig.load``
method. It contains several helper configurations, like ``DEFAULT``,
``TEST``, and ``AUTOMATA_INITIALIZER``, as well as production configs,
such as ``AUTOMATA_RETRIEVER``, ``AUTOMATA_MAIN``, and
``AUTOMATA_WRITER``.

Related Symbols
---------------

-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.automata_agent_config_utils.AutomataAgentConfigBuilder``
-  ``config.automata_agent_config.AutomataAgentConfig``

Example
-------

The following is an example demonstrating how to use the
``AgentConfigName`` enumeration when loading ``AutomataAgentConfig``
configurations:

.. code:: python

   from automata.config.config_types import AgentConfigName
   from automata.config.automata_agent_config import AutomataAgentConfig

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)

Limitations
-----------

``AgentConfigName`` enumeration has a limited set of values that
correspond to predefined configurations. Any new custom configurations
need to be added to the ``AgentConfigName`` enumeration and also need to
have a corresponding YAML file in the ``automata/configs/agent_configs``
directory.

Follow-up Questions:
--------------------

-  How can we extend the ``AgentConfigName`` enumeration to include
   custom configuration names without going through the process of
   modifying the code and creating new YAML files?
