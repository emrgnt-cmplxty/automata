PyDocWriter
===========

``PyDocWriter`` is a class designed to handle the automatic generation
of documentation for Python modules. It offers utility functions for
cleaning and preparing the content, as well as preparing the directory
structure for the generated documentation. This class is a tool to
automate the manual task and reduce the effort required to generate
readable and well-structured documentations.

Overview
--------

The primary purpose of the ``PyDocWriter`` class is to parse Python
files and generate corresponding RestructuredText (.rst) documentation
files. It provides functionalities including converting camel case to
snake case, checking if a string is in camel case, generating index
files, generating module summaries, and generating rst files.

Related Symbols
---------------

-  ``PyReader``: A utilitarian class for extracting syntax tree from
   python code.
-  ``DirectoryManager``: Handles operations related to directory
   manipulation like getting subdirectories, ensuring existence of a
   directory etc.
-  ``PyWriter``: A utility class for writing Python code along abstract
   syntax tree (AST) nodes.
-  ``Symbol``: A representation of Python classes, methods, or local
   variables.
-  ``PyReader``: Code retriever for fetching python source code and
   associated docstrings.

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
   from automata.code_handling.py.reader import PyReader
   from automata.ast_helpers.ast_utils.directory import DirectoryManager

Methods
-------

.. code:: python

   def __init__(self, base_path: str) -> None:
       self.base_path = base_path
       self.directory_manager = DirectoryManager(base_path)


   @staticmethod
   def check_camel_case(text: str) -> bool:
       return text != text.lower() and text != text.upper() and "_" not in text


   def generate_index_files(self, docs_dir: str) -> None:
       # Implementation...

   def generate_rst_files(self, docs: Dict[Symbol, SymbolDocEmbedding], symbols: List[Symbol], docs_dir: str) -> None:
       # Implementation...

   def write_documentation(self, docs: Dict[Symbol, SymbolDocEmbedding], symbols: List[Symbol], docs_dir: str) -> None:
       self.generate_rst_files(docs, symbols, docs_dir)
       self.generate_index_files(docs_dir)

Example Usage
-------------

.. code:: python

   from automata.code_handling.py.writer import PyDocWriter
   from typing import Dict, List
   from automata.symbol_embedding.base import SymbolDocEmbedding
   from automata.symbol.base import Symbol

   symbol1 = Symbol.from_string(symbol_str='package1 ClassA# method1().')
   symbol2 = Symbol.from_string(symbol_str='package2 ClassB# method2().')

   doc1 = SymbolDocEmbedding(symbol=symbol1, document='doc1', vector=np.array([1, 2, 3]))
   doc2 = SymbolDocEmbedding(symbol=symbol2, document='doc2', vector=np.array([4, 5, 6]))

   symbol_doc_pairs = {symbol1: doc1, symbol2: doc2}
   symbols = [symbol1, symbol2]

   py_doc_writer = PyDocWriter(base_path='/path/to/project')
   py_doc_writer.write_documentation(symbol_doc_pairs, symbols, docs_dir='/path/to/output')

Follow-up Questions
-------------------

-  What are the error handling mechanisms in PyDocWriter class methods?
-  Is there a way to customize the way PyDocWriter handles or formats
   the content of the documentation according to user preference?
-  How does PyDocWriter handle optional dependendencies like ‘pypandoc’
   if not present in the user’s environment?
-  What are the consequences of duplicated or repeated symbol keys for
   ‘write_documentation’ method? How can such a scenario be prevented?
-  How does PyDocWriter handle Python files that contain both underscore
   and camel case naming conventions?
-  Does the tool support generating documentation for private methods
   (those that start with underscore ’\_’) and how does it handle name
   mangling for private attributes/methods in Python?
-  Is the class designed to be used as part of any specific workflows
   for automating documentation generation? If so, how would a typical
   workflow look like?
