HandlerDict
===========

``HandlerDict`` is a class representing a dictionary for logging
handlers, which is used to store information about various logging
handlers in the system. This class is part of the
``automata.core.utils`` module and is used in configuring logging
features across the different components of the project.

Overview
--------

``HandlerDict`` is a dictionary subclass that represents a specific
logging handler. It is designed to provide a consistent interface for
working with logging handler configurations. It works in conjunction
with ``LoggingConfig``, ``RootDict``, and other related symbols to
enable proper logging configuration management.

Related Symbols
---------------

-  ``automata.core.utils.LoggingConfig``
-  ``automata.core.utils.RootDict``

Example
-------

The following example demonstrates how to create an instance of
``HandlerDict`` and use it as part of a logging configuration.

.. code:: python

   from automata.core.utils import HandlerDict, LoggingConfig, RootDict

   handler_dict = HandlerDict(
       {
           "level": "DEBUG",
           "class": "logging.StreamHandler",
           "formatter": "default",
       }
   )

   logging_config = LoggingConfig(
       {
           "version": 1,
           "disable_existing_loggers": False,
           "formatters": {
               "default": {
                   "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
               }
           },
           "handlers": {
               "console": handler_dict
           },
           "root": RootDict(
               {
                   "level": "DEBUG",
                   "handlers": ["console"],
               }
           ),
       }
   )

Limitations
-----------

``HandlerDict``, as a subclass of ``dict``, inherits the standard Python
dictionary limitations. The primary limitation is that it cannot enforce
any specific data structure or typing on the stored values. It is up to
the user to ensure that the configured values meet the required
specifications of the logging handlers being used.

Follow-up Questions:
--------------------

-  How can we enforce stricter typing and structure restrictions on the
   contents of the ``HandlerDict``?
