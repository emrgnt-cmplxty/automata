PyCodeRetrieverTool
===================

``PyCodeRetrieverTool`` is a class for interacting with the
PythonIndexer API, which provides functionality to read the code state
of local Python files.

Overview
--------

``PyCodeRetrieverTool`` works as a tool to retrieve code, docstrings, or
raw code from Python files using the ``PyCodeRetriever`` object. The
tool can be used with an ``AutomataAgent`` to perform code retrieval
tasks. It exposes methods that can be used to build and return tools to
fetch code, docstrings, or raw code from the specified Python paths.

Related Symbols
---------------

-  ``automata.core.agent.tools.agent_tool.AgentTool``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever.get_source_code_without_docstrings``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever.get_docstring``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever.get_source_code``

Example
-------

The following example demonstrates how to create an instance of
``PyCodeRetrieverTool`` and use it to retrieve code, docstrings, or raw
code from Python files.

.. code:: python

   from automata.core.agent.tools.py_code_retriever import PyCodeRetrieverTool
   from automata.core.coding.py_coding.retriever import PyCodeRetriever

   py_retriever = PyCodeRetriever()
   py_code_retriever_tool = PyCodeRetrieverTool(py_retriever=py_retriever)
   tools = py_code_retriever_tool.build()

   # Retrieve code without docstrings
   tool_retrieve_code = tools[0]
   code = tool_retrieve_code.func(('my_directory.my_file', None, 'my_function'))
   print(code)

   # Retrieve docstrings
   tool_retrieve_docstring = tools[1]
   docstring = tool_retrieve_docstring.func(('my_directory.my_file', 'MyClass.my_function'))
   print(docstring)

   # Retrieve raw code
   tool_retrieve_raw_code = tools[2]
   raw_code = tool_retrieve_raw_code.func(('my_directory.my_file'))
   print(raw_code)

Limitations
-----------

The primary limitation of ``PyCodeRetrieverTool`` is that it only
supports retrieving code, docstrings, or raw code from Python files. It
cannot work with other programming languages or file formats.
Additionally, its performance heavily depends on the underlying
``PyCodeRetriever`` object.

Follow-up Questions:
--------------------

-  How can we extend the ``PyCodeRetrieverTool`` to support other
   programming languages?
-  Is there any potential performance issue when using
   ``PyCodeRetrieverTool`` with large codebases?
