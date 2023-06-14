PyCodeRetriever
===============

``PyCodeRetriever`` is a code retriever class used for fetching Python
code. It provides various methods to extract the source code,
docstrings, and source code without docstrings, for specified modules,
classes, functions, or methods.

Overview
--------

``PyCodeRetriever`` provides a straightforward way to access the source
code, docstrings, and source code without docstrings from a module,
class, function, or method specified in the dot-separated format
(e.g. ‘package.module’). It uses a ``LazyModuleTreeMap`` to store and
manage access to the module tree map.

Related Symbols
---------------

-  ``automata_docs.core.context.py_context.retriever.PyContextRetriever``
-  ``automata_docs.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata_docs.tests.unit.test_py_code_retriever.getter``

Example
-------

The following example demonstrates the basic usage of
``PyCodeRetriever`` to fetch a method’s source code and docstring.

.. code:: python

   from automata_docs.core.coding.py_coding.retriever import PyCodeRetriever, LazyModuleTreeMap

   module_tree_map = LazyModuleTreeMap()
   retriever = PyCodeRetriever(module_tree_map)

   module_dotpath = 'package.module'
   object_path = 'ClassName.method_name'

   docstring = retriever.get_docstring(module_dotpath, object_path)
   source_code = retriever.get_source_code(module_dotpath, object_path)
   source_without_docstring = retriever.get_source_code_without_docstrings(module_dotpath, object_path)

Limitations
-----------

``PyCodeRetriever`` assumes that the provided module tree map (using the
default ``LazyModuleTreeMap``) has a correct and up-to-date
representation of the module and its contents. Any changes or
discrepancies in the module tree map may lead to incorrect or incomplete
results when fetching the source code or docstrings.

Follow-up Questions:
--------------------

-  How does the ``PyCodeRetriever`` handle dynamic code generation and
   execution?
-  Are there any performance optimizations for loading large modules or
   codebases?
