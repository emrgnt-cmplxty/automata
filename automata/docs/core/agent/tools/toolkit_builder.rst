ToolkitBuilder
==============

``ToolkitBuilder`` is a utility class for creating ``Tool`` objects from
an ``AgentTool``. By providing a toolkit builder object, it becomes easy
to build and manage tools for an agent. It helps interact with various
tools using the same interface and simplifies the process of building
custom tools for an agent.

Overview
--------

The ``ToolkitBuilder`` class has an ``__init__`` method that initializes
a ToolkitBuilder object with the provided inputs and a ``build`` method
that builds tools from a tool manager. The class can be instantiated
directly and used for building tools with the appropriate ``AgentTool``
provided.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.base.tool.Toolkit``
-  ``automata.core.base.tool.ToolkitType``

Example
-------

The following example demonstrates how to use the ``ToolkitBuilder``
with an ``AgentTool``:

.. code:: python

   from automata.core.agent.tools.agent_tool import AgentTool
   from automata.core.agent.tools.tool_utils import ToolkitBuilder

   class CustomAgentTool(AgentTool):
       def build(self):
           return [Tool("tool_name", tool_function, "tool_description")]

   my_agent_tool = CustomAgentTool()
   my_toolkit_builder = ToolkitBuilder()
   built_tools = my_toolkit_builder.build(agent_tool=my_agent_tool)

Limitations
-----------

The primary limitation of ``ToolkitBuilder`` is that it requires an
``AgentTool`` object to build tools. It cannot build tools directly from
a list of tools or a different toolkit manager object.

Follow-up Questions:
--------------------

-  Are there any alternative approaches to building tools other than
   using an ``AgentTool`` object?
