UnknownToolError
================

``UnknownToolError`` is an exception class that gets raised when an
unknown toolkit type is provided. This can occur when attempting to
create an instance of a toolkit that is not recognized or defined by the
system.

Related Symbols
---------------

-  ``automata.core.base.tool.Tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.core.agent.tool.tool_utils.AgentToolFactory``
-  ``automata.tests.unit.test_context_oracle_tool.test_init``

Example
-------

Here’s an example of how ``UnknownToolError`` might be raised when
trying to create an unsupported tool:

.. code:: python

   from automata.core.agent.tool.tool_utils import AgentToolFactory
   from automata.core.agent.error import UnknownToolError

   class UnsupportedTool:
       pass

   try:
       AgentToolFactory.create_tools_from_builder(UnsupportedTool)
   except UnknownToolError as e:
       print(e)

In this example, the ``AgentToolFactory`` attempts to create an instance
of an ``UnsupportedTool``. Since the ``UnsupportedTool`` is not a
recognized tool, the ``UnknownToolError`` will be raised.

Limitations
-----------

The primary limitation of ``UnknownToolError`` is that the error message
provided does not include sufficient context information about why the
specific toolkit type is not recognized or if there is a specific import
issue. This could make debugging and error resolution more difficult for
developers.

Follow-up Questions:
--------------------

-  Are there any plans to improve the error message for
   ``UnknownToolError`` to provide more information to developers?
-  Can ``UnknownToolError`` be extended to handle additional types of
   toolkit-related errors, such as import issues or misconfigured tools?
