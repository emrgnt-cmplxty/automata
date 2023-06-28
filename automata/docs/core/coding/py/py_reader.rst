PyReader
========

``PyReader`` is a utility class that provides methods for fetching
Python code and documentation from a given module, class, or
function/method. It highly relies on the RedBaron library for traversing
and parsing python code.

Overview
--------

``PyReader`` offers the following methods:

-  ``get_docstring()``: Get the docstring of a specified module, class,
   function, or method.
-  ``get_docstring_from_node()``: Get the docstring from the specified
   RedBaron node (static method).
-  ``get_source_code()``: Get the source code for a specified module,
   class, function, or method.
-  ``get_source_code_without_docstrings()``: Get the source code for a
   specified module, class, function, or method without the docstrings.

Related Symbols
---------------

-  ``automata.core.coding.py.navigation.find_syntax_tree_node``
-  ``automata.core.coding.py.module_loader.PyModuleLoader.fetch_module``

Example
-------

The following is an example demonstrating how to use ``PyReader`` to
retrieve the docstring of a specified function/method.

.. code:: python

   from automata.core.coding.py.reader import PyReader

   module_dotpath = "os.path.join"
   object_path = None
   reader = PyReader()
   docstring = reader.get_docstring(module_dotpath, object_path)
   print(docstring)

Limitations
-----------

The primary limitation of ``PyReader`` is that it highly relies on the
RedBaron library for parsing Python code, which is not being actively
maintained and can be slightly outdated when compared to newer Python
features. If RedBaron fails to handle certain syntax or node types, it
may affect the functionality of ``PyReader``.

Another limitation is that if the provided module path is invalid or not
accessible, PyReader won’t be able to get the desired output.

Follow-up Questions:
--------------------

-  How can ``PyReader`` be adapted to accommodate newer or custom syntax
   types not covered by RedBaron?
-  Can support be added for user-defined configuration options, such as
   handling custom file extensions or syntax additions?
