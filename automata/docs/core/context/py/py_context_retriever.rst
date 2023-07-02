PyContextRetriever
==================

``PyContextRetriever`` is a class used to retrieve the context of a
symbol in a Python project. It processes Python Abstract Syntax Trees
(ASTs) to provide information about the specified symbol, as well as
related symbols and dependencies. The class allows users to extract
import statements, docstrings, method definitions, and other relevant
information about the symbol.

Overview
--------

``PyContextRetriever`` is initialized with a ``SymbolGraph``, an
optional configuration ``PyContextRetrieverConfig``, and an optional
``VectorDatabaseProvider`` for document embeddings. It provides several
methods for processing and extracting context, such as
``process_symbol``, ``process_ast``, ``process_docstring``,
``process_imports``, and others.

The main method for processing a symbol is ``process_symbol``, which
takes in a symbol and an optional list of related symbols. It handles
building the context output and managing indentation levels with the
help of its ``IndentManager`` context manager. The output context can be
retrieved using the ``get_context_buffer`` method, which returns the
built context as a string.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.core.symbol.graph.SymbolGraph``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol.symbol_utils.convert_to_fst_object``
-  ``automata.core.symbol.symbol_utils.get_rankable_symbols``

Example
-------

The following example demonstrates how to use ``PyContextRetriever`` to
retrieve the context of a symbol from a given Python project:

.. code:: python

   from automata.core.symbol.graph import SymbolGraph
   from automata.core.retrievers.py.context import PyContextRetriever, PyContextRetrieverConfig
   from automata.core.symbol.base import Symbol

   # Load a SymbolGraph for the Python project
   symbol_graph = SymbolGraph(index_path="path/to/index_proto")

   # Initialize a PyContextRetriever
   config = PyContextRetrieverConfig(max_related_symbols_to_process=5, max_dependencies_to_process=5)
   retriever = PyContextRetriever(graph=symbol_graph, config=config)

   # Get a Symbol object for a specified dotpath
   symbol = Symbol.from_string("path.to.symbol")

   # Process the symbol and optionally provide a list of related symbols
   # (This example assumes there are ranked_symbols available)
   retriever.process_symbol(symbol, related_symbols=ranked_symbols)

   # Get the built context
   context = retriever.get_context_buffer()
   print(context)

Limitations
-----------

``PyContextRetriever`` relies on the provided ``SymbolGraph`` and the
structure of the Python project to retrieve symbol context. If the
``SymbolGraph`` is incomplete or the Python project contains irregular
structures, the retrieved context might be incomplete or misrepresented.

Another limitation is the performance when dealing with large Python
projects or when processing a high number of related symbols and
dependencies. The more symbols and dependencies to process, the slower
the context retrieval becomes.

Follow-up Questions:
--------------------

-  How can the performance be improved when dealing with a high number
   of related symbols and dependencies?
-  What strategies can be used to handle incomplete or irregular code
   structures in the Python project?
