HandlerDict
===========

``HandlerDict`` is a dictionary class, representing a logging handler in
the context of logging configuration. This class is used together with
other related symbols in different parts of the library to manage and
configure logging settings.

Related Symbols
---------------

-  ``automata.core.utils.RootDict``
-  ``automata.core.utils.LoggingConfig``
-  ``automata.tests.unit.sample_modules.sample_module_2.fhFSO``
-  ``automata.tests.unit.sample_modules.sample_module_2.ObNMl``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.tests.unit.sample_modules.sample_module_2.EmptyClass``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter.ModuleNotFound``
-  ``automata.core.coding.py_coding.module_tree.LazyModuleTreeMap``

Example
-------

The following is an example demonstrating how to create an instance of
``HandlerDict`` and use it within the context of creating a
``LoggingConfig`` object.

.. code:: python

   from automata.core.utils import HandlerDict, LoggingConfig, RootDict

   handler_dict = HandlerDict({"level": "WARNING", "class": "logging.StreamHandler", "formatter": "simple"})

   logging_config = LoggingConfig(
       version=1,
       disable_existing_loggers=False,
       formatters={
           "simple": {
               "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
           }
       },
       handlers={
           "console": handler_dict
       },
       root=RootDict({"level": "DEBUG", "handlers": ["console"]})
   )

Limitations
-----------

``HandlerDict`` itself is a utility class with limited functionality and
its primary purpose is to serve as a structured representation for
logging handlers. It is highly dependent on the context it is used in,
meaning it may not provide much value when used in isolation.

Follow-up Questions
-------------------

-  Is there any specific functionality or methods that should be added
   to the ``HandlerDict`` class for better flexibility and usage?
-  Are there any other potential use cases in which ``HandlerDict``
   might be beneficial?
