PyModuleLoader
==============

``PyModuleLoader`` is a Singleton class that provides a lazy dictionary
mapping dotpaths to their corresponding RedBaron FST objects. It is
responsible for loading and caching modules in memory as they are
accessed. The primary purpose of this class is to facilitate module
caching and retrieval for various python code manipulation tasks.

Overview
--------

``PyModuleLoader`` provides several methods to interact with and manage
the mapping of dotpaths to the corresponding RedBaron FST objects. The
mapping is managed in an internal dictionary, and modules are loaded
from their file paths as needed. The class utilizes a Singleton pattern,
ensuring that there is only one instance throughout the application.

Related Symbols
---------------

-  ``automata.core.base.singleton.Singleton``
-  ``automata.core.coding.py.reader.PyReader``
-  ``automata.core.coding.py.writer.PyWriter``

Example
-------

The following example demonstrates how to initialize and use
``PyModuleLoader`` to fetch a module:

.. code:: python

   from automata.core.coding.py.module_loader import PyModuleLoader
   from automata.core.utils import get_root_fpath, get_root_py_fpath

   # Initialize PyModuleLoader
   PyModuleLoader().initialize(root_fpath=get_root_fpath(), py_fpath=get_root_py_fpath())

   # Fetch a module by its dotpath
   module_dotpath = "path.to.module"
   module = PyModuleLoader().fetch_module(module_dotpath)

Limitations
-----------

Currently, the ``_assert_initialized`` method is used extensively
throughout the class. This can make the class more challenging to
maintain as new functionality is added.

In addition, there are several ``type: ignore`` comments in the code,
which indicate potential areas for improvement in type handling.

The Singleton pattern used in this class might not be ideal for all use
cases and might need to be reconsidered if multiple instances of
``PyModuleLoader`` are needed.

Follow-up Questions:
--------------------

-  Is there a cleaner way to ensure initialization without using
   ``_assert_initialized`` everywhere?
-  Can we improve the code to remove the ``type: ignore`` comments?
-  Are there situations where the Singleton pattern might no longer be
   the best approach for this class?
