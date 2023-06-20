AutomataInstance
================

``AutomataInstance`` is a class that represents an active instance of
Automata, a core autonomous agent designed to execute instructions and
report results back to the main system. It communicates with the OpenAI
API to generate responses based on given instructions and manages
interactions with various tools.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.core.agent.coordinator.AutomataCoordinator``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Example
-------

Here is an example of how to create an instance of ``AutomataInstance``:

.. code:: python

   from automata.core.agent.coordinator import AutomataInstance
   from config.config_types import AgentConfigName
   from automata.config.automata_agent_config import AutomataAgentConfigBuilder

   config_name = AgentConfigName.AUTOMATA_RETRIEVER
   config_builder = AutomataAgentConfigBuilder.from_name(config_name)
   instance = AutomataInstance(config_builder.build())

Limitations
-----------

The main limitation of ``AutomataInstance`` is that it relies on the
predefined configurations based on ``AgentConfigName`` and relies on the
``AutomataAgentConfigBuilder`` for building the configuration. It cannot
directly load custom configuration files.

Follow-up Questions:
--------------------

-  How can we include custom configuration files for loading into the
   ``AutomataInstance`` class?
