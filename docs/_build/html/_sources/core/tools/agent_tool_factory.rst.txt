AgentToolFactory
================

Overview
--------

The ``AgentToolFactory`` class is responsible for creating tools from a
given agent tool name. It leverages the system of agent tool names and
the registry of OpenAI Automata Agent toolkit builders to create and
manage tools. The primary methods of the ``AgentToolFactory`` are
``build_tools`` and ``create_tools_from_builder``, which are used for
generating tools and creating tools from builders respectively.

Methods
-------

The ``build_tools`` method creates a collection of tools given a list of
``toolkit_list`` tool names. It loops through the list of available tool
names, for each of them checks whether the agent tool manager can handle
it, and then applies the ``create_tools_from_builder`` function to
create the corresponding tool.

The ``create_tools_from_builder`` function creates tools from a given
``agent_tool`` tool name. This tool name is passed into the builder’s
``can_handle`` function to confirm if the builder can create the
requested tool. Once verified, the tool is created using the builder’s
corresponding build function.

Related Symbols
---------------

-  ``automata.tests.unit.test_tool.test_tool``
-  ``automata.tests.unit.test_tool.test_tool_instantiation``
-  ``automata.core.singletons.toolkit_registries.OpenAIAutomataAgentToolkitRegistry.register_tool_manager``
-  ``automata.tests.unit.test_py_writer_tool.python_writer_tool_builder``

Usage Example
-------------

.. code:: python

   from automata.core.tools.factory import AgentToolFactory
   from automata.core.agent.agent import AgentToolkitNames

   toolkit_list = ["tool_name1", "tool_name2"]
   tools = AgentToolFactory.build_tools(toolkit_list)

Limitations
-----------

The ``AgentToolFactory`` is limited by the builders registered in the
``OpenAIAutomataAgentToolkitRegistry``. If a builder for a desired tool
isn’t registered yet or doesn’t exist, the ``AgentToolFactory`` won’t be
able to create that tool.

Dependencies
------------

Some key dependencies include:

-  OpenAIAutomataAgentToolkitRegistry for querying the builder’s
   registry.
-  AgentToolkitNames for managing and validating tool names.
-  OpenAIAgentToolkitBuilder for building the tools for the OpenAI
   agent.

Follow-up Questions:
--------------------

-  How can we extend the ``AgentToolFactory`` to handle a wider range of
   tools or to handle custom tools?
-  Could there be a more efficient way to create enums from the tool
   names instead of handling them as plan strings?
