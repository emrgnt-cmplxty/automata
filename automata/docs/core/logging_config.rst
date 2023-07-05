LoggingConfig
=============

``LoggingConfig`` is a flexible dictionary-like configuration object
introduced in the ``automata.core.utils`` module. It provides a
structured form to define the logging configuration including the
logger’s version, control over disabling existing loggers, definitions
for formatters and handlers, and base root dictionary for logging.

Overview
--------

``LoggingConfig`` is a subclass of Python’s ``TypedDict`` that allows
you to have dictionary, where keys, values are restricted to specific
types. It is less error-prone and provides a higher quality of tooling
support. The ``total=False`` specification in the subclass definition
means that not all dictionary keys need to be present in initialized
instances of ``LoggingConfig``.

The ``LoggingConfig`` values can range from fundamental datatypes like
``int`` and ``bool`` to more compound ones like dictionaries of custom
types like ``HandlerDict`` and ``RootDict``.

Related Symbols
---------------

-  ``automata.core.utils.HandlerDict``: A dictionary representing a
   logging handler.
-  ``automata.core.utils.RootDict``: A dictionary representing the root
   logger.
-  ``automata.cli.commands.reconfigure_logging``: Methods to reconfigure
   logging.
-  ``automata.core.utils.get_logging_config``: Returns the logging
   configuration.
-  ``automata.tests.unit.test_task.test_task_inital_state, test_register_task, test_execute_automata_task_fail, test_execute_automata_task_success``:
   Unit tests validating various functionalities of ``LoggingConfig``.

Example
-------

Here is an illustrative example to create a ``LoggingConfig`` object:

.. code:: python

   from automata.core.utils import LoggingConfig

   log_config = LoggingConfig(
       version=1,
       disable_existing_loggers=False,
       formatters={},
       handlers={"handler": {"class": "logging.StreamHandler", "formatter": "default", "level": "DEBUG"}},
       root={"handlers": ["handler"], "level": "DEBUG"},
   )

Set ``disable_existing_loggers = False`` to permit the functionality of
existing loggers. Handlers can use a ``StreamHandler`` with a level of
“DEBUG”. In the root logger, this handler will be used at the debugging
level.

Limitations
-----------

The ``LoggingConfig`` object is structured to conform to the
``TypedDict`` constraints including the type specifications of keys and
their associated values. As such, it may not support dynamic
configurations if the keys and/or their attribute types vary beyond the
predefined schema.

Another potential limitation is the absence of some keys in the
dictionary due to the ``TypedDict`` was defined with ``total=False``.
That could lead to runtime errors if the code assumes the existence of
keys that might not be present.

Follow-up Questions:
--------------------

-  Is there a way for ``LoggingConfig`` to accept a broader range of
   logging formatters and handlers?
-  What happens if specified logging handlers aren’t available or
   configured incorrectly?
-  How are exceptions handled when logging configuration issues occur,
   due to reasons like missing keys in the dict or data-type mismatch?
-  Can ``LoggingConfig`` be extended to accept or support custom logging
   handlers and formatters?
-  What are performance implications of using ``TypedDict`` vs a
   standard dictionary in Python?
