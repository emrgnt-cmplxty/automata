Tool
====

``Tool`` directly exposes a function or coroutine. It takes inputs in
the form of dictionary in a run method. The ``Tool`` class is part of
the automata.core.tools.base module.

Overview
--------

In the larger context of the Automata software architecture, ``Tool`` is
an abstraction that represents a tool or functionality. It encapsulates
a function or routine, exposing it through a ``run`` method that accepts
inputs in form of a dictionary.

The principle use-case is to encapsulate tasks that involve fetching,
processing, or generating data summarized into a single callable method
``run``.

Related Symbols
---------------

-  ``automata.tests.unit.test_tool.test_tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.core.agent.providers.OpenAIAgentToolkitBuilder.can_handle``
-  ``automata.tests.unit.test_tool.test_tool_run``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.tests.unit.test_tool.TestTool.run``
-  ``automata.core.agent.agent.AgentToolkitBuilder.build``
-  ``automata.tests.unit.test_tool.test_tool_instantiation``
-  ``automata.core.tools.builders.symbol_search.SymbolSearchToolkitBuilder.build``
-  ``automata.tests.unit.test_symbol_search_tool.test_build``

Example
-------

The following is an example use-case of creating a ``Tool`` instance,
and running it with an input.

.. code:: python

   from automata.core.tools.base import Tool

   test_tool = Tool(
       name="TestTool", 
       description="A test tool for testing purposes", 
       function=lambda x: "TestTool response")

   # Running the tool
   tool_input = {"test": "test"}
   response = test_tool.run(tool_input)
   # Outputs: "TestTool response"

Limitations
-----------

The ``Tool`` class is designed to execute individually encapsulated
tasks, and is not suitable for managing tasks that involve significant
inter-dependence or require coordination between multiple tasks.

While ``Tool`` instances can be used simultaneously they lack built-in
mechanisms for sharing information between one another, which might
limit application in more complex, real-world scenarios.

Follow-up Questions
-------------------

-  How can ``Tool`` instances communicate with each other when running
   in parallel?
-  Is there a way to make the ``Tool`` capable of handling inter-task
   dependencies?
