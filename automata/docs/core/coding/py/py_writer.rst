PyWriter
========

``PyWriter`` is a utility class for writing Python code along Abstract
Syntax Tree (AST) nodes. It provides the ability to create, update, and
delete Python modules in an existing codebase. The class utilizes
RedBaron for syntax tree manipulations.

Overview
--------

``PyWriter`` uses a ``PyReader`` instance, which is another utility
class for reading Python code, to perform its functionalities. It
exposes methods for creating new modules, updating existing modules, and
deleting items from existing modules. Additionally, it offers utility
functions to replace newline characters and write module changes to
disk. This class is particularly useful when automating code-generation
processes or modifying existing Python code in a dynamic manner.

Related Symbols
---------------

-  ``automata.core.code_handling.py.reader.PyReader``
-  ``automata.tests.unit.test_py_writer.py_writer``
-  ``automata.core.singletons.dependency_factory.create_py_writer``
-  ``automata.tests.unit.test_py_writer_tool.PyWriterOpenAIToolkit``
-  ``automata.core.tools.builders.py_writer.PyWriterToolkit``

Example
-------

The following example demonstrates how to create and update a Python
module using ``PyWriter``.

.. code:: python

   from automata.core.code_handling.py.reader import PyReader
   from automata.core.code_handling.py.writer import PyWriter

   # Initialize PyWriter with a PyReader instance
   py_reader = PyReader()
   py_writer = PyWriter(py_reader)

   # Create a new module with some source code
   source_code = """def example_function():
       print("Hello, world!")
   """
   module_dotpath = "sample_module"
   py_writer.create_new_module(module_dotpath, source_code, do_write=True)

   # Update the existing module with additional source code
   additional_source_code = """def another_example_function():
       print("Welcome to PyWriter!")
   """
   py_writer.update_existing_module(module_dotpath, additional_source_code, do_write=True)

In this example, a new Python module called ``sample_module`` is created
with an ``example_function``, and then updated to include another
function, ``another_example_function``.

Limitations
-----------

The main limitation of ``PyWriter`` is that it’s specifically designed
for Python code and cannot be used for other programming languages.
Furthermore, it assumes a certain project directory structure and relies
on the built-in module loader.

Follow-up Questions:
--------------------

-  Is it possible to extend ``PyWriter`` to support other programming
   languages?
-  How can we improve the flexibility of ``PyWriter`` to handle
   different project directory structures?
