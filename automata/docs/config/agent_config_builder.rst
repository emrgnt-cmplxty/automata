AgentConfigBuilder
==================

``AgentConfigBuilder`` is a base class that defines a builder for
constructing instances of ``Agent``. It offers a flexible and
easy-to-use interface for setting various properties of the agent before
instantiation. The config builder is a builder pattern implementation
that helps organize the processing of agent specific configurations.

Overview
--------

The ``AgentConfigBuilder`` is an abstract class defining the base
methods needed to create a configuration for providers. The class
implements a generic structure with methods for configuration building.
It also provides a private attribute for storing the configuration data
and uses abstract methods to enforce the implementation of builder
methods in the related symbols.

This builder class supports setting multiple properties like ``model``,
``tools``, ``stream``, ``verbose``, ``max_iterations``, ``temperature``,
and ``session_id``. It also provides class methods for easily creating
an ``AgentConfigBuilder`` instance using the provided configuration
object or the configuration object name.

Related Symbols
---------------

-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``

Example
-------

The following example demonstrates how to create an instance of
``OpenAIAutomataAgentConfigBuilder``, a subclass of
``AgentConfigBuilder``, and configure its properties.

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.tools.registries import Tool

   builder = OpenAIAutomataAgentConfigBuilder()
   builder = builder.with_model("gpt-3.5-turbo")
   builder = builder.with_stream(True)
   builder = builder.with_verbose(True)
   builder = builder.with_max_iterations(500)
   builder = builder.with_temperature(0.5)
   builder = builder.with_session_id("test-session-id")
   builder = builder.with_tools([Tool("tool_name", "tool_function")])

   config = builder.build()

Limitations
-----------

The main limitation of ``AgentConfigBuilder`` is that it’s an abstract
class and can’t be used directly. Subclasses (like
``OpenAIAutomataAgentConfigBuilder``) should be used, which implement
the necessary methods, and can be built efficiently with specific
configurations.

Follow-up Questions:
--------------------

-  How can we extend the builder pattern to add support for new
   configurations and other providers?
-  Are there any common naming conventions or practices to better
   understand the builder pattern in Python?
