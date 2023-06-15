PyDocWriter
===========

``PyDocWriter`` is a class that generates documentation for Python
modules. It provides functionalities to convert camel case strings to
snake case, check if a string is camel case, generate index files,
module summaries, and individual reStructuredText (rst) files, and write
the full documentation with given symbols and directory.

Overview
--------

The main functionalities of the ``PyDocWriter`` class include generating
rst files from given symbols and their respective documentations and
generating index files and summaries for the documentation. It can also
manipulate strings to check for camel case and convert from camel case
to snake case. It relies on other classes like ``DirectoryManager`` and
``PyCodeRetriever`` for handling directories and getting relevant
information from the Python code.

Related Symbols
---------------

-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata_docs.core.symbol.symbol_types.Symbol``
-  ``automata_docs.core.symbol.symbol_types.SymbolDocEmbedding``
-  ``automata_docs.core.coding.directory.DirectoryManager``
-  ``automata_docs.core.coding.py_coding.retriever.PyCodeRetriever``

Example
-------

Here is an example of using ``PyDocWriter`` to generate documentation:

.. code:: python

   from automata_docs.core.coding.py_coding.writer import PyDocWriter
   from automata_docs.core.symbol.symbol_types import Symbol, SymbolDocEmbedding

   base_path = "path/to/project"
   doc_dir = "path/to/docs"

   pydoc_writer = PyDocWriter(base_path)

   # Mocked data
   docs = {Symbol(): SymbolDocEmbedding()}
   symbols = [Symbol()]

   # Generate documentation
   pydoc_writer.write_documentation(docs, symbols, doc_dir)

Limitations
-----------

The main limitation of ``PyDocWriter`` is that it assumes a specific
directory structure for the documentation files and does not allow
customization for the generated output format. It also does not
currently support summary generation out-of-the-box, requiring
developers to implement their own summary generation function.

Follow-up Questions:
--------------------

-  Can we include custom formats or templates for generating
   documentation output?
-  How to best implement the summary generation function for the
   module-level summaries?
