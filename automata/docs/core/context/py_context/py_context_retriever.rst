PyContextRetriever
==================

``PyContextRetriever`` is a class used to retrieve the context of a
symbol in a Python project. The retriever is capable of processing
abstract syntax tree (AST) nodes of classes, methods, and module-level
code to extract relevant information about the symbol. The
PyContextRetriever is useful for generating detailed documentation and
understanding the relationships between symbols in a codebase.

Overview
--------

``PyContextRetriever`` operates on a ``SymbolGraph`` and takes in a
configuration object ``PyContextRetrieverConfig``. With these inputs, it
offers several methods to process symbols, AST nodes of the methods and
class docstrings, and related symbols. The main entry point for
processing a symbol is the ``process_symbol`` method, which retrieves
the context and stores it in the local message buffer.

Related Symbols
---------------

-  ``automata_docs.core.symbol.graph.SymbolGraph``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_utils.convert_to_fst_object``

Usage Example
-------------

.. code:: python

   from automata_docs.core.context.py_context.retriever import PyContextRetriever
   from automata_docs.core.symbol.graph import SymbolGraph

   graph = SymbolGraph()
   py_context_retriever = PyContextRetriever(graph)
   symbol = some_symbol

   # Process the context of the symbol
   py_context_retriever.process_symbol(symbol)

   # Retrieve the context buffer
   context_buffer = py_context_retriever.get_context_buffer()

Limitations
-----------

``PyContextRetriever`` relies on the ``SymbolGraph`` and
``PyContextRetrieverConfig`` passed to it. It assumes that all symbols
are represented in the ``SymbolGraph`` and that the configuration values
are set correctly in the ``PyContextRetrieverConfig``. Inaccuracies or
errors in these inputs may lead to issues when processing symbols and
their relationships.

Follow-up Questions:
--------------------

-  What if symbol relationships in the ``SymbolGraph`` are not correctly
   defined?
-  How can we update or modify the ``PyContextRetrieverConfig`` after
   initializing the ``PyContextRetriever``?
