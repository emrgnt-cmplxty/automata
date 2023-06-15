PyContext
=========

``PyContext`` is used to retrieve the context of a symbol in a Python
project.

Overview
--------

``PyContext`` provides functionality to work with Python project symbols
and tools to easily navigate the project structure. Its main tasks
include retrieving context, related symbols, and dependencies for a
given Python project.

Import Statements
-----------------

.. code:: python

   import os
   from contextlib import contextmanager
   from typing import List, Optional, Set
   from redbaron import RedBaron
   from automata_docs.core.coding.py_coding.navigation import find_method_call_by_location
   from automata_docs.core.coding.py_coding.py_utils import build_repository_overview
   from automata_docs.core.coding.py_coding.retriever import PyCodeRetriever
   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.symbol.symbol_types import Symbol, SymbolDescriptor, SymbolReference
   from automata_docs.core.symbol.symbol_utils import convert_to_fst_object, get_rankable_symbols
   from automata_docs.core.utils import root_py_fpath

Initialization
--------------

To instantiate a ``PyContext`` object, you need to provide a
``SymbolGraph`` and an optional ``PyContextConfig`` object.

.. code:: python

   graph = SymbolGraph()
   config = PyContextConfig()
   pycontext = PyContext(graph, config)

Main Methods
------------

``PyContext`` provides several methods to work with symbols:

-  ``get_context_buffer()``: Returns the context buffer as a string.
-  ``process_ast()``: Processes the variables of a symbol.
-  ``process_docstring()``: Processes the docstring of a symbol.
-  ``process_headline()``: Processes the headline of a symbol.
-  ``process_imports()``: Processes the imports of a symbol.
-  ``process_message()``: Processes a message by appending indentation
   and adding it to the message.
-  ``process_method()``: Processes a specified method.
-  ``process_symbol()``: Process the context of a symbol. The output is
   stored in the local message buffer.
-  ``reset()``: Resets the retriever to its initial state.

Usage Example
-------------

.. code:: python

   from automata_docs.core.symbol.graph import SymbolGraph
   from automata_docs.core.context.py_context import PyContext
   from automata_docs.core.context.py_context_config import PyContextConfig

   graph = SymbolGraph()
   config = PyContextConfig()
   pycontext = PyContext(graph, config)

   # Get context of a symbol
   symbol = <some_symbol_instance>
   pycontext.process_symbol(symbol)

   # Retrieve context buffer
   context = pycontext.get_context_buffer()
   print(context)

Limitations and Follow-up Questions
-----------------------------------

-  What are some potential edge cases or limitations when working with
   symbols in ``PyContext``?
