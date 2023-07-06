InstructionConfigVersion
========================

``InstructionConfigVersion`` is an enumeration class that provides a
listing of possible instruction versions. This corresponds to files
located within the ``automata/configs/instruction_configs`` in the yaml
format. The enumeration currently contains a single instruction version:
``AGENT_INTRODUCTION``.

Overview
--------

The ``InstructionConfigVersion`` class aids in specifying the type of
instructions to be used within the Automata framework. Instructions are
integral to the functioning of the Automata OpenAI Agent as they guide
the behaviour and responses of the agent. They are often represented as
pre-configured yaml files.

Related Symbols
---------------

-  ``automata.tests.unit.test_automata_agent_builder.test_config_loading_different_versions``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfigBuilder.with_instruction_version``
-  ``automata.tests.unit.test_automata_agent.test_build_initial_messages``
-  ``automata.config.openai_agent.OpenAIAutomataAgentConfig``

Example
-------

The following is an example demonstrating how to utilize this Enum
within the ``OpenAIAutomataAgentConfigBuilder`` class.

.. code:: python

   from automata.config.openai_agent import OpenAIAutomataAgentConfigBuilder
   from automata.config.base import InstructionConfigVersion

   # Create an instance of the OpenAIAutomataAgentConfigBuilder
   config_builder = OpenAIAutomataAgentConfigBuilder()

   # Set the instruction version using the InstructionConfigVersion Enum
   config_builder = config_builder.with_instruction_version(InstructionConfigVersion.AGENT_INTRODUCTION)

Limitations
-----------

The ``InstructionConfigVersion`` class currently has limited usefulness
as it only contains a single instruction version. This might be expanded
upon in the future as more instruction versions are developed for the
Automata OpenAI Agent.

Follow-up Questions:
--------------------

-  What different kinds of instructions would warrant their own
   instruction version in the future?
-  Does the single currently available instruction version provide
   enough breadth for the variety of agents that can be created using
   the Automata framework?
