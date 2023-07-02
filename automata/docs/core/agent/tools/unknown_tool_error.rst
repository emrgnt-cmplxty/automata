UnknownToolError
================

``UnknownToolError`` is an exception class that is raised when an
unknown toolkit type is provided. It inherits from the ``Exception``
class and overrides the ``__init__`` method to provide a custom error
message.

Related Symbols
---------------

-  ``automata.core.tools.tool.ToolNotFoundError``
-  ``automata.tests.unit.test_tool.test_invalid_tool``
-  ``automata.tests.unit.test_tool.test_invalid_tool_async``
-  ``automata.core.tools.tool.InvalidTool``
-  ``automata.tests.unit.test_base_tool.TestTool``
-  ``automata.tests.unit.test_base_tool.MockTool``
-  ``automata.core.toolss.tool_utils.ToolCreationError``

Example
-------

Here’s an example showcasing the use of ``UnknownToolError``. Note that
this example assumes an unknown toolkit type.

.. code:: python

   from automata.core.tools.tool import ToolkitType
   from automata.core.toolss.tool_utils import UnknownToolError

   def get_tool_by_toolkit(toolkit_type: ToolkitType):
       if toolkit_type == ToolkitType.UNKNOWN:
           raise UnknownToolError(toolkit_type)
       # ... (handle other toolkit types)

   try:
       get_tool_by_toolkit(ToolkitType.UNKNOWN)
   except UnknownToolError as e:
       print(e)  # Prints: "Error: Unknown toolkit type: ToolkitType.UNKNOWN"

Limitations
-----------

The primary limitation of ``UnknownToolError`` is that it only handles a
single type of error - when an unknown toolkit type is provided. It does
not cover other scenarios where errors could occur, such as when a tool
cannot be created or a tool is not found.

Follow-up Questions:
--------------------

-  Are there any other scenarios where creating a custom error class
   like ``UnknownToolError`` would be beneficial in the process of
   handling errors?
