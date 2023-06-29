AutomataOpenAIAgentConfig
=========================

``AutomataOpenAIAgentConfig`` is a configuration class that helps
configure, setup, and interact with an ``OpenAIAutomataAgent``. It
contains various attributes such as ``config_name``, ``instructions``,
``tools``, and others to provide the necessary setup and settings to be
used by the agent. It also contains an inner class ``TemplateFormatter``
which is responsible for creating default template formatters based on
agent configurations.

Overview
--------

``AutomataOpenAIAgentConfig`` provides a way to load the agent
configurations specified by the ``AgentConfigName``. The configuration
options can be set during the instantiation of the class or can be
loaded using the ``load`` classmethod. It provides utility methods to
load and setup agent configurations while also validating the provided
settings. The class offers a convenient way to create an agent with
custom configurations and includes closely related symbols like
``AgentConfigName`` and ``AutomataOpenAIAgentConfigBuilder``.

Related Symbols
---------------

-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.config.openai_agent.AutomataOpenAIAgentConfigBuilder``
-  ``automata.tests.conftest.automata_agent_config_builder``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataOpenAIAgentConfig`` using a predefined configuration name.

.. code:: python

   from automata.config.openai_agent import AutomataOpenAIAgentConfig
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataOpenAIAgentConfig.load(config_name)

Limitations
-----------

The primary limitation of ``AutomataOpenAIAgentConfig`` is that it
relies on the predefined configuration files based on
``AgentConfigName``. It can only load configurations from those files
and cannot load custom configuration files. In addition, it assumes a
specific directory structure for the configuration files.

Follow-up Questions:
--------------------

-  How can we include custom configuration files for loading into the
   ``AutomataOpenAIAgentConfig`` class?
