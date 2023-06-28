InstructionConfigVersion
========================

``InstructionConfigVersion`` is an enumeration that represents different
versions of instruction configurations. This enumeration is used to
differentiate between the various instruction configurations provided in
the ``automata/configs/instruction_configs`` directory and is stored as
a field within the ``AutomataAgentConfig`` class.

Overview
--------

The ``InstructionConfigVersion`` enumeration provides a simple way to
define and access the names of different instruction configurations for
an ``AutomataAgent``. It corresponds to the names of YAML files in the
``automata/configs/instruction_configs`` directory.

Related Symbols
---------------

-  ``config.config_types.AutomataAgentConfig``
-  ``automata.config.agent_config_builder.AutomataAgentConfigBuilder``

Examples
--------

Here is an example demonstrating how to use ``InstructionConfigVersion``
as part of building an ``AutomataAgentConfig``.

.. code:: python

   from automata.config.agent_config_builder import AutomataAgentConfigBuilder
   from automata.config.config_types import InstructionConfigVersion

   config = (
       AutomataAgentConfigBuilder()
       .with_instruction_version(InstructionConfigVersion.AGENT_INTRODUCTION.value)
       .build()
   )

   print(config.instruction_version)

Limitations
-----------

The primary limitation of ``InstructionConfigVersion`` is that it relies
on predefined enumeration values and assumes a specific directory
structure for the instruction configurations. Adding new instruction
configuration versions requires updating the enumeration and maintaining
the directory structure.

Follow-up Questions:
--------------------

-  Are there plans to expand the instruction configuration versions with
   custom values?
-  What is the process for adding new instruction configuration versions
   to the enumeration and directory structure?
