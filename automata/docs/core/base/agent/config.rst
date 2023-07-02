AgentInstance
=============

``AgentInstance`` is an abstract class for implementing an agent
instance. It provides methods for creating instances with specified
configurations and running instructions.

Overview
--------

``AgentInstance`` serves as a base for implementing an agent instance
and is closely related to the ``AutomataOpenAIAgentInstance`` which is
an instance of an Automata OpenAI agent. It provides the ability to
create agent instances using different configurations and run
instructions on them.

Related Symbols
---------------

-  ``automata.core.agent.agent.AgentInstance.Config``
-  ``automata.tests.unit.test_automata_agent_builder.test_automata_agent_init``
-  ``automata.core.agent.agent.AgentInstance.create``
-  ``automata.tests.conftest.task``
-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.tests.conftest.automata_agent_config_builder``
-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance``
-  ``automata.tests.unit.sample_modules.sample2.PythonAgentToolkit.python_agent_python_task``
-  ``automata.core.agent.agent.Agent``

Example
-------

The following example demonstrates how to create and run an instance of
``AutomataOpenAIAgentInstance`` using an agent configuration.

.. code:: python

   from automata.core.agent.instances import AutomataOpenAIAgentInstance
   from automata.core.agent.config import AutomataOpenAIAgentConfig
   from automata.core.agent.config_config_enums import AgentConfigName

   config_name = AgentConfigName.TEST
   config = AutomataOpenAIAgentConfig.load(config_name)
   instructions = "This is a test."

   agent_instance = AutomataOpenAIAgentInstance.create(config_name)
   result = agent_instance.run(instructions)

Limitations
-----------

The primary limitation of ``AgentInstance`` is that it is an abstract
class and cannot be instantiated directly. Implementation of a specific
agent instance class is required (e.g.,
``AutomataOpenAIAgentInstance``).

Follow-up Questions:
--------------------

-  How to create an instance of a different type of agent?
-  What are other possible implementations of ``AgentInstance`` apart
   from the ``AutomataOpenAIAgentInstance``?
