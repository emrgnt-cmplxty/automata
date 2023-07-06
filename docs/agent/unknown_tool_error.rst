UnknownToolError
================

Overview
--------

``UnknownToolError`` is an exception class in the
``automata.agent.error`` module. This exception is raised when an
unknown tool type is provided to the framework.

In broad terms, a tool in this context refers to a callable
functionality of the system (such as ``TestTool`` or any class
inheriting from ``Tool``), which can be invoked with a certain input to
produce a certain output.

For instance, when building tools for an agent like this
``AgentToolFactory.create_tools_from_builder(agent_tool: AgentToolkitNames, **kwargs)``,
if an unrecognized ``agent_tool`` is provided, ``UnknownToolError`` is
raised.

Related Symbols
---------------

-  ``automata.tests.unit.test_tool.test_tool_instantiation``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.tests.unit.test_tool.test_tool_run``
-  ``automata.tools.base.Tool``
-  ``automata.tests.unit.test_context_oracle_tool.test_init``
-  ``automata.agent.providers.OpenAIAgentToolkitBuilder.can_handle``
-  ``automata.tests.unit.test_tool.test_tool``
-  ``automata.tools.factory.AgentToolFactory.create_tools_from_builder``
-  ``automata.tests.unit.test_context_oracle_tool.test_build``
-  ``automata.agent.agent.AgentToolkitBuilder.build``

Usage Example
-------------

.. code:: python

   from automata.tools.factory import AgentToolFactory
   from automata.agent.error import UnknownToolError

   try:
       tool = AgentToolFactory.create_tools_from_builder("NonExistentTool")
   except UnknownToolError as e:
       print(str(e))  # Will print error message about unknown tool type.

Limitations
-----------

``UnknownToolError`` is a basic extension of Python’s built-in
``Exception`` class, and thus shares the same limitations. It’s sole
purpose is to provide meaningful error information when an unrecognized
tool type is provided to the framework. It is not designed to handle
additional error processing or functionality.

As a part of error handling in the ``automata`` library, efficient usage
of this error class assumes that developers using this library have a
handle on the tool types that are permitted to be used.

Follow-up Questions
-------------------

-  What are the specific conditions which may lead to this error beyond
   the tool being unknown or unrecognized?
-  Does this exception handle other edge cases such as the input type
   not matching the expected tool type?
-  Besides the tool name, are there any other parameters or information
   that could be helpful to include in the error message?
