HandlerDict
===========

``HandlerDict`` is a dictionary class that represents a logging handler
in the logging configuration. It is used in the wider context of
``LoggingConfig``, which is an extended dictionary representing the
entire logging configuration.

Overview
--------

``HandlerDict`` is part of the ``automata.core.utils`` module and
inherits from Python’s built-in dictionary. It is designed to handle
logging configurations, specifically the handler configurations in a
structured manner. It can be used within a ``LoggingConfig`` object,
where handlers can be defined and accessed using keys. The primary
purpose of the ``HandlerDict`` is to provide a well-structured manner to
represent logging handlers configuration within a project.

Related Symbols
---------------

-  ``automata.core.utils.LoggingConfig``
-  ``automata.core.utils.RootDict``

Example
-------

Here’s an example demonstrating how to create and use a ``HandlerDict``
object along with a ``LoggingConfig`` object.

.. code:: python

   from automata.core.utils import HandlerDict, LoggingConfig

   handler_config = HandlerDict({
       'class': 'logging.StreamHandler',
       'level': 'DEBUG',
       'formatter': 'default',
       'stream': 'ext://sys.stdout',
   })

   logging_config = LoggingConfig({
       'version': 1,
       'disable_existing_loggers': False,
       'formatters': {'default': {'format': '%(asctime)s [%(levelname)s] %(name)s: %(message)s'}},
       'handlers': {'console': handler_config},
       'root': {'handlers': ['console'], 'level': 'DEBUG'},
   })

Limitations
-----------

The primary limitation of ``HandlerDict`` lies in its simplicity; it
only provides a structured representation of logging handler
configurations. It does not offer any direct methods or utilities to
interact with or manipulate its contents. It is mostly used as part of
the ``LoggingConfig`` and other logging management operations.

Follow-up Questions:
--------------------

-  How can ``HandlerDict`` be extended to provide additional
   functionality for interacting with logging configurations?
