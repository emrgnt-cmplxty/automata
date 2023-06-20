ToolCreationError
=================

``ToolCreationError`` is an exception class that is raised when a tool
cannot be created. It is used within the ``AgentToolFactory`` class to
raise an error if the required arguments for creating an agent tool are
not provided or if an unknown toolkit type is provided.

Related Symbols
---------------

-  ``agent.tools.tool_utils.UnknownToolError``
-  ``core.base.tool.ToolNotFoundError``
-  ``core.agent.tools.tool_utils.AgentToolFactory``
-  ``core.base.tool.ToolkitType``

Example
-------

The following example demonstrates how to catch a ``ToolCreationError``
when creating an agent tool using the ``AgentToolFactory``.

.. code:: python

   from automata.core.agent.tools.tool_utils import AgentToolFactory, ToolCreationError
   from automata.core.base.tool import ToolkitType

   toolkit_type = ToolkitType.CONTEXT_ORACLE

   try:
       tool = AgentToolFactory.create_agent_tool(toolkit_type)
   except ToolCreationError as e:
       print(f"An error occurred while creating the tool: {e}")

Limitations
-----------

The primary limitation of the ``ToolCreationError`` is that it only
provides an error message upon raising the exception but does not
include specific information about why the tool creation failed or which
required arguments are missing.

Follow-up Questions:
--------------------

-  How can we improve the error message provided by the
   ``ToolCreationError`` to include more specific information about why
   the tool creation failed?
-  Could there be improvements made to the tool creation process in
   ``AgentToolFactory`` that would make ``ToolCreationError`` more
   informative or even unnecessary?
