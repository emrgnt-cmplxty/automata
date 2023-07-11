DotPathMap
==========

``DotPathMap`` is a class that establishes a map between module
*dotpaths* and module *filepaths*. Dotpath is a representation of file
structure in dot notation, for example: ``dir_1.dir_2.file``. This
mapping is useful in handling python modules, which often use dotpaths
for import operations, while the file system uses filepaths.

Overview
--------

The ``DotPathMap`` class is initialized with a path and a prefix. The
path is the absolute root of the module tree, and the prefix is added to
the dotpath of each module. Using these, it constructs a
``_module_dotpath_to_fpath_map``, which maps dotpaths to their
corresponding filepaths. A counterpart map,
``_module_fpath_to_dotpath_map``, maps filepaths back to their dotpaths.

Related Symbols
---------------

-  ``automata.singletons.py_module_loader.PyModuleLoader``
-  ``automata.tests.unit.test_directory_manager.test_get_node_for_path``
-  ``automata.tests.unit.test_database_vector.test_lookup_symbol``

Example
-------

.. code:: python

   from automata.ast_helpers.ast_utils.py.dot_path_map import DotPathMap

   # Initialize a new DotPathMap
   dpm = DotPathMap('/path/to/your/module/root', 'prefix')

   # Check if a dotpath is in the map
   contains_dotpath = dpm.contains_dotpath('prefix.module_subpath')

   # Check if a filepath is in the map
   contains_fpath = dpm.contains_fpath('/path/to/your/module/root/module_subpath.py')

   # Get the module dotpath given its filepath
   module_dotpath = dpm.get_module_dotpath_by_fpath('/path/to/your/module/root/module_subpath.py')

   # Get the filepath given module dotpath
   module_fpath = dpm.get_module_fpath_by_dotpath('prefix.module_subpath')

   # Add a new module to the map
   dpm.put_module('prefix.new_module')

Discussions
-----------

Limitations
~~~~~~~~~~~

The ``DotPathMap`` has been designed to track and manage modules within
a directory structure, mapping dotpaths to filepaths and vice versa.
However, the class does not support any structural or naming changes to
the existing modules in the directory after the map is created. In such
cases, an exception may be raised or incorrect filepaths may be
returned. Furthermore, when adding a new module to the map with
``put_module``, it assumes that the dotpath does not already exist in
the map and raises an exception if it does.

Other uses
~~~~~~~~~~

``DotPathMap`` is a fairly generic class that might be useful in other
contexts where the mapping between a dot-separated path representation
and a file system path is needed.

Follow-up Questions:
--------------------

-  What happens if I attempt to add a module using a dotpath that
   already exists in the directory structure?
-  What is the behaviour if I manually add a module to the directory and
   then attempt to retrieve its dotpath or filepath from the
   ``DotPathMap``?
-  What is the expected behaviour if the module files or structure
   changes post the initialization of the ``DotPathMap`` object? Does it
   dynamically update or does it require re-initializing?
