PyContextRetriever
==================

``PyContextRetriever`` is a class that retrieves the context of a symbol
from a Python project. It interacts with ``SymbolGraph``,
``VectorDatabaseProvider``, and ``tiktoken.Encoding`` objects to manage
and manipulate this context.

Overview
--------

``PyContextRetriever`` provides methods to manage indentation, process
import statements, docstrings, documentation, and methods for specific
symbols, and can reset its internal states to a default setting. The
context it retrieves for a particular symbol includes all related
symbols and dependencies, with a restriction on the maximum number of
each to process, specified in the config.

Related Symbols
---------------

-  ``automata.core.base.database.vector.VectorDatabaseProvider``
-  ``automata.code_handling.py.reader.PyReader``
-  ``automata.symbol.base.Symbol``
-  ``automata.symbol.graph.SymbolGraph``
-  ``automata.symbol.symbol_utils.convert_to_fst_object``
-  ``automata.symbol.symbol_utils.get_rankable_symbols``
-  ``automata.core.utils.get_root_py_fpath``

Example
-------

The following is an example demonstrating how to use
``PyContextRetriever`` to retrieve the context of a symbol from a Python
project.

.. code:: python

   from automata.retrievers.py.context import PyContextRetriever
   from automata.symbol.graph import SymbolGraph
   from automata.symbol.base import Symbol

   graph = SymbolGraph(index_path="my_index_path")
   symbol = Symbol.from_string(symbol_str="my_symbol")

   context_retriever = PyContextRetriever(graph=graph)
   context_retriever.process_symbol(symbol=symbol)

Limitations
-----------

``PyContextRetriever`` is dependent on the ``SymbolGraph`` and the
``VectorDatabaseProvider`` objects for many of its operations. This can
limit its usability in scenarios where these objects are not accessible
or not as comprehensive as required. Moreover, its comprehensive context
retrieval can be limited by the number of symbols specified in the
config.

Follow-up Questions:
--------------------

-  Is it possible to modify the process of retrieving context as per
   some user-defined guidelines?
-  How does the context retrieval fail in scenarios where the
   ``SymbolGraph`` or ``VectorDatabaseProvider`` is not up to date?
-  How does ``PyContextRetriever`` decide which symbols are important
   enough to fetch while trying not to exceed the maximum number
   specified in the config?
