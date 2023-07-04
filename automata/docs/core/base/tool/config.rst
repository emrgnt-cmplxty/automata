Tool.Config
===========

``Tool.Config`` is a Pydantic configuration class for the ``Tool``
class. This configuration object validates and sets up the properties
like not allowing extra fields (``extra = Extra.forbid``) and allowing
arbitrary types (``arbitrary_types_allowed = True``).

Overview
--------

The ``Tool.Config`` class is part of the
``automata.core.tools.tool.Tool`` class and helps to set up the
configuration for the tool.

Related Symbols
---------------

-  ``automata.core.tools.tool.Tool``
-  ``automata.tests.unit.test_tool.test_tool``
-  ``automata.tests.unit.test_tool.TestTool``
-  ``automata.core.tools.tool.Tool.run``
-  ``automata.core.llm.providers.openai.OpenAITool``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkitBuilder.can_handle``

Example
-------

The following example demonstrates how to create a custom ``Tool`` that
uses the ``Tool.Config`` and is able to run with some input.

.. code:: python

   from automata.core.tools.tool import Tool
   from typing import Dict

   class TestTool(Tool):
       class Config:
           """Configuration for this pydantic object."""
           extra = Extra.forbid
           arbitrary_types_allowed = True

       def run(self, tool_input: Dict[str, str]) -> str:
           return "TestTool response"

   # Usage
   test_tool = TestTool(
       name="TestTool",
       description="A test tool for testing purposes",
       function=lambda x: "TestTool response",
   )
   tool_input = {"test": "test"}
   response = test_tool.run(tool_input)
   print(response)  # Output: TestTool response

Limitations
-----------

The primary limitation of ``Tool.Config`` is that it’s a basic
configuration and might not fulfill all the custom needs for different
tools. The default configuration is set assuming common requirements,
and if your tool needs more specific configuration options, you might
need to extend the ``Tool.Config`` to include your desired configuration
methods and properties.

Follow-up Questions:
--------------------

-  Are there any other configuration options that the ``Tool.Config``
   class should support by default?
-  How can we include more custom configuration options in the
   ``Tool.Config`` class?
