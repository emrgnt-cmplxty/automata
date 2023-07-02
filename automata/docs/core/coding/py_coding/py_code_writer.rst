PyCodeWriter
============

``PyCodeWriter`` is a utility class for writing Python code along
Abstract Syntax Tree (AST) nodes. It provides methods to create new
module objects from the source code, update existing modules by
inserting new code or modifying existing code, and delete classes or
functions from existing modules. It leverages
```PyCodeRetriever`` <automata.core.code_handling.py_coding.retriever.PyCodeRetriever>`__
to fetch Python code while providing methods to perform code
modifications.

Overview
--------

``PyCodeWriter`` includes methods for creating, updating, and deleting
code modules. It also has helper methods for replacing newline
characters in a given code string. The primary methods allow interacting
with Python code in a flexible way to create new modules, update
existing ones, or delete code from modules.

Related Symbols
---------------

-  ``automata.core.code_handling.py_coding.retriever.PyCodeRetriever``
-  ``automata.tests.unit.test_py_writer.py_writer``
-  ``automata.core.toolss.py_code_writer.PyCodeWriterTool``
-  ``automata.tests.unit.test_python_writer_tool.python_writer_tool_builder``

Example
-------

The following example demonstrates how to use ``PyCodeWriter`` to create
a new Python module, update it with additional code, and delete a
function from the module:

.. code:: python

   from automata.core.navigation.directory import DirectoryManager
   from automata.core.code_handling.py_coding.retriever import PyCodeRetriever
   from automata.core.code_handling.py_coding.writer import PyCodeWriter

   directory_manager = DirectoryManager("path/to/project")
   retriever = PyCodeRetriever(directory_manager)
   writer = PyCodeWriter(retriever)

   # Create a new Python module
   new_module_code = """
   def example_function():
       print("Hello, World!")
   """
   writer.create_new_module("new_module", new_module_code, do_write=True)

   # Update the existing Python module
   update_code = """
   def another_function():
       print("This is another function.")
   """
   writer.update_existing_module("new_module", update_code, do_write=True)

   # Delete a function from the existing Python module
   writer.delete_from_existing_module("new_module", "another_function")

Limitations
-----------

``PyCodeWriter`` relies on specific directory structures and
configuration setups. It assumes that the modules and code files are
placed in a specific folder structure. Additionally, its dependency
``PyCodeRetriever`` is limited in its ability to only read local Python
files.

Follow-up Questions:
--------------------

-  Can ``PyCodeWriter`` be easily adapted to support custom directory
   structures and configuration setups?
-  Is there a way to use ``PyCodeWriter`` with remote code repositories
   instead of just local files?
