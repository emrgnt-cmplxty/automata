LoggingConfig
=============

``LoggingConfig`` is a dictionary representing the logging configuration
settings in the project. Its main purpose is to configure and manage log
settings across various components of the application, such as version,
formatters, handlers, and the root logger settings.

Overview
--------

This class is a TypedDict subclass and provides type hints for the keys
allowed in the dictionary. The keys include ``version``,
``disable_existing_loggers``, ``formatters``, ``handlers``, and
``root``. It works closely with related symbols such as ``HandlerDict``,
``RootDict``, and ``get_logging_config``.

Related Symbols
---------------

-  ``automata_docs.core.utils.HandlerDict``
-  ``automata_docs.core.utils.RootDict``
-  ``automata_docs.core.utils.get_logging_config``

Example
-------

Below is an example of how to create a ``LoggingConfig`` dictionary and
configure logging settings using the ``reconfigure_logging`` command:

.. code:: python

   from automata_docs.cli.commands.reconfigure_logging import reconfigure_logging
   from automata_docs.core.utils import get_logging_config

   logging_config = get_logging_config(log_level=logging.DEBUG, log_file='example.log')
   reconfigure_logging(logging_config)

Limitations
-----------

``LoggingConfig`` is a dictionary and cannot provide additional
functionality beyond storing and accessing keys and values. It relies on
external functions and utilities like ``get_logging_config`` and
``reconfigure_logging`` for configuring the logging settings.

Follow-up Questions:
--------------------

-  How can additional keys and values be added to the ``LoggingConfig``
   dictionary, and what are the implications on the logging settings?
