LoggingConfig
=============

``LoggingConfig`` is a configuration class inheriting from ``TypedDict``
that represents the logging configuration. It consists of various
attributes such as ``version``, ``disable_existing_loggers``,
``formatters``, ``handlers``, and ``root`` to configure logging for the
application. The class is mainly used in the ``get_logging_config``
function, which returns the logging configuration.

Related Symbols
---------------

-  ``automata.core.utils.get_logging_config``
-  ``automata.core.utils.RootDict``
-  ``automata.core.utils.HandlerDict``

Example
-------

The following is an example demonstrating how to create an instance of
``LoggingConfig`` and use it with the ``get_logging_config`` function.

.. code:: python

   from automata.core.utils import LoggingConfig, get_logging_config

   logging_config = LoggingConfig(
       version=1,
       disable_existing_loggers=False,
       formatters={
           "detailed": {
               "class": "logging.Formatter",
               "format": "%(asctime)s %(name)-15s %(levelname)-8s %(message)s",
           },
           "brief": {
               "class": "logging.Formatter",
               "format": "%(name)-15s: %(levelname)-8s %(message)s",
           },
       },
       handlers={
           "console": {
               "class": "logging.StreamHandler",
               "formatter": "brief",
               "level": "INFO",
               "stream": "ext://sys.stdout",
           },
           "file": {
               "class": "logging.FileHandler",
               "formatter": "detailed",
               "level": "DEBUG",
               "filename": "logfile.log",
           },
       },
       root={"handlers": ["console", "file"], "level": "DEBUG"},
   )

   config = get_logging_config(logging_config)

Limitations
-----------

Since ``LoggingConfig`` is a TypedDict, it does not enforce the
attributes’ types at runtime, which means incorrect typing might not
raise an error during runtime. To avoid this, it is recommended to use
type-checking tools like ``mypy`` to identify type errors before the
code is executed.

Follow-up Questions
-------------------

-  Should we add more examples using other attributes and methods from
   the related symbols mentioned above?
