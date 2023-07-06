AgentToolkitNames
=================

``AgentToolkitNames`` is an enumeration class that represents different
types of agent tools in the ``automata.agent.agent`` package. This class
helps manage a collection of agent tools that can be used for distinct
tasks. Each named enum member corresponds to a particular type of agent
tool. The builders for these tools are located in the
``automata/core/agent/builder/`` directory.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample2.PythonAgentToolkit``: A
   class for building tools to interact with a PythonAgent.
-  ``automata.tests.unit.test_automata_agent_builder.test_builder_accepts_all_fields``:
   A test function that demonstrates the use of the builder.
-  ``automata.tools.builders.symbol_search.SymbolSearchOpenAIToolkitBuilder``:
   Builds tools for Open AI.
-  ``automata.tools.builders.context_oracle.ContextOracleOpenAIToolkitBuilder``:
   Builds tools for Context Oracle.
-  ``automata.tools.factory.AgentToolFactory``: A factory class for
   creating tools from a given agent tool name.
-  ``automata.agent.agent.AgentToolkitBuilder``: an abstract class for
   building tools.

Example
-------

Below is a brief example of how you can use ``AgentToolkitNames``:

.. code:: python

   from automata.agent.agent import AgentToolkitNames

   # Get a specific toolkit name
   toolkit_name = AgentToolkitNames.PYTHON

   # You can also list all toolkit names
   all_toolkit_names = list(AgentToolkitNames)

Limitations
-----------

The ``AgentToolkitNames`` enum is limited to the tool names it defines;
you can’t add new names to the enum after it’s defined. If a new tool is
to be supported, its name must be added to this enum class. Remember to
also create a corresponding builder in ``automata/core/agent/builder/``.

Follow-up Questions:
--------------------

-  What specific toolkits exist under each ``AgentToolkitNames``?
-  How are the builders for each ``AgentToolkitNames`` written and
   maintained?
-  Are there any best practices or guidelines when adding new toolkit
   names and their corresponding builders?
