Tool
====

``Tool`` is a class that allows users to define a tool or skill for an
LLM by taking in a function or coroutine directly. It inherits from the
``BaseTool`` class and provides an easy interface to create a custom
tool with minimal boilerplate.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.tests.unit.test_base_tool.MockTool``
-  ``automata.core.agent.agent_enums.ToolField``

Example
-------

The following is an example demonstrating how to create an instance of
the ``Tool`` class using a simple function for demonstration purposes:

.. code:: python

   from automata.core.base.tool import Tool

   def example_function(input: str) -> str:
       return f"Processed: {input}"

   tool = Tool(name="ExampleTool", func=example_function, description="Example tool for demonstration.")

Limitations
-----------

The ``Tool`` class creates a custom tool by taking a function or
coroutine directly, which might not be suited for more complex tools or
skills that require state management or more intricate interactions with
other components of the system. For more complex use cases, consider
subclassing ``BaseTool`` and implementing ``_run`` and ``_arun`` methods
instead.

Follow-up Questions
-------------------

-  How can we make the Tool class more suitable for more complex tools
   or skills?
