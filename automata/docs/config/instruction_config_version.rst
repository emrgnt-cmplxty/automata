InstructionConfigVersion
========================

``InstructionConfigVersion`` is an enumeration class containing
different versions of instruction configurations. This enumeration
corresponds to the name of the YAML file in the
``automata/configs/instruction_configs`` directory. The current
available versions of the instruction configurations are
``AGENT_INTRODUCTION``.

Overview
--------

``InstructionConfigVersion`` is used as an attribute in the
``AutomataAgentConfig`` class to specify the version of the introduction
instruction to be used by the ``AutomataAgent``. This allows easy
switching between different instruction config versions, according to
the user’s needs or purposes.

Related Symbols
---------------

-  ``automata.config.config_types.AutomataAgentConfig``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``
-  ``automata.tests.unit.test_automata_coordinator.MockAutomataInstance``

Example
-------

The following example demonstrates how to set the
``instruction_version`` attribute while creating an
``AutomataAgentConfig`` object:

.. code:: python

   from automata.config.config_types import AutomataAgentConfig, InstructionConfigVersion
   from automata.config.config_enums import AgentConfigName

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)
   config.instruction_version = InstructionConfigVersion.AGENT_INTRODUCTION

Additionally, the ``AutomataAgentConfigBuilder`` class allows easy
modification of the ``instruction_version`` attribute, as shown in the
example below:

.. code:: python

   from automata.configagent_config_builder import AutomataAgentConfigBuilder
   from automata.config.config_types import InstructionConfigVersion

   builder = AutomataAgentConfigBuilder()
   builder.with_instruction_version(InstructionConfigVersion.AGENT_INTRODUCTION.value)
   config = builder.build()

Limitations
-----------

The primary limitation of ``InstructionConfigVersion`` is that it
depends on the predefined enumeration values. Custom versions of
instruction configurations cannot be used unless they are added to the
enumeration class.

Follow-up Questions:
--------------------

-  Can we add support for custom versions of instruction configurations?
-  How can we handle backward compatibility issues when new versions of
   instruction configurations are introduced?
