PyModuleLoader
==============

``PyModuleLoader`` is a Singleton class that provides a reliable and
efficient way to load, cache and maintain in memory Python modules
specifically in the form of ``RedBaron`` FST objects. The class aims to
map modules from their corresponding dotpaths as they are accessed.

Overview
--------

Conversion to ``RedBaron`` FST objects helps with the advantage of it
being a full syntax tree, which gives a more detailed representation of
the source code, preserving details like the whitespace and comments
that would be discarded by a simple Abstract Syntax Tree (AST).

Throughout its methods, ``PyModuleLoader`` ensures initialization status
thereby maintaining the Singleton pattern. It also checks for module’s
dotpath presence to do selective loading of requested modules and offers
a variety of ways to fetch the module, depending on use-case.

Initialization
--------------

Initialization is performed by calling the ``initialize`` function,
passing in root_fpath and py_fpath, which default to ``get_root_fpath``
and ``get_root_py_fpath`` respectively if they’re not provided. The
initialize method raises an Exception if paths have already been
initialized, preventing any overriding of root directories.

Core Methods
------------

The ``_fetch_module`` fetches a specific module, ``_put_module`` puts a
module in the directory and the ``_fetch_existing_module_dotpath`` and
``_fetch_existing_module_fpath_by_dotpath`` return module file and dot
paths respectively. The ``_items`` method returns a dictionary listing
all modules. The ``__contains__`` checks if a module exists.

Example
-------

.. code:: python

   from automata.singletons.py_module_loader import PyModuleLoader
   from automata.core.utils import get_root_fpath, get_root_py_fpath

   # Initialize the loader
   PyModuleLoader.initialize(root_fpath=get_root_fpath(), py_fpath=get_root_py_fpath())

   # Fetch a module
   module = PyModuleLoader.fetch_module('automata.core.base')

   # Inspect the module
   print(module)

Related Symbols
---------------

-  ``automata.navigation.py.dot_path_map.DotPathMap``
-  ``automata.core.base.patterns.singleton.Singleton``
-  ``automata.navigation.py.dot_path_map.DotPathMap``
-  ``automata.navigation.py.dot_path_map.DotPathMap.contains_dotpath``
-  ``automata.core.utils.get_root_fpath``
-  ``automata.core.utils.get_root_py_fpath``

Dependencies
------------

-  ``automata.navigation.py.dot_path_map.DotPathMap.put_module``
-  ``automata.navigation.py.dot_path_map.DotPathMap.get_module_dotpath_by_fpath``

Limitations
-----------

One limitation is the dependency on ``DotPathMap`` to manage directories
and files with assurance on initialization. There is also a need to
manually ensure initialization with ``_assert_initialized`` in every
method.

Follow-up Questions:
--------------------

-  How can we handle module’s existence checks better to prevent
   redundant file accesses?
-  How can we enhance the Singleton design pattern application to not
   manually ensure initialization in every context?
-  Is there a way to optimize or remove the type-ignoring comments which
   are present now to suppress warnings?
