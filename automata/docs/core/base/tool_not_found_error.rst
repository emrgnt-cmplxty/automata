ToolNotFoundError
=================

``ToolNotFoundError`` is an exception class that is raised when a
specified tool with a given name cannot be found during the execution of
a toolset. It extends the ``BaseTool`` class and inherits all its
methods and properties.

This error may occur when trying to execute an invalid tool or a tool
that has not been properly loaded into the toolset.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.agent.tools.tool_utils.ToolCreationError``
-  ``automata.core.agent.tools.tool_utils.UnknownToolError``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter.ClassOrFunctionNotFound``
-  ``automata.core.base.tool.InvalidTool``

Usage Example
-------------

.. code:: python

   from automata.core.base.tool import ToolNotFoundError
   from automata.tests.unit.test_tool import TestTool

   def find_tool(tool_name: str):
       available_tools = {"test_tool": TestTool}
       
       try:
           return available_tools[tool_name]()
       except KeyError:
           raise ToolNotFoundError(tool_name)

   try:
       test_tool_instance = find_tool("invalid_tool_name")
   except ToolNotFoundError as e:
       print(e)

Limitations
-----------

``ToolNotFoundError`` assumes that the tool name provided is unique
within the toolset and can unambiguously identify the tool. If there are
duplicate tool names, this error might not accurately pinpoint the
issue. Additionally, the error message generated might not provide
enough context to determine why the tool was not found.

Follow-up Questions:
--------------------

-  How can the error message be improved to provide more information
   about why a tool was not found?
