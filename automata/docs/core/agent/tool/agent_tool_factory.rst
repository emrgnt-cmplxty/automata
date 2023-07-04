AgentToolFactory
================

``AgentToolFactory`` is a factory class that creates tool instances for
different types of providers using builders. It uses a static method,
``create_tools_from_builder``, to generate tools based on the agent tool
enumerator and builder registry.

The tool factory can be utilized to create multiple tools, keeping the
code cleaner and more maintainable. Its usage mainly involves creating
tools for various agent types and their respective providers.

Related Symbols
---------------

-  ``automata.core.tools.registries.OpenAIAutomataAgentToolkitRegistry``
-  ``automata.core.agent.agent.AgentToolkitNames``
-  ``automata.core.tools.tool.Tool``
-  ``automata.core.code_handling.py.reader.PyReader``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkitProvider``
-  ``automata.core.experimental.search.symbol_search.SymbolSearch``
-  ``automata.core.agent.error.UnknownToolError``

Usage Example
-------------

The following example demonstrates how to create tools using the
``AgentToolFactory``:

.. code:: python

   from automata.core.tools.tool_utils import AgentToolFactory
   from automata.core.agent.agent import AgentToolkitNames

   # Choose any supported AgentToolkitNames instance
   agent_tool = AgentToolkitNames.CHAT_COMPLETION
   # Create tools
   created_tools = AgentToolFactory.create_tools_from_builder(agent_tool)

Overview
--------

``AgentToolFactory`` checks the tool builders available in
``OpenAIAutomataAgentToolkitRegistry`` and determines which builder
can handle the given agent tool instance. It returns created tools
depending on the platform the tool is built for. If the tool builder
can’t handle the agent tool, it raises an ``UnknownToolError``.

Limitations
-----------

The current implementation of ``AgentToolFactory`` assumes all supported
platforms are part of the ``LLMPlatforms`` enumeration. If new platforms
are introduced in the future, it is necessary to update the
implementation accordingly. Moreover, it depends on the
``OpenAIAutomataAgentToolkitRegistry``, and adding or updating
builders should be done in this registry.

Follow-up Questions:
--------------------

-  How can we modify ``AgentToolFactory`` to support additional
   platforms without making major changes?
-  How can we extend this design to include more default tool builders
   without registering them explicitly in the
   ``OpenAIAutomataAgentToolkitRegistry``?
