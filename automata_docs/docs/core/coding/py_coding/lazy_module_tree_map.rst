LazyModuleTreeMap
=================

``LazyModuleTreeMap`` is a class that provides a lazy dictionary between
Python module dotpaths and their corresponding RedBaron FST objects. It
loads and caches modules in memory as they are accessed, allowing for
efficient lookups of code objects and their metadata. This class is used
in conjunction with other classes such as ``DotPathMap``,
``PyCodeRetriever``, and ``PyCodeWriter`` to perform operations such as
code retrieval and generation.

Overview
--------

``LazyModuleTreeMap`` retains a dictionary of module dotpaths and their
associated RedBaron FST objects. When a module is accessed, the class
will fetch and cache the module in memory if not already loaded. The
class includes methods to check if a module exists in the map, fetch a
module by its dotpath, and add a module to the map.
``LazyModuleTreeMap`` also integrates with the ``DotPathMap`` class to
enable interactions with module file paths and dotpaths.

Related Symbols
---------------

-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata_docs.core.coding.py_coding.module_tree.DotPathMap``
-  ``automata_docs.core.coding.py_coding.writer.PyCodeWriter``

Example
-------

Here’s an example of how to use ``LazyModuleTreeMap``:

.. code:: python

   from automata_docs.core.coding.py_coding.module_tree import LazyModuleTreeMap

   # Create a LazyModuleTreeMap instance with a custom root path
   path = "/path/to/modules"
   tree_map = LazyModuleTreeMap(path)

   # Check if a module exists in the map
   module_dotpath = "my_module.submodule"
   exists = module_dotpath in tree_map

   # Fetch a module by its dotpath
   module = tree_map.fetch_module(module_dotpath)

   # Add a module to the map
   new_module_dotpath = "my_module.new_submodule"
   new_module = RedBaron("import foo\n")
   tree_map.put_module(new_module_dotpath, new_module)

Limitations
-----------

``LazyModuleTreeMap`` assumes that the provided module dotpaths follow a
specific dotpath format and comply with the directory structure.
Additionally, it relies on the ``DotPathMap`` class for managing module
file paths and dotpaths which, in turn, also assumes a specific
directory structure for module files.

Follow-up Questions:
--------------------

-  Is it possible to use ``LazyModuleTreeMap`` with a custom dotpath
   format and directory structure?
-  How can we extend the functionality to support other code object
   types, such as functions or classes?
