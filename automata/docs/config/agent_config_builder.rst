AgentConfigBuilder
==================

``AgentConfigBuilder`` is a base class for agent configuration builders.
It helps build and configure AutomataAgents with user-defined settings
and validation checks. It provides the necessary methods to create and
build custom AgentConfig instances, while also allowing you to extend
the class to create more complex configurations and validations.

Overview
--------

``AgentConfigBuilder`` provides base methods and attributes, such as the
``_config`` attribute and ``build``, ``from_config``, and ``from_name``
classmethods, that can be extended and customized by inheriting classes.
It offers flexibility in building AgentConfig instances and makes
extending the agent configuration building process more straightforward.

Related Symbols
---------------

-  ``config.config_types.AgentConfig``
-  ``config.openai_agent.AutomataOpenAIAgentConfigBuilder``
-  ``core.agent.instances.AutomataOpenAIAgentInstance``
-  ``tests.unit.test_automata_agent_builder``

Example
-------

The following example demonstrates how to create and build an
``AutomataOpenAIAgentConfigBuilder`` instance using a predefined
configuration name and custom parameters:

.. code:: python

   from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.TEST
   builder = AutomataOpenAIAgentConfigBuilder.from_name(config_name)

   config = (
       builder.with_model("gpt-3.5-turbo")
       .with_stream(True)
       .with_verbose(True)
       .with_max_iterations(500)
       .with_temperature(0.5)
       .with_session_id("test-session-id")
       .build()
   )

Limitations
-----------

The ``AgentConfigBuilder`` class is a base class and cannot directly be
used to create custom AgentConfig instances. Instead, you should use an
inheriting class like ``AutomataOpenAIAgentConfigBuilder`` to create
custom configurations. Additionally, this class relies on the
``AgentConfigName`` enumeration to list the available config files,
making it somewhat inflexible when it comes to adding new configuration
files.

Follow-up Questions:
--------------------

-  How can we improve the flexibility of the ``AgentConfigBuilder``
   class for building and validating custom agent configurations?
