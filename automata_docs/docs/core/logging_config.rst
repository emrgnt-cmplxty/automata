LoggingConfig
=============

``LoggingConfig`` is a dictionary class representing the logging
configuration for the application. It helps set up logging
configurations such as version, loggers, formatters, handlers, and root
logger settings. The class is designed to comply with the ``TypedDict``
type and allows optional error-checking on dictionary key-value types.

Overview
--------

``LoggingConfig`` provides the necessary structure for setting up
logging configurations, which can be used by various logging utilities
and handlers in the application. The class defines keys like
``version``, ``disable_existing_loggers``, ``formatters``, ``handlers``,
and ``root`` to configure the different aspects of logging.

Related Symbols
---------------

-  ``automata_docs.core.utils.HandlerDict``
-  ``automata_docs.cli.commands.reconfigure_logging``
-  ``automata_docs.core.utils.RootDict``
-  ``automata_docs.core.utils.get_logging_config``

Example
-------

The following is an example demonstrating how to create an instance of
``LoggingConfig`` and set up a basic logging configuration.

.. code:: python

   from automata_docs.core.utils import LoggingConfig

   log_config: LoggingConfig = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {
           "simple": {
               "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
           },
       },
       "handlers": {
           "console": {
               "class": "logging.StreamHandler",
               "formatter": "simple",
               "level": "DEBUG",
           },
       },
       "root": {
           "level": "DEBUG",
           "handlers": ["console"],
       },
   }

Limitations
-----------

The primary limitation of ``LoggingConfig`` is that it only provides a
structure for setting up logging configurations and does not include
built-in utilities or methods to directly modify or manage the logging
configurations. It relies on external utilities and handlers for
configuring the application’s logging, as shown in the example above.

Follow-up Questions:
--------------------

-  Are there any specific pre-configured logging configurations that
   need to be documented?
-  How can we demonstrate using ``LoggingConfig`` in a more advanced
   logging configuration scenario?
