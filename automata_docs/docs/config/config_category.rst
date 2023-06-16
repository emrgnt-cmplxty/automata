ConfigCategory
==============

``ConfigCategory`` is an enumeration class that corresponds to the names
of folders holding config files. It provides a way to easily reference
the names of these folders and prevent typos when working with
configurations.

Related Symbols
---------------

-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator``
-  ``automata_docs.tests.unit.sample_modules.sample.EmptyClass``
-  ``automata_docs.cli.commands.cli``
-  ``automata_docs.core.context.py_context.retriever.PyContextRetrieverConfig``
-  ``automata_docs.tests.unit.test_py_writer.MockCodeGenerator.generate_code``
-  ``automata_docs.tests.unit.test_py_code_retriever.test_build_overview``
-  ``automata_docs.tests.unit.sample_modules.sample_module_2.ObNMl``
-  ``automata_docs.tests.unit.sample_modules.sample_module_2.ObNMl.method``
-  ``automata_docs.core.symbol.graph.SymbolGraph``

Example
-------

Here’s an example of how to use the ``ConfigCategory`` enumeration:

.. code:: python

   from automata_docs.config.config_enums import ConfigCategory

   config_name = ConfigCategory.PROMPT
   print(config_name.value)

This will output:

::

   prompt

In this example, the value of the ``PROMPT`` enumeration member is
printed, which is the name of the related configuration folder.

Limitations
-----------

The primary limitation of ``ConfigCategory`` is that it assumes a
specific directory structure for configuration folders and does not
allow for custom folder naming conventions. It can only represent the
config folder names that are defined within the enumeration class.

Follow-up Questions:
--------------------

-  How can we include custom directory structures for configuration
   files with ``ConfigCategory``?
-  Are there any sort of aliases or additional validation that should be
   included within the enumeration?
