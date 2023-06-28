RootDict
========

``RootDict`` is a class that represents a dictionary for the root logger
configuration. It is used to set up and configure logging within the
``automata`` library. Instances of ``RootDict`` contain logging-related
settings for the root logger, which can be used by the library when
generating logs.

Related Symbols
---------------

-  ``automata.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata.tests.conftest.MockRepositoryManager``
-  ``automata.core.utils.LoggingConfig``
-  ``automata.tests.unit.test_directory_manager.test_load_directory_structure``
-  ``automata.core.utils.HandlerDict``
-  ``automata.core.coding.py.module_loader.PyModuleLoader``
-  ``automata.tests.unit.test_task_environment.TestURL``
-  ``automata.core.symbol.symbol_types.Symbol``

Example
-------

The following example demonstrates how to create a custom root
dictionary logger and use it in the logging configuration:

.. code:: python

   from automata.core.utils import RootDict, LoggingConfig
   from logging.config import dictConfig

   root_dict: RootDict = {
       "level": "DEBUG",
       "handlers": ["console"],
   }

   logging_config: LoggingConfig = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "simple": {
               "format": "%(asctime)s - %(levelname)s - %(message)s"
           }
       },
       "handlers": {
           "console": {
               "class": "logging.StreamHandler",
               "level": "DEBUG",
               "formatter": "simple",
               "stream": "ext://sys.stdout"
           }
       },
       "root": root_dict,
   }

   dictConfig(logging_config)

Limitations
-----------

The ``RootDict`` class itself does not impose any major limitations, but
it does rely on the ``logging`` module from the Python Standard Library
for configuring logging settings. This does imply that any limitations
of the ``logging`` module would also apply when using ``RootDict``.

Follow-up Questions:
--------------------

-  Are there any performance implications when using a complex
   configuration with ``RootDict``?
-  How well do the default settings in ``RootDict`` work for most use
   cases, and is it necessary to provide a custom configuration in most
   cases?
