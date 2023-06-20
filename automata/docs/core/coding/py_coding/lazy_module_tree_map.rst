LazyModuleTreeMap
=================

Overview
--------

The ``LazyModuleTreeMap`` class represents a lazy dictionary that maps
module dotpaths to their corresponding RedBaron FST objects. It loads
and caches the modules in memory as they are accessed. The class also
provides methods for fetching existing module dotpaths and filepaths, as
well as for fetching, putting and updating the modules by their
dotpaths.

Related Symbols
---------------

-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever.__init__``
-  ``automata.tests.unit.test_py_code_retriever.module_map``
-  ``automata.tests.unit.test_py_code_retriever.getter``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``

Example
-------

The following example demonstrates how to create and use a
``LazyModuleTreeMap``:

.. code:: python

   from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap
   from automata.core.utils import root_fpath

   path_to_root = root_fpath()
   module_tree_map = LazyModuleTreeMap(path_to_root)

   # Fetch an existing module by its dotpath
   module_dotpath = "automata.core.agent.automata_agent"
   module = module_tree_map.fetch_module(module_dotpath)

   # Check if a module with the given dotpath exists
   exists = module_dotpath in module_tree_map

Limitations
-----------

``LazyModuleTreeMap`` assumes a specific directory structure for the
modules, according to the ``DotPathMap`` class. Custom directory
structures for modules are not supported.

Follow-up Questions:
--------------------

-  How can we adapt ``LazyModuleTreeMap`` to support custom directory
   structures for the modules?
