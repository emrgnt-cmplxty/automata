PyWriter
========

``PyWriter`` is a utility class for writing Python code along AST nodes.
It allows to create, update, and delete modules in a Python project. The
class employs Abstract Syntax Trees (AST) to perform various operations
such as updating an existing module or deleting a module object from an
existing module. It also provides methods to replace and modify newline
characters in the input strings.

Overview
--------

``PyWriter`` is initialized with a ``PyReader`` instance, which helps in
reading Python code. The class provides methods to create and manage
Python modules within a project, such as creating a new module, updating
an existing module, and deleting an object from an existing module. It
also has utility methods to replace newline characters in input strings.

Related Symbols
---------------

-  ``automata.core.coding.py.reader.PyReader``
-  ``automata.core.agent.tool.tool_utils.DependencyFactory.create_py_writer``
-  ``automata.core.agent.tool.builder.py_writer.PyWriterToolBuilder``
-  ``automata.core.agent.tool.builder.py_writer.PyWriterOpenAIToolBuilder``

Example
-------

The following is an example demonstrating how to create an instance of
``PyWriter`` and perform operations like creating a new module,
updating, and deleting.

.. code:: python

   from automata.core.coding.py.reader import PyReader
   from automata.core.coding.py.writer import PyWriter

   # Initialize PyReader and PyWriter
   py_reader = PyReader()
   py_writer = PyWriter(py_reader)

   # Create a new module
   module_dotpath = "sample_modules.sample_module_new"
   source_code = "class SampleClass:\n    def sample_method(self):\n        pass"
   py_writer.create_new_module(module_dotpath, source_code, do_write=True)

   # Update the existing module
   source_code_updated = "def new_method():\n    print('New method added')"
   py_writer.update_existing_module(module_dotpath, source_code_updated, do_write=True)

   # Delete an object from the existing module
   object_dotpath = "SampleClass.sample_method"
   py_writer.delete_from_existing__module(module_dotpath, object_dotpath, do_write=True)

Limitations
-----------

``PyWriter`` deals with AST nodes, which may lead to some edge cases
that are hard to handle. Also, managing newline characters might not be
perfect in all situations.

Follow-up Questions:
--------------------

-  What are some edge cases with AST nodes that ``PyWriter`` might find
   hard to handle?
-  Can the newline character management be further optimized?
