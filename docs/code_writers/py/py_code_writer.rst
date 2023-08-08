PyCodeWriter
============

``PyCodeWriter`` is a Python utility class designed to interpret and
manipulate Python code in the form of Abstract Syntax Tree (AST) nodes.
It enables creating, updating, deleting, and writing Python modules
using AST, providing an interface for programmatically generating and
modifying Python source code.

Overview
--------

``PyCodeWriter`` uses the Python built-in ``ast`` module and
interactions with ``py_module_loader``, an instance of the
``PyModuleLoader`` class, for operations. This class consists of methods
that map to typical file operations. Unique exceptions labeled
``ModuleNotFoundError``, ``StatementNotFoundError`` and
``InvalidArgumentsError``, each provide specific error handling for
common pitfalls.

Related Symbols
---------------

-  ``PyCodeWriter.ModuleNotFoundError``
-  ``PyCodeWriter.StatementNotFoundError``
-  ``PyCodeWriter.InvalidArgumentsError``
-  ``automata.tools.builders.py_writer_builder.PyCodeWriterToolkitBuilder``
-  ``automata.singletons.dependency_factory.DependencyFactory``

Example Usage
-------------

.. code:: python

   from automata.singletons.dependency_factory import DependencyFactory
   from automata.code_writers.py.py_code_writer import PyCodeWriter
   from ast import parse

   # Create an instance of PyCodeWriter
   dep_factory = DependencyFactory()
   py_writer = dep_factory.create_py_writer()

   # Create a new module with a function "foo"
   source_code = """
   def foo():
       return 'Hello, world!'
   """

   py_writer.create_new_module('sample_module', parse(source_code), do_write=True)

   # Update the module "foo" function logic
   source_code_update = """
   def foo():
       return 'Hello from updated world!'
   """
   py_writer.upsert_to_module(
       parse(source_code), 
       parse(source_code_update)
   )

In this example, the method ``create_new_module`` was used to create a
new Python module ``sample_module`` with a function ``foo``. Following
this, the function ``foo``\ ’s logic was updated with
``upsert_to_module`` to change its return string.

Limitations
-----------

``PyCodeWriter`` has strong dependencies on the project and file
structure. It requires the modules to be setup in a specific way. As
such, it may not work accurately if the project structure is not aligned
with its expectations.

Also, ``PyCodeWriter`` heavily relies on the ``ast`` module. It would
not be effective for changes not supported by the ``ast`` module.

In certain operations, such as ``delete_from_module``, there’s a need
for deletion items to already exist in the module, else it will throw an
error. Care must be taken to ensure the preconditions for each operation
are met before execution.

Follow-up Questions:
--------------------

-  Are there safeguards for handling common user errors such as
   attempting to modify a non-existent file or node?
-  How can this class be extended/modified to support different file and
   module structures?
