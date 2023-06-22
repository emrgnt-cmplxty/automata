PyCodeRetriever
===============

``PyCodeRetriever`` is a utility class responsible for fetching Python
code and associated docstrings from modules, classes, functions, or
methods. The class offers a convenient way to access code, docstrings or
even source code without docstrings for a specified dot-separated object
and module paths.

overview
--------

The ``PyCodeRetriever`` class uses the ``LazyModuleTreeMap`` and
``find_syntax_tree_node`` function to fetch modules and generate
docstrings or source code. The class also provides utility methods to
retrieve docstrings and source code from Full Syntax Trees (FST).
Supporting methods allow to remove docstrings from the FST to fetch
source code without docstring contents.

Related symbols
---------------

-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap.cached_default``
-  ``automata.core.coding.py_coding.navigation.find_syntax_tree_node``
-  ``redbaron.ClassNode``
-  ``redbaron.DefNode``
-  ``redbaron.Node``
-  ``redbaron.StringNode``

Examples
--------

.. code:: python

   from automata.core.coding.py_coding.retriever import PyCodeRetriever
   from automata.core.coding.py_coding.module_tree import LazyModuleTreeMap

   module_tree_map = LazyModuleTreeMap.cached_default()
   code_retriever = PyCodeRetriever(module_tree_map)
   module_dotpath = 'automata.core.agent.tools.py_code_retriever.PyCodeRetrieverTool'
   object_path = 'PyCodeRetrieverTool.__init__'

   source_code = code_retriever.get_source_code(module_dotpath, object_path)
   docstring = code_retriever.get_docstring(module_dotpath, object_path)
   source_code_without_docstrings = code_retriever.get_source_code_without_docstrings(module_dotpath, object_path)

Limitations
-----------

The primary limitation of the ``PyCodeRetriever`` class is that it is
designed only to work with Python code. Also, the underlying techniques
for searching and modifying Full Syntax Trees (FST) using ``redbaron``
can be slower for large codebases.

Follow-up Questions:
--------------------

-  Can ``PyCodeRetriever`` be extended to support other programming
   languages?
-  Are there alternative ways to improve the performance while working
   with Full Syntax Trees (FST)?
