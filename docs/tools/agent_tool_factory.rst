AgentToolFactory
================

Overview
--------

``AgentToolFactory`` is a class designed to utilize the toolkit registry
to create tools and builders according to provided agent tool names.
This tool factory maintains a mapping of toolkit types to their
arguments, allowing for quick and reliable tool creation. Tools are
fundamental components in handling various tasks like Python code
reading, writing, symbolic search, etc.

The main methods of ``AgentToolFactory`` include
``create_tools_from_builder`` which uses the toolkit registry to create
tools from a given agent tool name, and ``build_tools``, a method that
accepts a list of tool names and generates associated tools accordingly.
For all unknown or unhandled tool names, the factory raises
``UnknownToolError``.

Related Symbols
---------------

-  ``automata.singletons.toolkit_registry.OpenAIAutomataAgentToolkitRegistry``
-  ``automata.tools.builders.py_writer_builder.PyCodeWriterToolkitBuilder.build``
-  ``automata.tools.builders.py_writer_builder.PyCodeWriterOpenAIToolkitBuilder.build_for_open_ai``
-  ``automata.tools.builders.py_reader_builder.PyReaderOpenAIToolkitBuilder.build_for_open_ai``
-  ``automata.core.base.database.relational_database.SQLDatabase.close``
-  ``automata.symbol_embedding.vector_databases.ChromaSymbolEmbeddingVectorDatabase.__init__``
-  ``automata.tools.builders.TaskEnvironment.AutomataTaskEnvironment``

Usage Example
-------------

Here’s a simple example that demonstrates how to use
``AgentToolFactory``:

.. code:: python

   from automata.tools.agent_tool_factory import AgentToolFactory
   from automata.tool_agent_manager import AgentToolkitNames
   toolkits = ['symbol_search', 'py_reader']
   tools = AgentToolFactory.build_tools(toolkits)

In the above example, ``AgentToolFactory`` is imported and utilized to
build tools with the names ‘symbol_search’ and ‘py_reader’.

Limitations
-----------

While the ``AgentToolFactory`` provides significant flexibility in tool
creation, it does rely on the builder registry and canned toolkit types
defined in ``AgentToolkitNames``. This design makes it less adaptable to
toolkits not already defined in the software architecture. Furthermore,
the factory will raise an error if it is asked to build a toolkit that
is not registered or unknown, which could limit its extensibility with
other third-party tools or custom toolkits.

Follow-up Questions:
--------------------

-  Might there be a more flexible way to register new toolkit types
   without modifying internal code or the ``AgentToolkitNames``
   enumerator?
-  How can one implement an extension mechanism to allow support for
   other third-party toolkits outside OpenAI’s prebuilt toolkits?
