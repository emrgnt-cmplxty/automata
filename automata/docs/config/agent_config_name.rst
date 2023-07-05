``AgentConfigName`` Python Enum
===============================

The enum class ``AgentConfigName`` is a part of the
``automata.config.base`` module in the Automata framework. It includes
string constants representing the various configuration names of the
automata agents. This class is used to fetch specific configuration
files within the directory ``automata/config/agent/*.yaml`` for
configuring the automata agent.

Overview
--------

``AgentConfigName`` class is defined as an Enum (enumeration), which is
a symbolic name for a set of values. Enum attributes are read-only and
cannot be instantiated, but they can be iterated through with a for
loop.

This Enum helps to create more readable and manageable code by providing
meaningful names for specific configuration files. It contains two types
of config names

-  Helper Configs: DEFAULT and TEST.
-  Specific or production Configs: AUTOMATA_MAIN

It should be noted that the config name corresponds to config files
present in the directory ``automata/config/agent/*.yaml``.

Usage
-----

The ``AgentConfigName`` enumeration can be used when loading different
configurations of the automata agent. The string representation of the
enumerations defined in ``AgentConfigName`` corresponds to the filenames
of different configurations in the ``automata/config/agent/*.yaml``
directory.

.. code:: python

   from automata.config.base import AgentConfigName
   from automata.automata_builder import OpenAIAutomataAgentConfig

   def load_config():
       for config_name in AgentConfigName:  # iterate over all config names
           if config_name == AgentConfigName.DEFAULT:  # Skip the "default" config
               continue
           config = OpenAIAutomataAgentConfig.load(config_name)  # load the config
           assert isinstance(config, OpenAIAutomataAgentConfig)  # check the config type

Related Symbols
---------------

-  ``automata.core.agent.agent.AgentInstance.Config``: A class for
   configuring the agent instance arbitrary types allowed.
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``:
   A test function that iterates over all ``AgentConfigName``, skips the
   DEFAULT, loads the config and checks its type.
-  ``automata.tests.conftest.automata_agent_config_builder``: A pytest
   fixture to construct ``OpenAIAutomataAgentConfig``.
-  ``automata.core.agent.instances.OpenAIAutomataAgentInstance.Config``:
   Class for configuring the OpenAI automata agent instance.
-  ``automata.config.base.AgentConfig.Config``: Class for configuring
   the Agent, where arbitrary types are allowed and defines a provider.

Limitations
-----------

One primary limitation of ``AgentConfigName`` is that it can only
provide names for configuration files that exist in the
``automata/config/agent/*.yaml`` directory. If a configuration file does
not exist for a particular name enumerated in ``AgentConfigName``, an
error would occur when attempting to use it.

Follow-up Questions:
--------------------

-  How can we dynamically update ``AgentConfigName`` when a new
   configuration file is added to the ``automata/config/agent/``
   directory?
-  Where should we document newly added configuration names in code for
   future reference?
