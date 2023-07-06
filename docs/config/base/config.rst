AgentConfig
===========

``AgentConfig`` is a configuration class that provides a set of encoded
defaults regarding how the agent should behave in a given environment.
These behaviors include model, stream, verbosity, maximum iterations,
and temperature.

The ``AgentConfig`` class supports arbitrary types and defaults to the
``OPENAI`` provider.

Overview
--------

``AgentConfig`` plays a key role in defining the agent’s behavior in an
automata environment. The attributes set in ``AgentConfig`` include:

-  ``model``: Specifies the model to base the agent’s behavior on.
-  ``stream``: Specifies whether the agent streams or not.
-  ``verbose``: Specifies the level of verbosity for log output.
-  ``max_iterations``: Specifies the maximum number of processing
   iterations for the agent.
-  ``temperature``: Specifies the level of randomness in the agent’s
   choice.

Related Symbols
---------------

-  ``automata.agent.agent.AgentInstance.Config``: Specifies that as
   part of an agent instance, the ``AgentConfig`` allows arbitrary
   types.
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_default_config``:
   Demonstrates how to build a default configuration.
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``:
   Shows proper instantiation of ``AgentConfig``.
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_provided_parameters_override_defaults``:
   Demonstrates how to override the default parameters of
   ``AgentConfig``.
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``: An
   expanded class of ``AgentConfig`` that also includes instructional
   templates and formatters.
-  ``automata.tools.base.Tool.Config``: Defines an additional class
   for tool-specific Configuration that also allows arbitrary types but
   forbids extra parameters.

Example
-------

Here, we demonstrate how to create an instance of ``AgentConfig`` with
the help of an ``automata_agent_config_builder``:

.. code:: python

   config = (
       automata_agent_config_builder.with_model("gpt-3.5-turbo")
       .with_stream(True)
       .with_verbose(True)
       .with_max_iterations(500)
       .with_temperature(0.5)
       .with_session_id("test-session-id")
       .build()
   )

   assert config.model == "gpt-3.5-turbo"
   assert config.stream is True
   assert config.verbose is True
   assert config.max_iterations == 500
   assert config.temperature == 0.5
   assert config.session_id == "test-session-id"

Limitations
-----------

A possible limitation of ``AgentConfig`` is that the agent’s behavior
strictly depends on the defined parameters in ``AgentConfig``, meaning
it might be inflexible under certain scenarios where dynamic parameter
adjustment is required. Moreover, error handling for invalid
configurations may also present challenges.

Follow-up Questions:
--------------------

-  How does changing different parameters in configurations influence an
   agent’s performance?
-  Are there any strategies for handling faulty configurations?
-  What validations are present to ensure the ``AgentConfig`` parameters
   are valid?
