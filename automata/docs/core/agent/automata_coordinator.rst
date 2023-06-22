AutomataCoordinator
===================

``AutomataCoordinator`` is a class responsible for managing multiple
``AutomataAgent`` instances. It allows you to add, remove, and run
various agent instances and keep them in a list. It provides utility
methods to add and remove agent instances by their configuration name
and to execute specific actions on the agent instances.

Overview
--------

``AutomataCoordinator`` is used to manage a list of agent instances,
providing methods to add and remove instances, select and run an agent
based on a given action. Once instantiated, the coordinator can be used
to run agent actions using the given agent instances, providing a
centralized way to manage multiple agents. The class offers convenient
utility methods and closely integrates with the ``AutomataAgent``.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.agent.action.AgentAction``
-  ``automata.core.agent.coordinator.AutomataInstance``
-  ``config.config_types.AgentConfigName``

Example
-------

.. code:: python

   from automata.config.config_types import AgentConfigName
   from automata.core.agent.coordinator import AutomataInstance, AutomataCoordinator
   from automata.core.agent.action import AgentAction

   # Instantiate the AutomataCoordinator
   coordinator = AutomataCoordinator()

   # Create and add two AutomataInstances to the coordinator
   instance1 = AutomataInstance(config_name=AgentConfigName.TEST, description="Test instance 1")
   instance2 = AutomataInstance(config_name=AgentConfigName.DEFAULT, description="Test instance 2")
   coordinator.add_agent_instance(instance1)
   coordinator.add_agent_instance(instance2)

   # Define an AgentAction using the agent_version, agent_query, and agent_instruction
   action = AgentAction(
       agent_version=AgentConfigName.TEST,
       agent_query="Find the square of 2.",
       agent_instruction=["Compute the square of the given number."]
   )

   # Run the agent and receive the output
   output = coordinator.run_agent(action)
   print(output)

Limitations
-----------

``AutomataCoordinator`` currently assumes that agent instances use
unique ``AgentConfigName`` in their configurations. If there is a need
to manage multiple agent instances with the same configuration name, the
coordinator does not provide an easy way to track them.

Follow-up Questions:
--------------------

-  How can we support managing multiple agent instances with the same
   configuration name?
