UnknownToolError
================

``UnknownToolError`` is an exception class that is raised when an
unknown toolkit type is provided. It extends the standard ``Exception``
class in Python and is primarily used in the context of managing
toolkits within the Automata project. This error is specifically used
when the provided ``tool_kit`` variable is not a valid toolkit type.

Related Symbols
---------------

-  ``automata.core.base.tool.ToolNotFoundError``
-  ``automata.core.base.tool.InvalidTool``
-  ``automata.core.agent.tools.tool_utils.ToolCreationError``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.base.tool.ToolkitType``

Example
-------

The following example demonstrates how to catch an ``UnknownToolError``
when attempting to use an invalid toolkit type:

.. code:: python

   from automata.core.agent.tools.tool_utils import UnknownToolError

   def create_toolkit(tool_kit):
       try:
           # This function may raise an UnknownToolError
           toolkit_instance = setup_toolkit(tool_kit)
       except UnknownToolError:
           print(f"Error: Unknown toolkit type '{tool_kit}'")

Limitations
-----------

``UnknownToolError`` only provides information about the invalid toolkit
type input but does not suggest any alternative toolkit type or provide
any functionality to resolve the issue automatically.

Follow-up Questions:
--------------------

-  Are there other exceptions or error classes within the Automata
   project that should be documented more comprehensively?
