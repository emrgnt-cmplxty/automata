HandlerDict
===========

``HandlerDict`` is a special dictionary type that represents a logging
handler in the logging configuration structure. Handlers are responsible
for delivering a log record (LogRecord instance) to its destination.
Hence ``HandlerDict`` plays a crucial role in controlling how and where
every logging event is handled.

Overview
--------

``HandlerDict`` extends Python’s built-in ``dict`` class and it is used
within the larger scope of a ``LoggingConfig`` which is formatted as a
dictionary. The ``LoggingConfig`` includes the handler definitions,
which are represented as ``HandlerDict``.

Related Symbols
---------------

-  ``automata.core.utils.RootDict``
-  ``automata.core.utils.LoggingConfig``
-  ``automata.tests.unit.sample_modules.sample_module_write.CsSWU.__init__``

Example usage of HandlerDict
----------------------------

Although the ``HandlerDict`` is usually a part of a LoggingConfig, it
can be used independently as well.

In a ``LoggingConfig``, the HandlerDict usually is present in something
similar to the following structure:

.. code:: python

   logging_config = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'console': {
               'class': 'logging.StreamHandler',
               'level': 'INFO',
               'formatter': 'standard',
               'stream': 'ext://sys.stdout',
           }
       }
   }

Here, ‘console’ is a HandlerDict which further contains handler-specific
settings in its own dictionary.

It is important to note as this an integral part of logging
configuration, using it independently might not yield much significant
results.

Limitations:
------------

``HandlerDict`` is a subset of the larger ``LoggingConfig`` dictionary
and hence does not offer any specialized functionality or methods apart
from the dictionary structure it provides to store configuration. It
must be accurately formatted and used in a valid logging configuration
structure to function as intended. Furthermore, it assumes that proper,
valid handler properties are used as keys in the HandlerDict.

Follow-Up Questions
-------------------

-  What advanced customization options are available for
   ``HandlerDict``?
-  Can it be used outside a Logging configuration context effectively?
