PyContextConfig
===============

``PyContextConfig`` is a configuration class for the ``PyContext`` which
is used to retrieve the context of a symbol in a Python project. The
class provides options to set the string for indentation, maximum depth
of dependencies to process, and maximum number of nearest related
symbols to print.

Overview
--------

``PyContextConfig`` offers a convenient way to configure the behavior of
``PyContext``. The class allows instantiation with custom configurations
for the spacer, maximum dependencies to process, and maximum related
symbols to process. It is used as a parameter while creating a
``PyContext`` instance.

Related Symbols
---------------

-  ``automata_docs.core.context.py_context.retriever_slim.PyContext``
-  ``automata_docs.core.symbol.symbol_types.Symbol``

Example
-------

The following is an example demonstrating how to create an instance of
``PyContextConfig`` and use it to instantiate a ``PyContext``:

.. code:: python

   from automata_docs.core.context.py_context.retriever_slim import PyContextConfig, PyContext
   from automata_docs.core.symbol.graph import SymbolGraph

   # Custom configuration
   config = PyContextConfig(spacer="    ", max_dependencies_to_process=5, max_related_symbols_to_process=5)

   # Load symbol graph (replace with actual symbol graph instance)
   graph = SymbolGraph()

   # Create PyContext using the custom configuration
   context = PyContext(graph=graph, config=config)

Follow-up Questions:
--------------------

-  Are there any performance issues when using a large value for
   ``max_dependencies_to_process`` and
   ``max_related_symbols_to_process``?
