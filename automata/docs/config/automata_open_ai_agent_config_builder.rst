AutomataOpenAIAgentConfigBuilder
================================

``AutomataOpenAIAgentConfigBuilder`` is a builder class for constructing
instances of ``AutomataAgents`` with customized configurations for
interacting with the OpenAI API. It provides a flexible and easy-to-use
interface for setting various properties of the agent before
instantiation.

Overview
--------

``AutomataOpenAIAgentConfigBuilder`` extends the base class
``AgentConfigBuilder``. It provides methods to set the agent properties,
such as model, stream flag, verbose flag, toolkits, session ID, max
iterations, and temperature. The class provides type validation for
these properties and raises a ``ValueError`` for invalid inputs. It also
provides classmethods for creating an ``AutomataOpenAIAgentConfig``
instance from provided arguments, configuration name, or configuration
object.

Related Symbols
---------------

-  ``automata.config.openai_agent.AutomataOpenAIAgentConfig``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.conftest.automata_agent_config_builder``

Example
-------

In the following example, we demonstrate how to create an instance of
``AutomataOpenAIAgentConfigBuilder`` with custom configuration options:

.. code:: python

   from automata.config.openai_agent import AutomataOpenAIAgentConfigBuilder
   from automata.config.config_types import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   builder = AutomataOpenAIAgentConfigBuilder.from_name(config_name)

   # Customize configuration options
   builder = builder.with_model("gpt-3.5-turbo")
   builder = builder.with_stream(False)
   builder = builder.with_temperature(0.8)
   builder = builder.with_session_id("custom-session-id")

   # Build the configuration
   config = builder.build()

Follow-up Questions:
--------------------

-  How to support type validation for more complex custom types?
-  Can the ``AutomataOpenAIAgentConfigBuilder`` be made even more
   flexible and easy-to-use?
