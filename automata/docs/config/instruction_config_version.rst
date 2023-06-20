InstructionConfigVersion
========================

``InstructionConfigVersion`` is an enumeration class representing
different versions of instruction configurations. It corresponds to the
name of the YAML file in the ``automata/configs/instruction_configs``
directory.

Overview
--------

``InstructionConfigVersion`` is mainly used with ``AutomataAgentConfig``
to load and set specific versions of the introduction instruction. It
provides flexibility in loading and managing different sets of
instructions based on the provided version.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``config.config_types.AgentConfigName``
-  ``config.config_types.AutomataAgentConfig``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.action.AutomataActionExtractor``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.database.vector.JSONVectorDatabase``
-  ``config.agent_config_builder.AutomataAgentConfigBuilder``

Example
-------

The following example demonstrates how to create an
``AutomataAgentConfig`` instance and set the ``instruction_version``
using ``InstructionConfigVersion``.

.. code:: python

   from config.config_types import AutomataAgentConfig, InstructionConfigVersion
   from config.config_enums import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)
   config.instruction_version = InstructionConfigVersion.AGENT_INTRODUCTION

Limitations
-----------

The primary limitation of ``InstructionConfigVersion`` is that it
currently only supports enumeration values that are already defined in
the class. To include additional versions of instruction configurations,
they must be added to the enumeration manually.

Follow-up Questions:
--------------------

-  Can we improve the flexibility of ``InstructionConfigVersion`` to
   allow for dynamic loading of versioned instruction configurations?
