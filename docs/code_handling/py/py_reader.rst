PyReader
========

``PyReader`` is a class built for fetching and handling python code. It
primarily provides functionality to get python source code and
documentation from specified modules, classes, or functions/methods. It
also supports the removal of docstrings from python source code it
fetches.

Overview
--------

The ``PyReader`` interacts with the python module loader to fetch
specific modules based on the given dot-path format e.g.,
``package.module``. This class also contains methods to retrieve
docstrings from nodes or python code objects by interacting with the
syntax trees of these objects directly.

Related Symbols
---------------

-  ``PyWriter``: A utility class for writing Python code along AST
   nodes.
-  ``PyModuleLoader``: Class for loading python modules.
-  ``PyReaderToolkitBuilder``: A class for arranging components of
   ``PyReader``.

Example
-------

The following example demonstrates how to create an instance of
``PyReader`` and fetch python source code of specific modules:

.. code:: python

   from automata.code_handling.py.reader import PyReader

   py_reader = PyReader()
   module_dotpath = "package.module"
   node_path = "ClassName.method_name"

   source_code = py_reader.get_source_code(module_dotpath, node_path)
   print(source_code)

Limitations
-----------

The ``PyReader`` fetches python source code and docstrings based on the
provided module, class, function, or method paths. It may encounter
issues accurately fetching source code if the provided paths do not
directly correspond to valid python modules, classes, functions, or
methods.

Also, the quality of fetched results depends on the actual source code
in question. As such, if the source code is not well-formatted or lacks
standard python constructs (e.g., no docstrings, poorly structured
classes or methods), the ``PyReader`` may not provide optimal results.

One additional limitation is its dependence on external packages such as
‘redbaron’ and ‘typing’. The performance of this class is tied to the
performance of these external dependencies.

Follow-up Questions:
--------------------

-  How can this class handle exceptions that occur during source code
   fetching?
-  What strategies can be put in place to mitigate issues related to
   poorly constructed source code?
-  How does this class interact with other components in the Automata
   codebase?
-  What’s the use case for removing docstrings from code?
-  Are there constraints linked to the types and formats of modules,
   classes, and methods that ``PyReader`` can handle?
