MockTool
--------

``MockTool`` is a concrete implementation of the ``BaseTool`` class that
is used for testing purposes. It provides a simple tool that returns a
mock response when called. This allows testing your agents or any
tool-related components while mocking the actual functionality.

Important Symbols
~~~~~~~~~~~~~~~~~

-  ``automata.core.base.base_tool.BaseTool``

Example
~~~~~~~

The following is an example demonstrating how to create an instance of
``MockTool`` and use it.

.. code:: python

   from automata.tests.unit.test_base_tool import MockTool

   # Instantiate the MockTool
   tool = MockTool()

   # Running the MockTool
   tool_response = tool.run(("input",))
   print(tool_response)  # Output: "MockTool response"

   # Using the MockTool in an asynchronous context
   import asyncio

   async def main():
       async_response = await tool.arun(("input",))
       print(async_response)  # Output: "MockTool async response"

   asyncio.run(main())

Limitations
~~~~~~~~~~~

As ``MockTool`` is designed for testing and mocking purposes, it should
not be used in production systems or as a practical tool. Its purpose is
to facilitate the testing of more complex tools and systems by
simulating the responses and behavior of a real tool without affecting
the actual functionality.

Follow-up Questions:
~~~~~~~~~~~~~~~~~~~~

-  How can the ``MockTool`` class be extended or modified to include
   more complex test scenarios or responses?
