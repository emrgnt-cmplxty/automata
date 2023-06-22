Toolkit
=======

``Toolkit`` is a container class that holds a set of tools. Tools are
essentially functions or coroutines that perform specific tasks, used by
agents for various purposes. ``Toolkit`` keeps such tools organized and
simplifies their usage by providing methods for representing the toolkit
and handling its tools.

Overview
--------

``Toolkit`` has an attribute ``tools`` that is a list of the tools it
contains. The primary methods of the ``Toolkit`` class are ``__init__``
for initialization and ``__repr__`` for representing the toolkit as a
string.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.core.agent.tools.tool_utils.ToolkitType``
-  ``automata.core.agent.agent_enums.ToolField``

Example
-------

The following is an example demonstrating how to create an instance of
``Toolkit`` containing a single instance of ``TestTool``.

.. code:: python

   from automata.core.base.tool import Toolkit
   from automata.tests.unit.test_tool import TestTool

   test_tool = TestTool(
       name="TestTool",
       description="A test tool for testing purposes",
       func=lambda x: "TestTool response",
   )

   tools = [test_tool]
   toolkit = Toolkit(tools)

   assert len(toolkit.tools) == 1
   assert isinstance(toolkit.tools[0], TestTool)
   assert toolkit.tools[0].name == "TestTool"

Limitations
-----------

``Toolkit`` assumes that the tools it contains are well-formed instances
of ``Tool`` or subclasses thereof. If a user introduces a malformed
tool, it might lead to unexpected behavior during the execution of an
agent using the toolkit.

Follow-up Questions:
--------------------

-  How can we enforce the validation of tools within the toolkit at
   initialization?
