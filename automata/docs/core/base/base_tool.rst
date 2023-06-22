BaseTool
========

``BaseTool`` is an abstract base class responsible for defining tools or
skills for an LLM. These tools can be callable, which allow them to
accept and respond to string input. ``BaseTool`` provides methods to run
tools both synchronously and asynchronously.

Overview
--------

The primary purpose of the ``BaseTool`` class is to provide a basic
structure for creating various tools to be used by an LLM. The main
methods in this class are:

-  ``__call__``: Allows tools to be callable with string input.
-  ``run``: Runs the tool and returns a string output.
-  ``arun``: Runs the tool asynchronously and returns a string output.

``BaseTool`` is designed to be subclassed to create custom tools,
providing specific implementations for ``_run`` and ``_arun`` methods.

Related Symbols
---------------

-  ``automata.core.base.tool.Tool``
-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.base.tool.Toolkit``
-  ``automata.core.base.tool.InvalidTool``
-  ``automata.tests.unit.test_base_tool.MockTool``: This mock object is
   used for testing purposes; refer to actual implementations of
   ``BaseTool`` as examples.

Example
-------

Here’s an example of creating a custom tool by subclassing ``BaseTool``:

.. code:: python

   from automata.core.base.base_tool import BaseTool
   from typing import Optional, Tuple

   class MyTool(BaseTool):
       def _run(self, tool_input: Tuple[Optional[str], ...]) -> str:
           # Custom logic for synchronous run
           return "MyTool response"

       async def _arun(self, tool_input: Tuple[Optional[str], ...]) -> str:
           # Custom logic for asynchronous run
           return "MyTool async response"

   tool = MyTool(name="MyTool", description="A custom tool")
   tool_input = ("input",)
   response = tool(tool_input)
   print(response)  # Output: "MyTool response"

Limitations
-----------

-  You must subclass ``BaseTool`` and provide custom implementations of
   ``_run`` and ``_arun`` methods to create functional tools.
-  ``BaseTool`` expects input to be provided as tuples, which may not be
   suitable for all use cases.

Follow-up Questions:
--------------------

-  Are there any examples of predefined tools that inherit from
   ``BaseTool`` for reference?
-  Does ``BaseTool`` support any additional features or configuration
   options such as default values or error handling?
