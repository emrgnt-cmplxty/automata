Node
====

Overview
--------

The ``Node`` class is an abstract base class used in the creation of a
file tree in the ``automata.ast_helpers.ast_utils.directory`` module. Each node can
represent a file or a directory within this file tree. It is primarily
used in the construction of trees for file or directory navigation
within the Automata project. Each instance of the ``Node`` class
represents a node of the tree and has attributes ``name`` and ``parent``
corresponding to the name of the node and its parent node respectively.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tests.unit.test_directory_manager.test_get_node_for_path``
-  ``automata.ast_helpers.ast_utils.directory.File``
-  ``automata.tests.unit.sample_modules.sample.OuterClass``
-  ``automata.ast_helpers.ast_utils.directory.Directory``
-  ``automata.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata.tests.conftest.MockRepositoryClient``
-  ``automata.symbol.base.Symbol``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU``
-  ``automata.code_handling.py.writer.PyWriter``

Example
-------

The ``Node`` class is an abstract class, hence there can’t be an
instantiation of it. However, it serves as a base class for its
subclasses like ``File`` and ``Directory``. In the example below, a
``File`` object is created.

.. code:: python

   from automata.ast_helpers.ast_utils.directory import File

   file = File("sample_file", None)

Note: In the above example, ``sample_file`` is the name of the file and
``None`` represents that the file has no parent node.

Limitations
-----------

Since ``Node`` is an abstract base class, it can’t be instantiated on
its own. It doesn’t contain any method to manipulate its attributes
``name`` and ``parent``, hence, these should be handled carefully in the
subclasses.

Follow-up Questions
-------------------

-  Are additional methods required in the ``Node`` class to manipulate
   its attributes i.e., ``name`` or ``parent``?
-  Given ``Node`` is an abstract base class, what are the contract
   details, i.e., the methods subclasses are expected to implement?
