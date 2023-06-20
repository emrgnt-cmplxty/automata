RootDict
========

``RootDict`` is a dictionary representing the root logger in the logging
configuration.

Overview
--------

``RootDict`` is a typed dictionary subclass derived from the
``TypedDict`` base class. It provides a type-safe way to store the root
logger information, which includes logging level, handlers, and others.
The primary purpose of the ``RootDict`` class is to be used in
conjunction with the ``automata.core.utils.LoggingConfig`` class and
other related symbols for configuring logging settings in an
application.

Related Symbols
---------------

-  ``automata.core.utils.LoggingConfig``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.utils.HandlerDict``
-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.core.coding.py_coding.module_tree.DotPathMap``
-  ``automata.tests.unit.test_py_code_retriever.module_map``
-  ``automata.core.coding.directory.DirectoryManager``

Example
-------

The following example demonstrates how to create a ``RootDict`` instance
to store root logger information.

.. code:: python

   from automata.core.utils import RootDict

   root_dict: RootDict = {
       "level": "INFO",
       "handlers": ["console"],
   }

Limitations
-----------

``RootDict`` is just a typed dictionary that ensures the correct
structure for the root logger information, but it doesn’t provide any
built-in functionality for managing logging settings or interactions
with other logging components. For that purpose, you need to use other
related symbols and classes as shown in the Related Symbols section.

Follow-up Questions:
--------------------

-  Are there any other important methods or attributes that should be
   included in the documentation for ``RootDict``?
