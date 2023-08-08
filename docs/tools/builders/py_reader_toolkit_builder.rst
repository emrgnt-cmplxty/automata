PyReaderToolkitBuilder
======================

Overview
--------

``PyReaderToolkitBuilder`` is a class designed to provide an interface
with Python’s Indexer API, allowing direct retrieval of Python code. By
instantiating the ``PyReaderToolkitBuilder`` with a ``PyReader`` object,
users can construct tools that retrieve a Python package’s code,
including modules, standalone functions, classes or methods. Two types
of tools can be built: one for retrieving raw code and the other for
retrieving docstrings only.

Two private methods ``_run_indexer_retrieve_code`` and
``_run_indexer_retrieve_docstring`` in the class are the underlying
functions behind these tools. They attempt to fetch the source code or
docstring correspondingly, and return a failure message in case an
exception occurs.

Related Symbols
---------------

The related symbols associated with the ``PyReaderToolkitBuilder`` class
are:

-  ``automata.tools.builders.agent_toolkit_builder.AgentToolkitBuilder``
-  ``automata.common.types.PyReader``
-  ``automata.common.types.Tool``
-  ``typing.List``.
-  ``typing.Optional``

Usage Example
-------------

Before constructing the tools, you will first need a ``PyReader``
object. Suppose ``mock_py_reader`` is your ``PyReader`` object.

.. code:: python

   from automata.common.types.tool import Tool
   from automata.tools.builders.py_reader_builder import PyReaderToolkitBuilder

   # Instantiate PyReaderToolkitBuilder
   py_reader_builder = PyReaderToolkitBuilder(mock_py_reader)

   # Build Tools
   tools = py_reader_builder.build()

   for tool in tools:
       if tool.name == 'retrieve-code':
           # Retrieve source code
           result = tool.function('module_directory.target_module', 'TargetClass.target_function')
           print("Source Code: ", result)
       elif tool.name == 'retrieve-docstring':
           # Retrieve docstring
           result = tool.function('module_directory.target_module', 'TargetClass.target_function')
           print("Docstring: ", result)

In the above example, ``module_directory.target_module`` is the path to
the Python file and ``TargetClass.target_function`` is the function
defined in the ``TargetClass`` in the module we wish to retrieve.
Replace these with the actual values as per your requirements.

Limitations
-----------

``PyReaderToolkitBuilder`` depends on its ``PyReader`` attribute, an
instance of the ``PyReader`` class. It is possible to encounter
exceptions during the retrieval of Python code due to reasons such as
incorrect paths or missing files. These exceptions are captured and
returned as error messages.

In the current implementation, it is assumed that the desired Python
files are local and accessible. Therefore, fetching code from remote or
protected directories may not be directly supported.

Follow-up Questions:
--------------------

-  How can we make this class handle remote or restricted files or
   directories?
-  Can we add more tools into the ``build`` method to retrieve other
   components of Python code such as class variables or decorators?
