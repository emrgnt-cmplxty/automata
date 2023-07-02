LazyModuleTreeMap
=================

``LazyModuleTreeMap`` is a lazy dictionary between module dotpaths (str)
and their corresponding RedBaron FST (Full Syntax Tree) objects
(Optional[RedBaron]). It loads and caches modules in memory as they are
accessed.

Overview
--------

``LazyModuleTreeMap`` provides a convenient way to access modules in a
lazy manner, only loading and parsing the module when it’s accessed for
the first time. It caches the loaded modules for efficient subsequent
access and uses a ``DotPathMap`` for the dotpath to filepath mapping.
``LazyModuleTreeMap`` contains methods such as ``fetch_module``,
``fetch_existing_module_dotpath`` and ``items`` that help retrieve and
manage modules in the map with efficiency.

Related Symbols
---------------

-  ``automata.core.code_handling.py_coding.module_tree.DotPathMap``
-  ``automata.core.code_handling.py_coding.py_utils``
-  ``automata.tests.unit.test_py_code_retriever.module_map``

Example
-------

Here is an example of using ``LazyModuleTreeMap`` to create a new
instance and access a module.

.. code:: python

   from automata.core.code_handling.py_coding.module_tree import LazyModuleTreeMap
   from automata.core.utils import root_fpath

   root_path = root_fpath()
   lazy_map = LazyModuleTreeMap(root_path)

   module_dotpath = "automata.core.agent.agent"
   module = lazy_map.fetch_module(module_dotpath)

Limitations
-----------

The primary limitation of ``LazyModuleTreeMap`` is that it’s primarily
designed for the Automata project and assumes a specific directory
structure. Moreover, the default value for ‘py_path’ is ``automata`` and
requires customization for other use cases.

Follow-up Questions:
--------------------

-  How can we make ``LazyModuleTreeMap`` more generic for use in
   non-Automata projects?
-  Is there any performance concern when using ``LazyModuleTreeMap``
   with a large number of modules?
