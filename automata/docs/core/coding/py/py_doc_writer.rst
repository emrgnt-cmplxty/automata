PyDocWriter
===========

``PyDocWriter`` is a class to write documentation for Python modules. It
can generate reStructuredText (.rst) files for a given project, create
index files for each directory with .rst files, generate a summary for
each module, and includes capabilities to implement summary generation
from content.

Overview
--------

``PyDocWriter`` class provides the functionality to generate
documentation (in .rst format) for a given project by converting the
native markdown (.md) format to reStructuredText (.rst) format. This
class is useful when generating documentation for Python modules while
taking care of the different naming conventions (camel case and snake
case) used in the project. It also includes some utility methods, such
as converting camel case to snake case strings, checking if strings are
camel case, and generating index files and summaries for the project.

Related Symbols
---------------

-  ``automata.core.coding.py.reader.PyReader``
-  ``automata.core.coding.directory.DirectoryManager``
-  ``automata.core.symbol.base.Symbol``
-  ``automata.core.symbol_embedding.base.SymbolDocEmbedding``
-  ``type: ignore``

Example
-------

The following is an example demonstrating how to use ``PyDocWriter`` for
generating documentation for Python modules.

.. code:: python

   from automata.core.coding.py.writer import PyDocWriter

   base_path = "path/to/project"
   docs_dir = "path/to/docs"
   docs = {...}
   symbols = [...]

   py_doc_writer = PyDocWriter(base_path)
   py_doc_writer.write_documentation(docs, symbols, docs_dir)

Limitations
-----------

``PyDocWriter`` assumes certain directory structures and naming
conventions when generating documentation. It might not work well for
projects with unconventional layouts or names. The summary generation is
currently a placeholder method and needs to be implemented for its
intended use.

Follow-up Questions:
--------------------

-  Is the summary generation logic provided in the ``PyDocWriter`` class
   working as intended, or should it be replaced or extended with a
   custom implementation?
