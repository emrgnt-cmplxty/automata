AutomataOpenAIAgentConfig
=========================

``AutomataOpenAIAgentConfig`` is a configuration class that helps
configure, setup, and interact with an ``OpenAIAutomataAgent``. It
contains various attributes such as ``SUPPORTED_MODELS``,
``arbitrary_types_allowed``, and others to provide the necessary setup
and settings to be used by the agent.

Overview
--------

``AutomataOpenAIAgentConfig`` provides a way to manage the agent
configurations and settings for interacting with the OpenAI API. The
configuration includes the supported models, arbitrary types allowance,
and other necessary settings for generating responses based on given
instructions and managing agent interactions.

Related Symbols
---------------

-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.config.openai_agent.AutomataOpenAIAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.config.config_types.AgentConfigName``

Example
-------

The following is an example demonstrating how to create an instance of
``AutomataOpenAIAgentConfig`` using
``AutomataOpenAIAgentConfigBuilder``.

.. code:: python

   from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.TEST
   config_builder = AutomataOpenAIAgentConfigBuilder.from_name(config_name)
   config = config_builder.build()

Limitations
-----------

The primary limitation of ``AutomataOpenAIAgentConfig`` is that it
relies on the predefined configuration options. It does not support
custom configuration options outside of the specified settings, and any
customization should be done within the boundaries of these settings.

Follow-up Questions:
--------------------

-  How can we include custom configuration options in
   ``AutomataOpenAIAgentConfig`` to allow for more flexible agent
   configurations?
-  Are there any considerations regarding backward compatibility or
   dependency issues when adding new configuration options or modifying
   existing ones in ``AutomataOpenAIAgentConfig``?
