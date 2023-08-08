PyReader
========

Overview
--------

The ``PyReader`` class is designed to fetch Python code from specified
modules, classes, or methods. It provides comprehensive tools for
scanning and extracting requested information, and supports a range of
operations including fetching source code, extracting docstrings, and
retrieving source code without docstrings for specified sections of
code.

The class also includes comparison operations and contains static
utility methods for extracting docstrings from specific AST nodes.

Related Symbols
---------------

-  ``automata.code_writers.py.py_code_writer.PyCodeWriter`` : A utility
   class for writing Python code along AST nodes
-  ``automata.tools.builders.py_reader_builder.PyReaderToolkitBuilder``:
   A builder for a toolkit associated with directly retrieving python
   code.
-  ``automata.symbol.symbol_parser.parse_symbol``: Parses a ``Symbol``
   given a ``Symbol`` URI.
-  ``automata.code_writers.py.py_code_writer.PyCodeWriter.__init__``:
   Initializer for PyCodeWriter.
-  ``automata.tools.builders.py_reader_builder.PyReaderToolkitBuilder.__init__``:
   Initializer for PyReaderToolkitBuilder.
-  ``automata.symbol.symbol_base.Symbol``: Base class for symbols.
-  ``automata.code_writers.py.py_doc_writer.PyDocWriter``: Class for
   writing documentation for Python modules.
-  ``automata.experimental.code_parsers.py.context_processing.context_retriever.ContextComponent``:
   Enum class representing context components.
-  ``automata.tools.tool_base.Tool``: Exposes a function or coroutine
   directly.
-  ``automata.eval.agent.code_writing_eval.CodeWritingAction``:
   Represents written code.

Example
-------

Below is an example of how to use the ``PyReader`` class to retrieve the
source code and docstring from a module.

.. code:: python

   from automata.code_parsers.py.py_reader import PyReader

   # Initialize the PyReader class
   pyreader = PyReader()

   # Get the source code from a specific module
   source_code = pyreader.get_source_code('sample_module')

   # Get the docstring of a specific class in a module
   docstring = pyreader.get_docstring('sample_module', 'SampleClass')

Limitations
-----------

While ``PyReader`` provides extensive functionality for extracting
Python code and metadata, it is reliant on the specific syntax tree
structure of Python and as such may not correctly interpret non-standard
or complex code structures.

Follow-up Questions:
--------------------

-  Is it possible to expand ``PyReader`` to account for non-standard
   Python structures?
-  How does ``PyReader`` handle errors or exceptions when the specified
   code cannot be found? Are there specific tools for debugging such
   situations with ``PyReader``?
