InvalidTool
===========

``InvalidTool`` is a class that is run when an agent encounters an
invalid tool name. The purpose of this class is to inform the user that
the specified tool name is invalid, and to prompt them to try another
one. This class is a part of the Automata’s core tool handling system,
and it extends the ``BaseTool`` class.

Overview
--------

``InvalidTool`` returns an appropriate error message when it is called
upon encountering an invalid tool name. It works seamlessly with other
tool classes within the Automata framework and provides necessary error
handling for users.

Related Symbols
---------------

-  ``automata.core.base.tool.Toolkit``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.base.tool.ToolNotFoundError``
-  ``automata.core.base.base_tool.BaseTool``

Example
-------

The following example demonstrates how to create an ``InvalidTool``
instance and run it with an invalid tool name:

.. code:: python

   from automata.core.base.tool import InvalidTool

   invalid_tool = InvalidTool()
   response = invalid_tool.run(("InvalidToolName",))
   print(response)  # Output: "('InvalidToolName',) is not a valid tool, try another one."

Additionally, ``InvalidTool`` can be run asynchronously:

.. code:: python

   import asyncio
   from automata.core.base.tool import InvalidTool

   async def main():
       invalid_tool = InvalidTool()
       response = await invalid_tool.arun(("InvalidToolName",))
       print(response)  # Output: "InvalidToolName is not a valid tool, try another one."

   loop = asyncio.get_event_loop()
   loop.run_until_complete(main())

Limitations
-----------

``InvalidTool`` provides a straightforward solution to handle invalid
tool names. This class is straightforward and does not have many
limitations.

Follow-up Questions:
--------------------

-  Are there any alternative methods or strategies that can be employed
   to handle invalid tool names?
-  Is there a need for additional features or functionalities to be
   added within ``InvalidTool``?
