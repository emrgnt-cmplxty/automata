AgentTool
=========

``AgentTool`` is an abstract class for building tools for agents. It is
primarily used as a base class for creating specialized tools that can
be utilized by the agents.

Related Symbols
---------------

-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.action.AutomataActionExtractor``

Example
-------

To create a new tool, simply subclass ``AgentTool`` and implement its
abstract ``build`` method. The following example demonstrates how to
create a custom tool called ``MyTool``:

.. code:: python

   from automata.core.agent.tools.agent_tool import AgentTool

   class MyTool(AgentTool):

       def __init__(self):
           super().__init__()

       def build(self):
           # Implement the custom logic for the tool
           pass

Usage
-----

Once a custom tool is created, it can be used in combination with the
agents. Here’s an example of how to use the ``MyTool`` class with an
``AutomataAgent``:

.. code:: python

   from automata.core.agent.agent import AutomataAgent
   from automata.config.automata_agent_config import AutomataAgentConfig
   from config.config_enums import AgentConfigName
   from my_tool import MyTool

   config_name = AgentConfigName.AUTOMATA_MAIN
   config = AutomataAgentConfig.load(config_name)
   tool = MyTool()

   agent = AutomataAgent(instructions="Some instructions", config=config)
   agent.add_tool(tool)
   agent.run()

Limitations
-----------

Since ``AgentTool`` is an abstract class, it cannot be used directly as
a standalone tool. It serves as a base for creating specialized tools.

Follow-up Questions:
--------------------

-  How do we add multiple custom tools to the agent?
