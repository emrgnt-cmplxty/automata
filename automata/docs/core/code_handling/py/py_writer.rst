PyWriter
========

The ``PyWriter`` class is a utility designed for the task of writing
Python code along with its Abstract Syntax Tree (AST) nodes. Namely,
``PyWriter`` provides the foundational structure and tools for creating,
deleting, and updating Python modules.

This class allows for the modification of code within modules, such as
the insertion of new code, deletion of code segments, and updates to
existing modules. Several functionalities of ``PyWriter`` include
creating a new module from source code and writing updates to disk
output when called upon.

``PyWriter`` is typically initialized with a ``PyReader`` object to
assist in reading and writing Python source code.

Related Symbols
---------------

-  ``PyReader``
-  ``PyModuleLoader``
-  ``PyWriterToolkitBuilder``

Example
-------

The following is an example illustrating the usage of ``PyWriter``.

.. code:: python

   from automata.core.code_handling.py.reader import PyReader
   from automata.core.code_handling.py.writer import PyWriter

   # Initialize a PyReader and PyWriter instances
   py_reader = PyReader()
   py_writer = PyWriter(py_reader)

   # Create a new module
   code = 'print("Hello World!")'
   module_name = 'sample_module'
   py_writer.create_new_module(module_name, code, do_write=True)

   # Update existing module
   updated_code = 'print("Hello again, World!")'
   py_writer.update_existing_module(module_name, updated_code)

In the example above, a ``PyWriter`` instance is initialized and then
used to create and update a Python module.

Limitations
-----------

``PyWriter`` depends on the ``PyReader`` instance for reading Python
code. Consequently, the performance and functioning of ``PyWriter`` are
tied to the ``PyReader`` object it has been initialized with.
Additionally, errors in the Python source code or lack of write
permissions could pose potential limitations while trying to write new
modules or update existing ones.

Follow-up Questions
-------------------

-  How are Syntax Errors handled while creating or updating modules?
-  Can ``PyWriter`` support writing and updating of Individual methods
   or classes in a module?
