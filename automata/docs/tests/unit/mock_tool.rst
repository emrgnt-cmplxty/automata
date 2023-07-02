MockTool
========

``MockTool`` is a mock implementation of the ``BaseTool`` class used for
testing purposes within the Automata project. It provides two simple
methods, ``_run()`` and ``_arun()``, for synchronous and asynchronous
execution respectively. It is mainly used in unit tests where an
instance of a ``BaseTool`` subclass is required but the actual
functionality is not important.

Overview
--------

``MockTool`` inherits from the ``BaseTool`` and provides mock
implementations of the ``_run()`` and ``_arun()`` methods, returning
fixed strings as responses. This class is used in unit tests that
require ``BaseTool`` subclasses but do not need the specific
implementation.

Related Symbols
---------------

-  ``automata.core.base.base_tool.BaseTool``
-  ``automata.core.tools.tool.Tool``
-  ``automata.core.tools.tool.InvalidTool``
-  ``automata.core.tools.tool.Toolkit``
-  ``automata.core.tools.tool.tool``

Example
-------

.. code:: python

   from automata.tests.unit.test_base_tool import MockTool

   tool = MockTool(name="MockTool", description="A mock tool for testing purposes")
   tool_input = ("test",)
   response = tool(tool_input)
   print(response)  # Outputs: "MockTool response"

Limitations
-----------

``MockTool`` is created solely for testing purposes and is not intended
for usage in production code. It has minimal functionality, providing
only simple mock implementations of the ``_run()`` and ``_arun()``
methods. Consequently, using this class for anything other than testing
will not provide meaningful or correct results.

Follow-up Questions:
--------------------

-  Are there any specific usage requirements for ``MockTool`` in the
   unit tests where it is used?
-  Can the ``_run()`` and ``_arun()`` methods be customized to provide
   different responses or side effects when testing? If so, how?
