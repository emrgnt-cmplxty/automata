PyWriterToolkitBuilder
===================

``PyWriterToolkitBuilder`` is a class for interacting with the PythonWriter
API, which provides functionality to modify the code state of a given
directory of Python files. This class allows you to manage and update
existing Python files in a directory, create new modules, and delete
specific objects from existing modules.

Overview
--------

The ``PyWriterToolkitBuilder`` class provides a way to build a list of
tools associated with the Python code writer. These tools are used to
create, update, and delete Python files and objects in an existing
directory. It has utility methods to create new modules, update existing
modules, and delete specific objects from existing modules. It includes
related symbols like ``PyWriter``, ``AgentToolkitBuilder``, and ``Tool``.

Import Statements
-----------------

.. code:: python

   import logging
   from typing import List, Optional
   from automata.core.tools.registries import OpenAIAutomataAgentToolkitRegistry
   from automata.core.agent.agent import AgentToolkitBuilder, AgentToolkitNames
   from automata.core.tools.tool import Tool
   from automata.core.code_handling.py.writer import PyWriter
   from automata.core.llm.providers.available import LLMPlatforms
   from automata.core.llm.providers.openai import OpenAIAgentToolkitBuilder, OpenAITool

Related Symbols
---------------

-  ``automata.core.code_handling.py.writer.PyWriter``
-  ``automata.core.agent.agent.AgentToolkitBuilder``
-  ``automata.core.tools.tool.Tool``
-  ``automata.tests.unit.test_py_writer_tool.test_init``
-  ``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkitBuilder``
-  ``automata.tests.unit.test_py_writer_tool.python_writer_tool_builder``
-  ``automata.tests.unit.test_py_reader_tool.python_retriever_tool_builder``
-  ``automata.core.tools.builders.py_reader.PyReaderOpenAIToolkit``
-  ``automata.tests.unit.test_py_writer_tool.test_build``

Example
-------

The following is an example demonstrating how to create an instance of
``PyWriterToolkitBuilder`` and use it to build a list of tools.

.. code:: python

   from automata.tests.unit.test_py_writer_tool import python_writer_tool_builder

   # Instantiate the PyWriterToolkitBuilder
   writer_tool_builder = python_writer_tool_builder

   # Build a list of tools
   tools = writer_tool_builder.build()

   # Check the length of the tools list
   assert len(tools) == 3

   # Loop through the tools and check their types
   for tool in tools:
       assert isinstance(tool, Tool)

Limitations
-----------

``PyWriterToolkitBuilder`` assumes a specific directory structure for the
Python files it interacts with. Additionally, it relies on the
predefined tool functionalities that are built into the class and cannot
load custom tool functionalities without modifying the class directly.

Follow-up Questions:
--------------------

-  How can we include custom tool functionalities for loading into the
   ``PyWriterToolkitBuilder`` class?
