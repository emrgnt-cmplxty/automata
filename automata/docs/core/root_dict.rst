RootDict
========

``RootDict`` is a dictionary class representing the root logger in
``automata.core.utils``. It is primarily used with other related typed
dictionaries such as ``LoggingConfig`` and ``HandlerDict`` to build and
handle logging configurations for the project.

Overview
--------

``RootDict`` is a simple dictionary representation of the root logger
and is a part of the logging configuration settings. It is primarily
used in conjunction with other dictionaries and classes such as
``LoggingConfig`` and ``HandlerDict``.

Related Symbols
---------------

-  ``automata.core.utils.LoggingConfig``
-  ``automata.core.utils.HandlerDict``

Example
-------

The following is an example of how a ``RootDict`` object can be created
and used in conjunction with ``LoggingConfig`` and ``HandlerDict`` to
set up a logging configuration.

.. code:: python

   from automata.core.utils import HandlerDict, LoggingConfig, RootDict

   root_dict = RootDict({"level": "DEBUG", "handlers": ["console"]})
   handler_dict = HandlerDict({"class": "logging.StreamHandler", "formatter": "simple"})
   logging_config = LoggingConfig({
       "version": 1,
       "disable_existing_loggers": False,
       "formatters": {"simple": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"}},
       "handlers": {"console": handler_dict},
       "root": root_dict
   })

Limitations
-----------

``RootDict`` is a simple dictionary for representing the root logger and
does not contain any additional functionality or logic to work with
other logging configurations directly. It relies on being used in
conjunction with other classes and dictionaries, such as
``LoggingConfig`` and ``HandlerDict``, to handle its higher-level
interactions.

Follow-up Questions:
--------------------

-  Are there any additional methods or attributes needed within the
   ``RootDict`` class?
