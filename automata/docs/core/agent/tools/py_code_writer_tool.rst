PyCodeWriterTool
================

``PyCodeWriterTool`` is a class for interacting with the PythonWriter
API, which provides functionality to modify the code state of a given
directory of Python files. It is a subclass of ``AgentTool`` and works
by defining a set of associated tools to perform code writing tasks such
as updating existing modules, creating new modules, or deleting objects
from existing modules.

Overview
--------

``PyCodeWriterTool`` is built on top of the ``PyCodeWriter`` utility
class, which itself is a wrapper to interact with Python abstract syntax
trees. The primary goal of ``PyCodeWriterTool`` is to expose
functionality for updating existing modules, creating new modules, or
deleting objects from existing modules through a set of tools that can
be used by an agent in the context of code manipulation tasks. It can be
used alongside other agent-related classes like ``AutomataAgent`` and
``AgentConfigName`` to create powerful agents capable of code writing
tasks.

Related Symbols
---------------

-  ``automata.core.agent.tools.py_code_writer.PyCodeWriterTool``
-  ``automata.core.base.tool.Tool``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.config.config_types.AgentConfigName``
-  ``automata.core.agent.agent.AutomataAgent``
-  ``automata.core.symbol.symbol_types.Symbol``

Usage Example
-------------

.. code:: python

   from automata.core.agent.tools.py_code_writer import PyCodeWriterTool
   from automata.core.coding.py_coding.writer import PyCodeWriter
   from automata.config.config_types import AgentConfigName
   from automata.core.base.tool import Tool
   from automata.core.coding.py_coding.retriever import PyCodeRetriever

   # Create a PyCodeRetriever
   retriever = PyCodeRetriever()

   # Create a PyCodeWriter using the PyCodeRetriever
   writer = PyCodeWriter(py_retriever=retriever)

   # Initialize PyCodeWriterTool
   py_code_writer_tool = PyCodeWriterTool(py_writer=writer, automata_version=AgentConfigName.AUTOMATA_WRITER)

   # Build the associated tools
   tools = py_code_writer_tool.build()

   # Use created tools to interact with code modifications
   new_code = 'def example_function():\n    """An example function"""\n    print("Hello, world!")\n'
   tool_to_update_module = tools[0]
   result = tool_to_update_module.func(('my_project.my_module', 'ClassName', new_code))

   # Access the other tools using indices from 'tools' list
   tool_to_create_new_module = tools[1]
   tool_to_delete_from_existing_module = tools[2]

Limitations
-----------

The main limitation of ``PyCodeWriterTool`` is that it currently focuses
on updating, creating, and deleting functions, classes, or methods in
Python modules. It does not provide a built-in mechanism for modifying
other types of statements or handling more complex code structures.
Furthermore, to perform code modification tasks, users need to follow
the required input parameters and format for the tools, which can be
cumbersome and limiting in some cases.

Follow-up Questions:
--------------------

-  Are there any plans to extend the current functionality of
   ``PyCodeWriterTool`` to support more complex code modifications?
-  Is there any preferred formatting for input code when utilizing the
   associated tools, considering that the input code should be directly
   modifiable by the tools?
