PyContextRetrieverConfig
========================

``PyContextRetrieverConfig`` is a configuration class that helps
configure the ``PyContextRetriever`` class for extracting context
information from Python projects.

Overview
--------

The ``PyContextRetrieverConfig`` class provides configuration options
for the ``PyContextRetriever`` class, which is used for retrieving
context information of symbols in a Python project. The
``PyContextRetrieverConfig`` class accepts 3 parameters: ``spacer``,
``max_dependencies_to_process``, and ``max_related_symbols_to_process``.

Related Symbols
---------------

-  ``automata_docs.core.context.py_context.retriever.PyContextRetriever``
-  ``automata_docs.tests.unit.test_py_code_retriever.getter``
-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata_docs.tests.unit.test_py_writer.python_writer``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.coding.py_coding.writer.PyCodeWriter``

Example
-------

The following is an example demonstrating how to create an instance of
``PyContextRetrieverConfig`` with custom settings.

.. code:: python

   from automata_docs.core.context.py_context.retriever import PyContextRetrieverConfig

   config = PyContextRetrieverConfig(
       spacer="    ",  # Custom spacer with 4 spaces instead of the default 2 spaces
       max_dependencies_to_process=5,  # Limit maximum number of dependencies to process
       max_related_symbols_to_process=5  # Limit maximum number of related symbols to process
   )

Limitations
-----------

``PyContextRetrieverConfig`` is specifically designed for the
``PyContextRetriever`` class and might not be suitable for other context
retriever implementations. Additionally, it has limited configuration
options, which might restrict the flexibility of configuring the context
retrieval process.

Follow-up Questions:
--------------------

-  Could the ``PyContextRetrieverConfig`` class be extended or
   refactored to support a broader range of context retrievers?
-  Are there any additional configuration options that could be
   beneficial for the ``PyContextRetriever`` class, and what impact
   would they have on the retrieval process?
