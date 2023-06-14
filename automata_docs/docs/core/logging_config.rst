LoggingConfig
=============

``LoggingConfig`` is a class that represents the logging configuration
for the Automata Docs package. It allows you to configure the logging
settings to suit your specific needs, while providing a default logging
configuration that serves as a basis for most use cases.

Overview
--------

``LoggingConfig`` is a dictionary that contains various settings and
values that control the logging behavior in the package. By customizing
the ``LoggingConfig``, you can adjust log levels, enable/disable
handlers, and ensure that your logging infrastructure works as intended
in different circumstances.

Related Symbols
---------------

-  ``automata_docs.cli.commands.LoggingConfig``
-  ``automata_docs.core.utils.HandlerDict``
-  ``automata_docs.core.utils.RootDict``
-  ``automata_docs.cli.commands.HandlerDict``

Example
-------

The following example demonstrates how to create an instance of
``LoggingConfig``.

.. code:: python

   from automata_docs.core.utils import LoggingConfig

   logging_config = LoggingConfig()

Limitations
-----------

``LoggingConfig`` is limited in that it only provides a dictionary
structure for representing the configuration. You’ll need to work with
other parts of the logging system or use additional tools to make
changes to the logging infrastructure more effectively.

Follow-up Questions:
--------------------

-  What is the purpose of the related ``HandlerDict``, and ``RootDict``
   classes?
-  How do the related symbols
   ``automata_docs.cli.commands.LoggingConfig`` and
   ``automata_docs.cli.commands.HandlerDict`` fit into the overall
   logging setup?
