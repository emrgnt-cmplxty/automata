LazyModuleTreeMap
=================

Overview
--------

``LazyModuleTreeMap`` is a lazy dictionary between module dotpaths and
their corresponding RedBaron FST objects. It is used for loading and
caching modules in memory as they are accessed. The class has methods to
check if the map contains a module with a given dotpath, fetch a module
by its dotpath, add a module to the map, and return the module dotpath
to RedBaron FST object mapping for all loaded modules.

Related Symbols
---------------

-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata_docs.tests.unit.test_py_code_retriever.module_map``
-  ``automata_docs.tests.unit.test_py_code_retriever.getter``
-  ``automata_docs.core.coding.py_coding.module_tree.DotPathMap``

Example
-------

The following is an example demonstrating how to create an instance of
``LazyModuleTreeMap`` with a custom root path:

.. code:: python

   from automata_docs.core.coding.py_coding.module_tree import LazyModuleTreeMap
   from automata_docs.core.utils import root_fpath

   # Set the custom root path for the module tree
   custom_root_path = "/path/to/your/custom/root"
   module_tree_map = LazyModuleTreeMap(custom_root_path)

Limitations
-----------

``LazyModuleTreeMap`` assumes a specific directory structure for the
module files. It relies on the predefined ``DotPathMap`` for module
dotpath to filepath mapping, and cannot load custom mapping files.

Follow-up Questions:
--------------------

-  How can we include custom mapping files for loading into the
   ``LazyModuleTreeMap`` class?
