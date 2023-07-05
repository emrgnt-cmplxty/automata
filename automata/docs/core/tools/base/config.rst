Tool
====

``Tool`` is a class that exposes a function or coroutine directly. It
can be used throughout the Automata System and is highly customizable
and versatile.

Overview
--------

The ``Tool`` class in Automata includes a method ``run`` that takes a
dictionary input and returns a string. In simple terms, a ``Tool``
performs specific tasks or operations, given some input.

Related Symbols
---------------

-  ``automata.tests.unit.test_tool.test_tool``: A fixture that produces
   a test tool for testing purposes.
-  ``automata.tests.unit.test_tool.TestTool``: A subclass of ``Tool``
   used for testing purposes.
-  ``automata.core.agent.providers.OpenAIAgentToolkitBuilder.can_handle``:
   A method that checks if a tool can be handled.
-  ``automata.tests.unit.test_tool.test_tool_run``: A function that
   tests the ``run`` method of a tool.
-  ``automata.core.llm.providers.openai.OpenAITool``: A subclass of
   ``Tool`` that is designed for use by the OpenAI agent.
-  ``automata.core.agent.agent.AgentToolkitBuilder.build``: A method
   that builds a list of tools.
-  ``automata.core.tools.builders.symbol_search.SymbolSearchToolkitBuilder.build``:
   A method that builds a list of symbol search toolkits.

Example
-------

The following are examples demonstrating the use of ``Tool``:

Example of defining a ``Tool``:

.. code:: python

       class TestTool(Tool):
           def run(self, tool_input: Dict[str, str]) -> str:
               return "TestTool response"

Example of using a ``Tool``:

.. code:: python

       tool_input = {"test": "test"}
       response = test_tool.run(tool_input)
       assert response == "TestTool response"

Limitations
-----------

``Tool`` is a highly abstract class that by itself does not do much.
It’s supposed to be extended to perform specific tasks. When subclassing
``Tool``, the implementation of some methods is required.

Follow-up Questions:
--------------------

-  Providing more specialized examples of ``Tool`` subclasses may help
   users to understand the concept behind this class better, but such
   examples are not found in the provided context. Could we get these
   examples?
-  How can custom ``Tool`` classes be integrated into the Automata
   system?
-  Are there specific rules or recommendations when implementing the
   ``run`` method of a ``Tool`` subclass?
