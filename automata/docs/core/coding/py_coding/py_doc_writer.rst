PyDocWriter
===========

``PyDocWriter`` is a class responsible for writing documentation for
Python modules. It provides methods for generating .rst (restructured
text) files for classes and methods, generating index files for a
directory, and generating a summary for a module by reading its .rst
files.

Overview
--------

The primary goal of ``PyDocWriter`` is to generate documentation for
Python modules. It does this by converting markdown documentation to
.rst files and generating index files for each directory containing .rst
files or subdirectories. Moreover, it generates module-level summaries
by reading the .rst files and using a language model to generate the
summary.

Related Symbols
---------------

-  ``automata.core.coding.py_coding.writer.PyDocWriter``
-  ``automata.tests.unit.sample_modules.sample.OuterClass``
-  ``automata.tests.unit.sample_modules.sample.OuterClass.InnerClass``
-  ``automata.core.coding.py_coding.writer.PyCodeWriter``
-  ``automata.core.coding.py_coding.retriever.PyCodeRetriever``
-  ``automata.core.symbol.symbol_types.SymbolDocEmbedding``

Example
-------

Below is a usage example for ``PyDocWriter``, assuming that you have
generated documentation using the appropriate symbols and directory
structure:

.. code:: python

   from automata.core.coding.py_coding.writer import PyDocWriter
   from automata.core.symbol.symbol_types import Symbol, SymbolDocEmbedding

   # Assuming you have the documentation info in the following variables:
   # - docs: a dictionary containing the {Symbol: SymbolDocEmbedding} pairs
   # - symbols: a list of symbols

   docs_dir = "docs_directory"  # the directory where you want the documentation to be written

   doc_writer = PyDocWriter("base_project_path")
   doc_writer.write_documentation(docs, symbols, docs_dir)

This example assumes you have already generated the ``docs`` and
``symbols`` objects. Please refer to the documentation of ``Symbol`` and
``SymbolDocEmbedding`` for information on generating these objects.

Limitations
-----------

``PyDocWriter`` assumes a specific directory structure for the project.
The class currently only supports the generation of .rst (restructured
text) files and assumes the project uses Sphinx as its documentation
tool. The current implementation will only convert strings from camel
case to snake case if they match a regular expression pattern, which may
not work for all naming conventions.

Follow-up Questions:
--------------------

-  What other file formats and documentation tools should be supported
   by ``PyDocWriter``?
-  Is there a more accurate way to identify camel case strings for
   conversion to snake case?
