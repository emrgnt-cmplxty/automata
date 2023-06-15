PyContextRetrieverConfig
========================

``PyContextRetrieverConfig`` is a configuration class for the
``PyContextRetriever``. It provides options for retrieving Python code
context, such as indentation settings, maximum depth for processing
dependencies, and the number of nearest related symbols to print.

Overview
--------

``PyContextRetrieverConfig`` allows users to customize the behavior of
the ``PyContextRetriever`` by setting different options like the string
used for indentation (``spacer``), the maximum number of dependencies to
process (``max_dependencies_to_process``), and the maximum number of
related symbols to process (``max_related_symbols_to_process``). These
options can be set while initializing the ``PyContextRetrieverConfig``
object.

Related Symbols
---------------

-  ``automata_docs.core.context.py_context.retriever_slim.PyContextConfig``
-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata_docs.core.context.py_context.retriever_slim.PyContext``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.coding.py_coding.writer.PyCodeWriter.__init__``
-  ``automata_docs.core.context.py_context.retriever.PyContextRetriever``

Example
-------

The following example demonstrates how to create an instance of
``PyContextRetrieverConfig`` with custom settings.

.. code:: python

   from automata_docs.core.context.py_context.retriever import PyContextRetrieverConfig

   config = PyContextRetrieverConfig(spacer="    ", max_dependencies_to_process=5, max_related_symbols_to_process=5)

Limitations
-----------

``PyContextRetrieverConfig`` provides a limited set of options to
configure the behavior of the ``PyContextRetriever``. It may not cover
all possible use cases or configurations required for a specific project
or purpose.

Follow-up Questions:
--------------------

-  Are the customization options provided by
   ``PyContextRetrieverConfig`` comprehensive for all possible
   scenarios?
