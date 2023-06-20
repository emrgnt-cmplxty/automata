AutomataCoordinator
===================

``AutomataCoordinator`` is a class responsible for managing multiple
``AutomataAgent`` instances. It allows users to add, remove, and run
agent instances according to the specified action.

Overview
--------

``AutomataCoordinator`` provides methods for adding and removing agent
instances by using their configuration names. It can also execute a
specified action on the selected agent instance and return the output
produced by the agent. The class works closely with ``AutomataInstance``
and related symbols.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.agent.action.AgentAction``
-  ``automata.core.agent.coordinator.AutomataInstance``

Example
-------

The following example demonstrates how to create an instance of
``AutomataCoordinator``, add an agent, and execute an action on it:

.. code:: python

   from automata.core.agent.coordinator import AutomataCoordinator
   from automata.config.config_types import AgentConfigName
   from automata.core.agent.coordinator import AutomataInstance
   from automata.core.agent.action import AgentAction

   # Create an AutomataCoordinator
   coordinator = AutomataCoordinator()

   # Add an agent instance
   config_name = AgentConfigName.AUTOMATA_MAIN
   agent_instance = AutomataInstance.create(config_name)
   coordinator.add_agent_instance(agent_instance)

   # Run an action on the agent
   action = AgentAction(
       agent_version=config_name,
       agent_query="How to use AutomataCoordinator?",
       agent_instruction=["First, create an instance of AutomataCoordinator...",
                          "Next, create an AutomataInstance...",
                          "Finally, execute the action on the agent."]
   )
   output = coordinator.run_agent(action)
   print(output)

Limitations
-----------

``AutomataCoordinator`` can only manage instances of ``AutomataAgent``.
Therefore, it might not be able to handle other types of agents
directly. Additionally, it relies on predefined configuration names
(``AgentConfigName``) which limits its ability to load custom
configuration files.

Follow-up Questions:
--------------------

-  How can we extend ``AutomataCoordinator`` to handle other types of
   agents?
-  How can we include custom configuration files for agent instances in
   ``AutomataCoordinator``?
