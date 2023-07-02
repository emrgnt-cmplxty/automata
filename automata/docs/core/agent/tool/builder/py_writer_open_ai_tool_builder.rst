PyWriterOpenAIToolkit
=========================

``PyWriterOpenAIToolkit`` is a class for interacting with the
``PyWriter`` API that provides functionality to modify the code state of
a given directory of Python files and build tools suitable for use with
the OpenAI API. This class extends from ``AgentToolkit`` and
``OpenAIAgentToolkit``, allowing it to generate a list of
``OpenAITool`` instances for code writing.

Overview
--------

``PyWriterOpenAIToolkit`` provides a method ``build_for_open_ai`` to
build the tools associated with the Python code writer and return them
as a list of ``OpenAITool`` instances. The built tools can then be used
to write or modify the code in the specified module, class, or function.

Related Symbols
---------------

-  ``automata.core.code_handling.py.writer.PyWriter``
-  ``automata.core.tools.builders.py_writer.PyWriterToolkit``
-  ``automata.core.llm.providers.openai.OpenAIAgentToolkit``
-  ``automata.core.llm.providers.openai.OpenAITool``

Usage Example
-------------

.. code:: python

   from automata.core.code_handling.py.reader import PyReader
   from automata.core.code_handling.py.writer import PyWriter
   from automata.core.tools.builders.py_writer import PyWriterToolkit
   from automata.core.llm.providers.openai import OpenAITool

   py_reader = PyReader()
   py_writer = PyWriter(py_reader)
   py_writer_tool_builder = PyWriterToolkit(py_writer)

   # We assume that PyWriterToolkit is registered in the OpenAIAutomataAgentToolkitRegistry
   open_ai_tools = py_writer_tool_builder.build_for_open_ai()

   for tool in open_ai_tools:
       assert isinstance(tool, OpenAITool)

Limitations
-----------

The primary limitation of ``PyWriterOpenAIToolkit`` is that it works
only with instances of ``PyWriter``, which itself may have its own
limitations. Additionally, it requires that the ``build_for_open_ai``
method is called explicitly to generate the ``OpenAITool`` instances,
which may lead to less intuitive code in some cases.

Follow-up Questions:
--------------------

-  How can we streamline the use of ``PyWriterOpenAIToolkit`` in
   conjunction with the OpenAI API?
