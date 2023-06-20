TestTool
========

``TestTool`` is a simple, test implementation of the Tool class that
returns fixed strings in both synchronous and asynchronous contexts. It
extends the ``Tool`` class and overrides the ``_run`` and ``_arun``
methods, making it a minimal example of how to create a custom tool.

Overview
--------

``TestTool`` demonstrates how to create a basic implementation of the
``Tool`` class by returning fixed strings as responses when calling the
tool synchronously or asynchronously. It serves as a simple example for
developers looking to create their own custom tools.

Related Symbols
---------------

-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.base.tool.Tool``

Example
-------

The following example demonstrates how to create an instance of
``TestTool`` and call its methods:

.. code:: python

   from automata.tests.unit.test_tool import TestTool

   test_tool = TestTool()

   # Synchronous usage
   response = test_tool.run(("input",))
   print(response)  # Output: "TestTool response"

   # Asynchronous usage
   import asyncio

   async def main():
       async_response = await test_tool.arun(("input",))
       print(async_response)  # Output: "TestTool async response"

   asyncio.run(main())

Limitations
-----------

The primary limitation of ``TestTool`` is that it is a very basic
example of implementing the ``Tool`` class and only serves as a
demonstration. In real-world scenarios, more complex tools with specific
functionalities might be required.

Follow-up Questions:
--------------------

-  How can we extend the ``TestTool`` class to add custom
   functionalities or handle different types of input?
