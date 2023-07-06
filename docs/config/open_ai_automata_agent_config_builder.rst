OpenAIAutomataAgentConfigBuilder
================================

This class is part of the ``automata.config.openai_agent`` module and is
a subclass of ``AgentConfigBuilder``. The
``OpenAIAutomataAgentConfigBuilder`` class is used to build instances of
``AutomataAgents``, providing a flexible way to set different properties
of the agent before instantiation.

Overview
--------

The ``OpenAIAutomataAgentConfigBuilder`` class takes an
``OpenAIAutomataAgentConfig`` object as an attribute. This object holds
various configuration settings for the agent such as the model,
instruction version, system template formatter, etc.

The builder provides static methods ``create_config`` and
``create_from_args`` for instantiating the ``OpenAIAutomataAgentConfig``
class.

Individual properties of the agent can be set using the ``with_*``
methods such as ``with_model``, ``with_system_template_formatter``, or
``with_instruction_version``. For example, to specify the model for the
agent, the ``with_model`` method would be used, assuming the model is
present in the list of ``SUPPORTED_MODELS`` in
``OpenAIAutomataAgentConfig``.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``:
   A test to check if the builder creates the expected instance.
-  ``automata.tests.conftest.automata_agent_config_builder``: Pytest
   fixture that sets up a mocked ``OpenAIAutomataAgentConfigBuilder``.
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``: Holds the
   configuration for the Automata OpenAI Agent.
-  ``automata.core.agent.providers.OpenAIAutomataAgent``: An autonomous
   agent designed to execute instructions and report the results back to
   the main system with interactions with OpenAI API.

Example
-------

The below example demonstrates how to use the
``OpenAIAutomataAgentConfigBuilder`` to build and set up an
``OpenAIAutomataAgentConfig``:

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.config.base import AgentConfigName

   # Create an instance of OpenAIAutomataAgentConfig using create_config method
   config = OpenAIAutomataAgentConfigBuilder.create_config(config_name=AgentConfigName.DEFAULT)

   # Create an instance of OpenAIAutomataAgentConfigBuilder using with_model method
   builder = OpenAIAutomataAgentConfigBuilder.with_model("gpt-4")

Limitations
-----------

Using ``OpenAIAutomataAgentConfigBuilder`` requires a good understanding
of the different properties that can be set on the
``OpenAIAutomataAgentConfig`` object. Furthermore, errors may need to be
manually handled when invalid values are passed to the ``with_*``
methods.

Follow-up Questions
-------------------

-  What are the valid models that the ``with_model`` method will accept?
-  What happens if an invalid value is passed in the ``with_*`` methods?
