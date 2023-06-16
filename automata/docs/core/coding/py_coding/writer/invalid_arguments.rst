PyCodeWriter
============

``PyCodeWriter`` is a utility class responsible for writing Python code
along with the Abstract Syntax Tree (AST) nodes. It interacts with a
``PyCodeRetriever`` instance to write and update Python source code
files. The class offers methods to create new Python modules, update
existing modules with new code, and delete specific code from an
existing module.

Related Symbols
---------------

-  ``automata.core.coding.directory.DirectoryManager``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata.core.symbol.symbol_types.Symbol``
-  ``automata.core.symbol.symbol_types.SymbolDocEmbedding``

Import Statements
-----------------

.. code:: python

   import logging
   import os
   import re
   import subprocess
   import numpy as np
   import pypandoc
   from typing import Dict, List, Optional, Union, cast
   from redbaron import ClassNode, DefNode, Node, NodeList, RedBaron
   from automata.core.coding.directory import DirectoryManager
   from automata.core.coding.py_coding.navigation import (
       find_all_function_and_class_syntax_tree_nodes,
       find_import_syntax_tree_node_by_name,
       find_import_syntax_tree_nodes,
       find_syntax_tree_node,
   )
   from automata.core.coding.py_coding.retriever import PyCodeRetriever
   from automata.core.symbol.symbol_types import Symbol, SymbolDocEmbedding

Example
-------

The following example demonstrates how to use ``PyCodeWriter`` to
create, update, and write to a Python module.

.. code:: python

   from automata.tests.unit.test_py_writer import python_writer, MockCodeGenerator

   # Create a mock code generator
   mock_generator = MockCodeGenerator(
       has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
   )
   source_code = mock_generator.generate_code()

   # Instantiate a PythonWriter with a PyCodeRetriever
   py_writer = python_writer()

   # Create a new Python module with the generated source code
   py_writer.create_new_module("sample_module", source_code, do_write=True)

   # Update the existing Python module with new source code
   new_generator = MockCodeGenerator(
       has_class=True, has_class_docstring=True, has_function=True, has_function_docstring=True
   )
   new_source_code = new_generator.generate_code()
   py_writer.update_existing_module(
       source_code=new_source_code, module_dotpath="sample_module", do_write=True
   )

Limitations
-----------

``PyCodeWriter`` relies on the directory structure provided by
``DirectoryManager``. It cannot create or update Python source code
files that are outside of the directory specified in the ``base_path``
used to initialize ``DirectoryManager``. Additionally, ``PyCodeWriter``
handles only Python source code files and cannot be used for other
programming languages or file types.

Follow-up Questions:
--------------------

-  What is the role of ``PyCodeWriter`` in writing documentation for
   Python modules?
-  How does ``PyCodeWriter`` handle different code styles or formatting?
