LoggingConfig
=============

``LoggingConfig`` is a class representing the logging configuration in a
dictionary format. It is a TypedDict that provides fields such as
version, disable_existing_loggers, formatters, handlers, and root. This
configuration helps manage various logging behaviors and settings used
throughout the project.

Overview
--------

``LoggingConfig`` class provides a way to define the structure and type
information for the dictionary representing the logging configuration.
The primary purpose of this class is to provide a schema for the logging
configuration and enable type checking and validation of the
configuration settings. ``LoggingConfig`` works in conjunction with
other logging utilities, such as the ``get_logging_config`` function, to
create the final logging configuration used by the application.

Related Symbols
---------------

-  ``automata.core.utils.get_logging_config``
-  ``automata.core.utils.HandlerDict``
-  ``automata.core.utils.RootDict``

Example
-------

The following is an example demonstrating how to create an instance of
``LoggingConfig``.

.. code:: python

   from automata.core.utils import LoggingConfig

   logging_config: LoggingConfig = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "simple": {
               "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
           }
       },
       "handlers": {
           "console": {
               "class": "logging.StreamHandler",
               "level": "DEBUG",
               "formatter": "simple",
               "stream": "ext://sys.stdout",
           }
       },
       "root": {
           "level": "DEBUG",
           "handlers": [
               "console"
           ]
       }
   }

Limitations
-----------

``LoggingConfig`` is only a schema that defines the structure of the
logging configuration dictionary. It does not provide any functionality
on its own and relies on external utilities like ``get_logging_config``
to create the actual logging configuration. Furthermore,
``LoggingConfig`` only includes type information for the dictionary
fields and does not perform any validation of the actual values. This
means that the dictionary must be validated separately to ensure correct
logging behavior.

Follow-up Questions:
--------------------

-  How can we enforce validation of the logging configuration values
   within the ``LoggingConfig`` class?
