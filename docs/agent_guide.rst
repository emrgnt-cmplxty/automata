=================
Agent Guide
=================

OpenAIAutomataAgentConfigBuilder
================================

Overview
--------

The OpenAIAutomataAgentConfigBuilder is used to build instances of AutomataAgents. It provides a flexible way to set different properties of the agent before instantiation. This class is a subclass of AgentConfigBuilder and belongs to the `automata.config.openai_agent` module.

The builder takes an OpenAIAutomataAgentConfig object as an attribute, which holds various configuration settings for the agent. These settings can include the model, instruction version, system template formatter, etc. 

You can use the `create_config` and `create_from_args` static methods to instantiate the OpenAIAutomataAgentConfig class. Individual properties of the agent can be set using the `with_*` methods. 

Example
-------

.. code-block:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.config.base import AgentConfigName

   # Create an instance of OpenAIAutomataAgentConfig using create_config method
   config = OpenAIAutomataAgentConfigBuilder.create_config(config_name=AgentConfigName.DEFAULT)

   # Create an instance of OpenAIAutomataAgentConfigBuilder using with_model method
   builder = OpenAIAutomataAgentConfigBuilder.with_model("gpt-4")


OpenAIAutomataAgent
===================

Overview
--------

OpenAIAutomataAgent is an autonomous agent designed to execute instructions and report the results back to the main system. It uses the OpenAI API to generate responses based on given instructions and manages interactions with various tools.

The agent operates in iterations and stops when it completes its task or exceeds the maximum iterations set in the configuration. OpenAIAutomataAgent uses tools that are instances of OpenAITool.

Usage
-----

.. code-block:: python

   from automata.agent.providers import OpenAIAutomataAgent
   from automata.config.openai_agent import OpenAIAutomataAgentConfig

   # Create OpenAIAutomataAgentConfig
   config = OpenAIAutomataAgentConfig()

   # Initialize OpenAIAutomataAgent
   agent = OpenAIAutomataAgent('your_instructions', config)

   # Run the agent
   result = agent.run()

Limitations
-----------

OpenAIAutomataAgent's full functionality depends on the integration with OpenAI API requirements and limitations. Improvements might be needed in logging and exception handling. It currently does not support multiple assistants.

