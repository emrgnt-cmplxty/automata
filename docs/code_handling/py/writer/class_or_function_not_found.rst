PyWriter
========

``PyWriter`` is a utility class that facilitates the writing of Python
code along AST (Abstract Syntax Tree) nodes. It offers various
functionalities such as creating new Python modules, updating existing
modules, and deleting from existing modules, among others. It leverages
a ``PyReader`` instance, which fetches Python code, to initialize and
carry out its operations.

In addition to the primary ``PyWriter`` class, this document makes
reference to additional closely related symbols such as ``PyReader``,
``PyWriterToolkitBuilder``, ``PyWriter.ClassOrFunctionNotFound``, and so
on.

Related Symbols
---------------

-  ``automata.code_handling.py.reader.PyReader``
-  ``automata.tools.builders.py_writer.PyWriterToolkitBuilder``
-  ``automata.code_handling.py.writer.PyWriter.ClassOrFunctionNotFound``
-  ``automata.tests.unit.test_py_writer.py_writer``
-  ``automata.tests.unit.test_py_writer_tool.python_writer_tool_builder``
-  ``automata.tests.unit.test_py_writer_tool.test_init``
-  ``automata.tests.unit.test_py_reader.getter``
-  ``automata.tests.unit.test_py_writer.test_create_update_write_module``

Example
-------

An indicative Python session using ``PyWriter`` would look something
like the following:

.. code:: python

   from automata.code_handling.py.reader import PyReader
   from automata.code_handling.py.writer import PyWriter

   py_reader = PyReader()  # Creating an instance of PyReader
   py_writer = PyWriter(py_reader)  # Initializing PyWriter with a PyReader instance

   source_code = """
   def greet(name):
       return f"Hello, {name}!"
   """  # Python code that we aim to insert into a module

   module_dotpath = "module.name"  # The module into which we want to insert Python code

   # The following line will insert 'source_code' into the python file specified by 'module_dotpath'
   py_writer.create_new_module(module_dotpath, source_code, do_write=True)

Note: If the Python file specified by ``module_dotpath`` does not exist,
it will be created in the process.

Limitations
-----------

The primary constraint of ``PyWriter`` is that it relies on the
``PyReader`` instance passed to it during initialization for fetching
Python code. If the ``PyReader`` instance is associated with incorrect
or inaccessible Python modules, ``PyWriter`` might fail.

Follow-up Questions:
--------------------

1. How does ``PyWriter`` handle class hierarchy and nested classes when
   writing to AST nodes?
2. What are the limitations of using ``PyWriter`` on different types of
   Python modules, such as those containing metaclasses, dynamically
   generated code, etc.?
3. Can the ``PyWriter`` class handle conflict resolution in case of
   module name clashes?
