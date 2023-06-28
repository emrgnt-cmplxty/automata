AutomataAgentConfigBuilder
==========================

``AutomataAgentConfigBuilder`` is a builder class for constructing
instances of ``AutomataAgentConfig``. It offers a flexible and
easy-to-use interface for setting various properties of the agent
configuration before instantiation.

Overview
--------

``AutomataAgentConfigBuilder`` simplifies the process of creating and
configuring an ``AutomataAgentConfig`` instance. It provides an
interface to set various configuration properties of the agent such as
the model, stream, maximum iterations, temperature, tools, and more. The
builder uses method chaining, making it easy to configure the agent with
a cleaner and more readable syntax.

Related Symbols
---------------

-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.agents.AutomataOpenAIAgent``
-  ``automata.tests.conftest.automata_agent``
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``

Example
-------

The following is an example demonstrating how to create an
``AutomataAgentConfig`` instance using the
``AutomataAgentConfigBuilder``.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigBuilder
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.TEST
   builder = AutomataAgentConfigBuilder.from_name(config_name)
   config = builder.with_model("gpt-3.5-turbo").with_stream(True).with_max_iterations(50).build()

Limitations
-----------

-  Some methods in ``AutomataAgentConfigBuilder`` require a specific
   list of supported models or expect values to be in a particular
   format. If incorrect values are provided, it raises ``ValueError``.

-  The builder relies on predefined configuration files based on
   ``AgentConfigName``. It can only load configurations from those files
   and cannot easily load custom configuration files.

Follow-up Questions:
--------------------

-  How can we include custom configuration files for loading into the
   ``AutomataAgentConfig`` class?
