OpenAIAutomataAgentInstance
===========================

``OpenAIAutomataAgentInstance`` provides an interface for running an
instance of an Automata OpenAI agent multiple times without needing to
reinitialize the agent each time.

Overview
--------

The class stores instructions and configuration for an automata agent,
allowing it to execute those instructions, leveraging the OpenAI API. By
providing instruction configuration, this class enables consistent
responses from the AI agent across multiple runs, thus boosting
performance and efficiency.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder``

Example
-------

In the following example, an instance of ``OpenAIAutomataAgentInstance``
is created by providing instructions. The instance executes the
instructions and returns the result.

.. code:: python

   from automata.core.agent.instances import OpenAIAutomataAgentInstance
   from automata.config.base import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   instructions = "Hello, this is a test instruction"

   agent_instance = OpenAIAutomataAgentInstance(config_name=config_name)

   result = agent_instance.run(instructions)

Limitations
-----------

Currently, the ``run`` method raises a generic Exception for any error
that occurs during agent execution. More specific exceptions could offer
better insight into what could go wrong during execution.

Another limitation is that there is no explicit feature to save or load
previously created instances. Saving and restoring instances would allow
for better reusability and faster startup times.

Follow-up Questions:
--------------------

-  Can the exception handling be more specific, for instance, by
   throwing different types of exceptions based on different error
   conditions?
-  Is there a possibility to implement functionality for saving and
   loading previously created instances?
-  Does the agent have a limit on the number of times it can be run?
