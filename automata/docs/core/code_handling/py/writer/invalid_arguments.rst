PyWriter
========

``PyWriter`` is a utility class in Automata used for writing Python code
along Abstract Syntax Tree (AST) nodes. PyWriter is initialized with an
instance of ``PyReader`` which fetches the Python code. Once
initialized, there are methods available to create, update, and delete
from Python modules.

Related Symbols
---------------

-  ``automata.tests.unit.test_py_writer.py_writer``
-  ``automata.core.code_handling.py.writer.PyWriter``
-  ``automata.tests.unit.test_py_writer_tool.test_init``
-  ``automata.core.singletons.dependency_factory.DependencyFactory.create_py_writer``
-  ``automata.tests.unit.test_py_writer_tool.python_writer_tool_builder``
-  ``automata.core.tools.builders.py_writer.PyWriterToolkitBuilder.__init__``
-  ``automata.tests.unit.test_py_reader.getter``
-  ``automata.core.tools.builders.py_writer.PyWriterToolkitBuilder``
-  ``automata.tests.unit.test_py_writer.test_create_update_write_module``
-  ``automata.core.code_handling.py.reader.PyReader``

Usage Example
-------------

Below is an example illustrating the creation of a new Python module
using ``PyWriter``.

.. code:: python

   from automata.core.code_handling.py.writer import PyWriter
   from automata.core.code_handling.py.reader import PyReader

   # Initializing PyWriter
   py_reader = PyReader()
   py_writer = PyWriter(py_reader)

   # Creating a new Python module
   py_writer.create_new_module(
       module_dotpath="sample_module", 
       source_code="print('Hello, world!')",
       do_write=True
   )

In this example, ``create_new_module`` accepts a module path along with
source code as strings, and a boolean indicating whether to write these
changes to disk. The module’s path is given through dot notation (i.e.,
‘sample_module’).

Limitations
-----------

While the ``PyWriter`` class provides a useful way to modify Python code
programmatically, it has certain limitations. For instance, improper
manipulation of Python code may lead to syntax errors or unexpected
behaviour in the code. Additionally, the automatic writing of changes to
disk may, in some cases, lead to data loss if not used carefully.

Follow-up Questions:
--------------------

-  How does ``PyWriter`` handle potential errors and exceptions when
   writing Python code?
-  How does ``PyWriter`` interact with other Automata components and
   dependencies?
-  What are the best practices to ensure safe and effective usage of
   ``PyWriter``?
