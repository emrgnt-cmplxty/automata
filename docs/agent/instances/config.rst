OpenAIAutomataAgentInstance
===========================

The ``OpenAIAutomataAgentInstance`` is a class that stores the
instructions and configuration for an ``OpenAIAutomataAgent`` such that
it can be run multiple times without having to reinitialize the agent
each time. This class ensures reusability and efficient handling of the
``OpenAIAutomataAgent``.

Overview
--------

The ``OpenAIAutomataAgentInstance`` has the ability to store both the
instructions and the config of an agent while also providing a method to
run the agent using those stored instructions. Due to this, the same
instance of an agent can be reused for multiple runs, improving
efficiency and system performance.

Related Symbols
---------------

-  ``automata.agent.providers.OpenAIAutomataAgent``: The agent that this
   class holds an instance of.
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``: The
   configuration used by the agent.
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``:
   A test checking the initialization of the agent.
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_creates_proper_instance``:
   A test confirming a proper instance creation of the agent.

Example
-------

Here is an example of how to use the ``OpenAIAutomataAgentInstance``:

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfig
   from automata.config.config_enums import AgentConfigName
   from automata.agent.instances import OpenAIAutomataAgentInstance

   # load configuration
   config = OpenAIAutomataAgentConfig.load(AgentConfigName.TEST)

   # Create instance of OpenAIAutomataAgent
   agent_instance = OpenAIAutomataAgentInstance(config)

   # Use the run method with instructions
   result = agent_instance.run("Enter your instructions here")

Limitations
-----------

The ``OpenAIAutomataAgentInstance`` depends on ``OpenAIAutomataAgent``
and ``OpenAIAutomataAgentConfig``. Hence, it’s functionality is largely
dependent on these classes. Also, initialization of
``OpenAIAutomataAgentInstance`` requires configuration details which may
limit its usability.

Follow-Up Questions:
--------------------

-  How can we modify ``OpenAIAutomataAgentInstance`` to be more
   independent and less configuration-dependent?
-  Can there be a default configuration for
   ``OpenAIAutomataAgentInstance`` to improve its usability?
