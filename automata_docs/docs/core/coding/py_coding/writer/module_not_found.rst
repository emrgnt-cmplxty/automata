PyCodeWriter.ModuleNotFound
===========================

``PyCodeWriter.ModuleNotFound`` is a custom exception class that is
raised when a requested module is not found in the module dictionary
within the ``PyCodeWriter`` context. This can be useful in catching
cases where a module is requested but does not exist, causing the
\`PyCodeWriter\` to raise this exception.

Related Symbols
---------------

-  ``automata_docs.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``

Example
-------

To illustrate the usage of this exception, consider the following
example where a non-existent module is requested:

.. code:: python

   from automata_docs.core.coding.py_coding.writer import PyCodeWriter
   from automata_docs.core.coding.py_coding.retriever import PyCodeRetriever
   from automata_docs.utils.map.lazy_module_tree_map import LazyModuleTreeMap

   try:
       module_map = LazyModuleTreeMap("path/to/modules")
       retriever = PyCodeRetriever(module_map)
       writer = PyCodeWriter(retriever)
       
       writer.get_module_dotpath("non_existent_module")
   except PyCodeWriter.ModuleNotFound as ex:
       print(f"Module not found: {ex}")

In this example, the ``PyCodeWriter`` attempts to retrieve the dotpath
of a non-existent module. As a result, it will raise a
``PyCodeWriter.ModuleNotFound`` exception, which can be caught and
handled.

Limitations
-----------

This exception is specific to the ``PyCodeWriter`` class, and may not be
applicable for other classes or scenarios. It serves as a simple way to
raise an exception when a module is not found within the context of the
``PyCodeWriter``. Alternatively, Python’s default
``ModuleNotFoundError`` could also be used in this case.

Follow-up Questions:
--------------------

-  Are there any scenarios that might cause this exception to be raised
   inappropriately or fail to raise when it should?
-  Would it make more sense to use Python’s default
   ``ModuleNotFoundError`` in this case or continue to use the custom
   exception class?
