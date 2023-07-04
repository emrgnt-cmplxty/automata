Tool
====

``Tool`` is a base class that defines a tool to perform a specific
function or coroutine. Tools can be used as building blocks in larger
applications or libraries. Tools are created by inheriting the ``Tool``
base class and implementing its methods, primarily the ``run`` method.

Overview
--------

``Tool`` is designed to make it easy to create standalone tools that can
be reused and combined in various ways. It provides a structure for
defining a tool and standardizes how tools should be used. The primary
purpose of a tool is to perform a specific function, which can be either
synchronous or asynchronous. This is done by implementing the ``run``
method, which takes a dictionary of input parameters and returns the
output of the tool’s operation as a string.

Related Symbols
---------------

-  ``automata.tests.unit.test_tool.test_tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.tests.unit.test_tool.test_tool_run``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.tests.unit.test_tool.test_tool_instantiation``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkitBuilder.can_handle``
-  ``automata.tests.unit.test_tool.TestTool.run``
-  ``automata.core.agent.agent.AgentToolkitBuilder.build``
-  ``automata.tests.unit.test_symbol_search_tool.test_build``
-  ``automata.core.tools.tool_utils.AgentToolFactory``

Example
-------

Here’s an example demonstrating the creation of a custom ``Tool``
subclass, called ``TestTool``.

.. code:: python

   from automata.core.tools.tool import Tool
   from typing import Dict

   class TestTool(Tool):
       def run(self, tool_input: Dict[str, str]) -> str:
           return "TestTool response"

   test_tool = TestTool(
       name="TestTool",
       description="A test tool for testing purposes",
       function=lambda x: "TestTool response",
   )

   tool_input = {"test": "test"}
   response = test_tool.run(tool_input)
   assert response == "TestTool response"

Limitations
-----------

The ``Tool`` class assumes that the primary method of interaction with
the tool is through its ``run`` method. This might not be ideal for all
use cases, especially where the requirements are significantly more
complex than simply calling a function with a dictionary of input
parameters.

Follow-up Questions:
--------------------

-  How can we enhance the ``Tool`` class to support more complex
   workflows or additional features?
