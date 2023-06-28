AutomataOpenAIAgent
===================

``AutomataOpenAIAgent`` is an autonomous agent designed to execute
instructions and report the results back to the main system. It
communicates with the OpenAI API to generate responses based on given
instructions and manages interactions with various tools.

Overview
--------

An instance of ``AutomataOpenAIAgent`` is initialized with a set of
instructions and an optional configuration. The agent can then be used
to perform multiple iterations of tasks until a final result is produced
or the maximum number of iterations is reached. During execution, it
communicates with the OpenAI API to generate responses based on given
instructions.

The agent’s configuration options can be customized via an instance of
``AutomataAgentConfig``. This configuration can include specific
settings like model parameters, tool providers, iteration limits, and
more.

Related Symbols
---------------

-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance``
-  ``automata.core.llm.providers.openai.OpenAIAgent``
-  ``automata.config.config_types.AutomataAgentConfig``
-  ``config.automata_agent_config_utils.AutomataAgentConfigBuilder``
-  ``automata.core.agent.task.executor.IAutomataTaskExecution._build_agent``

Example
-------

Below is an example on how to create an instance of
``AutomataOpenAIAgent``:

.. code:: python

   from automata.config.config_enums import AgentConfigName
   from automata.core.agent.agents import AutomataOpenAIAgent
   from automata.config.automata_agent_config_utils import AutomataAgentConfigBuilder

   config_name = AgentConfigName.AUTOMATA_MAIN
   config_builder = AutomataAgentConfigBuilder.from_name(config_name)

   instructions = "Calculate the square of 5."
   agent = AutomataOpenAIAgent(instructions, config=config_builder.build())

   result = agent.run()
   print(result)  # Output: "The square of 5 is 25."

Limitations
-----------

-  The ``AutomataOpenAIAgent`` class relies on the OpenAI API for
   generating responses. If the OpenAI API is unavailable or if there
   are issues with the API key, the agent will not be able to function.
-  The agent’s execution is limited by the number of iterations
   configured in the ``AutomataAgentConfig``. If a valid result is not
   found within the given number of iterations, it raises an error.
-  The output of the agent may not always be accurate if the
   instructions provided are unclear or if the model used is not
   well-suited for the given task.

Follow-up Questions:
--------------------

-  How can we ensure more accurate and consistent results when using an
   ``AutomataOpenAIAgent``?
