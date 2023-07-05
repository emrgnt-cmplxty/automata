InstructionConfigVersion
========================

``InstructionConfigVersion`` is an enumerated class that represents the
various versions of instruction sets available for use in the
``OpenAIAutomataAgentConfig`` class. It corresponds to the name of the
YAML file in the ``automata/configs/instruction_configs`` directory.

Overview
--------

This enumeration helps to identify the specific instruction version to
be used in an ``OpenAIAutomataAgentConfig`` instance. The different
versions of instructions can be managed through these enumerated values,
allowing a user to switch between different sets of agent instructions
easily.

Related Symbols
---------------

-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``
-  ``automata.config.base.InstructionConfigVersion``
-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder.with_instruction_version``

Example
-------

The following is an example demonstrating how to use the
``InstructionConfigVersion`` enumeration when building an
``OpenAIAutomataAgentConfig`` instance:

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.config.base import InstructionConfigVersion

   config_builder = OpenAIAutomataAgentConfigBuilder()
   config = (
       config_builder.with_instruction_version(InstructionConfigVersion.AGENT_INTRODUCTION)
       .build()
   )

Limitations
-----------

The primary limitation of ``InstructionConfigVersion`` is that it
assumes a predefined set of available instruction configurations found
in the ``automata/configs/instruction_configs`` directory. It may be
less flexible for including custom or user-defined instruction sets.

Follow-up Questions:
--------------------

-  How can we extend ``InstructionConfigVersion`` to support custom
   instruction configurations?
