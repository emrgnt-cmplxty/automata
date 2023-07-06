AgentConfigBuilder
==================

``AgentConfigBuilder`` is a builder class that helps in the creation of
Agent configurations. It extends the generic type ``T`` and requires the
implementor to implement methods for creating the specific configuration
object and associating the correct model with the agent.

Overview
--------

``AgentConfigBuilder`` primarily functions by taking an optional
``config`` object, upon instantiation which defaults to the result of
the ``create_config`` function if not provided. The configuration object
can be constructed from scratch or from existing configurations by using
the ``from_config`` or ``from_name`` methods, respectively.

This configuration builder also has the capability to set specific
parameters related to the Agent including the tools it will use, the
model it should run, whether it will stream output, verbosity of
logging, maximum iterations the agent should run, and others. The
validity of all parameter types is thoroughly checked before being
updated in the builder configuration.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_provided_parameters_override_defaults``
-  ``automata.agent.agent.AgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_accepts_all_fields``
-  ``automata.agent.instances.OpenAIAutomataAgentInstance.Config``
-  ``automata.config.base.AgentConfigName``
-  ``automata.tools.base.Tool``

Usage Example
-------------

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.config.base import AgentConfigName

   # Using builder to construct with default config
   builder_default_config = OpenAIAutomataAgentConfigBuilder()
   config_default = builder_default_config.build()

   # Using builder to construct with existing config
   builder_from_config = OpenAIAutomataAgentConfigBuilder.from_config(config_default)
   config_from_config = builder_from_config.build()

   # Using builder to construct from named config
   builder_from_name = OpenAIAutomataAgentConfigBuilder.from_name(AgentConfigName.TEST)
   config_from_name = builder_from_name.build()

Limitations
-----------

The builder pattern, while providing a clean API, can lead to over
complicated code since each attribute is set individually. Be careful of
overusing builders and consider passing a single object with many
parameters. This can also make it more difficult to understand as the
logical groups of parameters can be broken up.

Follow-up Questions:
--------------------

-  Is there a way to populate the builder with a group of related
   parameters at once?
-  How can we ensure each attribute is being updated in a consistent
   manner?
