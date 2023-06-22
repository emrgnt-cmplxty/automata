AgentAction
===========

``AgentAction`` represents the actions performed by an agent in the
system. It includes essential information like the version of the agent
configuration (``agent_version``), the query to be executed by the agent
(``agent_query``), and the instructions for the agent
(``agent_instruction``). This class has been designed to work with the
``AutomataAgent`` class for communication and coordination.

Overview
--------

The ``AgentAction`` class is responsible for storing the essential
information needed by an agent to perform actions. It is an abstract
base class that needs to be implemented by subclasses with specific
action implementation. The framework depends on this class to provide
proper formatting and information for agent actions.

Related Symbols
---------------

-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.agent.Agent``
-  ``automata.core.agent.agent_enums.ActionIndicator``
-  ``automata.core.agent.agent.AutomataAgent``

Example
-------

The following example demonstrates how to create an instance of
``AgentAction`` and use it in a coordinator.

.. code:: python

   from automata.core.agent.action import AgentAction
   from automata.config.config_types import AgentConfigName

   # Create an AgentAction instance
   action = AgentAction(
       agent_version=AgentConfigName.TEST,
       agent_query="mock_agent_query",
       agent_instruction=["Test instruction."]
   )

   # Use the action in the coordinator
   coordinator.run_agent(action)

Limitations
-----------

The ``AgentAction`` class needs to be subclassed for specific action
implementations, as it is an abstract base class. This requires
developers to implement the necessary internal logic for each action in
their respective subclasses.

Follow-up Questions:
--------------------

-  Are there any specific actions that need to be implemented as
   subclasses of ``AgentAction``?
-  How are the pre-defined ``AgentAction`` instances stored and accessed
   in the system?
