RootDict
========

``RootDict`` is a dictionary class that represents the root logger. It
is a part of the ``automata_docs.core.utils.LoggingConfig`` class which
represents the logging configuration for the application.

Related Symbols
---------------

-  ``automata_docs.core.utils.LoggingConfig``
-  ``automata_docs.core.utils.HandlerDict``

Example
-------

Below is an example on how to use ``RootDict`` in conjunction with the
``LoggingConfig`` class.

.. code:: python

   from automata_docs.core.utils import RootDict, LoggingConfig

   root_logger: RootDict = {
       "level": "DEBUG",
       "handlers": ["console"]
   }

   logging_config: LoggingConfig = {
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {...},
       "handlers": {...},
       "root": root_logger
   }

Discussion
----------

RootDict is simply a dictionary that represents the root logger
configuration. It defines the log level and handlers for the root
logger. To make use of this class as part of the complete logging
configuration, you should work together with the ``LoggingConfig``
class, and other related classes such as ``HandlerDict``.

Follow-up Questions:
--------------------

-  What happen if we omit the RootDict or set it as an empty dictionary,
   how it will affect the logging configuration?
