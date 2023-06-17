PyCodeWriter
============

``PyCodeWriter`` is a utility class for writing Python code along AST
nodes. It builds on the ``PyCodeRetriever`` object and provides various
methods for creating, updating, and deleting modules. The
``PyCodeWriter`` class can be extended to write documentation for Python
modules and execute code generation tasks.

Overview
--------

The main functionality of ``PyCodeWriter`` is centered around creating,
updating, and deleting Python modules using AST nodes. It provides
methods to perform these actions, such as ``create_new_module``,
``delete_from_existing_module``, and ``update_existing_module``. The
class is initialized with a ``PyCodeRetriever`` instance that retrieves
Python code from modules and objects.

Related Symbols
---------------

-  ``PyCodeRetriever``
-  ``automata.tests.unit.test_py_writer.MockCodeGenerator``

Example
-------

The following example demonstrates how to create an instance of
``PyCodeWriter`` with a ``PyCodeRetriever`` instance:

.. code:: python

   from automata.core.coding.py_coding.retriever import PyCodeRetriever
   from automata.core.coding.py_coding.writer import PyCodeWriter
   from automata.core.coding.directory import DirectoryManager

   py_retriever = PyCodeRetriever(DirectoryManager().module_tree_map)
   code_writer = PyCodeWriter(py_retriever)

Limitations
-----------

``PyCodeWriter`` assumes that the provided module paths have the given
structure and can only work on modules with that structure. This makes
it less flexible for working with different modules’ structures.

Follow-up Questions
-------------------

-  Are there any plans to extend support for custom module structures in
   the future?
