AgentInstance
=============

``AgentInstance`` is an abstract class for implementing an agent
instance. It provides a way to create an instance of the agent and
define a ``run`` method to be executed when running the agent.

Overview
--------

``AgentInstance`` is meant to be subclassed by specific agent
implementations and provides a ``create`` method for instantiating the
agent along with providing a ``run`` method to be implemented. It acts
as a base class that can be inherited to provide the required
functionality for agent instances in the system.

Related Symbols
---------------

-  ``automata.core.agent.providers.OpenAIAutomataAgent``
-  ``automata.core.agent.instances.AutomataOpenAIAgentInstance``
-  ``automata.core.base.agent.Agent``
-  ``automata.core.base.tool.Tool``

Example
-------

The following is an example demonstrating how to create a custom agent
instance by subclassing ``AgentInstance``.

.. code:: python

   from automata.core.base.agent import AgentInstance
   from automata.core.config.config_types import AgentConfigName

   class CustomAgentInstance(AgentInstance):

       def run(self, instructions: str) -> str:
           # Add implementation for running the agent with given instructions
           return "Running custom agent instance with instructions: " + instructions

   config_name = AgentConfigName.TEST
   description = "Custom Agent Instance"
   custom_agent_instance = CustomAgentInstance.create(config_name=config_name, description=description)

   print(custom_agent_instance.run("Test instructions"))
   # Output: Running custom agent instance with instructions: Test instructions

Limitations
-----------

As an abstract class, ``AgentInstance`` cannot be used directly.
Instead, it should be subclassed by specific agent implementations that
provide their own implementation of the ``run`` method. This enables
different providers to run with various configurations and setups as
needed.

Follow-up Questions:
--------------------

-  Is there a specific agent implementation that can be used as an
   actual agent instance example along with the
   ``AgentInstance.create()`` method?
