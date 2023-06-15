HandlerDict
===========

``HandlerDict`` is a dictionary representing a logging handler. This
class is mainly used in the ``LoggingConfig`` configuration dictionary
to handle the logging handlers.

Related Symbols
---------------

-  ``automata_docs.core.utils.RootDict``
-  ``automata_docs.core.utils.LoggingConfig``
-  ``automata_docs.tests.unit.sample_modules.sample_module_2.OKjJY``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.tests.unit.sample_modules.sample_module_2.KavpK``
-  ``automata_docs.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata_docs.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Example
-------

The following example demonstrates the use of ``HandlerDict`` in the
context of ``LoggingConfig``.

.. code:: python

   from typing import Union
   from automata_docs.core.utils import HandlerDict, LoggingConfig, RootDict

   logging_handler = HandlerDict(level="DEBUG", formatter="simple")

   logging_config: LoggingConfig = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "simple": {
               "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
           },
       },
       "handlers": {"console": logging_handler},
       "root": RootDict(level="INFO", handlers=["console"]),
   }

This example shows how to create a ``HandlerDict`` object and add it to
a ``LoggingConfig`` dictionary specifying the configuration for the
logging system.

Limitations
-----------

``HandlerDict`` is primarily used in the context of ``LoggingConfig``.
It is not meant to be used as a standalone dictionary for other
purposes.

Follow-up Questions:
--------------------

-  Are there other use cases for ``HandlerDict`` outside of
   ``LoggingConfig``?
