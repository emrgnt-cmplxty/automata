PyCodeWriter
============

``PyCodeWriter`` is a utility class for writing and updating Python code
in the Abstract Syntax Tree (AST) format. It provides an interface for
creating a new Python module, updating an existing one by adding or
removing a class or function, and writing the updated module to disk.

The primary use case for ``PyCodeWriter`` is to enable programmatic
manipulation of Python code, including adding, updating, or deleting
elements like classes, functions, and imports.

Overview
--------

The main functionality provided by ``PyCodeWriter`` includes:

-  Initializing with a ``PyCodeRetriever`` instance, which is used for
   fetching Python code.
-  Creating a new module object from source code.
-  Updating an existing module with new or modified code.
-  Writing the updated module to disk.

Related Symbols
---------------

-  ``automata.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.test_py_writer.python_writer``
-  ``automata.core.coding.py_coding.writer.PyDocWriter``
-  ``automata.core.context.py_context.retriever.PyContextRetriever``
-  ``automata.tests.unit.test_py_code_retriever.getter``

Example
-------

The following is an example demonstrating how to create a new module,
update it by adding a new function, and write the updated module to
disk.

.. code:: python

   from automata.core.coding.py_coding.retriever import PyCodeRetriever
   from automata.core.coding.py_coding.writer import PyCodeWriter

   # Initialize the PyCodeWriter with a PyCodeRetriever instance
   retriever = PyCodeRetriever()
   writer = PyCodeWriter(retriever)

   # Create a new module object from source code
   module_dotpath = "my_module"
   source_code = "def hello():\n    print('Hello, World!')\n"
   writer.create_new_module(module_dotpath, source_code)

   # Update the existing module by adding a new function
   new_function_code = "def goodbye():\n    print('Goodbye, World!')\n"
   writer.update_existing_module(module_dotpath, new_function_code, do_write=True)

Limitations
-----------

The primary limitation of ``PyCodeWriter`` is the reliance on RedBaron
for the manipulation of the Abstract Syntax Tree. RedBaron has some
known limitations and bugs that may affect parsing and generating code
correctly in some cases. Additionally, the support for the RedBaron
library has been relatively low in recent years, which may result in
potential issues remaining unfixed.

Another limitation of ``PyCodeWriter`` is its current error reporting,
which could be improved to provide more meaningful error messages and
guidance for resolving issues.

Follow-up Questions:
--------------------

-  What alternative libraries or frameworks could be used to overcome
   the limitations of RedBaron?
-  How can error reporting be improved in ``PyCodeWriter`` for better
   user experience?
