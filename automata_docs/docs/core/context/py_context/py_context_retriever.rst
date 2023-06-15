PyContextRetriever
==================

``PyContextRetriever`` is a class used to retrieve the context of a
symbol in a Python project. It parses the Python source code and
extracts relevant information such as imports, class and method
docstrings, and method signatures. It helps in understanding and
documenting the behavior of specific symbols within a Python codebase.

Overview
--------

The main functionality of ``PyContextRetriever`` is provided through the
``process_symbol`` method, which processes the context of a symbol and
stores the output into a local message buffer. The retriever supports
handling primary symbols, related symbols, and their dependencies to
build a comprehensive context. It also allows configuration through the
``PyContextRetrieverConfig`` class to set indentation and limit the
number of related symbols and dependencies to process.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata_docs.core.context.py_context.retriever_slim.PyContextConfig``

Example
-------

Here is an example of how to use ``PyContextRetriever`` to retrieve the
context of a symbol:

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.context.py_context.retriever import PyContextRetriever, PyContextRetrieverConfig

   # ... Load or build the SymbolGraph ...
   symbol_graph = SymbolGraph()

   # Create an instance of PyContextRetriever
   config = PyContextRetrieverConfig()
   retriever = PyContextRetriever(graph=symbol_graph, config=config)

   # Retrieve the context of a specific symbol
   symbol = ...  # Load or find the symbol
   related_symbols = ...  # Load or find the related symbols
   retriever.process_symbol(symbol, related_symbols)

   # Get the context buffer
   context_buffer = retriever.get_context_buffer()
   print(context_buffer)

Limitations
-----------

``PyContextRetriever`` assumes that the provided ``SymbolGraph`` is
valid and contains all necessary information about the Python codebase.
It may not perform well with incomplete or invalid graphs. Also, it
relies on the ``redbaron`` library to parse the source code, which may
have limitations in handling some specific language constructs.

Follow-up Questions:
--------------------

-  Is there any specific need or customization for symbol context
   retrieval?
-  Are there any performance concerns while using ``PyContextRetriever``
   for larger projects?
