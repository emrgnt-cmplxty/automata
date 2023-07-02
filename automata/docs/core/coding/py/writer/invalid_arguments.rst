PyWriter
========

``PyWriter`` is a utility class for writing Python code along AST
(Abstract Syntax Tree) nodes. It is used together with the ``PyReader``
class to create, update, and delete Python code for specified modules
and objects within those modules. The primary functionalities of
``PyWriter`` include creating a new module, updating an existing module,
and deleting an object from an existing module. PyWriter is suited for
scenarios where code modifications need to be done programmatically.

Related Symbols
---------------

-  ``automata.core.code_handling.py.reader.PyReader``
-  ``automata.core.tools.builders.py_writer.PyWriterToolkit``
-  ``automata.tests.unit.test_py_writer_tool.test_init``
-  ``automata.core.singletons.dependency_factory.create_py_writer``
-  ``automata.core.tools.builders.py_writer.PyWriterOpenAIToolkit``

Usage Example
-------------

The following example demonstrates how to use ``PyWriter`` to create and
update a Python module by providing the ``source_code`` input.

.. code:: python

   import os
   from automata.core.code_handling.py.reader import PyReader
   from automata.core.code_handling.py.writer import PyWriter

   # Initialize the PyReader and PyWriter instances
   py_reader = PyReader()
   py_writer = PyWriter(py_reader)

   # Create a new Python module with the provided source code
   source_code = "def example_function():\n    return 'This is an example function'"
   module_dotpath = "example_module"
   py_writer.create_new_module(module_dotpath, source_code, do_write=True)

   # Update the existing Python module to include an additional function
   new_source_code = "def another_function():\n    return 'This is another function'"
   py_writer.update_existing_module(module_dotpath, new_source_code, do_write=True)

This example creates a new Python module named ``example_module.py``
with the provided source code and then updates it by adding an
additional function. Note that ``do_write=True`` is set in the method
call to actually modify the file.

Limitations
-----------

The primary limitation of ``PyWriter`` is that it relies on a specific
AST manipulation library, ``redbaron``, which may not always be
up-to-date with the latest Python syntax features. Additionally, it
assumes a specific directory structure for the Python modules to be
manipulated. Also, PyWriter doesn’t automatically handle import
statements when modifying code.

Follow-up Questions:
--------------------

-  What workarounds can be used to handle import statements when using
   ``PyWriter``?
